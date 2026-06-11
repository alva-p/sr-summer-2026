# Prompt Library

Generic, reusable prompts for each stage of [workflow.md](workflow.md). These are templates —
fill in the brackets with **abstracted** information per
[safe-use-policy.md](safe-use-policy.md). None of these reference any specific program.

## Spec

```text
Here is the public documentation for [protocol/component]. Summarize:
1. The main components and their responsibilities.
2. The core user flows (deposit, withdrawal, etc.).
3. Any explicit invariants or guarantees the docs claim.
4. Anything that seems underspecified or ambiguous.
```

```text
Here is a contract implementing [generic description, e.g. "an ERC4626-style vault with a
redemption queue"]. Without assuming anything from the docs, list what this code actually does:
state variables, external functions, access control, and any non-obvious computations
(e.g. rounding, scaling).
```

## Invariant

```text
For a system with these characteristics: [generic description of mechanism, e.g. "users deposit
asset A and receive shares; share price = totalAssets / totalSupply; fees accrue over time and are
minted as new shares"], propose:
1. Economic invariants (value conservation, solvency).
2. Authorization invariants.
3. State invariants (valid transitions).
4. Temporal invariants.
5. Cross-chain invariants (if relevant).

For each, state the precondition under which it should hold.
```

## Adversary

```text
For this invariant: [invariant statement], list adversarial scenarios that could violate it.
For each scenario, state:
1. What the attacker needs (role, capital, timing, prior state).
2. Whether those preconditions are realistic for an external actor.
3. What evidence (code location, test) would confirm or rule this out.
```

## PoC

```text
Generate a Foundry test skeleton (setup + helper functions only, no exploit logic) for a system
with these characteristics: [generic description]. Include fixtures for [actors/roles] and helper
functions for [common operations, e.g. deposit/withdraw/advance time].
```

## Report (skeptical triager)

```text
Act as a skeptical Immunefi triager reviewing this report draft. The report has been generalized
to remove identifying details, but the structure and reasoning are real. Flag:
1. Any claim not directly supported by the "Proof of Concept" section.
2. Any step that seems to assume something not stated as a precondition.
3. Any place where the severity claim seems higher than what's demonstrated.
4. Any wording that's ambiguous about which function/line/condition triggers the issue.
5. Anything that reads as exaggerated or speculative.

[paste generalized report draft]
```

## General learning / community content

```text
I want to write a short, educational post about [general security concept, e.g. "rounding errors
in share-price calculations"], aimed at other security researchers. Use only generic examples (no
real protocol names or unresolved issues). Suggest a clear structure and a couple of illustrative
(hypothetical) code snippets.
```
