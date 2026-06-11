# Learning Notes: Protocol Accounting

Working notes on share/vault accounting, valuation, fees, and rounding — priority areas 1-4 in the
[README specialization](../README.md#specialization). This file accumulates **general** learnings
(concepts, patterns, references) — not target-specific findings.

## Topics to cover

- [ ] Share-based accounting (ERC4626 and ERC4626-like vaults): `convertToShares` /
      `convertToAssets`, share price, inflation/donation attacks.
- [ ] Deposit/mint vs. withdraw/redeem semantics and rounding direction (round in favor of the
      protocol vs. the user).
- [ ] Fee accrual mechanisms: per-block/per-second streaming fees, high-water marks, performance
      fees.
- [ ] Valuation: how NAV/total assets is computed when assets include external positions
      (lending positions, LP tokens, debt).
- [ ] Debt/credit tracking: signed vs. unsigned accounting, interest accrual models
      (linear vs. compounding).
- [ ] Redemption queues: request/claim separation, partial fills, pricing at request time vs.
      settlement time.
- [ ] Precision/decimals handling across tokens with different decimals.

## General learnings

(Add dated, generic entries as they're learned — e.g. "2026-06-22 — rounding direction in
`convertToShares` matters most at the boundary between zero and one share; worth checking on every
new vault.")

## References

(Links to public documentation, audit reports, articles, and educational resources used. Add as
they're found — e.g. ERC-4626 spec, OpenZeppelin vault implementations, public post-mortems.)
