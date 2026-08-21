# Qwen3.8 recurrent context-reduction horizon v0

This standalone repository extends the sealed three-call recurrent-reduction trajectories to test whether the same policy eventually converges, mechanically thrashes, or permits construction.

Status: **offline implementation and freeze in progress; no measured inference has been authorized or run in this repository.**

Each seed begins with the exact request, action, and accepted-but-not-yet-delivered result from call 3 of `ScrappyTom/qwen38-recurrent-context-reduction-v0@9a42b85b`. The fixed policy replaces the minimum tokenizer-positive set of oldest resident exact-backed result bodies with reopenable receipts only when a pending exact result would otherwise violate the 4,096-token response reserve. It can run for at most 12 additional model calls per seed.

Offline exact tokenization reconstructed both pressure boundaries. Seed 42 recovers 1,607 tokens by replacing one old result and starts with +85 tokens of reserve-preserving headroom; seed 314159 recovers 1,545 tokens with one replacement and starts with +1,344 headroom.

The study records construction onset, submission, exact reopen/fault-in behavior, duplicate and novel acquisitions, mechanically defined short-cycle thrash, pressure resolution, capacity, cache use, and terminal candidate identity. A formal repetition pattern is not a semantic judgment that a read was unnecessary.

The complete structural outline remains resident. No summary, importance score, fixed recent window, semantic progress state, context increase, or response-reserve reduction is introduced.

Measured execution requires a clean frozen commit and a separate exact commit-specific user authorization.

## Provenance

- Direct predecessor: `ScrappyTom/qwen38-recurrent-context-reduction-v0@9a42b85b4d9fd25bd873d45c08a403c2ca1ff96e`
- Predecessor inference commit: `50e72ba467388bd4c116a5f2b4e5b38f80e820d3`
- Parent evidence: `ScrappyTom/custody-cards-experimental-workbench@40f9afdde9628e4fd5dbd8d18a6fcf85bdf9d820`
- Frozen task source: `f8c93e5ad33c8dd235c418df6561ba022d9077fb`

`parent_evidence/` is a byte-exact tracked snapshot of the direct predecessor. Neither the predecessor checkout nor Custody Cards is modified.
