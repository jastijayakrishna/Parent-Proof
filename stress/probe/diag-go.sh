#!/usr/bin/env bash
# Decides Go provider windows again with the verifier, as the scan does
# (local.Verify of the consumer at its commit, the provider's head against
# its base), and prints every change and finding with its evidence: rule,
# outcome, aspect, detail, file:line and the name it stands for, which a scan
# row has no room for. Then the compiler's answer, as `gate scan` judges it.
# Usage: diag-go.sh PROVIDER_URL CONSUMER_URL CONSUMER_COMMIT OUT HEAD:BASE...
# Needs the verifier at $RUNNER_TEMP/verifier.
set -uo pipefail
p=$1 c=$2 csha=$3 out=$4
shift 4
work=$RUNNER_TEMP/diag
mkdir -p "$work" "$out"
git clone -q "$p" "$work/p"
git clone -q "$c" "$work/c" && git -C "$work/c" checkout -q "$csha"
for w in "$@"; do
  head=${w%%:*} base=${w##*:} id=${w:0:12}
  "$RUNNER_TEMP/verifier" verify --repo "$work/p" --base "$base" --head "$head" --callers "$work/c" --out "$out/rec-$id.json" > "$out/verify-$id.txt" 2>&1
  echo "== $head (base $base): exit $?"
  python3 - "$out/rec-$id.json" <<'PY'
import json, sys
try:
    rec = json.load(open(sys.argv[1]))
except OSError as e:
    print("no record:", e)
    sys.exit(0)
d = rec["decision"]
print("VERDICT", d["verdict"], d["aspects"], d.get("unknown_reasons"))
for c in d.get("changes") or []:
    print("CHANGE", c.get("kind"), c.get("symbol"), c.get("old"), c.get("new"))
for f in d.get("findings") or []:
    ev = []
    for e in (f.get("evidence") or [])[:8]:
        loc = e.get("location") or {}
        ev.append(f"{loc.get('file', '')}:{loc.get('line', '')} {e.get('kind', '')} {e.get('member', '')} {e.get('note', '')}".strip())
    print("FINDING", f.get("outcome"), f.get("aspect"), f.get("rule"), "|", (f.get("detail") or "")[:500])
    for x in ev:
        print("   ", x)
PY
done
