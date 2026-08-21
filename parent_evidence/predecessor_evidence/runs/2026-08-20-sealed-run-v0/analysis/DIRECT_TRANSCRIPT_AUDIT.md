# Direct transcript audit

Run: `2026-08-20-sealed-run-v0`

Frozen standalone commit: `904c7a1eb67c7f667641dd1d74c0d6e65a54ce99`

Every one of the six new assistant turns, its exact request and response, parsed action, capacity receipt, delivered result where applicable, and candidate consequence was read directly. The model emitted bare JSON actions with no retained reasoning text.

## Seed 42 — `oldest_fit_receipts_v0`

The policy replaced result messages 5 and 7: the old `R002` target read and a repository listing. All other messages, including the task, full outline, later exact observations, assistant actions, order, and current candidate, remained byte-identical to the parent boundary.

- Call 1 request SHA-256: `3472ef02598073952a505ed2672be22d2a9fc05cb851a2f8cb01469f1fa070da`.
- Rendered prompt: 20,418 tokens; +574 headroom after the 4,096 reserve.
- Raw assistant content: `{"action":"read_lines","end_line":6,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":1}`.
- Parsed action: valid and exactly equal to the historical acquisition.
- Provider response SHA-256: `e5f46c8937d095db9f36fe328ebcde45b03df63a82cbcd686b253e0d0762c381`; HTTP 200; 30 completion tokens.
- Literal result: accepted target lines 1–6, 143 UTF-8 bytes, slice SHA-256 `f6796ea0f82c2d8765603987545be2609e511222f9bf26a9d0d4472279cb973e`.
- Result delivery: the next request SHA-256 was `5a3527588d30c30356a51fd504ecb757f234a4171ef6b4cd24e308ba14947f7c`, exactly the frozen post-historical-result packet. It was 20,838 prompt tokens with +154 headroom.
- Call 2 raw assistant content: `{"action":"read_region","region_id":"R030"}`.
- Parsed action: valid other acquisition; `R030` had not appeared among this trajectory's earlier accepted region reads and was not a demoted result reopen.
- Provider response SHA-256: `4e9f0f9706112f50fb3a210d2c46f12be61ab41191692520ff378efb42be4929`; HTTP 200; 15 completion tokens.
- Terminal handling: the acquisition result was not executed by design at the terminal second-decision boundary. Candidate bytes did not change.

Investigator interpretation: the small receipt substitution retained enough orientation to reproduce the exact historical decision and, after the formerly blocked observation entered, to select another target region. This does not establish that either observation was semantically sufficient for mutation.

## Seed 314159 — `oldest_fit_receipts_v0`

The policy replaced result messages 5 and 7: the old `R033` read and the same repository listing class. Later exact observations remained resident.

- Call 1 request SHA-256: `33632a754826238ca2d80255d5ba07bc94fb6174adecb687b99a03a1c5fb4783`.
- Rendered prompt: 18,573 tokens; +2,419 headroom after reserve.
- Raw assistant content: `{"action":"read_region","region_id":"R031"}`.
- Parsed action: valid and exactly equal to the historical acquisition.
- Provider response SHA-256: `3aeca5c819ffa5ec60112b88abcef6a40be2c9aad55369d150192fa33ce6f6ec`; HTTP 200; 15 completion tokens.
- Literal result: accepted target `R031`, lines 740–863, 7,454 UTF-8 bytes, SHA-256 `7d4c92f2cd3f9b2511a4e8b1fb8ae4a59bb5d2d85d31f09e47b010024b61570b`.
- Result delivery: the next request SHA-256 was `865a78054d30fb098aacb17dbd47c14bfe0f5fb46a6b0e55c3f161df84ef64aa`, exactly the frozen post-historical-result packet. It was 20,597 prompt tokens with +395 headroom.
- Call 2 raw assistant content: `{"action":"read_region","region_id":"R032"}`.
- Parsed action: valid other acquisition; `R032` had not appeared among this trajectory's earlier accepted region reads and was not a demoted result reopen.
- Provider response SHA-256: `49959af41dc95fe78ff924a3df6cf9846c3ef7a5338d0ea4f53b060747b7c480`; HTTP 200; 15 completion tokens.
- Terminal handling: the acquisition result was not executed by design. Candidate bytes did not change.

