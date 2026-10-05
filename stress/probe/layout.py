#!/usr/bin/env python3
"""Feasibility survey of one Java project of stress/java/projects.json (no
verifier runs): where its contract is, how often it changed since `since`,
which modules use it, which JDK it asks for, and its open pull requests that
change the contract. Usage: layout.py NAME OUT_DIR. Needs git, and GH_TOKEN
for the pull request listing."""
import json
import os
import re
import subprocess
import sys
import urllib.request

name, out = sys.argv[1], sys.argv[2]
cfg = json.load(open("stress/java/projects.json"))
since = cfg["since"]
p = next(x for x in cfg["projects"] if x["name"] == name)
work = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "layout-" + name)
os.makedirs(out, exist_ok=True)


def git(*args, cwd=None, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.strip()[:500]}")
    return r.stdout


def api(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={
        "Accept": "application/vnd.github+json", "Authorization": "Bearer " + os.environ.get("GH_TOKEN", ""),
        "User-Agent": "parent-proof"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def clone(repo, commit, dest):
    if not os.path.isdir(dest):
        git("clone", "-q", "--filter=blob:none", "--no-checkout", f"https://github.com/{repo}.git", dest)
    git("-C", dest, "fetch", "-q", "origin", commit, check=False)
    return dest


res = {"name": name, "set": p["set"], "consumer": p["consumer"]}
c = p["consumer"]
d = clone(c["repo"], c["commit"], work)
res["head"] = git("-C", d, "log", "-1", "--format=%H %cI", c["commit"]).strip()
res["default_branch"] = git("-C", d, "rev-parse", "--abbrev-ref", "origin/HEAD").strip()

# Build files and the contract files only.
git("-C", d, "sparse-checkout", "set", "--no-cone", "/**/pom.xml", "/pom.xml", "/**/build.gradle", "/**/build.gradle.kts",
    "/settings.gradle", "/settings.gradle.kts", "/gradle.properties", "/.gitmodules", "/**/*.proto", "/dev/proto.sh",
    "/scripts/proto.sh", "/.java-version", "/.sdkmanrc", "/MODULE.bazel", "/tools/API_SHAS")
git("-C", d, "checkout", "-q", c["commit"])

k = p["contract"]
hist = []
if "submodule" in k:
    path = k["submodule"]
    log = git("-C", d, "log", "--first-parent", f"--since={since}", "--format=%H %cs", c["commit"], "--", path).split("\n")
    prev = None
    for line in reversed([x for x in log if x.strip()]):
        sha, date = line.split()
        f = git("-C", d, "ls-tree", sha, "--", path).split()
        pin = f[2] if len(f) >= 3 and f[1] == "commit" else ""
        if pin and pin != prev:
            hist.append({"commit": sha, "date": date, "pin": pin})
        prev = pin or prev
elif "regex" in k:
    log = git("-C", d, "log", "--first-parent", f"--since={since}", "--format=%H %cs", c["commit"], "--", *k["paths"]).split("\n")
    prev = None
    for line in reversed([x for x in log if x.strip()]):
        sha, date = line.split()
        pin = None
        for f in k["paths"]:
            body = git("-C", d, "show", f"{sha}:{f}", check=False)
            m = re.search(k["regex"], body)
            if m:
                pin = m.group(1)
        if pin and pin != prev:
            hist.append({"commit": sha, "date": date, "pin": pin})
        prev = pin or prev
else:
    log = git("-C", d, "log", "--first-parent", f"--since={since}", "--format=%H %cs %s", c["commit"], "--", *k["paths"]).split("\n")
    for line in reversed([x for x in log if x.strip()]):
        sha, date, subj = (line.split(" ", 2) + [""])[:3]
        files = git("-C", d, "diff", "--name-only", f"{sha}^1", sha, "--", *k["paths"], check=False).split()
        protos = [f for f in files if f.endswith(".proto")]
        hist.append({"commit": sha, "date": date, "subject": subj[:100], "files": len(files), "protos": len(protos)})
res["history"] = {"count": len(hist), "with_proto_changes": sum(1 for h in hist if h.get("protos", 1)), "last": hist[-25:]}

# Modules that name the contract module in their build file.
users = []
if p.get("users"):
    rx = re.compile(p["users"])
    for root, dirs, files in os.walk(d):
        if ".git" in root:
            continue
        for f in files:
            if f in ("pom.xml", "build.gradle", "build.gradle.kts"):
                fp = os.path.join(root, f)
                try:
                    if rx.search(open(fp, encoding="utf-8", errors="replace").read()):
                        users.append(os.path.relpath(fp, d).replace("\\", "/"))
                except OSError:
                    pass
res["users"] = sorted(users)

# JDK hints from the root build files.
hints = []
for f in ("pom.xml", "build.gradle", "build.gradle.kts", "gradle.properties", ".java-version", ".sdkmanrc"):
    fp = os.path.join(d, f)
    if os.path.exists(fp):
        for i, line in enumerate(open(fp, encoding="utf-8", errors="replace")):
            if re.search(r"maven\.compiler|<release>|<java\.version>|java\.version|sourceCompatibility|targetCompatibility|languageVersion|toolchain|jdk", line, re.I):
                hints.append(f"{f}:{i + 1}: {line.strip()[:160]}")
res["jdk_hints"] = hints[:30]
res["proto_count"] = int(git("-C", d, "ls-tree", "-r", "--name-only", "HEAD").count(".proto\n"))
res["build_files"] = int(sum(1 for line in git("-C", d, "ls-tree", "-r", "--name-only", "HEAD").split("\n")
                              if line.endswith(("pom.xml", "build.gradle", "build.gradle.kts"))))

# Open pull requests that change the contract, updated in the last 30 days.
def open_prs(repo, match):
    found, seen = [], 0
    try:
        prs = api(f"repos/{repo}/pulls?state=open&sort=updated&direction=desc&per_page=50")
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}
    import datetime
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for pr in prs:
        if pr["updated_at"] < cutoff or pr.get("draft"):
            continue
        seen += 1
        try:
            files = api(f"repos/{repo}/pulls/{pr['number']}/files?per_page=100")
        except Exception:  # noqa: BLE001
            continue
        if any(match(f["filename"]) for f in files):
            found.append({"n": pr["number"], "title": pr["title"][:90], "updated": pr["updated_at"][:10]})
    return {"checked": seen, "matching": found}


if "submodule" in k:
    res["provider_prs"] = open_prs(k["provider"], lambda f: f.endswith(".proto"))
elif "regex" in k:
    res["provider_prs"] = open_prs(k["provider"], lambda f: f.endswith(".proto"))
else:
    res["prs"] = open_prs(c["repo"], lambda f: any(f.startswith(x.rstrip("/") + "/") or f == x for x in k["paths"]))

json.dump(res, open(os.path.join(out, "layout.json"), "w"), indent=1)
print(json.dumps(res, indent=1)[:20000])
