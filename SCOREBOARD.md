# Scoreboard

Updated 2026-10-07 23:58 UTC.

Every row is one pull request that changed a .proto file, decided by the
verifier before the compiler built the consumer against it.

- **Missed**: the verifier said *Merge*, the compiler says the consumer breaks.
- **False alarm**: the verifier said *Don't merge*, the compiler says it builds.
- **Needs review**: the verifier could not tell; the row says why.

| pull requests | Merge | Don't merge | Needs review | compiler judged | agree | missed | false alarm |
|---|---|---|---|---|---|---|---|
| 60 | 52 | 3 | 5 | 35 | 34 | 0 | 0 |

## Every pull request

| project | pull request | verifier | for the build | compiler | needs review because |
|---|---|---|---|---|---|
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Merge | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29322](https://github.com/argoproj/argo-cd/pull/29322) feat(appset): add metrics for appset to measure rollout durations for progressive sync | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| cometbft-cosmos-sdk | [#6100](https://github.com/cometbft/cometbft/pull/6100) fix(types,state): enforce minimum Block.MaxBytes floor and handle small limits defensively | Merge | Merge | compiles |  |
| csi-provisioner | [#603](https://github.com/container-storage-interface/spec/pull/603) Add ControllerGetNodeInfo RPC (alpha) | Merge | Merge | compiles |  |
| csi-provisioner | [#613](https://github.com/container-storage-interface/spec/pull/613) Add reason to ControllerUnpublishVolumeRequest | Merge | Merge | compiles |  |
| dapr | [#9974](https://github.com/dapr/dapr/pull/9974) feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#10322](https://github.com/dapr/dapr/pull/10322) Feat/conversation max tokens | Merge | Merge | compiles |  |
| dapr | [#10322](https://github.com/dapr/dapr/pull/10322) Feat/conversation max tokens | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10536](https://github.com/dapr/dapr/pull/10536) Actors: send Dapr-Reentrancy-Id on reminder and timer callbacks | Merge | Merge | compiles |  |
| istio | [#3722](https://github.com/istio/api/pull/3722) feat(tracing): add otel always_on sampler | Merge | Merge | compiles |  |
| istio | [#3787](https://github.com/istio/api/pull/3787)  add cert_signer_namespace_map field to MeshConfig for namespace-scoped CSR signer authorization | Merge | Merge | compiles |  |
| istio | [#3791](https://github.com/istio/api/pull/3791) docs: use camelCase prefixRewrite in HTTPRedirect example | Merge | Merge | compiles |  |
| istio | [#3792](https://github.com/istio/api/pull/3792) docs: expose presence field in JWTRule reference docs | Merge | Merge | compiles |  |
| istio | [#3796](https://github.com/istio/api/pull/3796) destinationrule: add hash_balance_factor to ConsistentHashLB | Merge | Merge | compiles |  |
| istio | [#3797](https://github.com/istio/api/pull/3797) docs: distinguish authorization rule matching from allowing | Merge | Merge | compiles |  |
| istio | [#3798](https://github.com/istio/api/pull/3798) docs: clarify maxConnections applies to HTTP/2 | Merge | Merge | compiles |  |
| istio | [#3799](https://github.com/istio/api/pull/3799) Allow 63-character WorkloadEntry port names | Merge | Merge | compiles |  |
| jaeger | [#231](https://github.com/jaegertracing/jaeger-idl/pull/231) feat(expression): Add phrase and fulltext text-search operators | Needs review | Needs review | compiles | OPTION_CHANGED |
| lnd | [#9457](https://github.com/lightningnetwork/lnd/pull/9457) routerrpc: add option PreventSubsequentPayment to TrackPaymentV2 | Merge | Merge | compiles |  |
| lnd | [#9888](https://github.com/lightningnetwork/lnd/pull/9888) Attributable failures | Merge | Merge | bump_side_effect |  |
| lnd | [#9907](https://github.com/lightningnetwork/lnd/pull/9907)   routing: add mission control namespace support to SendPaymentV2 | Merge | Merge | compiles |  |
| lnd | [#10067](https://github.com/lightningnetwork/lnd/pull/10067) Fees: add fractional sat/vB support (lncli) and sats_per_kw (RPC) | Merge | Merge | compiles |  |
| lnd | [#10316](https://github.com/lightningnetwork/lnd/pull/10316) Invoice rpc metadata support | Merge | Merge | compiles |  |
| lnd | [#10411](https://github.com/lightningnetwork/lnd/pull/10411) aliasmgr: Allow persisting manually added alias scids | Merge | Merge | compiles |  |
| lnd | [#10504](https://github.com/lightningnetwork/lnd/pull/10504) lnwallet/btcwallet: support taproot script path fee estimation in FundPSBT | Merge | Merge | compiles |  |
| lnd | [#10670](https://github.com/lightningnetwork/lnd/pull/10670) Add raw transaction hex to `pendingsweeps` response | Merge | Merge | compiles |  |
| lnd | [#10670](https://github.com/lightningnetwork/lnd/pull/10670) Add raw transaction hex to `pendingsweeps` response | Merge | Merge | compiles |  |
| lnd | [#10685](https://github.com/lightningnetwork/lnd/pull/10685) Update AddHoldInvoice to add support for optional preimage/hash generation | Merge | Merge | compiles |  |
| lnd | [#10735](https://github.com/lightningnetwork/lnd/pull/10735) Freebie onion message slot and per-peer stats in ListPeers | Merge | Merge | compiles |  |
| lnd | [#10744](https://github.com/lightningnetwork/lnd/pull/10744) lnrpc: add scid filter to ListChannels RPC and lncli | Merge | Merge | compiles |  |
| lnd | [#10889](https://github.com/lightningnetwork/lnd/pull/10889) Remove deprecated fee rate option --sat_per_byte | Merge | Merge | compiles |  |
| lnd | [#10943](https://github.com/lightningnetwork/lnd/pull/10943) lnrpc/chainrpc: surface re-org depth and Done over the chain notifier | Merge | Merge | compiles |  |
| lnd | [#10973](https://github.com/lightningnetwork/lnd/pull/10973) multi: expose peer address sources and offline peers in ListPeers | Merge | Merge | compiles |  |
| lnd | [#10993](https://github.com/lightningnetwork/lnd/pull/10993) walletrpc: return the master key birthday from ListAccounts | Merge | Merge | compiles |  |
| lnd | [#11095](https://github.com/lightningnetwork/lnd/pull/11095) keychain+walletrpc: add DeriveAndStoreKey | Merge | Merge | compiles |  |
| loki | [#24984](https://github.com/grafana/loki/pull/24984) feat(logql): Track stream-first query stats, add integration test | Merge | Merge | not judged |  |
| loki | [#24984](https://github.com/grafana/loki/pull/24984) feat(logql): Track stream-first query stats, add integration test | Merge | Merge | not judged |  |
| loki | [#24991](https://github.com/grafana/loki/pull/24991) feat(logline): Report Logline query stats on the metrics.go line | Merge | Merge | not judged |  |
| loki | [#25002](https://github.com/grafana/loki/pull/25002) feat(logql): Log stream-first and timestamp-first query counts in query stats | Merge | Merge | not judged |  |
| loki | [#25006](https://github.com/grafana/loki/pull/25006) feat(pattern-ingester): Add a gRPC method that accepts InternalPushRequest  | Needs review | Needs review | not judged | NEEDS_REVIEW |
| temporal | [#856](https://github.com/temporalio/api/pull/856) vts: add time skipping to schedules | Merge | Merge | not judged |  |
| temporal | [#871](https://github.com/temporalio/api/pull/871) Clarify namespace poller group snapshots | Merge | Merge | not judged |  |
| temporal | [#872](https://github.com/temporalio/api/pull/872) Klassenq/nexus per endpoint encryption | Don't merge | Merge | not judged |  |
| temporal | [#872](https://github.com/temporalio/api/pull/872) Klassenq/nexus per endpoint encryption | Don't merge | Merge | not judged |  |
| temporal | [#873](https://github.com/temporalio/api/pull/873) Preserve reset request IDs in workflow history | Don't merge | Merge | not judged |  |
| temporal | [#874](https://github.com/temporalio/api/pull/874) Add ExportedExecutions type for export | Merge | Merge | not judged |  |
| temporal | [#875](https://github.com/temporalio/api/pull/875) Add region_id to ComputeConfigScalingGroup | Merge | Merge | not judged |  |
| temporal | [#875](https://github.com/temporalio/api/pull/875) Add region_id to ComputeConfigScalingGroup | Merge | Merge | not judged |  |
| temporal | [#875](https://github.com/temporalio/api/pull/875) Add region_id to ComputeConfigScalingGroup | Merge | Merge | not judged |  |
| temporal | [#876](https://github.com/temporalio/api/pull/876) Add eager standalone activity start API | Merge | Merge | not judged |  |
| temporal | [#876](https://github.com/temporalio/api/pull/876) Add eager standalone activity start API | Merge | Merge | not judged |  |
| temporal | [#876](https://github.com/temporalio/api/pull/876) Add eager standalone activity start API | Merge | Merge | not judged |  |
| temporal | [#877](https://github.com/temporalio/api/pull/877) Add resource id annotation for standalone Nexus operations | Needs review | Needs review | not judged | OPTION_CHANGED, DESCRIPTOR_REFLECTION |
| temporal | [#878](https://github.com/temporalio/api/pull/878) Deprecate BatchOperationResetActivities.reset_attempts | Merge | Merge | not judged |  |
| temporal | [#880](https://github.com/temporalio/api/pull/880) Add Graal AOT and Kotlin worker runtimes | Merge | Merge | not judged |  |
