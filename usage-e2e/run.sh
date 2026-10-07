#!/usr/bin/env bash
# Usage records end to end: publish a service's records, decide a contract
# change from them, then attack the records every way the store must refuse.
# Each case must give its verdict and reason exactly, and none may say Merge.
#
#   run.sh VERIFIER OUT github   in GitHub Actions: the store is this
#                                repository, the records are signed by the run
#   run.sh VERIFIER OUT local    anywhere: a bare repository as the store and
#                                unsigned records (only a CI run can sign);
#                                the cases about signatures need github
#
# OUT/cases.txt: one line per case; OUT/result.txt: passed: true|false.
set -u
v="$1"; out="$2"; mode="${3:-github}"
here="$(cd "$(dirname "$0")" && pwd)"
tmp="${E2E_TMP:-$(mktemp -d)}"; rm -rf "$tmp"; mkdir -p "$tmp"
PY="$(command -v python3 || command -v python)"
export GIT_AUTHOR_NAME=e2e GIT_AUTHOR_EMAIL=e2e@parent.invalid GIT_COMMITTER_NAME=e2e GIT_COMMITTER_EMAIL=e2e@parent.invalid
rm -rf "$out"; mkdir -p "$out"; : > "$out/cases.txt"; : > "$out/timings.txt"
fail=0

if [ "$mode" = github ]; then
  STORE="https://github.com/$GITHUB_REPOSITORY.git"; REPO="github.com/$GITHUB_REPOSITORY"; REF="$GITHUB_REF"
  AUTH="https://x-access-token:${VERIFIER_USAGE_TOKEN}@github.com/$GITHUB_REPOSITORY.git"
  UNREACHABLE="https://github.com/$GITHUB_REPOSITORY-no-such-store.git"
  sign=(); trial=()
else
  STORE="$tmp/store.git"; git init -q --bare "$STORE"; REPO=github.com/acme/billing; REF=refs/heads/main
  AUTH="$STORE"; UNREACHABLE="$tmp/no-such-store.git"
  sign=(--unsigned); trial=(--unsigned)
fi
branch="usage/$REPO"

ms() { echo $(( ($(date +%s%N) - $1) / 1000000 )); }

# The service: the billing fixture as a repository of its own, two commits.
svc="$tmp/billing"; cp -r "$here/billing" "$svc"
(cd "$svc" && git init -q -b main && git add -A && git commit -q -m billing)
older=$(git -C "$svc" rev-parse HEAD)
(cd "$svc" && echo "# billing" > NOTES.md && git add NOTES.md && git commit -q -m notes)
commit=$(git -C "$svc" rev-parse HEAD)

# publish NAME COMMIT
publish() {
  local t0; t0=$(date +%s%N)
  "$v" usage publish ${sign[@]+"${sign[@]}"} --store "$STORE" --dir "$svc" --repo "$REPO" --commit "$2" --ref "$REF" > "$out/$1.out" 2>&1
  echo "exit $?" >> "$out/$1.out"
  echo "$1 $(ms "$t0") ms" >> "$out/timings.txt"
}

# report NAME OK DETAIL
report() {
  printf '%-18s %-5s %s\n' "$1" "$2" "$3" >> "$out/cases.txt"
  [ "$2" = true ] || fail=1
}

publish publish "$commit"
ok=true
grep -q '^exit 0$' "$out/publish.out" || ok=false
if [ "$mode" = github ]; then grep -q 'signed by this CI run' "$out/publish.out" || ok=false; fi
report publish "$ok" "$(grep -m1 '^Published' "$out/publish.out" | cut -c1-80)"

# A rerun of an older pipeline never moves the store back.
publish publish-older "$older"
ok=true; grep -q '^exit 0$' "$out/publish-older.out" && grep -q '^Not published' "$out/publish-older.out" || ok=false
report publish-older "$ok" "$(grep -m1 '^Not published' "$out/publish-older.out" | cut -c1-80)"

# The provider: payments.proto, then the removal of amount_cents, which both
# of billing's deploy units read.
prov="$tmp/payments-protos"; mkdir -p "$prov/proto/payments/v1"
cp "$here/provider/payments.proto" "$prov/proto/payments/v1/"
(cd "$prov" && git init -q -b main && git add -A && git commit -q -m contract && \
  sed -i '/int64 amount_cents = 7;/d' proto/payments/v1/payments.proto && git commit -q -am "remove amount_cents")

# decide NAME STORE [FLAGS...]: the change, decided from STORE.
decide() {
  local name="$1" store="$2" t0; shift 2
  t0=$(date +%s%N)
  "$v" verify --repo "$prov" --base HEAD~1 --usage "$store" --out "$out/$name.json" "$@" > "$out/$name.out" 2>&1
  echo "exit $?" >> "$out/$name.out"
  echo "$name $(ms "$t0") ms" >> "$out/timings.txt"
}

# expect NAME VERDICT REASON [TEXT]: decision NAME is VERDICT with REASON
# among its reasons ("-": no reason), TEXT in its output, and exit 3 (not Merge).
expect() {
  local name="$1" want="$2" reason="$3" text="${4:-}" got verdict reasons ok=true
  got=$("$PY" -c 'import json,sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))["decision"]
    print(d["verdict"], ",".join(d.get("unknown_reasons") or []) or "-")
except Exception:
    print("NONE -")' "$out/$name.json")
  verdict="${got%% *}"; reasons="${got#* }"
  [ "$verdict" = "$want" ] || ok=false
  if [ "$reason" = - ]; then [ "$reasons" = - ] || ok=false
  else case ",$reasons," in *",$reason,"*) ;; *) ok=false ;; esac; fi
  [ -z "$text" ] || grep -qF -- "$text" "$out/$name.out" || ok=false
  grep -q '^exit 3$' "$out/$name.out" || ok=false
  report "$name" "$ok" "$verdict $reasons"
}

