# Scoreboard

Every row is one pull request that changed a .proto file, decided by the
verifier before the compiler built the consumer against it. Wrong GO: the
verifier said the consumer still builds, the compiler says it breaks. False
NO-GO: the verifier said it breaks, the compiler says it builds.

| decided | GO | NO-GO | UNKNOWN | compiler judged | agree | wrong GO | false NO-GO |
|---|---|---|---|---|---|---|---|
| 20 | 19 | 0 | 1 | 15 | 15 | 0 | 0 |

## Every pull request

| project | pull request | verdict | build | compiler | UNKNOWN because |
|---|---|---|---|---|---|
| dapr | [#10322](https://github.com/dapr/dapr/pull/10322) Feat/conversation max tokens | GO | GO | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | GO | GO | compiles |  |
| dapr | [#10536](https://github.com/dapr/dapr/pull/10536) Actors: send Dapr-Reentrancy-Id on reminder and timer callbacks | GO | GO | compiles |  |
| istio | [#3787](https://github.com/istio/api/pull/3787)  add cert_signer_namespace_map field to MeshConfig for namespace-scoped CSR signer authorization | GO | GO | compiles |  |
| istio | [#3791](https://github.com/istio/api/pull/3791) docs: use camelCase prefixRewrite in HTTPRedirect example | GO | GO | compiles |  |
| istio | [#3792](https://github.com/istio/api/pull/3792) docs: expose presence field in JWTRule reference docs | GO | GO | compiles |  |
| istio | [#3796](https://github.com/istio/api/pull/3796) destinationrule: add hash_balance_factor to ConsistentHashLB | GO | GO | compiles |  |
| istio | [#3797](https://github.com/istio/api/pull/3797) docs: distinguish authorization rule matching from allowing | GO | GO | compiles |  |
| istio | [#3798](https://github.com/istio/api/pull/3798) docs: clarify maxConnections applies to HTTP/2 | GO | GO | compiles |  |
| istio | [#3799](https://github.com/istio/api/pull/3799) Allow 63-character WorkloadEntry port names | GO | GO | compiles |  |
| lnd | [#9457](https://github.com/lightningnetwork/lnd/pull/9457) routerrpc: add option PreventSubsequentPayment to TrackPaymentV2 | GO | GO | compiles |  |
| lnd | [#10504](https://github.com/lightningnetwork/lnd/pull/10504) lnwallet/btcwallet: support taproot script path fee estimation in FundPSBT | GO | GO | compiles |  |
| lnd | [#10670](https://github.com/lightningnetwork/lnd/pull/10670) Add raw transaction hex to `pendingsweeps` response | GO | GO | compiles |  |
| lnd | [#10943](https://github.com/lightningnetwork/lnd/pull/10943) lnrpc/chainrpc: surface re-org depth and Done over the chain notifier | GO | GO | compiles |  |
| lnd | [#10993](https://github.com/lightningnetwork/lnd/pull/10993) walletrpc: return the master key birthday from ListAccounts | GO | GO | compiles |  |
| temporal | [#874](https://github.com/temporalio/api/pull/874) Add ExportedExecutions type for export | GO | GO | not judged |  |
| temporal | [#876](https://github.com/temporalio/api/pull/876) Add eager standalone activity start API | GO | GO | not judged |  |
| temporal | [#877](https://github.com/temporalio/api/pull/877) Add resource id annotation for standalone Nexus operations | UNKNOWN | UNKNOWN | not judged | OPTION_CHANGED, DESCRIPTOR_REFLECTION |
| temporal | [#878](https://github.com/temporalio/api/pull/878) Deprecate BatchOperationResetActivities.reset_attempts | GO | GO | not judged |  |
| temporal | [#880](https://github.com/temporalio/api/pull/880) Add Graal AOT and Kotlin worker runtimes | GO | GO | not judged |  |
