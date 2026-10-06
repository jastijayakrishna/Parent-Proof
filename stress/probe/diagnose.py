#!/usr/bin/env python3
"""Reruns one window of a Java stress project and prints what the verifier
saw: the contract changes, the findings, the callers, and the implementations
and uses its footprint holds for the services and files the change touches;
then the compiler's answer with its errors. Usage: diagnose.py NAME MODE ID OUT.
Needs the verifier at $RUNNER_TEMP/verifier."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "java"))
import harness  # noqa: E402

name, mode, wid, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
p = harness.project(name)
ws = harness.windows(p, mode)
w = next(x for x in ws if x["id"].startswith(wid))
r = harness.run_window(p, w, out)
print(json.dumps({k: r[k] for k in r if k not in ("verifier",)}, indent=1)[:6000])
v = r.get("verifier") or {}
print("VERDICT", v.get("verdict"), v.get("aspects"), v.get("unknown_reasons"))
rec_path = os.path.join(out, v.get("record", ""))
if not v.get("record") or not os.path.exists(rec_path):
    print("no record", v.get("error", "")[:2000])
    sys.exit(0)
rec = json.load(open(rec_path, encoding="utf-8"))
d = rec.get("decision", {})
changes = d.get("changes") or []
java_changes = d.get("java_changes") or []
print(f"CHANGES {len(changes)} (java {len(java_changes)})")
for c in (changes + java_changes)[:40]:
    print("  ", c.get("kind"), (c.get("symbol") or {}).get("kind"), (c.get("symbol") or {}).get("name"), c.get("file", ""))
print("FINDINGS", len(d.get("findings") or []))
for f in (d.get("findings") or [])[:30]:
    ev = [f"{(u.get('location') or {}).get('file')}:{(u.get('location') or {}).get('line')}" for u in (f.get("evidence") or [])[:3]]
    print("  ", f.get("outcome"), f.get("aspect"), f.get("rule"), (f.get("symbol") or {}).get("name"), ev, (f.get("detail") or "")[:160])
print("CALLERS", [(c.get("caller", {}).get("deploy_unit"), c.get("outcome"), c.get("reasons")) for c in d.get("callers") or []])
touched = set()
for c in changes + java_changes:
    s = (c.get("symbol") or {}).get("name", "")
    touched.add(s.split("#")[0])
    if "." in s:
        touched.add(s.rsplit(".", 1)[0])
for c in rec.get("callers") or []:
    fp = c.get("footprint") or {}
    uses = fp.get("uses") or []
    print(f"FOOTPRINT {fp.get('deploy_unit')} lang={fp.get('language')} analyzer={fp.get('analyzer_version')} uses={len(uses)} gaps={len(fp.get('gaps') or [])}")
    for g in (fp.get("gaps") or [])[:8]:
        print("   gap", g.get("code"), (g.get("detail") or "")[:200])
    impl = [u for u in uses if u.get("kind") == "implement"]
    print(f"   implement uses: {len(impl)}")
    for u in impl[:40]:
        print("    ", (u.get("symbol") or {}).get("name"), u.get("note"), u.get("has_default"), (u.get("location") or {}).get("file"), (u.get("location") or {}).get("line"), len(u.get("cases") or []))
    hits = [u for u in uses if any(t and t in ((u.get("symbol") or {}).get("name") or "") for t in touched)]
    print(f"   uses of touched symbols: {len(hits)}")
    for u in hits[:40]:
        print("    ", u.get("kind"), (u.get("symbol") or {}).get("name"), (u.get("location") or {}).get("file"), (u.get("location") or {}).get("line"), u.get("note", ""))
o = r.get("oracle") or {}
print("COMPILER", o.get("outcome"), o.get("errors", [])[:10])
