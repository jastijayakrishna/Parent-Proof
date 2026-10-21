# Stress test: Go and Java consumers

Updated 2026-10-21 10:19 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language, set | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go dev | 185 | 85 | 7 | 7 | **0** | 0 | 38 (21%) | 0 |
| Go holdout | 256 | 206 | 22 | 12 | **0** | 2 | 63 (25%) | 0 |
| Java dev | 372 | 61 | 12 | 12 | **0** | 0 | 9 (3%) | 0 |
| Java holdout | 467 | 13 | 1 | 1 | **0** | 0 | 111 (32%) | 70 |
| Java regression | 70 | 55 | 5 | 5 | **0** | 0 | 21 (37%) | 0 |

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
| alluxio (history) | 27 | 13 | 1 | 1 | **0** | 0 | 2 (15%) | 0 |
| bazel (history) | 174 | 0 | 0 | 0 | **0** | 0 | 92 (88%) | 70 |
| beam (history) | 12 | 0 | 0 | 0 | **0** | 0 | 4 (50%) | 0 |
| camunda-zeebe (history) | 22 | 8 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 9 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 6 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| conductor (history) | 9 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-bigtable-history (history) | 254 | 0 | 0 | 0 | **0** | 0 | 13 (6%) | 0 |
| google-cloud-pubsub (history) | 10 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-pubsub-history (history) | 248 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 37 | 11 | 11 | **0** | 0 | 4 (9%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 14 | 10 | 1 | 1 | **0** | 0 | 4 (31%) | 0 |
| temporal-sdk-java (scan) | 12 | 6 | 0 | 0 | **0** | 0 | 1 (17%) | 0 |

## Missed: 0


## False alarms: 2

- Go cosmos-sdk -> gaia history v0.53.4 -> v0.53.8: verifier cites `app/keepers/keepers.go:595`
- Go cosmos-sdk -> gaia history v0.50.11-lsm.0.20250523173923-11578258172e -> v0.53.0: verifier cites `app/sim/sim_state.go:247`

## Needs review, by reason

- Go: CONTRACT_COMPILE_ERROR 55, GO_API_CHANGED_USED_BY_CALLER 28, DESCRIPTOR_REFLECTION 21, OPTION_CHANGED 16, NEEDS_REVIEW 15, AMBIENT_GENERATED_UNREAD 8, WHOLE_MESSAGE_FLOW 7, SECOND_CHECK_DISAGREES 7, UNRESOLVED_MEMBER 3, TYPE_ERROR_HIDES_USES 3
- Java: BAZEL_BUILD_NOT_READ 88, OPTION_CHANGED 24, CONTRACT_COMPILE_ERROR 22, NEEDS_REVIEW 13, JAVA_INLINED_CONSTANTS_UNCHECKED 5, JAVA_DYNAMIC_CODE 2, DESCRIPTOR_REFLECTION 2, WHOLE_MESSAGE_FLOW 2

## Not judged by the compiler, by reason

- Go: not judged 99, baseline_fails 39, bump_side_effect 8, oracle_error 2, judge not verified 2
- Java: oracle_error 397, not_built 174, judge not verified 105, baseline_fails 104

## Errors: 70

- Java bazel history a523c9bae3c0: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4097d9c5e814: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history cc335fd27e3f: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history dab6383ecef2: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4dc0d119a6f4: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 40d6780e2f33: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3e68f74f6f96: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 0e3bc1651a8c: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history ec0878f710c1: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 9f0f23211293: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 940b80fe9f6e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f4050eeddda5: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history fe64e59ce160: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history bd1c3af2ea14: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 54ef9629e361: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 40c731ab0834: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 1ce4ab15fab1: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history ad95b5492edf: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 0d7446cdb288: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history a0471c703bd0: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3dcb585fb2f2: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 19ecfc46d1c6: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 95bbed03758a: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 6999d55be31c: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 715a177a95bd: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4920115efbfa: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history c84737a98f01: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history d1975d893c52: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 58057c81c2d7: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 45cb268d96f7: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 5581066ddaee: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history b7b4dfcfedd2: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3510aded1062: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 9ed07e330516: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 22222ff19adc: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

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


## Job minutes: 115 jobs, slowest 40.0 min (stress/results/java/beam/history/job-25of40.json), 3 over 30 min
