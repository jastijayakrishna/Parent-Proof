# Scale test: pre-registration

Written and committed on 2026-10-21, before the verifier decided any change of the new projects below. Everything
here was fixed before the first decision; any later change is a new commit that says why.

## The question

**On hundreds of real contract changes, most in projects Parent has never seen, does Parent ever say Merge when the
change breaks a project's build?** And how often does it block a safe change, or answer Needs review?

## The binary

`bin/verifier-linux-amd64.gz`: Parent main `f3db8e9` (go-analyzer v0.25.0, rules-protobuf v0.15.0, rules-protobuf-java
v0.11.0, verdict v0.15.0), sha256 `b494ad99de344acfa7f391d9adbf1415e3abc5d3b9cef987c2c1ee14ac862a32`, the build a
customer would install today. Only this binary's decisions are counted ([scale/score.py](score.py) checks each result
directory's recorded binary). **Nothing in Parent changes during the test.**

## What is decided

1. **New projects** ([candidates.json](candidates.json), [plan.json](plan.json), [corpus.json](corpus.json)): 72
   contract → project pairs (66 projects, 32 contract modules), none ever used by Parent or Parent-Proof as that
   pair. Tier 1 (43 pairs, 744 upgrades): the contract and the project are both new. Tier 2 (29 pairs, 437
   upgrades): the contract or the project was used before with other partners, this pair never.
   - **Upgrades**: every real upgrade of the contract module in the project's own history since 2023-01-01 (each one
     a commit in that project, most of them its pull requests), at most the 40 most recent per pair (with any others
     on the day of the 40th). 1,181 upgrades.
   - **Contract commits**: each contract's last 20 commits that change a `.proto` file (most of them merged pull
     requests), decided against one project that uses it, pinned at its head of 2026-10-21 (28 contracts).
2. **Every corpus Parent-Proof already has, rerun on the same binary**: the history of 9 pairs, the Go stress test (dev
   and hold-out), the Java stress test (dev, hold-out, regression), open pull requests decided live. The release gates
   ran on this code this morning (run 39558324304: kvproto 152 and temporal-api 36 equal their baselines, the
   17-project scan equal to main window by window); the build there was the same source with only docs changed since.

How the new pairs were chosen: candidates were listed from the CNCF landscape and well-known Go gRPC ecosystems, then
kept when, by the GitHub API and a probe that only reads git history (workflow `scale-probe`, no verifier):
the project's go.mod requires the contract module without a replace to a fork; neither repository is archived; the
project clones and builds within a job; it upgraded the module at least once since 2023. Every candidate considered,
kept or not, is in [candidates.json](candidates.json) with the reason.

Why at most 40 upgrades per pair: one busy pair must not swamp the count or the budget (Istio's client-go alone has 688
automated upgrades since 2023, Pulumi YAML 113). The cap takes the most recent upgrades, by date only, and was set from
the probe's counts, which say nothing about any outcome.

## The truth

Exactly as the stress test ([stress/PREREG.md](../stress/PREREG.md)):

- **Upgrades** (`verifier suite build`, then `verifier gate`, in [scripts/history.sh](../scripts/history.sh)): the Go
  compiler builds the project's packages that import the module, at the upgrade's parent, against the old and the new
  version (linux/amd64, cgo off, compile only). **Breaks** = a compiler error in the project's own code. Every upgrade
  is judged whether or not Parent's own diff saw a contract change in it: a break in hand-written code of the module
  counts against Parent too.
- **Contract commits** (`verifier gate scan --oracle`): the compiler builds the pinned project against the contract
  before and after the commit, for commits inside the Go module the project builds against.
- **The judge is tested before it judges**: a canary (the contract package the project imports most, removed) must
  fail that project's build first, or the compiler's answers for it count as "judge not verified".
- Not judged, with the reason: the project did not build before the change, the module could not be resolved, the
  build failed without a compiler error, the change is outside a module the project builds.

## The score

For the build, Parent's answer is its `source_build` aspect:

- **caught**: breaks, Parent said Don't merge (with the file and line);
- **stopped with Needs review**: breaks, Parent said Needs review;
- **missed**: breaks, Parent said **Merge**;
- **false alarm**: compiles, Parent said Don't merge;
- **needs review on a safe change**: compiles, Parent said Needs review.

Reported per corpus, per pair, every break, every false alarm, and every Needs review reason: [SCALE.md](../SCALE.md).

## Pass, stop, report

- **Pass**: 0 missed on every judged change of every set.
- **A miss does not stop the runs**: the whole corpus is measured on the same binary, so the count of misses is
  complete; nothing in Parent is fixed during the test, and every miss goes to the founder with the change, the code
  and the cause. (Amended 2026-10-21 08:33 UTC, before any decision of the new projects was committed: the first
  draft stopped at the first miss, which would leave the rest unmeasured.)
- Every false alarm is listed with its cause. Nothing is dropped from the counts after the run: a pair or project whose
  harness failed is listed with what failed.

## Budgets

Every job aims for 15 minutes and is cut at 30 (the compiler's share at 16 minutes, decisions at 9; what finished is
kept). The upgrades run in four waves (`wave` in [plan.json](plan.json)), each about 445 job-minutes, so each run
ends in about 25 minutes with 20 jobs at a time; the contract commits are a fifth run. A pair whose jobs did not
finish gets more shards in a later run, never fewer upgrades. The laptop clones no project.
