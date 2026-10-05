#!/usr/bin/env bash
# Prints, as a JSON array, the open pull requests of the providers in
# corpus.json, and of stress/corpus.json's sets in $STRESS_SETS (default dev),
# that change a .proto file, were updated in the last DAYS days,
# and have no prediction yet for their current head. At most MAX_PRS, taken
# round-robin (each project's newest first) so every project gets its turn.
set -euo pipefail

api() {
  curl -fsSL -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" "https://api.github.com/$1"
}

max=${MAX_PRS:-20}
per=${PER_PROJECT:-5}
since=$(date -u -d "${DAYS:-14} days ago" +%Y-%m-%dT%H:%M:%SZ)
all='[]'

while IFS= read -r e; do
  eco=$(jq -r .name <<<"$e")
  prov=$(jq -r .provider.url <<<"$e" | sed -E 's#https://github.com/##; s#\.git$##')
  cons=$(jq -r .consumer.url <<<"$e" | sed -E 's#https://github.com/##; s#\.git$##')
  prs=$(api "repos/$prov/pulls?state=open&sort=updated&direction=desc&per_page=30") || { echo "skip $eco: cannot list pull requests" >&2; continue; }
  consumer_head=""
  if [ "$prov" != "$cons" ]; then
    consumer_head=$(api "repos/$cons/commits/HEAD" | jq -r .sha) || { echo "skip $eco: cannot read $cons" >&2; continue; }
  fi
  rank=0
  while IFS= read -r row; do
    [ "$rank" -ge "$per" ] && break
    n=$(jq -r .n <<<"$row")
    head=$(jq -r .head <<<"$row")
    key="$eco-$n-${head:0:12}"
    [ -e "predictions/$eco/$key.json" ] && continue
    files=$(api "repos/$prov/pulls/$n/files?per_page=100") || continue
    jq -e 'any(.[]; .filename | endswith(".proto"))' <<<"$files" >/dev/null || continue
    # In a repository that is both provider and consumer, the pull request's
    # own consumer code is what merges with its contract change.
    csha=${consumer_head:-$head}
    all=$(jq -c --argjson r "$row" --arg eco "$eco" --arg key "$key" --arg prov "$prov" --arg cons "$cons" --arg csha "$csha" --argjson rank "$rank" \
      '. + [$r + {eco: $eco, key: $key, provider: $prov, consumer: $cons, consumer_sha: $csha, rank: $rank}]' <<<"$all")
    rank=$((rank + 1))
  done < <(jq -c --arg s "$since" '.[] | select(.updated_at >= $s and (.draft | not)) | {n: .number, head: .head.sha, base: .base.sha, title: .title, url: .html_url, updated: .updated_at}' <<<"$prs")
done < <(jq -c '.ecosystems[]' corpus.json; jq -c --arg sets "${STRESS_SETS:-dev}" '.ecosystems[] | select(.set as $s | $sets | split(",") | index($s) != null)' stress/corpus.json)

jq -c --argjson max "$max" 'to_entries | sort_by(.value.rank, .key) | map(.value | del(.rank)) | .[:$max]' <<<"$all"
