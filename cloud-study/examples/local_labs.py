"""Offline teaching examples. No AWS access, file writes, or extra packages."""

from ipaddress import ip_network


def subnet_capacity(cidr):
    network = ip_network(cidr)
    if network.version != 4 or not 16 <= network.prefixlen <= 28:
        raise ValueError("Use an ordinary AWS IPv4 subnet, /16 through /28")
    return network.num_addresses, network.num_addresses - 5


def process_once(results, job_id, value):
    if job_id in results:
        if results[job_id]["input"] != value:
            raise ValueError("Same job ID with a different input")
        return "duplicate", results[job_id]["output"]
    output = value * 2
    results[job_id] = {"input": value, "output": output}
    return "created", output


def cached_value(cache, key, now, ttl, loader):
    if ttl <= 0:
        raise ValueError("TTL must be positive")
    if key in cache and now < cache[key]["expires"]:
        return "hit", cache[key]["value"]
    value = loader()
    cache[key] = {"value": value, "expires": now + ttl}
    return "miss", value


class TransientError(Exception):
    pass


def retry(operation, attempts):
    if attempts < 1:
        raise ValueError("At least one attempt is required")
    for attempt in range(1, attempts + 1):
        try:
            return operation(), attempt
        except TransientError:
            if attempt == attempts:
                raise


def main():
    print("LAB 1: total addresses, ordinary AWS usable addresses")
    for cidr in ("10.0.1.0/24", "10.0.2.0/26"):
        print(cidr, subnet_capacity(cidr))

    print("\nLAB 2: single-process idempotency")
    results = {}
    for job_id, value in (("job-1", 3), ("job-2", 4), ("job-1", 3)):
        print(job_id, process_once(results, job_id, value))
    print("stored jobs:", len(results))

    print("\nLAB 3: TTL with simulated time")
    cache = {}
    for now in (0, 5, 11):
        print(now, cached_value(cache, ("v1", 3), now, 10, lambda: 6))

    print("\nLAB 4: transient failures only")
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise TransientError("Try again")
        return "success"

    print(retry(operation, 3))


if __name__ == "__main__":
    main()
