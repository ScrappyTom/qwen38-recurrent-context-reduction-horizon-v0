# Large-world navigation continuity v0 — direct transcript audit

Date: 2026-08-18

## Scope and custody

This audit was performed after both sealed episodes stopped. It reviewed all
54 exact requests, responses, parsed actions, literal results, projection
receipts, candidate manifests, and final custody records.

The bank executed once per seed with zero retries. All 54 responses ended with
`finish_reason: stop`. Q3 XL ran at 25,088 context with q8 KV and full 66/66
GPU offload. The server stopped and returned the GPU to its idle allocation.

The automatic replay initially failed because of a study-local reconstruction
adapter error. The correction changed no model-facing evidence. Fresh-process
replay then verified all 54 saved requests byte-for-byte. The correction is
preserved in `POST_RUN_REPLAY_CORRECTION.md`.

## Seed 42

### Action sequence

| Turns | Observed behavior |
|---|---|
| 1–4 | Expands `ROOT` at cursors 0, 20, 40, and 60 exactly once each. |
| 5–9 | Inspects the candidate, expands two studies, and searches `large-world`. |
| 10–19 | Reads six exact evidence documents across five experiment directories. |
| 20–24 | Reopens already acquired evidence receipts. |
| 25–26 | Expands and reads one additional construction-boundary study. |
| 27–32 | Reopens already acquired evidence and reaches the call limit. |

Counts:

- 32 calls;
- 10 `atlas_expand`, seven `atlas_read`, one `atlas_search`, one candidate
  `tree`, and two candidate `read` actions;
- 11 `reopen_receipt` actions covering six unique receipts;
- seven unique exact atlas documents, 53,193 source bytes, across six
  experiment directories;
- zero repeated navigation operations;
- zero mutations, checks, or submissions.

The seven exact evidence documents came from the Qwen3.8 AD and UD trajectory
studies, the sparse-runtime field study, virtualized context residency,
incremental maintenance projection, and the construction-boundary study.

The actor repeatedly stated the correct high-level objective and recognized
the 32-call ceiling. At turn 25 it calculated that only eight calls remained
and that writing, checking, and submission required three of them. It also
recognized that its evidence covered only five or six of the required eight
experiment directories. That was a legitimate coverage gap.

The subsequent policy was not effective. After acquiring one more document,
the actor spent all six remaining calls reopening receipts it had already
read. Its reasoning continued to propose several additional reopens followed
by writing, even when the turn ledger no longer permitted that sequence. The
failure is therefore not loss of navigation state. It is a mixture of an
unfinished breadth requirement, poor call-budget organization, and repeated
exact reacquisition instead of committing to a feasible remaining plan.

## Seed 314159

### Action sequence

| Turns | Observed behavior |
|---|---|
| 1–5 | Reads the atlas root and expands all four root pages once each. |
| 6–15 | Descends through studies, reads three documents, and completes both pages of a `Q3 XL` search. |
| 16–18 | Reads three more exact evidence documents. |
| 19–22 | Reopens one receipt, expands another study, reads the candidate, and reads a seventh evidence document. |
| 23 | Capacity preflight rejects the next invocation before a model call. |

Counts:

- 22 model calls;
- nine `atlas_expand`, seven `atlas_read`, three `atlas_search`, one
  `atlas_root`, one candidate `read`, and one `reopen_receipt`;
- seven unique exact atlas documents, 51,990 source bytes, across six
  experiment directories;
- 13 navigation operations, all unique;
- zero mutations, checks, or submissions.

By turn 18 the actor had already formed a concrete and substantially correct
synthesis of the model-selected-window, sparse-runtime, virtualized-residency,
and handoff results. It explicitly said that it had strong content and should
write. It then continued gathering because the artifact required at least 12
links across eight experiment directories and its exact evidence still covered
fewer directories.

At turn 22 it again planned more acquisition before writing. The prospective
turn-23 request contained 21,312 prompt tokens; adding the frozen 4,096-token
response allowance would exceed the 25,088 context by 320 tokens. The harness
correctly stopped before inference. This is a combined-residency capacity
boundary, not response truncation or a failed model call.

## Navigation correction

The direct matched correction succeeded on its intended boundary:

```text
predecessor
page 0 -> page 20 -> prior page absent -> restart

successor
pages 0/20/40/60 remain addressable together
  -> descend into study
  -> read exact document
  -> retain/reopen exact evidence
```

Neither actor repeated a root page or another navigation operation. Both
reached cursor 60, descended into several studies, followed document IDs, and
read exact source. The predecessor did none of those downstream actions.

This supports the narrow conclusion that cumulative, deduplicated mechanical
navigation state was the missing interface component in the predecessor.

## Downstream boundary

The successor does not establish that the model had a task-complete sufficient
working set and irrationally refused to write. The task explicitly required 12
links across eight experiment directories. Each actor had read seven documents
from six directories when it stopped. Their belief that more breadth was needed
was therefore grounded in the task.

It does establish two narrower problems:

1. Seed 42 did not organize its remaining call budget around the known coverage
   gap and the need to reserve calls for mutation, check, and submission.
2. Seed 314159 filled the combined navigation-plus-exact-content projection
   before construction, showing that two independent byte budgets do not by
   themselves guarantee a safe total prompt budget.

The exact-content LRU also produced a reacquisition loop in seed 42. Previously
read sources collapsed as new large documents arrived, and the actor repeatedly
reopened them to regain literal access. This is not a duplicate navigation
loop; it is churn in the evidence working set.

## Interpretation boundary

Supported:

- bounded mechanical navigation continuity eliminated the predecessor's reset
  loop;
- Q3 XL can use the retained map to descend and selectively read exact evidence;
- the actor can form useful cross-document interpretations from that evidence;
- broad evidence requirements, one-action calls, exact-object churn, and
  independent residency budgets can jointly consume the available work horizon
  before construction; and
- explicit awareness of the call limit did not guarantee budget-conforming
  action organization in seed 42.

Not established:

- that seven documents across six directories were sufficient for the frozen
  artifact requirement;
- that a smaller complete working set would cause construction;
- artifact quality, qualifier preservation, verification, repair, or closure;
- benefit from semantic summaries, plans, action bases, or a forced commit
  decision; or
- a general Q3 XL inability to perform authentic large-world research.
