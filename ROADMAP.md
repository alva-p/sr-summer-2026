# SR Summer 2026 Roadmap

Campaign window: **2026-06-09 to 2026-08-31** (Immunefi SR Summer 2026).
Project work window: **2026-06-10 to 2026-08-31**, ~2 hours/day, Monday-Friday (59 weekdays).
Weekends are optional: rest, light reading, or recovery.

Timezone: America/Argentina/Cordoba.

This roadmap is a living document. Targets, surfaces and the second-target choice are decisions made
along the way (see [methodology/bounty-selection.md](methodology/bounty-selection.md) and
[methodology/scope-lock-template.md](methodology/scope-lock-template.md)), not fixed in stone.

Specific program/protocol names are tracked privately and are not published here before a report is
submitted (see [SECURITY_AND_DISCLOSURE.md](SECURITY_AND_DISCLOSURE.md)). This roadmap describes the
process and goals in general terms.

## Initial week (June 10-12, 2026)

**Goal:** build the working system.

* **Wed June 10**: Record completed setup (banner, commitment, repo, profiles). Create initial repo
  structure. Define goals, specialization and metrics. Prepare public/private separation. Draft
  preliminary target list. Write Day 1.
* **Thu June 11**: Complete the bounty-selection matrix. Re-validate the candidate programs against
  current Immunefi program pages. Document selection criteria. Create the scope-lock template.
  Prepare the local private workspace.
* **Fri June 12**: Officially select primary and secondary targets. Clone the primary target into the
  private workspace. Record commit, dependencies and versions. Run build and tests. Write the initial
  week retrospective.

## Week 1 (June 15-19)

**Goal:** technical onboarding of the primary target.

* Read documentation and prior audits.
* Complete scope lock.
* Identify assets, actors, roles and dependencies.
* Enumerate in-scope contracts.
* Build an architecture map.
* Record trust boundaries.
* Choose a small initial cluster.
* Publish a sanitized retrospective.

**Public deliverable:** onboarding methodology + weekly summary with no sensitive target details.

## Week 2 (June 22-26)

**Goal:** understand Shares, Valuation and Fees.

* Trace deposits, minting, burning and redemption.
* Study how value is calculated.
* Identify units, scales and rounding.
* Trace fee accrual and collection.
* Define at least five invariants.
* Map each invariant to functions and state.
* Write the first local tests.

## Week 3 (June 29 - July 3)

**Goal:** start invariant testing.

* Prepare handlers and actors.
* Define valid preconditions.
* Implement basic invariants.
* Run fuzzing.
* Triage failures: test bug / wrong assumption / documented behavior / potential hypothesis.
* Document false positives and learnings.

## Week 4 (July 6-10)

**Goal:** study redemption, queues and temporal state.

* Map request, cancel, claim and settlement flows.
* Look for duplicated claims.
* Analyze partial states.
* Evaluate pauses and locks.
* Study precision and rounding.
* Build state-machine tests.
* Write a public learning piece on queue testing, using educational examples.

## Week 5 (July 13-17)

**Goal:** debt accounting and integrations.

* Study debt creation, modification and repayment.
* Review signs, scales and conversions.
* Analyze external dependencies.
* Review non-standard tokens where relevant.
* Investigate adversarial scenarios.
* Validate or discard hypotheses.
* Update AI-workflow metrics.

## Week 6 (July 20-24)

**Goal:** first quality checkpoint.

* Review all existing hypotheses.
* Remove duplicates and out-of-scope cases.
* Reproduce tests from a clean environment.
* Apply the [PoC quality gate](methodology/poc-quality-gate.md).
* Apply the [report quality gate](methodology/report-quality-gate.md).
* Use Immunefi Studio when there's a suitable candidate.
* Submit only reports with sufficient evidence; never force a submission to hit a metric.
* If no valid finding exists: document learnings, identify missing coverage, continue or pivot with
  a documented reason.

## Week 7 (July 27-31)

**Goal:** close out the opportunistic target picked up at the end of Week 6 and formally decide the
second target.

