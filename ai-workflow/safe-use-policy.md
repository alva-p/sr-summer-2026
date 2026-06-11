# Safe Use Policy: AI Tools During Research

This policy governs what can and cannot be shared with AI tools (chat assistants, coding agents,
etc.) during SR Summer 2026 research. It complements
[SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

## Hard rule

> **A complete, active vulnerability, root cause + trigger conditions + impact, tied to a specific
> in-scope contract, is never submitted to a public AI service.**

This applies regardless of the tool's privacy policy. Treat any cloud AI service as a third party
that could, in principle, retain or expose what you send it.

## What's generally safe to share

* Public documentation, whitepapers, READMEs.
* Generic, anonymized code patterns ("a vault that calculates shares like this, what could go
  wrong in general?").
* Your own test code / harness scaffolding (without the specific exploit logic that completes it).
* General questions about a vulnerability *class* (e.g., "what are common rounding-error patterns in
  ERC4626-like vaults?").
* Draft report text **after** removing or generalizing identifying details, if you're using AI as a
  triager on wording/structure rather than substance.

## What requires care or should be avoided

* Pasting full contracts from a target whose program has a strict "don't share code externally"
  clause, check the program's rules first.
* Sharing a hypothesis that, combined with the contract code, fully describes an exploitable issue.
* Sharing draft reports that contain the full root cause + PoC + impact for an undisclosed finding.

## Practical pattern

1. Do the specific, sensitive analysis yourself, locally, in the private workspace.
2. When you want AI input, **abstract the question**: strip identifying names/addresses, generalize
   the mechanism, ask about the *pattern* not the *instance*.
3. If a question can't be abstracted without losing its meaning, don't ask it: that's a signal it's
   too close to the actual finding.
4. Log notable AI interactions (useful or not) in
   [evaluation.md](evaluation.md), without reproducing sensitive prompts.

## Local vs. cloud tools

Where practical, prefer local/offline tools (static analyzers, local linters, local LLMs) for
anything closer to the "sensitive" end of the spectrum. Cloud AI assistants are best used for the
**Spec**, general **Invariant**/**Adversary** brainstorming, test scaffolding, and report wording:
the stages where information can be kept generic.
