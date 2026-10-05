#!/usr/bin/env python3
"""Rewrites the live part of README.md, between <!-- live:begin --> and
<!-- live:end -->, from the records: the real upgrades of the history
(history/results), the open pull requests (predictions), and every real
break the verifier called Don't merge before the compiler judged it."""
import datetime
import glob
import json
import os
import re

REPO = "jastijayakrishna/Parent-Proof"


def history():
    rows = []
    for path in sorted(glob.glob("history/results/*/*/results-*.jsonl")):
        parts = path.replace("\\", "/").split("/")
        suite, consumer = parts[-3], parts[-2]
        with open(f"history/suites/{suite}.suite.json", encoding="utf-8") as f:
            repo = json.load(f)["consumers"][consumer]["repo"]
        with open(path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                w, o = r["window"], r.get("observed") or {}
                rows.append({
                    "what": f"{suite} → {consumer}",
                    "link": f"https://github.com/{repo}/commit/{w.get('bump', '')}",
                    "change": f"{w.get('old_pin', '')} → {w.get('new_pin', '')}",
                    "date": w.get("date", ""),
                    "build": (o.get("aspects") or {}).get("source_build", ""),
                    "compiler": (w.get("oracle") or {}).get("outcome", "not judged"),
                    "where": (o.get("evidence") or [""])[0],
                })
    return rows


def live():
    rows = []
    for path in sorted(glob.glob("predictions/*/*.json")):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        pr = r.get("pr") or {}
        for res in r.get("results") or []:
            rows.append({
                "what": pr.get("eco", ""),
                "link": pr.get("url", ""),
                "change": f"#{pr.get('n', '')} {pr.get('title', '')}",
                "date": (pr.get("updated") or "")[:10],
                "verdict": res.get("verdict", ""),
                "build": (res.get("aspects") or {}).get("source_build", ""),
                "compiler": (res.get("oracle") or {}).get("outcome", "not judged"),
                "where": "",
            })
    return rows


def counts(rows, by_verdict):
    breaks = [r for r in rows if r["compiler"] == "breaks"]
    safe = [r for r in rows if r["compiler"] == "compiles"]
    review = [r for r in rows if (r.get("verdict") == "UNKNOWN" if by_verdict else r["build"] == "UNKNOWN")]
    return (len(rows), len(breaks), sum(r["build"] == "NO_GO" for r in breaks), sum(r["build"] == "GO" for r in breaks),
            sum(r["build"] == "NO_GO" for r in safe), len(review))


def cell(s):
    return str(s).replace("|", "/")


def render(now):
    h, l = history(), live()
    out = [
        f"**Updated {now:%Y-%m-%d %H:%M} UTC.** "
        f"[![shadow](https://github.com/{REPO}/actions/workflows/shadow.yml/badge.svg)](https://github.com/{REPO}/actions/workflows/shadow.yml)",
        "",
        "| | changes | broke the build | caught | missed | false alarms | needs review |",
        "|---|---|---|---|---|---|---|",
    ]
    hc, lc = counts(h, False), counts(l, True)
    projects = len({r["what"] for r in h})
    out.append(f"| [Real upgrades](HISTORY.md), {projects} projects' history | " + " | ".join(map(str, hc)) + " |")
    out.append("| [Open pull requests](SCOREBOARD.md), decided live | " + " | ".join(map(str, lc)) + " |")
    out.append("")
    out.append("**Caught**: it broke the build and the verifier said Don't merge first. **Missed**: the verifier said "
               "Merge and the compiler says it breaks, the failure that matters most.")
    out.append("")
    catches = [r for r in h + l if r["compiler"] == "breaks" and r["build"] == "NO_GO"]
    catches.sort(key=lambda r: r["date"], reverse=True)
    out.append(f"### Catches: {len(catches)} real breaks, each called Don't merge before the compiler built it")
    out.append("")
    out.append("| contract → project | change | date | where it breaks |")
    out.append("|---|---|---|---|")
    for r in catches:
        where = f"`{cell(r['where'])}`" if r["where"] else ""
        out.append(f"| {cell(r['what'])} | [{cell(r['change'])}]({r['link']}) | {r['date']} | {where} |")
    return "\n".join(out)


def main():
    with open("README.md", encoding="utf-8") as f:
        readme = f.read()
    body = render(datetime.datetime.now(datetime.timezone.utc))
    new, n = re.subn(r"<!-- live:begin -->.*?<!-- live:end -->",
                     lambda _: "<!-- live:begin -->\n" + body + "\n<!-- live:end -->", readme, flags=re.S)
    if n != 1:
        raise SystemExit("README.md: no <!-- live:begin --> ... <!-- live:end --> section")
    with open("README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(new)


if __name__ == "__main__":
    main()
