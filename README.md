# Qwen3.8 recurrent context-reduction horizon v0

This standalone repository tests whether the same deterministic, pressure-triggered receipt substitution remains useful beyond the predecessor's three-call window.

Status: **measured 24-call run complete**. The policy preserved physical operability through all authorized result-delivery boundaries, but neither trajectory converged to construction. Across two 12-call continuations it resolved 17 recurrent pressure events, in addition to the two frozen starting events, and delivered 24 exact results to later model decisions when the two predecessor-pending results are included. Both candidates remained byte-identical.

Behaviorally, all 24 decisions remained acquisition decisions: 15 exact reopens and nine other acquisitions. Seed 42 ended in a descriptive exact three-action reopen cycle repeated twice; seed 314159 showed repeated reopen churn and one apparatus-caused rejected continuation request. Neither trajectory met the narrower predeclared formal-thrash rule, mutated, or submitted.

See [RESULTS.md](RESULTS.md), [DIRECT_TRANSCRIPT_AUDIT.md](DIRECT_TRANSCRIPT_AUDIT.md), and [POSTRUN_APPARATUS_NOTE.md](POSTRUN_APPARATUS_NOTE.md).

## Fixed policy

1. Use ordinary resident chronology while the prospective next request fits with the frozen 4,096-token reserve.
2. On actual result-delivery pressure, inspect resident action/result pairs oldest first.
3. Skip existing receipts.
4. Replace a full exact-backed result body only when exact tokenization proves positive savings.
5. Stop as soon as the prospective request fits.
6. Keep the just-requested result exact during that delivery cycle.

There is no semantic relevance score, summary, fixed recent window, outline demotion, background rewriting, context enlargement, or reserve reduction.

## Measured run

- Run: `runs/2026-08-20-sealed-horizon-run-v0`
- Frozen inference commit: `ca07e84cde79c7db147ba4cc43f06133fc6d353e`
- Calls: 12 per seed, 24 total
- Attempts: one per seed
- Retries: zero
- Result: recurrent capacity preservation; continued acquisition/reopen behavior; no artifact action

The run contains exact requests, provider responses, parsed actions, literal results, exact backing objects, capacity and projection receipts, candidate identities, runtime custody/logs, deterministic analysis, replay, and a content seal.

## Offline verification

```powershell
python -m apparatus.replay --run-root runs/2026-08-20-sealed-horizon-run-v0 --output runs/2026-08-20-sealed-horizon-run-v0/replay/REPLAY.json
python -m apparatus.analyze --run-root runs/2026-08-20-sealed-horizon-run-v0
python -m apparatus.seal --verify runs/2026-08-20-sealed-horizon-run-v0
python -m postrun.verify --run-root runs/2026-08-20-sealed-horizon-run-v0
```

Measured inference is no longer authorized by repository state. The exact user approval used for this run is preserved under `model/AUTHORIZATION.json`.

## Qualifications

The frozen candidate `read_lines` adapter emitted an unusable placeholder continuation cursor after a truncated read, despite the action description promising a valid version-bound cursor. Seed 314159 spent call 5 requesting it and received an `invalid_or_stale_cursor` rejection, then recovered with explicit line ranges. This weakens that seed's behavioral horizon but does not alter the measured capacity receipts.

The standalone source surface includes candidate operations, historical exact reopens, and exact reads of four materialized governing documents. It does not reproduce the complete donor Git index/search/history surface. No measured request crossed that unqualified surface. The inherited action schema exposes mutation and submission but no explicit check action.

## Provenance

- Direct predecessor: `ScrappyTom/qwen38-recurrent-context-reduction-v0@9a42b85b4d9fd25bd873d45c08a403c2ca1ff96e`
- Predecessor inference commit: `50e72ba467388bd4c116a5f2b4e5b38f80e820d3`
- Parent evidence: `ScrappyTom/custody-cards-experimental-workbench@40f9afdde9628e4fd5dbd8d18a6fcf85bdf9d820`
- Frozen task source: `f8c93e5ad33c8dd235c418df6561ba022d9077fb`

All imported files retain original and copied hashes in `provenance/PREDECESSOR_MATERIALIZATION_RECEIPT.json`. Neither the predecessor checkout nor Custody Cards was modified.
