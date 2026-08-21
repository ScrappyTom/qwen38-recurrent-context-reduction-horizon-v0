# Qwen3.8 recurrent context reduction v0

This standalone repository tests whether the same deterministic, pressure-triggered receipt substitution can keep admitting exact observations across successive context-pressure events.

Status: **measured run complete**. At four of four authorized post-call pressure events, the oldest-first positive-savings rule restored the frozen 4,096-token response reserve. Both seeds completed three new calls. The models used the resulting opportunity for four exact reopens and two target reads; neither candidate mutated or submitted.

See [RESULTS.md](RESULTS.md) and [DIRECT_TRANSCRIPT_AUDIT.md](DIRECT_TRANSCRIPT_AUDIT.md).

## Policy

1. Use ordinary resident chronology while the prospective next request fits with the frozen reserve.
2. On actual result-delivery pressure, inspect resident action/result pairs oldest first.
3. Skip existing receipts.
4. Replace a full result body only when the exact tokenizer confirms positive savings.
5. Stop rewriting as soon as the prospective packet fits.
6. Keep the just-requested result exact during that pressure cycle.

There is no semantic relevance score, summary, fixed recent window, outline demotion, background compaction, or general context manager.

## Runs

- `runs/2026-08-20-sealed-run-v0`: preserved zero-call launcher integrity failure at commit `587850ca`; no model inference.
- `runs/2026-08-20-sealed-run-v1`: completed authorized six-call measured run at commit `50e72ba`.

The measured run contains exact requests, provider responses, actions, literal results, external backing objects, capacity/projection receipts, candidate identities, runtime custody and logs, deterministic analysis, and replay.

## Reproduce offline verification

```powershell
python -m apparatus.replay --run-root runs/2026-08-20-sealed-run-v1 --output runs/2026-08-20-sealed-run-v1/replay/REPLAY.json
python -m apparatus.analyze --run-root runs/2026-08-20-sealed-run-v1
python -m apparatus.seal --verify runs/2026-08-20-sealed-run-v1
python -m postrun.verify --run-root runs/2026-08-20-sealed-run-v1
```

Measured inference is not authorized by repository state. `AUTHORIZATION_REQUEST.json` remains the frozen request artifact, while the exact approval used for execution is preserved under the measured run's `model/AUTHORIZATION.json`.

## Apparatus bound

Historical exact reopens, candidate operations, and novel exact reads of the four materialized governing documents were executable. The complete donor Git search/list/history surface was not copied. Any novel request requiring that surface would have stopped the whole run as an apparatus invariant endpoint; none occurred. The inherited schema exposed mutation and submission but no explicit check action.

## Provenance

- Predecessor: `ScrappyTom/qwen38-context-reduction-pressure-boundary-v0@ab0e21b201d04521a43f83c223a364bca35a7b86`
- Parent result: `ScrappyTom/custody-cards-experimental-workbench@40f9afdde9628e4fd5dbd8d18a6fcf85bdf9d820`
- Frozen task source: `f8c93e5ad33c8dd235c418df6561ba022d9077fb`

All imported files retain original and copied hashes in `provenance/PREDECESSOR_MATERIALIZATION_RECEIPT.json`. Neither the predecessor nor Custody Cards was modified by this experiment.
