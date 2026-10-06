#!/usr/bin/env bash
# Decides one Go provider window again with the verifier and prints what its
# check of the provider's hand-written Go code saw: whether the change was
# read as Go-only, the caller's uses of the provider's Go code by module, the
# facts the check read at base and head, and every use whose package or name
# matches PATTERN. Then where the consumer's own code names PATTERN.
# Usage: diag-goapi.sh PROVIDER_URL CONSUMER_URL CONSUMER_COMMIT BASE HEAD PATTERN OUT
# Needs the verifier at $RUNNER_TEMP/verifier.
set -uo pipefail
p=$1 c=$2 csha=$3 base=$4 head=$5 pat=$6 out=$7
work=$RUNNER_TEMP/diag
mkdir -p "$work" "$out"
git clone -q "$p" "$work/p"
git clone -q "$c" "$work/c" && git -C "$work/c" checkout -q "$csha"
echo "== consumer $(git -C "$work/c" rev-parse HEAD), provider $base -> $head"
echo "== provider Go files changed: $(git -C "$work/p" diff --name-only "$base" "$head" -- '*.go' | grep -v _test.go | wc -l), .proto changed: $(git -C "$work/p" diff --name-only "$base" "$head" -- '*.proto' | wc -l)"
git -C "$work/p" diff --stat "$base" "$head" -- '*.go' | grep -i "$pat" | head -20
echo "== consumer files naming $pat (not tests):"
grep -rln --include=*.go "$pat" "$work/c" | grep -v _test.go | sed "s|$work/c/||" | head -20
"$RUNNER_TEMP/verifier" verify -v --repo "$work/p" --base "$base" --head "$head" --callers "$work/c" --out "$out/rec.json" > "$out/verify.txt" 2>&1
echo "== verify exit $?"
tail -40 "$out/verify.txt"
python3 - "$out/rec.json" "$pat" <<'PY'
import json, sys, collections
pat = sys.argv[2]
try:
    rec = json.load(open(sys.argv[1]))
except OSError as e:
    print("no record:", e)
    sys.exit(0)
d = rec["decision"]
print("VERDICT", d["verdict"], d["aspects"], "go_only", rec.get("go_only"), "provider_api_error", rec.get("provider_api_error"))
facts = rec.get("provider_api") or {}
print("FACTS modules", facts.get("modules"))
for k, v in sorted((facts.get("decls") or {}).items()):
    if pat in k:
        print("FACT", k, v)
for m in rec.get("missing") or []:
    print("MISSING", m.get("caller"), m.get("reason"), (m.get("detail") or "")[:300])
for c in rec.get("callers") or []:
    fp = c.get("footprint") or {}
    uses = fp.get("provider_api") or []
    by = collections.Counter(u.get("module") for u in uses)
    print("CALLER", c.get("repo"), c.get("deploy_unit"), "uses of provider Go code:", len(uses), dict(by))
    for u in uses:
        if pat in (u.get("package", "") + "." + u.get("name", "")):
            print("   USE", u.get("module"), u.get("package"), u.get("name"), u.get("member", ""), (u.get("location") or {}), u.get("in", ""))
    gens = sorted({x.get("go_import", "") + " @" + x.get("module", "") for x in (fp.get("descriptors") or [])})
    print("   generated packages:", len(gens), gens[:5])
for f in d.get("findings") or []:
    print("FINDING", f.get("outcome"), f.get("aspect"), f.get("rule"), "|", (f.get("detail") or "")[:400])
PY
