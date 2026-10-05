#!/usr/bin/env python3
"""Prints one setting of a project of stress/java/projects.json:
cfg.py NAME KEY[.KEY]. A list prints space-separated; a missing key prints
nothing."""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
projects = json.load(open(os.path.join(here, "projects.json"), encoding="utf-8"))["projects"]
v = next(x for x in projects if x["name"] == sys.argv[1])
for k in sys.argv[2].split("."):
    v = v.get(k, "") if isinstance(v, dict) else ""
print(" ".join(v) if isinstance(v, list) else v)
