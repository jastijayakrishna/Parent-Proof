# History: real upgrades, judged by the compiler

Updated 2026-10-06 14:05 UTC.

Every row is one upgrade a project really made of a contract module it
uses, mined from its git history. The Go compiler builds the project's code
at that upgrade against the old and the new module. None of these projects
was used to tune the verifier.

- **Caught**: the upgrade broke the build and the verifier said *Don't merge*.
- **Missed**: the upgrade broke the build but the verifier said *Merge*.
- **False alarm**: the upgrade was safe but the verifier said *Don't merge*.
- **Needs review**: the verifier could not tell; the row says why.
- **Judge not verified**: the compiler's answer is not counted, because a
  planted break (a canary: the contract package the project imports most,
  removed) did not fail that project's build, so its build may not see the
  contract at all.

| upgrades | judge not verified | broke the build | caught | missed | safe | said Merge | false alarm | needs review |
|---|---|---|---|---|---|---|---|---|
| 178 | 0 | 24 | 21 | 0 | 148 | 125 | 1 | 25 |

## By project

| contract -> project | upgrades | broke the build | caught | missed | false alarm | needs review |
|---|---|---|---|---|---|---|
| containerd-api -> nerdctl | 13 | 0 | 0 | 0 | 1 | 2 |
| cri-api -> containerd | 27 | 4 | 3 | 0 | 0 | 1 |
| cri-api -> cri-o | 33 | 5 | 4 | 0 | 0 | 2 |
| dapr -> go-sdk | 26 | 4 | 4 | 0 | 0 | 0 |
| lnd -> lndclient | 10 | 3 | 3 | 0 | 0 | 1 |
| milvus -> milvus-client | 25 | 2 | 1 | 0 | 0 | 4 |
| milvus -> milvus-sdk-go | 13 | 0 | 0 | 0 | 0 | 4 |
| otlp -> otel-go | 14 | 0 | 0 | 0 | 0 | 10 |
| tipb -> tidb | 17 | 6 | 6 | 0 | 0 | 1 |

## Every break, miss, false alarm and needs-review

