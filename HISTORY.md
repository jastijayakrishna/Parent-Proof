# History: real upgrades, judged by the compiler

Every row is one upgrade a project really made of a contract module it
uses, mined from its git history. The Go compiler builds the project's code
at that upgrade against the old and the new module. A break is an upgrade
the compiler says breaks the build; caught means the verifier said NO-GO for
the build. None of these projects was used to tune the verifier.

| upgrades | compiler breaks | caught | wrong GO | compiler-safe | GO | false NO-GO | UNKNOWN (build) |
|---|---|---|---|---|---|---|---|
| 55 | 7 | 6 | 1 | 31 | 30 | 0 | 1 |

## By project

| contract -> project | upgrades | breaks | caught | wrong GO | false NO-GO | UNKNOWN |
|---|---|---|---|---|---|---|
| containerd-api -> nerdctl | 7 | 0 | 0 | 0 | 0 | 0 |
| cri-api -> containerd | 7 | 2 | 1 | 1 | 0 | 0 |
| cri-api -> cri-o | 8 | 1 | 1 | 0 | 0 | 1 |
| dapr -> go-sdk | 15 | 4 | 4 | 0 | 0 | 0 |
| lnd -> lndclient | 6 | 0 | 0 | 0 | 0 | 0 |
| otlp -> otel-go | 12 | 0 | 0 | 0 | 0 | 0 |

## Every break and every disagreement

| contract -> project | upgrade | compiler | verifier (build) | UNKNOWN because |
|---|---|---|---|---|
| cri-api -> containerd | v0.36.1 -> v0.36.3 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW, UNRESOLVED_MEMBER, WHOLE_MESSAGE_FLOW |
| cri-api -> containerd | v0.27.1 -> v0.28.0-beta.0 | breaks | GO (GO) |  |
| cri-api -> cri-o | v0.34.0-beta.0 -> v0.34.0-rc.2 | compiles | UNKNOWN (UNKNOWN) | OPTION_CHANGED |
| cri-api -> cri-o | v0.33.0-beta.0.0.20250313010358-ab383b81657e -> v0.33.0-beta.0.0.20250324233632-87ee4e17aba6 | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.12.0-rc.4 -> v1.12.1-0.20231013174004-b6540a1c464d | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.12.1-0.20231013174004-b6540a1c464d -> v1.12.1-0.20231030205344-441017b888c5 | breaks | NO_GO (NO_GO) |  |
| dapr -> go-sdk | v1.14.0-rc.2 -> v1.14.0-rc.5 | breaks | NO_GO (NO_GO) | NEEDS_REVIEW |
| dapr -> go-sdk | v1.15.0-rc.9 -> v1.15.0-rc.17 | breaks | NO_GO (NO_GO) |  |
