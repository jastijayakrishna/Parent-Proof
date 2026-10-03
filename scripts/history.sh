#!/usr/bin/env bash
# One history job: mines every pin bump of $SUITE's provider in $CONSUMER's
# history since $SINCE, lets the compiler judge shard $SHARD (i/N) of the
# breaking ones and of a sample of additive ones, then decides each with the
# pinned verifier. Writes out/{windows,results}-<shard>.jsonl and log tails.
set -uo pipefail

shard=${SHARD:-1/1}
tag=${shard/\//of}
tmp=${RUNNER_TEMP:-/tmp}
mkdir -p out "$tmp/suite"
bin="$tmp/verifier"
gunzip -c bin/verifier-linux-amd64.gz > "$bin"
chmod +x "$bin"

suite="$tmp/suite/$SUITE.suite.json"
cp "history/suites/$SUITE.suite.json" "$suite"

echo "mining $SUITE -> $CONSUMER since $SINCE, shard $shard"
timeout 200m "$bin" suite build --suite "$suite" --oss "$tmp/oss" --work "$tmp/build" \
  --consumers "$CONSUMER" --since "$SINCE" --additive "${ADDITIVE:-6}" --workers 2 --shard "$shard" > "$tmp/build.log" 2>&1
echo "suite build exit $?"
tail -c 6000 "$tmp/build.log" > "out/build-$tag.log"
cp "$tmp/suite/$SUITE.jsonl" "out/windows-$tag.jsonl" 2>/dev/null || : > "out/windows-$tag.jsonl"
echo "windows mined: $(wc -l < "out/windows-$tag.jsonl")"

: > "out/results-$tag.jsonl"
if [ -s "out/windows-$tag.jsonl" ]; then
  timeout 120m "$bin" gate --suite "$suite" --oss "$tmp/oss" --work "$tmp/gate" --workers 2 \
    --consumers "$CONSUMER" --out "out/results-$tag.jsonl" --timeout 20m > "$tmp/gate.log" 2>&1
  echo "gate exit $?"
  tail -c 6000 "$tmp/gate.log" > "out/gate-$tag.log"
fi
{ "$bin" version 2>&1 | head -1; sha256sum "$bin" | cut -c1-64; } > out/verifier.txt
tail -5 "out/gate-$tag.log" 2>/dev/null
tail -5 "out/build-$tag.log"

# A one-line summary as a run annotation, readable without access to the logs.
mined=$(wc -l < "out/windows-$tag.jsonl")
breaking=$(grep -c '"select":"breaking"' "out/windows-$tag.jsonl" 2>/dev/null || true)
total=$(grep -m1 '^TOTAL' "out/gate-$tag.log" 2>/dev/null | cut -c1-400)
err=$(grep -m1 -iE 'error|fatal|refus|no such|not found' "out/build-$tag.log" 2>/dev/null | cut -c1-300)
echo "::notice title=$SUITE -> $CONSUMER ($shard)::compiled $mined upgrades ($breaking breaking). ${total:-no decisions}. ${err:+first error: $err}"
