# Direct transcript audit

Every measured request, raw provider response, parsed action, literal result, exact backing object, budget receipt, projection change, and candidate receipt in `runs/2026-08-20-sealed-horizon-run-v0` was inspected directly. This audit distinguishes host custody, actual model-visible delivery, and investigator interpretation.

All raw assistant contents were one bare JSON action. The exact text equals the canonical JSON shown below. Hashes and complete literal result bodies remain in each cell's `requests/`, `responses/`, `actions/`, `results/`, and `objects/` directories.

## Seed 42

### Starting boundary

The exact predecessor call-3 result was source-navigation `DIRECT_TRANSCRIPT_AUDIT.md`. Without treatment, appending it produced a 22,514-token request with -1,522 reserve-preserving headroom. The frozen policy replaced the oldest eligible full `R031` result at message 19, recovered 1,607 tokens, and produced the 20,907-token call-1 request with +85 headroom. The pending result was rendered into and observed by call 1.

### New calls

| Call | Exact raw action | Admission and literal result | Delivery/capacity transition |
|---:|---|---|---|
| 1 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,546-byte blob | Untreated -2,263; three demotions saved 3,637; delivered to call 2 at +1,374 |
| 2 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}` | Admitted exact reopen; 7,224-byte blob | Untreated -546; one demotion saved 1,747; delivered to call 3 |
| 3 | `{"action":"read_lines","end_line":970,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":864}` | Admitted novel candidate slice, exact lines 864–970, 8,466 bytes | Untreated -844; one demotion saved 2,100; delivered to call 4 |
| 4 | `{"action":"read_lines","end_line":33,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":7}` | Admitted novel exact lines 7–33, 814 bytes | Fit untreated; delivered to call 5 |
| 5 | `{"action":"read_lines","end_line":35,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":34}` | Admitted novel exact lines 34–35, 27 bytes | Fit untreated; delivered to call 6 |
| 6 | `{"action":"read_lines","end_line":863,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":740}` | Admitted novel exact lines 740–863, 7,454 bytes | Untreated -1,739; two demotions saved 3,166; delivered to call 7; frozen local-nonchurn window ends here |
| 7 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,063-byte blob | Untreated -680; one demotion saved 1,497; delivered to call 8 |
| 8 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}` | Admitted exact reopen; 5,299-byte blob | Untreated -803; one demotion saved 1,522; delivered to call 9 |
| 9 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,546-byte blob | Untreated -1,629; three demotions saved 3,245; delivered to call 10 |
| 10 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,063-byte blob; repeats call 7 | Untreated -491; one demotion saved 1,195; delivered to call 11 |
| 11 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}` | Admitted exact reopen; 5,299-byte blob; repeats call 8 | Untreated -916; one demotion saved 1,928; delivered to call 12 |
| 12 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,546-byte blob; repeats call 9 | Result custodied; prospective packet 22,328 / -1,336; not treated or delivered at frozen limit |

### Seed-42 audit judgment

- Twelve calls, zero retries, all 12 operations admitted.
- The frozen predecessor-pending result plus calls 1–11 crossed later model boundaries; call 12's result did not.
- Four novel acquisitions were followed by eight exact reopens.
- Calls 7–12 form an exact period-three action cycle repeated twice on an unchanged candidate.
- Repeat-within-four was recorded at calls 10, 11, and 12.
- No four-decision window used at most two keys, so the predeclared formal-thrash flag is correctly false.
- No mutation or submission; candidate identity remained `19296f…24fd`.

## Seed 314159

### Starting boundary

The exact predecessor call-3 result was source-navigation `RESULTS.md`. Without treatment, appending it produced a 21,193-token request with -201 headroom. The policy replaced the oldest eligible navigation-continuity direct-audit result at message 17, recovered 1,545 tokens, and produced the 19,648-token call-1 request with +1,344 headroom. The pending result crossed into call 1.

### New calls

