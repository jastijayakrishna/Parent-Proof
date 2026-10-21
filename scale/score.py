#!/usr/bin/env python3
"""Prints SCALE.md: the scale test (scale/PREREG.md), counted only from
decisions made by the binary in bin/ (its sha256 is in bin/VERSION).

For the build, the verifier's answer is its source_build aspect; the Go
compiler (or javac) judges it, and a judge counts only when it first broke on
its canary (a planted change that must break the consumer):
- caught: the change breaks the consumer and the verifier said Don't merge;
- missed: it breaks and the verifier said Merge (the failure that matters);
- false alarm: it compiles and the verifier said Don't merge;
- needs review: the verifier said Needs review.
Rows decided by any other binary are left out of every count and listed by
how many there are, so an old result can never stand in for a new one."""
import collections
import datetime
import glob
import json
import os
import re

WORD = {"GO": "Merge", "NO_GO": "Don't merge", "UNKNOWN": "Needs review", "ERROR": "error", "": "-"}


def binary():
    text = open("bin/VERSION", encoding="utf-8").read()
    sha = re.search(r"sha256[^:]*:\s*([0-9a-f]{64})", text).group(1)
    commit = re.search(r"commit\s+([0-9a-f]{40})", text).group(1)
    return sha, commit


SHA, COMMIT = binary()


def ours(verifier_txt):
    """Was this directory decided by today's binary? history.sh writes the
    version and the sha256; the scan writes bin/VERSION's first line."""
    if not os.path.exists(verifier_txt):
        return False
    t = open(verifier_txt, encoding="utf-8").read()
    return SHA in t or COMMIT in t


def trusted(compiler, canary):
    if compiler in ("breaks", "compiles") and canary != "breaks":
        return "judge not verified"
    return compiler


def canary_of(d):
    """One canary for a whole directory: "breaks" only when every job's judge
    broke on its canary, else the first other outcome in name order."""
    outs = []
    for cf in sorted(glob.glob(os.path.join(d, "canary-*.jsonl"))):
        outs += [json.loads(x)["oracle"]["outcome"] for x in open(cf, encoding="utf-8") if x.strip()]
    if outs and all(c == "breaks" for c in outs):
        return "breaks"
    return next((c for c in outs if c != "breaks"), "none")


def canaries_by_bump(d):
    """The canary of the job that decided each window (by its bump): a job's
    windows-KofN.jsonl goes with its canary-KofN.jsonl, so an answer counts
    only when its own judge broke on the canary. Three pairs had jobs that
    disagreed (2026-10-21); reading one canary per directory then depended
    on the order the file system listed the files."""
    out = {}
    for wf in glob.glob(os.path.join(d, "windows-*.jsonl")):
        k = os.path.basename(wf)[len("windows-"):-len(".jsonl")]
        cf = os.path.join(d, f"canary-{k}.jsonl")
        outs = [json.loads(x)["oracle"]["outcome"] for x in open(cf, encoding="utf-8") if x.strip()] if os.path.exists(cf) else []
        c = "breaks" if outs and all(o == "breaks" for o in outs) else next((o for o in outs if o != "breaks"), "none")
        for x in open(wf, encoding="utf-8"):
            if x.strip():
                out[json.loads(x).get("bump", "")] = c
    return out


def suite_repos(*dirs):
    repos = {}
    for d in dirs:
        for f in glob.glob(os.path.join(d, "*.suite.json")):
            s = json.load(open(f, encoding="utf-8"))
            for name, c in s.get("consumers", {}).items():
                repos[(s["name"], name)] = c.get("repo", "")
    return repos