| contract -> project | upgrade | compiler | verifier (for the build) | needs review because |
|---|---|---|---|---|
| containerd-api -> nerdctl | v1.7.19 -> v1.8.0-rc.2 | compiles | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW, NEEDS_REVIEW |
| containerd-api -> nerdctl | v1.9.0 -> v1.10.0-rc.0 | compiles | Needs review (Needs review) | GO_API_CHANGED_USED_BY_CALLER |
| containerd-api -> nerdctl | v1.10.0 -> v1.11.0-beta.1 | compiles | Needs review (Needs review) | GO_API_CHANGED_USED_BY_CALLER |
| cri-api -> containerd | v0.33.4 -> v0.34.1 | breaks | Needs review (Needs review) | OPTION_CHANGED, UNRESOLVED_MEMBER |
| cri-api -> containerd | v0.36.1 -> v0.36.3 | breaks | Don't merge (Don't merge) | NEEDS_REVIEW, UNRESOLVED_MEMBER, WHOLE_MESSAGE_FLOW |
| cri-api -> containerd | v0.36.4 -> v0.37.0 | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW, NEEDS_REVIEW |
| cri-api -> containerd | v0.32.3 -> v0.33.0 | breaks | Don't merge (Don't merge) |  |
| cri-api -> cri-o | v0.34.0-beta.0 -> v0.34.0-rc.2 | compiles | Needs review (Needs review) | OPTION_CHANGED |
| cri-api -> cri-o | v0.33.2 -> v0.34.0-beta.0 | breaks | Needs review (Needs review) | OPTION_CHANGED, UNRESOLVED_MEMBER |
| cri-api -> cri-o | v0.34.1 -> v0.35.0-alpha.1 | breaks | Don't merge (Don't merge) |  |
| cri-api -> cri-o | v0.36.3 -> v0.37.0 | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW, NEEDS_REVIEW |
| cri-api -> cri-o | v0.35.1 -> v0.36.0-beta.0 | breaks | Don't merge (Don't merge) | GO_API_CHANGED_USED_BY_CALLER |
| cri-api -> cri-o | v0.33.0-beta.0.0.20250313010358-ab383b81657e -> v0.33.0-beta.0.0.20250324233632-87ee4e17aba6 | breaks | Don't merge (Don't merge) |  |
| dapr -> go-sdk | v1.12.0-rc.4 -> v1.12.1-0.20231013174004-b6540a1c464d | breaks | Don't merge (Don't merge) |  |
| dapr -> go-sdk | v1.12.1-0.20231013174004-b6540a1c464d -> v1.12.1-0.20231030205344-441017b888c5 | breaks | Don't merge (Don't merge) |  |
| dapr -> go-sdk | v1.14.0-rc.2 -> v1.14.0-rc.5 | breaks | Don't merge (Don't merge) | NEEDS_REVIEW |
| dapr -> go-sdk | v1.15.0-rc.9 -> v1.15.0-rc.17 | breaks | Don't merge (Don't merge) |  |
| lnd -> lndclient | v0.19.3-beta -> v0.20.0-beta | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW, DESCRIPTOR_REFLECTION |
| lnd -> lndclient | v0.17.4-beta -> v0.18.4-beta | compiles | Don't merge (Needs review) | GO_API_CHANGED_USED_BY_CALLER |
| lnd -> lndclient | v0.20.1-beta -> v0.21.0-beta | breaks | Don't merge (Don't merge) | DESCRIPTOR_REFLECTION, WHOLE_MESSAGE_FLOW |
| lnd -> lndclient | v0.18.5-beta -> v0.19.0-beta | breaks | Don't merge (Don't merge) | GO_API_CHANGED_USED_BY_CALLER |
| milvus -> milvus-client | v2.3.4-0.20240228061649-a922b16f2a46 -> v2.3.4-0.20240430035521-259ae1d10016 | compiles | Needs review (Needs review) | OPTION_CHANGED, NEEDS_REVIEW |
| milvus -> milvus-client | v2.3.4-0.20240815123953-6dab6fcd6454 -> v2.3.4-0.20241108105827-266fb751b620 | compiles | Don't merge (Needs review) | OPTION_CHANGED |
| milvus -> milvus-client | v2.6.4-0.20251013093953-f3e0a710c654 -> v2.6.5-0.20251102105128-d157e5f676d6 | breaks | Needs review (Needs review) | OPTION_CHANGED |
| milvus -> milvus-client | v2.6.6-0.20251119054300-fcb3986f4af1 -> v2.6.6-0.20251124145901-0b96e4c8af45 | breaks | Don't merge (Don't merge) | NEEDS_REVIEW, WHOLE_MESSAGE_FLOW |
| milvus -> milvus-client | v2.6.6-0.20260309063517-8b5776d31f2b -> v2.6.6-0.20260323081523-53649783989c | compiles | Needs review (Needs review) | OPTION_CHANGED |
| milvus -> milvus-sdk-go | v2.3.1 -> v2.3.2 | compiles | Needs review (Needs review) | OPTION_CHANGED |
| milvus -> milvus-sdk-go | v2.3.3 -> v2.3.4 | compiles | Needs review (Needs review) | OPTION_CHANGED |
| milvus -> milvus-sdk-go | v2.3.4-0.20240109020841-d367b5a59df1 -> v2.4.0-rc.1 | compiles | Needs review (Needs review) | OPTION_CHANGED |
| milvus -> milvus-sdk-go | v2.4.3 -> v2.4.6 | compiles | Needs review (Needs review) | OPTION_CHANGED |
| otlp -> otel-go | v1.3.1 -> v1.4.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE |
| otlp -> otel-go | v0.19.0 -> v0.20.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE |
| otlp -> otel-go | v1.4.0 -> v1.5.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE |
| otlp -> otel-go | v1.5.0 -> v1.6.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE, AMBIENT_GENERATED_UNREAD |
| otlp -> otel-go | v1.6.0 -> v1.7.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE |
| otlp -> otel-go | v1.7.1 -> v1.8.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE |
| otlp -> otel-go | v1.8.0 -> v1.9.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE |
| otlp -> otel-go | v1.9.0 -> v1.10.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE, AMBIENT_GENERATED_UNREAD |
| otlp -> otel-go | v1.1.0 -> v1.2.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE, AMBIENT_GENERATED_UNREAD |
| otlp -> otel-go | v1.0.0 -> v1.1.0 | compiles | Needs review (Needs review) | GENERATED_BINDINGS_UNAVAILABLE, AMBIENT_GENERATED_UNREAD |
| tipb -> tidb | v0.0.0-20250513092957-b555ca3fc078 -> v0.0.0-20250529123214-bb8180a479ec | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW, NEEDS_REVIEW |
| tipb -> tidb | v0.0.0-20240823074000-a40c2347786e -> v0.0.0-20240919023442-cf70966bef25 | breaks | Don't merge (Don't merge) | NEEDS_REVIEW, WHOLE_MESSAGE_FLOW |
| tipb -> tidb | v0.0.0-20230523034258-1bbc3bbbd369 -> v0.0.0-20230602100112-acb7942db1ca | breaks | Don't merge (Don't merge) |  |
| tipb -> tidb | v0.0.0-20240305085524-87f5b80908ab -> v0.0.0-20240318032315-55a7867ddd50 | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW |
| tipb -> tidb | v0.0.0-20241022082558-0607513e7fa4 -> v0.0.0-20241105053214-f91fdb81a69e | compiles | Needs review (Needs review) | OPTION_CHANGED |
| tipb -> tidb | v0.0.0-20250321085733-a91a8fafd4ed -> v0.0.0-20250331100511-d2c561dad347 | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW |
| tipb -> tidb | v0.0.0-20241212101007-246f91188357 -> v0.0.0-20250321085733-a91a8fafd4ed | breaks | Don't merge (Don't merge) | WHOLE_MESSAGE_FLOW |
