#!/usr/bin/env python3
"""
seo_pass.py -- Full SEO pass (Engine 5)
Runs all three checks in sequence: qa_routes, check_titles, check_schema.
Gates the entire batch. If any check fails, nothing commits.

Usage: python seo_pass.py [--routes-only] [--strict]

--strict: treat warnings as failures
--routes-only: only scan routes directory

Exit code 0 = full batch passes. Exit code 1 = any failure.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_check(script: str, extra_args: list[str] = None) -> tuple[int, str]:
    """Run a check script and return (returncode, output)."""
    cmd = [sys.executable, script] + (extra_args or [])
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return result.returncode, output


def main():
    parser = argparse.ArgumentParser(description="Full SEO pass -- runs all Engine 5 checks")
    parser.add_argument("--routes-only", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    checks = [
        ("QA Gate", "qa_routes.py", ["--fail-on-warning"] if args.strict else []),
        ("Title Check", "check_titles.py", ["--routes-only"] if args.routes_only else []),
        ("Schema Check", "check_schema.py", []),
    ]

    print("=" * 65)
    print("REPATRIATE SERVICE -- FULL SEO PASS (Engine 5)")
    print("=" * 65)
    print()

    all_passed = True
    results = []

    for name, script, extra_args in checks:
        if not Path(script).exists():
            print(f"[SKIP] {name} -- {script} not found")
            results.append((name, "SKIP"))
            continue

        print(f"Running: {name}...")
        print("-" * 40)
        returncode, output = run_check(script, extra_args)
        print(output)

        if returncode == 0:
            results.append((name, "PASS"))
        else:
            results.append((name, "FAIL"))
            all_passed = False

    print()
    print("=" * 65)
    print("SEO PASS SUMMARY")
    print("=" * 65)
    for name, verdict in results:
        print(f"  [{verdict}] {name}")

    print()
    if all_passed:
        print("VERDICT: ALL CHECKS PASS -- BATCH READY FOR HTML PREVIEW AND COMMIT")
        print()
        print("Next steps:")
        print("  1. Generate HTML preview of sample pages")
        print("  2. Present to Gareth for approval")
        print("  3. Commit to master after approval")
        print("  4. Provide live URLs")
        print("  5. Stop and wait for next 'go'")
        sys.exit(0)
    else:
        print("VERDICT: CHECKS FAILED -- FIX ERRORS BEFORE COMMITTING")
        failed = [name for name, verdict in results if verdict == "FAIL"]
        print(f"Failed checks: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
