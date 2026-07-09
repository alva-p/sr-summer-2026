# Day 30, 2026-07-09 (Thursday)

* **Campaign day:** 30 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 4 (July 6-10) — redemption, queues and temporal state

## Objective

Close the Day 29 next step: stress the batch execute against ordering and value effects rather than
just membership. Model a large batch of all-live ids settled under a share price that moves between
request time and execution time, and check that the summed assets paid out and shares burned match
the per-id sum regardless of the order ids appear in the batch — no cross-id interference and no
rounding drift accumulating across the loop.

## Time

* **Planned:** ~2h
* **Actual:** ~2h15m

## Area studied

The value-effect side of the batch execute loop: how a batch of independently-requested ids settles
when the per-share price is not constant across the batch's lifetime. Until today the batch tests all
ran at a fixed price, so the loop's arithmetic was only ever exercised against a single conversion
rate. The two things that had never been fuzzed were (a) whether batch ordering changes the totals,
and (b) whether the per-id rounding in the shares-to-assets conversion accumulates a drift when many
ids are summed in one call versus settled one at a time.

## Activities

* Added a price-perturbation hook to the invariant handler so the share price can be nudged (up or
  down, bounded) at a point between when a request is recorded and when its id is executed, letting
  the batch settle against a rate that differs from the rate at request time.
* Extended the batch-execute action to draw a larger all-live batch (up to the handler's id cap) and
  to optionally shuffle the id array before the call, so the same membership set is settled in
  different orders across runs.
* Wrote a ghost that accumulates, per id, the assets that *should* be paid and the shares that
  *should* be burned computed independently (one id at a time at the execution-time price), then
  compares that independent sum against the batch call's actual aggregate movement.
* Added INV-BATCH-02 (batch totals are order-independent and equal the per-id sum): the summed assets
  out and shares burned from a batch equal the sum of the same ids settled individually, and are
  invariant under permutation of the id array.
* Added a bounded-drift assertion alongside it: any divergence between the batch aggregate and the
  independent per-id sum must be zero for shares burned, and at most the documented per-id rounding
  bound (not per-id-times-n) for assets, so a systematic drift accumulating across the loop would
  trip it.
* Added two deterministic tests to the state-machine suite: the same three-id batch settled in two
  different orders pays out byte-for-byte identical totals; and a batch settled after a mid-life price
  bump pays the execution-time rate, not the request-time rate.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* Extended the redeem-queue invariant suite from eleven invariants to twelve (added INV-BATCH-02) and
  added the price-perturbation hook plus the shuffle option to the existing batch-execute action (no
  new handler action).
* Full suite green: 12 invariants pass at the default 256 runs / depth 500, 128,000 calls each, zero
  reverts. The perturbed/shuffled batch path fired ~9.4k times, and the order-permutation branch
  reached both the shuffled and unshuffled arms.
* Added two deterministic state-machine tests (order-independence and price-bump-uses-execution-rate);
  both pass.

## Hypotheses generated

* One low-confidence note filed to the private workspace on where per-id rounding *direction* is
  chosen in the conversion and whether a batch could ever round in the protocol's favour on every id
  and against a single user on aggregate. Kept generic here; details and the concrete check live in
  the private hypothesis file per
  [methodology/hypothesis-template.md](../methodology/hypothesis-template.md).

## Hypotheses discarded

* "Batch ordering could change the payout totals" — discarded as wrong assumption. Each id's
  conversion reads only that id's stored request and the current price; ids do not read each other's
  intermediate state, so the loop is a pure sum of independent terms and any permutation yields the
  same total. The fuzzer confirmed identical aggregates across thousands of shuffled orders.
* "Rounding drift accumulates linearly with batch size" — discarded as no impact at the observed
  scale: the per-id rounding is bounded and does not compound, because each id converts from its own
  full-precision share amount rather than from a running remainder carried across the loop. The
  aggregate error stayed within the single-id bound, not n times it.

## AI usage

* Drafted the price-perturbation hook, the shuffle option, the order-independence invariant, and the
  two deterministic tests in the existing suite style, and drafted this entry.
* Cross-checked that the independent per-id ghost computes conversion at the execution-time price (not
  the request-time price), so the comparison isolates ordering/drift effects and does not spuriously
  fail on the intended price change.

## Human verification

* Traced two ids through the loop by hand at a changed price: each reads its own stored shares and the
  single current rate, so the second id's payout does not depend on whether the first ran before it.
  Confirmed the summation has no carried remainder between iterations, which is what makes the drift
  bounded by one id's rounding rather than n.
* Confirmed the order-independence test actually permutes the array (not just relabels it) and asserts
  equality of both totals and post-state, so a cross-id interference would fail the equality, not pass
  silently.
* Checked the price-bump test asserts the execution-time rate is used by pinning the expected payout to
  the post-bump price and showing the request-time price would have produced a different, failing number.
* Verified the bounded-drift assertion uses the single-id bound, not n times it, so it would actually
  catch a linear accumulation rather than being loose enough to hide it.
* Ran `make safety-check` and read the output before marking the entry ready.

## Public learnings

* A loop that sums independent per-item conversions is order-independent for free — but only if each
  item converts from its own full-precision amount and no remainder is carried between iterations. The
  bug to hunt for is a running accumulator or a shared intermediate that makes item N's result depend
  on item N-1, which turns permutation into a value change and makes rounding drift compound with batch
  size.
* Fuzzing a batch at a single fixed price under-tests it. The interesting invariant is temporal: settle
  the same membership set against a price that moved between request and execution, and assert the
  execution-time rate is used and the totals still match the per-id sum. A fixed-price suite passes
  while a request-time/execution-time price confusion sits undetected.
* When asserting "no rounding drift", pin the bound to a single item's rounding, not n items'. A bound
  of n times the per-item error is loose enough to pass even when the error genuinely accumulates —
  the tight bound is the one that turns the invariant into a real check.

## Blockers

* None.

## Next step

Close Week 4 (Day 31, Friday) with the pause/lock dimension of the queue: model request, cancel and
execute interleaved with the contract entering and leaving a paused state mid-batch, and check that no
operation half-commits across a pause boundary and that a cancel during pause cannot strand or
double-free shares. Then write the Week 4 public learning piece on queue state-machine testing using
educational (non-target) examples, per the Week 4 roadmap deliverable.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes generic
      order-independence and rounding-drift invariant testing of an ERC7540-like redeem queue with no
      target or finding specifics.
