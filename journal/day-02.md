# Day 2, 2026-06-11 (Thursday)

* **Campaign day:** 2 of 59 working days (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Initial week (2026-06-10 to 2026-06-12)

## Objective

Re-validate candidate programs against current Immunefi program pages, complete the
bounty-selection scoring matrix, confirm the scope-lock template is ready, and prepare the
local private workspace, per [ROADMAP.md](../ROADMAP.md) (initial week, Thursday).

## Time

* **Planned:** 2h
* **Actual:** Extended session — re-validation/selection/clone work plus two full audit
  passes and a follow-up PoC (well beyond the usual ~2h, by mutual choice since momentum was
  good).

## Area studied

No protocol code yet. Today was program/scope re-validation and workspace prep for the two
leading candidates (an accounting/vault-style program and a lending/credit-delegation program),
plus lighter checks on the stretch-goal program and two alternatives.

## Activities

* Re-validated all five candidate programs directly against their current Immunefi pages
  (status, scope, impacts, exclusions, known issues, rules, rewards), dated 2026-06-11.
* Wrote full program-evaluation entries (per
  [methodology/program-evaluation-template.md](../methodology/program-evaluation-template.md))
  for the two leading primary/secondary candidates in the private workspace.
* Wrote lighter re-validation notes for the stretch-goal program and two alternative programs.
* Built a selection-scoring matrix for the two leading candidates against the
  [bounty-selection.md](../methodology/bounty-selection.md) criteria; both scored very close
  (35/40 and 34/40), confirming the existing primary/secondary framing still holds.
* Confirmed the scope-lock template (created Day 1) is complete and generic, ready for use.
* Prepared the local private workspace: created per-target directories with pre-filled
  scope-lock drafts (program name, URL, impacts, exclusions, rules already copied in from
  today's re-validation).
* **Officially selected primary and secondary targets** (brought forward from the planned
  Friday slot, since both were already confirmed Solidity/EVM smart-contract programs during
  today's re-validation): the accounting/vault-style program as primary, the
  lending/credit-delegation program as secondary.
* Cloned the primary target's repository into the private workspace at the current `main`
  commit, ran `forge build` (success, 200 files compiled) and `forge test` (365/366 passing;
  the 1 failure is a mainnet-fork test that needs an RPC env var, not a code issue).
* Locked the scope for the primary target: recorded repo/commit, build/test status, the 24
  in-scope contracts with paths, impacts/exclusions/rules, and an initial cluster for next
  week's onboarding (shares, valuation, fees, debt tracking, deposit/redemption queues). A
  first pass had missed about half the in-scope contracts; corrected after re-checking the
  full scope page.
* Updated the private daily tracker with today's row.

## Tests / experiments

* Ran a multi-lens deep-audit pass over the primary target's full in-scope codebase (24
  contracts): one sequential pass plus five parallel adversarial-lens passes (known-pattern
  hunting, state-machine/reentrancy "breaker" modeling, economic/rounding analysis,
  trust-boundary mapping, and asymmetric-griefing analysis).
* The economic-analysis lens wrote a Foundry fuzz suite (3 properties, 20,000 runs each)
  checking round-trip rounding direction across the share/value/asset conversion math —
  all passed, rounding consistently favors the protocol.
* The boundary lens wrote a Foundry PoC checking an external-automation integration's
  metadata-decoding against malformed inputs — confirmed safe given the upstream trust
  assumption.
* Followed up on a code-ordering smell (effects-before-payment) flagged by the breaker lens in
  one of the deposit handlers, with a dedicated Foundry PoC using a reentrant mock token (3
  scenarios: re-entering the same call, double-balance double deposit, and transferring
  freshly-minted shares mid-reentrancy). All 3 scenarios confirmed no value extraction is
  possible; 16/16 tests pass (13 pre-existing + 3 new). Lead closed empirically, repo working
  tree left clean.

## Hypotheses generated

None reached a confidence level worth recording as an open hypothesis yet.

## Hypotheses discarded

* Across both sessions, ~24 hypotheses spanning arithmetic/overflow, fee accounting,
  donation/inflation variants, cross-chain message handling, redeem/deposit queue ordering,
  validator bypasses, and griefing via request cancellation were investigated and discarded.
  Reasons: documented behavior / by-design admin responsibility (several map directly to the
  scope's documented exclusions), required trust assumptions that hold, or no exploitable
  path found. Full reasoning is recorded privately per target.

## AI usage

* Used an AI assistant to search and summarize current Immunefi program pages for five
  candidate programs, draft the program-evaluation write-ups, build the scoring matrix, and
  pre-fill/lock the per-target scope-lock files, based on the existing methodology templates
  and yesterday's preliminary candidate notes.
* Used AI agents (one sequential pass, then five running in parallel under different
  adversarial lenses, plus one focused follow-up) to read the full in-scope codebase, apply
  audit methodologies, cross-check candidates against documented exclusions, and write/run
  Foundry fuzz tests and a reentrancy PoC, per
  [ai-workflow/workflow.md](../ai-workflow/workflow.md).

## Human verification

* Cross-checked the AI-summarized program data (status, scope, impacts, rewards, rules) against
  the actual Immunefi program pages it cited before recording it as the re-validated state, and
  caught/corrected an incomplete first pass at the in-scope asset list.
* Reviewed the scoring matrix and reasoning to confirm the existing primary/secondary framing
  (accounting/valuation focus first, lending/credit delegation as the planned second target)
  still makes sense given today's numbers, rather than accepting the scores at face value.
* Reviewed each agent's reasoning for discarded hypotheses and the final reentrancy PoC
  (including its 3 scenarios and test results) before accepting "no exploit found" as the
  conclusion, per
  [ai-workflow/verification-checklist.md](../ai-workflow/verification-checklist.md), and
  confirmed the cloned repo's working tree was left clean.

## Public learnings

* Re-validating bounty programs directly against the live Immunefi page, on a fixed date,
  before spending research time, surfaces useful details (reward ceilings, KYC requirements,
  dynamic scope clauses, embargo/disclosure categories) that are easy to miss if you work from
  memory or older notes. It's also worth re-checking the *full* in-scope asset list carefully —
  an initial pass missed about half of the in-scope contracts because newer additions weren't
  visible without expanding the scope table fully.
* Running several independent "lenses" (pattern-matching, state-machine, economic, trust
  boundary, griefing/asymmetry) over the same codebase in parallel, each required to
  cross-check candidates against the program's documented exclusions before treating anything
  as a finding, is a good way to get broad coverage quickly while keeping the false-positive
  rate manageable, even when the result for a session is "nothing yet."

## Blockers

None.

## Next step

Friday (2026-06-12): since target selection, clone, and two audit passes were brought forward
into today, Friday shifts to writing the initial-week retrospective and starting Week 1
onboarding (documentation/prior audits, architecture map, trust boundaries for the initial
cluster) — plus deciding where to point the next audit session (a less-covered cluster, e.g.
the cross-chain/automation contracts, or the secondary target).

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).
