# Qwen3.8 recurrent context-reduction horizon v0 — results

Date: 2026-08-20

Status: **completed; recurrent physical operability sustained, construction not reached, late reopen churn observed**

## Executive result

The pressure-triggered, oldest-first, minimum-necessary exact-receipt policy remained mechanically effective through the full authorized horizon. Both seeds completed 12 new model calls without a reserve-preserving capacity failure. The rule resolved every pressure event at which another call was authorized: two frozen starting events and 17 post-call events. Five other post-call results fit without treatment. The two call-12 results were executed and custodied but, by design, were not delivered after the call limit.

This did not converge to construction. All 24 model decisions requested acquisition. There were 15 exact reopens of demoted results and nine other acquisitions; 23 operations were admitted. No mutation, submission, candidate change, or formal short-cycle-thrash episode occurred.

The frozen formal-thrash result needs a behavioral qualification. Seed 42's calls 7–12 were an exact three-action reopen sequence repeated twice:

```text
source-navigation RESULTS
→ source-navigation DIRECT_TRANSCRIPT_AUDIT
→ navigation-continuity RESULTS
→ source-navigation RESULTS
→ source-navigation DIRECT_TRANSCRIPT_AUDIT
→ navigation-continuity RESULTS
```

That is strong descriptive period-three churn, but it falls outside the predeclared formal definition, which required at most two distinct keys in a four-decision window. Seed 314159 moved through four target chunks and then five document reopens, with only the final action repeating within four calls. Both seeds had earlier four-action local nonchurn windows, so the observed pattern is not immediate short-cycle collapse.

The bounded answer is therefore:

> Recurrent minimum-necessary demotion prevented context capacity from ending either trajectory through 12 additional decisions, but it did not produce construction. One seed settled into a clear longer-period reopen loop and the other shifted into repeated reopens without satisfying the frozen thrash criterion. The study supports durable physical operability, not convergence to a productive working set.

## Capacity and lifecycle result

The context limit was 25,088 tokens with 4,096 reserved, so each model request had to remain at or below 20,992 prompt tokens.

| Measure | Seed 42 | Seed 314159 | Total |
|---|---:|---:|---:|
| New model calls | 12 | 12 | 24 |
| Frozen starting demotions | 1 | 1 | 2 |
| Recurrent demotions | 14 | 14 | 28 |
| All message substitutions | 15 | 15 | 30 |
| Starting tokens recovered | 1,607 | 1,545 | 3,152 |
| Recurrent tokens recovered | 20,037 | 21,302 | 41,339 |
| Cumulative tokens recovered | 21,644 | 22,847 | 44,491 |
| Recurrent pressure events resolved | 9 | 8 | 17 |
| Results delivered to new decisions, including predecessor-pending result | 12 | 12 | 24 |

Seed 42 began at 20,907 prompt tokens with +85 reserve-preserving headroom. Its nine treated post-call packets began between -2,263 and -491 headroom and ended between +704 and +1,616. Seed 314159 began at 19,648 with +1,344 headroom; its eight treated post-call packets began between -2,853 and -403 and ended between +774 and +2,182.

No authorized delivery failed. At the frozen endpoint, the two terminal prospective packets were again too large: seed 42 was 22,328 tokens (-1,336 headroom), and seed 314159 was 21,793 (-801). The policy was intentionally not applied because no later model call was authorized. These are endpoint-censored opportunities, not policy failures.

The cumulative 44,491-token figure is lifecycle work, not permanent free space. Reopened or newly read exact bodies re-entered chronology and later became eligible for another receipt substitution. That repeated fault-in/demotion cycle is the central long-horizon systems finding.

## Behavior by seed

| Seed | Novel/other acquisition phase | Later behavior | Frozen formal thrash | Construction / submission | Candidate |
|---|---|---|---|---|---|
| 42 | Four novel target reads through call 6 | Eight exact reopens overall; exact period-three reopen cycle on calls 7–12 | No | 0 / 0 | unchanged |
| 314159 | Four target range decisions plus one rejected continuation request through call 7 | Seven exact reopens; one repeat-within-four at call 12 | No | 0 / 0 | unchanged |

