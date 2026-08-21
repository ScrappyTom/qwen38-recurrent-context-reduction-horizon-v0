# Large-world source navigation v0 — results

Date: 2026-08-18

Status: **completed; negative at cumulative navigation state; downstream questions not reached**

## Executive result

Both sealed Q3 XL episodes used the full 32-call allowance without reading one
exact atlas document or section, changing the candidate, running the check, or
submitting. The result is repeatable across the two frozen seeds, but it is not
evidence that Q3 XL cannot select relevant evidence or refuses to construct
after obtaining a sufficient working set.

The failure occurred earlier. The current-object projection retained the task,
candidate identity, atlas identity, current exact objects, and only the latest
literal action/result frontier. Atlas expansion and search results were treated
as transient frontiers rather than cumulative current navigation objects. Once
the actor requested another page or performed another action, its earlier map
pages and its own prior reasoning were absent from the next request.

Both actors consequently repeated a short orientation loop instead of building
and using a stable map of the evidence world.

## Frozen execution

| Episode | Calls | Terminal state | Exact atlas reads | Mutations | Checks | Submission |
|---|---:|---|---:|---:|---:|---:|
| seed 42 | 32 | call limit | 0 | 0 | 0 | no |
| seed 314159 | 32 | call limit | 0 | 0 | 0 | no |

Execution stayed inside the authorization:

- fixed order: seed 42, then seed 314159;
- 64 total model calls under the 64-call ceiling;
- one attempt per episode and zero retries;
- Q3 XL at 25,088 context with q8 KV and 66/66 layers offloaded;
- exact fresh-process replay of all 64 requests passed; and
- the model server stopped and released the GPU.

## What the actors did

Seed 42 made 24 root expansions, one atlas search, one atlas-root request, and
six candidate-tree requests. It requested root cursor 0 eleven times, cursor
20 ten times, and cursor 40 three times. It never requested cursor 60 and never
descended into a study or document.

Seed 314159 made 22 root expansions, one atlas search, one atlas-root request,
seven candidate-tree requests, and one read of the 545-byte starting memo. It
requested root cursor 0 twelve times, cursor 20 nine times, and cursor 40 once.
It likewise never requested cursor 60 or descended into a study or document.

Each seed's one `Q3 XL` search succeeded mechanically. It returned 12 of 24
literal matches from six unique evidence paths, with exact document and section
identities available. Neither actor followed those identities into an exact
source read. The search result disappeared from the visible working surface
after the actor chose its next non-search action.

The root pages collectively exposed 60 of the 77 study identities to each
actor, but not in one invocation. Exposure across separate calls did not become
a durable selected set.

## Direct transcript pattern

The two trajectories are unusually repetitive. Their reasoning repeatedly
announces that it will start by exploring the atlas, inspect the complete study
list, find relevant Q3 XL evidence, then write the memo. Seed 42 successfully
requests root pages 0, 20, and 40 on its first three calls. On call 4 it returns
to cursor 0 and begins the same orientation sequence again. Similar resets
continue through call 32.

Seed 314159 also recognizes the six-stage task, the 32-call limit, and the need
for at least 12 links across eight experiment directories. It repeatedly says
it must be efficient, but the prior navigation program is not present on its
next invocation. It rerequests the root or candidate tree instead of descending
through a study ID obtained moments earlier.

[The direct transcript audit](DIRECT_TRANSCRIPT_AUDIT.md) records the exact
turn-level sequence and interpretation boundary.

## Boundary diagnosis

The primary boundary is **cumulative navigation state**.

This runtime correctly solved several mechanical problems from earlier work:

- exact sources remained externally addressable;
- the prompt remained small (maximum 3,507 prompt tokens);
- no accepted exact result was silently evicted before first delivery;
- current exact content was deduplicated;
- replay was deterministic; and
- the event log remained in custody without being appended to every request.

But it overcorrected transcript accumulation. A paged structural map is useful
only if the actor can retain enough of its traversal to decide where to descend.
The model-visible state contained neither a short phase-local transcript nor a
deduplicated set of observed atlas pages/search results. It also did not retain
the actor's prior plan or reasoning. The latest frontier alone supported one
step of navigation but not an accumulating navigation program.

This is not the same as the previously observed passive-action-basis result.
The missing object here is mechanically grounded: which atlas pages and search
results the actor has observed, which node IDs they contained, and where its
traversal currently is. The host need not infer relevance or preserve a
semantic hypothesis to retain that information.

## What this bank does and does not establish

Supported by this run:

- A root/search hierarchy can be mechanically queried and delivered.
- A standing task plus current exact objects plus only the latest frontier is
  insufficient for this broad, paged research task under the tested package.
- Bounded prompt size alone does not create useful large-world continuity.
- Structural navigation observations are part of the active work surface, not
  merely disposable event history.
- Removing the transcript can produce cheap, low-token loops rather than
  productive selectivity.

Not tested fairly by this run:

- exact-evidence selection among candidate documents;
- multi-hop descent through study, document, and section nodes;
- whether the resulting exact working set would be semantically sufficient;
- whether Q3 XL would accept such a set and stop acquiring;
- construction quality, qualifier preservation, effect/check uptake, repair,
  or closure; and
- whether semantic digests, action bases, hypotheses, plans, or a forced
  construction gate help.

There is no artifact to grade semantically. The unchanged candidate skeleton
is not a failed memo; construction never began.

## Cost

| Episode | Prompt tokens | Cached prompt | Uncached prompt | Completion tokens | Maximum prompt |
|---|---:|---:|---:|---:|---:|
| seed 42 | 93,739 | 55,975 | 37,764 | 2,655 | 3,391 |
| seed 314159 | 94,721 | 57,800 | 36,921 | 4,130 | 3,507 |

The bounded surface prevented context overflow, but both actors spent all calls
restarting orientation. This is an efficiency failure despite low per-call
residency.

## Recommendation

Do not tune eviction, add semantic memory, force construction, or infer a model
selection weakness from this result.

If the large-world question remains a priority, the smallest corrected
successor should preserve **mechanical navigation continuity** while leaving
semantic selection with the model. Two defensible implementations are:

1. retain a short phase-local navigation transcript; or
2. represent observed atlas pages and search results as deduplicated current
   navigation objects, with a separate small structural-residency budget.

The second is the cleaner direct correction because it treats structural pages
like current address-space objects rather than permanent event history. It
should retain each observed `node_id + cursor` page and active search page long
enough for the actor to descend, while preserving exact reopenability and
canonical ordering. It must not add relevance rankings, summaries, or a host
choice of sources.

A corrected successor would be a repair of the information interface, not a
retry of a model failure. It requires a new freeze and authorization. Until
then, the proper verdict is:

> The minimal latest-frontier current-object runtime is too sparse for broad
> paged research navigation. The intended downstream large-world capability
> test remains unanswered.