| Call | Exact raw action | Admission and literal result | Delivery/capacity transition |
|---:|---|---|---|
| 1 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}` | Admitted exact reopen; 7,224-byte blob | Untreated -576; one demotion saved 2,104; delivered to call 2 |
| 2 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,546-byte blob | Untreated -820; one demotion saved 1,594; delivered to call 3 |
| 3 | `{"action":"read_lines","end_line":33,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":1}` | Admitted novel exact lines 1–33, 957 bytes | Fit untreated; delivered to call 4 |
| 4 | `{"action":"read_lines","end_line":619,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":34}` | Admitted novel transfer-limited slice, exact lines 34–265, 11,934 bytes | Untreated -2,853; four demotions saved 4,479; delivered to call 5 |
| 5 | `{"action":"continue_lines","cursor":"standalone-terminal-cursor-not-used"}` | Rejected `invalid_or_stale_cursor`; exact 328-byte error result | Fit untreated; error crossed into call 6 |
| 6 | `{"action":"read_lines","end_line":619,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":266}` | Admitted novel transfer-limited slice, exact lines 266–482, 11,996 bytes | Untreated -1,589; two demotions saved 3,421; delivered to call 7; local-nonchurn window ends here |
| 7 | `{"action":"read_lines","end_line":619,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":483}` | Admitted novel exact lines 483–619, 8,001 bytes | Untreated -403; two demotions saved 2,585; delivered to call 8; local-nonchurn window also ends here |
| 8 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}` | Admitted exact reopen; 5,299-byte blob | Fit untreated; delivered to call 9 |
| 9 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,063-byte blob | Untreated -1,545; one demotion saved 2,538; delivered to call 10 |
| 10 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}` | Admitted exact reopen; 7,224-byte blob | Untreated -927; one demotion saved 1,705; delivered to call 11 |
| 11 | `{"action":"repo_read","path":"experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,546-byte blob | Untreated -1,570; two demotions saved 2,876; delivered to call 12 |
| 12 | `{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}` | Admitted exact reopen; 8,063-byte blob; repeats call 9 | Result custodied; prospective packet 21,793 / -801; not treated or delivered at frozen limit |

### Cursor-interface qualification

Call 4's literal accepted result stated `request_complete:false`, `next_start_line:266`, and `continuation_cursor:"standalone-terminal-cursor-not-used"`. The visible tool contract said a truncated candidate read would return a version-bound cursor usable by `continue_lines`. The frozen adapter registered cursors only for repository reads, not candidate reads. Call 5 therefore followed the supplied interface and was rejected.

The actor used the exact `next_start_line` field to recover manually on calls 6 and 7, ultimately observing target lines 1–619. The rejection was not caused by context reduction, malformed model JSON, or a stale candidate. It is an apparatus/interface defect discovered by the measured run. It consumed one of this seed's 12 authorized decisions and must qualify any cross-seed behavioral comparison.

### Seed-314159 audit judgment

- Twelve calls, zero retries; 11 admitted operations and one interface-caused rejection.
- The predecessor-pending result plus calls 1–11 crossed later model boundaries; call 12's result did not.
- Five actions were mechanically novel on the unchanged-candidate basis; seven were duplicate exact reopens.
- The late sequence revisited four governing documents and repeated one within four calls, but did not form the frozen ≤2-key formal-thrash pattern.
- No mutation or submission; candidate unchanged.

## Cross-seed judgment

The physical result is seed-consistent in this two-trajectory study. Every authorized pressure treatment restored the frozen reserve, and each seed received 12 exact results across new model boundaries when its predecessor-pending result is included. The apparent gain was not merely permission for more calls: 22 new call results actually entered later invocations under packets that would otherwise often have been infeasible.

The behavior did not converge to construction within the horizon. Both trajectories first displayed noncycling acquisition and later returned repeatedly to demoted governing documents. Seed 42's exact period-three loop is direct evidence of late churn even though the frozen formal detector does not label it. Seed 314159's pattern is less conclusive and is additionally censored by the cursor defect.

This audit does not assert that any exact read was semantically unnecessary. Reasoning was off, the transcript contains only tool actions, and there is no matched untreated continuation. “The model had enough information to write” would be investigator interpretation, not a host fact. The defensible conclusion is that physical capacity was kept operable while action remained acquisition, with one clear longer-period cycling pattern and no artifact progress.
