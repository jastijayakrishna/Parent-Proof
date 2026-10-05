#!/usr/bin/env python3
"""The Java part of the stress test (stress/PREREG.md): real contract changes
of the projects in projects.json, each decided by the verifier and judged by
the project's own build (javac, and kotlinc for Kotlin modules).

A window is one contract change seen by one consumer tree:
  consumer_commit  the consumer's code that is built and read
  provider         the repository holding the contract (the consumer's own
                   for contracts kept in it)
  old, new         the provider commits before and after the change

For each window the harness
  1. builds the consumer with the contract at `old` (the baseline);
  2. runs `verifier verify --repo PROVIDER --base old --head new --callers
     TREE`, then `verifier replay` on its record;
  3. builds the same tree again from clean, with the contract at `new`, and
     reads the compiler's errors: errors in the consumer's main sources mean
     the change breaks it.
The verifier never sees the compiler's answer: it runs before the second build.

Usage:
  harness.py windows NAME MODE            print the windows (history, scan)
  harness.py run NAME MODE --shard I/N --out FILE [--pr JSON]
  harness.py live-plan [--done DIR]       open pull requests to decide (JSON)
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "projects.json"), encoding="utf-8"))
WORK = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "java-stress")
BIN = os.environ.get("VERIFIER", os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "verifier"))
LOG_TAIL = 4000


def project(name):
    for p in CFG["projects"]:
        if p["name"] == name:
            return p
    raise SystemExit(f"no project {name} in projects.json")


def sh(cmd, cwd=None, timeout=None, env=None):
    """Runs a shell command; returns (exit code, combined output, seconds)."""
    t0 = time.time()
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env,
                           errors="replace")
        return r.returncode, r.stdout + r.stderr, time.time() - t0
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return 124, out + f"\n[timed out after {timeout} s]", time.time() - t0


def git(*args, cwd=None, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:400]}")
    return r.stdout.strip()


def api(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "parent-proof",
        **({"Authorization": "Bearer " + os.environ["GH_TOKEN"]} if os.environ.get("GH_TOKEN") else {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def clone(repo, full=False):
    """A clone of owner/name under WORK, made once: blobless for consumers
    (blobs come when a tree is checked out), full for providers."""
    d = os.path.join(WORK, "repos", repo.replace("/", "__"))
    if not os.path.isdir(d):
        os.makedirs(os.path.dirname(d), exist_ok=True)
        args = ["clone", "-q", "--no-checkout"] + ([] if full else ["--filter=blob:none"])
        git(*args, f"https://github.com/{repo}.git", d)
    return d


def ensure(repo_dir, *shas):
    for s in shas:
        if s and subprocess.run(["git", "-C", repo_dir, "cat-file", "-e", s + "^{commit}"], capture_output=True).returncode != 0:
            git("-C", repo_dir, "fetch", "-q", "origin", s, check=False)


def kind(p):
    k = p["contract"]
    if "submodule" in k:
        return "submodule"
    if "regex" in k:
        return "regex"
    return "inrepo"


def provider_repo(p):
    k = p["contract"]
    return k.get("provider") or p["consumer"]["repo"]


# ---------------------------------------------------------------- windows

def pin_at(p, cdir, commit):
    """The provider commit the consumer's tree at commit pins: the
    submodule's gitlink, or the commit the pin file names."""
    k = p["contract"]
    if "submodule" in k:
        f = git("-C", cdir, "ls-tree", commit, "--", k["submodule"], check=False).split()
        return f[2] if len(f) >= 3 and f[1] == "commit" else ""
    for path in k["paths"]:
        body = git("-C", cdir, "show", f"{commit}:{path}", check=False)
        for rx in patterns(k):
            m = re.search(rx, body, re.M)
            if m:
                return m.group(1)
    return ""


def patterns(k):
    """The pin file's patterns, tried in order: group 1 is the commit."""
    return k["regex"] if isinstance(k["regex"], list) else [k["regex"]]


