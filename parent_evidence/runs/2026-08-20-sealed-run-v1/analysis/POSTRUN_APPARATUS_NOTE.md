# Post-run apparatus note

## Measured execution

Run `2026-08-20-sealed-run-v1` executed against frozen inference commit `50e72ba467388bd4c116a5f2b4e5b38f80e820d3` and source-lock SHA-256 `7384b2792a98401e1510294f1f0d203f7cf4f39fe214cc3e8d97c4eff6920f5f`.

The exact 11,141,912,032-byte `Qwen3.8-27B-AD-IQ2_S.gguf` file and llama.cpp build `b10434-7e4c0a968` passed the frozen SHA-256 checks. The runtime used the inherited 25,088-token observed context, q8 KV, reasoning off, 4,096-token maximum completion/reserve, frozen sampler, and seed-specific seed values. Main-model offload was 66/66 layers before and after measured calls.

Exactly six `/v1/chat/completions` calls ran: three for seed 42 followed by three for seed 314159. There was one attempt per seed and zero retries. No source-surface invariant was reached, no action was rejected, and no runtime or serialization failure occurred.

The server stopped normally. Port 18080 was closed before and after execution, no llama process remained, and GPU usage returned from 11,286 MiB after load to the same 319 MiB used state recorded before launch.

## Prior zero-call launch

The earlier authorized attempt at commit `587850ca` remains preserved separately as `runs/2026-08-20-sealed-run-v0`. It made zero chat-completion calls and exposed only the launcher-owned dirty-tree ordering defect. It is not counted as a model attempt or experimental cell.

The correction at `50e72ba` changed launcher staging hygiene and clean-gate order only. It did not change model-visible packets, treatment policy, budgets, response reserve, tools, seeds, or schedule.

## Action-surface qualification

All six measured requests stayed within the qualified standalone surface. Historical reopens, candidate reads and mutations, submission, and exact reads of the four materialized governing documents were available. The run did not request unmaterialized repository list/search/history operations.

The inherited schema did not expose an explicit check action, although it exposed mutation and submission. Therefore the absence of checks cannot be interpreted as refusal to check.

## Token and cache qualification

Provider usage reports total 120,030 prompt tokens, 221 completion tokens, and 120,251 serialized tokens. Only 7,875 prompt tokens were reported cached. Because each pressure response rewrites an older prompt position, latency and cache differences are descriptive and cannot be attributed solely to token count.

## Post-run processing

No additional model or GPU call was made during analysis. `apparatus.analyze` reduces the raw measured records mechanically. Measured replay checks all request/response hashes, exact result backing, terminal candidates, and declared call count. The sealed run includes raw provider records, exact requests/responses/actions/results, capacity and projection receipts, candidates, runtime logs/custody, analysis, and replay.

The frozen source lock is verified against Git commit `50e72ba`. The five predeclared report files—`README.md`, `RESULTS.md`, `DIRECT_TRANSCRIPT_AUDIT.md`, `POSTRUN_APPARATUS_NOTE.md`, and `PARENT_PROJECT_IMPLICATIONS.md`—are the only frozen paths allowed to differ after inference.
