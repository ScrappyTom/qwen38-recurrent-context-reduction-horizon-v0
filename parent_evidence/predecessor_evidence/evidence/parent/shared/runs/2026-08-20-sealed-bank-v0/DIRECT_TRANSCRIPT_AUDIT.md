# Direct transcript audit

Date: 2026-08-20

Scope: all 42 saved model requests, assistant outputs, parsed actions, literal
tool results, candidate snapshots, capacity preflights, and terminal records in
the four authorized cells.

## Model-visible surface

The actor received ordinary native chronology. Reasoning was disabled and
`preserve_thinking` was false. Each assistant-visible output was one JSON
action; no hidden or durable prose interpretation, plan, or edit intention was
available for review. Claims below therefore concern exact visible inputs and
chosen actions, not inferred internal reasoning.

The full saved response objects retain the serialized prompt. Direct review
confirmed that accepted source and region bytes appeared literally in the
next request. The fresh replay regenerated every saved request byte-for-byte
from the frozen task, tool schema, fixture, profile, and native history:

| Cell | Replayed requests | Exact |
|---|---:|---|
| seed 42 C0 | 10 | yes |
| seed 42 S1 | 12 | yes |
| seed 314159 S1 | 10 | yes |
| seed 314159 C0 | 10 | yes |

## Seed 42, C0

The exact action sequence was:

1. request the complete target with `read` (rejected by the disclosed transfer
   limit);
2. read target lines 1–200;
3. read 201–400;
4. read 401–600;
5. request 601–800 and receive the largest fitting exact prefix, 601–774;
6. continue 775–800;
7. request 801–970 and receive 801–960;
8. continue 961–970;
9. enumerate the first designated source-run directory; and
10. read its `RESULTS.md`.

The actor had then acquired all 970 target lines and 8,063 bytes from one of
the four governing records. The prospective turn-11 request measured 22,263
prompt tokens; preserving the 4,096 response allowance would exceed the
25,088 envelope by 1,271 tokens. No turn 11 was sent.

## Seed 314159, C0

The action types and accepted target ranges were identical to seed 42 C0. It
also reconstructed the entire target, enumerated the first source directory,
and read the same `RESULTS.md`. Its prospective turn-11 prompt was 22,242
tokens, 1,250 beyond the full-response-reserve boundary. No effect occurred.

## Seed 42, S1

The exact sequence was:

1. inspect the candidate tree;
2. open region R002, lines 7–33;
3. enumerate the first source-run directory;
4. read its `RESULTS.md`;
5. read its `DIRECT_TRANSCRIPT_AUDIT.md`;
6. enumerate the second source-run directory;
7. read its `RESULTS.md`;
8. read its `DIRECT_TRANSCRIPT_AUDIT.md`;
9. open R031, lines 740–863, “Phase-continuity and diagnostic update”;
10. open R032, lines 864–889, “Design consequences”;
11. open R033, lines 890–970, “What is not yet known”; and
12. read target lines 1–6.

All four governing source records crossed the model boundary. The actor
acquired 264 distinct target lines / 16,877 target bytes. There were no
rejected actions.

After turn 10, the prompt was 18,617 tokens and a full response still fit. The
actor next opened R033. After turn 11, the prompt was 19,541 tokens and a full
response still fit. The actor next requested lines 1–6. These observations show
continued acquisition after a plausible investigator-qualified source/target
route was visible. They do not prove semantic sufficiency or irrational
acquisition. The prospective turn-13 prompt was 21,386 tokens, 394 beyond the
full-response-reserve boundary.

## Seed 314159, S1

The exact sequence was:

1. inspect the candidate tree;
2. open R033, lines 890–970;
3–8. enumerate both named source directories and read all four governing
   records;
9. open R030, lines 620–739, “Operational model”; and
10. open R031, lines 740–863, “Phase-continuity and diagnostic update.”

All four governing source records crossed the model boundary. The actor
acquired 325 distinct target lines / 22,109 target bytes. It did not open R032,
the design-consequences region, before the prospective turn-11 prompt reached
22,037 tokens, 1,045 beyond the reserve boundary. There were no rejected
actions and no effect.

## Exact evidence content reviewed by the investigator

The four governing records say, in scoped form:

- the original latest-frontier navigation representation caused reset-like
  exploration loops and reached neither exact governing documents nor an
  artifact; and
- the corrected cumulative mechanical navigation state removed those resets
  and let both seeds traverse seven documents and six directories, but neither
  produced an artifact; one path churned on calls/reopens and the other reached
  capacity. The records do not establish an action-sufficient selected set or
  promote a runtime.

The relevant target regions contain the maintained account of phase
continuity, acquisition stopping, action organization, combined prompt
capacity, design consequences, and open questions. Seed 42 S1 saw the complete
four-source record plus R031/R032/R033 and the opening purpose/boundary text.
Seed 314159 S1 saw the complete four-source record plus R030/R031/R033, but not
R032. C0 saw the entire target but only the first source `RESULTS.md`.

## Effect and artifact audit

No action in any cell was `patch`, `replace_file`, `check`, or `submit`.
Candidate hashes and terminal snapshots confirm that all four artifacts remain
identical to the starting blob. The unchanged starting file is not scored as a
model-authored failed artifact because no construction attempt occurred.

## Diagnostic boundary

The transcripts support three separate observations:

```text
mechanical structural addressability
        -> different and substantially narrower target acquisition
        -> complete designated-source coverage

selected acquisition
        != bounded resident execution state

information visible
        != information proven sufficient
        != information accepted as sufficient
        != construction
```

The first is directly observed twice. The second describes the four terminal
paths. The third prevents an unsupported diagnosis: the audit cannot establish
the minimum action-sufficient footprint or claim that Qwen possessed it.

## Custody limits

- This is one maintained artifact and two seeds, not a fresh-world transfer.
- S1 is a coherent addressability package, not an isolated factor.
- The 7,894-byte outline remained resident in native history; this study does
  not test an external/nonresident address plane.
- Because no actor constructed, the study says nothing about semantic
  distinction survival, effect coverage, verification, repair, or closure.
- Recorded timing differs sharply between methods, but the completion lengths
  and cache paths also differ. Timing is descriptive, not a single-mechanism
  estimate.
