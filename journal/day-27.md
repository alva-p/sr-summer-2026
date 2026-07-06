# Day 27, 2026-07-06 (Monday)

* **Campaign day:** 27 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 4 (July 6-10) — redemption, queues and temporal state

## Objective

Start Week 4 by modelling the fee-recipient value-owed accounting the exit fee feeds into as
invariants, closing the three gaps flagged as the Day 26 next step: recipient claims never exceed
what is owed, no value is created or destroyed across the lifecycle, and a mid-flight change of the
exit fee recipient preserves value already owed to the previous recipient rather than stranding or
duplicating it.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

Fee accounting over its full lifecycle: accrual on the deposit and execute paths, the claim path
that decreases owed value, and rotation of the fee recipient while value is outstanding. Until today
the fee invariants had only ever been exercised under increases; the decrease path and the
recipient-change edge case were reasoned about but never fuzzed.

## Activities

* Added a claim action to the invariant handler: it picks a tracked recipient, bounds the claimed
  value to what is actually owed, refreshes the rate and funds the vault so the fee-asset conversion
  and withdrawal can succeed, and records the claimed value on success. This exercises the
  owed-decrease path that every prior fuzz call had left untouched.
* Added a recipient-rotation action: the admin rotates the exit fee recipient among a small
  candidate set that includes an overlapping existing recipient, a fresh address, and the
  zero-address fee-burn branch, keeping the fee rate non-zero so accrual continues across the
  change.
* Instrumented the two accrual paths (deposit for the entrance fee, execute for the exit fee) to
  track cumulative accrued value as the total-owed delta across each call. Both paths only ever
  increase total owed, so the delta is pure accrual with no risk of underflow.
* Added INV-FEE-03, a full-lifecycle conservation invariant: cumulative accrued equals current total
  owed plus cumulative claimed. Neither claiming nor rotating the recipient may create or destroy fee
  value.
* Set the fee asset in the invariant setup so the claim path resolves and can pay out.
* Wired the claim value, when the conversion rounds a tiny value to zero, through the protocol's own
  zero-fee-asset guard: the revert is caught, nothing is claimed, and owed value is unchanged, so it
  is not treated as a violation.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* Extended the redeem-queue invariant suite from seven to eight invariants (added INV-FEE-03) and
  from seven to nine handler actions (added claim and recipient rotation).
* Full suite green: 8 invariants pass at the default 256 runs / depth 500, 128,000 calls each, zero
  reverts across all handler actions including the two new ones (claim exercised ~14.1k times,
  recipient rotation ~14.3k times).
* Confirmed the new conservation invariant is non-vacuous: accrual, claim and rotation actions all
  fire in volume, so cumulative accrued and cumulative claimed both move independently of current
  owed.

## Hypotheses generated

* None. The fee accounting held under the decrease path and under mid-flight recipient rotation,
  confirming that `[redacted]` only repoints the recipient and never touches value already owed, and
  that claim and accrual keep total owed exactly reconciled with per-recipient owed.

## Hypotheses discarded

* The mid-flight recipient-change concern from Week 2 (that rotating the exit fee recipient could
  strand or duplicate outstanding owed value) is discarded as documented behaviour: the sum-equals-
  total invariant holds across every rotation, so owed value is preserved intact.

## AI usage

* Drafted the two new handler actions and the conservation invariant matching the existing suite
  style, and drafted this entry.
* Cross-checked that the two accrual paths only increase total owed, so the delta-based accrual ghost
  cannot underflow and captures every unit of accrued value.

## Human verification

* Traced the claim path by hand: the protocol decreases per-recipient and total owed by the same
  delta and guards over-claim by underflow revert, so bounding the claimed value to owed can never
  drive either below zero.
* Verified the rotation path leaves prior owed untouched: `[redacted]` overwrites only the recipient
  pointer, so the sum-equals-total invariant is what would catch any loss or duplication.
* Confirmed each new assertion bites: an asymmetric decrease, or a rotation that moved owed value,
  would break INV-FEE-02 or INV-FEE-03, so the green result is meaningful and not vacuous.
* Ran `make safety-check` and read the output before marking the entry ready.

## Milestone

* A medium-severity report submitted earlier in the campaign was triaged and accepted on a bug
  bounty platform other than Immunefi. First accepted finding of the summer; recorded here as a
  campaign milestone with no target or finding specifics.

## Public learnings

* Fee accounting is easy to test only on the way up. The accrual paths get exercised by every
  deposit and redemption, but the claim path that decreases owed value, and the admin action that
  rotates the recipient while value is outstanding, are exactly the transitions where an asymmetric
  update would hide. Pinning a single conservation property — accrued equals owed plus claimed —
  turns the whole lifecycle into one assertion that fires on any leak.
* When a rotation edge case has an obvious "value must be preserved" story, the cheapest proof is
  the existing sum-equals-total invariant plus a handler action that actually performs the rotation
  under fuzzing, rather than a fresh bespoke check.

## Blockers

* None.

## Next step

Continue Week 4 on the redemption queue's temporal state: model the cancel-window and settlement
timing as invariants (a request cannot be cancelled before its minimum duration nor executed in a
way that races the cancel window), and check for any partial-settlement or duplicate-claim state the
current single-id execution path does not yet exercise.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes generic fee-lifecycle
      invariant testing and records an accepted-report milestone with no target or finding details.
