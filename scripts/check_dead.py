#!/usr/bin/env python3
"""Report domains in src/domains.txt that no longer resolve.

This is informational only — a domain that fails DNS may be temporarily down,
geo-blocked, or only used by an app's API. Maintainers should verify before removing.
Writes a Markdown report to stdout (and to $GITHUB_STEP_SUMMARY when run in Actions).
"""

import os
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from build import SRC, parse  # noqa: E402

socket.setdefaulttimeout(5)


def resolves(domain):
    try:
        socket.getaddrinfo(domain, None)
        return True
    except (socket.gaierror, OSError):
        return False


def main():
    _, entries = parse(SRC)
    domains = [d for _, d, _ in entries]
    with ThreadPoolExecutor(max_workers=16) as pool:
        dead = [d for d, ok in zip(domains, pool.map(resolves, domains)) if not ok]

    lines = [f"## Dead domain check", "", f"Checked {len(domains)} domains, {len(dead)} did not resolve.", ""]
    lines += [f"- `{d}`" for d in dead]
    report = "\n".join(lines) + "\n"

    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
