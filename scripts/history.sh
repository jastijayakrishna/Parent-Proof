#!/usr/bin/env bash
# One history job: mines every pin bump of $SUITE's provider in $CONSUMER's
# history since $SINCE (the compiler judging every breaking one and a sample
# of additive ones), then decides each with the pinned verifier. Writes
# out/results.jsonl, out/windows.jsonl and the tails of both logs.
set -uo pipefail

tmp=${RUNNER_TEMP:-/tmp}
mkdir -p out "$tmp/suite"
bin="$tmp/verifier"
gunzip -c bin/verifier-linux-amd64.gz > "$bin"
chmod +x "$bin"

suite="$tmp/suite/$SUITE.suite.json"
cp "history/suites/$SUITE.suite.json" "$suite"

echo "mining $SUITE -> $CONSUMER since $SINCE"
timeout 200m "$bin" suite build --suite "$suite" --oss "$tmp/oss" --work "$tmp/build" \
  --consumers "$CONSUMER" --since "$SINCE" --additive "${ADDITIVE:-6}" --workers 2 > "$tmp/build.log" 2>&1
echo "suite build exit $?"
tail -c 6000 "$tmp/build.log" > out/build.log
cp "$tmp/suite/$SUITE.jsonl" out/windows.jsonl 2>/dev/null || : > out/windows.jsonl
echo "windows mined: $(wc -l < out/windows.jsonl)"

: > out/results.jsonl
if [ -s out/windows.jsonl ]; then
  timeout 120m "$bin" gate --suite "$suite" --oss "$tmp/oss" --work "$tmp/gate" --workers 2 \
    --consumers "$CONSUMER" --out out/results.jsonl --timeout 20m > "$tmp/gate.log" 2>&1
  echo "gate exit $?"
  tail -c 6000 "$tmp/gate.log" > out/gate.log
fi
"$bin" version 2>&1 | head -1 > out/verifier.txt
sha256sum "$bin" | cut -c1-64 >> out/verifier.txt
tail -5 out/gate.log 2>/dev/null
tail -5 out/build.log

# A one-line summary as a run annotation, readable without access to the logs.
mined=$(wc -l < out/windows.jsonl)
breaking=$(grep -c '"select":"breaking"' out/windows.jsonl 2>/dev/null || true)
total=$(grep -m1 '^TOTAL' out/gate.log 2>/dev/null | cut -c1-400)
err=$(grep -m1 -iE 'error|fatal|refus|no such|not found' out/build.log 2>/dev/null | cut -c1-300)
echo "::notice title=$SUITE -> $CONSUMER::mined $mined upgrades ($breaking breaking). ${total:-no decisions}. ${err:+first error: $err}"
