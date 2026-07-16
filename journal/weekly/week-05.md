# Week 5, 2026-07-13 to 2026-07-17

### Objective for the week

Debt accounting and integrations: study debt creation, modification and repayment; review signs,
scales and conversions; analyse external dependencies and non-standard tokens where relevant;
investigate adversarial scenarios; validate or discard hypotheses; update the AI-workflow metrics.
(Week 5 runs July 13-17; retrospective written as the Day 37 week open on Monday July 20.)

### What I did

* Closed the carried-over cleanup (Day 32): re-committed the Day 30 batch value-effect /
  order-independence property as a running invariant (INV-BATCH-02), bringing the committed
  redeem-queue suite from 11 to 12. Read the execute loop again first to confirm the independent
  per-id computation mirrors the protocol, added a handler action that settles an all-live batch at a
  perturbed share price with optional id shuffling and compares vault outflow and supply burn against
  the independent per-id sum, and added two deterministic state-machine tests (order-independent
  totals, execution-time rate). Full suite green at the default runs and depth, zero reverts. Then
  scoped the Week 5 debt surface against the actual component: the target's debt equivalent is a
  signed linear credit/debt line-item tracker, a signed-arithmetic plus temporal surface rather than a
  borrow/collateral one.
* Read the signed linear write-down tracker (Day 33): a pure function of admin-set state plus the
  block timestamp, no external calls, each item a settled portion plus a portion that vests linearly
  over a duration. Found a sign-dependent rounding direction: the pro-rata uses signed integer
  division, which truncates toward zero, so the same formula lowers the reported magnitude for a
  credit (conservative) and also lowers it for a debt, reporting less debt than the exact pro-rata
  during the whole vesting window. Traced that bias end to end into the aggregate positions value and
  the net share value, confirming the debt direction inflates the share price. Checked the width
  boundaries and the negative-aggregate revert; the bias pushes away from the revert rather than
  toward it.
* Resolved the rounding surface by the trigger, not the arithmetic (Day 34): the read that sums the
  write-down is reachable only through the privileged share-value update, and unprivileged users
  consume a stored snapshot rather than a live recompute at their own timestamp. So an untrusted actor
  controls neither the inputs nor the instant the biased value is sampled, which closes the surface
  harder than an inputs-are-admin argument alone. Then mapped the external-dependency surface: the
  write-down component contributes no oracle or token dependency; the dependency enters the same
  aggregate through a sibling component that values a live on-chain balance, pulling in a per-asset
  rate and a token-decimals read. Characterised the conversion layer: an admin-pushed per-asset rate
  at 18-decimal precision, staleness enforced purely by an expiry timestamp with no deviation or
  heartbeat bound, and a precision base built from a live decimals read.
* Probed the conversion staleness on the permissionless mint (Day 35): the asset-to-value conversion
  happens live at call time on the manual rate, while the per-share price it divides by is the pushed
  snapshot, so one mint mixes two inputs of different freshness origins. The snapshot share price is
  checked against a configurable rolling max-age, whereas the per-asset rate is checked only against an
  absolute operator-set expiry with no rolling max-age and no deviation bound, the weaker gate.
  Confirmed the whitelist prevents pointing the live decimals read at an attacker token, and that a
  same-asset deposit-then-redeem round trip cancels the rate, so any profit would need a cross-asset
  path plus a deviation exceeding entrance and exit fees.
* Closed the week on the fee-handler interaction in the aggregate (Day 36): fees owed are subtracted
  from total positions value before the per-share division. There are two checked subtractions on the
  path; bounding the operands showed the settlement's subtraction is the binding one and the
  aggregate's underflows only under the same condition, so the second check is redundant with the
  first rather than an independent risk. The only failure is a documented revert (a valuation-liveness
  stop), reachable only under an operator-config plus a market drawdown, and the settlement is doubly
  access-controlled while the consume path reads a stored snapshot.

### Metrics summary

