# Scoreboard

Updated 2026-10-30 18:49 UTC.

Every row is one pull request that changed a .proto file, decided by the
verifier before the compiler built the consumer against it.

- **Missed**: the verifier said *Merge*, the compiler says the consumer breaks.
- **False alarm**: the verifier said *Don't merge*, the compiler says it builds.
- **Needs review**: the verifier could not tell; the row says why.

| pull requests | Merge | Don't merge | Needs review | compiler judged | agree | missed | false alarm |
|---|---|---|---|---|---|---|---|
| 275 | 205 | 7 | 63 | 90 | 89 | 0 | 0 |

## Every pull request

| project | pull request | verifier | for the build | compiler | needs review because |
|---|---|---|---|---|---|
| argo-cd | [#24121](https://github.com/argoproj/argo-cd/pull/24121) feat(azure): allow setting azure cloud (gov, china) for authentication | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#24756](https://github.com/argoproj/argo-cd/pull/24756) feat: add paramPrefix to git generator to namespace data included from files (#18048) | Merge | Merge | not judged |  |
| argo-cd | [#25416](https://github.com/argoproj/argo-cd/pull/25416) feat(repo-server): partial-clone | Merge | Merge | not judged |  |
| argo-cd | [#25416](https://github.com/argoproj/argo-cd/pull/25416) feat(repo-server): partial-clone | Merge | Merge | not judged |  |
| argo-cd | [#25756](https://github.com/argoproj/argo-cd/pull/25756) feat: Pull Request Generator - Support excluding PRs by label (#25755) | Merge | Merge | not judged |  |
| argo-cd | [#25756](https://github.com/argoproj/argo-cd/pull/25756) feat: Pull Request Generator - Support excluding PRs by label (#25755) | Merge | Merge | not judged |  |
| argo-cd | [#27124](https://github.com/argoproj/argo-cd/pull/27124) feat: add support for attaching ephemeral containers (debug containers) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#27124](https://github.com/argoproj/argo-cd/pull/27124) feat: add support for attaching ephemeral containers (debug containers) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#27458](https://github.com/argoproj/argo-cd/pull/27458) feat: add sso.auto-login option to skip SSO login button click | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#27585](https://github.com/argoproj/argo-cd/pull/27585) feat: add bearer token support to Bitbucket Cloud SCM provider Fixes #26929 | Merge | Merge | not judged |  |
| argo-cd | [#27932](https://github.com/argoproj/argo-cd/pull/27932) feat(appset): add Refresh RPC and UI action (#27798) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#28233](https://github.com/argoproj/argo-cd/pull/28233) feat: disambiguate local users from SSO users in RBAC with strict mode | Merge | Merge | not judged |  |
| argo-cd | [#28233](https://github.com/argoproj/argo-cd/pull/28233) feat: disambiguate local users from SSO users in RBAC with strict mode | Merge | Merge | not judged |  |
| argo-cd | [#28309](https://github.com/argoproj/argo-cd/pull/28309) feat: add --output-parameters to argocd appset generate (#27599) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#28531](https://github.com/argoproj/argo-cd/pull/28531) feat: add ignoreDuplicateResources to suppress RepeatedResourceWarning (#28026) | Merge | Merge | not judged |  |
| argo-cd | [#28531](https://github.com/argoproj/argo-cd/pull/28531) feat: add ignoreDuplicateResources to suppress RepeatedResourceWarning (#28026) | Merge | Merge | not judged |  |
| argo-cd | [#28840](https://github.com/argoproj/argo-cd/pull/28840) feat(SyncWindow): CRD for sync window | Merge | Merge | not judged |  |
| argo-cd | [#28840](https://github.com/argoproj/argo-cd/pull/28840) feat(SyncWindow): CRD for sync window | Merge | Merge | not judged |  |
| argo-cd | [#28908](https://github.com/argoproj/argo-cd/pull/28908) fix: base auto-sync change detection on the last synced revision (#27875, #21692) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29105](https://github.com/argoproj/argo-cd/pull/29105) feat: expose health check code in UI (#7773) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29198](https://github.com/argoproj/argo-cd/pull/29198) feat(cli): implement OAuth 2.0 Device Authorization Grant (Beta) | Needs review | Merge | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29236](https://github.com/argoproj/argo-cd/pull/29236) feat: add seal signing inspection command | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29236](https://github.com/argoproj/argo-cd/pull/29236) feat: add seal signing inspection command | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29236](https://github.com/argoproj/argo-cd/pull/29236) feat: add seal signing inspection command | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29236](https://github.com/argoproj/argo-cd/pull/29236) feat: add seal signing inspection command | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29322](https://github.com/argoproj/argo-cd/pull/29322) feat(appset): add metrics for appset to measure rollout durations for progressive sync | Merge | Merge | not judged |  |
| argo-cd | [#29647](https://github.com/argoproj/argo-cd/pull/29647) refactor: filter appset file patterns in the repo-server | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29926](https://github.com/argoproj/argo-cd/pull/29926) feat: allow rollback while auto-sync is enabled | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29926](https://github.com/argoproj/argo-cd/pull/29926) feat: allow rollback while auto-sync is enabled | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29926](https://github.com/argoproj/argo-cd/pull/29926) feat: allow rollback while auto-sync is enabled | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#29926](https://github.com/argoproj/argo-cd/pull/29926) feat: allow rollback while auto-sync is enabled | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30028](https://github.com/argoproj/argo-cd/pull/30028) feat(syncPolicy): Allow to define prune by default for manual sync applications. | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedRevisionOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30033](https://github.com/argoproj/argo-cd/pull/30033) feat(util): add signedTagsOnly option for source integrity | Merge | Merge | not judged |  |
| argo-cd | [#30132](https://github.com/argoproj/argo-cd/pull/30132) fix(hydrator): point README clone command at dry source repo (#29197) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#30244](https://github.com/argoproj/argo-cd/pull/30244) feat: add enableDNS flag for Helm (#17596) | Merge | Merge | not judged |  |
| argo-cd | [#30352](https://github.com/argoproj/argo-cd/pull/30352) feat: add sso.autoLogin to redirect the login page to SSO (#8027, #7918) | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| argo-cd | [#30359](https://github.com/argoproj/argo-cd/pull/30359) feat: add observed generation to applicationset controller  | Merge | Merge | not judged |  |
| argo-cd | [#30359](https://github.com/argoproj/argo-cd/pull/30359) feat: add observed generation to applicationset controller  | Merge | Merge | not judged |  |
| argo-cd | [#30359](https://github.com/argoproj/argo-cd/pull/30359) feat: add observed generation to applicationset controller  | Merge | Merge | not judged |  |
| argo-cd | [#30359](https://github.com/argoproj/argo-cd/pull/30359) feat: add observed generation to applicationset controller  | Merge | Merge | not judged |  |
| argo-cd | [#30645](https://github.com/argoproj/argo-cd/pull/30645) feat(applicationset): support GitLab pull request generator mTLS (#30644) | Merge | Merge | not judged |  |
| argo-cd | [#30645](https://github.com/argoproj/argo-cd/pull/30645) feat(applicationset): support GitLab pull request generator mTLS (#30644) | Merge | Merge | not judged |  |
| cometbft-cosmos-sdk | [#6100](https://github.com/cometbft/cometbft/pull/6100) fix(types,state): enforce minimum Block.MaxBytes floor and handle small limits defensively | Merge | Merge | compiles |  |
| containerd | [#12829](https://github.com/containerd/containerd/pull/12829) Fix transfer-service registry host config to support multi-root config_path | Merge | Merge | not judged |  |
| containerd | [#12951](https://github.com/containerd/containerd/pull/12951) cri: add configurable DNS servers for resolving registry hostnames | Merge | Merge | not judged |  |
| containerd | [#13822](https://github.com/containerd/containerd/pull/13822) cri: implement pod-level checkpoint/restore (KEP-5823) | Merge | Merge | not judged |  |
| containerd | [#13822](https://github.com/containerd/containerd/pull/13822) cri: implement pod-level checkpoint/restore (KEP-5823) | Merge | Merge | not judged |  |
| containerd | [#13822](https://github.com/containerd/containerd/pull/13822) cri: implement pod-level checkpoint/restore (KEP-5823) | Merge | Merge | not judged |  |
| containerd | [#13822](https://github.com/containerd/containerd/pull/13822) cri: implement pod-level checkpoint/restore (KEP-5823) | Merge | Merge | not judged |  |
| containerd | [#13908](https://github.com/containerd/containerd/pull/13908) cri: Upgrade go-criu to v8 | Merge | Merge | not judged |  |
| containerd | [#14453](https://github.com/containerd/containerd/pull/14453) Update NRI to latest (0.12.4) | Merge | Merge | not judged |  |
| containerd | [#14453](https://github.com/containerd/containerd/pull/14453) Update NRI to latest (0.12.5) | Merge | Merge | not judged |  |
| containerd | [#14453](https://github.com/containerd/containerd/pull/14453) Update NRI to latest (0.12.4) | Merge | Merge | not judged |  |
| containerd | [#14453](https://github.com/containerd/containerd/pull/14453) Update NRI to latest (0.12.5) | Merge | Merge | not judged |  |
| containerd | [#14477](https://github.com/containerd/containerd/pull/14477) [release/2.4] Update NRI to latest (0.12.5) | Merge | Merge | not judged |  |
| containerd | [#14477](https://github.com/containerd/containerd/pull/14477) [release/2.4] Update NRI to latest (0.12.5) | Merge | Merge | not judged |  |
| cortex | [#7384](https://github.com/cortexproject/cortex/pull/7384) Add per-tenant cardinality API endpoint | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR, NEEDS_REVIEW |
| csi-provisioner | [#603](https://github.com/container-storage-interface/spec/pull/603) Add ControllerGetNodeInfo RPC (alpha) | Merge | Merge | compiles |  |
| csi-provisioner | [#603](https://github.com/container-storage-interface/spec/pull/603) Add ControllerGetNodeInfo RPC (alpha) | Merge | Merge | compiles |  |
| csi-provisioner | [#613](https://github.com/container-storage-interface/spec/pull/613) Add reason to ControllerUnpublishVolumeRequest | Merge | Merge | compiles |  |
| csi-provisioner | [#613](https://github.com/container-storage-interface/spec/pull/613) Add reason to ControllerUnpublishVolumeRequest | Merge | Merge | compiles |  |
| dapr | [#9974](https://github.com/dapr/dapr/pull/9974) feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#9974](https://github.com/dapr/dapr/pull/9974) feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#9974](https://github.com/dapr/dapr/pull/9974) feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#9974](https://github.com/dapr/dapr/pull/9974) feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#9974](https://github.com/dapr/dapr/pull/9974) feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#10322](https://github.com/dapr/dapr/pull/10322) Feat/conversation max tokens | Merge | Merge | compiles |  |
| dapr | [#10322](https://github.com/dapr/dapr/pull/10322) Feat/conversation max tokens | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary store building block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10367](https://github.com/dapr/dapr/pull/10367) Binary storebuilding block support | Merge | Merge | compiles |  |
| dapr | [#10536](https://github.com/dapr/dapr/pull/10536) Actors: send Dapr-Reentrancy-Id on reminder and timer callbacks | Merge | Merge | compiles |  |
| dapr | [#10682](https://github.com/dapr/dapr/pull/10682) Security: Scheduler accepted actor reminders targeting another app's internal workflow actors | Merge | Merge | compiles |  |
| dapr | [#10682](https://github.com/dapr/dapr/pull/10682) Security: Scheduler accepted actor reminders targeting another app's internal workflow actors | Merge | Merge | compiles |  |
| dapr | [#10682](https://github.com/dapr/dapr/pull/10682) Security: Scheduler accepted actor reminders targeting another app's internal workflow actors | Merge | Merge | compiles |  |
| dapr | [#10717](https://github.com/dapr/dapr/pull/10717) jobs: allow overriding the app route a triggered job is delivered on | Merge | Merge | compiles |  |
| dapr | [#10771](https://github.com/dapr/dapr/pull/10771) [Backport release-1.19] Binary store building block support | Merge | Merge | compiles |  |
| dapr | [#10866](https://github.com/dapr/dapr/pull/10866) [Backport release-1.19] feat: search and vector blocks | Merge | Merge | compiles |  |
| dapr | [#11003](https://github.com/dapr/dapr/pull/11003) Add app error details to dead-letter pub/sub messages | Merge | Merge | compiles |  |
| istio | [#3088](https://github.com/istio/api/pull/3088) Doc: Add note on DR workloadSelector | Merge | Merge | compiles |  |
| istio | [#3722](https://github.com/istio/api/pull/3722) feat(tracing): add otel always_on sampler | Merge | Merge | compiles |  |
| istio | [#3787](https://github.com/istio/api/pull/3787)  add cert_signer_namespace_map field to MeshConfig for namespace-scoped CSR signer authorization | Merge | Merge | compiles |  |
| istio | [#3791](https://github.com/istio/api/pull/3791) docs: use camelCase prefixRewrite in HTTPRedirect example | Merge | Merge | compiles |  |
| istio | [#3792](https://github.com/istio/api/pull/3792) docs: expose presence field in JWTRule reference docs | Merge | Merge | compiles |  |
| istio | [#3796](https://github.com/istio/api/pull/3796) destinationrule: add hash_balance_factor to ConsistentHashLB | Merge | Merge | compiles |  |
| istio | [#3797](https://github.com/istio/api/pull/3797) docs: distinguish authorization rule matching from allowing | Merge | Merge | compiles |  |
| istio | [#3798](https://github.com/istio/api/pull/3798) docs: clarify maxConnections applies to HTTP/2 | Merge | Merge | compiles |  |
| istio | [#3799](https://github.com/istio/api/pull/3799) Allow 63-character WorkloadEntry port names | Merge | Merge | compiles |  |
| istio | [#3801](https://github.com/istio/api/pull/3801) feat: add `presence: IGNORED` and `failedStatusInMetadata` to JWTRule | Merge | Merge | compiles |  |
| istio | [#3801](https://github.com/istio/api/pull/3801) feat: add `presence: IGNORED` and `failedStatusInMetadata` to JWTRule | Merge | Merge | compiles |  |
| istio | [#3809](https://github.com/istio/api/pull/3809) document case-insensitive method matching in authorizationpolicy | Merge | Merge | compiles |  |
| istio | [#3810](https://github.com/istio/api/pull/3810) fix wasm docs | Merge | Merge | compiles |  |
| istio | [#3818](https://github.com/istio/api/pull/3818) networking: add retryBudget to DestinationRule portLevelSettings | Merge | Merge | compiles |  |
| istio | [#3819](https://github.com/istio/api/pull/3819) security: add payloadToMetadata to JWTRule to keep claims of all tokens | Merge | Merge | compiles |  |
| jaeger | [#231](https://github.com/jaegertracing/jaeger-idl/pull/231) feat(expression): Add phrase and fulltext text-search operators | Needs review | Needs review | compiles | OPTION_CHANGED |
| jaeger | [#237](https://github.com/jaegertracing/jaeger-idl/pull/237) feat(api_v3): Add a sql field to TraceQueryParameters and an ExplainQuery RPC | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| lnd | [#9457](https://github.com/lightningnetwork/lnd/pull/9457) routerrpc: add option PreventSubsequentPayment to TrackPaymentV2 | Merge | Merge | compiles |  |
| lnd | [#9888](https://github.com/lightningnetwork/lnd/pull/9888) Attributable failures | Merge | Merge | bump_side_effect |  |
| lnd | [#9907](https://github.com/lightningnetwork/lnd/pull/9907)   routing: add mission control namespace support to SendPaymentV2 | Merge | Merge | compiles |  |
| lnd | [#10067](https://github.com/lightningnetwork/lnd/pull/10067) Fees: add fractional sat/vB support (lncli) and sats_per_kw (RPC) | Merge | Merge | compiles |  |
| lnd | [#10067](https://github.com/lightningnetwork/lnd/pull/10067) Fees: add fractional sat/vB support (lncli) and sats_per_kw (RPC) | Merge | Merge | compiles |  |
| lnd | [#10067](https://github.com/lightningnetwork/lnd/pull/10067) Fees: add fractional sat/vB support (lncli) and sats_per_kw (RPC) | Merge | Merge | compiles |  |
| lnd | [#10316](https://github.com/lightningnetwork/lnd/pull/10316) Invoice rpc metadata support | Merge | Merge | compiles |  |
| lnd | [#10411](https://github.com/lightningnetwork/lnd/pull/10411) aliasmgr: Allow persisting manually added alias scids | Merge | Merge | compiles |  |
| lnd | [#10425](https://github.com/lightningnetwork/lnd/pull/10425) RBF Coop Close using sat/kw instead of sat/vb | Merge | Merge | compiles |  |
| lnd | [#10504](https://github.com/lightningnetwork/lnd/pull/10504) lnwallet/btcwallet: support taproot script path fee estimation in FundPSBT | Merge | Merge | compiles |  |
| lnd | [#10624](https://github.com/lightningnetwork/lnd/pull/10624) multi: expose local and remote spendable balance in listchannels | Merge | Merge | compiles |  |
| lnd | [#10624](https://github.com/lightningnetwork/lnd/pull/10624) multi: expose local and remote spendable balance in listchannels | Merge | Merge | compiles |  |
| lnd | [#10624](https://github.com/lightningnetwork/lnd/pull/10624) multi: expose local and remote spendable balance in listchannels | Merge | Merge | compiles |  |
| lnd | [#10624](https://github.com/lightningnetwork/lnd/pull/10624) multi: expose local and remote spendable balance in listchannels | Merge | Merge | compiles |  |
| lnd | [#10670](https://github.com/lightningnetwork/lnd/pull/10670) Add raw transaction hex to `pendingsweeps` response | Merge | Merge | compiles |  |
| lnd | [#10670](https://github.com/lightningnetwork/lnd/pull/10670) Add raw transaction hex to `pendingsweeps` response | Merge | Merge | compiles |  |
| lnd | [#10685](https://github.com/lightningnetwork/lnd/pull/10685) Update AddHoldInvoice to add support for optional preimage/hash generation | Merge | Merge | compiles |  |
| lnd | [#10735](https://github.com/lightningnetwork/lnd/pull/10735) Freebie onion message slot and per-peer stats in ListPeers | Merge | Merge | compiles |  |
| lnd | [#10744](https://github.com/lightningnetwork/lnd/pull/10744) lnrpc: add scid filter to ListChannels RPC and lncli | Merge | Merge | compiles |  |
| lnd | [#10798](https://github.com/lightningnetwork/lnd/pull/10798) Add BIP-0322 message signing to `SignMessageWithAddr` RPC | Merge | Merge | compiles |  |
| lnd | [#10807](https://github.com/lightningnetwork/lnd/pull/10807) chainntnfs: add a pkscript notifier stream | Merge | Merge | compiles |  |
| lnd | [#10889](https://github.com/lightningnetwork/lnd/pull/10889) Remove deprecated fee rate option --sat_per_byte | Merge | Merge | compiles |  |
| lnd | [#10943](https://github.com/lightningnetwork/lnd/pull/10943) lnrpc/chainrpc: surface re-org depth and Done over the chain notifier | Merge | Merge | compiles |  |
| lnd | [#10973](https://github.com/lightningnetwork/lnd/pull/10973) multi: expose peer address sources and offline peers in ListPeers | Merge | Merge | compiles |  |
| lnd | [#10976](https://github.com/lightningnetwork/lnd/pull/10976) multi: add `--forget_node` and `--forget_address` to `lncli disconnect` | Merge | Merge | compiles |  |
| lnd | [#10993](https://github.com/lightningnetwork/lnd/pull/10993) walletrpc: return the master key birthday from ListAccounts | Merge | Merge | compiles |  |
| lnd | [#11013](https://github.com/lightningnetwork/lnd/pull/11013) routerrpc: refuse local dispatch on a switchrpc build | Merge | Merge | compiles |  |
| lnd | [#11095](https://github.com/lightningnetwork/lnd/pull/11095) keychain+walletrpc: add DeriveAndStoreKey | Merge | Merge | compiles |  |
| lnd | [#11095](https://github.com/lightningnetwork/lnd/pull/11095) keychain+walletrpc: add DeriveAndStoreKey | Merge | Merge | compiles |  |
| lnd | [#11244](https://github.com/lightningnetwork/lnd/pull/11244) routerrpc: correct timeout_seconds field documentation | Merge | Merge | compiles |  |
| lnd | [#11282](https://github.com/lightningnetwork/lnd/pull/11282) multi: add switchrpc external HTLC dispatch subsystem | Merge | Merge | compiles |  |
| lnd | [#11327](https://github.com/lightningnetwork/lnd/pull/11327) lnrpc: make forwarding package counts optional | Merge | Merge | compiles |  |
| lnd | [#11365](https://github.com/lightningnetwork/lnd/pull/11365) multi: add reverse ordering to listchaintxns | Merge | Merge | compiles |  |
| lnd | [#11365](https://github.com/lightningnetwork/lnd/pull/11365) multi: add reverse ordering to listchaintxns | Merge | Merge | compiles |  |
| lnd | [#11365](https://github.com/lightningnetwork/lnd/pull/11365) multi: add reverse ordering to listchaintxns | Merge | Merge | compiles |  |
| lnd | [#11365](https://github.com/lightningnetwork/lnd/pull/11365) multi: add reverse ordering to listchaintxns | Merge | Merge | compiles |  |
| lnd | [#11365](https://github.com/lightningnetwork/lnd/pull/11365) multi: add reverse ordering to listchaintxns | Merge | Merge | compiles |  |
| lnd | [#11374](https://github.com/lightningnetwork/lnd/pull/11374) bolt12handler+devrpc: dispatch invoice requests and add CreateOffer | Merge | Merge | compiles |  |
| lnd | [#11374](https://github.com/lightningnetwork/lnd/pull/11374) bolt12handler+devrpc: dispatch invoice requests and add CreateOffer | Merge | Merge | compiles |  |
| lnd | [#11396](https://github.com/lightningnetwork/lnd/pull/11396) walletrpc: make no-expiry leases explicit | Needs review | Merge | compiles | WHOLE_MESSAGE_FLOW, DESCRIPTOR_REFLECTION |
| lnd | [#11396](https://github.com/lightningnetwork/lnd/pull/11396) walletrpc: make no-expiry leases explicit | Needs review | Merge | compiles | WHOLE_MESSAGE_FLOW, DESCRIPTOR_REFLECTION |
| lnd | [#11422](https://github.com/lightningnetwork/lnd/pull/11422) funding: reject new static remote key channels | Merge | Merge | compiles |  |
| lnd | [#11422](https://github.com/lightningnetwork/lnd/pull/11422) funding: reject new static remote key channels | Merge | Merge | compiles |  |
| lnd | [#11439](https://github.com/lightningnetwork/lnd/pull/11439) routing: add experimental fee levels to mission control | Merge | Merge | compiles |  |
| loki | [#24984](https://github.com/grafana/loki/pull/24984) feat(logql): Track stream-first query stats, add integration test | Merge | Merge | not judged |  |
| loki | [#24984](https://github.com/grafana/loki/pull/24984) feat(logql): Track stream-first query stats, add integration test | Merge | Merge | not judged |  |
| loki | [#24991](https://github.com/grafana/loki/pull/24991) feat(logline): Report Logline query stats on the metrics.go line | Merge | Merge | not judged |  |
| loki | [#25002](https://github.com/grafana/loki/pull/25002) feat(logql): Log stream-first and timestamp-first query counts in query stats | Merge | Merge | not judged |  |
| loki | [#25006](https://github.com/grafana/loki/pull/25006) feat(pattern-ingester): Add a gRPC method that accepts InternalPushRequest  | Needs review | Needs review | not judged | NEEDS_REVIEW |
| loki | [#25024](https://github.com/grafana/loki/pull/25024) feat(dataobj-compactor): Add an IndexFilter compaction task | Merge | Merge | not judged |  |
| loki | [#25027](https://github.com/grafana/loki/pull/25027) feat(dataobj-compactor): Keep unmerged runs by filtering the source index | Merge | Merge | not judged |  |
| loki | [#25034](https://github.com/grafana/loki/pull/25034) feat(querier): Add object-store and section resolution metrics to data-object queries | Merge | Merge | not judged |  |
| loki | [#25077](https://github.com/grafana/loki/pull/25077) fix(logline): Recompute effective concurrency across parallel hint lookups | Merge | Merge | not judged |  |
| loki | [#25077](https://github.com/grafana/loki/pull/25077) fix(logline): Recompute effective concurrency across parallel hint lookups | Merge | Merge | not judged |  |
| loki | [#25082](https://github.com/grafana/loki/pull/25082) feat(logline): Report Logline stats and outcome in data.stats.logline | Don't merge | Needs review | not judged | UNRESOLVED_MEMBER |
| loki | [#25117](https://github.com/grafana/loki/pull/25117) feat(dataobj): Decide data object routing in the query-frontend | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| loki | [#25117](https://github.com/grafana/loki/pull/25117) feat(dataobj): Decide data object routing in the query-frontend | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| loki | [#25208](https://github.com/grafana/loki/pull/25208) fix(storage): Remove propagate_chunk_fetch_errors flag. Part 1 | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25208](https://github.com/grafana/loki/pull/25208) fix(storage): Remove propagate_chunk_fetch_errors flag | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25208](https://github.com/grafana/loki/pull/25208) fix(storage): Remove propagate_chunk_fetch_errors flag. Part 1 | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25259](https://github.com/grafana/loki/pull/25259) perf(logline): Run pass-through intervals without waiting for the hint lookup | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25259](https://github.com/grafana/loki/pull/25259) perf(logline): Run pass-through intervals without waiting for the hint lookup | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25425](https://github.com/grafana/loki/pull/25425) feat(logline): Plan OR-aware hint needles | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25436](https://github.com/grafana/loki/pull/25436) refactor(compactor): Delete sort object task | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25501](https://github.com/grafana/loki/pull/25501) feat(server): Enable configurable TLS curve preferences | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25501](https://github.com/grafana/loki/pull/25501) feat(server): Enable configurable TLS curve preferences | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25501](https://github.com/grafana/loki/pull/25501) feat(server): Enable configurable TLS group preferences | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25557](https://github.com/grafana/loki/pull/25557) refactor(dataobj): Move the layout information to the streams section | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25557](https://github.com/grafana/loki/pull/25557) refactor(dataobj): Move the layout information to the streams section | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25575](https://github.com/grafana/loki/pull/25575) feat(dataobj): Record the stream layout in the streams section | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25578](https://github.com/grafana/loki/pull/25578) feat(dataobj): Read the stream layout only from the streams section | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25629](https://github.com/grafana/loki/pull/25629) refactor(dataobj-compactor): Write common sort layout into stats section headers | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25629](https://github.com/grafana/loki/pull/25629) refactor(dataobj-compactor): Write common sort layout into stats section headers | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25719](https://github.com/grafana/loki/pull/25719) chore(deps): Update module go.etcd.io/etcd/api/v3 to v3.7.2 (release-3.7.x) | Merge | Merge | not judged |  |
| loki | [#25719](https://github.com/grafana/loki/pull/25719) chore(deps): Update module go.etcd.io/etcd/api/v3 to v3.7.3 (release-3.7.x) | Merge | Merge | not judged |  |
| loki | [#25736](https://github.com/grafana/loki/pull/25736) chore(deps): Update module go.etcd.io/etcd/client/v3 to v3.7.3 (release-3.7.x) | Merge | Merge | not judged |  |
| loki | [#25747](https://github.com/grafana/loki/pull/25747) fix(queryrange): Preserve scan statistics for detected-field queries | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR |
| loki | [#25755](https://github.com/grafana/loki/pull/25755) fix(ingester): Stamp backfilled chunks with the Kafka record timestamp | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25755](https://github.com/grafana/loki/pull/25755) fix(ingester): Stamp backfilled chunks with the Kafka record timestamp | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25798](https://github.com/grafana/loki/pull/25798) feat(dataobj-compactor): Split large tasks into parallelisable sub-tasks by size | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25798](https://github.com/grafana/loki/pull/25798) feat(dataobj-compactor): Split large tasks into parallelisable sub-tasks by size | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25848](https://github.com/grafana/loki/pull/25848) chore(deps): Update module k8s.io/client-go to v0.37.1 (release-3.7.x) | Merge | Merge | not judged |  |
| loki | [#25888](https://github.com/grafana/loki/pull/25888) chore(deps): Update module github.com/containerd/containerd/v2 to v2.4.2 (release-3.7.x) | Merge | Merge | not judged |  |
| loki | [#25950](https://github.com/grafana/loki/pull/25950) refactor(logql): Move pkg/logqlmodel to pkg/logql/model | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR, TOOLCHAIN_TOO_OLD |
| loki | [#25964](https://github.com/grafana/loki/pull/25964) feat!: Upgrade Go module to v4 | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR, TOOLCHAIN_TOO_OLD |
| loki | [#25971](https://github.com/grafana/loki/pull/25971) refactor(ingester): Pass the Kafka record timestamp on the push request | Needs review | Needs review | not judged | TOOLCHAIN_TOO_OLD |
| loki | [#25972](https://github.com/grafana/loki/pull/25972) feat!: Upgrade Go module to github.com/grafana/loki/v4 | Needs review | Needs review | not judged | CONTRACT_COMPILE_ERROR, TOOLCHAIN_TOO_OLD |
| spire | [#102](https://github.com/spiffe/spire-api-sdk/pull/102) Add unauthenticated server Version GetVersion API | Merge | Merge | compiles |  |
| temporal | [#781](https://github.com/temporalio/api/pull/781) add GetWorkflowExecutionResult as a system nexus endpoint | Merge | Merge | not judged |  |
| temporal | [#827](https://github.com/temporalio/api/pull/827) Add RESOURCE_EXHAUSTED_CAUSE_CALLER_RPS_LIMIT resource-exhausted cause | Merge | Merge | not judged |  |
| temporal | [#852](https://github.com/temporalio/api/pull/852) Task queue config for whole-queue concurrency limit | Merge | Merge | not judged |  |
| temporal | [#852](https://github.com/temporalio/api/pull/852) Task queue config for whole-queue concurrency limit | Merge | Merge | not judged |  |
| temporal | [#856](https://github.com/temporalio/api/pull/856) vts: add time skipping to schedules | Merge | Merge | not judged |  |
| temporal | [#856](https://github.com/temporalio/api/pull/856) vts: add time skipping to schedules | Merge | Merge | not judged |  |
| temporal | [#856](https://github.com/temporalio/api/pull/856) vts: add time skipping to schedules | Merge | Merge | not judged |  |
| temporal | [#856](https://github.com/temporalio/api/pull/856) vts: add time skipping to schedules | Merge | Merge | not judged |  |
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
| temporal | [#876](https://github.com/temporalio/api/pull/876) Add eager standalone activity start API | Merge | Merge | not judged |  |
| temporal | [#877](https://github.com/temporalio/api/pull/877) Add resource id annotation for standalone Nexus operations | Needs review | Needs review | not judged | OPTION_CHANGED, DESCRIPTOR_REFLECTION |
| temporal | [#877](https://github.com/temporalio/api/pull/877) Add resource id annotation for standalone Nexus operations | Needs review | Needs review | not judged | OPTION_CHANGED, DESCRIPTOR_REFLECTION |
| temporal | [#878](https://github.com/temporalio/api/pull/878) Deprecate BatchOperationResetActivities.reset_attempts | Merge | Merge | not judged |  |
| temporal | [#880](https://github.com/temporalio/api/pull/880) Add Graal AOT and Kotlin worker runtimes | Merge | Merge | not judged |  |
| temporal | [#882](https://github.com/temporalio/api/pull/882) ACT-1185: Expose standalone activity principals in Describe API | Merge | Merge | not judged |  |
| temporal | [#882](https://github.com/temporalio/api/pull/882) ACT-1185: Expose standalone activity principals in Describe API | Merge | Merge | not judged |  |
| temporal | [#882](https://github.com/temporalio/api/pull/882) ACT-1185: Expose standalone activity principals in Describe API | Merge | Merge | not judged |  |
| temporal | [#882](https://github.com/temporalio/api/pull/882) ACT-1185: Expose standalone activity principals in Describe API | Merge | Merge | not judged |  |
| temporal | [#883](https://github.com/temporalio/api/pull/883) Adding PropagatedNexusSerializationContext to UpdateWorkflow apis | Merge | Merge | not judged |  |
| temporal | [#884](https://github.com/temporalio/api/pull/884) Add activity async handoff API definitions | Don't merge | Merge | not judged |  |
| temporal | [#886](https://github.com/temporalio/api/pull/886) Document current activity attempt start time | Merge | Merge | not judged |  |
| temporal | [#886](https://github.com/temporalio/api/pull/886) Document current activity attempt start time | Merge | Merge | not judged |  |
| temporal | [#887](https://github.com/temporalio/api/pull/887) Add PollerScalingInfo to poll requests | Merge | Merge | not judged |  |
| temporal | [#887](https://github.com/temporalio/api/pull/887) Report poller target on poll requests and in the worker heartbeat | Merge | Merge | not judged |  |
| temporal | [#887](https://github.com/temporalio/api/pull/887) Report poller target on poll requests and in the worker heartbeat | Merge | Merge | not judged |  |
| temporal | [#890](https://github.com/temporalio/api/pull/890) marking time skipping API experimental | Merge | Merge | not judged |  |
| temporal | [#891](https://github.com/temporalio/api/pull/891) PoC Workflow Heartbeat Notification | Merge | Merge | not judged |  |
| temporal | [#891](https://github.com/temporalio/api/pull/891) PoC Workflow Heartbeat Notification | Merge | Merge | not judged |  |
| temporal | [#891](https://github.com/temporalio/api/pull/891) PoC Workflow Heartbeat Notification | Merge | Merge | not judged |  |
| temporal | [#893](https://github.com/temporalio/api/pull/893) Propose basic session API shape | Don't merge | Merge | not judged | WHOLE_MESSAGE_FLOW |
| temporal | [#893](https://github.com/temporalio/api/pull/893) Propose basic session API shape | Don't merge | Merge | not judged | WHOLE_MESSAGE_FLOW |
| temporal | [#897](https://github.com/temporalio/api/pull/897) Require a temporal-resource-id annotation or exemption on every RPC | Needs review | Needs review | not judged | OPTION_CHANGED, DESCRIPTOR_REFLECTION |
| temporal | [#899](https://github.com/temporalio/api/pull/899) Add RPC definitions for namespace soft deletion and restoration | Merge | Merge | not judged |  |
| temporal | [#899](https://github.com/temporalio/api/pull/899) Add RPC definitions for namespace soft deletion and restoration | Merge | Merge | not judged |  |
| temporal | [#899](https://github.com/temporalio/api/pull/899) Add RPC definitions for namespace soft deletion and restoration | Merge | Merge | not judged |  |
