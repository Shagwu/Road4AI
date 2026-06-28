#!/usr/bin/env python3
"""
Drift monitoring agent — reads Hermes checkpoints, calculates variance,
alerts on threshold breaches. Zero API calls, local only.

Usage:
    # Run drift check
    python tools/drift_monitor.py check --social-voice 0.94 --memory-ops 0.91

    # Watch mode (check every 60s)
    python tools/drift_monitor.py watch --interval 60

    # Watch checkpoint file
    python tools/drift_monitor.py watch --checkpoint reports/skillopt/orchestration/latest.json

    # Watch with scoring script
    python tools/drift_monitor.py watch --script tools/get_scores.py

    # Show baseline
    python tools/drift_monitor.py baseline

    # Show status
    python tools/drift_monitor.py status

    # Show history
    python tools/drift_monitor.py history

    # Show alerts
    python tools/drift_monitor.py alerts
"""

import argparse
import json
import sys
import time
import signal
from pathlib import Path
from datetime import datetime, timezone


# Watch mode globals
_running = True

def _signal_handler(sig, frame):
    global _running
    _running = False
    print("\nStopping watch mode...")



BASELINE_FILE = Path("state/drift_baseline_v2p1.json")
DRIFT_LOG = Path("state/drift_log.jsonl")
DRIFT_ALERTS = Path("state/drift_alerts.jsonl")
DRIFT_HALT = Path("state/drift_halts.jsonl")

ALERT_THRESHOLD = 0.05  # ±5%
HALT_THRESHOLD = 0.10   # ±10%


