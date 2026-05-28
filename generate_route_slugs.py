#!/usr/bin/env python3
"""
generate_route_slugs.py
Generates all 38,612 country-to-country route slugs from data/countries-197.json.

Usage:
    python3 generate_route_slugs.py
    python3 generate_route_slugs.py --format csv
    python3 generate_route_slugs.py --format txt

Output files:
    data/route-slugs.json  (default)
    data/route-slugs.csv
    data/route-slugs.txt   (one slug per line)
"""

import json
import csv
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
COUNTRIES_FILE = SCRIPT_DIR / "data" / "countries-197.json"

def load_countries():
    with open(COUNTRIES_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data["countries"]

def generate_combinations(countries):
    slugs = [c["slug"] for c in countries]
    names = {c["slug"]: c["name"] for c in countries}
    iso2  = {c["slug"]: c["iso2"] for c in countries}
    combos = []
    for o in slugs:
        for d in slugs:
            if o != d:
                combos.append({
                    "route_slug":        f"{o}-to-{d}",
                    "url":               f"/repatriation/{o}-to-{d}/",
                    "origin_slug":       o,
                    "origin_name":       names[o],
                    "origin_iso2":       iso2[o],
                    "destination_slug":  d,
                    "destination_name":  names[d],
                    "destination_iso2":  iso2[d],
                })
    return combos

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["json","csv","txt"], default="json")
    args = parser.parse_args()

    countries = load_countries()
    combos = generate_combinations(countries)
    n = len(combos)
    print(f"Generated {n:,} route combinations from {len(countries)} countries")

    out_dir = SCRIPT_DIR / "data"
    out_dir.mkdir(exist_ok=True)

    if args.format == "json":
        out_path = out_dir / "route-slugs.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {"total": n, "countries": len(countries)},
                "routes": combos
            }, f, separators=(",", ":"))
        print(f"Written: {out_path}  ({out_path.stat().st_size/1024:.0f} KB)")

    elif args.format == "csv":
        out_path = out_dir / "route-slugs.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["route_slug","url","origin_slug","origin_name","origin_iso2","destination_slug","destination_name","destination_iso2"])
            w.writeheader()
            w.writerows(combos)
        print(f"Written: {out_path}  ({out_path.stat().st_size/1024:.0f} KB)")

    elif args.format == "txt":
        out_path = out_dir / "route-slugs.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            for c in combos:
                f.write(c["route_slug"] + "\n")
        print(f"Written: {out_path}  ({out_path.stat().st_size/1024:.0f} KB)")

if __name__ == "__main__":
    main()
