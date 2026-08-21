# Post-run apparatus note

## Measured execution

Run `2026-08-20-sealed-horizon-run-v0` executed against frozen commit `ca07e84cde79c7db147ba4cc43f06133fc6d353e` and source-lock SHA-256 `fba8c448df959e03b50e13a03b429a582a2a9c4d2cf9df5f10b1b262f8794b2c`.

The exact 11,141,912,032-byte `Qwen3.8-27B-AD-IQ2_S.gguf` and llama.cpp build `b10434-7e4c0a968` passed their frozen SHA-256 checks. Runtime settings matched the lock: observed context 25,088; q8 KV; reasoning off; 4,096-token completion maximum/reserve; frozen sampler; seeds 42 and 314159; and 66/66 main-model layers offloaded before calls.

Exactly 24 `/v1/chat/completions` calls ran in the frozen order: 12 for seed 42, then 12 for seed 314159. There was one attempt per seed and zero retries. All provider responses ended normally and parsed as one schema-valid action. One valid `continue_lines` action was rejected by the local environment for the cursor-interface defect described below. No request used an unqualified repository source surface, and no provider, serialization, model, or server integrity failure occurred.

The server stopped normally. Port 18080 was closed before and after execution, no llama process remained, and GPU usage returned from 11,286 MiB after load to the same 319 MiB state recorded before launch. Runtime duration was 409.360 seconds; measured HTTP time summed to 354.840 seconds.

## Candidate continuation-cursor defect

The frozen candidate `read_lines` result renderer returned `standalone-terminal-cursor-not-used` for a transfer-limited candidate slice, while the visible action catalog promised a version-bound cursor accepted by `continue_lines`. The executor only registers continuation cursors for repository reads. Seed 314159 call 5 requested the literal supplied cursor and received `invalid_or_stale_cursor`.

This was not classified as the frozen run's global source-surface invariant because the request was on the qualified candidate surface and the environment returned an ordinary admitted/rejected action result. Direct post-run inspection nevertheless identifies it as a tool-contract conformance defect. It cost one model decision and weakens the behavioral horizon for seed 314159. The run is preserved unchanged; no after-the-fact correction or retry was made.

## Action and source surfaces

Historical exact reopens, candidate tree/search/read/read-lines/read-region, mutation, submission, and exact reads of the four materialized governing documents were available. Novel Git list/catalog/search/history and novel reads outside those four documents were intentionally not materialized. No measured action crossed that boundary.

The inherited schema exposed `patch`, `replace_file`, and `submit`, but no explicit check. Therefore zero checks cannot be interpreted as refusal to use a checker.

## Outcome-definition qualification

The frozen formal-thrash detector requires four consecutive acquisition decisions on an unchanged candidate with no more than two distinct canonical action keys and a repeat. It correctly returned false for both seeds. Direct audit found seed 42 calls 7–12 to be an exact period-three sequence repeated twice. This is reported as descriptive period-three churn without altering the frozen metric.

## Token, cache, and lifecycle accounting

Provider receipts report 477,994 prompt tokens, 935 completion tokens, and 478,929 serialized tokens. Of the prompt tokens, 242,195 were reported cached (50.67%). The policy made 30 message substitutions including the two starting transformations and cumulatively recovered 44,491 prompt tokens. “Cumulative recovered” sums individual pressure interventions; it is not persistent terminal headroom.

The rule resolved 17 post-call pressure events and the two frozen starting events. Five other new-call results fit without treatment. Each terminal call's result was executed and custodied, but no treatment or later invocation was attempted after the frozen limit.

## Replay, tests, and sealing

No additional model or GPU call was made during analysis. `apparatus.analyze` mechanically reduced raw records. Measured replay verified all 24 request/response pairs, exact result backing objects, terminal candidates, and the declared call count.

The frozen inference commit's verifier records 26/26 preflight tests passing. The added analysis test and three post-run source-lock/seal tests pass 4/4. The complete current 30-test suite reports 29 passes and one expected lifecycle failure: `test_fresh_preflight_replay` evaluates today's five finalized report files against the pre-run source lock. `postrun.verify` resolves that distinction by verifying the lock against Git commit `ca07e84c` and requiring exactly the five declared mutable reports to differ. A separate unscoped `pytest` command also traversed the byte-exact `parent_evidence/tests` snapshot and failed during collection because predecessor and current tests share module basenames and require different apparatus modules. Both limitations are preserved rather than hidden.

The frozen source lock is verified against Git commit `ca07e84c`. The five predeclared report paths—`README.md`, `RESULTS.md`, `DIRECT_TRANSCRIPT_AUDIT.md`, `POSTRUN_APPARATUS_NOTE.md`, and `PARENT_PROJECT_IMPLICATIONS.md`—are the only frozen paths allowed to differ after inference. Post-run verification, run seal, and their exact hashes are recorded in `POSTRUN_VERIFICATION.json` and the run tree.