# From the store as published.
decide signed "$STORE" ${trial[@]+"${trial[@]}"}
expect signed NO_GO - "2 of 2 deploy units break"
ok=true; grep -qF 'Checked 1 service(s) from the usage store' "$out/signed.out" || ok=false
report signed-scope "$ok" "$(grep -m1 -o 'Checked [0-9]* service(s)' "$out/signed.out")"

if [ "$mode" = github ]; then
  wf="$GITHUB_REPOSITORY/.github/workflows/usage-e2e.yml"
  decide pinned "$STORE" --workflow "$wf";                expect pinned NO_GO -
  decide pinned-ref "$STORE" --workflow "$wf@$REF";       expect pinned-ref NO_GO -
  decide pin-other "$STORE" --workflow "$GITHUB_REPOSITORY/.github/workflows/gates.yml"
  expect pin-other UNKNOWN USAGE_SIGNATURE_INVALID
  # The run's real ref extends the pinned one (refs/heads/mai vs …/main): a
  # branch named main-evil against a pin of main, seen from the other side.
  decide pin-sibling "$STORE" --workflow "$wf@${REF%?}";  expect pin-sibling UNKNOWN USAGE_SIGNATURE_INVALID
  decide pin-prefix "$STORE" --workflow "${wf%.yml}";     expect pin-prefix UNKNOWN USAGE_SIGNATURE_INVALID
  # The issuer's keys cannot be fetched.
  decide issuer-down "$STORE" --oidc-issuer "https://issuer.invalid"
  expect issuer-down UNKNOWN USAGE_SIGNATURE_INVALID
fi

sleep 2
decide expired "$STORE" ${trial[@]+"${trial[@]}"} --max-age 1s
expect expired UNKNOWN USAGE_RECORD_EXPIRED
decide unreachable "$UNREACHABLE" ${trial[@]+"${trial[@]}"}
expect unreachable UNKNOWN USAGE_STORE_UNREACHABLE

# Attacks on copies of the published branch, each a store of its own.
base="$tmp/base"
git clone -q --depth 1 --branch "$branch" "$AUTH" "$base" && rm -rf "$base/.git"
cat > "$tmp/drop-record.py" <<'EOF'
import json
i = json.load(open("index.json", encoding="utf-8"))
del i["records"][sorted(i["records"])[0]]
open("index.json", "w", encoding="utf-8").write(json.dumps(i))
EOF
# attacked NAME BRANCH COMMANDS: the published branch, changed by COMMANDS
# (run in its checkout), at BRANCH of a new store; prints the store.
attacked() {
  local w="$tmp/w-$1" s="$tmp/s-$1.git"
  cp -r "$base" "$w"
  (cd "$w" && eval "$3") >&2
  git init -q --bare "$s"
  (cd "$w" && git init -q -b x && git add -A && git commit -q -m "$1" && git push -q "$s" "HEAD:refs/heads/$2") >&2
  echo "$s"
}

s=$(attacked unsigned "$branch" 'rm -f index.jwt')
decide unsigned "$s";  expect unsigned UNKNOWN USAGE_RECORD_UNSIGNED
s=$(attacked other-service usage/github.com/acme/other ':')
decide other-service "$s" ${trial[@]+"${trial[@]}"};  expect other-service UNKNOWN USAGE_SIGNATURE_INVALID
s=$(attacked record-tampered "$branch" 'printf x >> records/billing-worker@*.json.gz')
decide record-tampered "$s" ${trial[@]+"${trial[@]}"};  expect record-tampered NO_GO USAGE_DIGEST_MISMATCH
s=$(attacked records-tampered "$branch" 'for f in records/*.json.gz; do printf x >> "$f"; done')
decide records-tampered "$s" ${trial[@]+"${trial[@]}"};  expect records-tampered UNKNOWN USAGE_DIGEST_MISMATCH
s=$(attacked record-deleted "$branch" 'rm -f records/billing-worker@*.json.gz')
decide record-deleted "$s" ${trial[@]+"${trial[@]}"};  expect record-deleted NO_GO USAGE_DIGEST_MISMATCH
if [ "$mode" = github ]; then
  # Hiding a deploy unit by editing the signed index.
  s=$(attacked index-edited "$branch" "\"$PY\" \"$tmp/drop-record.py\"")
  decide index-edited "$s";  expect index-edited UNKNOWN USAGE_SIGNATURE_INVALID
  # The default branch's signed records replayed as an open pull request's.
  s=$(attacked pr-replay "usage-pr/$REPO/5" ':')
  decide pr-replay "$s";  expect pr-replay UNKNOWN USAGE_SIGNATURE_INVALID
fi

# Tampering with the store itself: the next check fetches the new tip.
t="$tmp/tamper"; git clone -q --depth 1 --branch "$branch" "$AUTH" "$t"
(cd "$t" && printf x >> records/billing-worker@*.json.gz && git commit -q -am tamper && git push -q origin "HEAD:$branch")
decide store-tampered "$STORE" ${trial[@]+"${trial[@]}"}
expect store-tampered NO_GO USAGE_DIGEST_MISMATCH

# Leave no store behind.
if [ "$mode" = github ]; then git push -q "$AUTH" --delete "$branch" || true; fi

pass=true; [ "$fail" = 0 ] || pass=false
echo "passed: $pass" > "$out/result.txt"
cat "$out/cases.txt" "$out/result.txt"
$pass
