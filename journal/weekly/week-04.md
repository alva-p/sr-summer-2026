# Week 4, 2026-07-06 to 2026-07-10

### Objective for the week

Study redemption, queues and temporal state: map the request / cancel / claim / settle flows, look
for duplicated claims and partial states, evaluate pause and lock behaviour, study precision and
rounding, and build state-machine tests. Close the week with a public learning piece on queue
testing using educational examples. (Week 4 runs July 6-10; retrospective written Friday July 10 as
Day 31.)

### What I did

* Fee-recipient value-owed accounting (Day 27): modelled the value-owed accounting the exit fee
  feeds into as invariants — recipient claims never exceed what is owed, no value is created or
  destroyed across the lifecycle (accrued equals owed plus claimed), and a mid-flight change of the
  exit-fee recipient preserves value already owed rather than stranding or duplicating it. Added a
  claim action (the decrease path that prior fuzzing never exercised) and a recipient-rotation
  action so the sum-equals-total property is tested under a real rotation, not a bespoke check.
* Temporal state (Day 28): modelled the queue's time-dependent guards as invariants — a request
  cannot be cancelled before its minimum duration elapses, and a request cannot be settled twice
  (no cancel-then-execute or execute-then-execute double-spend on the single-id path). Moved these
  from isolated deterministic transitions into fuzzer-callable adversarial actions so the guards are
  exercised interleaved with every other action across randomised sequences.
* Batch atomicity (Day 29): pushed execution to multi-id and modelled a batch mixing live,
  already-settled, and duplicate ids. Established the all-or-none property: a failing batch settles
  every id or none, leaving zero footprint (no shares burned, no supply moved) on the revert. Added
  a non-vacuity predicate splitting inputs into settle/revert branches with a counter on each so a
  passing invariant is also a covered one.
* Batch value-effect analysis (Day 30): reasoned through order-independence and rounding drift for
  the multi-id loop. Because execution reads the share price once per call and each id converts from
  its own full-precision amount with no remainder carried between iterations, the loop is a pure sum
  of independent terms: permuting the id array cannot change the totals and per-id rounding cannot
  compound with batch size. Also studied settling the same membership set against a share price that
  moved between request and execution, confirming the payout uses the execution-time rate. (See
  "What didn't work" for the coverage status of this property.)
* Pause / lock evaluation and week close (Day 31): checked the component for a pause mechanism and
  found none exists in scope — there is no pausable/freeze/shutdown surface, so the only lock is the
  min-duration cancel gate, already covered by the temporal invariants. Recorded that as a scope
  fact rather than building a mock to test. Wrote the public learning piece on queue state-machine
  testing and this retrospective.

### Metrics summary

| Metric | Total |
|---|---|
| Research minutes | ~560 |
| Learning minutes | ~60 (drafting the public queue-testing piece) |
| Community minutes | 0 |
| Contracts read (new) | 0 (re-reads of the already-mapped redeem/execute/fee surface) |
| Tests written | Deterministic state-machine tests for the temporal guards and the mixed batch, plus new handler actions (claim, recipient-rotation, second-settlement, batch execute) |
| Invariants defined | Committed suite now 11 (up from 7 at end of Week 3), spanning queue conservation, fee-lifecycle, temporal-state and batch-atomicity clusters |
| Hypotheses investigated | 1 low-confidence (per-id rounding direction and whether a batch could round in the protocol's favour on aggregate; filed privately) |
| Hypotheses discarded | 2 (batch ordering changing totals — wrong assumption; rounding drift compounding with batch size — no impact) |
| PoCs reproducible | 0 |
| Public contributions | 1 (public learning piece on queue state-machine testing drafted) |

### What worked

* Sequencing the week as one theme per day (fee lifecycle, then temporal, then batch atomicity)
  kept each addition landing on a stable, green baseline, so each new invariant's effect on the
  suite read cleanly instead of being tangled with the previous day's changes.
* Testing one-shot and adversarial properties by making the *attack* a fuzzer-callable action —
  second settlement, recipient rotation, zero-balance request — rather than asserting the happy
  path. The guards that survived thousands of randomised retries are the ones worth trusting.
* Treating "evaluate pause and lock" as a checklist item that can legitimately return "no such
  surface exists" saved a day of building and testing a mock pause that would have proven nothing
  about the actual code.

### What didn't work

* The Day 30 order-independence and rounding-drift property is reasoned through and recorded, but
  its invariant encoding is not committed in the current test tree — the suite on disk stands at 11
  committed invariants, and the batch value-effect check exists as analysis rather than a pinned
  invariant. This is the same reasoning-vs-coverage gap flagged in Week 3: a paper argument standing
  where a committed test should be. Re-committing it as a running invariant is the first cleanup
  task before extending the suite further.
* No community contributions landed live this week beyond drafting; the queue-testing piece is
  written but not yet posted.

### AI workflow notes

* Useful AI interactions: modelling the fee, temporal and batch properties as invariants and
  handler actions; reasoning through the order-independence and price-perturbation arguments from
  the execution loop's source; drafting the public learning piece and this retrospective.
* AI outputs rejected and why: none substantive this week.
* AI errors detected: a gap between a described invariant addition and what was actually committed to
  the test tree (the Day 30 batch value-effect invariant); caught by diffing the journal against the
  committed suite during the Day 31 close, and recorded above rather than papered over.

### Public learning to share

A redemption queue is a small state machine wearing accounting as a hat: each request walks
`pending -> settled` exactly once through one of two mutually exclusive doors (cancel or execute).
Almost every interesting queue bug is a way to walk a door twice, walk it before it opens, or walk
two ids through in an order that changes the total. Deterministic tests enumerate the edges; a
stateful invariant run composes them and finds the bug you did not write an edge for. And a negative
result — "this component has no pause surface" — is a fact about scope worth recording, not a hole to
fill with a mock. Full writeup:
[learning/queue-state-machine-testing.md](../../learning/queue-state-machine-testing.md).

### Blockers

None.

### Plan for next week

* Week 5 objective: debt accounting and integrations — study debt creation, modification and
  repayment; review signs, scales and conversions; analyse external dependencies and non-standard
  tokens where relevant.
* First cleanup task before new surface: re-commit the Day 30 batch value-effect / order-independence
  property as a running invariant so the committed suite matches the reasoning, closing the gap noted
  above.
* Then move into the debt/integration surface per the roadmap, opening any hypothesis in the private
  workspace and tracing it manually before logging.
* No adjustments to [ROADMAP.md](../../ROADMAP.md) required; Week 4 objectives met (flows mapped,
  duplicated-claim and partial-state properties modelled, pause/lock evaluated, precision/rounding
  studied, state-machine tests built, public learning piece drafted).