def history_windows(p, since):
    """Every first-parent commit of the consumer since `since` that changed
    its contract: a new pin (submodule, pin file), or changed .proto files
    under the contract paths (inrepo)."""
    c = p["consumer"]
    cdir = clone(c["repo"])
    ensure(cdir, c["commit"])
    k, kd = p["contract"], kind(p)
    paths = [k["submodule"]] if kd == "submodule" else k["paths"]
    log = git("-C", cdir, "log", "--first-parent", f"--since={since}", "--format=%H %cs %s", c["commit"], "--", *paths)
    out = []
    for line in reversed([x for x in log.split("\n") if x.strip()]):
        sha, date, subj = (line.split(" ", 2) + [""])[:3]
        parent = git("-C", cdir, "rev-parse", f"{sha}^1", check=False)
        if not parent:
            continue
        w = {"project": p["name"], "mode": "history", "id": sha[:12], "bump": sha, "date": date, "subject": subj[:120],
             "consumer_commit": parent, "provider": provider_repo(p)}
        if kd == "inrepo":
            changed = git("-C", cdir, "diff", "--name-only", parent, sha, "--", *paths).split("\n")
            if not any(f.endswith(".proto") for f in changed):
                continue
            w["old"], w["new"] = parent, sha
        else:
            old, new = pin_at(p, cdir, parent), pin_at(p, cdir, sha)
            if not old or not new or old == new:
                continue
            w["old"], w["new"] = old, new
        out.append(w)
    return out


def scan_windows(p, limit):
    """The provider's last `limit` commits that change .proto files, up to
    the pinned provider commit, each against the consumer's pinned tree."""
    if kind(p) == "inrepo":
        return []
    k, c = p["contract"], p["consumer"]
    pdir = clone(provider_repo(p), full=True)
    head = k.get("provider_commit") or git("-C", pdir, "rev-parse", "origin/HEAD")
    ensure(pdir, head)
    log = git("-C", pdir, "log", f"-{limit}", "--format=%H %cs %s", head, "--", "*.proto")
    out = []
    for line in [x for x in log.split("\n") if x.strip()]:
        sha, date, subj = (line.split(" ", 2) + [""])[:3]
        parent = git("-C", pdir, "rev-parse", f"{sha}^1", check=False)
        if parent:
            out.append({"project": p["name"], "mode": "scan", "id": sha[:12], "date": date, "subject": subj[:120],
                        "consumer_commit": c["commit"], "provider": provider_repo(p), "old": parent, "new": sha})
    return list(reversed(out))


def live_window(p, pr):
    """One open pull request as one change: the provider's merge base to the
    pull request's head. A contract kept in the consumer is read with the
    consumer's code at the merge base; another repository's contract with
    the consumer's pinned tree."""
    prov = provider_repo(p)
    pdir = clone(prov, full=(kind(p) != "inrepo"))
    git("-C", pdir, "fetch", "-q", "origin", f"pull/{pr['n']}/head", pr["base"], check=False)
    mbase = git("-C", pdir, "merge-base", pr["head"], pr["base"])
    w = {"project": p["name"], "mode": "live", "id": f"pr{pr['n']}-{pr['head'][:12]}", "date": pr.get("updated", "")[:10],
         "subject": pr.get("title", "")[:120], "provider": prov, "old": mbase, "new": pr["head"], "pr": pr,
         "consumer_commit": mbase if kind(p) == "inrepo" else p["consumer"]["commit"]}
    return w


# ---------------------------------------------------------------- trees

def export(repo_dir, sha, dest):
    """Writes the tree of sha into dest (replacing it)."""
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest, exist_ok=True)
    rc, out, _ = sh(f"git -C '{repo_dir}' archive --format=tar {sha} | tar -x -C '{dest}'")
    if rc != 0:
        raise RuntimeError(f"export {sha}: {out[-400:]}")


