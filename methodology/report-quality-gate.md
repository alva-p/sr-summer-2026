# Report Quality Gate

Run through this checklist before submitting a report on Immunefi. Report drafts live in the private
`reports/` directory, never in this public repo.

## Checklist

- [ ] **Asset in scope**: the affected contract/component is explicitly listed as in scope, on the
      version/commit covered by the program.
- [ ] **Impact in scope**: the claimed impact matches one of the program's defined impact
      categories.
- [ ] **Correct version**: the report references the correct deployed/target version, not a stale
      fork or outdated commit.
- [ ] **Root cause explained**: the underlying issue is described clearly, not just the symptom.
- [ ] **Attacker conditions stated**: what an attacker needs (capital, role, timing, prior state) is
      explicit and realistic.
- [ ] **Reproducible steps**: numbered, complete steps from a clean environment to the impact.
- [ ] **Functional PoC**: passed the [PoC quality gate](poc-quality-gate.md).
- [ ] **Demonstrated impact**: the PoC shows the actual impact (e.g., funds at risk, broken
      invariant), not just "this looks suspicious".
- [ ] **Severity justified**: severity claim is backed by the program's severity classification
      system and the demonstrated impact, not inflated.
- [ ] **Known issues reviewed**: checked against the program's documented known issues.
- [ ] **Prior audits reviewed**: checked whether this issue (or something close) was already
      flagged/accepted/fixed in a prior audit.
- [ ] **Clear writing**: no ambiguity about which function, line, or condition triggers the issue.
- [ ] **No exaggerated claims**: impact described matches what was actually demonstrated, not a
      worst-case extrapolation presented as fact.
- [ ] **No irrelevant information**: the report stays focused; remove exploratory dead ends,
      personal notes, and unrelated observations.
- [ ] **Final skeptical-triager pass**: re-read the report as if you were a triager looking for a
      reason to reject it (see [ai-workflow/verification-checklist.md](../ai-workflow/verification-checklist.md)
      for how AI can help with this pass).

## If any box is unchecked

Do not submit. Either close the gap, or downgrade/reframe the report to match what's actually
demonstrated.
