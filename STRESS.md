# Stress test: Go and Java consumers

Updated 2026-10-05 17:42 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go | 68 | 25 | 2 | 1 | **1** | 0 | 6 (9%) | 0 |
| Java | 61 | 13 | 5 | 5 | **0** | 0 | 0 (0%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| cometbft -> cosmos-sdk (history) | 8 | 7 | 2 | 1 | **1** | 0 | 0 (0%) | 0 |
| csi-provisioner (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 6 (30%) | 0 |
| kubelet-device-plugin (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |

## Java by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| client-java (history) | 10 | 6 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 2 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |

## Missed: 1

- Go cometbft -> cosmos-sdk history v0.39.0-beta.2 -> v0.39.0-beta.2.0.20260217150107-284338bcd3d9: compiler: server/cmt_abci.go:16:9: cannot use cometABCIWrapper{…} (value of struct type cometABCIWrapper) as "github.com/cometbft/cometbft/abci/types".Application value in return statement: cometABCIWrapper does not implement "github.com/cometbft/cometbft/abci/types".Application (missing method InsertTx)

## False alarms: 0


## Needs review, by reason

- Go: DESCRIPTOR_REFLECTION 9, CONTRACT_COMPILE_ERROR 9, OPTION_CHANGED 6, NEEDS_REVIEW 6, WHOLE_MESSAGE_FLOW 2, UNRESOLVED_MEMBER 1

## Not judged by the compiler, by reason

- Go: baseline_fails 21, not judged 20, bump_side_effect 2
- Java: baseline_fails 47, oracle_error 1

## Errors: 0


## Job minutes: 19 jobs, slowest 6.9 min (stress/results/java/client-java/history/job-1of1.json), 0 over 30 min
