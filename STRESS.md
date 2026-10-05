# Stress test: Go and Java consumers

Updated 2026-10-05 18:18 UTC. Plan and rules: [stress/PREREG.md](stress/PREREG.md).

Every row is a real contract change of an open-source project never used to tune the verifier, decided by the
verifier before the project's own compiler judged it (Go: `go build`; Java: the project's Maven or Gradle build).
For the build, **missed** means the verifier said Merge and the compiler says the change breaks the code, the
failure that matters most; **false alarm** means it said Don't merge and the code compiles.

| language | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| Go | 105 | 53 | 6 | 5 | **1** | 0 | 8 (8%) | 0 |
| Java | 300 | 182 | 21 | 5 | **16** | 1 | 21 (11%) | 0 |

## Go by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| argo-cd (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| cometbft -> cosmos-sdk (history) | 12 | 11 | 5 | 4 | **1** | 0 | 0 (0%) | 0 |
| cometbft-cosmos-sdk (scan) | 20 | 19 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| csi-provisioner (scan) | 20 | 18 | 0 | 0 | **0** | 0 | 6 (30%) | 0 |
| csi-spec -> external-provisioner (history) | 5 | 5 | 0 | 0 | **0** | 0 | 2 (40%) | 0 |
| kubelet -> k8s-device-plugin (history) | 8 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| kubelet-device-plugin (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |

## Java by project

| project (what) | windows | compiler judged | broke the build | caught | missed | false alarm | needs review (build) | errors |
|---|---|---|---|---|---|---|---|---|
| camunda-zeebe (history) | 56 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| client-java (history) | 10 | 9 | 3 | 3 | **0** | 0 | 0 (0%) | 0 |
| client-java (scan) | 20 | 20 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| conductor (history) | 25 | 23 | 0 | 0 | **0** | 1 | 0 (0%) | 0 |
| google-cloud-pubsub (history) | 3 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| google-cloud-pubsub-history (history) | 28 | 28 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| hbase (history) | 57 | 56 | 16 | 0 | **16** | 0 | 0 (0%) | 0 |
| java-control-plane (history) | 23 | 23 | 0 | 0 | **0** | 0 | 21 (91%) | 0 |
| jetcd (history) | 5 | 5 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (history) | 6 | 6 | 1 | 1 | **0** | 0 | 0 (0%) | 0 |
| skywalking-java (scan) | 20 | 12 | 0 | 0 | **0** | 0 | 0 (0%) | 0 |
| temporal-sdk-java (history) | 27 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |
| temporal-sdk-java (scan) | 20 | 0 | 0 | 0 | **0** | 0 | 0 (-) | 0 |

## Missed: 17

- Go cometbft -> cosmos-sdk history v0.39.0-beta.2 -> v0.39.0-beta.2.0.20260217150107-284338bcd3d9: compiler: server/cmt_abci.go:16:9: cannot use cometABCIWrapper{…} (value of struct type cometABCIWrapper) as "github.com/cometbft/cometbft/abci/types".Application value in return statement: cometABCIWrapper does not implement "github.com/cometbft/cometbft/abci/types".Application (missing method InsertTx)
- Java hbase history 364fcea01c45: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/io/hfile/PrefetchProtoUtils.java:31: incompatible types: java.util.Map<java.lang.String,java.lang.Boolean> cannot be converted to java.util.Map<java.lang.String,org.apache.hadoop.hbase.shaded.protobuf.generated.PersistentPrefetchProtos.R
- Java hbase history b54cb7db6df0: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:459: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method clearManagedKeyDataCache(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history 20c9e4ba5f66: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:449: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method flushTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hbase.
- Java hbase history 9e74cc0d655b: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/io/hfile/PrefetchProtoUtils.java:24: cannot find symbol
- Java hbase history 398c5ef3132d: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:442: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method isReplicationPeerModificationEnabled(org.apache.hbase.thirdparty.com.google.protobuf.RpcControlle
- Java hbase history ffed09d96bba: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:454: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method rollAllWALWriters(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop
- Java hbase history 9ba5d3e55a36: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:462: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method refreshHFiles(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hba
- Java hbase history 91ac8abe5d40: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:451: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method truncateRegion(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoop.hb
- Java hbase history c6a0c3b2b7af: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:456: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method restoreBackupSystemTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history f81bdebedba3: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/replication/AssignReplicationQueuesProcedure.java:133: an enum switch case label must be the unqualified name of an enumeration constant
- Java hbase history c37fba61e2db: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:451: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method getCachedFilesList(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoo
- Java hbase history 7f7b9e6ef298: compiler: hbase-client/src/main/java/org/apache/hadoop/hbase/client/RawAsyncHBaseAdmin.java:4656: cannot find symbol
- Java hbase history b961eb2ddd02: compiler: hbase-client/src/main/java/org/apache/hadoop/hbase/client/RawAsyncHBaseAdmin.java:135: cannot find symbol
- Java hbase history 0f11becf4761: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:456: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method restoreBackupSystemTable(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache
- Java hbase history fa4c8960e587: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:451: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method getCachedFilesList(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoo
- Java hbase history 6e14c22aae2b: compiler: hbase-server/src/main/java/org/apache/hadoop/hbase/master/MasterRpcServices.java:457: org.apache.hadoop.hbase.master.MasterRpcServices is not abstract and does not override abstract method reopenTableRegions(org.apache.hbase.thirdparty.com.google.protobuf.RpcController,org.apache.hadoo

## False alarms: 1

- Java conductor history ef0a6920d45d: verifier cites ``

## Needs review, by reason

- Go: DESCRIPTOR_REFLECTION 12, CONTRACT_COMPILE_ERROR 9, OPTION_CHANGED 8, NEEDS_REVIEW 7, WHOLE_MESSAGE_FLOW 4, UNRESOLVED_MEMBER 2, TYPE_ERROR_HIDES_USES 1
- Java: GENERATED_BINDINGS_UNAVAILABLE 34, OPTION_CHANGED 21, CONTRACT_COMPILE_ERROR 20, NEEDS_REVIEW 5, WHOLE_MESSAGE_FLOW 1

## Not judged by the compiler, by reason

- Go: baseline_fails 29, not judged 20, bump_side_effect 3
- Java: baseline_fails 115, oracle_error 3

## Errors: 0


## Job minutes: 62 jobs, slowest 17.4 min (stress/results/java/conductor/history/job-1of2.json), 0 over 30 min
