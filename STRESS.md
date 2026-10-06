# Stress test: Go and Java consumers

Updated 2026-10-06 05:31 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go | 147 | 83 | 7 | 6 | **1** | 0 | 19 (13%) | 0 |
| Java | 563 | 172 | 24 | 16 | **7** | 0 | 32 (6%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (live) | 1 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| cometbft -> cosmos-sdk (history) | 41 | 40 | 6 | 5 | **1** | 0 | 3 (7%) | 0 |
| cometbft-cosmos-sdk (scan) | 20 | 19 | 1 | 1 | **0** | 0 | 3 (15%) | 0 |
| csi-provisioner (live) | 2 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| csi-provisioner (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 7 (35%) | 0 |
| csi-spec -> external-provisioner (history) | 6 | 6 | 0 | 0 | **0** | 0 | 3 (50%) | 0 |
| kubelet -> k8s-device-plugin (history) | 17 | 0 | 0 | 0 | **0** | 0 | 1 (6%) | 0 |
| kubelet-device-plugin (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 2 (10%) | 0 |

## Java by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| camunda-zeebe (history) | 55 | 12 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 9 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| conductor (history) | 25 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-pubsub (history) | 19 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| google-cloud-pubsub-history (history) | 276 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 56 | 16 | 9 | **7** | 0 | 3 (5%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 27 | 19 | 2 | 1 | **0** | 0 | 7 (27%) | 0 |
| temporal-sdk-java (scan) | 20 | 10 | 0 | 0 | **0** | 0 | 1 (10%) | 0 |

## Missed: 8

- Go cometbft -> cosmos-sdk history v1.0.0-rc1 -> v1.0.0-rc1.0.20240908111210-ab0be101882f (verifier's answer: Merge, build line: Merge): compiler: module github.com/cometbft/cometbft@latest found (v1.0.1), but does not contain package github.com/cometbft/cometbft/crypto/sr25519; module github.com/cometbft/cometbft@latest found (v1.0.1), but does not contain package github.com/cometbft/cometbft/crypto/sr25519; module github.com/cometbft/cometbf
- Java hbase history ffed09d96bba (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:454: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method rollAllWALWriters(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop
- Java hbase history 9ba5d3e55a36 (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:462: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method refreshHFiles(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hba
- Java hbase history 91ac8abe5d40 (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:451: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method truncateRegion(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hb
- Java hbase history c6a0c3b2b7af (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:456: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method restoreBackupSystemTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history 7f7b9e6ef298 (verifier's answer: Needs review, build line: Merge): compiler: hbase-client/src/main/java/org/apache/hadoop/hbase/client/RawAsyncHBaseAdmin.java:4656: cannot find symbol
- Java hbase history 0f11becf4761 (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:456: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method restoreBackupSystemTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history 6e14c22aae2b (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:457: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method reopenTableRegions(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoo

## False alarms: 0


## Needs review, by reason

- Go: DESCRIPTOR_REFLECTION 12, CONTRACT_COMPILE_ERROR 10, OPTION_CHANGED 8, NEEDS_REVIEW 7, GO_API_CHANGED_USED_BY_CALLER 4, WHOLE_MESSAGE_FLOW 4, SECOND_CHECK_DISAGREES 4, UNRESOLVED_MEMBER 2, TYPE_ERROR_HIDES_USES 1
- Java: OPTION_CHANGED 26, CONTRACT_COMPILE_ERROR 19, NEEDS_REVIEW 10, JAVA_INLINED_CONSTANTS_UNCHECKED 6, DESCRIPTOR_REFLECTION 2, WHOLE_MESSAGE_FLOW 2

## Not judged by the compiler, by reason

- Go: baseline_fails 38, not judged 21, bump_side_effect 3, judge not verified 2
- Java: oracle_error 227, judge not verified 96, baseline_fails 68

## Errors: 0


## Job minutes: 74 jobs, slowest 21.5 min (stress/results/java/camunda-zeebe/history/job-6of12.json), 0 over 30 min
