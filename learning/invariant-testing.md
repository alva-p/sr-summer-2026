# Learning Notes: Invariant & Fuzz Testing

Working notes on invariant-based testing techniques (Foundry invariant tests, handlers, ghost
variables), priority area 10 in the [README specialization](../README.md#specialization). General
learnings only; specific invariants for a target go in
[methodology/invariant-template.md](../methodology/invariant-template.md) copies in the private
workspace.

## Topics to cover

- [ ] Foundry invariant testing basics: `targetContract`, `targetSelector`, handler-based fuzzing.
- [ ] Designing handlers that model realistic actor behavior (bounding inputs to valid ranges).
- [ ] Ghost variables for tracking cumulative values (e.g. total deposited, total fees accrued).
- [ ] Shrinking and reproducing failures (`failed()` / replay seeds).
- [ ] Triage framework for invariant failures: test bug vs. wrong assumption vs. documented
      behavior vs. real bug (see [methodology/invariant-template.md](../methodology/invariant-template.md)).
- [ ] Stateful vs. stateless fuzzing, when each is appropriate.
- [ ] Combining invariant testing with differential testing against a reference implementation.

## General learnings

(Add dated, generic entries as they're learned, e.g. "2026-06-29, bounding handler inputs to
realistic ranges found more meaningful violations than unbounded fuzzing.")

## References

(Foundry book sections, public invariant-testing writeups, example repos.)
