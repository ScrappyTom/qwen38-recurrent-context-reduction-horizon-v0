# Frozen long-horizon recurrent context-reduction study

## Question

Beyond the predecessor's three-call window, does repeated pressure-triggered minimum-necessary demotion converge to a stable productive working set, mechanically thrash, or eventually enable construction?

This is a bounded continuation of one fixed policy. It is not a comparison of general context managers and cannot promote a general memory architecture.

## Exact starting states

Each seed starts from its sealed predecessor call-03 request, followed by that exact assistant action and its accepted exact result. The result was custodied by the predecessor but did not cross another model boundary because the frozen three-call endpoint had been reached.

- Seed 42 requested the source-navigation `DIRECT_TRANSCRIPT_AUDIT.md`; the raw next packet is frozen at 22,514 prompt tokens and -1,522 reserve-preserving headroom.
- Seed 314159 requested the source-navigation `RESULTS.md`; the raw next packet is frozen at 21,193 prompt tokens and -201 headroom.

Offline preflight must reconstruct both raw packets exactly, apply the unchanged policy, and prove the first horizon request fits. The first new call therefore observes the exact predecessor call-03 result.

The exact frozen start transformations are:

- Seed 42: replace the oldest eligible full `R031` result at message 19; recover 1,607 tokens; start at 20,907 prompt tokens and +85 headroom.
- Seed 314159: replace the oldest eligible full navigation-continuity direct-audit result at message 17; recover 1,545 tokens; start at 19,648 prompt tokens and +1,344 headroom.

Each treatment changes one old result body. The pending call-03 result remains exact and last in the first horizon request.

## Fixed policy

Policy ID: `pressure_oldest_positive_savings_until_fit_v1`.

1. Trigger only when the prospective request exceeds 20,992 prompt tokens under the exact parent tokenizer.
2. Scan resident action/result pairs oldest first.
3. Skip existing receipts.
4. Substitute an exact reopenable receipt only when exact tokenization shows positive savings.
5. Stop at the first feasible packet.
6. Do not demote the pending result during its own delivery cycle.

No semantic scoring, summarization, deduplication, recent-window eviction, outline demotion, background rewriting, token filler, context enlargement, or reserve reduction is allowed.

## Horizon and stops

- Order: seed 42, then seed 314159.
- At most 12 new calls per seed; 24 total.
- One attempt per seed; zero retries.
- Do not stop merely on mutation or a formal thrash event.
- Stop a seed on admitted submission, inability to restore the response reserve, or its 12-call limit.
- Stop the whole run on provider/runtime/serialization integrity failure or use of an unqualified standalone source surface.
- The final call's result may be executed and custodied but is not called model-visible unless another invocation actually receives it.

## Outcomes

Construction onset means an admitted `patch` or `replace_file`. Closure means an admitted `submit`.

A formal short-cycle thrash episode is four consecutive acquisition decisions, including the direct-predecessor tail where available, on an unchanged candidate, with no more than two distinct canonical action keys and at least one repeat. Repeat-within-four, duplicate acquisition, novel acquisition, exact reopen, and fault-in churn are also recorded mechanically.

A local non-churn window is four consecutive acquisition decisions on an unchanged candidate with four distinct canonical action keys and no exact-receipt reopen. It is evidence consistent with bounded noncycling continuation, not proof of asymptotic convergence or semantic sufficiency.

These labels describe action sequences. They do not assert that further acquisition was unnecessary.

Terminal classes, in precedence order, are apparatus-censored, submission, mutation without submission, formal thrash without mutation, continued acquisition without formal thrash, and other.

## Claim bounds

The run can show whether this exact policy sustains two trajectories longer than three calls and what pressure/action pattern follows. It cannot establish general convergence, semantic sufficiency, or superiority over another policy because there is no matched behavioral comparator after the sealed boundary. Cache and wall-time effects are descriptive.
