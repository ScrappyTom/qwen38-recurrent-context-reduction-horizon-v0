# Experimental freeze

Frozen on 2026-08-20 before measured inference.

## Question

At an authentic boundary where historical Prompt N fits but Prompt N plus its requested exact observation does not, can a fixed mechanical reduction of older exact-backed results:

1. preserve the same useful next decision;
2. admit that decision's exact result with the original response reserve; and
3. support one further productive decision?

The optimization target is not minimum tokens. It is reduced residency subject to decision preservation, exact recoverability, result absorption, and response headroom.

## Historical boundaries

- `s42-s1`, turn 12: 20,966 prompt tokens and 26 tokens of headroom after the 4,096 reserve. The model requested target lines 1–6. Appending the exact result yields 21,386 prompt tokens and -394 headroom.
- `s314159-s1`, turn 10: 20,013 prompt tokens and 979 tokens of headroom after reserve. The model requested target region `R031`. Appending the exact result yields 22,037 prompt tokens and -1,045 headroom.

In both trajectories the candidate remained unchanged and no check or submission occurred. The source observations requested at these turns had not yet crossed a model boundary; that is the pressure event deliberately tested here, not an eligibility defect.

## Conditions

The historical control is exact prior evidence: Prompt N, observed action X, exact result X, and the mechanically censored Prompt N+1. It receives no reconstructed model call.

Four measured cells cross two seeds with two frozen policies:

- minimal oldest-first exact-backed receipts;
- exact last-two-result window plus receipts for older results.

The schedule, seeds, model profile, response reserve, equivalence classes, packet bytes, and call limit are frozen in JSON artifacts. No prompt, policy, result, or equivalence rule may change after an outcome appears.

## Primary gates

- `decision_preserved`: first treated action is the exact historical acquisition or the sole predeclared byte-equivalent acquisition for that seed.
- `result_absorbed`: the actual result is appended and the next exact prompt fits while preserving all 4,096 response tokens.

The second decision is descriptive. A mutation or submission is stronger continuation evidence, but is not required to establish result absorption.

## Claim limits

This experiment can support only a local statement about these two trajectories, pressure boundaries, and fixed policies. It cannot validate summaries, semantic eviction, model-controlled residency, chronology compaction generally, or a complete working-set architecture.

The policies do not compare every DROP/COMPRESS/HYBRID family. They compare two understandable exact-backed reduction rules at one authentic pressure type. That smaller scope is intentional.

## Stop rules

- explicit user approval is required after this freeze;
- the exact full model and parent server hashes must verify;
- one attempt and zero retries;
- at most eight measured calls total;
- at most two calls per cell;
- a divergent first action ends that cell;
- a result that cannot preserve the reserve ends that cell before call two;
- any provider, parser, candidate, model, or server invariant failure preserves the run and stops the affected execution;
- no successor is selected automatically.
