# Scope Lock Template

A "scope lock" is a snapshot of exactly what you are allowed to look at, on which version, and under
which rules — taken **once per research sprint** before deep work begins, so that scope drift and
"but the docs said..." disputes are minimized.

This file should be copied into your **private** workspace (`private/<target>/scope-lock.md`) — it
will contain target-specific information that should not be published. This template itself stays
generic.

---

## Target

* **Program name:**
* **Immunefi program URL:**
* **Date locked:** (YYYY-MM-DD)

## Code reference

* **Repository URL:**
* **Commit hash / tag covered by scope:**
* **Build instructions verified?** yes/no
* **Tests passing locally?** yes/no (record command + summary, not full output if sensitive)

## Assets in scope

| Contract / component | Address (if deployed) | Chain | Notes |
|---|---|---|---|
| | | | |

## Impacts in scope

* (copy directly from program page, with date checked)

## Exclusions / known issues

* (copy directly from program page, with date checked)

## Rules

* **Primacy of Impact / Primacy of Rules:**
* **PoC requirements:**
* **Disclosure policy:**
* **Operational restrictions:**

## Actors and roles

| Actor | Description | Privileges |
|---|---|---|
| | | |

## External dependencies

| Dependency | Type (oracle, bridge, token, etc.) | Trust assumption |
|---|---|---|
| | | |

## Initial cluster for this sprint

List the small set of contracts/components chosen as a starting point, and why.

* Component:
* Reason:

## Re-validation log

| Date | Change observed | Action taken |
|---|---|---|
| | | |
