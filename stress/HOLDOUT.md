# Hold-out run

Recorded before the run (stress/PREREG.md). Fixes froze with this binary after its dev and regression reruns; the
hold-out runs once on it and is not rerun.

source: jastijayakrishna/Parent, branch main, commit ee76650f0b0c72dda852a20b7fb882d299a51e4b
sha256 (uncompressed linux/amd64): 1f24e8c7682e1b85bc9e705feeb6e80dd6a54883c78a71977c6989391cd9cd68
built: 2026-10-06T09:31Z

Correction after the run, 2026-10-06: the Go judge did not build an upgrade made by a replace line (gaia pins
cosmos-sdk so), so 25 of gaia's 32 windows compiled without the new version. The judge was fixed (Parent 13510aa) and
every Go history window, dev and hold-out, judged again with a binary that differs from this one only in the judge;
the verifier's answers are compared window by window with this run's. Both results are reported.

## Result

Missed breaks (Merge where the compiler fails): 0 in Go and 0 in Java, before and after the judge correction. The
verifier's answers in the re-judged run equal this binary's on all 218 Go history windows.

- Go, as run: 254 windows, 20 broke the build, 12 caught, 5 false alarms. Re-judged: 22 broke, 12 caught, the other 10
  Needs review, 4 false alarms.
- Java: 491 windows, 27 judged (Alluxio), 2 broke, 2 caught, 1 false alarm. Beam and Bigtable: judge not verified
  (the canary did not break cleanly). Bazel (174): no build to read; no window said Merge.
- False alarms: gaia v0.53.4->v0.53.8 and v0.50.11->v0.53.0 cite only packages the judge left out of its build; Tempo
  v1.5.0->v1.6.0 and v1.7.1->v1.9.0 cite vendored pdata, whose own generated copy of OTLP does not change with the OTLP
  module (the verifier counts it as the provider's); Alluxio dbac084c moved BuildVersion to another .proto package
  while its Java class, alluxio.grpc.BuildVersion, stayed the same (the verifier compares .proto names, not Java names).