def history_rows(root, corpus, setof, repos, skipped):
    out = []
    for f in sorted(glob.glob(f"{root}/*/*/results-*.jsonl")):
        d = os.path.dirname(f)
        suite, consumer = d.replace("\\", "/").split("/")[-2:]
        lines = [x for x in open(f, encoding="utf-8") if x.strip()]
        if not ours(os.path.join(d, "verifier.txt")):
            skipped[corpus] += len(lines)
            continue
        canary, by_bump = canary_of(d), canaries_by_bump(d)
        repo = repos.get((suite, consumer), "")
        for line in lines:
            r = json.loads(line)
            w, o = r.get("window", {}), r.get("observed") or {}
            c = by_bump.get(w.get("bump", ""), canary)
            out.append({"corpus": corpus, "set": setof(suite, consumer), "lang": "Go", "project": f"{suite} -> {consumer}",
                        "mode": "upgrade", "id": f"{w.get('old_pin', '')} -> {w.get('new_pin', '')}",
                        "link": f"https://github.com/{repo}/commit/{w.get('bump', '')}" if repo else "", "date": w.get("date", ""),
                        "verdict": o.get("verdict", "ERROR"), "build": (o.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted((w.get("oracle") or {}).get("outcome", "not judged"), c),
                        "reasons": o.get("unknown_reasons") or [], "where": (o.get("evidence") or [""])[0],
                        "error": o.get("error", ""), "errors": (w.get("oracle") or {}).get("errors", [])[:2]})
    return out


def scan_rows(root, corpus, corpus_file, setof, skipped):
    eco = {}
    if os.path.exists(corpus_file):
        eco = {e["name"]: e for e in json.load(open(corpus_file, encoding="utf-8"))["ecosystems"]}
    out = []
    for f in sorted(glob.glob(f"{root}/*/scan.jsonl")):
        d = os.path.dirname(f)
        name = d.replace("\\", "/").split("/")[-1]
        lines = [x for x in open(f, encoding="utf-8") if x.strip()]
        if not ours(os.path.join(d, "verifier.txt")):
            skipped[corpus] += len(lines)
            continue
        url = (eco.get(name) or {}).get("provider", {}).get("url", "")
        repo = url.split("github.com/")[-1].removesuffix(".git") if url else ""
        for line in lines:
            r = json.loads(line)
            o = r.get("oracle") or {}
            out.append({"corpus": corpus, "set": setof(name, ""), "lang": "Go", "project": name, "mode": "pull request",
                        "id": r.get("commit", "")[:12], "link": f"https://github.com/{repo}/commit/{r.get('commit', '')}" if repo else "",
                        "date": r.get("date", ""), "verdict": r.get("verdict", "ERROR"),
                        "build": (r.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted(o.get("outcome") or "not judged", (r.get("canary") or {}).get("outcome", "none")),
                        "reasons": r.get("unknown_reasons") or [], "where": (r.get("evidence") or [""])[0],
                        "error": r.get("error", ""), "errors": o.get("errors", [])[:2], "unjudged": r.get("unjudged", "")})
    return out


def java_rows(since, setof, skipped):
    out = []
    files = sorted(glob.glob("stress/results/java/*/*/results-*.jsonl")) + sorted(glob.glob("stress/results/java-live/*/*.jsonl"))
    for f in files:
        canary = "none"
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if "window" not in r:
                if "shard" in r:
                    canary = (r.get("canary") or {}).get("outcome", "none")
                continue
            if r.get("started", "") < since:
                skipped["Java stress test"] += 1
                continue
            w, v, o = r["window"], r.get("verifier") or {}, r.get("oracle") or {}
            pr = w.get("pr") or {}
            repo = w.get("provider", "")
            out.append({"corpus": "Java stress test", "set": setof(w["project"], ""), "lang": "Java", "project": w["project"],
                        "mode": "pull request" if pr else ("upgrade" if w["mode"] == "history" else w["mode"]),
                        "id": (f"#{pr['n']}" if pr else w["id"]),
                        "link": pr.get("url", "") or (f"https://github.com/{repo}/commit/{w.get('bump', '')}" if repo and w.get("bump") else ""),
                        "date": w.get("date", ""), "verdict": v.get("verdict", "ERROR" if v else ""),
                        "build": (v.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted(o.get("outcome", "not judged"), canary), "reasons": v.get("unknown_reasons") or [],
                        "where": (o.get("errors") or [""])[0] if o.get("outcome") == "breaks" else "",
                        "error": (r.get("harness_error") or v.get("error") or "")[:300], "errors": (o.get("errors") or [])[:2],
                        "replay": v.get("replay", "")})
    return out


def live_rows(skipped):
    out = []
    for f in sorted(glob.glob("predictions/*/*.json")):
        r = json.load(open(f, encoding="utf-8"))
        pr = r.get("pr") or {}
        if (r.get("verifier") or {}).get("sha256") != SHA:
            skipped["Open pull requests, live"] += len(r.get("results") or [])
            continue
        for res in r.get("results") or []:
            o = res.get("oracle") or {}
            out.append({"corpus": "Open pull requests, live", "set": "live", "lang": "Go", "project": pr.get("eco", ""),
                        "mode": "pull request", "id": f"#{pr.get('n', '')}", "link": pr.get("url", ""), "date": res.get("date", ""),
                        "verdict": res.get("verdict", "ERROR"), "build": (res.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted(o.get("outcome") or "not judged", (res.get("canary") or {}).get("outcome", "none")),
                        "reasons": res.get("unknown_reasons") or [], "where": (res.get("evidence") or [""])[0],
                        "error": res.get("error", ""), "errors": o.get("errors", [])[:2]})
    return out


def score(rows):
    judged = [r for r in rows if r["compiler"] in ("breaks", "compiles")]
    breaks = [r for r in judged if r["compiler"] == "breaks"]
    safe = [r for r in judged if r["compiler"] == "compiles"]
    decided = [r for r in rows if r["verdict"] not in ("", "ERROR")]
    return {"decided": len(decided), "judged": len(judged), "broke": len(breaks),
            "caught": sum(r["build"] == "NO_GO" for r in breaks), "missed": sum(r["build"] == "GO" for r in breaks),
            "review_break": sum(r["build"] == "UNKNOWN" for r in breaks),
            "safe": len(safe), "merge_safe": sum(r["build"] == "GO" for r in safe),
            "false_alarm": sum(r["build"] == "NO_GO" for r in safe), "review_safe": sum(r["build"] == "UNKNOWN" for r in safe),
            "errors": sum(1 for r in rows if r["verdict"] == "ERROR" or r.get("error")),
            "replay_bad": sum(1 for r in rows if r.get("replay") and r["replay"] != "same"),
            "unjudged": len(rows) - len(judged)}


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "-"


def table(groups):
    print("| | decided | judged by the compiler | broke the build | caught (Don't merge) | stopped with Needs review | **missed (said Merge)** | safe | said Merge on safe | false alarms | needs review on safe |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for name, rows in groups:
        s = score(rows)
        print(f"| {name} | {s['decided']} | {s['judged']} | {s['broke']} | {s['caught']} | {s['review_break']} | **{s['missed']}** | "
              f"{s['safe']} | {s['merge_safe']} | {s['false_alarm']} | {s['review_safe']} |")


def main():
    plan = json.load(open("scale/plan.json", encoding="utf-8")) if os.path.exists("scale/plan.json") else {"history": []}
    tiers = {}
    for p in json.load(open("scale/candidates.json", encoding="utf-8"))["pairs"]:
        tiers[(p["suite"], p["consumer"]["name"])] = p["tier"]
    scale_eco = {}
    if os.path.exists("scale/corpus.json"):
        scale_eco = {e["name"]: e.get("tier", 1) for e in json.load(open("scale/corpus.json", encoding="utf-8"))["ecosystems"]}
    stress_sets = {}
    for h in json.load(open("stress/go-plan.json", encoding="utf-8"))["history"]:
        stress_sets[(h["suite"], h["consumer"])] = h["set"]
    for e in json.load(open("stress/corpus.json", encoding="utf-8"))["ecosystems"]:
        stress_sets[(e["name"], "")] = e.get("set", "dev")
    for v in json.load(open("stress/java/projects.json", encoding="utf-8"))["projects"]:
        stress_sets[(v["name"], "")] = v.get("set", "dev")

    skipped = collections.Counter()
    bin_time = os.environ.get("BIN_SINCE", "2026-10-21T07:30:00Z")
    new = history_rows("scale/results/history", "New projects", lambda s, c: f"tier {tiers.get((s, c), 1)}",
                       suite_repos("scale/suites"), skipped)
    new += scan_rows("scale/results/scan", "New projects", "scale/corpus.json", lambda n, _: f"tier {scale_eco.get(n, 1)}", skipped)
    hist = history_rows("history/results", "History (9 pairs)", lambda s, c: "history", suite_repos("history/suites"), skipped)
    sgo = history_rows("stress/results/go/history", "Go stress test", lambda s, c: stress_sets.get((s, c), "dev"),
                       suite_repos("stress/suites"), skipped)
    sgo += scan_rows("stress/results/go/scan", "Go stress test", "stress/corpus.json", lambda n, _: stress_sets.get((n, ""), "dev"), skipped)
    java = java_rows(bin_time, lambda n, _: stress_sets.get((n, ""), "dev"), skipped)
    live = live_rows(skipped)
    allrows = new + hist + sgo + java + live

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print("# Scale test: real contract changes, judged by the compiler\n")
    print(f"Updated {now}. Every count below comes from one binary: Parent main `{COMMIT[:7]}`, "
          f"sha256 `{SHA[:16]}…` ([bin/VERSION](bin/VERSION)), the build a customer would install today. "
          "Rules, fixed before the run: [scale/PREREG.md](scale/PREREG.md).\n")
    s = score(allrows)
    print(f"**{s['decided']} real changes decided; the compiler judged {s['judged']}. "
          f"{s['broke']} broke a project's build: Parent said Don't merge on {s['caught']}, Needs review on {s['review_break']}, "
          f"and Merge on {s['missed']}. Of the {s['safe']} safe changes it said Merge on {s['merge_safe']} "
          f"({pct(s['merge_safe'], s['safe'])}), Don't merge on {s['false_alarm']}, Needs review on {s['review_safe']}.**\n")
    print("- **Caught**: the change broke the build; Parent said Don't merge, with the file and line.")
    print("- **Stopped with Needs review**: it broke; Parent could not prove which way, so it did not say Merge.")
    print("- **Missed**: it broke and Parent said Merge. The failure that matters most.")
    print("- **False alarm**: it compiled and Parent said Don't merge.")
    print("- Not judged (counted in *decided* only): the compiler could not build the project before the change, or its "
          "judge did not break on the planted canary, so its answer would prove nothing.\n")

    print("## By corpus\n")
    groups = [("**New projects, never used before: contract and project new**", [r for r in new if r["set"] == "tier 1"]),
              ("**New projects: a known contract, a project never used**", [r for r in new if r["set"] == "tier 2"]),
              ("History: 9 contract → project pairs, rerun", hist),
              ("Go stress test, rerun: dev", [r for r in sgo if r["set"] == "dev"]),
              ("Go stress test, rerun: hold-out", [r for r in sgo if r["set"] == "holdout"]),
              ("Java stress test, rerun: dev", [r for r in java if r["set"] == "dev"]),
              ("Java stress test, rerun: hold-out", [r for r in java if r["set"] == "holdout"]),
              ("Java stress test, rerun: regression", [r for r in java if r["set"] == "regression"]),
              ("Open pull requests, decided live", live),
              ("**All**", allrows)]
    table(groups)
    print()
    by_mode = collections.Counter(r["mode"] for r in allrows)
    print(f"Kinds of change: {by_mode['upgrade']} real upgrades a project made of a contract it uses (its own commit, "
          f"usually its own pull request); {by_mode['pull request']} merged or open pull requests of the contract itself, "
          f"decided against a project that uses it.\n")
    if sum(skipped.values()):
        print("Left out because another binary decided them (rerun pending): " +
              ", ".join(f"{k} {v}" for k, v in sorted(skipped.items()) if v) + ".\n")

    print("## Every change that broke a build\n")
    print("| corpus | contract → project | change | date | compiler | Parent, for the build | where Parent points |")
    print("|---|---|---|---|---|---|---|")
    for r in sorted((r for r in allrows if r["compiler"] == "breaks"), key=lambda r: (r["build"] != "GO", r["corpus"], r["project"], r["date"])):
        change = f"[{r['id']}]({r['link']})" if r["link"] else r["id"]
        mark = "**MISSED: Merge**" if r["build"] == "GO" else WORD.get(r["build"], r["build"])
        where = r["where"] if r["build"] == "NO_GO" else ", ".join(r["reasons"][:2])
        first = (r["errors"] or [""])[0].replace("|", "\\|")[:110]
        print(f"| {r['corpus']} | {r['project']} | {change} | {r['date']} | breaks: `{first}` | {mark} | {str(where).replace('|', '/')[:120]} |")
    print()

    fa = [r for r in allrows if r["compiler"] == "compiles" and r["build"] == "NO_GO"]
    print(f"## False alarms ({len(fa)})\n")
    if fa:
        print("| corpus | contract → project | change | date | Parent's finding |")
        print("|---|---|---|---|---|")
        for r in sorted(fa, key=lambda r: (r["corpus"], r["project"], r["date"])):
            change = f"[{r['id']}]({r['link']})" if r["link"] else r["id"]
            print(f"| {r['corpus']} | {r['project']} | {change} | {r['date']} | {str(r['where'])[:160].replace('|', '/')} |")
        print()

    print("## Needs review, by reason (judged changes)\n")
    reasons = collections.Counter()
    for r in allrows:
        if r["build"] == "UNKNOWN" and r["compiler"] in ("breaks", "compiles"):
            for x in (r["reasons"] or ["(no reason recorded)"]):
                reasons[x] += 1
    for k, v in reasons.most_common():
        print(f"- {k}: {v}")
    print()

    print("## New projects, pair by pair\n")
    print("| tier | contract → project | decided | judged | broke | caught | needs review on a break | missed | false alarms | needs review on safe | not judged |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    per = collections.defaultdict(list)
    for r in new:
        per[(r["set"], r["project"], r["mode"])].append(r)
    for (tier, proj, mode), rows in sorted(per.items()):
        s = score(rows)
        label = proj + (" (pull requests)" if mode == "pull request" else "")
        print(f"| {tier} | {label} | {s['decided']} | {s['judged']} | {s['broke']} | {s['caught']} | {s['review_break']} | "
              f"{s['missed']} | {s['false_alarm']} | {s['review_safe']} | {s['unjudged']} |")
    print()
    unj = collections.Counter()
    for r in allrows:
        if r["compiler"] not in ("breaks", "compiles"):
            unj[r["compiler"] if r["compiler"] != "not judged" else (r.get("unjudged") or "not judged")] += 1
    print("Not judged, by reason: " + ", ".join(f"{k} {v}" for k, v in unj.most_common()) + ".\n")
    errs = [r for r in allrows if r["verdict"] == "ERROR" or r.get("error")]
    named = sorted({r["project"] + ": " + str(r["error"])[:80] for r in errs})[:8]
    print(f"Errors: {len(errs)}" + (" (" + "; ".join(named) + ")" if errs else "") + ".")


if __name__ == "__main__":
    main()
