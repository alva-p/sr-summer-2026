# Invariant Template

An invariant is a property that should hold **across all reachable states** of the system, regardless
of the sequence of operations that led there. Use this template to define and track invariants
during invariant testing (Week 2-3 onward, see [ROADMAP.md](../ROADMAP.md)).

---

## Invariant ID: `INV-XXX`

* **Category:** economic / authorization / state / temporal / cross-chain
* **Statement:** (plain-language description of what should always be true)
* **Formal expression:** (pseudo-code or Solidity-like expression, if applicable)

```text
e.g. sum(userShares) == totalSupply
e.g. totalAssets >= sum(userClaimable)
e.g. for any user, claimedAmount <= requestedAmount
```

* **Relevant functions/contracts:**
* **Relevant state variables:**
* **Preconditions** (when does this invariant apply? e.g., "only after the queue is unpaused"):

## Test status

| Status | Meaning |
|---|---|
| Defined | Invariant written, not yet implemented as a test |
| Implemented | Implemented in a fuzzing/invariant test suite |
| Holds | Ran with no violations found (record run parameters) |
| Violated, test bug | Failure traced to an issue in the test/handler, not the protocol |
| Violated, wrong assumption | Failure traced to an incorrect assumption in this invariant |
| Violated, documented behavior | Failure matches documented/expected behavior, not a bug |
| Violated, potential hypothesis | Failure may indicate a real issue, promote to [hypothesis-template.md](hypothesis-template.md) |

* **Current status:**
* **Run parameters** (runs, depth, seed if reproducible):
* **Notes:**

## Categories reference

* **Economic**: value conservation, solvency, share price monotonicity (under defined conditions),
  fee bounds.
* **Authorization**: only role X can call function Y; privilege escalation is impossible.
* **State**: valid state transitions only; no unreachable or stuck states.
* **Temporal**: ordering and timing constraints (e.g., a claim cannot happen before a request,
  cooldowns are respected).
* **Cross-chain**: message integrity, replay protection, ordering, and consistency between chains.