class DriftMonitor:
    def __init__(self, baseline_path: Path = BASELINE_FILE):
        self.baseline = self._load_baseline(baseline_path)
        self.alert_threshold = ALERT_THRESHOLD
        self.halt_threshold = HALT_THRESHOLD

    def _load_baseline(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Baseline file not found: {path}")
        return json.loads(path.read_text())

    def calculate_variance(self, current_score: float, baseline_score: float) -> float:
        """Return variance as percentage of baseline."""
        return abs(current_score - baseline_score) / baseline_score

    def check_drift(self, domain: str, current_score: float, current_tier: str = "green") -> tuple:
        """
        Returns (status, action, reason)
        status: 'green' | 'yellow' | 'blue'
        action: 'auto-store' | 'alert' | 'halt'
        reason: human-readable
        """
        baseline_score = self.baseline["domains"][domain]["score"]
        baseline_tier = self.baseline["domains"][domain]["confidence_tier"]

        variance = self.calculate_variance(current_score, baseline_score)

        # Variance check
        if variance > self.halt_threshold:
            return ('blue', 'halt', f'{domain} variance {variance:.2%} exceeds halt threshold (±10%)')
        elif variance > self.alert_threshold:
            return ('yellow', 'alert', f'{domain} variance {variance:.2%} exceeds alert threshold (±5%)')

        # Tier check
        if baseline_tier == "green" and current_tier != "green":
            return ('yellow', 'alert', f'{domain} tier demoted: {baseline_tier} → {current_tier}')

        return ('green', 'auto-store', f'{domain} within tolerance')

    def cross_domain_correlation(self, social_voice_score: float, memory_ops_score: float) -> float:
        """Simple correlation check — are both domains drifting in the same direction?"""
        sv_baseline = self.baseline["domains"]["social_voice"]["score"]
        mo_baseline = self.baseline["domains"]["memory_ops"]["score"]

        sv_variance = self.calculate_variance(social_voice_score, sv_baseline)
        mo_variance = self.calculate_variance(memory_ops_score, mo_baseline)

        # If both variance in same direction and similar magnitude, assume high correlation
        if (sv_variance * mo_variance) > 0 and abs(sv_variance - mo_variance) < 0.03:
            return 0.7  # High correlation
        elif abs(sv_variance) > 0.05 or abs(mo_variance) > 0.05:
            return 0.4  # Low correlation (drifting independently)
        else:
            return 0.8  # Both stable

    def run_check(self, checkpoint_data: dict) -> dict:
        """
        Takes orchestration checkpoint JSON, returns drift report.
        """
        report = {
            'timestamp': checkpoint_data.get('timestamp', datetime.now(timezone.utc).isoformat()),
            'domain_checks': [],
            'cross_domain': {},
            'overall_status': 'green',
            'human_action_needed': False
        }

        for domain_data in checkpoint_data['domains']:
            domain = domain_data['name']
            status, action, reason = self.check_drift(
                domain,
                domain_data['score'],
                domain_data.get('confidence_tier', 'green')
            )
            report['domain_checks'].append({
                'domain': domain,
                'status': status,
                'action': action,
                'reason': reason,
                'current_score': domain_data['score'],
                'variance': self.calculate_variance(domain_data['score'], self.baseline['domains'][domain]['score'])
            })

            # Track overall status (blue > yellow > green)
            if status == 'blue':
                report['overall_status'] = 'blue'
                report['human_action_needed'] = True
            elif status == 'yellow' and report['overall_status'] != 'blue':
                report['overall_status'] = 'yellow'
                report['human_action_needed'] = True

        # Cross-domain correlation
        sv_score = next((d['score'] for d in checkpoint_data['domains'] if d['name'] == 'social_voice'), 0.95)
        mo_score = next((d['score'] for d in checkpoint_data['domains'] if d['name'] == 'memory_ops'), 0.915)
        corr = self.cross_domain_correlation(sv_score, mo_score)

        report['cross_domain']['correlation'] = corr
        if corr < 0.4:
            report['cross_domain']['status'] = 'blue'
            report['human_action_needed'] = True
            report['overall_status'] = 'blue'
        elif corr < 0.6:
            report['cross_domain']['status'] = 'yellow'
            report['human_action_needed'] = True
        else:
            report['cross_domain']['status'] = 'green'

        return report

    def log_result(self, report: dict) -> None:
        """Log drift check result to appropriate file."""
        DRIFT_LOG.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            'timestamp': report['timestamp'],
            'overall_status': report['overall_status'],
            'human_action_needed': report['human_action_needed'],
            'domain_checks': report['domain_checks'],
            'cross_domain': report['cross_domain']
        }

        with open(DRIFT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")

        if report['overall_status'] == 'yellow':
            alert_entry = {
                'timestamp': report['timestamp'],
                'severity': 'yellow',
                'reason': next((c['reason'] for c in report['domain_checks'] if c['status'] == 'yellow'), 'Unknown'),
                'domains_affected': [c['domain'] for c in report['domain_checks'] if c['status'] == 'yellow'],
                'action_required': 'Review and approve next run',
                'decision_by': None,
                'decision_reason': None
            }
            with open(DRIFT_ALERTS, "a") as f:
                f.write(json.dumps(alert_entry) + "\n")

        elif report['overall_status'] == 'blue':
            halt_entry = {
                'timestamp': report['timestamp'],
                'severity': 'blue',
                'reason': next((c['reason'] for c in report['domain_checks'] if c['status'] == 'blue'), 'Unknown'),
                'domains_affected': [c['domain'] for c in report['domain_checks'] if c['status'] == 'blue'],
                'action_required': 'STOP — investigate before resuming',
                'root_cause_investigation': {
                    'hypothesis': None,
                    'check_performed': None,
                    'finding': None
                },
                'resolution': None,
                'decision_by': None,
                'approved_to_continue': False
            }
            with open(DRIFT_HALT, "a") as f:
                f.write(json.dumps(halt_entry) + "\n")


def show_history(limit: int = 10) -> None:
    """Show recent drift check history."""
    if not DRIFT_LOG.exists():
        print("No drift history found.")
        return

    lines = DRIFT_LOG.read_text().splitlines()
    recent = lines[-limit:]

    print(f"\n=== Drift History (last {len(recent)} checks) ===")
    for line in recent:
        entry = json.loads(line)
        ts = entry['timestamp'][:16]
        status = entry['overall_status']
        marker = {'green': '✓', 'yellow': '⚠', 'blue': '✗'}.get(status, '?')
        print(f"  {marker} {ts} — {status.upper()}")
        for check in entry.get('domain_checks', []):
            print(f"    {check['domain']}: {check['variance']:.2%}")


def show_alerts(limit: int = 10) -> None:
    """Show recent drift alerts."""
    if not DRIFT_ALERTS.exists():
        print("No alerts found.")
        return

    lines = DRIFT_ALERTS.read_text().splitlines()
    recent = lines[-limit:]

    print(f"\n=== Drift Alerts (last {len(recent)}) ===")
    for line in recent:
        entry = json.loads(line)
        ts = entry['timestamp'][:16]
        print(f"  ⚠ {ts} — {entry['severity'].upper()}")
        print(f"    Reason: {entry['reason']}")
        print(f"    Domains: {', '.join(entry['domains_affected'])}")
        print(f"    Action: {entry['action_required']}")


def show_status() -> None:
    """Show current drift monitoring status."""
    monitor = DriftMonitor()

    print("\n=== Drift Monitoring Status ===")
    print(f"\nBaseline: {monitor.baseline['baseline_date']}")
    print(f"Domains:")
    for domain, data in monitor.baseline['domains'].items():
        print(f"  {domain}: {data['score']} (±{data['variance_observed']:.0%}) — {data['confidence_tier']}")

    # Count recent incidents
    alerts = 0
    halts = 0
    if DRIFT_ALERTS.exists():
        alerts = len(DRIFT_ALERTS.read_text().splitlines())
    if DRIFT_HALT.exists():
        halts = len(DRIFT_HALT.read_text().splitlines())

    print(f"\nIncidents:")
    print(f"  Alerts (yellow): {alerts}")
    print(f"  Halts (blue): {halts}")

    if DRIFT_LOG.exists():
        total = len(DRIFT_LOG.read_text().splitlines())
        print(f"  Total checks: {total}")


def watch_mode(interval: int, checkpoint: str = None, script: str = None) -> None:
    """Run drift checks on an interval."""
    global _running

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    monitor = DriftMonitor()
    check_count = 0

    print(f"=== Drift Watch Mode ===")
    print(f"Interval: {interval}s")
    if checkpoint:
        print(f"Watching checkpoint: {checkpoint}")
    elif script:
        print(f"Running script: {script}")
    print("Press Ctrl+C to stop\n")

    while _running:
        check_count += 1
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            if script:
                # Run external script to get scores
                import subprocess
                result = subprocess.run(
                    ["python3", script],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode != 0:
                    print(f"Script failed: {result.stderr[:100]}")
                    time.sleep(interval)
                    continue

                # Parse script output (expect JSON with social_voice and memory_ops scores)
                scores = json.loads(result.stdout)
                checkpoint_data = {
                    'timestamp': timestamp,
                    'domains': [
                        {'name': 'social_voice', 'score': scores['social_voice'], 'confidence_tier': 'green'},
                        {'name': 'memory_ops', 'score': scores['memory_ops'], 'confidence_tier': 'green'}
                    ]
                }
            elif checkpoint:
                # Check if checkpoint file changed
                checkpoint_path = Path(checkpoint)
                if not checkpoint_path.exists():
                    print(f"[{check_count}] {timestamp[:19]} — checkpoint file not found")
                    time.sleep(interval)
                    continue

                checkpoint_data = json.loads(checkpoint_path.read_text())
                checkpoint_data['timestamp'] = timestamp
            else:
                # Demo mode with simulated scores (for testing)
                import random
                checkpoint_data = {
                    'timestamp': timestamp,
                    'domains': [
                        {'name': 'social_voice', 'score': 0.95 + random.uniform(-0.02, 0.02), 'confidence_tier': 'green'},
                        {'name': 'memory_ops', 'score': 0.915 + random.uniform(-0.02, 0.02), 'confidence_tier': 'green'}
                    ]
                }

            report = monitor.run_check(checkpoint_data)
            monitor.log_result(report)

            # Compact output
            status = report['overall_status']
            marker = {'green': '✓', 'yellow': '⚠', 'blue': '✗'}.get(status, '?')
            sv_var = next((c['variance'] for c in report['domain_checks'] if c['domain'] == 'social_voice'), 0)
            mo_var = next((c['variance'] for c in report['domain_checks'] if c['domain'] == 'memory_ops'), 0)

            print(f"[{check_count}] {timestamp[:19]} — {marker} {status.upper()} (sv:{sv_var:.1%} mo:{mo_var:.1%})")

            # Stop on blue (halt)
            if status == 'blue':
                print(f"\n✗ HALT — Blue status detected. Stopping watch mode.")
                print(f"  Reason: {next((c['reason'] for c in report['domain_checks'] if c['status'] == 'blue'), 'Unknown')}")
                return 1

        except Exception as e:
            print(f"[{check_count}] {timestamp[:19]} — ERROR: {str(e)[:50]}")

        time.sleep(interval)

    print(f"\nWatch mode stopped after {check_count} checks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="drift",
        description="Drift Monitoring Agent — Multi-Domain Orchestration v2.1"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # check command
    check_parser = subparsers.add_parser("check", help="Run drift check")
    check_parser.add_argument("--checkpoint", help="Path to checkpoint JSON file")
    check_parser.add_argument("--social-voice", type=float, help="Social voice score")
    check_parser.add_argument("--memory-ops", type=float, help="Memory ops score")

    # baseline command
    subparsers.add_parser("baseline", help="Show current baseline")

    # status command
    subparsers.add_parser("status", help="Show monitoring status")

    # history command
    history_parser = subparsers.add_parser("history", help="Show drift history")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of entries to show")

    # alerts command
    alerts_parser = subparsers.add_parser("alerts", help="Show drift alerts")
    alerts_parser.add_argument("--limit", type=int, default=10, help="Number of entries to show")

    # watch command
    watch_parser = subparsers.add_parser("watch", help="Run drift checks on interval")
    watch_parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds (default: 60)")
    watch_parser.add_argument("--checkpoint", help="Watch checkpoint file for changes")
    watch_parser.add_argument("--script", help="Run script to get scores (must output JSON with social_voice, memory_ops)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "baseline":
        monitor = DriftMonitor()
        print(json.dumps(monitor.baseline, indent=2))
        return 0

    if args.command == "status":
        show_status()
        return 0

    if args.command == "history":
        show_history(args.limit)
        return 0

    if args.command == "alerts":
        show_alerts(args.limit)
        return 0

    if args.command == "watch":
        return watch_mode(args.interval, args.checkpoint, args.script)

    if args.command == "check":
        monitor = DriftMonitor()

        if args.checkpoint:
            checkpoint_data = json.loads(Path(args.checkpoint).read_text())
        elif args.social_voice is not None and args.memory_ops is not None:
            checkpoint_data = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'domains': [
                    {'name': 'social_voice', 'score': args.social_voice, 'confidence_tier': 'green'},
                    {'name': 'memory_ops', 'score': args.memory_ops, 'confidence_tier': 'green'}
                ]
            }
        else:
            print("Error: Provide --checkpoint or --social-voice and --memory-ops")
            return 1

        report = monitor.run_check(checkpoint_data)
        monitor.log_result(report)

        # Print summary
        print(f"\n=== Drift Check: {report['overall_status'].upper()} ===")
        for check in report['domain_checks']:
            print(f"  {check['domain']}: {check['status']} (variance: {check['variance']:.2%}) — {check['reason']}")
        print(f"  Cross-domain correlation: {report['cross_domain']['correlation']:.2f} ({report['cross_domain']['status']})")
        if report['human_action_needed']:
            print(f"\n⚠ Human action required")
        else:
            print(f"\n✓ All clear — auto-store to Hermes")

        return 1 if report['overall_status'] == 'blue' else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
