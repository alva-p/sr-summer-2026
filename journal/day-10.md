# Day 10, 2026-06-19 (Friday)

* **Campaign day:** 10 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 1 (June 15-19) — technical onboarding of the primary target

## Objective

Close out Week 1. Process the second triage response of SR Summer 2026 and extract the learning.

## Time

* **Planned:** ~1h
* **Actual:** ~1h

## Area studied

Triage feedback on a submitted report; intentional design patterns in perpetuals market close paths.

## Activities

* Received a closed/out-of-scope verdict on a submitted bug report. The triage team ruled the
  finding describes an intentional design distinction between two settlement paths, not a security
  vulnerability: in the manual close flow, liquidation is evaluated at mid-price by design and the
  spread is an execution cost on the trader, not a solvency criterion. No theft from the vault.
* Processed the rejection reason in detail, mapped it against the original hypothesis, and
  categorized the discarded hypothesis.
* Posted a tweet acknowledging the outcome (the bad alongside the good).
* Updated private daily tracker and contribution log.

## Tests / experiments

* None today.

## Hypotheses generated

* None new.

## Hypotheses discarded

* Report closed by triage: the difference between mid-price liquidation check and effective
  settlement price in the manual close path. Category: documented behavior / intentional design
  distinction. The spread is an execution cost, not a solvency gap.

## AI usage

* Drafting the journal entry and tweet from the triage response.

## Human verification

* Read the triage feedback in full and cross-referenced the original hypothesis before updating
  the discarded list.
* Reviewed the tweet draft for confidentiality compliance: no target-specific names, no function
  names, no in-scope contract references.

## Public learnings

* Getting a "closed" verdict early is useful signal: it forces precision about what counts as a
  design choice versus a vulnerability. The triage team's explanation is a free lesson on where
  the protocol's risk model sits.
* Intentional asymmetry between paths (manual vs. automation) is common in perpetuals protocols.
  Before submitting on a path difference, the question to answer first is: "is this asymmetry
  documented, and does it create loss from the vault's perspective or only from the trader's?"
* The second triage closed too. That is two data points, not one. Each rejection sharpens the question to ask before submitting.

## Blockers

* None.

## Next step

Week 2 starts Monday 2026-06-22. Objective: understand Shares, Valuation and Fees in depth;
define at least five invariants for the initial cluster per the campaign roadmap.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).
