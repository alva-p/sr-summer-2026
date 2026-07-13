# Day 34, 2026-07-15 (Wednesday)

* **Campaign day:** 34 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 5 (July 13-17) — debt accounting and integrations

## Objective

Resolve the Day 33 open question before building on it: decide whether the sign-dependent rounding
surface in the linear write-down has any repeatable, no-cost path an unprivileged actor can influence,
given every input is admin-set. If it does not, record it as reviewed with that reason. Then move to the
next Week 5 angle: the external dependencies and the conversions on the paths that consume the aggregate
value.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

How the aggregate value is *sampled and consumed*, rather than how it is computed: who can trigger the
read that sums the write-down, whether users see a live recompute or a stored snapshot, and what external
dependencies and unit conversions sit on the paths that turn the aggregate into a share price and into
per-user asset amounts.

## Activities

* Resolved the Day 33 open question by looking at the trigger, not the arithmetic. The read that sums the
  linear write-down into the aggregate is reachable only through the privileged share-value update; there
  is no other live caller. The value that unprivileged users actually consume on deposit and redeem is a
  stored snapshot, refreshed only when that privileged call runs, not a recompute at the user's
  timestamp. So an unprivileged actor can neither set the inputs nor choose when the biased value is
  sampled. This closes the surface harder than Day 33 framed it: the concern was not just that the inputs
  are admin-set, but that the *sampling instant* is admin-controlled too, and the per-item rounding error
  is sub-unit and admin-scheduled on top of that.
* Mapped the external-dependency surface of the consuming paths. The linear write-down component is
  self-contained: a pure function of admin-set state plus the block timestamp, no external calls, values
  already quoted in the shares value asset, so it contributes no oracle or token dependency to the
  aggregate. The dependency enters the same aggregate through a *sibling* position component that values a
  live on-chain balance, which pulls in a per-asset rate and a token-decimals read. Deposit, redeem and
  fee payout also cross the same conversion layer.
* Characterized the conversion layer that those paths use. It converts between an asset amount and the
  value-asset unit with an admin-pushed per-asset rate at 18-decimal precision, guarded by a
  rate-is-set and a not-expired check, where staleness is enforced purely by an expiry timestamp with no
  deviation or heartbeat bound. The precision base is built from a *live* decimals read on the asset.
  All of the conversion and per-share math is unsigned and floor-rounded through checked mul-div, so the
  signed-rounding subtlety from Day 33 does not recur on this path.
* Recorded the candidate surfaces generically in the private workspace: the expiry-only staleness model
  on the manual rate, and the reliance on a live external decimals read inside the precision base.

## Tests / experiments

* None built today. Reading and tracing pass; the deliverable was the resolution of the open question and
  the dependency map, not a committed property. The existing suite was not touched and stays at its Day 33
  state.

## Hypotheses generated

* One candidate surface, recorded generically: the manual per-asset rate on the consuming path has a
  staleness model (an expiry) but no deviation model, so a rate stays usable at its last value until it
  expires regardless of how far the real price has moved. Not yet a hypothesis with demonstrated impact,
  and gated by the admin's update cadence and expiry choice; the open question is whether any repeatable,
  no-cost path lets an unprivileged actor profit inside that window.

## Hypotheses discarded

* The Day 33 sign-dependent rounding surface in the linear write-down: closed as reviewed, no unprivileged
  and no user-timed path. The biased value is only ever produced by a privileged read and is delivered to
  users as a stored snapshot, so an unprivileged actor can influence neither the inputs nor the moment it
  is sampled, and the per-item error is sub-unit.

## AI usage

* Used AI to enumerate the live callers of the aggregate read and confirm the snapshot-versus-recompute
  distinction on the deposit and redeem paths, and to map the external-dependency and conversion surface
  of the components that feed and consume the aggregate.

## Human verification

* Re-read the consumer call sites myself to confirm that deposit and redeem read the stored share-value
  snapshot rather than recomputing the aggregate at the caller's timestamp, since the whole resolution of
  the open question rests on that being true.
* Confirmed by hand that the linear write-down component makes no external call while the sibling balance
  component does, so I could state which component actually drags the rate and decimals dependency into
  the shared aggregate rather than assuming they all behave the same.

## Public learnings

* A rounding bias is only exploitable if an untrusted party can influence both halves: the inputs *and*
  the instant it is sampled. A value delivered as a pushed snapshot removes the timing half even when the
  arithmetic in isolation looks skewed, so check the trigger and the delivery before spending time on the
  math.
* When several components feed one aggregate, their external-dependency surface is not uniform. A
  self-contained, pre-quoted component adds no oracle or token dependency, while a sibling that values a
  live balance drags a rate and a token-decimals read into the very same total. "What does the aggregate
  depend on" has to be answered per component, not for the aggregate as a whole.
* A manual push-rate guarded only by an expiry has a staleness model but no deviation model: it bounds how
  *old* a rate can be, not how *wrong*. Those are different guarantees, and only the first one is present.

## Blockers

* None.

## Next step

Probe the expiry-only rate staleness and the live-decimals precision base on the conversion path for any
repeatable, no-cost angle an unprivileged actor could drive inside an unexpired-but-stale window. If none
holds, record it as reviewed and move to the remaining Week 5 angle: the fee-handler interaction in the
aggregate, where fees owed are subtracted before the per-share division.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes a generic reading pass
      over a snapshot-based valuation aggregate and its conversion layer in generic terms, with no target
      name, contract identifier, or target-specific finding or exploit detail.
