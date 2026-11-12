"""Detect bursts of failed logins and successful logins after a failure burst in offline JSONL logs."""
import argparse
from collections import defaultdict, deque
from datetime import datetime
import ipaddress
import json
from pathlib import Path

def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timestamps must include a UTC offset')
    return result

def analyze(events, threshold=3, window_seconds=60):
    if threshold < 1 or window_seconds < 1:
        raise ValueError('threshold and window must be positive')
    parsed = []
    for event in events:
        if event['status'] not in {'failure', 'success'}:
            raise ValueError('status must be failure or success')
        parsed.append((timestamp(event['timestamp']), str(ipaddress.ip_address(event['ip'])), str(event['user']), event['status']))
    failures = defaultdict(deque)
    alerts = []
    # Sort once: exports do not always preserve event order.
    for time, ip, user, status in sorted(parsed, key=lambda row: row[0]):
        bucket = failures[(ip, user)]
        while bucket and (time - bucket[0]).total_seconds() > window_seconds:
            bucket.popleft()
        if status == 'failure':
            bucket.append(time)
            if len(bucket) == threshold:
                alerts.append(dict(kind='failure_burst', ip=ip, user=user, timestamp=time.isoformat(), count=len(bucket)))
        else:
            if len(bucket) >= threshold:
                alerts.append(dict(kind='success_after_burst', ip=ip, user=user, timestamp=time.isoformat(), count=len(bucket)))
            bucket.clear()
    return alerts

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--threshold', type=int, default=3)
    parser.add_argument('--window', type=int, default=60)
    args = parser.parse_args()
    try:
        events = [json.loads(line) for line in args.input.read_text(encoding='utf-8').splitlines() if line.strip()]
        print(json.dumps(analyze(events, args.threshold, args.window), indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'error: {exc}\n')

if __name__ == '__main__':
    main()
