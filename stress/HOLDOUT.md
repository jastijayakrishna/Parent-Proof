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
