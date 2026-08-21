# Qwen3.8 recurrent context reduction v0 — results

Date: 2026-08-20

Status: **completed; positive local mechanical recurrence, acquisition/reopen behavior only**

## Executive result

The same pressure-triggered, oldest-first, positive-savings receipt rule restored the frozen response reserve at every delivery boundary where the experiment was authorized to apply it.

Both starting pending results crossed into a new model decision. After measured calls began, four further result-delivery packets became too large; the unchanged rule treated all four successfully. Each seed therefore received three exact results across model boundaries: its frozen pending result plus the results of calls 1 and 2.

The continuation did not produce construction. All six actions were admitted acquisitions: four exact reopens of demoted results and two target reads. Neither candidate changed, and there was no mutation or submission. The call-3 results were executed and custodied but were not delivered because the frozen three-call-per-seed limit had been reached.

This supports a narrow mechanism-level result:

> On these two trajectories, pressure-triggered minimum-necessary demotion of older exact-backed results was recurrently capable of admitting newly requested exact information while preserving the 4,096-token response reserve. It did not turn the resulting opportunity into artifact action during the bounded continuation.

It does not establish a general context manager, long-run stability, semantic expendability of old information, or that further acquisition was unnecessary.

## Capacity result

The limit was 25,088 tokens with 4,096 reserved, so a request had to remain at or below 20,992 prompt tokens.

| Seed and boundary | Untreated prompt | Untreated headroom | Treated prompt | Treated headroom | Tokens recovered | New demotions | Disposition |
|---|---:|---:|---:|---:|---:|---:|---|
| 42, frozen pending `R030` | 23,353 | -2,361 | 20,355 | +637 | 2,998 | 2 | delivered to call 1 |
| 42, after call 1 | 22,462 | -1,470 | 19,928 | +1,064 | 2,534 | 2 | delivered to call 2 |
| 42, after call 2 | 22,443 | -1,451 | 20,894 | +98 | 1,549 | 1 | delivered to call 3 |
| 42, after call 3 | 22,514 | -1,522 | — | — | — | — | result custodied; treatment not attempted at call limit |
| 314159, frozen pending `R032` | 21,521 | -529 | 19,775 | +1,217 | 1,746 | 1 | delivered to call 1 |
| 314159, after call 1 | 21,236 | -244 | 19,992 | +1,000 | 1,244 | 1 | delivered to call 2 |
| 314159, after call 2 | 21,612 | -620 | 19,086 | +1,906 | 2,526 | 2 | delivered to call 3 |
| 314159, after call 3 | 21,193 | -201 | — | — | — | — | result custodied; treatment not attempted at call limit |

Across the four measured post-call treatments, six result bodies were replaced by receipts and 7,853 prompt tokens were recovered. Including the two frozen starting treatments, nine substitutions recovered 12,597 tokens.

The two untreated call-3 prospective packets are not policy failures. The frozen endpoint prohibited another delivery attempt, so whether the same rule could have admitted those results remains untested.

## Behavior by seed

| Seed | Call 1 | Call 2 | Call 3 | Mutation/check/submit | Candidate effect |
|---|---|---|---|---|---|
| 42 | exact reopen: source-navigation `RESULTS.md` | duplicate exact read of still-available `R030` | exact reopen: source-navigation `DIRECT_TRANSCRIPT_AUDIT.md` | 0 / unavailable / 0 | unchanged |
| 314159 | exact adjacent target read, lines 890–970 after delivered `R032` lines 864–889 | exact reopen: source-navigation `DIRECT_TRANSCRIPT_AUDIT.md` | exact reopen: source-navigation `RESULTS.md` | 0 / unavailable / 0 | unchanged |

All raw assistant outputs were bare schema-valid JSON. All six operations were admitted, and all six literal results were placed in exact backing custody. Four measured-call results crossed into a later invocation; the two final results did not.

The inherited action schema exposed `patch`, `replace_file`, and `submit`, but no explicit check operation. Accordingly, zero checks is an action-surface qualification rather than evidence that the model declined an available check.

The four exact reopens are behaviorally important. Every reopen targeted information that the policy had represented by a receipt. Exact recoverability was therefore used by the model, not merely demonstrated offline. At the same time, the 42 trajectory's duplicate `R030` read shows that residency alone did not prevent redundant acquisition.

## Artifact and evaluator result

Initial and terminal candidate IDs were identical in both cells:

`19296f821cc2bf7e32384ec88080ba49aedc4afe1f1f9961c31d57c2e1dc24fd`

No external evaluator was run. There was no candidate transition to evaluate, and evaluator output was not part of the frozen primary question. No evaluator or investigator judgment was fed back to the model.

## Cost and cache

| Seed | Prompt tokens | Cached prompt | Uncached prompt | Completion | Serialized total | HTTP time |
|---|---:|---:|---:|---:|---:|---:|
| 42 | 61,177 | 3,150 | 58,027 | 101 | 61,278 | 79.764 s |
| 314159 | 58,853 | 4,725 | 54,128 | 120 | 58,973 | 75.482 s |
| **Total** | **120,030** | **7,875** | **112,155** | **221** | **120,251** | **155.246 s** |

Only 6.56% of prompt tokens were reported cached. After the cold first call, each request reported only 1,575 cached tokens. This is descriptive but consistent with the expected cost of repeatedly rewriting old prefix content: the context-space benefit came with substantial re-prefill and latency.

## Custody and execution

- Inference commit: `50e72ba467388bd4c116a5f2b4e5b38f80e820d3`.
- Frozen source-lock SHA-256: `7384b2792a98401e1510294f1f0d203f7cf4f39fe214cc3e8d97c4eff6920f5f`.
- Run: `runs/2026-08-20-sealed-run-v1`.
- Calls: 6 of 6 authorized; one attempt per seed; zero retries.
- Main-model GPU offload: 66/66 before and after calls.
- Runtime integrity failures: none.
- Measured replay: 6/6 request/response records and exact result backings passed.
- Server shutdown: passed; port closed; llama process absent; GPU returned to 319 MiB used.

## Interpretation

Strongest supported interpretation:

The same simple mechanical rule can do more than rescue one blocked observation. It resolved two successive post-call delivery pressures per seed while leaving the current requested result exact and maintaining the fixed response reserve. Exact receipts also supported model-initiated fault-in.

Strongest interpretation weakened by the result:

Physical context capacity was not the sole reason construction had not begun. Both trajectories received multiple additional decision opportunities and still selected acquisition or reopen actions. Because there is no matched untreated behavioral continuation and the new reads may have been legitimate, the run does not distinguish information demand from acquisition-stopping or action-commitment weakness.

Remaining uncertainty:

- whether recurrence remains stable beyond two post-call reductions per seed;
- whether repeated fault-in eventually thrashes, converges, or enables construction;
- whether a less prefix-destructive representation can retain the capacity benefit with better cache reuse;
- which old exact objects can be demoted without inducing unnecessary reopens; and
- whether a longer trajectory would mutate, check through another surface, or submit.

No general architecture is promoted, and no successor is selected or authorized by this result.
