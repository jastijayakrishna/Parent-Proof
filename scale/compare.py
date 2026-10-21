#!/usr/bin/env python3
"""Compares two binaries on the scale test's recorded upgrades (not part of
the pre-registered count): the decisions of the test itself
(scale/results/history, binary bin/VERSION) and a decision-only rerun
(scale/after/LABEL, scripts/decide.sh), each judged by the same frozen
compiler answers. Prints the counts for both and every upgrade whose answer
for the build moved.

usage: compare.py LABEL"""
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score  # noqa: E402

label = sys.argv[1]


def load(root):
    out = {}
    for f in sorted(glob.glob(os.path.join(root, "*", "*", "results-*.jsonl"))):
        d = os.path.dirname(f)
        suite, consumer = os.path.normpath(d).split(os.sep)[-2:]
        canary = score.canary_of(d)
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            w, o = r.get("window", {}), r.get("observed") or {}
            out[(suite, consumer, w.get("bump", ""))] = {
                "pins": f"{w.get('old_pin', '')} -> {w.get('new_pin', '')}",
                "compiler": score.trusted((w.get("oracle") or {}).get("outcome", "not judged"), canary),
                "build": (o.get("aspects") or {}).get("source_build", ""), "verdict": o.get("verdict", "ERROR"),
                "reasons": o.get("unknown_reasons") or [], "where": (o.get("evidence") or [""])[0], "error": o.get("error", "")}
    return out


def tally(rows):
    c = collections.Counter()
    for r in rows:
        if r["compiler"] == "breaks":
            c["broke"] += 1
            c[{"NO_GO": "caught", "UNKNOWN": "needs review on a break", "GO": "MISSED"}.get(r["build"], "error")] += 1
        elif r["compiler"] == "compiles":
            c["safe"] += 1
            c[{"NO_GO": "false alarm", "UNKNOWN": "needs review on safe", "GO": "merge on safe"}.get(r["build"], "error")] += 1
        if r["verdict"] == "ERROR" or r["error"]:
            c["errors"] += 1
    return c


before = load("scale/results/history")
after = load(os.path.join("scale/after", label))
diag = {k: v for k, v in after.items() if k[0].endswith("-gomodule")}
after = {k: v for k, v in after.items() if not k[0].endswith("-gomodule")}
common = sorted(set(before) & set(after))
print(f"# Before and after on the scale test's upgrades ({label})\n")
print(f"{len(common)} upgrades decided by both ({len(before)} by the test, {len(after)} by the rerun).\n")
tb, ta = tally(before[k] for k in common), tally(after[k] for k in common)
keys = ["broke", "caught", "needs review on a break", "MISSED", "safe", "merge on safe", "false alarm", "needs review on safe", "errors"]
print("| | " + " | ".join(keys) + " |")
print("|---|" + "---|" * len(keys))
print("| before | " + " | ".join(str(tb[k]) for k in keys) + " |")
print("| after | " + " | ".join(str(ta[k]) for k in keys) + " |\n")
moved = [k for k in common if before[k]["build"] != after[k]["build"]]
print(f"## {len(moved)} upgrades whose answer for the build moved\n")
print("| contract -> project | upgrade | compiler | before | after | after: why |")
print("|---|---|---|---|---|---|")
word = score.WORD
for k in sorted(moved, key=lambda k: (before[k]["compiler"] != "breaks", k)):
    b, a = before[k], after[k]
    why = a["where"] if a["build"] == "NO_GO" else ", ".join(a["reasons"][:3])
    print(f"| {k[0]} -> {k[1]} | {b['pins'][:70]} | {b['compiler']} | {word.get(b['build'], b['build'])} | {word.get(a['build'], a['build'])} | {str(why)[:110]} |")
if diag:
    print("\n## Diagnostic suites (the provider given another way)\n")
    for k in sorted(diag):
        r = diag[k]
        print(f"- {k[0]} -> {k[1]} {r['pins'][:60]}: compiler {r['compiler']}, build {word.get(r['build'], r['build'])}, overall {word.get(r['verdict'], r['verdict'])} {', '.join(r['reasons'][:3])}")
    td = tally(diag.values())
    print("\n" + ", ".join(f"{k} {td[k]}" for k in keys if td[k]))