Investigator interpretation: this is the stronger capacity case because the 7,454-byte observation moved the prompt by 2,024 tokens. The minimal rule still preserved the exact decision and left 395 reserved tokens of headroom after its delivery. The next choice remained acquisition rather than action.

## Seed 42 — `recent2_receipts_v0`

The policy replaced eight older result bodies and protected only the final two historical results. It removed 9,236 decision tokens.

- Call 1 request SHA-256: `f7aa3cf2bd2777e0cb372a4b0e814d0a4a4d5dffa61367f788d12570a983c2fb`.
- Rendered prompt: 11,730 tokens; +9,262 headroom after reserve.
- Raw assistant content: `{"action":"repo_read_lines","end_line":1,"path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md","start_line":1}`.
- Parsed action: schema-valid acquisition, but neither the historical target read nor the sole predeclared byte-equivalent action.
- Direct object comparison: that exact path was represented by a demoted receipt. The requested one-line operation was an alternate access to the same backing object, not the receipt's original full-read reopen action.
- Provider response SHA-256: `b8a0bc2d23d1aab2af1aa7888c11b40bdd3e9c3069bff53cfe44dcd157416228`; HTTP 200; 52 completion tokens.
- Gate consequence: `decision_not_preserved`. The host made no tool call, delivered no result, and made no second model call. Result absorption is untested, not capacity-failed. Candidate bytes did not change.

Investigator interpretation: the larger reduction removed information with continuing decision value or made its absence salient enough to trigger recovery. The transcript contains no reasoning text, so it does not establish which explanation governed the choice.

## Seed 314159 — `recent2_receipts_v0`

The policy replaced six older result bodies, removed 6,956 decision tokens, and protected the last two results.

- Call 1 request SHA-256: `435b7362dc073e035e34b5aee03da9360516f779d11e3753d52e3a5e21fb0519`.
- Rendered prompt: 13,057 tokens; +7,935 headroom after reserve.
- Raw assistant content: `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}`.
- Parsed action: schema-valid acquisition, but not the frozen historical target action or its byte-equivalent alternate.
- Direct object comparison: this was exactly the original reopen action recorded in the receipt for a demoted result.
- Provider response SHA-256: `23dba9872482e4ed68494e7bd2893d0599da43271b1cbf00855bdb4682a1dcdf`; HTTP 200; 41 completion tokens.
- Gate consequence: `decision_not_preserved`. The exact reopen was requested but not executed or delivered; no second call occurred. Result absorption is untested. Candidate bytes did not change.

Investigator interpretation: exact recoverability was behaviorally addressable, but this cell did not exercise completed recovery because the experiment's primary preservation gate stopped first. The result argues against treating the six demoted objects as behaviorally inert at this boundary.

## Cross-cell audit

- All six requests used the frozen task, full structural outline, action schema, response reserve, reasoning-off setting, and seed-specific sampler.
- Every response was one valid JSON action with `finish_reason: stop`; no output was retried or repaired.
- No outline was demoted, referenced for recovery, or reopened.
- No mutation, check, or submission occurred.
- The two delivered results crossed actual model boundaries only in the oldest-fit cells.
- The two recent-two result-absorption opportunities were intentionally not measured after their first decisions diverged.
- The original analysis reducer's zero-reopen aggregate was incomplete because it inspected only terminal second actions. [AUDITED_ANALYSIS.json](runs/2026-08-20-sealed-run-v0/analysis/AUDITED_ANALYSIS.json) adds first-action object-access auditing without changing the frozen equivalence judgment.
