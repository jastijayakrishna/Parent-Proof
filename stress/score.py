#!/usr/bin/env python3
"""Prints STRESS.md: the stress test's results (stress/PREREG.md) per language
and per project, from every result file under stress/results and the live
predictions of stress/corpus.json's projects.

For the build, the verifier's answer is its source_build aspect; the compiler
judges it:
- caught: the compiler says the change breaks the consumer, the verifier said
  Don't merge;
- missed: the compiler says it breaks, the verifier said Merge;
- false alarm: the compiler says it compiles, the verifier said Don't merge;
- needs review: the verifier said Needs review.
A window the compiler could not judge (its baseline does not build, the new
generated code does not compile, or the build failed without a compiler
diagnostic) is counted as not judged, with the reason."""
import collections
import datetime
import glob
import json
import os

WORD = {"GO": "Merge", "NO_GO": "Don't merge", "UNKNOWN": "Needs review", "ERROR": "error", "": "-"}


def trusted(compiler, canary_outcome):
    """A compiler answer counts only when the judge broke on its canary, a
    change that must break the consumer; otherwise it is 'judge not
    verified' (the build may not see the contract at all)."""
    if compiler in ("breaks", "compiles") and canary_outcome != "breaks":
        return "judge not verified"
    return compiler


def rows_go():
    out = []
    for f in sorted(glob.glob("stress/results/go/history/*/*/results-*.jsonl")):
        parts = f.replace("\\", "/").split("/")
        suite, consumer = parts[-3], parts[-2]
        canaries = []
        for cf in glob.glob(os.path.join(os.path.dirname(f), "canary-*.jsonl")):
            canaries += [json.loads(x)["oracle"]["outcome"] for x in open(cf, encoding="utf-8") if x.strip()]
        canary = "breaks" if canaries and all(c == "breaks" for c in canaries) else (canaries[0] if canaries else "none")
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            w, o = r.get("window", {}), r.get("observed") or {}
            out.append({"lang": "Go", "project": f"{suite} -> {consumer}", "mode": "history",
                        "id": f"{w.get('old_pin', '')} -> {w.get('new_pin', '')}", "link": "",
                        "verdict": o.get("verdict", "ERROR"), "build": (o.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted((w.get("oracle") or {}).get("outcome", "not judged"), canary),
                        "reasons": o.get("unknown_reasons") or [], "where": (o.get("evidence") or [""])[0],
                        "error": o.get("error", ""), "errors": (w.get("oracle") or {}).get("errors", [])[:3]})
    for f in sorted(glob.glob("stress/results/go/scan/*/scan.jsonl")):
        eco = f.replace("\\", "/").split("/")[-2]
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            o = r.get("oracle") or {}
            out.append({"lang": "Go", "project": eco, "mode": "scan", "id": r.get("commit", "")[:12], "link": "",
                        "verdict": r.get("verdict", "ERROR"), "build": (r.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted(o.get("outcome") or "not judged", (r.get("canary") or {}).get("outcome", "none")),
                        "reasons": r.get("unknown_reasons") or [],
                        "where": (r.get("evidence") or [""])[0], "error": r.get("error", ""), "errors": o.get("errors", [])[:3],
                        "unjudged": r.get("unjudged", "")})
    names = set()
    if os.path.exists("stress/corpus.json"):
        names = {e["name"] for e in json.load(open("stress/corpus.json"))["ecosystems"]}
    for f in sorted(glob.glob("predictions/*/*.json")):
        r = json.load(open(f, encoding="utf-8"))
        pr = r.get("pr") or {}
        if pr.get("eco") not in names:
            continue
        for res in r.get("results") or []:
            o = res.get("oracle") or {}
            out.append({"lang": "Go", "project": pr.get("eco", ""), "mode": "live", "id": f"#{pr.get('n', '')}", "link": pr.get("url", ""),
                        "verdict": res.get("verdict", "ERROR"), "build": (res.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted(o.get("outcome") or "not judged", (res.get("canary") or {}).get("outcome", "none")),
                        "reasons": res.get("unknown_reasons") or [],
                        "where": (res.get("evidence") or [""])[0], "error": res.get("error", ""), "errors": o.get("errors", [])[:3]})
    return out


def rows_java():
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
            w, v, o = r["window"], r.get("verifier") or {}, r.get("oracle") or {}
            pr = w.get("pr") or {}
            out.append({"lang": "Java", "project": w["project"], "mode": w["mode"],
                        "id": (f"#{pr['n']}" if pr else w["id"]), "link": pr.get("url", ""),
                        "verdict": v.get("verdict", "ERROR" if v else ""), "build": (v.get("aspects") or {}).get("source_build", ""),
                        "compiler": trusted(o.get("outcome", "not judged"), canary), "reasons": v.get("unknown_reasons") or [],
                        "where": (o.get("errors") or [""])[0] if o.get("outcome") == "breaks" else "",
                        "error": (r.get("harness_error") or v.get("error") or "")[:300],
                        "replay": v.get("replay", ""), "seconds": r.get("seconds", 0)})
    return out


def score(rows):
    judged = [r for r in rows if r["compiler"] in ("breaks", "compiles")]
    breaks = [r for r in judged if r["compiler"] == "breaks"]
    safe = [r for r in judged if r["compiler"] == "compiles"]
    decided = [r for r in rows if r["verdict"] not in ("", "ERROR")]
    return {
        "windows": len(rows), "decided": len(decided), "judged": len(judged), "broke": len(breaks),
        "caught": sum(r["build"] == "NO_GO" for r in breaks), "missed": sum(r["build"] == "GO" for r in breaks),
        "false_alarm": sum(r["build"] == "NO_GO" for r in safe),
        "review_judged": sum(r["build"] == "UNKNOWN" for r in judged), "review": sum(r["build"] == "UNKNOWN" for r in decided),
        "errors": sum(1 for r in rows if r["verdict"] == "ERROR" or r.get("error")),
        "replay_bad": sum(1 for r in rows if r.get("replay") and r["replay"] != "same"),
        "merge": sum(r["verdict"] == "GO" for r in decided), "dont": sum(r["verdict"] == "NO_GO" for r in decided),
        "unknown": sum(r["verdict"] == "UNKNOWN" for r in decided),
    }


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "-"


def table(groups, label):
    lines = [f"| {label} | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |",
             "|---|---|---|---|---|---|---|---|---|"]
    for name, rows in groups:
        s = score(rows)
        lines.append(f"| {name} | {s['windows']} | {s['judged']} | {s['broke']} | {s['caught']} | **{s['missed']}** | {s['false_alarm']} | "
                     f"{s['review']} ({pct(s['review'], s['decided'])}) | {s['errors']} |")
    return lines


def main():
    go, java = rows_go(), rows_java()
    allrows = go + java
    print("# Stress test: Go and Java consumers")
    print()
    print(f"Updated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).")
    print()
    print("Every row is a real contract change of an open-source project never used to tune the verifier, decided by the")
    print("verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).")
    print("For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the")
    print("failure that matters most; **false alarm** means it said Don't merge and the code compiles.")
    print()
    for line in table([("Go", go), ("Java", java)], "language"):
        print(line)
    print()
    for lang, rows in (("Go", go), ("Java", java)):
        if not rows:
            continue
        print(f"## {lang} by project")
        print()
        groups = collections.OrderedDict()
        for r in sorted(rows, key=lambda r: (r["project"], r["mode"])):
            groups.setdefault(f"{r['project']} ({r['mode']})", []).append(r)
        for line in table(groups.items(), "project (what)"):
            print(line)
        print()
    bad = [r for r in allrows if r["compiler"] == "breaks" and r["build"] == "GO"]
    print(f"## Missed: {len(bad)}")
    print()
    for r in bad:
        print(f"- {r['lang']} {r['project']} {r['mode']} {r['id']} (verifier's answer: {WORD.get(r['verdict'], r['verdict'])}, build line: Merge): "
              f"compiler: {'; '.join(r.get('errors') or [r['where']])[:300]}")
    alarms = [r for r in allrows if r["compiler"] == "compiles" and r["build"] == "NO_GO"]
    print()
    print(f"## False alarms: {len(alarms)}")
    print()
    for r in alarms:
        print(f"- {r['lang']} {r['project']} {r['mode']} {r['id']}: verifier cites `{r['where']}`")
    print()
    print("## Needs review, by reason")
    print()
    for lang, rows in (("Go", go), ("Java", java)):
        c = collections.Counter()
        for r in rows:
            if r["build"] == "UNKNOWN" or r["verdict"] == "UNKNOWN":
                for reason in r["reasons"] or ["(none given)"]:
                    c[reason] += 1
        if c:
            print(f"- {lang}: " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    print()
    print("## Not judged by the compiler, by reason")
    print()
    for lang, rows in (("Go", go), ("Java", java)):
        c = collections.Counter(r["compiler"] for r in rows if r["compiler"] not in ("breaks", "compiles"))
        if c:
            print(f"- {lang}: " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    errs = [r for r in allrows if r["verdict"] == "ERROR" or r.get("error")]
    print()
    print(f"## Errors: {len(errs)}")
    print()
    for r in errs[:40]:
        print(f"- {r['lang']} {r['project']} {r['mode']} {r['id']}: {r['error'][:240]}")
    jobs = []
    for f in glob.glob("stress/results/*/*/*/job-*.json") + glob.glob("stress/results/go/history/*/*/job-*.json"):
        try:
            j = json.load(open(f, encoding="utf-8"))
            jobs.append((j.get("seconds", 0), f.replace("\\", "/")))
        except (OSError, ValueError):
            pass
    if jobs:
        jobs.sort(reverse=True)
        print()
        print(f"## Job minutes: {len(jobs)} jobs, slowest {jobs[0][0] / 60:.1f} min ({jobs[0][1]}), "
              f"{sum(1 for s, _ in jobs if s > 1800)} over 30 min")


if __name__ == "__main__":
    main()
