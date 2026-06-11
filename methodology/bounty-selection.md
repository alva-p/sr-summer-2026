# Bounty / Target Selection

This document records **how** targets are chosen and re-validated, and the current state of that
decision. It is updated whenever a target is selected, re-validated, or dropped.

## Selection criteria

For each candidate program, score on these dimensions (1-5, 5 = best fit):

| Criterion | Description |
|---|---|
| Scope clarity | Are in-scope assets, impacts and exclusions clearly defined? |
| Codebase quality | Modern tooling (Foundry/Hardhat), tests present, readable code |
| Fit with specialization | Accounting, lending, cross-chain, vaults, oracles, see [README](../README.md#specialization) |
| Documentation quality | Docs, audits, specs available and up to date |
| Activity/freshness | Program active, code not frozen/abandoned, recent commits |
| Reward structure | Rewards proportional to expected effort, primacy of impact vs. rules is workable |
| Time budget fit | Realistic to make progress at ~2h/day within the campaign |
| Learning value | Even without a finding, will this teach something useful (protocol accounting, lending, cross-chain)? |

## Process

1. Long-list candidates (from personal interest, community discussion, Immunefi explore page).
2. For each candidate, fill out [program-evaluation-template.md](program-evaluation-template.md):
   this re-validates current status directly on Immunefi (do not trust cached/old info).
3. Score against the criteria above.
4. Pick a primary and a secondary target; document the reasoning here.
5. Complete a [scope-lock](scope-lock-template.md) for the selected target before starting research.
6. Re-run this process whenever a target is dropped, paused, or a sprint ends (see
   [ROADMAP.md](../ROADMAP.md), Week 7).

## Current selection

The current candidates, scores and selection notes are tracked in the private workspace, not in
this public repo. This avoids signaling which programs are under active review before any report
is submitted (see [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md)).

What is public is the process above, and once a research sprint starts, a
[scope-lock](scope-lock-template.md) is completed for the selected target before deep work begins.
