# Stress test of Parent on Go and Java consumers: pre-registration

Written and committed on 2026-10-05, before the verifier decided any window of these projects. Everything below
was fixed before the first run; any later change is a new commit that says why.

## The question, and the numbers that answer it

**Does Parent ever say Merge when a contract change breaks a Go or Java consumer it has never seen?**

Answered on real contract changes of open-source projects never used to tune Parent, each decided by Parent before
the project's own compiler judges it:

- **missed** (said Merge for the build, the compiler says it breaks): must be **0** on every compiler-judged window,
  in both languages, old projects and new;
- **false Don't merge** (said Don't merge, the compiler says it builds): each one fixed, or kept with a written
  reason the founder approves;
- **Needs review** rate, per project and language, with its reasons;
- errors and crashes, replay mismatches (a record that does not replay to the same answer), minutes per job.

## What is tested

`bin/verifier-linux-amd64.gz`: Parent main fd5ae27 (go-analyzer v0.20.0, jvm-analyzer v0.8.2), sha256 92fa9f95…
After each fix the binary is rebuilt from Parent main, recorded in `bin/VERSION`, and the previous one is kept as
`bin/verifier-before-linux-amd64.gz`.

## Projects

Each was checked before use: every pin resolves, every Go consumer's go.mod requires the provider's module, and
every Java project builds on a GitHub runner (feasibility probes, below). **Dev** runs first; failures found there are
fixed. **Hold-out** gets no run of any kind (history, scan or live pull requests) until the fixes freeze; it then
runs once, on a binary recorded in `stress/HOLDOUT.md` before the run starts. **Regression** projects were used to
tune Parent before; they rerun after every fix.

### Go (`stress/corpus.json`, `stress/suites`, `stress/go-plan.json`)

| project | provider at | consumer at | set | runs |
|---|---|---|---|---|
| CSI spec → external-provisioner | container-storage-interface/spec 25b3f102 | kubernetes-csi/external-provisioner b1d6b6de | dev | history, scan, live |
| kubelet API → NVIDIA device plugin | kubernetes/kubelet db196013 | NVIDIA/k8s-device-plugin d5dce58a | dev | history, scan (the kubelet repository is a read-only mirror: no pull requests) |
| CometBFT → Cosmos SDK (gogoproto) | cometbft/cometbft 65c54ed4 | cosmos/cosmos-sdk 358be568 | dev | history, scan, live |
| Argo CD (contract and users in one repository) | argoproj/argo-cd 87b9b4e3 | the same | dev | scan, live |
| CSI spec → external-attacher | container-storage-interface/spec 25b3f102 | kubernetes-csi/external-attacher 951c194a | hold-out | history, scan |
| Cosmos SDK → Gaia (gogoproto, amino JSON) | cosmos/cosmos-sdk release/v0.53.x 24dfbad7 | cosmos/gaia 7b4bfd71 | hold-out | history, scan, live |
| BuildKit → Buildx | moby/buildkit 106f55ce | docker/buildx 63076c46 | hold-out | history, scan, live |
| OTLP → Grafana Tempo | open-telemetry/opentelemetry-proto b3f75588 (history: opentelemetry-proto-go) | grafana/tempo 85248acb | hold-out | history, scan, live |
| Vitess (one repository) | vitessio/vitess 950050fa | the same | hold-out | scan, live |

Gaia's scan reads the Cosmos SDK release branch Gaia builds against (v0.53.8): main is 956 commits past it, so
Gaia does not build against main's contract commits. Excluded, with the reason: Envoy Gateway (its .proto files
and Go code are in repositories with no version link), Grafana Mimir (built on a Prometheus fork),
otel-collector-contrib (it uses its own generated copy).

### Java (`stress/java/projects.json`)

