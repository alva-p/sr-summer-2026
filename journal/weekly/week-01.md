# Week 1, 2026-06-15 to 2026-06-19

### Objective for the week

Technical onboarding of the primary target: full in-scope component inventory, scope
re-validation, architecture map with data-flow and trust-boundary sections, and confirmation
of the initial cluster for Week 2. (Week 1 runs June 15-19; retrospective written Thursday
June 18 with one day of slack before Week 2.)

### What I did

* Architecture / reading: read all 7 remaining in-scope source files not yet covered in the
  initial audit sessions (transfer-validator cluster: `[redacted]`,
  `[redacted]`, `[redacted]`, `[redacted]`; utility/infra: `Global`,
  `[redacted]`, `[redacted]`, `[redacted]`). All 24 in-scope contracts
  are now represented in the architecture map.
* AI workflow infrastructure: built the `solodit-vault` external findings corpus from scratch
  (266 methodology checks and 269 EVM findings across 15 sectors) and wired two integration
  points into the `alva-audit` agent (pre-audit context injection and raw-finding intake).
* Architecture map extensions: added the Shares transfer/compliance-list check data-flow path
  and three new trust-boundary rows (`[redacted]` / compliance lists,
  `Global.owner` as [redacted] root-of-trust, `[redacted].SHARES` immutable binding).
* Scope re-validation: confirmed scope page shows the same 25 items as the June 11 snapshot
  (24 contracts + 1 Primacy of Impact policy entry). No changes. Re-validation log added to
  `scope-lock.md`.
* Course completion: finished the Cyfrin Updraft Smart Contract Security Auditor course.
* Manual review / tests / fuzzing: none this week; all work was onboarding, documentation, and
  AI workflow infrastructure.
* Hypotheses opened: 0.
* Hypotheses closed: 0 (the one bypass path traced on Day 6 was already ruled out on Day 2;
  no new discard, just a re-confirmation).
* PoCs: none.
* Reports: two triage responses received during the week. Both closed: one on Day 4's submission
  (reason: out of scope or duplicate per earlier triage), one on Day 10 (reason: intentional
  design distinction between manual and automation close paths in a perpetuals protocol; the
  spread in the manual path is a trader execution cost, not a vault solvency gap). Two discarded
  hypotheses logged.

### Metrics summary

| Metric | Total |
|---|---|
| Research minutes | 120 |
| Learning minutes | 360 |
| Community minutes | 30 |
| Contracts read | 7 |
| Tests written | 0 |
| Invariants defined | 0 |
| Hypotheses investigated | 0 |
| Hypotheses discarded | 2 |
| PoCs reproducible | 0 |
| Public contributions | 4 |

### What worked

* Building the `solodit-vault` during the onboarding week was the right call: the corpus is
  now available for every session starting in Week 2, and the vault/lending sectors (the primary
  and secondary target types) have the deepest coverage. One-time infrastructure investment with
  immediate payoff.
* Doing the scope re-validation at the *end* of the onboarding week (Day 8) rather than only
  at the start caught any additions that might have appeared during the research window, at the
  cost of a 5-minute check.
* The full 24-contract component inventory being in place before the Week 1 architecture-map
  extension passes meant the data-flow and trust-boundary additions had a stable base to
  reference rather than needing to re-read files already covered.
* Finishing the Cyfrin course this week draws a clean line: Week 2 starts as active research
  with no pending curriculum obligations.

### What didn't work

* Day 7 was a full pivot away from the planned onboarding work (scope lock open items +
  architecture-map extensions), which pushed those tasks to Day 8. The pivot was the right
  call given the solodit-vault's long-term value, but it meant the Week 1 onboarding plan
  had to be compressed into Day 8 and partially Day 9.
* Zero new hypotheses this week. That is expected for an onboarding/mapping week, but Week 2
  needs to shift the ratio back toward active investigation.

### AI workflow notes

* Useful AI interactions this week: reading and normalizing Solodit/Rekt findings into the vault
  format; drafting architecture-map table entries and trust-boundary rows from source files;
  tracing call paths (transfer/mint/burn); cross-referencing findings against existing notes;
  re-fetching and parsing the Immunefi scope page; drafting the retrospective and the milestone
  tweet.
* AI outputs rejected and why: none this week.
* AI errors detected: none this week.

### Public learning to share

Building a generalized sector-level findings corpus (checks + concrete examples, separated into
two levels) before the deep-dive week makes the audit agent's pre-audit context injection
immediately useful rather than theoretical. The key design decision is keeping findings and
checks in separate files: findings answer "what does this look like in practice?" while checks
answer "what should I always verify for this sector?" Mixing them into one format loses the
distinction.

### Blockers

None.

### Plan for next week

* Week 2 objective (per campaign roadmap): understand Shares, Valuation and Fees in depth;
  define at least five invariants for the initial cluster.
* Starting point: architecture map and trust-boundary notes already complete for the full
  24-contract scope; initial cluster (Shares/Valuation/Fees) already confirmed on Day 8.
* Expected daily rhythm: read source files for the cluster in depth, trace accounting paths,
  draft invariant candidates, verify against tests.
* No adjustments to [ROADMAP.md](../../ROADMAP.md) required; Week 1 objectives fully met.
