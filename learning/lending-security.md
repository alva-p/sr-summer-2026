# Learning Notes: Lending & Liquidation Security

Working notes on lending protocols, collateral/debt accounting, and liquidations. Priority area 5
in the [README specialization](../README.md#specialization). General learnings only.

## Topics to cover

- [ ] Collateral factors / loan-to-value (LTV) and liquidation thresholds.
- [ ] Health factor calculation and edge cases (zero collateral, zero debt, dust amounts).
- [ ] Liquidation mechanics: full vs. partial liquidation, liquidation incentives/bonuses.
- [ ] Interest rate models (linear, jump-rate, kinked curves) and accrual timing.
- [ ] Credit delegation / intermediate vault patterns used by some lending protocols.
- [ ] Oracle dependency for collateral valuation: staleness, manipulation resistance,
      circuit breakers.
- [ ] Bad debt handling and socialization mechanisms.
- [ ] Cross-protocol composition risk (e.g. a vault that itself deposits into another lending
      market).

## General learnings

(Add dated, generic entries as they're learned.)

## References

(Public docs, audits, articles.)
