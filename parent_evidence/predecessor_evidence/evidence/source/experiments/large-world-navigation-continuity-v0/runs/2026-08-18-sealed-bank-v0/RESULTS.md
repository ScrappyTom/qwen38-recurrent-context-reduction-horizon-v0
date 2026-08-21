# Large-world navigation continuity v0 — results

Date: 2026-08-18

Status: **navigation correction succeeded; construction not reached; mixed downstream boundary**

## Executive result

The matched successor fixed the exact problem it was designed to fix. Both Q3
XL actors traversed all four atlas root pages once, descended into studies, and
read seven exact evidence documents. Neither repeated a navigation operation.
The predecessor had repeatedly restarted root enumeration and read zero exact
atlas documents.

The correction did not produce an artifact. Seed 42 used all 32 calls and spent
11 of them reopening already acquired evidence. Seed 314159 made 22 model calls
and then hit the combined prompt-capacity guard before call 23. Neither actor
mutated, checked, or submitted.

This is not one undifferentiated failure. The evidence supports three separate
conclusions:

1. cumulative mechanical navigation state was a real missing interface;
2. after that repair, both actors assembled a useful but not task-complete
   evidence set; and
3. the remaining horizon was lost differently—call-budget/reacquisition churn
   in seed 42 and combined residency capacity in seed 314159.

## Frozen execution

| Episode | Calls | Terminal state | Exact atlas docs | Experiment dirs | Mutation/check/submit |
|---|---:|---|---:|---:|---|
| seed 42 | 32 | call limit | 7 | 6 | 0 / 0 / 0 |
| seed 314159 | 22 | capacity guard before call 23 | 7 | 6 | 0 / 0 / 0 |

Execution stayed inside authorization:

- fixed order: seed 42, then seed 314159;
- 54 model calls under the 64-call ceiling;
- one attempt per seed and zero retries;
- identical frozen task, corpus, starting candidate, model package, seeds, and
  action surface;
- Q3 XL at 25,088 context, q8 KV, and 66/66 GPU layers;
- all responses ended normally; and
- the model server stopped and released the GPU.

Fresh-process replay verifies all 54 requests after a post-run correction to
the study-local replay adapter. The original failed replay record is preserved;
see `POST_RUN_REPLAY_CORRECTION.md`.

## Intended comparison

| Behavior | Predecessor: latest frontier only | Successor: retained navigation objects |
|---|---:|---:|
| Calls | 64 | 54 |
| Repeated root pages | 46 total requests to root pages | 0 repeated operations |
| Reached root cursor 60 | 0/2 | 2/2 |
| Descended into a study | 0/2 | 2/2 |
| Exact atlas documents read | 0 | 14 reads; 9 unique across bank |
| Experiment directories read | 0 | 8 unique across bank |
| Mutation/check/submission | 0 / 0 / 0 | 0 / 0 / 0 |

The successor therefore answers the narrow causal question. Retaining exact,
deduplicated atlas pages and search results was sufficient to move Q3 XL from
restarting orientation into actual source selection and multi-document reading.

## Evidence selection

Each seed selected seven exact documents across six experiment directories.
Five documents were common to both: the Qwen3.8 AD results and direct audit,
the sparse-runtime results, the virtualized-residency results, and the
construction-boundary results. The remaining choices differed by seed. Across
the bank, the actors selected nine unique documents from eight directories.

The selections were substantively relevant to the requested memo. They covered
package comparisons, semantic/detail loss, sparse runtime behavior, working-set
transfer, context residency, handoff, incremental maintenance, and construction
boundaries. The transcripts contain useful cross-source syntheses before either
stop. This is positive evidence for navigation and selection under the retained
mechanical map.

It is not evidence that either actor completed the frozen information demand.
The task required at least 12 evidence links spanning at least eight experiment
directories. At termination each actor's exact reads covered seven documents
and six directories. The actors repeatedly recognized that shortfall.

## Why construction still did not begin

