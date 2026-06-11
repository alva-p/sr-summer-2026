# Learning Notes: Cross-Chain Security

Working notes on cross-chain message validation and bridge/CCIP-style integrations. Priority area 7
in the [README specialization](../README.md#specialization), and the basis for a possible cross-chain
stretch goal. General learnings only.

## Topics to cover

- [ ] Message validation: sender/receiver authentication, source chain verification.
- [ ] Replay protection and message ordering guarantees (or lack thereof).
- [ ] Rate limiting patterns (e.g. CCIP token pool rate limiters) and their failure modes.
- [ ] Trust assumptions in relayers/oracles/DONs that carry messages between chains.
- [ ] Token pool accounting: minting/burning vs. lock/unlock, and consistency across chains.
- [ ] Handling of failed/stuck messages and manual execution paths.
- [ ] Receiver contract patterns: gas limits, reentrancy from cross-chain callbacks, malformed
      payload handling.

## General learnings

(Add dated, generic entries as they're learned.)

## References

(Public docs, e.g. CCIP-style documentation, bridge security frameworks, audit reports.)
