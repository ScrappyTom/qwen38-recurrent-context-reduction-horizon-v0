# Frozen recurrent context-reduction experiment

## Question

Can the same pressure-triggered, oldest-first, positive-savings receipt rule repeatedly admit newly requested exact results under the unchanged 25,088-token envelope and 4,096-token response reserve?

This is a test of recurrence at two authentic continuation boundaries. It is not a test or promotion of a general memory system, semantic compactor, eviction controller, or working-set architecture.

## Starting boundaries

The starting state for each seed is the exact predecessor minimal-policy call-02 request plus the exact action that call produced and its exact result:

- Seed 42: `read_region(R030)`, 9,168 exact bytes. Without another reduction, the next packet is 23,353 prompt tokens and has -2,361 tokens of reserve-preserving headroom.
- Seed 314159: `read_region(R032)`, 2,979 exact bytes. Without another reduction, the next packet is 21,521 prompt tokens and has -529 tokens of reserve-preserving headroom.

The historical actions were made before this successor treatment. The first new model call therefore tests actual result absorption and continuation, not preservation of those already-observed decisions.

## Treatment

`pressure_oldest_positive_savings_until_fit_v1` applies only when the exact prospective packet exceeds 20,992 prompt tokens. It scans prior resident action/result pairs in chronology order, skips results already represented by exact receipts, accepts only substitutions with positive exact token savings, and stops at the first feasible packet. The pending result is protected from demotion in its own delivery cycle.

At the first recurrent boundary this mechanically produces:

- Seed 42: demote result messages 9 and 11; recover 2,998 tokens; call-01 packet 20,355 tokens / +637 headroom.
- Seed 314159: demote result message 9; recover 1,746 tokens; call-01 packet 19,775 tokens / +1,217 headroom.

The complete 4,123-token structural outline remains resident.

## Continuation and stop rules

- Three new model calls per seed; six total maximum.
- One attempt per seed; zero retries.
- Execute and custody every valid action result.
- Before a later result is delivered, apply the same rule only if actual pressure recurs.
- Stop a cell on admitted submission, inability to restore the reserve, or the three-call limit.
- Stop the entire run on provider/runtime/serialization failure or an unqualified standalone source-surface request.
- Do not change prompts, policy, schedule, tools, budgets, or seeds after an outcome appears.

The last call's action result may be executed and custodied but is not described as model-visible when the call limit prevents another invocation.

## Measures and claim bounds

Primary mechanical measures are the number of exact results that cross into later model decisions and the number of recurrent pressure events resolved. Action class, exact reopen, mutation, submission, candidate effects, token occupancy, cache use, and latency are secondary.

Only the first absorption boundary has a mechanical untreated control. There is no matched untreated behavioral trajectory after treatment begins, so later behavior is descriptive. Cache and latency observations are descriptive and confounded by prefix changes.

Physical capacity restoration does not establish that further reads were unnecessary. A no-mutation result leaves legitimate information demand and acquisition-stopping/action-commitment weakness unresolved.
