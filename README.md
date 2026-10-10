# Parent-Proof

A public, timestamped record of how a contract verifier does on real pull
requests it has never seen.

<!-- live:begin -->
**Updated 2026-10-10 10:09 UTC.** [![shadow](https://github.com/jastijayakrishna/Parent-Proof/actions/workflows/shadow.yml/badge.svg)](https://github.com/jastijayakrishna/Parent-Proof/actions/workflows/shadow.yml)

| | changes | judge not verified | broke the build | caught | missed | false alarms | needs review |
|---|---|---|---|---|---|---|---|
| [Real upgrades](HISTORY.md), 9 projects' history | 178 | 0 | 24 | 21 | 0 | 1 | 25 |
| [Open pull requests](SCOREBOARD.md), decided live | 87 | 25 | 0 | 0 | 0 | 0 | 9 |
| [Stress test](STRESS.md), Go: projects never used to tune it | 159 | 2 | 7 | 7 | 0 | 0 | 28 |
| [Stress test](STRESS.md), Go: hold-out projects, run once | 254 | 0 | 22 | 12 | 0 | 4 | 58 |
| [Stress test](STRESS.md), Java: projects never used to tune it | 450 | 71 | 17 | 16 | 0 | 0 | 13 |
| [Stress test](STRESS.md), Java: hold-out projects, run once | 491 | 80 | 2 | 2 | 0 | 1 | 31 |
| [Stress test](STRESS.md), Java: projects it was tuned on | 84 | 0 | 5 | 5 | 0 | 0 | 21 |

**Caught**: it broke the build and the verifier said Don't merge first. **Missed**: the verifier said Merge and the compiler says it breaks, the failure that matters most. **Judge not verified**: not counted, because a planted break did not fail that project's build, so the compiler's answer proves nothing there.

### Catches: 21 real breaks, each called Don't merge before the compiler built it

| contract → project | change | date | where it breaks |
|---|---|---|---|
| cri-api → cri-o | [v0.36.3 → v0.37.0](https://github.com/cri-o/cri-o/commit/4596ee6f26b0c0244b158ada056598ee5529ab11) | 2026-09-07 | `server/container_create.go:1657` |
| cri-api → containerd | [v0.36.4 → v0.37.0](https://github.com/containerd/containerd/commit/7e66a3f76aef5b6616add5c28da7f7e2c0ef6a1f) | 2026-08-27 | `internal/cri/server/container_create.go:331` |
| cri-api → containerd | [v0.36.1 → v0.36.3](https://github.com/containerd/containerd/commit/857237845d8c57734e7bc8057aca258295bc8f58) | 2026-07-23 | `internal/cri/server/container_checkpoint_linux.go:483` |
| lnd → lndclient | [v0.20.1-beta → v0.21.0-beta](https://github.com/lightninglabs/lndclient/commit/f3260ef33ca86362aa12b312f4bf9583c2037954) | 2026-06-05 | `github.com/lightningnetwork/lnd@v0.20.1-beta/invoices/sql_migration.go:514` |
| cri-api → cri-o | [v0.35.1 → v0.36.0-beta.0](https://github.com/cri-o/cri-o/commit/c17ee8b0a3639350bd3911af3eb3d1b83e2ee489) | 2026-04-13 | `cmd/crio/main.go:408` |
| milvus → milvus-client | [v2.6.6-0.20251119054300-fcb3986f4af1 → v2.6.6-0.20251124145901-0b96e4c8af45](https://github.com/milvus-io/milvus/commit/3f063a29b009adb37cdf47b4b53cc5deb06a5fca) | 2025-12-10 | `milvusclient/read_options.go:105` |
| lnd → lndclient | [v0.19.3-beta → v0.20.0-beta](https://github.com/lightninglabs/lndclient/commit/793e683c7b8eb418f6678540a831490b955d8e07) | 2025-11-13 | `lightning_client.go:1351` |
| cri-api → cri-o | [v0.34.1 → v0.35.0-alpha.1](https://github.com/cri-o/cri-o/commit/8beeed1ea9357cd8adb05bbc394eb23a02807ff7) | 2025-10-16 | `vendor/k8s.io/cri-client/pkg/remote_image.go:102` |
| tipb → tidb | [v0.0.0-20250513092957-b555ca3fc078 → v0.0.0-20250529123214-bb8180a479ec](https://github.com/pingcap/tidb/commit/ac6ea64b370f8736122ca19248c7f824461bc4b6) | 2025-06-04 | `pkg/distsql/request_builder.go:100` |
| cri-api → containerd | [v0.32.3 → v0.33.0](https://github.com/containerd/containerd/commit/e393f41d2063adb78fa649958ca21b7abe389c8a) | 2025-05-27 | `internal/cri/instrument/instrumented_service.go:51` |
| lnd → lndclient | [v0.18.5-beta → v0.19.0-beta](https://github.com/lightninglabs/lndclient/commit/50295c0c5027833032d6bf59614b84c3e2321f83) | 2025-05-26 | `invoices_client.go:392` |
| cri-api → cri-o | [v0.33.0-beta.0.0.20250313010358-ab383b81657e → v0.33.0-beta.0.0.20250324233632-87ee4e17aba6](https://github.com/cri-o/cri-o/commit/07a1e0ee6c8956d8ffba8d24c2b01c0287ec8e6f) | 2025-04-08 | `cmd/crio/main.go:407` |
| tipb → tidb | [v0.0.0-20250321085733-a91a8fafd4ed → v0.0.0-20250331100511-d2c561dad347](https://github.com/pingcap/tidb/commit/7232aeab67e14fc757633393515d49da7117de36) | 2025-04-01 | `br/pkg/storage/batch.go:55` |
| tipb → tidb | [v0.0.0-20241212101007-246f91188357 → v0.0.0-20250321085733-a91a8fafd4ed](https://github.com/pingcap/tidb/commit/ca8a0707ab0605260b8bbce8427190607b3fe6d1) | 2025-03-23 | `pkg/planner/core/plan_to_pb.go:279` |
| dapr → go-sdk | [v1.15.0-rc.9 → v1.15.0-rc.17](https://github.com/dapr/go-sdk/commit/81312e9da99ac6ac594cfc1766afea1c8c0e7cc9) | 2025-02-28 | `client/conversation.go:107` |
| tipb → tidb | [v0.0.0-20240823074000-a40c2347786e → v0.0.0-20240919023442-cf70966bef25](https://github.com/pingcap/tidb/commit/5ead7e9a4812f2967be5df96b6a02f377ae089b6) | 2024-09-20 | `pkg/expression/infer_pushdown.go:240` |
| dapr → go-sdk | [v1.14.0-rc.2 → v1.14.0-rc.5](https://github.com/dapr/go-sdk/commit/9bc7d823cc233f092c2956e364f6a802216f1215) | 2024-07-23 | `client/subscribe.go:184` |
| tipb → tidb | [v0.0.0-20240305085524-87f5b80908ab → v0.0.0-20240318032315-55a7867ddd50](https://github.com/pingcap/tidb/commit/3f915c0a369a824c8b1adb37d8a877c1066ea6df) | 2024-03-18 | `pkg/util/execdetails/execdetails.go:755` |
| dapr → go-sdk | [v1.12.1-0.20231013174004-b6540a1c464d → v1.12.1-0.20231030205344-441017b888c5](https://github.com/dapr/go-sdk/commit/87bbb8cd690a7d9049e27c68ce71f7095d7833f7) | 2023-11-01 | `client/client.go:372` |
| dapr → go-sdk | [v1.12.0-rc.4 → v1.12.1-0.20231013174004-b6540a1c464d](https://github.com/dapr/go-sdk/commit/69e788045df06c67a03474a749056d315dcb7323) | 2023-10-13 | `client/actor.go:222` |
| tipb → tidb | [v0.0.0-20230523034258-1bbc3bbbd369 → v0.0.0-20230602100112-acb7942db1ca](https://github.com/pingcap/tidb/commit/aedbcd085bb4ea5777699eac7d25dfd42222b8e5) | 2023-06-07 | `expression/builtin_grouping.go:101` |
<!-- live:end -->

Every hour a GitHub Actions job finds the open pull requests that change
a `.proto` file in 17 open-source projects (Istio, etcd, raft, Temporal,
containerd, cri-api, Envoy's data-plane-api, Linkerd, SPIFFE, Consul, lnd,
Dapr, authzed, Jaeger, Loki, Cortex, Thanos; the pairs are in
[corpus.json](corpus.json)). For each one it:

1. decides the whole pull request (its merge base to its head) with the pinned
   verifier in [bin/](bin/): whether the project that
   uses the contract (Istio for istio/api, etcd for raft, and so on) breaks:
   **Merge**, **Don't merge** or **Needs review**;
2. builds that consumer against the pull request's code with the Go compiler,
   which says **compiles** or **breaks**; the verifier never sees this answer;
3. commits both to [predictions/](predictions/) and recounts
   [SCOREBOARD.md](SCOREBOARD.md).

The record is committed while the pull request is still open, so the
prediction cannot be fitted to what happened afterwards. The commit history and
the Actions run linked in each record show when it was made.

## History: the hard cases

Open pull requests rarely break anything, so a second workflow, **history**
(run on demand), mines every real upgrade of a contract module in seven
projects' git histories: Kubernetes CRI in containerd and cri-o,
OpenTelemetry's OTLP in the OpenTelemetry Go SDK, Dapr's runtime API in its Go
SDK, tipb in TiDB, lnd's RPC in lndclient, containerd's API in nerdctl
([history/suites/](history/suites/)). The Go compiler builds each project's
code at each upgrade against the old and the new module, so every upgrade
that really broke the build is known; the verifier, which was never tuned on
these projects, decides each one. Results: [HISTORY.md](HISTORY.md).

## Reading the scoreboard

- **Missed**: the verifier said *Merge*; the compiler says the consumer
  breaks. The failure that matters most: a customer would have trusted it.
- **False alarm**: the verifier said *Don't merge*; the compiler says the
  consumer builds.
- **Needs review**: the verifier could not prove either; each row says why.
- **Not judged**: the compiler could not build the consumer before the change
  either, or the contract's Go code is not in a module the consumer builds
  against. Those predictions are graded later by what happened to the pull
  request (reverts and fix-up commits).

## Checking a record yourself

Each record holds the pull request, the commits decided, the verifier's
version and sha256, and the compiler's result. `bin/VERSION` names the
verifier's source commit; `gunzip -c bin/verifier-linux-amd64.gz | sha256sum`
must match it.