| Metric | Total |
|---|---|
| Research minutes | ~600 (five sessions at ~2h) |
| Learning minutes | 0 |
| Community minutes | 0 |
| Contracts read (new) | The signed linear write-down tracker, the sibling live-balance position component, and the conversion layer; plus re-reads of the batch execute loop and the fee aggregate |
| Tests written | INV-BATCH-02 plus two deterministic state-machine tests (all Day 32); no new tests Days 33-36 |
| Invariants defined | Committed suite now 12 (up from 11 at end of Week 4) |
| Hypotheses investigated | Debt/integration candidates: sign-dependent rounding in the linear write-down, and expiry-only staleness with no deviation bound on the manual conversion rate |
| Hypotheses discarded | 4 (sign-dependent rounding as an unprivileged angle; expiry-only staleness as an unprivileged no-cost angle; the fee-aggregate subtraction as an unprivileged distortion; unprivileged deposit/redeem inverting the owed-versus-positions inequality) |
| PoCs reproducible | 0 |
| Public contributions | 0 |

### What worked

* Resolving each candidate by asking who controls the sampling instant, not only whether the
  arithmetic is biased. The Day 34 move (the read is privileged-only and users consume a snapshot)
  closed the rounding surface more firmly than the Day 33 inputs-are-admin observation, and the same
  lens closed the staleness and fee-subtraction candidates later in the week.
* Sequencing the week as one angle per day down a single value path: the write-down math, then how it
  is sampled and consumed, then the conversion staleness on the consume path, then the fee subtraction
  at the aggregate. Each day started where the previous one's open question ended, so nothing was
  re-derived.
* Bounding the operands to find the binding one of two subtractions on the fee path (Day 36), which
  turned an apparent second failure mode into a redundant check rather than a separate risk.

### What didn't work

* The week produced no committed test after Day 32. Days 33 through 36 were reading and tracing
  passes whose deliverables were recorded surfaces and closures, not pinned properties, so the
  rounding-bias and staleness-asymmetry observations live as prose in the private workspace rather
  than as committed invariants. This is the same reasoning-versus-coverage gap flagged in Weeks 3 and
  4: an argument standing where a committed artifact could.
* No finding with demonstrated unprivileged impact emerged. Every candidate closed on the same reason:
  admin-controlled inputs plus a stored-snapshot consume path. That is an honest negative, but it
  means Week 5 opened surfaces and closed them rather than landing a report, which is worth flagging
  going into the Week 6 checkpoint.
* No community contribution this week; the metric line is zero on learning and community minutes.

### AI workflow notes

* Useful AI interactions: enumerating the callers of the settlement entrypoint, confirming the
  operands and ordering of the two subtractions on the fee-aggregate path, and confirming that the
  permissionless consume path reads the stored snapshot rather than re-running the settlement.
* AI outputs rejected and why: none substantive this week.
* AI errors detected: none this week; the enumerations were spot-checked by hand against the source
  and matched.

### Public learning to share

A biased or stale derived value is only an unprivileged exploit if an untrusted actor can influence
its input, choose the instant it is sampled, and consume the result atomically. Across the whole week
three different-looking candidates (a sign-dependent rounding direction, an expiry-only rate staleness,
a fee-subtraction distortion) died on the same wall: the inputs are admin-controlled and users consume
a stored snapshot, which severs the influence-then-consume chain. The trust boundary on a value path
is who controls the sampling instant, not whether the arithmetic is imperfect. When you find biased
arithmetic, trace forward to the trigger before opening a hypothesis; the bug is only there if an
untrusted caller owns the trigger.

### Blockers

None.

### Plan for next week

* Week 6 objective: first quality checkpoint. Review every hypothesis opened across Weeks 1 to 5,
  remove duplicates and out-of-scope entries, reproduce the committed suite from a clean checkout, and
  apply the PoC and report quality gates to the strongest survivors. Submit only with sufficient
  evidence; do not force a submission to hit a metric.
* Close the reasoning-versus-coverage gap where a surface is worth keeping: decide, per closed
  candidate, whether it belongs as a committed invariant, a documented scope fact, or a discard.
* Fold the Day 36 position-tracker value-timing thread into the hypothesis review rather than treating
  it as new surface to hunt; judge it against the same trigger-ownership test that closed the Week 5
  candidates.
* No adjustments to [ROADMAP.md](../../ROADMAP.md) required; Week 5 objectives met (debt surface
  studied, signs and scales and conversions reviewed, external dependencies analysed, adversarial
  scenarios investigated, hypotheses validated or discarded).
