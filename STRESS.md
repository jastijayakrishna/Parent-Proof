# Stress test: Go and Java consumers

Updated 2026-10-05 19:52 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go | 106 | 54 | 6 | 6 | **0** | 4 | 13 (12%) | 0 |
| Java | 298 | 231 | 28 | 14 | **13** | 1 | 32 (13%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| cometbft -> cosmos-sdk (history) | 12 | 11 | 5 | 5 | **0** | 0 | 1 (8%) | 0 |
| cometbft-cosmos-sdk (scan) | 20 | 19 | 1 | 1 | **0** | 4 | 3 (15%) | 0 |
| csi-provisioner (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 6 (30%) | 0 |
| csi-spec -> external-provisioner (history) | 6 | 6 | 0 | 0 | **0** | 0 | 2 (33%) | 0 |
| kubelet -> k8s-device-plugin (history) | 8 | 0 | 0 | 0 | **0** | 0 | 1 (12%) | 0 |
| kubelet-device-plugin (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |

## Java by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| camunda-zeebe (history) | 55 | 20 | 5 | 1 | **4** | 0 | 0 (0%) | 0 |
| client-java (history) | 10 | 9 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| conductor (history) | 25 | 23 | 0 | 0 | **0** | 1 | 0 (0%) | 0 |
| google-cloud-pubsub (history) | 2 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| google-cloud-pubsub-history (history) | 28 | 28 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 56 | 16 | 7 | **9** | 0 | 3 (5%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 27 | 19 | 2 | 1 | **0** | 0 | 7 (27%) | 0 |
| temporal-sdk-java (scan) | 20 | 10 | 0 | 0 | **0** | 0 | 1 (10%) | 0 |

## Missed: 13

- Java camunda-zeebe history 7e28eeef5fab (verifier's answer: Merge, build line: Merge): compiler: gateways/gateway-mapping-http/src/main/java/io/camunda/gateway/mapping/http/ResponseMapper.java:236: cannot find symbol
- Java camunda-zeebe history 9bb12c7c0442 (verifier's answer: Merge, build line: Merge): compiler: gateways/gateway-mapping-http/src/main/java/io/camunda/gateway/mapping/http/ResponseMapper.java:240: cannot find symbol
- Java camunda-zeebe history 7a1b436a8e78 (verifier's answer: Merge, build line: Merge): compiler: gateways/gateway-mapping-http/src/main/java/io/camunda/gateway/mapping/http/ResponseMapper.java:241: cannot find symbol
- Java camunda-zeebe history 6fcdafd024e1 (verifier's answer: Merge, build line: Merge): compiler: gateways/gateway-mapping-http/src/main/java/io/camunda/gateway/mapping/http/ResponseMapper.java:237: cannot find symbol
- Java hbase history 20c9e4ba5f66 (verifier's answer: Merge, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:449: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method flushTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hbase.
- Java hbase history 398c5ef3132d (verifier's answer: Merge, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:442: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method isReplicationPeerModificationEnabled(org.apache.hbase.thirdparty.com.google.protobuf.RpcControlle
- Java hbase history ffed09d96bba (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:454: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method rollAllWALWriters(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop
- Java hbase history 9ba5d3e55a36 (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:462: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method refreshHFiles(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hba
- Java hbase history 91ac8abe5d40 (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:451: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method truncateRegion(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hb
- Java hbase history c6a0c3b2b7af (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:456: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method restoreBackupSystemTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history 7f7b9e6ef298 (verifier's answer: Needs review, build line: Merge): compiler: hbase-client/src/main/java/org/apache/hadoop/hbase/client/RawAsyncHBaseAdmin.java:4656: cannot find symbol
- Java hbase history 0f11becf4761 (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:456: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method restoreBackupSystemTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history 6e14c22aae2b (verifier's answer: Needs review, build line: Merge): compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:457: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method reopenTableRegions(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoo

## False alarms: 5

- Go cometbft-cosmos-sdk scan d95e35aa96cb: verifier cites `client/query.go:101`
- Go cometbft-cosmos-sdk scan 354d4dbf89ec: verifier cites `client/query.go:101`
- Go cometbft-cosmos-sdk scan 00e34367d7a3: verifier cites `client/query.go:101`
- Go cometbft-cosmos-sdk scan 8e875cb76428: verifier cites `client/query.go:101`
- Java conductor history ef0a6920d45d: verifier cites ``

## Needs review, by reason

- Go: DESCRIPTOR_REFLECTION 12, CONTRACT_COMPILE_ERROR 9, OPTION_CHANGED 8, NEEDS_REVIEW 7, WHOLE_MESSAGE_FLOW 4, GO_API_CHANGED_USED_BY_CALLER 3, UNRESOLVED_MEMBER 2, TYPE_ERROR_HIDES_USES 1
- Java: OPTION_CHANGED 26, CONTRACT_COMPILE_ERROR 19, NEEDS_REVIEW 10, JAVA_INLINED_CONSTANTS_UNCHECKED 6, DESCRIPTOR_REFLECTION 2, WHOLE_MESSAGE_FLOW 2

## Not judged by the compiler, by reason

- Go: baseline_fails 29, not judged 20, bump_side_effect 3
- Java: baseline_fails 57, oracle_error 10

## Errors: 0


## Job minutes: 62 jobs, slowest 27.6 min (stress/results/java/camunda-zeebe/history/job-7of12.json), 0 over 30 min
