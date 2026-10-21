#!/usr/bin/env bash
# Decision-only rerun (scale/after, not part of the pre-registered count):
# the windows a history job committed, with the compiler's answers and the
# judge's canary frozen as they were recorded, decided again by the binary
# BIN_FILE. Inputs: SUITE, CONSUMER, BIN_FILE, SUITE_DIR (default
# scale/suites), SRC (the committed results directory; default
# scale/results/history/$SUITE/$CONSUMER, its windows-*.jsonl and
# canary-*.jsonl; or WINDOWS, one windows file), DEST (where to write).
set -uo pipefail
tmp=${RUNNER_TEMP:-/tmp}
suite_dir=${SUITE_DIR:-scale/suites}
src=${SRC:-scale/results/history/$SUITE/$CONSUMER}
dest=${DEST:?}
mkdir -p "$dest" "$tmp/suite"
bin="$tmp/verifier"
gunzip -c "$BIN_FILE" > "$bin" && chmod +x "$bin"
suite="$tmp/suite/$SUITE.suite.json"
cp "$suite_dir/$SUITE.suite.json" "$suite"
windows=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['windows'])" "$suite")
python3 - "$src" "${WINDOWS:-}" "$tmp/suite/$windows" "$CONSUMER" <<'PY'
import glob, json, os, sys
src, one, dst, consumer = sys.argv[1:5]
files = [one] if one else sorted(glob.glob(os.path.join(src, "windows-*.jsonl")))
seen = {}
for f in files:
    for line in open(f, encoding="utf-8"):
        if line.strip():
            w = json.loads(line)
            if w.get("consumer") == consumer:
                seen[w["bump"]] = w
with open(dst, "w", encoding="utf-8") as o:
    for k in sorted(seen):
        o.write(json.dumps(seen[k]) + "\n")
print(f"{len(seen)} windows of {consumer}")
PY
# The judge's canary, as it was recorded: its answers count only if it broke.
cp "$src"/canary-*.jsonl "$dest"/ 2>/dev/null || true
started=$(date +%s)
timeout 25m "$bin" gate --suite "$suite" --oss "$tmp/oss" --work "$tmp/gate" --workers 2 --consumers "$CONSUMER" \
  --out "$dest/results-1of1.jsonl" --timeout 20m > "$tmp/gate.log" 2>&1
echo "gate exit $? seconds $(( $(date +%s) - started ))" >> "$tmp/gate.log"
tail -c 6000 "$tmp/gate.log" > "$dest/gate-1of1.log"
{ "$bin" version 2>&1 | head -1; sha256sum "$bin" | cut -c1-64; } > "$dest/verifier.txt"
tail -3 "$dest/gate-1of1.log"
