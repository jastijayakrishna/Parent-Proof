#!/usr/bin/env bash
# Decides one pull request (the JSON object in $PR) with the pinned verifier,
# lets the Go compiler judge the consumer against it, and writes the record to
# out/<key>.json. The verifier never sees the compiler's answer.
set -uo pipefail

eco=$(jq -r .eco <<<"$PR")
key=$(jq -r .key <<<"$PR")
n=$(jq -r .n <<<"$PR")
head=$(jq -r .head <<<"$PR")
base=$(jq -r .base <<<"$PR")
csha=$(jq -r .consumer_sha <<<"$PR")
tmp=${RUNNER_TEMP:-/tmp}
oss="$tmp/oss"
mkdir -p out "$oss"

bin="$tmp/verifier"
gunzip -c bin/verifier-linux-amd64.gz > "$bin"
chmod +x "$bin"

# The ecosystem's entry, from corpus.json or the stress test's corpus.
entry=$(jq -c --arg eco "$eco" '.ecosystems[] | select(.name == $eco)' corpus.json stress/corpus.json | head -1)
purl=$(jq -r .provider.url <<<"$entry")
curl_=$(jq -r .consumer.url <<<"$entry")
: > "$tmp/scan.out"

# A pull request's head is reachable only from its pull ref: fetch it into the
# clones the scan reuses. The whole pull request is decided as one change: a
# local commit holding the head's files on the merge base (nothing is pushed
# anywhere).
export GIT_AUTHOR_NAME=proto-shadow GIT_AUTHOR_EMAIL=proto-shadow@localhost
export GIT_COMMITTER_NAME=proto-shadow GIT_COMMITTER_EMAIL=proto-shadow@localhost
{
  git clone --quiet --filter=blob:none --no-checkout "$purl" "$oss/p-$eco"
  git -C "$oss/p-$eco" fetch --quiet origin "pull/$n/head" "$base"
  if [ "$purl" = "$curl_" ]; then
    git clone --quiet --filter=blob:none --no-checkout "$curl_" "$oss/c-$eco"
    git -C "$oss/c-$eco" fetch --quiet origin "pull/$n/head"
  fi
} >> "$tmp/scan.out" 2>&1
mbase=$(git -C "$oss/p-$eco" merge-base "$head" "$base" 2>> "$tmp/scan.out")
whole=$(git -C "$oss/p-$eco" commit-tree "$head^{tree}" -p "$mbase" -m "pull request $n as one change" 2>> "$tmp/scan.out")

# The corpus entry of this ecosystem, pinned to that commit and the consumer's
# commit, deciding that one change.
jq -n --argjson e "$entry" --arg whole "$whole" --arg csha "$csha" \
  '{description: "one pull request", limit: 1, max_unknown_percent: 100,
    ecosystems: [$e | .provider.commit = $whole | .consumer.commit = $csha]}' > "$tmp/corpus.json"

started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
: > "$tmp/scan.jsonl"
timeout 40m "$bin" gate scan --corpus "$tmp/corpus.json" --only "$eco" --oracle \
  --oss "$oss" --work "$tmp/work" --out "$tmp/scan.jsonl" >> "$tmp/scan.out" 2>&1
rc=$?

jq -n --argjson pr "$PR" --arg mbase "$mbase" --arg whole "$whole" \
  --arg started "$started" --arg finished "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg version "$("$bin" version 2>&1 | head -1)" --arg sha "$(sha256sum "$bin" | cut -c1-64)" \
  --arg run "${GITHUB_SERVER_URL:-}/${GITHUB_REPOSITORY:-}/actions/runs/${GITHUB_RUN_ID:-}" \
  --argjson rc "$rc" --slurpfile results "$tmp/scan.jsonl" --arg log "$(tail -c 4000 "$tmp/scan.out" 2>/dev/null)" \
  '{pr: $pr, merge_base: $mbase, decided: $whole, started: $started, finished: $finished, run: $run,
    verifier: {version: $version, sha256: $sha}, exit: $rc, results: $results, log: $log}' > "out/$key.json"

tail -30 "$tmp/scan.out"
