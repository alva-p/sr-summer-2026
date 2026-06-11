# Hypothesis Template

This template tracks a candidate vulnerability hypothesis from "interesting observation" to
"validated / discarded". **Filled-out copies of this file containing target-specific information must
live in the private workspace** (`private/<target>/hypotheses/`), never in this public repo. Only the
*aggregate counts* (investigated / discarded) go into [data/daily-metrics.csv](../data/daily-metrics.csv)
and [data/weekly-metrics.csv](../data/weekly-metrics.csv).

---

## Hypothesis ID: `HYP-XXX`

* **Date opened:**
* **Related invariant(s):** (link to INV-XXX)
* **Component(s) involved:**
* **Summary:** (one paragraph — what could go wrong, in plain language)

## Adversarial framing

* **Attacker goal:**
* **Attacker capabilities / preconditions assumed:**
* **Trust assumptions being challenged:**

## Evidence so far

* **Code references (file:line):**
* **Relevant tests/fuzz runs:**
* **Supporting observations:**
* **Contradicting observations:**

## Validation plan

* [ ] Reproduce minimal scenario in a test
* [ ] Confirm preconditions are reachable in scope
* [ ] Confirm impact maps to an in-scope impact category
* [ ] Check against known issues / prior audits
* [ ] Check primacy of impact vs. rules implications

## Outcome

* **Status:** open / validated / discarded
* **If discarded — reason:** test bug / wrong assumption / documented behavior / out of scope /
  duplicate / no real impact / other (explain)
* **If validated — next step:** proceed to [poc-quality-gate.md](poc-quality-gate.md)
* **Date closed:**
* **Public-safe learning** (one sentence, generic, suitable for the public journal — optional):