Both trajectories produced a predeclared local nonchurn window: seed 42 at call 6 and seed 314159 at calls 6 and 7. Those windows show bounded noncycling acquisition, not semantic convergence. Each was followed by repeated access to previously demoted governing documents rather than mutation.

The exact reopen path was behaviorally usable 15 times. This is positive evidence for recoverability, but it also shows the policy can create a recurring demand to fault old bodies back into context. The experiment does not determine whether those reopens were semantically necessary.

## Artifact and evaluator result

Initial and terminal candidate IDs were identical in both cells:

`19296f821cc2bf7e32384ec88080ba49aedc4afe1f1f9961c31d57c2e1dc24fd`

No external semantic evaluator was run. There was no candidate transition to evaluate, and scoring the untouched starting artifact as a completed attempt would be misleading. No evaluator or investigator judgment was fed back to the model.

The inherited schema offered `patch`, `replace_file`, and `submit`, but no explicit check action. Zero checks is therefore an action-surface fact, not evidence that the model declined an available checker.

## Cost and cache

| Seed | Prompt tokens | Cached prompt | Uncached prompt | Completion | Serialized total | HTTP time |
|---|---:|---:|---:|---:|---:|---:|
| 42 | 240,676 | 119,988 | 120,688 | 479 | 241,155 | 181.765 s |
| 314159 | 237,318 | 122,207 | 115,111 | 456 | 237,774 | 173.075 s |
| **Total** | **477,994** | **242,195** | **235,799** | **935** | **478,929** | **354.840 s** |

Reported cache reuse was 50.67% overall. Calls immediately following older-prefix rewrites often retained only a shorter common prefix, while calls without a pressure rewrite could reuse nearly the complete preceding prompt. Cache and latency remain descriptive because prompt content and rewritten prefix position changed together.

## Apparatus qualifications

Seed 314159 call 4 requested target lines 34–619 and received an exact transfer-limited slice through line 265. The frozen candidate `read_lines` adapter returned the literal placeholder cursor `standalone-terminal-cursor-not-used`, although the visible tool description promised a usable version-bound continuation cursor. The model requested that cursor on call 5 and received `invalid_or_stale_cursor`. It recovered on calls 6 and 7 by explicitly requesting lines 266–619 and 483–619, respectively. This cost one authorized call and qualifies behavioral comparisons involving that seed. It does not change the capacity-policy receipts or candidate identity.

The predeclared formal-thrash detector was too narrow to label seed 42's exact period-three loop. The post-run label “descriptive period-three churn” is a direct transcript observation, not a retroactive change to the primary metric.

The frozen inference commit's preflight verifier records 26/26 tests passing. All four added post-run analysis/lock/seal tests also pass. Rerunning the complete current 30-test suite after report finalization produces 29 passes and one expected failure: the preflight replay test compares current files with the frozen lock and therefore flags the five declared mutable reports. The post-run verifier instead checks that lock against commit `ca07e84c` and verifies that exactly those five paths changed. Separately, an unscoped `pytest` invocation traversed pinned predecessor tests under `parent_evidence/` and failed during collection because of duplicate module names and predecessor-only imports. These are test-scope/lifecycle qualifications, not measured-run failures.

## Interpretation

Strongest supported interpretation:

The fixed mechanical policy can sustain repeated exact-result delivery much farther than one or two pressure events. It kept both trajectories physically operable for 12 new decisions while preserving the 4,096-token reserve and exact reopenability. Long-horizon use, however, produced repeated fault-in/demotion churn and no construction; seed 42 supplies especially clear evidence in the form of a repeated period-three reopen cycle.

Strongest interpretation weakened by the result:

More decision opportunities under the same capacity policy were not sufficient to cause artifact action within this horizon. The strong claim that recurring minimum-necessary demotion by itself will converge to construction is not supported.

Remaining uncertainty:

- A 12-call continuation cannot establish asymptotic nonconvergence; construction could occur later.
- Tool-only outputs with reasoning off do not reveal whether further reads were judged necessary.
- There is no matched behavioral comparator beyond the sealed boundary.
- The cursor defect reduced seed 314159's usable horizon by one call.
- The study does not compare eviction order, receipt form, pinned objects, or another policy.

No general context manager is promoted, and no successor is selected or authorized by this result.
