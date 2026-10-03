#!/usr/bin/env bash
# Decides one pull request (the JSON object in $PR) with the pinned verifier,
# lets the Go compiler judge the consumer against it, and writes the record to
# out/<key>.json. The verifier never sees the compiler's answer.
set -uo pipefail

eco=$(jq -r .eco <<<"$PR")
key=$(jq -r .key <<<"$PR")
n=$(jq -r .n <<<"$PR")
head=$(jq -r .head <<<"$PR")
csha=$(jq -r .consumer_sha <<<"$PR")
tmp=${RUNNER_TEMP:-/tmp}
oss="$tmp/oss"
mkdir -p out "$oss"

bin="$tmp/verifier"
gunzip -c bin/verifier-linux-amd64.gz > "$bin"
chmod +x "$bin"

# The corpus entry of this ecosystem, pinned to the pull request's head and
# the consumer's commit, deciding only the last contract commit.
jq --arg eco "$eco" --arg head "$head" --arg csha "$csha" \
  '{description: "one pull request", limit: 1, max_unknown_percent: 100,
    ecosystems: [.ecosystems[] | select(.name == $eco) | .provider.commit = $head | .consumer.commit = $csha]}' \
  corpus.json > "$tmp/corpus.json"

# A pull request's head is reachable only from its pull ref: fetch it into
# the clones the scan reuses.
purl=$(jq -r '.ecosystems[0].provider.url' "$tmp/corpus.json")
curl_=$(jq -r '.ecosystems[0].consumer.url' "$tmp/corpus.json")
git clone --quiet --filter=blob:none --no-checkout "$purl" "$oss/p-$eco"
git -C "$oss/p-$eco" fetch --quiet origin "pull/$n/head"
if [ "$purl" = "$curl_" ]; then
  git clone --quiet --filter=blob:none --no-checkout "$curl_" "$oss/c-$eco"
  git -C "$oss/c-$eco" fetch --quiet origin "pull/$n/head"
fi

started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
: > "$tmp/scan.jsonl"
timeout 40m "$bin" gate scan --corpus "$tmp/corpus.json" --only "$eco" --oracle \
  --oss "$oss" --work "$tmp/work" --out "$tmp/scan.jsonl" > "$tmp/scan.out" 2>&1
rc=$?

jq -n --argjson pr "$PR" --arg started "$started" --arg finished "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg version "$("$bin" version 2>&1 | head -1)" --arg sha "$(sha256sum "$bin" | cut -c1-64)" \
  --arg run "${GITHUB_SERVER_URL:-}/${GITHUB_REPOSITORY:-}/actions/runs/${GITHUB_RUN_ID:-}" \
  --argjson rc "$rc" --slurpfile results "$tmp/scan.jsonl" \
  '{pr: $pr, started: $started, finished: $finished, run: $run,
    verifier: {version: $version, sha256: $sha}, exit: $rc, results: $results}' > "out/$key.json"

tail -30 "$tmp/scan.out"
