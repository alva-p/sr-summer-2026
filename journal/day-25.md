# Day 25, 2026-07-04 (Saturday)

* **Campaign day:** 25 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Optional weekend session (between Week 3 and Week 4)

## Objective

Optional Saturday bridge session. Two tasks:
1. Prepare the sanitized Week 3 public learning for posting. Week 3 closed with zero community
   contributions, and the retrospective flagged a generic testing takeaway as queued content, so
   the goal today is to turn it into a post-ready, disclosure-safe draft.
2. Firm up the Week 4 opening tasks from the Week 3 retrospective so Monday starts on
   implementation instead of re-planning.

## Time

* **Planned:** ~1h (optional session)
* **Actual:** ~1h

## Area studied

No new contract surface (weekend bridge day, the target repo is not touched on bridge days).
Community content preparation and Week 4 task scoping from the existing Week 3 notes.

## Activities

* Reviewed the Week 3 retrospective and reworked its "public learning to share" paragraph into a
  sanitized, post-ready form (see Public learnings). Confirmed it carries no target name, no
  in-scope contract or function reference, and no hypothesis content.
* Scoped the two Week 3 coverage-gap tests as the concrete first Monday task: a rounding-direction
  fuzz property for the asset-amount conversion, and a composed round-trip (value to asset to
  value) no-leak fuzz property. Both are pure-function tests, so they need no new handler wiring
  or protocol state.
* Ordered the Week 4 focus behind the gap-closers: model the fee-recipient value-owed accounting
  that the exit fee feeds into as invariants (does the sum of recipient claims ever exceed total
  fees accrued, can a recipient be owed or claim more than its share, and how does this interact
  with the mid-flight recipient-change edge case from Week 2).
* Ran the repo safety check before treating the post draft as ready.

## Tests / experiments

* None. Weekend prep session; no fuzz or invariant runs and no target source touched.

## Hypotheses generated

* None new.

## Hypotheses discarded

* None new.

## AI usage

* Reformatted the Week 3 retrospective's public-learning paragraph into a concise post-ready draft.
* Cross-checked the draft against the disclosure policy's "never published" list.
* Drafted this journal entry.

## Human verification

* Re-read the drafted post line by line for target name, in-scope function references, and
  hypothesis content: none present. The takeaway is a generic testing principle that would hold for
  any protocol.
* Confirmed the Week 4 task list matches the Week 3 retrospective's "plan for next week" and adds
  no new claim not already grounded there.
* Ran `make safety-check` and read the output before marking the post ready to publish.

## Public learnings

Prepared for posting (queued to the Monday light community slot, not auto-posted):

> Two failure modes I hit at the end of a precision/rounding study block, both about the gap
> between reasoning and coverage:
>
> 1. "We found no leak" is not a durable artifact. A refactor can silently break a property you
>    only reasoned about, with no test going red. The durable artifact is a per-property table
>    that splits what is pinned by a committed test from what still rests on an argument.
>
> 2. A committed test can be narrower than the reasoning that motivated it. A round-trip argument
>    ("both truncations together cannot leak in either direction") is easy to make on paper, but if
>    the test pins only one of the two directions, the round-trip property is still uncovered.
>
> Rule of thumb: write the test for the property the user actually experiences, not the
> intermediate step that was convenient to check.

## Blockers

* None.

## Next step

Week 4 starts Monday July 6. Objective: redemption, queues and temporal state, opening with the
fee-recipient accounting the exit fee feeds into.
* First task, close the two Week 3 coverage gaps: a rounding-direction fuzz property for the
  asset-amount conversion, and a composed round-trip (value to asset to value) no-leak fuzz
  property. Both are cheap pure-function tests.
* Then model the fee-recipient value-owed accounting as invariants (recipient claims never exceed
  total fees accrued, no recipient over-owed or over-claiming, interaction with the mid-flight
  recipient-change edge case).
* Post the prepared Week 3 learning during the week and log it in the contribution tracking.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). The community draft is a generic
      testing principle with no target-specific content.
