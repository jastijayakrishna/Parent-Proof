# Stress test: Go and Java consumers

Updated 2026-10-21 12:03 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language, set | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go dev | 185 | 85 | 7 | 7 | **0** | 0 | 38 (21%) | 0 |
| Go holdout | 256 | 206 | 22 | 12 | **0** | 2 | 63 (25%) | 0 |
| Java dev | 451 | 80 | 10 | 9 | **0** | 0 | 10 (3%) | 0 |
| Java holdout | 492 | 0 | 0 | 0 | **0** | 0 | 166 (50%) | 0 |
| Java regression | 84 | 46 | 2 | 2 | **0** | 0 | 21 (44%) | 0 |

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
| alluxio (history) | 27 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| bazel (history) | 174 | 0 | 0 | 0 | **0** | 0 | 146 (84%) | 0 |
| beam (history) | 37 | 0 | 0 | 0 | **0** | 0 | 13 (42%) | 0 |
| camunda-zeebe (history) | 55 | 16 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| conductor (history) | 25 | 8 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-bigtable-history (history) | 254 | 0 | 0 | 0 | **0** | 0 | 7 (5%) | 0 |
| google-cloud-pubsub (history) | 19 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-pubsub-history (history) | 248 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 27 | 7 | 7 | **0** | 0 | 2 (6%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 27 | 19 | 2 | 1 | **0** | 0 | 7 (27%) | 0 |
| temporal-sdk-java (scan) | 20 | 10 | 0 | 0 | **0** | 0 | 1 (10%) | 0 |

## Missed: 0


## False alarms: 2

- Go cosmos-sdk -> gaia history v0.53.4 -> v0.53.8: verifier cites `app/keepers/keepers.go:595`
- Go cosmos-sdk -> gaia history v0.50.11-lsm.0.20250523173923-11578258172e -> v0.53.0: verifier cites `app/sim/sim_state.go:247`

## Needs review, by reason

- Go: CONTRACT_COMPILE_ERROR 55, GO_API_CHANGED_USED_BY_CALLER 28, DESCRIPTOR_REFLECTION 21, OPTION_CHANGED 16, NEEDS_REVIEW 15, AMBIENT_GENERATED_UNREAD 8, WHOLE_MESSAGE_FLOW 7, SECOND_CHECK_DISAGREES 7, UNRESOLVED_MEMBER 3, TYPE_ERROR_HIDES_USES 3
- Java: BAZEL_BUILD_NOT_READ 140, CONTRACT_COMPILE_ERROR 26, OPTION_CHANGED 26, NEEDS_REVIEW 9, JAVA_INLINED_CONSTANTS_UNCHECKED 5, WHOLE_MESSAGE_FLOW 3, DESCRIPTOR_REFLECTION 1

## Not judged by the compiler, by reason

- Go: not judged 99, baseline_fails 39, bump_side_effect 8, oracle_error 2, judge not verified 2
- Java: oracle_error 332, baseline_fails 277, not_built 174, judge not verified 118

## Errors: 0


## Job minutes: 170 jobs, slowest 40.0 min (stress/results/java/beam/history/job-22of40.json), 23 over 30 min
