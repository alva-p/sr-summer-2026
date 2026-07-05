# Day 12, 2026-06-21 (Sunday)

* **Campaign day:** 12 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Bridge day before Week 2 (June 22-26)

## Objective

Optional Sunday session. Goal: read the shares token contract and the async redeem-queue contract in full with
the same formula/invariant focus applied on Day 11 to the valuation handler and the fee handler, and
formalize the eight invariant candidates from private notes into structured stubs ready to be
implemented as Foundry tests on Monday.

## Time

* **Planned:** ~1.5h
* **Actual:** ~1.5h

## Area studied

the shares token contract and the async redeem-queue contract source code; invariant candidate formalization.

## Activities

* Read the shares token contract in full with focus on the mint and burn formulas, total supply tracking, and
  the relationship between share amounts and underlying asset amounts.
* Read the async redeem-queue contract in full with focus on the request/cancel/claim state machine,
  how pending redemptions are accounted, and what invariants govern the queue at each state
  transition.
* Formalized the eight invariant candidates from private notes into structured stubs: each stub
  names the invariant, states the precondition, and describes the property that must hold after
  any state-changing operation.
* Stored the formalized stubs in the private workspace, ready to implement as Foundry tests on
  Monday.

## Tests / experiments

* None written today. Stubs are structured prose/pseudocode, not runnable code yet.

## Hypotheses generated

* None new. Stub formalization confirmed the eight candidates identified on Day 11 and did not
  surface additional signals warranting separate hypothesis entries.

## Hypotheses discarded

* None.

## AI usage

* Helped organize and structure the eight invariant stubs into a consistent format (name,
  precondition, property).
* Drafted this journal entry.

## Human verification

* All formulas and state transitions referenced in the stubs were verified directly against the
  source code before being recorded.
* No stub was accepted based solely on the AI's description; every claim was traced back to a
  specific function or storage variable in the contracts.

## Public learnings

* Reading two contracts back-to-back with the same invariant-focused lens (rather than general
  comprehension) produces structured candidates directly, without a separate analysis pass.
* Prose-level invariant stubs are faster to write than Foundry test code and serve as a useful
  intermediate artifact: they can be reviewed, discarded or refined before spending time on
  implementation.
* An optional Sunday session is most effective when it has a single, concrete deliverable
  (formalized stubs) rather than an open-ended exploration goal.

## Blockers

* None.

## Next step

Week 2 starts Monday June 22. Objective: understand Shares, Valuation and Fees in depth.
Monday cadence: planning, scope, architecture, documentation. Specific actions:
* Implement Foundry test stubs for the formalized invariants.
* Trace the full deposit and mint flow end-to-end.
* Define at least five invariants with function and state mappings per the Week 2 roadmap goal.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).
