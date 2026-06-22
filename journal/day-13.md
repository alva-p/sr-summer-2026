# Day 13, 2026-06-22 (Monday)

* **Campaign day:** 13 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 2 (June 22-26) — Shares, Valuation and Fees

## Objective

Week 2 kickoff. Monday cadence: planning, scope, architecture, documentation.
Goals for today:
* Trace the full deposit and mint flow end-to-end across the cluster contracts.
* Implement the eight invariant stubs from Day 12 as Foundry test skeletons (compilable,
  preconditions set, assertion placeholder in place).
* Formally define at least five invariants with function and state mappings per the Week 2
  roadmap goal.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

Deposit and mint flow (end-to-end trace); invariant formalization and Foundry test skeleton
implementation; external bug bounty activity.

## Activities

* Traced the full deposit and mint flow end-to-end across the cluster: entry point through share
  minting, valuation update, and fee state side effects. Mapped which functions mutate which
  storage variables and in what order.
* Implemented the eight invariant stubs from Day 12 as Foundry test skeletons: each test
  compiles, has setup scaffolding, precondition calls in place, and an assertion placeholder
  marking where the property check will go.
* Selected the five strongest stubs and wrote formal invariant definitions for each: invariant
  name, the property that must hold, the function(s) that can violate it, and the storage
  variables involved.
* Received a High severity triage confirmation on an external bug bounty platform (separate from
  Immunefi). No technical details recorded here per confidentiality policy.

## Tests / experiments

* Eight Foundry test skeletons implemented and confirmed compilable. No fuzzing runs yet —
  handlers and actors are not wired, only the skeleton structure is in place.

## Hypotheses generated

* None new. The flow trace confirmed the expected behavior and produced no unexpected branches
  worth logging as a hypothesis at this stage.

## Hypotheses discarded

* None.

## AI usage

* Helped structure the five formal invariant definitions into a consistent format.
* Drafted this journal entry.

## Human verification

* All flow mappings were verified by reading function bodies and storage layouts directly in
  source code, not inferred from docs alone.
* Each Foundry test skeleton was compiled locally to confirm there are no syntax errors before
  recording as done.

## Public learnings

* Writing a Foundry test skeleton before the implementation forces you to think about the
  preconditions explicitly. If you cannot write a realistic setup, the invariant is probably
  under-specified.
* A formal invariant definition (name, property, functions that can violate it, storage
  variables) takes about ten minutes per invariant and saves significant time when debugging
  fuzzer counterexamples later.
* External triage confirmations are a signal to keep the current methodology going, not an
  excuse to skip the structured work.

## Blockers

* None.

## Next step

Tuesday cadence: manual review, critical flows, entry points. Specific actions:
* Trace the redeem and withdrawal flow end-to-end with the same mapping approach used today
  for deposits.
* Begin wiring handlers and actors for the five formalized invariants.
* Review the fee accrual path to verify the fee invariants are correctly scoped.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).
