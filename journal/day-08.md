# Day 8, 2026-06-17 (Wednesday)

* **Campaign day:** 8 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 1 (June 15-19) — technical onboarding of the primary target

## Objective

Complete the remaining Week 1 onboarding items deferred from Day 7: scope re-validation,
extension of the architecture map's data-flow and trust-boundary sections for the 7 components
mapped on Day 6, and formal re-confirmation of the initial cluster for Week 2.

## Time

* **Planned:** ~1h
* **Actual:** ~1h

## Area studied

Primary target: scope re-validation + architecture-map trust-boundary and data-flow extensions
for the transfer-validator cluster (the transfer-validator contract, an ownable address list,
an owned-shares address list, the address-list base) and utility/infra contracts (the global config contract,
a 1:1 price aggregator, the component beacon proxy, the storage-helpers library).

## Activities

* Re-validated the scope page on Immunefi: page shows ~25 items = 24 contracts +
  1 Primacy of Impact policy entry (already documented in the June 11 lock as a non-contract
  entry). No new contracts added, no changes to impacts in scope, exclusions, or max bounty
  ($200k). Re-validation log entry added to `scope-lock.md`.
* Extended `architecture-map.md` section 2 (Data flow): added the shares token contract
  transfer / compliance-list check path — `transfer`/`transferFrom` →
  the transfer-validation internal → the transfer validator — and the key
  bypass: the internal mint function/the internal burn function call OZ `_mint`/`_burn` directly, so the validator is never
  invoked during deposit/redeem issuance or share-burning.
* Extended `architecture-map.md` section 4 (Trust boundaries): added 3 new rows:
  1. Transfer-validator / compliance lists: who controls each list type and what the validator
     does and does not gate (issuance is uncontrolled).
  2. the global owner as the ownable root-of-trust: immediate control over
     the beacon factory's implementation setter for all deployed the depositor wallet proxies.
  3. the shares beacon proxy binding: immutable at deploy time, the on-chain mechanism
     that locks each component to exactly one fund.
* Added a Week 1 completion note to `architecture-map.md` section 6 (Open questions)
  confirming initial cluster for Week 2.
* Updated private daily tracker.

## Tests / experiments

* None today; documentation / architecture-mapping pass only.

## Hypotheses generated

* None new.

## Hypotheses discarded

* None new.

## AI usage

* Re-fetching and parsing the Immunefi scope page to compare current asset count against the
  June 11 snapshot.
* Drafting the new data-flow bullet and trust-boundary rows for the architecture map.

## Human verification

* Cross-checked the transfer-validator data-flow addition against the shares token contract
  the transfer-validation internal / the internal mint function / the internal burn function call paths already traced on Day 6 and
  Day 2 (audit-session-01 hyp. #6 / asymmetry item 3) — no new content, only formalizing into
  the architecture-map sections.
* Confirmed scope count reasoning: 25 page items = 24 contracts + 1 policy entry, consistent
  with the June 11 note already in `scope-lock.md`.

## Public learnings

* A compliance-list transfer validator gating `transfer`/`transferFrom` is architecturally
  distinct from controlling *who receives shares*: in systems where issuance goes through
  `mint` (bypassing the transfer hook), a compliance-excluded address can still receive shares
  via the deposit flow. Auditing compliance controls requires tracing every path that results
  in a balance increase, not just the transfer path.
* Re-validating scope at the end of an onboarding week (not just at the start) catches any
  asset additions that happened during the research window. A 5-minute check before the weekly
  retrospective is cheaper than discovering a missed in-scope contract mid-audit.

## Blockers

* None.

## Next step

Day 9 (2026-06-18, Thursday): Week 1 weekly retrospective — summarize what was covered,
what worked, and the plan for Week 2.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).