| project | contract (how it reaches the build) | consumer at | build | set | runs |
|---|---|---|---|---|---|
| Temporal SDK (Java and Kotlin) | temporalio/api, git submodule | temporalio/sdk-java 1af71ba3 | Gradle, JDK 17, all modules | dev | history, scan, live |
| Camunda / Zeebe | gateway-protocol, in the repository | camunda/camunda 5ed25b7c | Maven, JDK 21, every module that uses the generated gRPC code, and what they need | dev | history, live |
| Google Cloud Pub/Sub (googleapis) | protos and generated code checked in | googleapis/google-cloud-java 70c7439d (java-pubsub); history also from the archived googleapis/java-pubsub ba2b8a32 | Maven, JDK 17 / 11 | dev | history, live |
| Apache HBase (shaded protobuf) | hbase-protocol-shaded, in the repository | apache/hbase 8559faed | Maven, JDK 17, hbase-server and what it needs | dev | history, live |
| Conductor | grpc module, in the repository | conductor-oss/conductor ab2de6da | Gradle, JDK 21 | dev | history, live |
| Apache Beam (vendored, relocated protobuf) | model/pipeline, fn-execution, job-management | apache/beam 7711c534 | Gradle, JDK 17, runners core, harness, fn execution | hold-out | history |
| Google Cloud Bigtable (googleapis) | checked in | archived googleapis/java-bigtable 949c6965 | Maven, JDK 11 | hold-out | history |
| Alluxio | core/transport, in the repository | Alluxio/alluxio ca893e83 | Maven, JDK 11, the master server and what it needs | hold-out | history |
| Bazel | src/main/protobuf | bazelbuild/bazel 9ed3f23e | none: it builds with Bazel, whose output Parent does not read | hold-out | history, checked without a build: no window may say Merge |
| tikv/client-java | pingcap/kvproto, pinned in a build script | c12047a0 | Maven, JDK 8 | regression | history since 2018, scan |
| Envoy java-control-plane | vendored copy | a3ecf70d | Maven, JDK 11 | regression | history since 2022 |
| Apache SkyWalking Java agent | skywalking-data-collect-protocol, git submodule | ea2fb09b | Maven, JDK 17 | regression | history since 2022, scan |
| etcd jetcd | copy in the repository | 9f509770 | Gradle, JDK 17 | regression | history since 2022 |

## The truth

**Go.** History (`verifier suite build`): every pin bump of the provider module in the consumer's history since
2023-01-01; the Go compiler builds the consumer's packages that import the module at the bump's parent, against the
old and the new pin (linux/amd64, cgo off, compile only). Every bump whose contract diff is not empty is judged
(breaking and additive alike: `--additive 100000`). A bump whose contract diff is empty, or whose pins cannot be
resolved, is counted from the build log but not judged: a change only to generated code, with no .proto change, is
outside what Parent checks and is not measured here. Scan (`verifier gate scan --oracle`): the provider's last 20
contract commits against the pinned consumer, the compiler judging those inside a Go module the consumer builds
against (for a contract and its users in one repository, and for OTLP whose Go code lives in another repository,
the scan is not judged). Live pull requests: as the shadow workflow does today.

**Java** (`stress/java/harness.py`). A window is a contract change seen by one consumer tree:

- history: every first-parent commit of the consumer since 2023-01-01 (regression: as listed) that moves the
  contract (a new submodule commit, a new pin in the build script) or changes a .proto file of the contract kept
  in the repository; the consumer's code is the commit's parent;
- scan: the provider's last 20 commits that change .proto files, against the consumer's pinned tree;
- live: an open pull request, as one change from its merge base to its head.

For each window: the consumer is built with the contract before the change; Parent decides the change against that
build (`verifier verify`, then `verifier replay` of its record); then the same tree is built again from clean with
the contract after the change. **Breaks** = javac or kotlinc errors in the consumer's own main sources.
**Compiles** = the build succeeds. Not judged, with the reason: the baseline does not build; only generated or
provider code fails; the build fails without a compiler error. The second build never reuses Gradle's build cache.
In a repository where the build compiles only some modules, Parent reads exactly the modules the build compiles:
the sources of the others are removed from the copy Parent reads, so Parent and the compiler see the same code.
Build recipes may be fixed when a baseline fails for a reason unrelated to the contract; that is a harness change,
recorded in git, never a change to Parent.

