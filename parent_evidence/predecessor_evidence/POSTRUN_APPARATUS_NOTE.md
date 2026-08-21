# Post-run apparatus note

## Frozen execution identity

- Run: `2026-08-20-sealed-run-v0`.
- Frozen standalone commit: `904c7a1eb67c7f667641dd1d74c0d6e65a54ce99`.
- Authorization-bound source-lock SHA-256: `18d49cae06d0ac73067f72208530fd80e5827d04ebb62990c9deac13e31cd45c`.
- Authorization: four named cells, eight calls maximum, one attempt per cell, zero retries.
- Actual execution: four cells, six calls, zero retries.

The user authorization statement and all authorization fields are embedded in `model/runtime-custody.json` and copied into the sealed run as `model/AUTHORIZATION.json`.

## Runtime acquisition and qualification

The exact full model was resumed from the official pinned Hugging Face revision and verified before use:

- repository: `AtomicChat/Qwen3.8-27B-GGUF`;
- revision: `ca10ebceb1887be9d33b838770a36b39d75a8a4c`;
- file: `Qwen3.8-27B-AD-IQ2_S.gguf`;
- size: 11,141,912,032 bytes;
- SHA-256: `d416fa422c9035605c778f60d90a94b288c38b4f9ec2126b58ef938ce8d5f716`.

The measured server used the pinned official Windows CUDA 13.3 b10434 release. The `llama-server.exe` size was 9,216 bytes and its SHA-256 was `5f1f831bc21dcbff4ca40e05cb59dbcbc0802d20b2046540bbbf3bd45cd61610`. The two release archives matched the hashes and sizes frozen in `provenance/MODEL_PROFILE_LOCK.json`.

Live endpoint checks passed for health, alias, build `b10434-7e4c0a968`, model path, chat template, observed 25,088-token context, reasoning-off profile, and seed-specific sampler. Main-model offload was 66/66 before calls. No llama server occupied port 8080 before execution. After the run the server exited, the port was closed, no llama process remained, and GPU memory returned to its 319 MiB baseline.

The exact launch arguments, endpoint properties, lifecycle snapshots, GPU receipts, authorization, server log, stdout, and stderr are archived under `runs/2026-08-20-sealed-run-v0/model/`.

## Post-run-only additions

No prompt, policy, action rule, schedule, or measured runner source changed between freeze and the final model response. After server shutdown, the following read-only analysis/custody helpers were added:

- `postrun/audit_reduce.py`, to audit first- or second-action access to demoted backing objects;
- `postrun/metrics.py`, to aggregate raw provider usage, timing, capacity, and runtime receipts;
- `postrun/seal.py`, to hash the complete measured run tree;
- focused tests for demoted-object classification, absorption-status wording, and seal integrity.

The original `analysis/ANALYSIS.json` is preserved. Its `reopens: 0` field means “no exact reopen as a terminal second action” under that reducer's implementation; it is not a complete all-turn fault-in count. `analysis/AUDITED_ANALYSIS.json` supplies the corrected all-turn object-access view. Raw requests, responses, classifications, and endpoints were not altered.

## Source-lock lifecycle

The pre-run source lock intentionally binds the exact frozen commit and includes placeholder result documents. Updating `README.md` and `RESULTS.md` after measurement therefore makes a current-worktree hash comparison against that pre-run lock inappropriate. The authorization remains bound to the immutable commit named above; the frozen verifier receipt was captured after execution and before result-document edits. The final result commit and run seal custody the post-run state separately.

## Evaluator qualification

No external semantic evaluator was invoked. No cell changed the candidate, and the terminal candidate SHA-256 remained exactly equal to the initial candidate. Running a semantic checker would add no treatment-specific artifact evidence. This run's artifact-quality result is exact byte identity and no construction progress.

## Limitations

- The historical control is exact prior behavior plus a mechanical capacity rejection, not a new simultaneous model call.
- Only two seeds and one task/world/boundary family were measured.
- The terminal second acquisition requests were not executed; the design observes the second decision, not another result-delivery cycle.
- Aggressive-policy result absorption was not evaluated after decision divergence.
- Exact-backed receipts combine nonresidency with compact mechanical representation; this is not a pure DROP-versus-semantic-COMPRESS comparison.
- No retained reasoning content explains why the model chose acquisition or recovery.

No successor was selected or run.
