# SR Summer 2026: alvap (alva-p) 🏖️ 💻

Public tracking repository for my participation in [Immunefi SR Summer 2026](https://immunefisupport.zendesk.com/hc/en-us/articles/47558436152209-SR-Summer-2026) (June 9 – August 31, 2026).

> 🏖️💻 I'm joining @immunefi SR Summer 2026.
>
> After earning a paid finding, I'm committing to consistent EVM/DeFi hunting, stronger Foundry PoCs, and a transparent AI-assisted workflow.
>
> I'll share weekly lessons never confidential findings. #SRSummer

## Disclaimer

This repository is a **personal planning, accountability, and portfolio project**. It does **not**
contain active vulnerabilities, exploit sequences, or advice for attacking live systems. Anything
related to in-progress research on in-scope assets is kept in a local, untracked, private workspace
(see [SECURITY_AND_DISCLOSURE.md](SECURITY_AND_DISCLOSURE.md)). Content here is for educational and
methodological purposes only.

## What this is

This repo is where I plan, track, and publish my work as a security researcher during SR Summer 2026.
It serves four purposes at once:

1. **Personal planning and accountability system** — daily journal, weekly retrospectives, and a
   campaign dashboard that I update as I go.
2. **Public progress log** — an honest record of what I studied, tested, got wrong, and learned,
   without revealing anything confidential.
3. **Technical portfolio** — case studies, templates, and tools that show how I work, for people
   evaluating me for Web3 security roles.
4. **Reusable base for other researchers** — every template here is sanitized and empty by default,
   so anyone can fork this structure for their own bounty/research workflow.

## Who I am

I'm **alvap**, an advanced Information Systems Engineering student and Web3 security
researcher. Background: Solidity, Foundry, OpenZeppelin, Ethers.js, smart contracts, DeFi protocols,
Chainlink/CCIP, unit testing, fuzzing and invariant testing. I've done bug bounty work on Immunefi and
HackenProof, prepared PoCs and reports, and have at least one rewarded finding on Immunefi.

## Specialization

> **EVM Security Researcher focused on protocol accounting, DeFi integrations, invariant-based
> testing and cross-chain security.**

Priority areas:

1. Share and vault accounting
2. Deposits, withdrawals and redemption queues
3. Fees, interest and debt accounting
4. Rounding and precision errors
5. Lending and liquidation flows
6. Oracle and external integration assumptions
7. Cross-chain message validation
8. Access control and privileged operations
9. State-machine inconsistencies
10. Invariant-based security testing

## Goals for SR Summer 2026

* Improve my hunting methodology and consistency.
* Write higher-quality reports.
* Learn protocol accounting in depth.
* Go deeper on lending and cross-chain security.
* Build a realistic, transparent AI-assisted research workflow.
* Share useful learnings with the community.
* Meet other researchers and build reputation.
* Work toward Web3 security job opportunities.

I'm aiming for **two or more confirmed/paid reports** during the campaign — but that's a stretch
goal, not a guarantee. Success is also measured by process quality, technical depth, tests written,
hypotheses correctly ruled out, reporting improvements, public contributions, consistency, and
professional relationships built. See [methodology/](methodology/) for how each of these is tracked.

## SR Summer 2026 recognition focus

This project is organized to produce real evidence for these SR Summer categories:

* **Most Consistent Hunter** — sustained activity all campaign long, even on weeks without findings.
  Evidence: [journal/](journal/), [data/daily-metrics.csv](data/daily-metrics.csv).
* **Best AI-Assisted Workflow** — a practical, honest workflow where AI helps without replacing human
  verification. See [ai-workflow/](ai-workflow/).
* **Best Community Contributor** — public learnings, tools, templates and retrospectives, plus real
  interaction (not just broadcasting) on Twitter/X and Discord. See [community/](community/).

## Methodology

The research workflow follows this pipeline (see [methodology/](methodology/) for the templates
behind each step):

```text
Program Selection
    ↓
Scope Lock
    ↓
Architecture Mapping
    ↓
Trust Assumptions
    ↓
Invariants
    ↓
Adversarial Scenarios
    ↓
Manual Review
    ↓
Tests / Fuzzing / Invariant Testing
    ↓
Hypothesis Validation
    ↓
PoC
    ↓
Severity and Scope Validation
    ↓
Report Quality Gate
    ↓
Immunefi Studio Review
    ↓
Submission
    ↓
Sanitized Retrospective
```

Standard weekly cadence (when the [ROADMAP](ROADMAP.md) doesn't say otherwise):

| Day | Focus |
|---|---|
| Monday | Planning, scope, architecture, documentation |
| Tuesday | Manual review, critical flows, entry points |
| Wednesday | Invariants, tests, fuzzing, state machines |
| Thursday | Adversarial scenarios, hypothesis validation, PoCs |
| Friday | Quality review, metrics, retrospective, public contribution, next week's plan |

## AI-assisted workflow

> **Spec → Invariant → Adversary → PoC → Report**

AI is used as a thinking and review aid — **never** as a replacement for human verification, and
**never** fed an active vulnerability. Full policy and prompts: [ai-workflow/](ai-workflow/).

| Stage | What AI can help with |
|---|---|
| Spec | Summarize public docs, enumerate components, propose diagrams, compare spec vs. implementation |
| Invariant | Propose economic, authorization, state, temporal and cross-chain invariants |
| Adversary | Turn invariants into general adversarial questions |
| PoC | Generate test skeletons — always run and verified manually |
| Report | Act as a skeptical triager: flag unproven assumptions, irreproducible steps, exaggerated impact, scope issues |

## What's public vs. what's never published

### Public

Methodology, roadmap, aggregated metrics, general learnings, empty templates, educational examples,
sanitized retrospectives, resources, reusable tools, public summaries.

### Never published

Cloned targets, target-specific notes, hypotheses, PoCs, reports, evidence, screenshots, tool output,
Immunefi Studio information, active vulnerabilities, exploit sequences, secrets/keys.

Full rules: [SECURITY_AND_DISCLOSURE.md](SECURITY_AND_DISCLOSURE.md). A local, conservative
[safety check](scripts/safety_check.py) (`make safety-check`) scans tracked files for obvious
red flags before anything is published.

## Schedule

Full schedule (June 10 – August 31, 2026, ~2h/day Monday-Friday): [ROADMAP.md](ROADMAP.md).

## Dashboard & metrics

* Live status: run `make status` (see [scripts/campaign_status.py](scripts/campaign_status.py)).
* Curated snapshot: [dashboard/status.md](dashboard/status.md).
* Daily metrics: [data/daily-metrics.csv](data/daily-metrics.csv).
* Weekly metrics: [data/weekly-metrics.csv](data/weekly-metrics.csv).
* Bounty/program comparison: [data/bounty-comparison.csv](data/bounty-comparison.csv).

Metrics are honest, not a "hours worked" competition: hypotheses ruled out and learnings count as much
as findings. See [methodology/weekly-retrospective-template.md](methodology/weekly-retrospective-template.md).

## Reusing this repo

Everything under `methodology/`, `ai-workflow/`, `learning/`, `community/` and `portfolio/` is written
to be forkable: empty templates, no project-specific information. If you're a researcher setting up
your own accountability system, feel free to copy this structure. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Local commands

```bash
make help            # list available commands
make new-day         # create today's journal entry from the template
make status          # compute campaign status (day, week, progress)
make weekly-summary  # generate a sanitized weekly summary from daily metrics
make safety-check    # scan tracked files for confidentiality red flags
```

## Repository structure

```text
sr-summer-2026/
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── SECURITY_AND_DISCLOSURE.md
├── LICENSE
├── config/campaign.yaml
├── dashboard/status.md
├── journal/                 # daily entries + weekly retrospectives
├── methodology/              # research process templates
├── ai-workflow/              # AI-assisted workflow docs and policy
├── learning/                 # study notes on accounting, lending, cross-chain, etc.
├── community/                # content plan, post templates, contribution log
├── portfolio/                # case studies and final retrospective
├── data/                      # CSV metrics
└── scripts/                   # local automation (Python 3, stdlib only)
```
