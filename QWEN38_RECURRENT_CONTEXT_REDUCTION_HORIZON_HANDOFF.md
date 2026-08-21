# Qwen3.8 recurrent context-reduction horizon handoff

Implement and run a standalone, exact continuation of `ScrappyTom/qwen38-recurrent-context-reduction-v0@9a42b85b4d9fd25bd873d45c08a403c2ca1ff96e`.

The narrow question is whether the already-tested `pressure_oldest_positive_savings_until_fit_v1` rule, continued beyond three calls, converges to a stable/productive working set, exhibits mechanically defined repeated cycling, or eventually produces construction.

Use the two sealed call-03 requests and their exact accepted results. Apply no new context policy. Preserve the 25,088-token context, 4,096-token reserve, model profile, seeds, tools, task, candidate, structural outline, and source surface. Permit at most 12 additional calls per seed in fixed order, one attempt, zero retries. Continue after mutation and after formal thrash; stop on submission, capacity-restoration failure, call limit, or apparatus integrity failure.

Record exact requests/responses, actions/results, candidates, pressure projections, token/caching/runtime receipts, reopens, duplicate/novel acquisitions, short-cycle thrash, mutation, and submission. Keep mechanical sequence labels separate from investigator judgments about information sufficiency.

Do not launch measured inference without a clean frozen commit and explicit authorization naming that commit. After execution, replay, seal, directly audit every turn, publish the result, and stop without automatically selecting a successor.
