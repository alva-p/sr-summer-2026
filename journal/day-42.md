# Day 42, 2026-07-21 (Tuesday)

* **Campaign day:** 42 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 6 (July 20-24) — transition after the first quality checkpoint

## Objective

Choose the next research surface from the technical retrospective, revalidate it before touching
code, and leave its first invariant backed by a reproducible check.

## Time

* **Planned:** ~2h
* **Actual:** ~2h30m

## Area studied

Second-sprint target selection and onboarding: scope/rule drift, lending and credit-delegation
architecture, trust boundaries, entry points, and the first solvency invariant.

## Activities

* Compared the remaining primary-target surface against the planned secondary target and moved the
  active sprint to the latter; the first target remains parked with its evidence intact.
* Revalidated the official program before review and found material drift from the initial
  evaluation: asset count, recent components, update date, and known-issue wording had changed.
* Cloned and pinned both the core repository and its required integration repository, including
  submodules.
* Built the core from a clean checkout and documented the one explicit dependency remapping needed
  for a reproducible build.
* Produced an architecture/threat/entry-point x-ray and selected the smallest first cluster that
  spans reserved credit, borrower collateral, external debt, and liquidation.
* Defined the first dynamic credit-reservation invariant and reused an existing fork test that
  already exercises it instead of adding a duplicate.

## Tests / experiments

* Targeted existing mainnet-fork invariant test: **1 passed, 0 failed**.
* Full coverage baseline attempted but discarded: the default profile did not initialize 16 fork
  suites, so the partial coverage number was not representative.
* No new test added today.

## Hypotheses generated

* Reserved credit must remain correctly sized through deposits, borrows, external risk-parameter
  changes, permissionless rebalancing, and both internal and external liquidation transitions.

## Hypotheses discarded

* None today; this was target onboarding and first-invariant selection.

## AI usage

* Used AI to compare the retrospective against the next-target matrix, recheck the live scope,
  enumerate architecture and git hotspots, trace the end-to-end integration, and identify the
  existing test that already encoded the chosen invariant.

## Human verification

* Confirmed the live program page and addresses, pinned both repository commits, read the relevant
  source paths end to end, ran the build, and executed the targeted fork test myself.

## Public learnings

* Refreshing scope is an onboarding deliverable, not clerical work: a month-old evaluation can be
  materially stale before the first deep review starts.
* If an existing fork test already expresses the chosen invariant, reusing it gives stronger and
  cheaper evidence than writing a renamed duplicate.
* A partial coverage report from suites that failed setup is noise; preserve the failure reason and
  establish the correct profile before using the number.

## Blockers

* The clean build needs an explicit dependency remapping not documented in the repository's default
  command.
* A representative full-suite/coverage baseline still needs the intended fork profiles and RPC
  environment.

## Next step

Compare prior audits and current known issues against the independent x-ray, then exercise the
first invariant across its state transitions rather than only its current single-path check.

## Confidentiality check

- [x] This entry contains only sanitized process, aggregate test status, and general learning. All
      target, address, contract, source, hypothesis-detail, and artifact names remain private.
