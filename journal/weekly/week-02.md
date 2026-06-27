# Week 2, 2026-06-22 to 2026-06-26

### Objective for the week

Understand Shares, Valuation and Fees in depth; define at least five invariants for the initial
cluster and write the first local tests. (Week 2 runs June 22-26; retrospective written Friday
June 26 as Day 17.)

### What I did

* Architecture / reading: read `Shares.sol` and `[redacted].sol` in full on the
  optional Sunday bridge session (Day 12), focusing on mint/burn formulas, total supply
  tracking, and the request/cancel/claim state machine. All contract source readings done in
  the Week 2 session were re-reads for invariant and adversarial analysis, not new contracts.
* Invariants: formalized eight invariant candidates as structured stubs (Day 12), then selected
  the five strongest and wrote formal definitions with function and state mappings (Day 13).
  Added a sixth precise sum invariant (INV-FEE-02) on Day 15. Total: 6 invariants defined this
  week.
* Test suite: implemented eight Foundry test skeletons (Day 13); implemented [redacted]
  and [redacted].t.sol with all five invariants fully wired and passing (Day 14);
  extended the handler with pre-registered fee recipients and a ghost sum view, added INV-FEE-02,
  and wrote [redacted].t.sol with 9 state transition unit tests (Day 15). Added
  [redacted].t.sol with 3 targeted tests for the mid-flight recipient change scenario
  (Day 16). Total: 26 tests written this week.
* Invariant fuzzing: ran the full 6-invariant suite at 256 runs (Day 14) and then at 2,000 runs
  (Day 15); 0 violations, 0 reverts, 0 discards.
* Adversarial analysis: mapped adversarial scenarios against all six formalized invariants,
  identifying which assumptions each invariant relies on and whether those assumptions are
  reachable from an unprivileged caller (Day 16).
* Hypotheses opened: 0.
* Hypotheses closed: 2 discarded (H-ORDERING: wrong assumption; H-QUEUE02-BYPASS: impossible
  path from documented behavior).
* PoCs: 0 with exploitable signal. The [redacted] tests confirmed a documented
  behavioral edge case, not a vulnerability.
* Reports: 1 High severity triage confirmation received on Day 13 (external platform, separate
  from this primary target). No new submissions on the primary target this week.

### Metrics summary

| Metric | Total |
|---|---|
| Research minutes | 690 |
| Learning minutes | 0 |
| Community minutes | 30 |
| Contracts read (new) | 2 |
| Tests written | 26 |
| Invariants defined | 6 |
| Hypotheses investigated | 2 |
| Hypotheses discarded | 2 |
| PoCs reproducible | 0 |
| Public contributions | 1 |

### What worked

* Prose-level invariant stubs as an intermediate artifact (Day 12) made the Day 13 formalization
  session significantly faster: the properties were already clear, only the format needed
  standardization. One optional Sunday session turned into a forcing function for the entire
  week's test structure.
* Pre-registering all fee recipients in the handler constructor (Day 15) made INV-FEE-02
  non-trivial from the first fuzzer call, avoiding the common pitfall of a vacuously-true fee
  invariant when fees are configured only after the first relevant action.
* The three-test pattern for mid-flight config changes (baseline, mutated, symmetry) identified
  the right question clearly: not "does changing the config produce a different outcome?" but
  "does changing the destination of value affect the user's net payout?" The symmetry test
  answers the latter directly.
* The adversarial mapping framework (invariant, assumption needed to break it, access-control
  check, verdict) gave a structured way to draw the line between "robust against unprivileged
  callers" and "relies on admin trust." This is the output the Week 3 expansion should be
  measured against.

### What didn't work

* The `FOUNDRY_FUZZ_RUNS` vs. `FOUNDRY_INVARIANT_RUNS` distinction was missed on Day 14 and
  caught only on Day 15. The first heavy run was actually at the default invariant depth. No
  correctness impact, but the timing was off.
* No new hypotheses with exploitable signal this week. The invariant suite passing consistently
  and the adversarial analysis producing only "admin-level" trust surfaces is a correct result
  given the access-control model, not a sign of missing coverage. However, Week 3 should
  expand the attack surface to the deposit/entrance-fee path and cross-component interactions
  to confirm coverage is genuinely complete rather than narrow.

### AI workflow notes

* Useful AI interactions: writing both Foundry test files (handler, invariant suite, state
  machine tests, mid-flight tests) from source-derived specifications; structuring invariant
  definitions into consistent format; proposing the adversarial mapping framework; drafting all
  journal entries.
* AI outputs rejected and why: none this week.
* AI errors detected: one (FOUNDRY_FUZZ_RUNS vs. FOUNDRY_INVARIANT_RUNS on Day 15 initial
  run suggestion; caught during local verification before recording results).

### Public learning to share

For each formalized invariant, the useful adversarial question is: "what would a caller need
to be able to do to break this?" The answer either points to a concrete attack surface worth
investigating or confirms the invariant is robust for unprivileged callers. Invariants that
can only be broken by admin-level access are not findings, but they do mark a trust surface
worth noting in the report context. Mapping this explicitly for every invariant, as a table,
is faster than case-by-case analysis and produces a structured coverage artifact.

### Blockers

None.

### Plan for next week

* Week 3 objective (per campaign roadmap): start invariant testing expansion.
* Starting point: 6 passing invariants for the redemption queue and fee cluster; handler and
  actor infrastructure in place; adversarial analysis complete for the current invariant set.
* Planned expansion:
  * Extend the handler and invariant suite to the deposit/entrance-fee path; add invariants
    covering the mint side (shares issued vs. assets deposited, entrance fee accounting).
  * Add cross-component invariants covering state consistency between the share supply and
    the redemption queue (pending shares never exceed total supply).
  * Introduce an adversarial actor into the handler: a caller that attempts to cancel a
    non-cancelable request, re-execute a settled request, or request a redemption while
    holding no shares; confirm the handler guards hold and record whether any unconstrained
    fuzzer path causes an unexpected state.
  * Investigate precision and rounding in the valuation path: how does the share price change
    under minimal deposit sizes and maximum fee rates? Are there rounding directions that
    consistently favor or disfavor one party?
  * If any of the above surfaces a hypothesis: open it in the private workspace and trace it
    manually before logging.
* No adjustments to [ROADMAP.md](../../ROADMAP.md) required; Week 2 objectives met (6
  invariants defined vs. 5 minimum, 26 tests written vs. 0 at start of week).
