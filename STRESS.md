# Stress test: Go and Java consumers

Updated 2026-10-21 10:52 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language, set | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go dev | 185 | 85 | 7 | 7 | **0** | 0 | 38 (21%) | 0 |
| Go holdout | 256 | 206 | 22 | 12 | **0** | 2 | 63 (25%) | 0 |
| Java dev | 414 | 66 | 11 | 11 | **0** | 0 | 9 (3%) | 0 |
| Java holdout | 475 | 6 | 1 | 1 | **0** | 0 | 136 (39%) | 35 |
| Java regression | 77 | 46 | 2 | 2 | **0** | 0 | 21 (44%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (live) | 36 | 0 | 0 | 0 | **0** | 0 | 14 (39%) | 0 |
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 9 (45%) | 0 |
| buildkit -> buildx (history) | 106 | 105 | 19 | 11 | **0** | 0 | 16 (15%) | 0 |
| buildkit-buildx (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| cometbft -> cosmos-sdk (history) | 41 | 40 | 6 | 6 | **0** | 0 | 3 (7%) | 0 |
| cometbft-cosmos-sdk (live) | 1 | 1 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| cometbft-cosmos-sdk (scan) | 20 | 19 | 1 | 1 | **0** | 0 | 3 (15%) | 0 |
| cosmos-sdk -> gaia (history) | 32 | 28 | 3 | 1 | **0** | 2 | 10 (31%) | 0 |
| cosmos-sdk-gaia (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 14 (70%) | 0 |
| csi-attacher (scan) | 20 | 17 | 0 | 0 | **0** | 0 | 3 (15%) | 0 |
| csi-provisioner (live) | 4 | 2 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| csi-provisioner (scan) | 20 | 17 | 0 | 0 | **0** | 0 | 3 (15%) | 0 |
| csi-spec -> external-attacher (history) | 6 | 6 | 0 | 0 | **0** | 0 | 3 (50%) | 0 |
| csi-spec -> external-provisioner (history) | 6 | 6 | 0 | 0 | **0** | 0 | 3 (50%) | 0 |
| kubelet -> k8s-device-plugin (history) | 17 | 0 | 0 | 0 | **0** | 0 | 1 (6%) | 0 |
| kubelet-device-plugin (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 2 (10%) | 0 |
| otlp-tempo (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 2 (10%) | 0 |
| otlp-tempo -> tempo (history) | 12 | 12 | 0 | 0 | **0** | 0 | 7 (58%) | 0 |
| vitess (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 1 (5%) | 0 |

## Java by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| alluxio (history) | 27 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| bazel (history) | 174 | 0 | 0 | 0 | **0** | 0 | 118 (85%) | 35 |
| beam (history) | 20 | 0 | 0 | 0 | **0** | 0 | 6 (40%) | 0 |
| camunda-zeebe (history) | 36 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 13 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| conductor (history) | 17 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-bigtable-history (history) | 254 | 0 | 0 | 0 | **0** | 0 | 12 (6%) | 0 |
| google-cloud-pubsub (history) | 19 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-pubsub-history (history) | 248 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 31 | 10 | 10 | **0** | 0 | 2 (5%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 21 | 15 | 1 | 1 | **0** | 0 | 6 (30%) | 0 |
| temporal-sdk-java (scan) | 16 | 8 | 0 | 0 | **0** | 0 | 1 (12%) | 0 |

## Missed: 0


## False alarms: 2

- Go cosmos-sdk -> gaia history v0.53.4 -> v0.53.8: verifier cites `app/keepers/keepers.go:595`
- Go cosmos-sdk -> gaia history v0.50.11-lsm.0.20250523173923-11578258172e -> v0.53.0: verifier cites `app/sim/sim_state.go:247`

## Needs review, by reason

- Go: CONTRACT_COMPILE_ERROR 55, GO_API_CHANGED_USED_BY_CALLER 28, DESCRIPTOR_REFLECTION 21, OPTION_CHANGED 16, NEEDS_REVIEW 15, AMBIENT_GENERATED_UNREAD 8, WHOLE_MESSAGE_FLOW 7, SECOND_CHECK_DISAGREES 7, UNRESOLVED_MEMBER 3, TYPE_ERROR_HIDES_USES 3
- Java: BAZEL_BUILD_NOT_READ 113, OPTION_CHANGED 25, CONTRACT_COMPILE_ERROR 23, NEEDS_REVIEW 10, JAVA_INLINED_CONSTANTS_UNCHECKED 5, WHOLE_MESSAGE_FLOW 2, DESCRIPTOR_REFLECTION 1

## Not judged by the compiler, by reason

- Go: not judged 99, baseline_fails 39, bump_side_effect 8, oracle_error 2, judge not verified 2
- Java: oracle_error 375, baseline_fails 183, not_built 174, judge not verified 116

## Errors: 35

- Java bazel history 3c5f4cc77196: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 9731e6906cba: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3774f0057922: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history c68ef68e821e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 8b75e0b2b9c1: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 718f400c61e2: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4b7c808ec913: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 2d93597df29e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 746d261ab4cc: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4bcf8552d32e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f51eaab090c1: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3e2a3c1ffdbb: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 73b0faff39ed: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 89c486654df3: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3010caeb83dc: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 9392f8f24ead: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history c2f539c899e3: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history e5ab94bfdebb: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4b38f2fdc9a6: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 779d6976f8fe: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 7879fac3ad36: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history a7167d384e7d: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 91b1e8e28afc: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 97f182ae36fd: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history cb24261bde72: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history ca9413484c61: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history aa4b847b27a4: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 585e16c701a6: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 60b1e19baa4d: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 2ce32e70485a: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 7e58b1069395: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 65b4adbf6c81: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 56c4403bbb1e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history cb8de5c6bfcf: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 7e63e204eeb5: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above


## Job minutes: 135 jobs, slowest 40.0 min (stress/results/java/beam/history/job-22of40.json), 7 over 30 min