def prepare(p, w, side, wt):
    """Makes wt the consumer's tree at consumer_commit with the contract at
    w[side] (old or new), from clean."""
    c = p["consumer"]
    cdir = clone(c["repo"])
    ensure(cdir, w["consumer_commit"])
    if os.path.isdir(wt):
        git("-C", cdir, "worktree", "remove", "--force", wt, check=False)
        shutil.rmtree(wt, ignore_errors=True)
    git("-C", cdir, "worktree", "prune", check=False)
    git("-C", cdir, "worktree", "add", "-q", "--detach", "--force", wt, w["consumer_commit"])
    k, kd = p["contract"], kind(p)
    # Other submodules the build needs, at the consumer's own gitlinks.
    for s in p.get("submodules", []):
        if kd == "submodule" and s == k["submodule"]:
            continue
        f = git("-C", cdir, "ls-tree", w["consumer_commit"], "--", s, check=False).split()
        if len(f) >= 3 and f[1] == "commit":
            repo = re.sub(r"^https://github.com/|\.git$", "", submodule_url(wt, s))
            sdir = clone(repo, full=True)
            ensure(sdir, f[2])
            export(sdir, f[2], os.path.join(wt, s))
    sha = w[side]
    if kd == "submodule":
        pdir = clone(provider_repo(p), full=True)
        ensure(pdir, sha)
        export(pdir, sha, os.path.join(wt, k["submodule"]))
    elif kd == "regex":
        for path in k["paths"]:
            fp = os.path.join(wt, path)
            if not os.path.exists(fp):
                continue
            body = open(fp, encoding="utf-8").read()
            for rx in patterns(k):
                if re.search(rx, body, re.M):
                    body = re.sub(rx, lambda m: m.group(0).replace(m.group(1), sha), body, count=1, flags=re.M)
                    open(fp, "w", encoding="utf-8").write(body)
                    break
    elif side == "new":
        # The contract paths and every changed .proto file, from new.
        diff = git("-C", cdir, "diff", "--name-status", "--no-renames", w["old"], w["new"], "--", *k["paths"], "*.proto")
        add, rm = [], []
        for line in [x for x in diff.split("\n") if x.strip()]:
            st, path = line.split("\t", 1)
            (rm if st.startswith("D") else add).append(path)
        for path in rm:
            try:
                os.remove(os.path.join(wt, path))
            except FileNotFoundError:
                pass
        for i in range(0, len(add), 200):
            git("-C", wt, "checkout", w["new"], "--", *add[i:i + 200])
        return {"overlaid": len(add), "removed": len(rm)}
    return {}


def submodule_url(wt, path):
    """The URL .gitmodules gives the submodule at path."""
    names = git("-C", wt, "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$", check=False)
    for line in names.splitlines():
        key, _, val = line.partition(" ")
        if val.strip() == path:
            return git("-C", wt, "config", "-f", ".gitmodules", key[: -len(".path")] + ".url", check=False)
    return ""


def provider_paths(p):
    """Where the provider's own code is in the consumer's tree: the
    contract's submodule or paths. Errors there are not the consumer's."""
    k = p["contract"]
    if "submodule" in k:
        return [k["submodule"]]
    if kind(p) == "inrepo":
        return k["paths"]
    return []


CLASS_DIRS = ("target/classes", "build/classes/java/main", "build/classes/kotlin/main")
SRC_DIRS = ("src/main/java", "src/main/kotlin")


def modules(wt):
    """Module directories with compiled main classes, and those with main
    sources but none (not in this build)."""
    built, unbuilt = [], []
    for root, dirs, files in os.walk(wt):
        rel = os.path.relpath(root, wt)
        base = os.path.basename(root)
        if base.startswith(".") or base in ("node_modules", "src") or rel.count(os.sep) > 12:
            dirs[:] = []
            continue
        if base in ("target", "build", "out") and not any(f in files for f in ("pom.xml", "build.gradle", "build.gradle.kts")):
            dirs[:] = []
            continue
        has_classes = any(os.path.isdir(os.path.join(root, d)) for d in CLASS_DIRS)
        has_src = any(os.path.isdir(os.path.join(root, d)) for d in SRC_DIRS)
        if has_classes:
            built.append(rel)
        elif has_src:
            unbuilt.append(rel)
    return sorted(built), sorted(unbuilt)


