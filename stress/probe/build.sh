#!/usr/bin/env bash
# Build trial of one Java project of stress/java/projects.json at its pinned
# commit (no verifier runs): a cold build, then a clean rebuild with the
# dependency caches warm (what each window costs twice), and the compiled
# class directories the verifier would read. Usage: build.sh NAME OUT_DIR.
set -uo pipefail
name=$1 out=$2
mkdir -p "$out"
cfg() { python3 stress/java/cfg.py "$name" "$1"; }
repo=$(cfg consumer.repo) commit=$(cfg consumer.commit) jdk=$(cfg jdk)
build=$(cfg build) clean=$(cfg clean) prebuild=$(cfg prebuild) subs=$(cfg submodules)
src="${RUNNER_TEMP:-/tmp}/src-$name"

t0=$(date +%s)
git clone -q --filter=blob:none --no-checkout "https://github.com/$repo.git" "$src"
git -C "$src" checkout -q "$commit"
for s in $subs; do git -C "$src" submodule update -q --init -- "$s"; done
echo "clone seconds $(( $(date +%s) - t0 ))"
du -sh "$src" 2>/dev/null

jh="JAVA_HOME_${jdk}_X64"
export JAVA_HOME=${!jh:-$JAVA_HOME}
export PATH="$JAVA_HOME/bin:$PATH"
java -version 2>&1 | head -1
mvn -version 2>&1 | head -1

summary() { python3 - "$@" <<'EOF'
import json, sys, os
out, name, cold, crc, warm, wrc, src = sys.argv[1:8]
dirs = []
for root, ds, fs in os.walk(src):
    if "/.git" in root or "/node_modules" in root:
        continue
    rel = os.path.relpath(root, src)
    if rel.endswith(("target/classes", "build/classes/java/main", "build/classes/kotlin/main")):
        n = sum(len([f for f in files if f.endswith(".class")]) for _, _, files in os.walk(root))
        dirs.append({"dir": rel, "classes": n})
        ds[:] = []
json.dump({"name": name, "cold_seconds": int(cold), "cold_exit": int(crc), "warm_clean_seconds": int(warm), "warm_exit": int(wrc),
           "class_dirs": len(dirs), "classes": sum(d["classes"] for d in dirs), "dirs": dirs}, open(os.path.join(out, "summary.json"), "w"), indent=1)
print(f"class dirs {len(dirs)}, classes {sum(d['classes'] for d in dirs)}")
EOF
}

if [ -z "$build" ]; then
  echo "no build for $name"
  summary "$out" "$name" 0 0 0 0 "$src"
  exit 0
fi
cd "$src"
if [ -n "$prebuild" ]; then
  t0=$(date +%s); bash -c "$prebuild" > "$out/prebuild.log" 2>&1; echo "prebuild exit $? seconds $(( $(date +%s) - t0 ))"; tail -5 "$out/prebuild.log"
fi
t0=$(date +%s); timeout 40m bash -c "$build" > "$RUNNER_TEMP/cold.log" 2>&1; crc=$?; cold=$(( $(date +%s) - t0 ))
echo "cold build exit $crc seconds $cold"
tail -c 20000 "$RUNNER_TEMP/cold.log" > "$out/cold.log"
grep -E "ERROR|FAILURE|error:|BUILD" "$RUNNER_TEMP/cold.log" | head -40
wrc=-1 warm=0
if [ "$crc" = 0 ]; then
  bash -c "$clean" > /dev/null 2>&1
  t0=$(date +%s); timeout 30m bash -c "$build" > "$RUNNER_TEMP/warm.log" 2>&1; wrc=$?; warm=$(( $(date +%s) - t0 ))
  echo "warm clean build exit $wrc seconds $warm"
  tail -c 6000 "$RUNNER_TEMP/warm.log" > "$out/warm.log"
fi
cd - > /dev/null
summary "$out" "$name" "$cold" "$crc" "$warm" "$wrc" "$src"
df -h / | tail -1
