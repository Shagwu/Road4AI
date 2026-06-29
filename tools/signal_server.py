#!/usr/bin/env python3
"""
Signal Server — Agent-to-Agent protocol for harvester signals.

Other agents request signals, we search Twitter, extract, gate-check, and return.

Usage:
    # Start signal server (file-based protocol)
    python tools/signal_server.py serve

    # Request signals (called by other agents)
    python tools/signal_server.py request --query "AI agents" --limit 5 --requester codex

    # Check request status
    python tools/signal_server.py status --request-id <id>

    # Read response
    python tools/signal_server.py response --request-id <id>

    # List pending requests
    python tools/signal_server.py pending

    # Get recent signals (last N)
    python tools/signal_server.py recent --limit 10

Protocol:
    1. Agent writes request to state/signal_requests/<id>.json
    2. Harvester picks up request, processes it
    3. Response written to state/signal_responses/<id>.json
    4. Agent reads response

    All files are JSON. Request includes query, limit, requester, timestamp.
    Response includes signals, gate status, summary.
"""

import argparse
import json
import sys
import os
import uuid
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvester_pipeline import run_twitter_search, extract_signals
from harvester_drift_hook import gate_check, process_signal, load_gate

REQUESTS_DIR = Path("state/signal_requests")
RESPONSES_DIR = Path("state/signal_responses")
SIGNAL_LOG = Path("state/signal_log.jsonl")


def ensure_dirs():
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)


def create_request(query: str, limit: int, requester: str, domain: str = "social_voice") -> dict:
    """Create a signal request."""
    ensure_dirs()
    request_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]

    request = {
        "id": request_id,
        "query": query,
        "limit": limit,
        "requester": requester,
        "domain": domain,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "processed_at": None,
        "response_id": None
    }

    request_path = REQUESTS_DIR / f"{request_id}.json"
    request_path.write_text(json.dumps(request, indent=2) + "\n")

    return request


def process_request(request: dict) -> dict:
    """Process a signal request through the harvester pipeline."""
    # Gate check
    gate = gate_check()
    if not gate["allowed"]:
        return {
            "request_id": request["id"],
            "status": "blocked",
            "gate_status": gate["gate_status"],
            "reason": gate.get("reason", "Gate closed"),
            "signals": [],
            "summary": {"total": 0, "auto_store": 0, "queue_review": 0, "discard": 0},
            "processed_at": datetime.now(timezone.utc).isoformat()
        }

    # Twitter search
    tweets = run_twitter_search(request["query"], request["limit"])
    if not tweets:
        return {
            "request_id": request["id"],
            "status": "no_data",
            "gate_status": gate["gate_status"],
            "signals": [],
            "summary": {"total": 0, "auto_store": 0, "queue_review": 0, "discard": 0},
            "processed_at": datetime.now(timezone.utc).isoformat()
        }

    # Extract signals
    signals = extract_signals(tweets, request["query"])

    # Route through drift gate
    routed = []
    actions = {"auto-store": 0, "queue-for-review": 0, "discard": 0}
    for signal in signals:
        result = process_signal(signal)
        routed.append({
            "tweet_id": signal.get("tweet_id", ""),
            "author": signal.get("author", ""),
            "text": signal.get("text", "")[:200],
            "confidence": signal.get("confidence", 0),
            "action": result.get("action", "unknown"),
            "domain": signal.get("domain", "social_voice"),
            "engagement": signal.get("engagement", {})
        })
        action = result.get("action", "unknown")
        if action in actions:
            actions[action] += 1

    return {
        "request_id": request["id"],
        "status": "complete",
        "gate_status": gate["gate_status"],
        "signals": routed,
        "summary": {
            "total": len(routed),
            "auto_store": actions["auto-store"],
            "queue_review": actions["queue-for-review"],
            "discard": actions["discard"]
        },
        "processed_at": datetime.now(timezone.utc).isoformat()
    }


