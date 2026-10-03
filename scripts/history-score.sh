#!/usr/bin/env bash
# Prints HISTORY.md from history/results/<suite>/<consumer>/results.jsonl:
# for every real upgrade the consumer made, what the verifier decided and what
# the Go compiler says about the consumer's code at that upgrade.
set -euo pipefail
shopt -s nullglob
files=(history/results/*/*/results*.jsonl)

echo "# History: real upgrades, judged by the compiler"
echo
echo "Every row is one upgrade a project really made of a contract module it"
echo "uses, mined from its git history. The Go compiler builds the project's code"
echo "at that upgrade against the old and the new module. A break is an upgrade"
echo "the compiler says breaks the build; caught means the verifier said NO-GO for"
echo "the build. None of these projects was used to tune the verifier."
echo
if [ ${#files[@]} -eq 0 ]; then
  echo "No results yet."
  exit 0
fi
for f in "${files[@]}"; do
  s=$(basename "$(dirname "$(dirname "$f")")")
  c=$(basename "$(dirname "$f")")
  jq -c --arg s "$s" --arg c "$c" '. + {suite: $s, consumer_name: $c}' "$f"
done | jq -s -r '
  map({suite, c: .consumer_name, w: .window, v: (.observed.verdict // "ERROR"),
       build: (.observed.aspects.source_build // ""), compiler: (.window.oracle.outcome // "not judged"),
       reasons: ((.observed.unknown_reasons // []) | join(", "))}) as $all
  | ($all | map(select(.compiler == "breaks"))) as $breaks
  | ($all | map(select(.compiler == "compiles"))) as $safe
  | "| upgrades | compiler breaks | caught | wrong GO | compiler-safe | GO | false NO-GO | UNKNOWN (build) |",
    "|---|---|---|---|---|---|---|---|",
    "| \($all | length) | \($breaks | length) | \($breaks | map(select(.build == "NO_GO")) | length) | \($breaks | map(select(.build == "GO")) | length) | \($safe | length) | \($safe | map(select(.build == "GO")) | length) | \($safe | map(select(.build == "NO_GO")) | length) | \($all | map(select(.build == "UNKNOWN")) | length) |",
    "",
    "## By project",
    "",
    "| contract -> project | upgrades | breaks | caught | wrong GO | false NO-GO | UNKNOWN |",
    "|---|---|---|---|---|---|---|",
    ($all | group_by(.suite + "/" + .c)[] |
      "| \(.[0].suite) -> \(.[0].c) | \(length) | \(map(select(.compiler == "breaks")) | length) | \(map(select(.compiler == "breaks" and .build == "NO_GO")) | length) | \(map(select(.compiler == "breaks" and .build == "GO")) | length) | \(map(select(.compiler == "compiles" and .build == "NO_GO")) | length) | \(map(select(.build == "UNKNOWN")) | length) |"),
    "",
    "## Every break and every disagreement",
    "",
    "| contract -> project | upgrade | compiler | verifier (build) | UNKNOWN because |",
    "|---|---|---|---|---|",
    ($all | map(select(.compiler == "breaks" or (.compiler == "compiles" and .build == "NO_GO") or .build == "UNKNOWN"))[] |
      "| \(.suite) -> \(.c) | \(.w.old_pin // "") -> \(.w.new_pin // "") | \(.compiler) | \(.v) (\(.build)) | \(.reasons) |")
'