def build(p, wt, oracle):
    """Runs the project's build in wt. The oracle never reuses Gradle's
    build cache: it compiles everything from source."""
    cmd = p["build"]
    if "gradlew" in cmd:
        cmd = cmd.replace("--build-cache", "")
        cmd += " --no-build-cache" if oracle else " --build-cache"
    jh = os.environ.get(f"JAVA_HOME_{p['jdk']}_X64") or os.environ.get("JAVA_HOME", "")
    env = dict(os.environ, JAVA_HOME=jh, PATH=os.path.join(jh, "bin") + os.pathsep + os.environ["PATH"])
    log, secs = "", 0.0
    if p.get("prebuild"):
        rc, out, s = sh(p["prebuild"], cwd=wt, timeout=900, env=env)
        log, secs = out[-LOG_TAIL:], s
        if rc != 0:
            return rc, log, secs
    rc, out, s = sh(cmd, cwd=wt, timeout=int(os.environ.get("BUILD_TIMEOUT", "1500")), env=env)
    return rc, (log + "\n" + out)[-200000:], secs + s


# javac (Maven, Gradle) and kotlinc diagnostics: file, line, message.
DIAG = [
    re.compile(r"^\[ERROR\] (/\S+\.(?:java|kt)):\[(\d+),\d+\] (.*)$"),
    re.compile(r"^(/\S+\.java):(\d+): error: (.*)$"),
    re.compile(r"^e: (?:file://)?(/\S+\.kt):(\d+):\d+ (.*)$"),
    re.compile(r"^e: (/\S+\.kt): \((\d+), \d+\): (.*)$"),
]


def diagnostics(log, wt):
    out = []
    for line in log.split("\n"):
        line = line.strip()
        for rx in DIAG:
            m = rx.match(line)
            if m:
                f = m.group(1)
                rel = (os.path.relpath(f, wt) if f.startswith(wt) else f).replace(os.sep, "/")
                out.append((rel, int(m.group(2)), m.group(3)[:200]))
                break
    seen, uniq = set(), []
    for d in out:
        if d not in seen:
            seen.add(d)
            uniq.append(d)
    return uniq


def generated(path):
    """Code a generator wrote into the build (target/generated-sources,
    build/generated/...)."""
    return re.search(r"(^|/)generated[^/]*/", path) is not None


def test_code(path):
    return re.search(r"(^|/)src/test/", path) is not None


def judge(rc, log, wt, theirs=()):
    """breaks: the compiler rejects the consumer's own main sources;
    compiles; or why the compiler's answer says nothing about the
    consumer (generated code that does not compile, a failure without a
    compiler diagnostic)."""
    if rc == 0:
        return {"outcome": "compiles"}
    diags = diagnostics(log, wt)
    own = [d for d in diags if not generated(d[0]) and not test_code(d[0])
           and not any(d[0].startswith(t.rstrip("/") + "/") for t in theirs)]
    if own:
        return {"outcome": "breaks", "error_count": len(own), "errors": [f"{f}:{n}: {m}" for f, n, m in own[:20]]}
    if diags:
        return {"outcome": "generated_fails", "error_count": len(diags), "errors": [f"{f}:{n}: {m}" for f, n, m in diags[:10]]}
    tail = [x for x in log.strip().split("\n") if x.strip()][-12:]
    return {"outcome": "oracle_error", "detail": "\n".join(tail)[-1500:]}


