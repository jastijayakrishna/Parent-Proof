# proto-shadow

A public, timestamped record of how a contract verifier does on real pull
requests it has never seen.

Every hour a GitHub Actions job finds the open pull requests that change
a `.proto` file in 17 open-source projects (Istio, etcd, raft, Temporal,
containerd, cri-api, Envoy's data-plane-api, Linkerd, SPIFFE, Consul, lnd,
Dapr, authzed, Jaeger, Loki, Cortex, Thanos; the pairs are in
[corpus.json](corpus.json)). For each one it:

1. decides, with the pinned verifier in [bin/](bin/), whether the project that
   uses the contract (Istio for istio/api, etcd for raft, and so on) breaks:
   **GO**, **NO-GO** or **UNKNOWN**;
2. builds that consumer against the pull request's code with the Go compiler,
   which says **compiles** or **breaks**; the verifier never sees this answer;
3. commits both to [predictions/](predictions/) and recounts
   [SCOREBOARD.md](SCOREBOARD.md).

The record is committed while the pull request is still open, so the
prediction cannot be fitted to what happened afterwards. The commit history and
the Actions run linked in each record show when it was made.

## Reading the scoreboard

- **Wrong GO**: the verifier said the consumer still builds; the compiler says
  it breaks. The failure that matters most.
- **False NO-GO**: the verifier said the consumer breaks; the compiler says it
  builds.
- **UNKNOWN**: the verifier could not prove either; each row says why.
- **Not judged**: the compiler could not build the consumer before the change
  either, or the contract's Go code is not in a module the consumer builds
  against. Those predictions are graded later by what happened to the pull
  request (reverts and fix-up commits).

## Checking a record yourself

Each record holds the pull request, the commits decided, the verifier's
version and sha256, and the compiler's result. `bin/VERSION` names the
verifier's source commit; `gunzip -c bin/verifier-linux-amd64.gz | sha256sum`
must match it.
