"""Six offline teaching experiments; standard library, no network or disk writes.

Not an AWS emulator. Route priority only models unequal CIDR prefix lengths.
SQLite atomicity covers local DB effects, not external service side effects.
"""

import hashlib
import ipaddress
import json
import math
import sqlite3
from decimal import Decimal


def longest_prefix(address, routes):
    destination = ipaddress.ip_address(address)
    candidates = []
    for cidr, target in routes:
        network = ipaddress.ip_network(cidr)
        if network.version == destination.version and destination in network:
            candidates.append((network.prefixlen, target))
    if not candidates:
        return None
    best_length = max(length for length, _ in candidates)
    winners = [target for length, target in candidates if length == best_length]
    if len(winners) != 1:
        raise ValueError("Equal-prefix priority is outside this teaching model")
    return winners[0]


def queue_history(initial, arrivals, capacity):
    if initial < 0 or capacity < 0 or any(value < 0 for value in arrivals):
        raise ValueError("Counts must be nonnegative")
    backlog = initial
    rows = []
    for second, incoming in enumerate(arrivals, start=1):
        available = backlog + incoming
        completed = min(available, capacity)
        backlog = available - completed
        rows.append((second, incoming, completed, backlog))
    return rows


def drain_time(backlog, arrival_rate, service_rate):
    if min(backlog, arrival_rate, service_rate) < 0:
        raise ValueError("Rates and backlog must be nonnegative")
    if backlog == 0:
        return 0.0
    if service_rate <= arrival_rate:
        return math.inf
    return backlog / (service_rate - arrival_rate)


def nearest_rank(values, percentile):
    if not values or not 0 < percentile <= 100:
        raise ValueError("Need observations and 0 < percentile <= 100")
    if any(not math.isfinite(value) for value in values):
        raise ValueError("Observations must be finite")
    ordered = sorted(values)
    return ordered[math.ceil(percentile / 100 * len(ordered)) - 1]


def cost(fixed, per_request, requests):
    if requests < 0:
        raise ValueError("Requests must be nonnegative")
    return Decimal(fixed) + Decimal(per_request) * Decimal(requests)


def break_even(fixed_a, variable_a, fixed_b, variable_b):
    denominator = Decimal(variable_a) - Decimal(variable_b)
    if denominator == 0:
        return None
    result = (Decimal(fixed_b) - Decimal(fixed_a)) / denominator
    return result if result >= 0 else None


def new_database():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE results (job_id TEXT PRIMARY KEY, fingerprint TEXT, result TEXT)"
    )
    return connection


def persist_once(connection, job_id, payload, crash_before_commit=False):
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
    result = json.dumps({"score": sum(payload["features"]), "version": payload["version"]})
    with connection:
        existing = connection.execute(
            "SELECT fingerprint, result FROM results WHERE job_id = ?", (job_id,)
        ).fetchone()
        if existing:
            if existing[0] != fingerprint:
                raise ValueError("Job ID reused with different payload")
            return "duplicate", json.loads(existing[1])
        connection.execute("INSERT INTO results VALUES (?, ?, ?)", (job_id, fingerprint, result))
        if crash_before_commit:
            raise RuntimeError("Simulated exception before commit")
    return "created", json.loads(result)


def retry_delays(retries, base, cap, fractions):
    if retries < 0 or base < 0 or cap < 0 or len(fractions) < retries:
        raise ValueError("Invalid retry configuration")
    if any(not 0 <= value <= 1 for value in fractions[:retries]):
        raise ValueError("Jitter fractions must be in [0, 1]")
    return [min(cap, base * 2**attempt) * fractions[attempt] for attempt in range(retries)]


def main():
    print("1. Longest prefix")
    routes = [("0.0.0.0/0", "default"), ("10.20.0.0/16", "peer"), ("10.20.5.0/24", "inspection")]
    for ip in ("10.20.5.12", "10.20.8.12", "8.8.8.8"):
        print(ip, longest_prefix(ip, routes))

    print("\n2. Queue (second, arrivals, completed, remaining)")
    for row in queue_history(0, [8, 8, 20, 20, 0, 0], 10):
        print(row)
    print("drain 1200 with arrival 8/service 12:", drain_time(1200, 8, 12))

    print("\n3. Tail latency")
    latencies = [100] * 95 + [3000] * 5
    print("mean", sum(latencies) / len(latencies), "p95", nearest_rank(latencies, 95), "p99", nearest_rank(latencies, 99))

    print("\n4. Hypothetical costs, not AWS prices")
    print("break-even requests:", break_even("20", ".000002", "2", ".000008"))
    for requests in (1000000, 3000000, 5000000):
        print(requests, cost("20", ".000002", requests), cost("2", ".000008", requests))

    print("\n5. Atomic local result recording")
    db = new_database()
    payload = {"features": [1, 2, 3], "version": "v1"}
    try:
        persist_once(db, "job-1", payload, crash_before_commit=True)
    except RuntimeError:
        print("before commit failure: rows", db.execute("SELECT COUNT(*) FROM results").fetchone()[0])
    print(persist_once(db, "job-1", payload))
    print("redelivery after committed result:", persist_once(db, "job-1", payload))
    db.close()

    print("\n6. Retry timing; no actual sleeping")
    print("without jitter", retry_delays(5, 1, 8, [1] * 5))
    print("worker A", retry_delays(5, 1, 8, [.2, .8, .4, .6, .3]))
    print("worker B", retry_delays(5, 1, 8, [.9, .1, .7, .2, .8]))


if __name__ == "__main__":
    main()
