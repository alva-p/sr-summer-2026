# Day 35, 2026-07-16 (Thursday)

* **Campaign day:** 35 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 5 (July 13-17) — debt accounting and integrations

## Objective

Probe the expiry-only rate staleness and the live-decimals precision base on the conversion path for any
repeatable, no-cost angle an unprivileged actor could drive inside an unexpired-but-stale window. If none
holds, record it as reviewed and move to the remaining Week 5 angle: the fee-handler interaction in the
aggregate, where fees owed are subtracted before the per-share division.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The freshness model on the permissionless synchronous mint path: how the manual per-asset rate's staleness
gate compares to the dedicated share-price staleness gate that sits on the *same* call, and whether an
unprivileged actor can drive a profitable path inside an unexpired-but-stale rate window. Also the live
external decimals read that builds the conversion's precision base.

## Activities

* Traced the permissionless synchronous mint entrypoint end to end and confirmed the asset-amount to value
  conversion happens *live* at call time using the current manual per-asset rate, while the per-share price
  it then divides by is the pushed snapshot studied on Day 34. So the two inputs to one mint have different
  freshness origins: one live, one snapshot.
* Contrasted the two freshness gates on that single call. The snapshot share price is checked against a
  configurable rolling max-age (which the operator can also disable outright), whereas the per-asset rate
  is checked only against an absolute, operator-set expiry with no rolling max-age and no deviation bound.
  The two inputs to the same mint are held to different standards, and the rate's is the weaker, age-only
  one.
* Examined the live external decimals read that forms the conversion's precision base and confirmed the
  asset set is operator-whitelisted, so an unprivileged caller cannot point that read at an
  attacker-controlled token.
* Checked the exit leg: the value to asset conversion on redemption crosses the *same* manual rate, so a
  same-asset deposit-then-redeem round trip cancels the rate and yields no gain from staleness alone. Any
  profit would need a cross-asset path plus a deviation large enough to clear entrance and exit fees.

## Tests / experiments

* None built. Reading and tracing pass; the deliverable was the resolution of the Day 34 open question,
  not a committed property. The suite was not touched and stays at its prior state.

## Hypotheses generated

* No new hypothesis with demonstrated impact. Reconfirmed the recorded candidate (age-only staleness on the
  manual rate) and sharpened it with the asymmetry against the share-price staleness gate that lives on the
  same permissionless call. Recorded generically in the private workspace.

## Hypotheses discarded

* The expiry-only rate staleness as an unprivileged, no-cost angle: closed as reviewed. No driver. An
  unprivileged actor cannot set the rate or its expiry, cannot force the rate to go stale, and can only
  react to staleness the trusted operator allowed; the whole valuation is a manual push where expiry is a
  liveness backstop, so rate accuracy is a trust assumption outside the untrusted-actor model. Even when
  reacting, any profit is gated by needing a cross-asset path and a deviation exceeding entrance plus exit
  fees.
* The live-decimals precision base as an angle: closed the same way. The asset set is operator-whitelisted,
  so there is no unprivileged path to a token with attacker-chosen decimals.

## AI usage

* Used AI to enumerate the live consumers of the conversion helper across the deposit and redeem handlers,
  to confirm which input on the permissionless mint call is a live rate versus a pushed snapshot, and to
  locate and compare the two distinct freshness gates that sit on that same call.

## Human verification

* Re-read the permissionless mint function myself to confirm the ordering: live asset-to-value conversion
  at the current rate, then division by the snapshot share price guarded by its own max-age check. The
  whole resolution rests on the rate being validated only by an expiry there, so I confirmed that by hand
  rather than trusting the enumeration.
* Confirmed by hand that the redemption path crosses the same manual rate, so a single-asset round trip
  cannot profit from staleness alone, which is what downgrades the surface from an attacker-driven path to
  a trust assumption.

## Public learnings

* Two inputs to the same operation can be held to different freshness standards. On one permissionless
  mint, one input was guarded by a rolling max-age and the other only by an absolute, operator-set expiry
  with no deviation bound. Finding the weaker gate means comparing the guards input by input, not assuming
  a call validates all of its inputs equally.
* An expiry bounds how *old* a value may be, never how *wrong* it is. A rolling max-age is also age-only,
  but it is strictly tighter than an absolute expiry that an operator can push far into the future. Neither
  is a deviation bound.
* A stale price is only an unprivileged exploit if an untrusted actor can drive it: set it, force it, or
  profit from it at no cost. When the value is an operator push and the *same* rate sits on both the entry
  and the exit leg, a same-asset round trip cancels it, and what is left is a trust assumption on the
  operator's refresh cadence, not an attacker-driven path.

## Blockers

* None.

## Next step

Move to the remaining Week 5 angle: the fee-handler interaction in the aggregate, where fees owed are
subtracted from the total positions value before the per-share division. Check the subtraction's
underflow and revert behavior at the boundary where fees owed approach total value, and whether the
dynamic-fee settlement that sets fees-owed can be influenced or ordered within the same update to distort
the per-share result an unprivileged actor then consumes.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes a generic reading pass over
      a permissionless mint path, comparing two freshness gates and a round-trip conversion in generic
      terms, with no target name, contract identifier, or target-specific finding or exploit detail.
