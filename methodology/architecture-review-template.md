# Architecture Review Template

Use this to build a working mental model of a target before forming hypotheses. This template is
generic; target-specific notes go in your private workspace.

---

## 1. Component inventory

| Component | Role | Upgradeable? | Owner / privileged roles |
|---|---|---|---|
| | | | |

## 2. Data flow

Describe (or diagram) how value and information move through the system for the core flows:

* Deposit:
* Withdrawal / redemption:
* Fee accrual / collection:
* Borrowing / debt creation (if applicable):
* Liquidation (if applicable):
* Cross-chain message flow (if applicable):

## 3. State variables of interest

| Variable | Contract | Meaning | Who can change it | Invariant candidates |
|---|---|---|---|---|
| | | | | |

## 4. Trust boundaries

| Boundary | Trusted party | What could go wrong if trust is violated |
|---|---|---|
| Oracle / price feed | | |
| Bridge / cross-chain messenger | | |
| Privileged role (admin, keeper, etc.) | | |
| External token / integration | | |

## 5. Spec vs. implementation

| Behavior described in docs/spec | Matches implementation? | Notes |
|---|---|---|
| | | |

## 6. Open questions

List anything unclear that needs more reading, testing, or (sanitized) discussion.

* [ ]