def decide(p, w, wt, out_dir):
    """verifier verify on the baseline tree, then replay of its record."""
    pdir = clone(provider_repo(p), full=(kind(p) != "inrepo"))
    ensure(pdir, w["old"], w["new"])
    rec = os.path.join(out_dir, "records", f"{w['project']}-{w['mode']}-{w['id']}.json")
    os.makedirs(os.path.dirname(rec), exist_ok=True)
    cmd = f"'{BIN}' verify --repo '{pdir}' --base {w['old']} --head {w['new']} --callers '{wt}' --json --out '{rec}'"
    rc, out, secs = sh(cmd, timeout=int(os.environ.get("VERIFY_TIMEOUT", "1200")))
    v = {"exit": rc, "seconds": round(secs, 1)}
    if rc not in (0, 3) or not os.path.exists(rec):
        v["verdict"], v["error"] = "ERROR", out[-1500:]
        return v
    d = json.load(open(rec, encoding="utf-8")).get("decision", {})
    v["verdict"] = d.get("verdict", "")
    v["aspects"] = d.get("aspects", {})
    v["unknown_reasons"] = d.get("unknowns") or d.get("unknown_reasons") or []
    ev = []
    for f in d.get("findings", []) or []:
        if f.get("outcome") in ("NO_GO", "UNKNOWN"):
            for u in f.get("evidence", []) or []:
                loc = u.get("location", {})
                ev.append(f"{f.get('aspect', '')} {f.get('outcome', '')} {f.get('rule', '')} {loc.get('file', '')}:{loc.get('line', '')}")
    v["evidence_count"] = len(ev)
    v["evidence"] = ev[:12]
    v["callers"] = [f"{c.get('caller', {}).get('deploy_unit', '')} {c.get('outcome', '')} {';'.join(c.get('reasons') or [])}"[:300]
                    for c in d.get("callers", []) or []][:10]
    rrc, rout, _ = sh(f"'{BIN}' replay --file '{rec}'", timeout=600)
    v["replay"] = "same" if rrc == 0 else f"exit {rrc}: {rout[-300:]}"
    v["record"] = os.path.relpath(rec, out_dir)
    return v


