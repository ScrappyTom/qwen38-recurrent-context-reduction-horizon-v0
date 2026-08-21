# Direct transcript audit

Every measured request, raw assistant response, parsed action, literal result, budget receipt, projection change, and candidate receipt in `runs/2026-08-20-sealed-run-v1` was read directly. This audit distinguishes exact host custody, model-visible delivery, and investigator interpretation.

## Seed 42

### Starting delivery boundary

The frozen pending result was exact `read_region(R030)`, target lines 620–739, 9,168 content bytes. The untreated packet was 23,353 prompt tokens with -2,361 reserve-preserving headroom. The frozen policy replaced the older source-navigation `RESULTS.md` and `DIRECT_TRANSCRIPT_AUDIT.md` result bodies with exact receipts, recovered 2,998 tokens, and produced the 20,355-token call-1 packet with +637 headroom.

The pending `R030` result was rendered into and seen by call 1. This is actual model-visible delivery, not host acquisition alone.

### Call 1

Raw assistant output:

```json
{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}
```

The parser admitted the exact reopen. The literal result contained the frozen 8,063-byte document and was custodied as an 8,617-byte action-result message. Candidate identity did not change.

Appending this result without treatment would have produced 22,462 prompt tokens and -1,470 headroom. The rule demoted two older exact-backed results—the navigation-continuity run listing (554-token saving) and its `RESULTS.md` (1,980-token saving). The resulting call-2 packet was 19,928 tokens with +1,064 headroom. Call 1's result crossed into call 2.

### Call 2

Raw assistant output:

```json
{"action":"read_region","region_id":"R030"}
```

The read was admitted and returned the same exact target region, lines 620–739, that had already been delivered in call 1. The original `R030` body had not been demoted by the first recurrent treatment, so this is a duplicate acquisition rather than a reopen forced by nonresidency. The 9,168-byte content was custodied as a 9,993-byte result message. Candidate identity did not change.

Appending it untreated would have produced 22,443 tokens and -1,451 headroom. The rule demoted the older navigation-continuity `DIRECT_TRANSCRIPT_AUDIT.md` result for a 1,549-token saving. The call-3 packet was 20,894 tokens with +98 headroom. Call 2's result crossed into call 3.

### Call 3

Raw assistant output:

```json
{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}
```

The parser admitted this exact reopen of the second object demoted at the starting boundary. The literal 5,299-byte document was custodied as a 5,836-byte result message. Candidate identity did not change.

The prospective untreated next packet would have been 22,514 tokens with -1,522 headroom. The result was not rendered into another invocation because call 3 was the frozen endpoint. The policy was not attempted, so this is neither a successful nor failed recurrence event.

### Seed-42 disposition

- Three calls, zero retries.
- Three admitted acquisition actions: two exact reopens and one duplicate region read.
- Frozen pending result plus call-1 and call-2 results reached later model decisions.
- Two post-call pressure events were treated and resolved.
- No mutation or submission; candidate byte identity unchanged.
- Endpoint imposed by the frozen call limit, not selected by the model.

## Seed 314159

### Starting delivery boundary

The frozen pending result was exact `read_region(R032)`, target lines 864–889, 2,979 content bytes. The untreated packet was 21,521 prompt tokens with -529 headroom. The policy replaced the older source-navigation `RESULTS.md` body with an exact receipt, recovered 1,746 tokens, and produced the 19,775-token call-1 packet with +1,217 headroom.

The pending `R032` result was rendered into and seen by call 1.

### Call 1

Raw assistant output:

```json
{"action":"read_lines","end_line":970,"path":"QWEN_RELATION_ACTION_WORKING_MODEL.md","start_line":890}
```

The read was admitted. It returned the complete requested 5,487-byte slice, lines 890–970, directly adjacent to the already delivered `R032` lines 864–889. The result was custodied as a 6,370-byte action-result message. Candidate identity did not change.

Appending it untreated would have produced 21,236 tokens and -244 headroom. The rule demoted the older source-navigation `DIRECT_TRANSCRIPT_AUDIT.md` result, saving 1,244 tokens. The call-2 packet was 19,992 tokens with +1,000 headroom. Call 1's result crossed into call 2.

### Call 2

Raw assistant output:

```json
{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md"}
```

The parser admitted an exact reopen of the object demoted immediately before this call. The literal 5,299-byte document was custodied as a 5,836-byte action-result message. Candidate identity did not change.

Appending it untreated would have produced 21,612 tokens and -620 headroom. The rule demoted the navigation-continuity run listing (550-token saving) and its `RESULTS.md` (1,976-token saving). The call-3 packet was 19,086 tokens with +1,906 headroom. Call 2's result crossed into call 3.

### Call 3

Raw assistant output:

```json
{"action":"repo_read","path":"experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md"}
```

The parser admitted this exact reopen of the object demoted at the starting boundary. The literal 8,063-byte document was custodied as an 8,617-byte result message. Candidate identity did not change.

The prospective untreated next packet would have been 21,193 tokens with -201 headroom. The result was not delivered because the call limit had been reached, and the policy was not attempted.

### Seed-314159 disposition

- Three calls, zero retries.
- Three admitted acquisition actions: two exact reopens and one adjacent target read.
- Frozen pending result plus call-1 and call-2 results reached later model decisions.
- Two post-call pressure events were treated and resolved.
- No mutation or submission; candidate byte identity unchanged.
- Endpoint imposed by the frozen call limit.

## Cross-seed audit judgment

The mechanical recurrence result is seed-consistent within this two-trajectory study: four of four authorized post-call pressure events were resolved, and six exact results in total crossed treatment-backed decision boundaries when the two frozen pending results are included.

The behavior is also qualitatively consistent: both trajectories spent the full continuation on acquisition, and both used exact receipts to recover demoted information. That does not establish that the reads were unnecessary. The response format retained only tool actions, reasoning was off, and there is no matched untreated behavioral continuation. “The model already had enough information to act” would be an investigator judgment, not a host-visible fact, and is not asserted here.

The apparent benefit was not merely more nominal calls: four newly acquired results actually crossed into subsequent model invocations under packets that would otherwise have violated the frozen reserve. Nevertheless, no artifact progress occurred. The remaining behavioral boundary is unresolved between legitimate information demand, redundant acquisition, and acquisition-stopping/action-commitment control.