**Wire.** The Go release gate keeps scoring the runtime with the wire. For Java, the trap suite (below) is judged by
javac and the wire; real Java windows are judged by the compiler only.

## Java trap suite

Grown from 341 cases toward the Go suite's 71 programs, on the Go suite's contract and 34 mutations plus
Java-only ones (java_package, java_outer_classname, java_multiple_files), each case judged by javac against code
regenerated from the changed contract, and by the wire along the idiom's flows. First, before anything else: a
ClientInterceptor and a ServerInterceptor that log every message as JSON, the Java twin of the Go interceptor wrong
Merge fixed in 68371ce/db103ac. Then: getters and builders; JsonFormat printer and parser, with and without
ignoringUnknownFields; DynamicMessage and Descriptors; Any pack/unpack; blocking, async and future stubs and
streaming observers; oneofs, maps, enums (UNRECOGNIZED, valueOf, getNumber); proto2 extensions; the lite runtime;
shaded protobuf; two protoc versions; Kotlin DSL builders. Pass: 0 said Merge where javac or the wire says it breaks;
every other mismatch listed with its reason, as testdata/adversarial/justified.json does for Go.

## Other checks

`verifier report` and `verifier now` run on Java consumers (Temporal, Camunda, client-java). What the GitHub server
would need to check Java services is assessed and reported; nothing is built for it without the founder's approval.

## Rules

- **Stop:** on any missed window (said Merge, the compiler or the wire says it breaks), stop and report to the founder
  the window, the code and the root cause, before fixing anything.
- **Fix:** root causes only, never special-casing a project; a trap program that reproduces the pattern comes first;
  the analyzer or rules version is bumped when a decision changes; docs/rules.md is regenerated if the rules change.
  Never trade a missed window for less Needs review.
- **After every fix:** `go vet ./...` and `go test ./...` (both trap suites); the proof binary rebuilt; the release
  gates, the 17-project scan and every stress run of both languages rerun; required: 0 missed, 0 new false Don't merge,
  no new unexplained Needs review.
- **Pass:** 0 missed on every compiler-judged window of every set; every false Don't merge fixed or approved; 0 replay
  mismatches; release gates and the 17-project scan unchanged (or each difference explained); vet and tests pass.
- **Kill a project** (recorded, not counted): its baseline fails on more than half its windows for reasons unrelated
  to the contract after one recipe fix, or one window cannot finish in a 30-minute job.
- **Kill a fix:** it is reverted if it adds a missed window or a false Don't merge anywhere in the proof.

## Budgets

Every GitHub job aims for 20 minutes and must stay under 30: the shards in `stress/go-plan.json` and in each Java
project's `shards`; a job's hard timeout (45-60 minutes) only guards against hangs, and a job over 30 minutes gets
more shards next run, never fewer windows. The laptop runs unit tests and one suite at a time and clones no
project. Whole test: about 2.5 to 3 days.

## Feasibility probes run before this registration

Layout and build trials of every Java project, without the verifier (`stress/probe/out`, workflow `probe`): where
the contract is, how often it changed since 2023 (HBase 57, Camunda 56, Beam 56, Bigtable 36, Pub/Sub 28, Alluxio 27,
Temporal 27, Conductor 25, java-control-plane 16, SkyWalking 4, jetcd 3, Bazel 174), and cold and clean build times
on a runner (from 38 s for Conductor to 409 s for Beam). HBase and Alluxio needed `test-compile
-Dmaven.test.skip=true` (their builds ask for other modules' test jars), Conductor JDK 21.
