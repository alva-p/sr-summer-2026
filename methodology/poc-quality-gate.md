# PoC Quality Gate

Run through this checklist before considering a PoC "done" and moving to the
[report quality gate](report-quality-gate.md). PoC code and outputs live in the private
`pocs/` directory — never in this public repo.

## Checklist

- [ ] **Reproducible environment** — exact framework/version (e.g. Foundry version), dependencies
      pinned, documented.
- [ ] **Commit recorded** — the exact commit/tag of the target code the PoC runs against.
- [ ] **Initial state documented** — fork block number (if forking), starting balances/state
      relevant to the PoC.
- [ ] **Realistic preconditions** — the setup reflects conditions an actual attacker could reach
      (no privileged test-only setup unless that privilege is realistically attainable).
- [ ] **Complete sequence** — every step from initial state to impact is included, no missing
      "and then magic happens" steps.
- [ ] **Expected result stated** — what the PoC is supposed to demonstrate, written down *before*
      running it.
- [ ] **Actual result recorded** — what actually happened when run, including any deviations from
      expectations.
- [ ] **Observable impact** — the impact is measurable (e.g., balance change, stuck funds, broken
      invariant) and matches an in-scope impact category.
- [ ] **Runs from a clean checkout** — a fresh clone + the documented setup steps reproduces the
      result, not just "works on my machine".
- [ ] **No dangerous interaction with public networks** — no mainnet transactions, no interaction
      with real user funds or live infrastructure beyond what the program explicitly allows.

## If any box is unchecked

Do not proceed to the report quality gate. Either fix the gap, or — if the gap reveals the hypothesis
doesn't hold — return to [hypothesis-template.md](hypothesis-template.md) and mark it discarded with
the reason.