def run_window(p, w, out_dir):
    wt = os.path.join(WORK, "wt")
    r = {"window": w, "started": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    t0 = time.time()
    try:
        prepare(p, w, "old", wt)
        if not p.get("build"):
            r["baseline"] = {"ok": None, "note": "no build"}
            r["modules"] = {"built": [], "unbuilt": []}
            r["verifier"] = decide(p, w, wt, out_dir)
            r["oracle"] = {"outcome": "not_built", "detail": p.get("note", "")}
            return r
        rc, log, secs = build(p, wt, oracle=False)
        r["baseline"] = {"ok": rc == 0, "seconds": round(secs, 1)}
        if rc != 0:
            r["baseline"]["tail"] = log[-2500:]
            r["oracle"] = {"outcome": "baseline_fails"}
            return r
        built, unbuilt = modules(wt)
        # Modules this build does not compile are not callers: their sources
        # go, so the verifier reads exactly the code the compiler builds.
        for m in unbuilt:
            for s in SRC_DIRS:
                shutil.rmtree(os.path.join(wt, m, s), ignore_errors=True)
        r["modules"] = {"built": built, "unbuilt": unbuilt}
        r["verifier"] = decide(p, w, wt, out_dir)
        overlay = prepare(p, w, "new", wt)
        rc, log, secs = build(p, wt, oracle=True)
        o = judge(rc, log, wt, provider_paths(p))
        o["seconds"] = round(secs, 1)
        o.update(overlay)
        r["oracle"] = o
        b2, _ = modules(wt)
        if rc == 0 and sorted(b2) != built:
            r["oracle"]["note"] = f"the build compiled other modules after the change: {sorted(set(b2) ^ set(built))[:10]}"
    except Exception as e:  # noqa: BLE001 - a harness failure is recorded, never dropped
        r["harness_error"] = str(e)[:1500]
    finally:
        r["seconds"] = round(time.time() - t0, 1)
    return r


def cmd_run(a):
    p = project(a.name)
    os.makedirs(WORK, exist_ok=True)
    out_dir = os.path.dirname(os.path.abspath(a.out))
    os.makedirs(out_dir, exist_ok=True)
    if a.mode == "live":
        ws = [live_window(p, json.loads(a.pr))]
    else:
        ws = windows(p, a.mode)
    i, n = (int(x) for x in a.shard.split("/"))
    mine = [w for j, w in enumerate(ws) if j % n == i - 1]
    print(f"{p['name']} {a.mode}: {len(ws)} windows, shard {a.shard} has {len(mine)}", flush=True)
    with open(a.out, "a", encoding="utf-8") as f:
        f.write(json.dumps({"shard": a.shard, "windows_total": len(ws), "windows_in_shard": [w["id"] for w in mine]}) + "\n")
        for w in mine:
            r = run_window(p, w, out_dir)
            f.write(json.dumps(r) + "\n")
            f.flush()
            v, o = r.get("verifier", {}), r.get("oracle", {})
            print(f"{w['id']} {w.get('date', '')} verifier={v.get('verdict')} build={v.get('aspects', {}).get('source_build')} "
                  f"compiler={o.get('outcome')} {r['seconds']}s {r.get('harness_error', '')[:200]}", flush=True)


def windows(p, mode):
    if mode == "history":
        return history_windows(p, p.get("since") or CFG["since"])
    if mode == "scan":
        return scan_windows(p, int(p.get("scan_limit", 20)))
    raise SystemExit(f"unknown mode {mode}")


def cmd_windows(a):
    for w in windows(project(a.name), a.mode):
        print(json.dumps(w))


def cmd_live_plan(a):
    """Open pull requests updated in the last DAYS days that change a
    project's contract and have no record yet for their head."""
    days = int(os.environ.get("DAYS", "14"))
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sets = (os.environ.get("SETS") or "dev,regression").split(",")
    todo = []
    for p in CFG["projects"]:
        if p["set"] not in sets or not p.get("build") or p.get("live") is False:
            continue
        repo = provider_repo(p)
        k = p["contract"]
        inrepo = kind(p) == "inrepo"
        try:
            prs = api(f"repos/{repo}/pulls?state=open&sort=updated&direction=desc&per_page=30")
        except Exception as e:  # noqa: BLE001
            print(f"skip {p['name']}: {e}", file=sys.stderr)
            continue
        rank = 0
        for pr in prs:
            if pr["updated_at"] < cutoff or pr.get("draft") or rank >= int(os.environ.get("PER_PROJECT", "4")):
                continue
            key = f"{p['name']}-pr{pr['number']}-{pr['head']['sha'][:12]}"
            if a.done and os.path.exists(os.path.join(a.done, p["name"], key + ".jsonl")):
                continue
            try:
                files = api(f"repos/{repo}/pulls/{pr['number']}/files?per_page=100")
            except Exception:  # noqa: BLE001
                continue
            names = [f["filename"] for f in files]
            if inrepo:
                hit = any(n.endswith(".proto") and any(n.startswith(x.rstrip("/") + "/") for x in k["paths"]) for n in names)
            else:
                hit = any(n.endswith(".proto") for n in names)
            if not hit:
                continue
            todo.append({"project": p["name"], "key": key, "rank": rank, "jdk": p["jdk"],
                         "pr": {"n": pr["number"], "head": pr["head"]["sha"], "base": pr["base"]["sha"], "title": pr["title"][:120],
                                "url": pr["html_url"], "updated": pr["updated_at"]}})
            rank += 1
    todo.sort(key=lambda x: (x["rank"], x["project"]))
    print(json.dumps(todo[: int(os.environ.get("MAX_PRS", "20"))]))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("windows")
    s.add_argument("name")
    s.add_argument("mode", choices=["history", "scan"])
    s.set_defaults(fn=cmd_windows)
    s = sub.add_parser("run")
    s.add_argument("name")
    s.add_argument("mode", choices=["history", "scan", "live"])
    s.add_argument("--shard", default="1/1")
    s.add_argument("--out", required=True)
    s.add_argument("--pr", default="")
    s.set_defaults(fn=cmd_run)
    s = sub.add_parser("live-plan")
    s.add_argument("--done", default="")
    s.set_defaults(fn=cmd_live_plan)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
