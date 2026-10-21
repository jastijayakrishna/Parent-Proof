#!/usr/bin/env python3
"""Scale test probe (scale/PREREG.md): for each pair of scale/candidates.json
in part i/n, count the consumer's real upgrades of the provider module since
2023-01-01 from its go.mod history (first parent), without running the
verifier. Writes scale/probe/<suite>__<consumer>.json.

usage: scale_probe.py i/n"""
import json
import os
import re
import subprocess
import sys

SINCE = "2023-01-01"


def git(d, *a, check=True):
    r = subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr[-400:]}")
    return r.stdout


def version(gomod, module):
    """The version the build uses: a same-path replace wins over require."""
    if gomod is None:
        return None
    q = re.escape(module)
    rep = re.search(r"^\s*(?:replace\s+)?" + q + r"(?:\s+v\S+)?\s+=>\s+(\S+)\s+(v\S+)\s*$", gomod, re.M)
    if rep and rep.group(1) == module:
        return rep.group(2)
    if rep:
        return "replaced:" + rep.group(1) + "@" + rep.group(2)
    req = re.search(r"^\s*(?:require\s+)?" + q + r"\s+(v[^\s/]+)", gomod, re.M)
    return req.group(1) if req else None


def main():
    i, n = map(int, sys.argv[1].split("/"))
    cands = json.load(open("scale/candidates.json"))["pairs"]
    repos = sorted({p["consumer"]["repo"] for p in cands})
    mine = [r for k, r in enumerate(repos) if k % n == i - 1]
    os.makedirs("scale/probe", exist_ok=True)
    tmp = os.environ.get("RUNNER_TEMP", "/tmp")
    for repo in mine:
        d = os.path.join(tmp, repo.replace("/", "__") + ".git")
        try:
            subprocess.run(["git", "clone", "-q", "--bare", "--single-branch", f"https://github.com/{repo}.git", d], check=True,
                           capture_output=True, text=True, timeout=600)
        except Exception as e:  # recorded, never silent
            err = str(e)[-400:]
            for p in cands:
                if p["consumer"]["repo"] == repo:
                    out = {"suite": p["suite"], "consumer": p["consumer"]["name"], "error": "clone: " + err}
                    json.dump(out, open(f"scale/probe/{p['suite']}__{p['consumer']['name']}.json", "w"), indent=1)
            continue
        for p in cands:
            if p["consumer"]["repo"] != repo:
                continue
            gm = p["consumer"].get("gomod", "go.mod")
            mod = p["provider"]["module"]
            log = git(d, "log", "--first-parent", f"--since={SINCE}", "--format=%H %cs", "HEAD", "--", gm)
            bumps = []
            for line in log.splitlines():
                c, date = line.split()
                new = version(git(d, "show", f"{c}:{gm}", check=False) or None, mod)
                old = version(git(d, "show", f"{c}^:{gm}", check=False) or None, mod)
                if new != old:
                    bumps.append({"commit": c, "date": date, "old": old, "new": new})
            head = version(git(d, "show", f"HEAD:{gm}", check=False) or None, mod)
            out = {"suite": p["suite"], "tier": p["tier"], "consumer": p["consumer"]["name"], "repo": repo, "module": mod,
                   "head_version": head, "gomod_commits": len(log.splitlines()),
                   "upgrades": sum(1 for b in bumps if b["old"] and b["new"]),
                   "added_or_removed": sum(1 for b in bumps if not (b["old"] and b["new"])),
                   "replaced_by_fork": sum(1 for b in bumps if (b["new"] or "").startswith("replaced:")),
                   "first": bumps[-1]["date"] if bumps else "", "last": bumps[0]["date"] if bumps else "", "bumps": bumps}
            json.dump(out, open(f"scale/probe/{p['suite']}__{p['consumer']['name']}.json", "w"), indent=1)
            print(f"{p['suite']:>20} -> {p['consumer']['name']:<32} upgrades {out['upgrades']:>4}  head {head}", flush=True)
        subprocess.run(["rm", "-rf", d])


if __name__ == "__main__":
    main()
