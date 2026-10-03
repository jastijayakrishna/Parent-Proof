# History: real upgrades, judged by the compiler

Every row is one upgrade a project really made of a contract module it
uses, mined from its git history. The Go compiler builds the project's code
at that upgrade against the old and the new module. A break is an upgrade
the compiler says breaks the build; caught means the verifier said NO-GO for
the build. None of these projects was used to tune the verifier.

| upgrades | compiler breaks | caught | wrong GO | compiler-safe | GO | false NO-GO | UNKNOWN (build) |
|---|---|---|---|---|---|---|---|
| 127 | 20 | 18 | 2 | 84 | 81 | 0 | 3 |

## By project

| contract -> project | upgrades | breaks | caught | wrong GO | false NO-GO | UNKNOWN |
|---|---|---|---|---|---|---|
| containerd-api -> nerdctl | 14 | 0 | 0 | 0 | 0 | 0 |
| cri-api -> containerd | 14 | 4 | 2 | 2 | 0 | 0 |
| cri-api -> cri-o | 16 | 2 | 2 | 0 | 0 | 2 |
| dapr -> go-sdk | 30 | 8 | 8 | 0 | 0 | 0 |
| lnd -> lndclient | 12 | 0 | 0 | 0 | 0 | 0 |
| otlp -> otel-go | 24 | 0 | 0 | 0 | 0 | 0 |
| tipb -> tidb | 17 | 6 | 6 | 0 | 0 | 1 |

## Every break and every disagreement

| contract -> project | upgrade | compiler | verifier (build) | UNKNOWN because |
|---|---|---|---|---|
| cri-api -> containerd | v0.36.1 -> v0.36.3 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW, UNRESOLVED_MEMBER, WHOLE_MESSAGE_FLOW |
| cri-api -> containerd | v0.27.1 -> v0.28.0-beta.0 | breaks | GO (GO) |  |
| cri-api -> containerd | v0.36.1 -> v0.36.3 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW, UNRESOLVED_MEMBER, WHOLE_MESSAGE_FLOW |
| cri-api -> containerd | v0.27.1 -> v0.28.0-beta.0 | breaks | GO (GO) |  |
| cri-api -> cri-o | v0.34.0-beta.0 -> v0.34.0-rc.2 | compiles | UNKNOWN (UNKNOWN) | OPTION_CHANGED |
| cri-api -> cri-o | v0.33.0-beta.0.0.20250313010358-ab383b81657e -> v0.33.0-beta.0.0.20250324233632-87ee4e17aba6 | breaks | NO_GO (NO_GO) |  |
| cri-api -> cri-o | v0.34.0-beta.0 -> v0.34.0-rc.2 | compiles | UNKNOWN (UNKNOWN) | OPTION_CHANGED |
| cri-api -> cri-o | v0.33.0-beta.0.0.20250313010358-ab383b81657e -> v0.33.0-beta.0.0.20250324233632-87ee4e17aba6 | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.12.0-rc.4 -> v1.12.1-0.20231013174004-b6540a1c464d | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.12.1-0.20231013174004-b6540a1c464d -> v1.12.1-0.20231030205344-441017b888c5 | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.14.0-rc.2 -> v1.14.0-rc.5 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW |
| dapr -> go-sdk | v1.15.0-rc.9 -> v1.15.0-rc.17 | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.12.0-rc.4 -> v1.12.1-0.20231013174004-b6540a1c464d | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.12.1-0.20231013174004-b6540a1c464d -> v1.12.1-0.20231030205344-441017b888c5 | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.14.0-rc.2 -> v1.14.0-rc.5 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW |
| dapr -> go-sdk | v1.15.0-rc.9 -> v1.15.0-rc.17 | breaks | NO_GO (NO_GO) |  |
| tipb -> tidb | v0.0.0-20250513092957-b555ca3fc078 -> v0.0.0-20250529123214-bb8180a479ec | breaks | NO_GO (NO_GO) | WHOLE_MESSAGE_FLOW, NEEDS_REVIEW |
| tipb -> tidb | v0.0.0-20240823074000-a40c2347786e -> v0.0.0-20240919023442-cf70966bef25 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW, WHOLE_MESSAGE_FLOW |
| tipb -> tidb | v0.0.0-20230523034258-1bbc3bbbd369 -> v0.0.0-20230602100112-acb7942db1ca | breaks | NO_GO (NO_GO) |  |
| tipb -> tidb | v0.0.0-20240305085524-87f5b80908ab -> v0.0.0-20240318032315-55a7867ddd50 | breaks | NO_GO (NO_GO) | WHOLE_MESSAGE_FLOW |
| tipb -> tidb | v0.0.0-20241022082558-0607513e7fa4 -> v0.0.0-20241105053214-f91fdb81a69e | compiles | UNKNOWN (UNKNOWN) | OPTION_CHANGED |
| tipb -> tidb | v0.0.0-20250321085733-a91a8fafd4ed -> v0.0.0-20250331100511-d2c561dad347 | breaks | NO_GO (NO_GO) | WHOLE_MESSAGE_FLOW |
| tipb -> tidb | v0.0.0-20241212101007-246f91188357 -> v0.0.0-20250321085733-a91a8fafd4ed | breaks | NO_GO (NO_GO) | WHOLE_MESSAGE_FLOW |
