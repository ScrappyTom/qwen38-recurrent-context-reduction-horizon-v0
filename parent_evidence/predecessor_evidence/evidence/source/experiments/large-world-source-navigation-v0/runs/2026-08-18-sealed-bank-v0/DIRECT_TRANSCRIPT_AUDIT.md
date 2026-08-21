# Large-world source navigation v0 — direct transcript audit

Date: 2026-08-18

## Scope and custody

This audit was performed after both sealed episodes stopped. It reviewed all
64 exact requests, responses, parsed actions, literal result messages,
projection receipts, candidate manifests, and final custody records.

Fresh-process replay verified all 64 requests byte-for-byte. Each episode has
195 chained records and 293 verified artifact references. The runtime record
confirms one attempt per seed, no retry, the 25,088-token context, 66/66 GPU
layers, and GPU release after execution.

## Seed 42

### Action sequence

| Turns | Observed behavior |
|---|---|
| 1–3 | Expands `ROOT` at cursors 0, 20, and 40. |
| 4–5 | Restarts at cursors 0 and 20. |
| 6 | Searches for `Q3 XL`; receives 12 of 24 exact literal matches. |
| 7–8 | Requests candidate tree, then atlas root. |
| 9–32 | Repeats root pages and candidate-tree orientation; never descends. |

Counts:

- `atlas_expand`: 24;
- `ROOT:0`: 11;
- `ROOT:20`: 10;
- `ROOT:40`: 3;
- `ROOT:60`: 0;
- `atlas_search`: 1;
- `atlas_root`: 1;
- `tree`: 6;
- exact atlas reads, candidate reads, mutations, checks, submissions: 0.

The reasoning on turn 1 says it will explore the atlas and then navigate to
relevant evidence. Turn 2 recognizes that it has seen the first page and asks
for the next. Turn 3 asks for cursor 40. Turn 4 again says it is starting its
exploration and requests cursor 0. That reset is the first complete, directly
observable loop.

Later turns sometimes recognize the 32-call bound and say they must be
strategic. Nevertheless, every invocation reconstructs a similar initial plan:
inspect the atlas, inspect the candidate, find Q3 XL evidence, then write. No
prior traversal state survives strongly enough to organize the next action.

## Seed 314159

### Action sequence

| Turns | Observed behavior |
|---|---|
| 1–2 | Expands `ROOT` at cursors 0 and 20. |
| 3 | Searches for `Q3 XL`; receives the same 12-of-24 first page. |
| 4–23 | Alternates repeated root pages and candidate-tree requests. |
| 24 | Reads the 545-byte starting memo. |
| 25–32 | Restarts root enumeration; never descends or writes. |

Counts:

- `atlas_expand`: 22;
- `ROOT:0`: 12;
- `ROOT:20`: 9;
- `ROOT:40`: 1;
- `ROOT:60`: 0;
- `atlas_search`: 1;
- `atlas_root`: 1;
- `tree`: 7;
- candidate `read`: 1;
- exact atlas reads, mutations, checks, submissions: 0.

This actor articulates the complete intended workflow several times: inspect
the corpus, search Q3 XL evidence, read key sources, write, check, and submit.
On turn 9 it explicitly notes the one-action-per-call rule and the 32-call
limit. On turn 16 it calculates that cursors 20, 40, and 60 are needed. The
next invocations still return to candidate-tree or cursor-0 orientation.

The turn-24 candidate read is delivered and retained as a 545-byte current
exact object. That proves exact current-object residency operated. It did not
help atlas traversal because the missing information was the accumulated
navigation state, not the candidate bytes.

## Result-delivery audit

Every request was reconstructed from the frozen renderer and the saved prior
results. The current surface always contained the immediately preceding
literal frontier. The seed-314159 candidate-read receipt crossed the next
model boundary and remained exactly reopenable.

There was no accepted-result/immediate-eviction defect of the kind observed in
the earlier event-virtualization scout. The problem is instead that successful
non-content navigation results were deliberately represented only as the
latest frontier. When the next action succeeded, the prior structural result
ceased to be visible.

## Interpretation boundary

The transcripts support this causal description:

```text
page 0 visible
  -> actor requests page 20
page 20 visible; page 0 and prior reasoning absent
  -> actor requests another orientation result
new result visible; earlier pages absent
  -> actor reconstructs the initial exploration plan
  -> repeated root/tree acquisition
```

They do not show that the actor selected a sufficient evidence set and then
refused to construct. They do not show failure to understand exact evidence,
because no exact evidence document or section was read. They also do not test
semantic persistence: no model-authored semantic conclusion was formed from
source material.

The defensible failure boundary is **navigation-state accumulation / action
organization** caused by an overly sparse model-visible work surface. Model
policy contributes—the actor could have descended immediately from any one
visible page—but the task required broad cross-study coverage, making its wish
to inventory the corpus reasonable. The apparatus gave it no durable,
mechanical way to accumulate that inventory.

## Semantic review disposition

No mutation occurred. The final candidate in both episodes is byte-identical
to the frozen 545-byte skeleton. Therefore:

- substantive memo review: not applicable;
- provenance review: not applicable;
- qualifier/scope review: not applicable;
- visible check review: not reached; and
- closure review: incorrect by turn-limit, downstream of navigation failure.

The skeleton must not be scored as though it were an attempted final artifact.
