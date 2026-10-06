# Stress test: Go and Java consumers

Updated 2026-10-06 14:19 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language, set | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go dev | 149 | 81 | 7 | 7 | **0** | 0 | 24 (16%) | 0 |
| Go holdout | 254 | 204 | 22 | 12 | **0** | 4 | 58 (23%) | 0 |
| Java dev | 451 | 97 | 19 | 18 | **0** | 0 | 13 (3%) | 0 |
| Java holdout | 491 | 27 | 2 | 2 | **0** | 1 | 31 (10%) | 174 |
| Java regression | 84 | 75 | 5 | 5 | **0** | 0 | 21 (27%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (live) | 3 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 9 (45%) | 0 |
| buildkit -> buildx (history) | 104 | 103 | 19 | 11 | **0** | 0 | 16 (15%) | 0 |
| buildkit-buildx (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| cometbft -> cosmos-sdk (history) | 41 | 39 | 6 | 6 | **0** | 0 | 3 (7%) | 0 |
| cometbft-cosmos-sdk (scan) | 20 | 19 | 1 | 1 | **0** | 0 | 3 (15%) | 0 |
| cosmos-sdk -> gaia (history) | 32 | 28 | 3 | 1 | **0** | 2 | 10 (31%) | 0 |
| cosmos-sdk-gaia (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 14 (70%) | 0 |
| csi-attacher (scan) | 20 | 17 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| csi-provisioner (live) | 2 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| csi-provisioner (scan) | 20 | 17 | 0 | 0 | **0** | 0 | 3 (15%) | 0 |
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
| alluxio (history) | 27 | 27 | 2 | 2 | **0** | 1 | 5 (19%) | 0 |
| bazel (history) | 174 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 174 |
| beam (history) | 36 | 0 | 0 | 0 | **0** | 0 | 12 (40%) | 0 |
| camunda-zeebe (history) | 55 | 12 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 9 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| conductor (history) | 25 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-bigtable-history (history) | 254 | 0 | 0 | 0 | **0** | 0 | 14 (6%) | 0 |
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
- Go cosmos-sdk -> gaia history v0.50.11-lsm.0.20250523173923-11578258172e -> v0.53.0: verifier cites `app/sim/sim_state.go:247`
- Go otlp-tempo -> tempo history v1.7.1 -> v1.9.0: verifier cites `vendor/go.opentelemetry.io/collector/pdata/internal/generated_wrapper_location.go:100`
- Go otlp-tempo -> tempo history v1.5.0 -> v1.6.0: verifier cites `vendor/go.opentelemetry.io/collector/pdata/pprofile/generated_profile.go:101`
- Java alluxio history dbac084c1e1d: verifier cites ``

## Needs review, by reason

- Go: CONTRACT_COMPILE_ERROR 41, GO_API_CHANGED_USED_BY_CALLER 28, DESCRIPTOR_REFLECTION 21, OPTION_CHANGED 16, NEEDS_REVIEW 14, SECOND_CHECK_DISAGREES 6, WHOLE_MESSAGE_FLOW 4, UNRESOLVED_MEMBER 3, TYPE_ERROR_HIDES_USES 3
- Java: CONTRACT_COMPILE_ERROR 28, OPTION_CHANGED 26, NEEDS_REVIEW 17, JAVA_INLINED_CONSTANTS_UNCHECKED 6, JAVA_DYNAMIC_CODE 5, DESCRIPTOR_REFLECTION 2, WHOLE_MESSAGE_FLOW 2

## Not judged by the compiler, by reason

- Go: not judged 66, baseline_fails 39, bump_side_effect 8, oracle_error 3, judge not verified 2
- Java: oracle_error 431, not_built 174, judge not verified 148, baseline_fails 74

## Errors: 174

- Java bazel history 0e099d92b434: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 0e6cc076b320: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history df82dcd1b57a: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history a3ba48e7bf87: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f84329e007e2: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 24de276977b4: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 3b0b6ed419e6: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 9f167a97f46f: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 2ddb7eb806de: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history e885b89410e8: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 4042fd6e6eaf: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history a03388ac74ca: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 18a674ba8f92: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f4cfc846dbdf: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 0d8a2e14f45b: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f8540dbbd98c: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 7383d33ae565: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 31b412581eb0: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 8f7ffcfd9c86: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 48e940f18d4f: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 5fd0c026608c: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history fd6a9833ba9f: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f99a46f150fb: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 7ab1dc97e2c2: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 106903d38f6d: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 80819273b91c: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history b6b13274cec6: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 9cf808426bf3: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 815b9632e584: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history b8589c3b278e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history e61a426a13d3: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 35530d45e72d: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 6a5aec80fd84: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 19553db9b2ff: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 40f1c7d30b4b: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 5a23ab2f6416: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history bc83389808d5: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history f6c2ef95adeb: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 28715dedc7a6: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above

- Java bazel history 04342878d02e: error: /home/runner/work/_temp/java-stress/wt: neither a Go module (go.mod) nor a Maven or Gradle project
verifier verify: nothing was analyzed: fix the inputs above


## Job minutes: 128 jobs, slowest 40.0 min (stress/results/java/beam/history/job-9of17.json), 15 over 30 min
