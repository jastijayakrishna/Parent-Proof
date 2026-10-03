#!/usr/bin/env bash
# Prints SCOREBOARD.md from every record under predictions/: what the verifier
# predicted for each pull request, and where the Go compiler judged it.
set -euo pipefail
shopt -s nullglob
files=(predictions/*/*.json)

{
  echo "# Scoreboard"
  echo
  echo "Every row is one pull request that changed a .proto file, decided by the"
  echo "verifier before the compiler built the consumer against it. Wrong GO: the"
  echo "verifier said the consumer still builds, the compiler says it breaks. False"
  echo "NO-GO: the verifier said it breaks, the compiler says it builds."
  echo
  if [ ${#files[@]} -eq 0 ]; then
    echo "No predictions yet."
    exit 0
  fi
  jq -s -r '
    [ .[] | .pr as $pr | .exit as $exit | (.results // [])[] |
      { eco: $pr.eco, n: $pr.n, url: $pr.url, title: $pr.title,
        verdict: .verdict, build: (.aspects.source_build // ""),
        compiler: (.oracle.outcome // "not judged"),
        reasons: ((.unknown_reasons // []) | join(", ")) } ] as $w
    | ($w | map(select(.compiler == "breaks" or .compiler == "compiles"))) as $j
    | ($j | map(select(.build == "GO" and .compiler == "breaks"))) as $wrong
    | ($j | map(select(.build == "NO_GO" and .compiler == "compiles"))) as $false
    | "| decided | GO | NO-GO | UNKNOWN | compiler judged | agree | wrong GO | false NO-GO |",
      "|---|---|---|---|---|---|---|---|",
      "| \($w | length) | \($w | map(select(.verdict == "GO")) | length) | \($w | map(select(.verdict == "NO_GO")) | length) | \($w | map(select(.verdict == "UNKNOWN")) | length) | \($j | length) | \($j | length - ($wrong | length) - ($false | length) - ($j | map(select(.build == "UNKNOWN")) | length)) | \($wrong | length) | \($false | length) |",
      "",
      "## Every pull request",
      "",
      "| project | pull request | verdict | build | compiler | UNKNOWN because |",
      "|---|---|---|---|---|---|",
      ($w | sort_by(.eco, .n)[] | "| \(.eco) | [#\(.n)](\(.url)) \(.title | gsub("\\|"; "/")) | \(.verdict) | \(.build) | \(.compiler) | \(.reasons) |")
  ' "${files[@]}"
}
