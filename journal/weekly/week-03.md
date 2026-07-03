# Week 3, 2026-06-29 to 2026-07-03

### Objective for the week

Begin invariant testing expansion: extend the handler and invariant suite beyond the Week 2
redemption cluster to the deposit/entrance-fee path and cross-component consistency, introduce an
adversarial actor, and investigate precision/rounding in the valuation path. (Week 3 runs June
29-July 3; retrospective written Friday July 3 as Day 24.)

### What I did

* Handler expansion (Day 20): extended the existing redeem-queue handler with deposit, mint, and
  entrance-fee-settlement actions, and wired a cross-component invariant that pending redemption
  shares never exceed total share supply. Refreshing the asset rate and last share value before
  the deposit action was needed so the action reaches fee and mint logic instead of stopping at
  validation reverts.
* Adversarial actor (Day 21): added an unprivileged caller with zero shares that attempts a
  redemption request, deliberately left unguarded in the handler so the protocol's own access
  control is what gets tested. Ran the extended suite and classified it as the Week 3 adversarial
  baseline: no violations, ghost state uncorrupted.
* Precision/rounding analysis (Days 22-23): studied the redeem-execution conversion chain, the
  shares-to-value helper, the asset-amount conversion, and the exit-fee split that runs before
  them. Established that every floor on the value-out path rounds toward the vault, that the
  net/fee share split is exact, and that the combined distribution never exceeds valuing the
  gross shares once. Identified the sub-threshold zero-exit-fee dust case as a gas-bounded
  fee-avoidance pattern, not a finding.
* Consolidation (Day 24): built a per-property coverage table splitting the seven precision
  properties studied into three test-pinned and two reasoned-only, and queued the two gaps as the
  first Week 4 task. Re-verified both baseline suites.

### Metrics summary

| Metric | Total |
|---|---|
| Research minutes | ~420 |
| Learning minutes | 0 |
| Community minutes | 0 |
| Contracts read (new) | 0 (re-reads and precision analysis of already-mapped surface) |
| Tests written | 3 (exit-fee split fuzz, zero-fee boundary, shares-to-value never-rounds-up fuzz) plus handler/adversarial/cross-component invariant additions |
| Invariants defined | 1 new cross-component (pending shares <= total supply); suite now 7 |
| Hypotheses investigated | 1 (fee-floor / value-floor compounding leak) |
| Hypotheses discarded | 1 (no impact: share split exact, combined value <= gross) |
| PoCs reproducible | 0 |
| Public contributions | 0 |

### What worked

* Deferring the precision work to a dedicated two-day block (Days 22-23) after the handler and
  adversarial expansion (Days 20-21) kept the two kinds of work from interfering: the suite was
  stable and green before any rounding analysis started, so a rounding property could be added
  and its effect on the baseline read cleanly.
* Testing the adversarial actor by leaving it unguarded in the handler (Day 21) is the correct
  design: guarding `if (balance == 0) return` would have skipped the test instead of exercising
  the protocol's access control. This is now the rule for every future adversarial handler.
* Analysing precision on pure conversion functions directly, with fuzzed inputs and no protocol
  state (Day 22), ran far more cases per second than a stateful invariant and isolated the
  rounding property from everything else.
* Closing the week with a per-property coverage table (Day 24) rather than a prose "no leak
  found" made the two remaining reasoned-only properties explicit and turned them into concrete
  Week 4 tasks instead of vague comfort.

### What didn't work

* The committed round-trip coverage is narrower than the Day 22 reasoning. The argument was about
  the full value-to-asset-to-value round-trip, but the committed test only pins the single
  shares-to-value direction. The gap was caught during the Day 24 consolidation, not when the
  test was written, so it survived three days as an unnoticed hole between reasoning and coverage.
* The asset-amount conversion's rounding direction is still asserted only by value-based unit
  tests, not a fuzz property. Minor, and now queued, but it means one link in the value-out chain
  is assumed rather than tested.
* No community contributions this week; the focus was entirely on the invariant expansion.

### AI workflow notes

* Useful AI interactions: extending the handler with the new actions and the adversarial caller;
  writing the precision fuzz tests and the boundary test from the source formulas; building the
  per-property coverage table by cross-referencing journal entries against committed test names;
  drafting all journal entries and this retrospective.
* AI outputs rejected and why: none this week.
* AI errors detected: none this week (the Foundry fuzz-vs-invariant env-var confusion from Week 2
  did not recur; the distinction was applied correctly from Day 20 onward).

### Public learning to share

At the end of a precision/rounding study block, the deliverable that matters is a per-property
table separating what is pinned by a committed test from what still rests on an argument. "We
found no leak" is not durable, a refactor can break a reasoned-only assumption with no test going
red. And a committed test can be narrower than the reasoning that motivated it: a round-trip
argument is easy to make on paper, but if the test pins only one direction, the round-trip is
still uncovered. Write the test for the property the user actually experiences.

### Blockers

None.

### Plan for next week

* Week 4 objective: continue invariant expansion into the fee-recipient value-owed accounting
  that the exit fee feeds into.
* First task, close the two Week 3 coverage gaps: a rounding-direction fuzz property for the
  asset-amount conversion, and a composed round-trip (value to asset to value) no-leak fuzz test.
  Both are cheap pure-function tests.
* Then model the fee-recipient value-owed accounting as invariants: does the sum of recipient
  claims ever exceed total fees accrued, can a recipient be owed or claim more than its share,
  and how does this interact with the mid-flight recipient-change edge case from Week 2.
* If any of the above surfaces a hypothesis: open it in the private workspace and trace it
  manually before logging.
* No adjustments to [ROADMAP.md](../../ROADMAP.md) required; Week 3 objectives met (handler
  expanded, adversarial actor added, cross-component invariant wired, precision analysis
  complete, suite at 7 passing invariants).
