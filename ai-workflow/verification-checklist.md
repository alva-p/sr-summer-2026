# AI Output Verification Checklist

Every AI output used in research must pass through human verification before it influences a
hypothesis, test, or report. This checklist is the "trust but verify" layer referenced throughout
[workflow.md](workflow.md).

## For Spec-stage outputs (summaries, component lists, diagrams)

- [ ] Cross-checked against the actual source code, not just docs.
- [ ] Component responsibilities verified by reading the relevant contract(s).
- [ ] Any claimed spec/implementation mismatch independently confirmed.

## For Invariant-stage outputs

- [ ] Invariant maps to real, existing state variables and functions.
- [ ] Invariant is actually meaningful in this system (not a generic template that doesn't apply).
- [ ] Preconditions for the invariant are stated and checked for reachability.

## For Adversary-stage outputs

- [ ] Each adversarial scenario's preconditions checked against the real scope/permissions.
- [ ] Scenarios that require unreachable preconditions are explicitly marked as ruled out (with
      reason), not silently dropped.

## For PoC-stage outputs (test skeletons)

- [ ] Code compiles and runs as-is (after filling in target-specific details).
- [ ] Every assertion reflects actual observed behavior, run locally, not an assumption carried
      over from the AI's suggestion.
- [ ] Test passes/fails for the *reason* documented, not for an unrelated reason (e.g., a revert
      earlier in the call).
- [ ] Passes the [PoC quality gate](../methodology/poc-quality-gate.md).

## For Report-stage outputs (triager feedback)

- [ ] Every flagged issue (unproven assumption, exaggerated impact, etc.) addressed or explicitly
      dismissed with reasoning.
- [ ] Severity claims double-checked against the program's own severity classification, not just
      the AI's suggestion.
- [ ] Final report passes the [report quality gate](../methodology/report-quality-gate.md)
      independently of the AI's pass.

## Logging errors

When an AI output is wrong, misleading, or just not useful, record it briefly in
[evaluation.md](evaluation.md) and in the day's journal entry ("AI errors detected" field). This is
useful signal for the AI-workflow writeups and is itself part of demonstrating that verification is
real, not theater.
