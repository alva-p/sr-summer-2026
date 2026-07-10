# Learning Notes: State-Machine Testing of Redemption Queues

A public, disclosure-safe writeup from a week spent building invariant and state-machine tests for a
redemption-queue component. Priority area 10 in the [README specialization](../README.md#specialization).
General technique only, with a generic ERC-7540-style queue as the running example; no target,
finding, or exploit specifics (see [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md)).

## The shape of the problem

A redemption queue is a small state machine wearing accounting as a hat. A user *requests* a redeem,
which locks their shares and mints a request id; later the request is either *cancelled* by its
controller (shares refunded) or *executed* by an operator (shares burned, assets paid out). Each id
walks `pending -> settled` exactly once, and "settled" is reached by one of two mutually exclusive
doors.

That "exactly once, one of two doors" is the whole game. Almost every interesting bug in a queue is a
way to walk through a door twice, walk through it before it opens, or walk two ids through in an order
that changes the total. So the tests worth writing are the ones that attack those three things
directly.

## Deterministic transitions first, then interleave them

Start with plain unit tests, one per edge of the state machine: request results in pending; execute a
pending id results in settled and pays out; cancel before the lock elapses reverts; cancel after it
elapses refunds; a second settlement of the same id reverts. These are cheap, they document the
intended machine, and they fail loudly when a refactor moves an edge.

But a deterministic edge test proves a guard holds *for one transition in isolation*. It says nothing
about whether the guard survives being interleaved with every other action against the same storage.
The valuable increment is a stateful (invariant) test: a handler that exposes request / cancel /
execute / warp-time as fuzzer-callable actions, bounded to realistic inputs, driven for thousands of
randomised sequences, with a set of invariants checked after every call. That is where a cancel and
an execute race the same id, where a warp lands exactly on a lock boundary, where an id gets settled
and then a stale reference to it gets replayed.

Rule of thumb: **unit tests enumerate the edges; the invariant run composes them.** You want both, and
the invariant run is the one that finds the bug you did not think to write an edge for.

## Three properties that earn their keep

**1. The one-shot resource.** A request must settle exactly once. Do not test this by asserting the
happy path succeeds. Test it by making a *second* settlement a fuzzer-callable action: pick an id the
handler has already settled and try to cancel or execute it again. The property is not "the retry
reverts" but "the retry moves nothing" — assert the share balance of the queue is byte-for-byte
unchanged across the failed retry. A guard you trust is one an adversarial action repeatedly failed
to break, not one you reasoned should hold.

**2. The timing gate, and who it actually protects.** Queues usually have a minimum duration before a
request can be cancelled. It is worth stating out loud *which party* the gate restricts. A
min-duration-before-cancel gate restricts the controller's own cancel; it does not restrict the
operator's fulfilment. So "can this be executed before the cancel window opens?" is a design question,
not a bug — the thing that actually forecloses a double-spend is the conservation invariant
(shares in equal shares out plus shares still pending), not the timing gate. Mislabelling who a gate
protects is how you write a test for the wrong property and feel safe.

**3. Batch atomicity and order-independence.** When execution takes a list of ids, two new properties
appear that a single-id test cannot reach:

- *Atomicity.* A batch that mixes live, already-settled, and duplicate ids must settle all or none.
  Here platform semantics do a lot of work for free: a loop with no per-item try/catch and no swallowed
  low-level calls is all-or-none, because one revert unwinds the whole transaction. So the bug to hunt
  for is the *opposite* of what you might guess — a `try/catch` or low-level `call` inside the loop that
  lets one failing item be skipped while its siblings commit. Fuzz a mixed batch and assert the failing
  case leaves zero footprint (no shares burned, no supply moved), not merely that it reverts.
- *Order-independence and rounding drift.* If per-item payouts are summed in a loop, permuting the id
  array must not change the totals, and per-item rounding must not accumulate. This holds *for free*
  only when each item converts from its own full-precision amount and no remainder is carried between
  iterations. The bug to hunt for is a running accumulator or a shared intermediate that makes item N's
  result depend on item N-1 — which turns a permutation into a value change and makes rounding drift
  compound with batch size. When you assert "no drift", pin the bound to a *single* item's rounding, not
  N items'; a bound of N times the per-item error is loose enough to pass even when the error genuinely
  accumulates.

## Temporal state is the dimension unit tests skip

A fixed-price, fixed-time suite under-tests a queue, because the whole point of a queue is that request
time and settlement time differ. The interesting invariant is temporal: settle a request against a
share price that *moved* between when it was recorded and when it executed, and assert the payout uses
the execution-time rate and still matches the per-id sum. A suite that only ever runs at one price
passes happily while a request-time / execution-time confusion sits undetected. Perturbing time and
price between request and execution is the cheapest way to expose that class of bug.

## A negative result is still a result

Part of studying a component is enumerating the mechanisms it *should* have and checking each. When the
checklist says "evaluate pause and lock behaviour" and the component turns out to have no pause
mechanism at all, that is not a gap in the test suite — it is a fact about the scope, and it belongs in
the notes. Do not build a mock pause and test it; you would be testing fiction, not the code. Write down
"no pause surface exists; the only lock is the min-duration cancel gate, covered by the temporal
invariants" and move on. Testing that the absent feature is absent is a waste; recording that you looked
is not.

## Checklist for the next queue

- [ ] One deterministic test per state-machine edge (request, cancel-too-early, cancel-after-lock,
      execute, double-settle).
- [ ] Stateful handler with bounded actions; invariants checked after every call.
- [ ] Conservation invariant (shares in = out + pending) as the backstop for double-spend.
- [ ] Second-settlement as an adversarial action asserting zero state movement, not just a revert.
- [ ] Batch action mixing live / settled / duplicate ids; assert all-or-none with zero footprint on
      failure.
- [ ] Order-permutation and price-perturbation between request and execution; assert execution-time rate
      and per-item-sum equality, with a single-item drift bound.
- [ ] Explicitly record which mechanisms (pause, lock, access gates) exist and which do not.

## References

(Foundry book: invariant testing, `targetSelector`, handler-based fuzzing. ERC-7540 asynchronous
redemption interface. Public writeups on stateful fuzzing of vault/queue components.)
