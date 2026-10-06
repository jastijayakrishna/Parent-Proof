# Stress test: Go and Java consumers

Updated 2026-10-06 11:17 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language, set | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go dev | 149 | 82 | 7 | 7 | **0** | 0 | 28 (19%) | 0 |
| Go holdout | 254 | 207 | 20 | 12 | **0** | 5 | 58 (23%) | 0 |
| Java dev | 451 | 97 | 19 | 18 | **0** | 0 | 13 (3%) | 0 |
| Java holdout | 51 | 0 | 0 | 0 | **0** | 0 | 5 (10%) | 0 |
| Java regression | 84 | 75 | 5 | 5 | **0** | 0 | 21 (27%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (live) | 3 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 9 (45%) | 0 |
| buildkit -> buildx (history) | 104 | 103 | 19 | 11 | **0** | 0 | 16 (15%) | 0 |
| buildkit-buildx (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| cometbft -> cosmos-sdk (history) | 41 | 40 | 6 | 6 | **0** | 0 | 3 (7%) | 0 |
| cometbft-cosmos-sdk (scan) | 20 | 19 | 1 | 1 | **0** | 0 | 3 (15%) | 0 |
| cosmos-sdk -> gaia (history) | 32 | 31 | 1 | 1 | **0** | 3 | 10 (31%) | 0 |
| cosmos-sdk-gaia (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 14 (70%) | 0 |
| csi-attacher (scan) | 20 | 17 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| csi-provisioner (live) | 2 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| csi-provisioner (scan) | 20 | 17 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| csi-spec -> external-attacher (history) | 6 | 6 | 0 | 0 | **0** | 0 | 3 (50%) | 0 |
| csi-spec -> external-provisioner (history) | 6 | 6 | 0 | 0 | **0** | 0 | 3 (50%) | 0 |
| kubelet -> k8s-device-plugin (history) | 17 | 0 | 0 | 0 | **0** | 0 | 1 (6%) | 0 |
| kubelet-device-plugin (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 2 (10%) | 0 |
| otlp-tempo (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| otlp-tempo -> tempo (history) | 12 | 12 | 0 | 0 | **0** | 2 | 0 (0%) | 0 |
| vitess (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 1 (5%) | 0 |

## Java by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| beam (history) | 8 | 0 | 0 | 0 | **0** | 0 | 2 (33%) | 0 |
| camunda-zeebe (history) | 55 | 12 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 9 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| conductor (history) | 25 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-bigtable-history (history) | 43 | 0 | 0 | 0 | **0** | 0 | 3 (7%) | 0 |
| google-cloud-pubsub (history) | 19 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-pubsub-history (history) | 248 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 56 | 16 | 16 | **0** | 0 | 5 (9%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 27 | 19 | 2 | 1 | **0** | 0 | 7 (27%) | 0 |
| temporal-sdk-java (scan) | 20 | 10 | 0 | 0 | **0** | 0 | 1 (10%) | 0 |

## Missed: 0


## False alarms: 5

- Go cosmos-sdk -> gaia history v0.53.4 -> v0.53.8: verifier cites `app/keepers/keepers.go:595`
- Go cosmos-sdk -> gaia history v0.45.16-ics-lsm -> v0.47.7-0.20240117142932-85b42a599468: verifier cites `ante/ante.go:60`
- Go cosmos-sdk -> gaia history v0.50.11-lsm.0.20250523173923-11578258172e -> v0.53.0: verifier cites `app/sim/sim_state.go:247`
- Go otlp-tempo -> tempo history v1.7.1 -> v1.9.0: verifier cites `vendor/go.opentelemetry.io/collector/pdata/internal/generated_wrapper_location.go:100`
- Go otlp-tempo -> tempo history v1.5.0 -> v1.6.0: verifier cites `vendor/go.opentelemetry.io/collector/pdata/pprofile/generated_profile.go:101`

## Needs review, by reason

- Go: CONTRACT_COMPILE_ERROR 41, GO_API_CHANGED_USED_BY_CALLER 28, DESCRIPTOR_REFLECTION 21, OPTION_CHANGED 16, NEEDS_REVIEW 14, SECOND_CHECK_DISAGREES 6, WHOLE_MESSAGE_FLOW 4, UNRESOLVED_MEMBER 3, TYPE_ERROR_HIDES_USES 3
- Java: OPTION_CHANGED 26, NEEDS_REVIEW 12, CONTRACT_COMPILE_ERROR 7, JAVA_INLINED_CONSTANTS_UNCHECKED 6, DESCRIPTOR_REFLECTION 2, WHOLE_MESSAGE_FLOW 2

## Not judged by the compiler, by reason

- Go: not judged 66, baseline_fails 39, bump_side_effect 6, judge not verified 2, oracle_error 1
- Java: oracle_error 259, judge not verified 85, baseline_fails 70

## Errors: 0


## Job minutes: 94 jobs, slowest 39.1 min (stress/results/java/beam/history/job-2of17.json), 1 over 30 min