def save_response(response: dict) -> Path:
    """Save response to file."""
    ensure_dirs()
    response_path = RESPONSES_DIR / f"{response['request_id']}.json"
    response_path.write_text(json.dumps(response, indent=2) + "\n")

    # Also log to signal_log.jsonl
    log_entry = {
        "request_id": response["request_id"],
        "status": response["status"],
        "summary": response["summary"],
        "processed_at": response["processed_at"]
    }
    with open(SIGNAL_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return response_path


def update_request_status(request_id: str, status: str, response_id: str = None):
    """Update request file with status."""
    request_path = REQUESTS_DIR / f"{request_id}.json"
    if request_path.exists():
        request = json.loads(request_path.read_text())
        request["status"] = status
        request["processed_at"] = datetime.now(timezone.utc).isoformat()
        if response_id:
            request["response_id"] = response_id
        request_path.write_text(json.dumps(request, indent=2) + "\n")


def handle_request(query: str, limit: int, requester: str, domain: str = "social_voice") -> dict:
    """Full request cycle: create → process → save → return."""
    # Create request
    request = create_request(query, limit, requester, domain)
    print(f"Request created: {request['id']}")

    # Process
    print(f"Processing: query='{query}' limit={limit} requester={requester}")
    response = process_request(request)

    # Save response
    response_path = save_response(response)
    update_request_status(request["id"], "complete", response["id"] if "id" in response else response["request_id"])

    print(f"Response saved: {response_path}")
    return response


def list_pending():
    """List pending requests."""
    ensure_dirs()
    pending = []
    for f in sorted(REQUESTS_DIR.glob("*.json")):
        request = json.loads(f.read_text())
        if request.get("status") == "pending":
            pending.append(request)
    return pending


def get_response(request_id: str) -> dict:
    """Get response for a request."""
    response_path = RESPONSES_DIR / f"{request_id}.json"
    if response_path.exists():
        return json.loads(response_path.read_text())
    return {"error": "Response not found"}


def get_recent(limit: int = 10) -> list:
    """Get recent signal log entries."""
    if not SIGNAL_LOG.exists():
        return []
    lines = SIGNAL_LOG.read_text().splitlines()
    entries = [json.loads(line) for line in lines[-limit:]]
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Signal Server — Agent-to-Agent harvester protocol")
    sub = parser.add_subparsers(dest="command")

    # request
    req = sub.add_parser("request", help="Request signals from harvester")
    req.add_argument("--query", required=True, help="Twitter search query")
    req.add_argument("--limit", type=int, default=5, help="Number of tweets")
    req.add_argument("--requester", required=True, help="Requesting agent name")
    req.add_argument("--domain", default="social_voice", help="Signal domain")

    # status
    stat = sub.add_parser("status", help="Check request status")
    stat.add_argument("--request-id", required=True)

    # response
    resp = sub.add_parser("response", help="Read response")
    resp.add_argument("--request-id", required=True)

    # pending
    sub.add_parser("pending", help="List pending requests")

    # recent
    rec = sub.add_parser("recent", help="Recent signal log")
    rec.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.command == "request":
        response = handle_request(args.query, args.limit, args.requester, args.domain)
        print(json.dumps(response, indent=2))
        return 0

    if args.command == "status":
        request_path = REQUESTS_DIR / f"{args.request_id}.json"
        if request_path.exists():
            print(json.dumps(json.loads(request_path.read_text()), indent=2))
        else:
            print(f"Request not found: {args.request_id}")
        return 1

    if args.command == "response":
        response = get_response(args.request_id)
        print(json.dumps(response, indent=2))
        return 0 if "error" not in response else 1

    if args.command == "pending":
        pending = list_pending()
        if pending:
            print(json.dumps(pending, indent=2))
        else:
            print("No pending requests")
        return 0

    if args.command == "recent":
        recent = get_recent(args.limit)
        if recent:
            print(json.dumps(recent, indent=2))
        else:
            print("No signal history")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
