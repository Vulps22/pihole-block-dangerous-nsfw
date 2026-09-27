#!/usr/bin/env python3
"""Validate src/domains.txt and build the blocklists in dist/.

Usage:
    python3 scripts/build.py           # validate, then build dist/
    python3 scripts/build.py --check   # validate only (used by CI on PRs)
    python3 scripts/build.py --fix     # sort + de-duplicate src files in place, then build
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "domains.txt"
ALLOW = ROOT / "src" / "allowlist.txt"
DIST = ROOT / "dist"

TITLE = "AI Character Blocklist"
HOMEPAGE = "https://github.com/Vulps22/pihole-block-ai-character-rp"
DESCRIPTION = "Blocks AI character creation, roleplay and companion services."

LABEL = r"(?!-)[a-z0-9-]{1,63}(?<!-)"
DOMAIN_RE = re.compile(rf"^(?:{LABEL}\.)+[a-z]{{2,63}}$|^(?:{LABEL}\.)+xn--[a-z0-9-]{{1,59}}$")


def parse(path):
    """Return (header_lines, entries) where entries is a list of (lineno, domain, note)."""
    header, entries = [], []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            if not entries:
                header.append(raw)
            continue
        domain, _, note = line.partition("#")
        entries.append((lineno, domain.strip(), note.strip()))
    return header, entries


def validate(path, entries):
    errors = []
    seen = {}
    prev = None
    for lineno, domain, _ in entries:
        where = f"{path.relative_to(ROOT)}:{lineno}"
        if domain != domain.lower():
            errors.append(f"{where}: '{domain}' must be lowercase")
        if " " in domain or "\t" in domain:
            errors.append(f"{where}: '{domain}' contains whitespace (one domain per line)")
        elif not DOMAIN_RE.match(domain.lower()):
            errors.append(f"{where}: '{domain}' is not a valid domain (no URLs, paths, wildcards or IPs)")
        if domain in seen:
            errors.append(f"{where}: '{domain}' is a duplicate of line {seen[domain]}")
        else:
            seen[domain] = lineno
        if prev is not None and domain < prev:
            errors.append(f"{where}: '{domain}' is out of order (should come before '{prev}')")
        prev = domain
    return errors


def fix(path, header, entries):
    unique = {}
    for _, domain, note in entries:
        domain = domain.lower()
        if domain not in unique or (note and not unique[domain]):
            unique[domain] = note
    lines = list(header)
    if lines and lines[-1].strip():
        lines.append("")
    for domain in sorted(unique):
        lines.append(f"{domain}  # {unique[domain]}" if unique[domain] else domain)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(domains):
    DIST.mkdir(exist_ok=True)
    meta = [
        f"Title: {TITLE}",
        f"Description: {DESCRIPTION}",
        f"Homepage: {HOMEPAGE}",
        f"Entries: {len(domains)}",
    ]
    outputs = {
        # Plain domains: Pi-hole (v5/v6), Technitium, NextDNS etc. Exact-match only.
        "domains.txt": ("# ", domains),
        # Hosts file: anything that reads /etc/hosts-style lists.
        "hosts.txt": ("# ", [f"0.0.0.0 {d}" for d in domains]),
        # Adblock syntax: Pi-hole v6, AdGuard Home, uBlock Origin. Also blocks subdomains.
        "adblock.txt": ("! ", [f"||{d}^" for d in domains]),
    }
    for name, (comment, body) in outputs.items():
        text = "\n".join([comment + m for m in meta] + [""] + body) + "\n"
        (DIST / name).write_text(text, encoding="utf-8")
    print(f"Built {len(outputs)} lists with {len(domains)} domains in {DIST.relative_to(ROOT)}/")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate only, do not write dist/")
    mode.add_argument("--fix", action="store_true", help="sort and de-duplicate source files before building")
    args = parser.parse_args()

    if args.fix:
        for path in (SRC, ALLOW):
            fix(path, *parse(path))

    _, block = parse(SRC)
    _, allow = parse(ALLOW)
    errors = validate(SRC, block) + validate(ALLOW, allow)

    allowed = {d for _, d, _ in allow}
    for lineno, domain, _ in block:
        if domain in allowed:
            errors.append(f"src/domains.txt:{lineno}: '{domain}' is in src/allowlist.txt")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"\n{len(errors)} problem(s) found. Try `python3 scripts/build.py --fix` for ordering/duplicates.", file=sys.stderr)
        return 1

    print(f"OK: {len(block)} domains, {len(allow)} allowlisted")
    if not args.check:
        build([d for _, d, _ in block])
    return 0


if __name__ == "__main__":
    sys.exit(main())
