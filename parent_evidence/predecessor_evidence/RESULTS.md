# Results

## Disposition

The measured run is complete. The narrowest reduction rule passed both primary gates in both seeds; the more aggressive rule failed decision preservation in both seeds.

`oldest_fit_receipts_v0` replaced only the first two older result bodies that produced positive exact token savings. In both trajectories Qwen3.8 then made the exact historical acquisition, received the exact result that the historical context could not admit, and made a second valid decision. Those second decisions were additional target-region reads, not mutation, checking, or submission.

`recent2_receipts_v0` retained only the last two result messages exactly and replaced six or eight older result bodies with exact-backed receipts. It saved far more tokens, but neither trajectory reproduced the frozen historical acquisition. Both instead requested material from the same older source object that the policy had demoted. One request was the exact reopen action; the other requested only line 1 of that object. The frozen gate therefore stopped both cells before executing or delivering those divergent reads.

The strongest supported conclusion is local: replacing a small mechanically selected set of old exact-backed results can preserve the immediate useful decision and solve an authentic result-delivery capacity failure. More aggressive reduction was not behaviorally neutral, and this two-decision study did not turn the restored capacity into artifact construction.

## Historical pressure control

The historical control consumes no reconstructed model calls. Its Prompt N action is observed parent behavior; its unsent Prompt N+1 is a mechanical capacity result.

| Seed | Historical Prompt N | Headroom after 4,096 reserve | Historical action | Prompt N + exact result | Headroom after reserve |
|---|---:|---:|---|---:|---:|
| 42 | 20,966 | +26 | target lines 1–6 | 21,386 | -394 |
| 314159 | 20,013 | +979 | target region `R031` | 22,037 | -1,045 |

## Measured cells

| Seed / policy | Results replaced | Decision tokens removed | Treated Prompt N / headroom | First decision | Exact result absorbed | Prompt N+1 / headroom | Second decision |
|---|---:|---:|---:|---|---|---:|---|
| 42 / oldest-fit | 2 | 548 | 20,418 / +574 | exact historical `read_lines(1–6)` | yes, 143 bytes | 20,838 / +154 | `read_region(R030)` |
| 314159 / oldest-fit | 2 | 1,440 | 18,573 / +2,419 | exact historical `read_region(R031)` | yes, 7,454 bytes | 20,597 / +395 | `read_region(R032)` |
| 42 / recent-two | 8 | 9,236 | 11,730 / +9,262 | divergent one-line access to a demoted source result | not evaluated after gate | — | — |
| 314159 / recent-two | 6 | 6,956 | 13,057 / +7,935 | divergent exact reopen of a demoted source result | not evaluated after gate | — | — |

The two oldest-fit call-02 request hashes exactly equal their frozen prospective post-historical-result packet hashes. Provider prompt counts also equal the exact preflight counts. Thus “result absorbed” means the actual accepted result crossed a new model decision boundary with all 4,096 response tokens still reserved.

The recent-two rows are not result-delivery failures. Result absorption was deliberately not evaluated because the first decision failed the predeclared equivalence gate.

## Continuation and artifact outcome

After seeing the newly deliverable result, both oldest-fit trajectories requested a previously unread target region: `R030` for seed 42 and `R032` for seed 314159. The terminal second decisions were recorded but their results were not executed or delivered, as frozen in the two-decision/one-result design.

No cell requested or executed mutation, check, or submission. The candidate remained byte-identical at SHA-256 `899a37f188de42075d5559bcaf6ba4bea96713ba192517021dbcc533c9844387`, candidate ID `19296f821cc2bf7e32384ec88080ba49aedc4afe1f1f9961c31d57c2e1dc24fd`. No semantic evaluator was run because there was no candidate transition to evaluate; byte identity is the direct artifact result.

The full structural outline remained resident in every condition. This study neither demoted nor tested reopening of the outline.

## Fault-in audit qualification

The first frozen reducer reported zero reopens because it counted only exact reopens occurring as terminal second actions. Direct audit found two first-action accesses to a demoted object in the aggressive-policy cells:

- seed 42 requested line 1 of the demoted `large-world-source-navigation-v0/.../RESULTS.md` object;
- seed 314159 requested the exact original full-read action for that same demoted object.

The supplemental audited reducer records one exact reopen request and one alternate access to the same demoted object. It does not reclassify either first decision as equivalent to the historical target acquisition. Neither request was executed because the frozen decision-preservation gate had already failed.

## Calls, tokens, and runtime

- Measured calls: 6 of 8 authorized; one attempt per cell; zero retries.
- Prompt tokens: 105,213, of which 43,708 were reported cached.
- Completion tokens: 168.
- Total provider tokens: 105,381.
- Summed HTTP duration: 87.313 seconds.
- Recorded runtime lifecycle: 127.935 seconds.
- Every response returned HTTP 200 with `finish_reason: stop` and one schema-valid action.
- Exact model: `Qwen3.8-27B-AD-IQ2_S.gguf`, 11,141,912,032 bytes, SHA-256 `d416fa422c9035605c778f60d90a94b288c38b4f9ec2126b58ef938ce8d5f716`.
- Exact llama.cpp build: `b10434-7e4c0a968`; executable SHA-256 `5f1f831bc21dcbff4ca40e05cb59dbcbc0802d20b2046540bbbf3bd45cd61610`.
- Main-model offload was 66/66 before measured calls. Port 8080 was closed and GPU memory returned from 11,286 MiB after load to the 319 MiB baseline after shutdown.

## Replay and custody

Measured replay passed: all six request/response pairs match their HTTP receipts, declared and observed call counts are both six, and candidate receipts are consistent. The frozen offline verifier also passed after the run but before result documents changed: 18/18 focused tests, exact preflight replay, JSON audit, and read-only donor checks.

The run supplements the frozen reducer with [AUDITED_ANALYSIS.json](runs/2026-08-20-sealed-run-v0/analysis/AUDITED_ANALYSIS.json) and records aggregate custody in [METRICS.json](runs/2026-08-20-sealed-run-v0/analysis/METRICS.json). Every measured artifact, archived runtime log, analysis receipt, and replay receipt is covered by the run seal.

## Interpretation boundary

Supported:

- The minimal oldest-first exact-backed receipt rule preserved the exact useful next decision and admitted its exact result in both observed seeds at these two pressure boundaries.
- The aggressive recent-two rule altered immediate behavior in both seeds and caused both actors to seek a demoted old source object.
- Restored result-delivery capacity did not yield artifact action within the one allowed follow-up decision.

Not supported:

- a general context manager;
- a general optimal retention window;
- semantic summaries or model-controlled eviction;
- the claim that old exact content is dispensable;
- the claim that physical headroom alone solves acquisition stopping or action commitment.

The frozen forecast category realized was “decision preservation is mixed in another pattern and no cell requests mutation or submission” (15% prior): preservation separated completely by policy rather than by seed.

No successor was selected or run.
