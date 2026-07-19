# Day 40, 2026-07-23 (Thursday)

* **Campaign day:** 40 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 6 (July 20-24) — first quality checkpoint

## Objective

Reproduce the pinned audit-test artifact from a clean copy to confirm it is portable, then close the
Week 6 quality checkpoint.

## Time

* **Planned:** ~1h30m
* **Actual:** ~1h30m

## Area studied

Reproducibility and artifact provenance: turning a green local suite into one that runs from a clean
checkout.

## Activities

* Pinned the private test artifact with its exact test diff and toolchain version alongside the command.
* Cloned the workspace into a fresh directory and ran the invariant suite there from scratch.
* Confirmed the suite passes on the clean copy with no manual fix-ups.
* Recorded the reproduction command and environment in the private workspace so the evidence stands alone.
* Marked the Week 6 quality checkpoint closed.

## Tests / experiments

* Local invariant suite reproduced and passed on a clean checkout. No new test was added.

## Hypotheses generated

* None.

## Hypotheses discarded

* None.

## AI usage

* Used AI to diff the pinned artifact against the working tree and check nothing outside the recorded set
  was needed to reproduce it.

## Human verification

* Ran the suite on the clean copy myself and confirmed the result before closing the checkpoint.

## Public learnings

* Reproducibility is a separate deliverable from a passing test: pin the diff, the toolchain, and the
  command, not just the output.
* A clean-checkout run is the cheapest proof that evidence is portable and the most-skipped one.

## Blockers

* None. The Week 6 checkpoint is closed.

## Next step

Start Week 7 by picking the next surface to review from the private target queue and defining its first
invariant.

## Confidentiality check

- [x] This entry contains only sanitized process, aggregate test status, and general learning. All target,
      coverage, source, hypothesis, and artifact details remain in the private workspace.
