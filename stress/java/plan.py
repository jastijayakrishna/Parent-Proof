#!/usr/bin/env python3
"""Prints the jobs of a Java stress run as a JSON list (a CI matrix):
plan.py SET ONLY MODES. SET is dev, holdout, regression or all (or a comma
list); ONLY a comma list of project names (empty: every project of the set);
MODES a comma list of history and scan. Each project's `shards` says how many
jobs share each mode's windows."""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(here, "projects.json"), encoding="utf-8"))
sets = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] else ["dev"]
only = [x for x in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if x]
modes = (sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "history,scan").split(",")
jobs = []
for p in cfg["projects"]:
    if "all" not in sets and p["set"] not in sets:
        continue
    if only and p["name"] not in only:
        continue
    for mode in modes:
        n = int(p.get("shards", {}).get(mode, 0))
        for i in range(1, n + 1):
            jobs.append({"project": p["name"], "mode": mode, "shard": f"{i}/{n}", "jdk": p["jdk"]})
print(json.dumps(jobs))
