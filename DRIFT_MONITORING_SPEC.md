# Drift Monitoring Spec

## Overview

Drift monitoring tracks multi-domain orchestration health by comparing current scores against locked baselines. Zero API calls, local only.

## Baseline

Locked in `state/drift_baseline_v2p1.json`:

| Domain | Score | Variance | Tier |
|--------|-------|----------|------|
| social_voice | 0.950 | ±3% | green |
| memory_ops | 0.915 | ±2% | green |

Cross-domain correlation baseline: 0.8

## Thresholds

- **Green** (auto-store): variance ≤ ±5%
- **Yellow** (alert): variance > ±5% — investigate, human review required
- **Blue** (halt): variance > ±10% — stop, root cause investigation before resuming

## Components

### Core Monitor (`tools/drift_monitor.py`)

Commands:
- `check --social-voice 0.94 --memory-ops 0.91` — run single check
- `watch --interval 60` — continuous monitoring (demo/simulated mode)
- `watch --checkpoint <file>` — watch checkpoint file for changes
- `watch --script <script>` — run external script for scores
- `baseline` — show locked baseline
- `status` — show monitoring status and incident counts
- `history` — show drift check history
- `alerts` — show yellow alerts

### Daily Check (`tools/daily_drift_check.py`)

Runs once per day, logs to state files:
```
python tools/daily_drift_check.py
python tools/daily_drift_check.py --dry-run
```

### Hermes Checkpoint (`tools/drift_hermes_checkpoint.py`)

Generates `[hermes-context]` block for git commits:
```
python tools/drift_hermes_checkpoint.py
python tools/drift_hermes_checkpoint.py --print-only
```

### Harvester Hook (`tools/harvester_drift_hook.py`)

Routes harvester signals through confidence tiering:
- `--gate-check` — is harvesting allowed?
- --signal '{...}'` — route signal (≥0.8 auto-store, 0.5-0.8 queue, <0.5 discard)
- `--pause "reason"` / `--resume "reason"` — manual override

## State Files

| File | Purpose |
|------|---------|
| `state/drift_baseline_v2p1.json` | Locked baseline scores |
| `state/drift_log.jsonl` | All drift check results |
| `state/drift_alerts.jsonl` | Yellow alerts |
| `state/drift_halts.jsonl` | Blue halts |
| `state/harvester_gate.json` | Harvester pause/resume state |

## Scheduling

macOS launchd runs daily at 09:00 UTC:
```
bash config/install_drift_schedule.sh install
bash config/install_drift_schedule.sh status
bash config/install_drift_schedule.sh uninstall
```

Logs: `state/drift-cron.log`, `state/drift-cron-error.log`

## Slack Notifications

Set `SLACK_WEBHOOK_URL` in `.env` to enable. Notifications sent on yellow/blue status.

## Governance

- Protected files (SkillOpt cannot touch): `AGENTS.md`, `docs/brand-voice.md`, `state/current-queue.json`, operating contracts
- Drift monitor itself is read-only — it logs but never auto-corrects
- Blue halt requires human investigation and explicit resume before harvesting continues