### Seed 42: call organization and exact-evidence churn

Seed 42 had a maximum prompt of 19,999 tokens and did not hit the context guard.
It reached the 32-call ceiling instead. After seven source reads, it made 11
`reopen_receipt` calls covering six existing receipts.

The actor knew the run limit and, at turn 25, explicitly budgeted for writing,
checking, and submission. Its subsequent choices did not follow that budget.
It continued to reopen large sources while repeatedly planning several more
reads and a later write that no longer fit in the remaining calls.

That is a real action-organization/acquisition-stopping weakness. It is
qualified by a real task gap: the actor still lacked two required experiment
directories and five evidence links. This was not a clean “all needed evidence
was present, but the model read anyway” case.

### Seed 314159: combined residency capacity

Seed 314159's next projected prompt was 21,312 tokens. With the frozen 4,096
completion allowance, it exceeded the 25,088 context limit by 320 tokens. The
harness stopped before inference, so there was no truncated response or failed
model call.

At that point the projection had reached 22,201 bytes of navigation objects and
23,921 bytes of exact evidence. The independent 24,000-byte limits each worked
as specified, but their combination plus task, tools, frontier, ledgers, and
handles did not guarantee a safe total prompt. This is a concrete apparatus
finding: regional byte caps need an enclosing prompt-level capacity invariant.

## Cost

| Episode | Prompt tokens | Cached prompt | Uncached prompt | Completion | Maximum prompt |
|---|---:|---:|---:|---:|---:|
| seed 42 | 441,957 | 61,553 | 380,404 | 32,333 | 19,999 |
| seed 314159 | 279,890 | 41,184 | 238,706 | 20,160 | 20,684 |
| **Total** | **721,847** | **102,737** | **619,110** | **52,493** | — |

The successor performed productive navigation, but it was expensive. Retained
map pages, changing exact objects, and the repeated tool loop produced little
prefix reuse: only 102,737 of 721,847 prompt tokens were reported cached.

The run therefore does not support keeping all observed map pages and a near-
full exact-content allowance resident together as a production default. It
supports the narrower facility—durable navigation continuity—while exposing
the need for global capacity accounting and less evidence churn.

## What this establishes

Supported:

- Mechanical navigation observations can be useful current state rather than
  disposable event history.
- Deduplicated navigation continuity materially changes Q3 XL behavior on a
  broad authentic research task.
- Q3 XL can traverse the retained hierarchy, choose relevant documents, read
  exact evidence, and form useful cross-document interpretations.
- Explicit knowledge of a call limit does not reliably produce a feasible
  acquisition/construction schedule.
- Independent structural and exact-content byte budgets are insufficient
  without a total rendered-prompt guard.

Not supported or not reached:

- a task-complete sufficient working set;
- transition from sufficient evidence to construction;
- semantic quality of a large evidence memo;
- effect, verification, repair, or closure;
- promotion of semantic memory, digests, action bases, forced gates, or a live
  controller; and
- a general claim that Q3 XL cannot perform large-world research.

## Decision

Record the navigation correction as successful and stop this matched repair
line. Do not rerun either seed, raise the cap, or tune another eviction policy
around these trajectories.

The broader framework should carry forward two safeguards:

1. Before execution, calculate whether the required evidence breadth, one-
   action tool ecology, construction, checking, and submission have a plausible
   path inside the frozen call allowance.
2. Enforce one global rendered-prompt budget across every resident region,
   rather than assuming separate byte limits compose safely.

For future authentic large-world tasks, report the pipeline in stages:

```text
navigation continuity
  -> exact selection
  -> coverage/sufficiency
  -> acquisition stopping
  -> construction
  -> effect/check/repair
  -> closure
```

This run moved the observed frontier two stages downstream. It does not justify
another immediate mechanism experiment. The useful next step is to retain this
result as a design constraint and observe whether the same breadth-versus-
construction boundary recurs on a naturally arising research, writing, or
repository-scale task with a feasible action budget.
