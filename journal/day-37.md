# Day 37, 2026-07-20 (Monday)

* **Campaign day:** 37 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 6 (July 20-24) — first quality checkpoint

## Objective

Open Week 6, the first quality checkpoint. Inventory every hypothesis opened across Weeks 1 to 5 from
the private workspace, remove duplicates and out-of-scope entries, and triage each survivor against the
[PoC quality gate](../methodology/poc-quality-gate.md) to decide which, if any, is worth reproducing.
Reproduce the committed invariant suite from a clean checkout to confirm the recorded results still
hold outside the working tree. Fold the Day 36 position-tracker value-timing thread into this review as
a hypothesis to judge, not new surface to hunt.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The accumulated hypothesis set and the committed test suite as artifacts, judged against the PoC and
report quality gates, rather than any new protocol surface. The focus was deduplication, scope
filtering, and clean-room reproduction.

## Activities

* Pulled the full hypothesis list from the private workspace across Weeks 1 to 5 and grouped the
  entries by the value path each one touches, so restatements of the same observation from different
  callers would sit next to each other rather than scattered across weekly notes.
* Deduplicated. Several Week 5 candidates are the same underlying observation seen from different
  entrypoints: the sign-dependent rounding, the expiry-only rate staleness, and the fee-subtraction
  distortion all reduce to "a derived value is biased or stale but consumed as an admin-pushed
  snapshot". Merged those into one closed cluster with a single shared reason instead of carrying four
  separate entries.
* Filtered for scope. The candidates that closed as trust assumptions (rate accuracy on a manual push,
  operator-scheduled sampling) sit outside the untrusted-actor model, so they were marked out of the
  active hypothesis set and kept only as documented scope facts, not as open surfaces.
* Triaged the survivors against the PoC quality gate. Every surviving candidate is a "no unprivileged
  driver" closure, so none clears the gate's realistic-preconditions and observable-in-scope-impact
  boxes: there is no attacker-reachable setup and no measurable in-scope impact to demonstrate. None
  warrants a PoC yet. Recorded that honestly rather than forcing a candidate through the gate to
  produce one.
* Reproduced the committed invariant suite from a clean checkout: fresh clone, the pinned Foundry
  version, the documented setup, then ran the full redeem-queue suite (12 invariants) at the default
  runs and depth. Green, matching the Day 32 recorded result. That satisfies the gate's
  runs-from-a-clean-checkout box for the suite itself, which is the box most likely to be silently
  false when a suite has only ever run in a dirty working tree.
* Judged the reasoning-versus-coverage gap per candidate. The Week 5 rounding-bias and
  staleness-asymmetry arguments live as prose in the private workspace, not as committed invariants.
  Because both closed as "no unprivileged driver", pinning them as adversarial invariants would assert
  a property no untrusted actor can violate, which is not what an invariant is for. Decided they belong
  as documented scope facts rather than running invariants, and recorded that decision so the gap is
  closed by a judgment rather than left open.
* Placed the Day 36 position-tracker value-timing thread into the same review and applied the
  trigger-ownership test that closed the Week 5 candidates: the timing gap between an unprivileged
  balance change and the operator's next snapshot only matters if an untrusted actor can consume the
  distorted snapshot atomically, and the consume path reads the stored snapshot, so the thread joins
  the closed cluster pending a second-pass check against the report quality gate.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* No new invariants or PoCs. Reproduced the existing 12-invariant redeem-queue suite from a clean
  clone at the default runs and depth; green, matching the recorded Day 32 state. This was a checkpoint
  and verification pass, so the deliverable is the triaged hypothesis list and the clean-room
  reproduction, not a new committed property. The suite on disk stays at 12.

## Hypotheses generated

* None new. A checkpoint consolidates the existing set rather than opening surface.

## Hypotheses discarded

* Merged and closed the Week 5 cluster (sign-dependent rounding in the linear write-down, expiry-only
  staleness on the manual conversion rate, and the fee-aggregate subtraction distortion) into one
  reviewed closure with the shared reason: admin-controlled inputs plus a stored-snapshot consume path
  with no atomic influence-then-consume chain, so none has an unprivileged driver. Removed the
  duplicates so the private tracker now holds one entry per distinct surface with its closure reason,
  rather than four framings of the same fact.

## AI usage

* Used AI to cross-index the hypothesis entries across the weekly private notes and flag which were
  restatements of the same underlying observation, and to drive the clean-checkout reproduction of the
  suite (fresh clone, pinned toolchain, run) so the result is a real clean-room run rather than a cached
  one.

## Human verification

* Re-read each merged hypothesis's original closure reason by hand before collapsing them, to confirm
  the merge does not hide a candidate with a distinct driver behind a shared summary.
* Verified the clean-checkout suite result myself, watching the run complete green on the fresh clone
  rather than trusting the working-tree run or a cached result, since the whole point of the box is that
  it reproduces outside my machine's state.

## Public learnings

* A quality checkpoint is where you find out how many of your "surfaces" are the same observation
  wearing different function names. Deduplicating first turns a long backlog into a short list of
  distinct facts, and the count of real open questions is usually smaller than the count of notes.
* Reproducing your own test suite from a clean clone is the cheapest box on the PoC quality gate and
  the one most likely to be silently false. A suite that only runs in your dirty working tree is not
  evidence; run it from a fresh checkout before you trust its result.
* A negative checkpoint, where no candidate clears the gate this week, is a real result. Forcing a PoC
  to hit a metric is how invalid reports get written. Recording "reviewed, no driver" for a cluster is
  a stronger deliverable than a PoC that would not survive a reviewer.

## Blockers

* None.

## Next step

Continue the Week 6 checkpoint. With the backlog deduplicated and the suite reproduced from a clean
checkout, walk the [report quality gate](../methodology/report-quality-gate.md) against the strongest
closed cluster to confirm the "no unprivileged driver" reasoning would survive an external reviewer,
and map the coverage gaps the checkpoint exposes: which value-path surfaces were closed by reasoning
alone and would need a committed artifact if revisited. If that second pass surfaces a realistic driver
on any survivor, open it as the Week 6 PoC candidate; otherwise document the coverage map and select
the Week 7 surface with a recorded reason.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes a generic quality-checkpoint
      pass that inventories, deduplicates and scope-filters an internal hypothesis list, triages the
      survivors against a PoC quality gate, and reproduces an existing invariant suite from a clean
      checkout, all in generic terms with no target name, contract identifier, or target-specific finding
      or exploit detail.
