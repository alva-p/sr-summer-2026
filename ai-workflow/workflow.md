# Workflow: Spec → Invariant → Adversary → PoC → Report

This is the AI-assisted layer that runs alongside the main research pipeline (see
[README methodology section](../README.md#methodology)). At every stage, AI is a collaborator that
proposes, summarizes, and challenges; a human verifies before anything moves forward.

```text
Spec → Invariant → Adversary → PoC → Report
```

## 1. Spec

**Goal:** build an accurate, shared understanding of what the system is supposed to do.

AI can help with:

* Summarizing public documentation, whitepapers, and READMEs.
* Enumerating components, contracts, and their stated responsibilities.
* Proposing preliminary architecture diagrams (to be corrected against the actual code).
* Comparing the written specification against the implementation and flagging mismatches to check
  manually.

**Human verification:** every component and responsibility AI lists is checked against the actual
source code, not just the docs.

## 2. Invariant

**Goal:** turn the mental model into testable properties.

AI can propose invariants in five categories (see
[methodology/invariant-template.md](../methodology/invariant-template.md)):

* Economic invariants (value conservation, solvency, fee bounds).
* Authorization invariants (who can call what).
* State invariants (valid transitions, no stuck states).
* Temporal invariants (ordering, cooldowns, timing).
* Cross-chain invariants (message integrity, replay protection, ordering).

**Human verification:** each proposed invariant is checked against the actual state variables and
functions before being recorded. Invariants that don't map to real code are discarded.

## 3. Adversary

**Goal:** turn invariants into adversarial questions.

AI can transform "X should always hold" into general questions like:

* "Under what sequence of calls could X be violated?"
* "What if a privileged role acts maliciously or is compromised?"
* "What if an external dependency (oracle, bridge, token) returns unexpected values?"
* "What if two operations are reordered or interleaved?"

**Human verification:** each adversarial question is evaluated for whether the preconditions are
actually reachable in scope. Most are ruled out quickly: that's expected and is itself a useful
output (see [methodology/hypothesis-template.md](../methodology/hypothesis-template.md)).

## 4. PoC

**Goal:** turn a validated hypothesis into a reproducible demonstration.

AI can help generate **test skeletons**: boilerplate setup, fixtures, helper functions.

**Human verification (non-negotiable):**

* Every test is run locally.
* Every assertion is checked against the actual contract behavior, not assumed.
* No PoC is considered valid until it has been executed from a clean environment and produces the
  claimed result.

## 5. Report

**Goal:** produce a report that survives a skeptical triager.

AI can act as a **skeptical triager** on a draft report (using only generic descriptions, see
[safe-use-policy.md](safe-use-policy.md)) and flag:

* Unproven assumptions.
* Irreproducible or ambiguous steps.
* Exaggerated impact claims.
* Scope mismatches.
* Incorrect severity reasoning.
* Missing evidence.
* Ambiguous wording.

**Human verification:** the researcher resolves every flag before submission, using the
[report quality gate](../methodology/report-quality-gate.md).

## What this workflow is not

* It is not a way to skip reading code.
* It is not a way to generate reports from a vulnerability description without a working PoC.
* It is not a substitute for the [PoC](../methodology/poc-quality-gate.md) and
  [report](../methodology/report-quality-gate.md) quality gates.
