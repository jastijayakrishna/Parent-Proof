# Scoreboard

Every row is one pull request that changed a .proto file, decided by the
verifier before the compiler built the consumer against it.

- **Missed**: the verifier said *Merge*, the compiler says the consumer breaks.
- **False alarm**: the verifier said *Don't merge*, the compiler says it builds.
- **Needs review**: the verifier could not tell; the row says why.

| pull requests | Merge | Don't merge | Needs review | compiler judged | agree | missed | false alarm |
|---|---|---|---|---|---|---|---|
| 18 | 17 | 0 | 1 | 13 | 13 | 0 | 0 |

## Every pull request

| project | pull request | verifier | for the build | compiler | needs review because |
|---|---|---|---|---|---|
| dapr | [#10322](https://github.com/dapr/dapr/pull/10322) Feat/conversation max tokens | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10536](https://github.com/dapr/dapr/pull/10536) Actors: send Dapr-Reentrancy-Id on reminder and timer callbacks | Merge | Merge | compiles |  |
| istio | [#3787](https://github.com/istio/api/pull/3787)  add cert_signer_namespace_map field to MeshConfig for namespace-scoped CSR signer authorization | Merge | Merge | compiles |  |
| istio | [#3796](https://github.com/istio/api/pull/3796) destinationrule: add hash_balance_factor to ConsistentHashLB | Merge | Merge | compiles |  |
| istio | [#3797](https://github.com/istio/api/pull/3797) docs: distinguish authorization rule matching from allowing | Merge | Merge | compiles |  |
| istio | [#3798](https://github.com/istio/api/pull/3798) docs: clarify maxConnections applies to HTTP/2 | Merge | Merge | compiles |  |
| istio | [#3799](https://github.com/istio/api/pull/3799) Allow 63-character WorkloadEntry port names | Merge | Merge | compiles |  |
| lnd | [#9457](https://github.com/lightningnetwork/lnd/pull/9457) routerrpc: add option PreventSubsequentPayment to TrackPaymentV2 | Merge | Merge | compiles |  |
| lnd | [#10504](https://github.com/lightningnetwork/lnd/pull/10504) lnwallet/btcwallet: support taproot script path fee estimation in FundPSBT | Merge | Merge | compiles |  |
| lnd | [#10670](https://github.com/lightningnetwork/lnd/pull/10670) Add raw transaction hex to `pendingsweeps` response | Merge | Merge | compiles |  |
| lnd | [#10943](https://github.com/lightningnetwork/lnd/pull/10943) lnrpc/chainrpc: surface re-org depth and Done over the chain notifier | Merge | Merge | compiles |  |
| lnd | [#10993](https://github.com/lightningnetwork/lnd/pull/10993) walletrpc: return the master key birthday from ListAccounts | Merge | Merge | compiles |  |
| temporal | [#874](https://github.com/temporalio/api/pull/874) Add ExportedExecutions type for export | Merge | Merge | not judged |  |
| temporal | [#876](https://github.com/temporalio/api/pull/876) Add eager standalone activity start API | Merge | Merge | not judged |  |
| temporal | [#877](https://github.com/temporalio/api/pull/877) Add resource id annotation for standalone Nexus operations | Needs review | Needs review | not judged | OPTION_CHANGED, DESCRIPTOR_REFLECTION |
| temporal | [#878](https://github.com/temporalio/api/pull/878) Deprecate BatchOperationResetActivities.reset_attempts | Merge | Merge | not judged |  |
| temporal | [#880](https://github.com/temporalio/api/pull/880) Add Graal AOT and Kotlin worker runtimes | Merge | Merge | not judged |  |