* Finish the ledger/core (blockchain/DLT) component review deferred from the end of Week 6.
* Resolve the blocked PoC (confirm/pin a working dependency version for the affected test harness)
  and execute the deferred hypothesis.
* Run the surviving candidates through the [PoC quality gate](methodology/poc-quality-gate.md) and
  [report quality gate](methodology/report-quality-gate.md); submit only what clears the bar, write
  up the rest as documented hardening notes if they don't.
* Decide formally: this opportunistic target becomes the second target for Weeks 8-9, and the
  lending/credit-delegation surface started at Day 42-43 is **parked, not abandoned**, at its Day 43
  state (architecture map + first invariant already committed).
* Technical retrospective comparing the two onboarding experiences (EVM/lending-style vs.
  DAG-ledger + autonomous-agent-style) as input for Week 8 planning.
* Update the AI-assisted workflow notes.

## Week 8 (August 3-7)

**Goal:** depth on the second target — contingent on what Week 7 leaves open.

If the opportunistic target still has open, promising surface after Week 7 (e.g. asset/component
areas flagged but deprioritized under time budget):

* Pick the next-highest-signal surface within it.
* Build its architecture map and a scope lock for it.
* Record external assumptions and trust boundaries.
* Define initial invariants.

If the opportunistic target is exhausted (Week 7 submission, if any, was the ceiling):

* Resume the parked lending/credit-delegation surface from its Day 43 state.
* Understand the credit delegation model.
* Map external lending integrations and intermediate vaults.
* Identify collateral, debt and liquidations.
* Build the architecture map.
* Complete a new scope lock.
* Record external assumptions.
* Define initial invariants.

## Week 9 (August 10-14)

**Goal:** tests for whichever surface Week 8 continued.

* Review deposits and withdrawals (or the equivalent value-in/value-out flow for a non-EVM target).
* Analyze solvency.
* Study liquidations (where applicable).
* Review oracles or equivalent external-price/rate dependencies.
* Analyze credit or exposure limits.
* Implement unit tests, fuzzing or invariants.
* Compare this process with the first target.

## Week 10 (August 17-21)

**Goal:** validate results and contribute to the community.

* Investigate the highest-signal hypotheses.
* Build PoCs where appropriate.
* Discard cases with no impact.
* Review scope and severity.
* Prepare a public article on methodology.
* Publish a mature version of the AI-assisted workflow.
* Show sanitized, educational examples.

## Week 11 (August 24-28)

**Goal:** finish strong.

* Finish pending tests and reports.
* Run quality gates.
* Clean up and improve the public repo.
* Update README, dashboard and portfolio.
* Prepare sanitized case studies.
* Summarize metrics.
* Document community contributions.
* Prepare the final retrospective.
* Identify teams, firms or protocols to connect with professionally.

## Closing (August 31)

**Goal:** publish the final SR Summer result.

Produce:

* Full campaign summary.
* Final metrics.
* Skills developed.
* Target areas studied.
* Tools and tests built.
* Invariants developed.
* Hypotheses discarded.
* Reports submitted/valid/paid (without revealing prohibited information).
* Community contributions.
* AI-workflow evaluation.
* Errors and limitations.
* Next 90-day plan.
* Final portfolio.
* Draft posts for X and LinkedIn.

## Stretch goal

If reached, do **not** analyze an entire large protocol at once. Pick one small, concrete surface,
e.g.: cross-chain token pools, rate limiters, receiver contracts, oracle/price feed integrations,
automation registries, or adapters.

## Important note on targets

The current candidates (primary, secondary, stretch and alternatives) are **initial candidates, not
permanent scopes**, and are tracked privately, not in this file. Before starting research on any
program, re-check on Immunefi: active status, assets in scope, impacts in scope, PoC requirements,
known issues, prior audits, exclusions, latest version/commit, primacy of impact vs. rules,
disclosure policy, and operational restrictions. See
[methodology/program-evaluation-template.md](methodology/program-evaluation-template.md).
