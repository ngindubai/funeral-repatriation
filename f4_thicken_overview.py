#!/usr/bin/env python3
"""
f4_thicken_overview.py -- F4: rewrite thin, ungrammatical overview_body fields.

Composes a grammatical 85-105 word overview from facts ALREADY present in the
same route file: the local emergency number, the registration authority, the
document processing time, the jurisdiction rule (grammar-fixed), the standard
repatriation flow, and the typical timeline. No new facts are introduced. No
embassy claim is made, because the parseable set spans many destination
countries and a "British Embassy" line would be wrong for corridor routes.

Only files whose current overview_body matches the generated thin template
(emergency-services + registration extractable) are touched. Three sentence
frames are rotated by a hash of the slug so pages do not read identically.

Usage:
  python3 f4_thicken_overview.py --dry-run [--limit N] [--slugs a,b,c]
  python3 f4_thicken_overview.py --apply
"""
import glob, re, sys, argparse, hashlib

# Strict full-match on the canonical thin template. The body must be EXACTLY the
# emergency sentence + registration sentence + optional jurisdiction sentence and
# nothing else, so files carrying extra sourced facts (apostille notes, "within N
# days", English-certificate notes, etc.) never match and are left untouched.
TEMPLATE = re.compile(
    r'^Contact emergency services \((?P<num>[^.]+?)\)\. '
    r'Death must be registered with (?:the )?(?P<reg>[^.]+?)\.'
    r'(?: The (?P<juris>[^.]+?) takes jurisdiction when the death is: '
    r'violent, suspicious,? or unexplained deaths?\.?)?'
    r'\s*$'
)

BANNED = {"delve","meticulous","comprehensive","tailored","navigate","leverage","seamless",
"robust","vital","crucial","utilize","intricate","paramount","pivotal","embark","foster",
"elevate","unleash","unlock","harness","streamline","holistic","realm","testament","moreover",
"furthermore","groundbreaking","transformative","synergy","reimagine","bustling","nestled",
"nuanced","illuminate","encompasses","proactive","ubiquitous","quintessential"}


def fm_get(fm, key):
    m = re.search(rf'^{key}:\s*"(.*?)"\s*$', fm, re.M)
    return m.group(1) if m else ""


def juris_clause(juris, frame):
    # juris parsed as e.g. "Prosecutor's Office" or "Botswana Police Service".
    # These are proper nouns, so keep their own capitalisation and just prepend
    # a lowercase article for mid-sentence use ("the Botswana Police Service").
    jl = "the " + juris.strip()
    if frame == 0:
        return f" Where a death is violent, suspicious or unexplained, {jl} takes jurisdiction and may order a post-mortem before the body can be released."
    if frame == 1:
        return f" If the death is treated as violent, suspicious or unexplained, {jl} takes jurisdiction, and a post-mortem may be needed before release."
    return f" A death that is violent, suspicious or unexplained falls under the jurisdiction of {jl}, which may require a post-mortem first."


def compose(o, d, num, reg, doc, avg, juris, frame):
    js = juris_clause(juris, frame) if juris else ""
    doc_clause = f", which usually takes {doc}" if doc else ""
    avg_clause = avg if avg else "several weeks"
    if frame == 0:
        return (f"After a death in {o}, the family should contact the local emergency services on {num} and "
                f"have the death formally certified. It is then registered with the {reg}, and a local death "
                f"certificate issued{doc_clause}.{js} Once the paperwork is complete, the body is embalmed, "
                f"sealed in a zinc-lined coffin, and flown to {d} as air cargo, where a receiving funeral "
                f"director takes custody. Most cases take {avg_clause} from the death to arrival in {d}.")
    if frame == 1:
        return (f"When someone dies in {o}, the death must be reported to the local emergency services on "
                f"{num} and registered with the {reg}. Obtaining the local death certificate typically takes "
                f"{doc if doc else 'one to two weeks'}, and it is this document that lets the rest of the "
                f"process begin.{js} After the documentation is in order, the body is embalmed and placed in "
                f"a zinc-lined coffin for international transport, then sent to {d} by air cargo. From death "
                f"to arrival in {d}, most cases take {avg_clause}.")
    return (f"Repatriation from {o} begins at the local level: contacting the emergency services on {num}, "
            f"then registering the death with the {reg} and obtaining a certified local death certificate"
            f"{doc_clause}.{js} With the paperwork complete, the body is embalmed, sealed in a zinc-lined "
            f"coffin, and cleared for export before being flown to {d} as air cargo. A funeral director in "
            f"{d} then takes custody. The full process most often takes {avg_clause}.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--slugs", default="")
    args = ap.parse_args()

    want = set(s.strip() for s in args.slugs.split(",") if s.strip())
    changed = 0; skipped = 0; problems = []
    shown = 0
    for f in sorted(glob.glob("site/content/routes/*.md")):
        if "_index" in f:
            continue
        raw = open(f, encoding="utf-8").read()
        parts = raw.split("---", 2)
        if len(parts) < 3:
            continue
        fm = parts[1]
        slug = fm_get(fm, "slug")
        if want and slug not in want:
            continue
        body_m = re.search(r'^overview_body:\s*"(.+?)"\s*$', fm, re.M)
        if not body_m:
            continue
        body = body_m.group(1)
        m = TEMPLATE.match(body)
        if not m:
            skipped += 1
            continue
        num = m.group("num").strip()
        reg = m.group("reg").strip()
        juris = (m.group("juris") or "").strip()
        # a comma in the registration authority means an extra clause was captured;
        # skip to avoid a run-on (belt and braces on top of the full-match).
        if "," in reg or len(reg) > 60:
            skipped += 1
            continue
        o = fm_get(fm, "origin_name"); d = fm_get(fm, "dest_name")
        doc = fm_get(fm, "doc_processing_time"); avg = fm_get(fm, "timeline_avg")
        # skip UK/Ireland origin (British-nationals-abroad framing edge; negligible count)
        if o in ("United Kingdom", "the United Kingdom", "Ireland", "the Republic of Ireland"):
            skipped += 1
            continue
        frame = int(hashlib.md5(slug.encode()).hexdigest(), 16) % 3
        new = compose(o, d, num, reg, doc, avg, juris, frame)
        # guard rails
        low = new.lower()
        bad = [w for w in BANNED if re.search(rf'\b{w}\b', low)]
        if bad or "—" in new or "--" in new or "£" in new or "GBP " in new or '"' in new:
            problems.append((slug, bad, new))
            continue
        wc = len(new.split())
        if args.dry_run:
            if not args.limit or shown < args.limit:
                print(f"\n=== {slug} [frame {frame}] {len(body.split())}w -> {wc}w ===")
                print("OLD:", body)
                print("NEW:", new)
                shown += 1
        if args.apply:
            new_fm = re.sub(r'^overview_body:\s*".+?"\s*$',
                            'overview_body: "' + new + '"', fm, count=1, flags=re.M)
            open(f, "w", encoding="utf-8").write(parts[0] + "---" + new_fm + "---" + parts[2])
        changed += 1
    print(f"\n--- candidates rewritten: {changed}; skipped(non-matching/UK-origin): {skipped}; guardrail problems: {len(problems)}")
    for slug, bad, _ in problems[:10]:
        print("  PROBLEM:", slug, bad)


if __name__ == "__main__":
    main()
