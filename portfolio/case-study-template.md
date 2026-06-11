# Case Study Template

A sanitized write-up of a research sprint, what was studied, how, and what came out of it. Written
so that **no confidential information** is revealed (see
[SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md)): generalize protocol-specific details
where needed, and never describe an unresolved vulnerability.

---

## Title

(e.g. "Mapping a redemption-queue system and building invariant tests")

## Context

* **Type of system:** (e.g. "ERC4626-style vault with asynchronous redemption queue")
* **Time period:**
* **Goal:**

## Approach

* Architecture mapping process, what worked, what was hard.
* Trust assumptions identified.
* Invariants developed (categories, count, generic descriptions).
* Testing approach: unit tests, fuzzing, invariant testing, tools and techniques used.

## Outcome

* Coverage achieved (generic terms, e.g. "covered the full deposit/redemption lifecycle and fee
  accrual").
* Hypotheses investigated and discarded (counts, generic reasons).
* Reports submitted, if any, **and the program's public disclosure status** (only reference once
  disclosure is allowed).
* Tools or templates produced that are now part of [methodology/](../methodology/) or
  [scripts/](../scripts/).

## What I'd do differently

## Skills demonstrated

(e.g. Foundry invariant testing, ERC4626 accounting analysis, report writing)
