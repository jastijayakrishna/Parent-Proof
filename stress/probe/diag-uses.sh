#!/usr/bin/env bash
# Decides one Go window again and prints, for the findings whose evidence is in
# files matching PATTERN, each finding and each evidence use as the bound
# footprint holds it (kind, symbol, shipped, module), and the generated
# packages the caller's footprint matched to the contract.
# Usage: diag-uses.sh PROVIDER_URL CONSUMER_URL CONSUMER_REV BASE HEAD PATTERN OUT
set -uo pipefail
p=$1 c=$2 crev=$3 base=$4 head=$5 pat=$6 out=$7
work=$RUNNER_TEMP/diag
mkdir -p "$work" "$out"
git clone -q "$p" "$work/p"
git clone -q "$c" "$work/c" && git -C "$work/c" checkout -q "$crev"
"$RUNNER_TEMP/verifier" verify --repo "$work/p" --base "$base" --head "$head" --callers "$work/c" --out "$work/rec.json" > "$out/verify.txt" 2>&1
echo "== verify exit $?"
python3 - "$work/rec.json" "$pat" <<'PY'
import json, sys
rec = json.load(open(sys.argv[1])); pat = sys.argv[2]
d = rec["decision"]
print("VERDICT", d["verdict"], d["aspects"])
for c in rec.get("callers") or []:
    fp = c.get("footprint") or {}
    print("CALLER", c.get("repo"), c.get("deploy_unit"), "generated:", (fp.get("generated_version") or "")[:600])
    n = 0
    for u in fp.get("uses") or []:
        loc = u.get("location") or {}
        if pat in loc.get("file", "") and n < 12:
            n += 1
            print("   USE", loc.get("file"), loc.get("line"), u.get("kind"), (u.get("symbol") or {}).get("name"), "shipped=", u.get("shipped", False), "module=", u.get("module", ""))
seen = 0
for f in d.get("findings") or []:
    ev = [e for e in (f.get("evidence") or []) if pat in (e.get("location") or {}).get("file", "")]
    if ev and seen < 8:
        seen += 1
        print("FINDING", f.get("outcome"), f.get("aspect"), f.get("rule"), (f.get("symbol") or {}).get("name"), "|", (f.get("detail") or "")[:200])
PY
