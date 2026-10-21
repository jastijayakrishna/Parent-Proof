#!/usr/bin/env bash
# Diagnostic (scale/PREREG.md counts none of this): decide one missed change
# again with `verifier verify` and keep what explains the answer: the
# decision, the provider Go API facts, and what the caller's footprint
# recorded of the provider's hand-written code. Reads one line of
# scale/diag/why.txt: NAME PROVIDER_URL BASE HEAD CONSUMER_URL CONSUMER_REV GOMOD_DIR
set -uo pipefail
line=$(grep -v '^#' scale/diag/why.txt | grep -v '^bin=' | sed -n "${LINE}p")
# bin=FILE in scale/diag/why.txt picks the binary (default bin/verifier-linux-amd64.gz).
bin_file=$(sed -n 's/^bin=//p' scale/diag/why.txt); bin_file=${bin_file:-bin/verifier-linux-amd64.gz}
read -r name purl base head curl crev gdir <<< "$line"
out="scale/diag/why/$name"
mkdir -p "$out"
tmp=${RUNNER_TEMP:-/tmp}
bin="$tmp/verifier"
gunzip -c "$bin_file" > "$bin" && chmod +x "$bin"
git clone -q --filter=blob:none "$purl" "$tmp/p" && git -C "$tmp/p" fetch -q origin "$base" "$head" 2>/dev/null
git clone -q "$curl" "$tmp/c" && git -C "$tmp/c" checkout -q "$crev"
callers="$tmp/c/${gdir:-.}"
"$bin" verify --repo "$tmp/p" --base "$base" --head "$head" --callers "$callers" --json --out "$out/record.json" > "$out/verify.json" 2> "$out/verify.err"
echo "exit $?" >> "$out/verify.err"
python3 - "$out" <<'PY'
import json, sys, os
out = sys.argv[1]
rec = json.load(open(os.path.join(out, "record.json")))
d = rec.get("decision", {})
s = {"verdict": d.get("verdict"), "aspects": d.get("aspects"), "changes": len(d.get("changes") or []),
     "go_only": rec.get("go_only"), "contract_files": len(rec.get("contract_files") or []),
     "provider_api_error": rec.get("provider_api_error"),
     "generated_gone": rec.get("generated_gone"), "contract_outside": rec.get("contract_outside"),
     "findings": [{k: f.get(k) for k in ("rule", "outcome", "aspect", "symbol", "reason", "detail")} for f in d.get("findings") or []][:40],
     # Every finding that needs review, with where it points (file:line, sink).
     "unknown_findings": [dict({k: f.get(k) for k in ("rule", "reason", "symbol", "detail")}, evidence=[json.dumps(e)[:600] for e in (f.get("evidence") or [])[:4]])
                          for f in d.get("findings") or [] if f.get("outcome") == "UNKNOWN"][:60],
     "callers": [{"unit": (c.get("caller") or {}).get("deploy_unit"), "outcome": c.get("outcome")} for c in d.get("callers") or []][:20]}
api = rec.get("provider_api") or {}
s["provider_api_facts"] = {k: (v if len(json.dumps(v)) < 400 else json.dumps(v)[:400]) for k, v in list(api.items())[:40]} if isinstance(api, dict) else str(api)[:2000]
uses = []
for c in rec.get("callers") or []:
    fp = c.get("footprint") or {}
    for u in fp.get("provider_api") or []:
        uses.append(u)
s["caller_provider_api_uses"] = len(uses)
s["caller_provider_api_sample"] = uses[:40]
json.dump(s, open(os.path.join(out, "summary.json"), "w"), indent=1)
print(json.dumps({k: s[k] for k in ("verdict", "aspects", "changes", "go_only", "contract_files", "caller_provider_api_uses")}))
PY
rm -f "$out/record.json"
