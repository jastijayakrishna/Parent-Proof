#!/usr/bin/env bash
# Prints SCOREBOARD.md from every record under predictions/: what the verifier
# said about each pull request, and where the Go compiler judged it.
set -euo pipefail
shopt -s nullglob
files=(predictions/*/*.json)

{
  echo "# Scoreboard"
  echo
  echo "Updated $(date -u '+%Y-%m-%d %H:%M') UTC."
  echo
  echo "Every row is one pull request that changed a .proto file, decided by the"
  echo "verifier before the compiler built the consumer against it."
  echo
  echo "- **Missed**: the verifier said *Merge*, the compiler says the consumer breaks."
  echo "- **False alarm**: the verifier said *Don't merge*, the compiler says it builds."
  echo "- **Needs review**: the verifier could not tell; the row says why."
  echo
  if [ ${#files[@]} -eq 0 ]; then
    echo "No predictions yet."
    exit 0
  fi
  jq -s -r '
    def word: {"GO": "Merge", "NO_GO": "Don'"'"'t merge", "UNKNOWN": "Needs review"}[.] // .;
    [ .[] | .pr as $pr | (.results // [])[] |
      { eco: $pr.eco, n: $pr.n, url: $pr.url, title: $pr.title,
        verdict: .verdict, build: (.aspects.source_build // ""),
        compiler: (.oracle.outcome // "not judged"),
        reasons: ((.unknown_reasons // []) | join(", ")) } ] as $w
    | ($w | map(select(.compiler == "breaks" or .compiler == "compiles"))) as $j
    | ($j | map(select(.build == "GO" and .compiler == "breaks"))) as $missed
    | ($j | map(select(.build == "NO_GO" and .compiler == "compiles"))) as $alarm
    | "| pull requests | Merge | Don'"'"'t merge | Needs review | compiler judged | agree | missed | false alarm |",
      "|---|---|---|---|---|---|---|---|",
      "| \($w | length) | \($w | map(select(.verdict == "GO")) | length) | \($w | map(select(.verdict == "NO_GO")) | length) | \($w | map(select(.verdict == "UNKNOWN")) | length) | \($j | length) | \($j | length - ($missed | length) - ($alarm | length) - ($j | map(select(.build == "UNKNOWN")) | length)) | \($missed | length) | \($alarm | length) |",
      "",
      "## Every pull request",
      "",
      "| project | pull request | verifier | for the build | compiler | needs review because |",
      "|---|---|---|---|---|---|",
      ($w | sort_by(.eco, .n)[] | "| \(.eco) | [#\(.n)](\(.url)) \(.title | gsub("[|]"; "/")) | \(.verdict | word) | \(.build | word) | \(.compiler) | \(.reasons) |")
  ' "${files[@]}"
}
