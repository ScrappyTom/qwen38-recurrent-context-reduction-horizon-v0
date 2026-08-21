# Qwen relation-to-action working model

Date: 2026-08-17

Status: **evidence-bounded engineering model; not a claim about hidden cognition**

## Purpose

This document records the smallest behavioral model that explains the current
Qwen3.6-27B and Qwen3.8-27B evidence well enough to guide experiments. Every
result must name its actual package; observations shared here are not assumed
to transfer merely because both packages are Qwen. “Psychology” means
repeatable model-visible input/output behavior. The repository has no access
to the model's hidden mental state, and no result should be presented as proof
of an internal cognitive mechanism.

The model is:

```text
available information
        ↓
claim ↔ evidence discrimination
        ↓
active obligation selection
        ↓
local action
        ↓
artifact recomposition and closure
```

These are distinct capability boundaries. Success at one does not imply
success at the next.

## Supported observations

### 1. Availability is weaker than use

Exact task text, complete source files, current candidate facts, checks, and
review results have repeatedly been present without governing the deciding
action. More factual projection is therefore not a general remedy. This is
supported across the projection, review-surface, model-package, paper, and
creation results indexed in [`EXPERIMENT_INDEX.md`](EXPERIMENT_INDEX.md).

### 2. Aggregation can lose relationships the model can express locally

The heat-response section assessor received all four claims and all four
records. Its explanation named missing H1/H3 relationships, but its exhaustive
applicable-ID field copied only the existing H4 citation and omitted H2. When
the same fixture was decomposed into 16 stateless one-claim/one-record calls,
Qwen returned the frozen four-positive/twelve-negative matrix exactly.

This supports a narrow claim: removing simultaneous cross-claim comparison and
list maintenance can expose relationship discrimination that a section-level
output loses. It does not show which aggregation demand caused the loss, and it
does not make every atomic judgment correct.

Evidence:

- [`experiments/reviewer-frame-factorial-v1/QUALIFICATION_RESULT.md`](experiments/reviewer-frame-factorial-v1/QUALIFICATION_RESULT.md)
- [`experiments/atomic-claim-binding-v0/QUALIFICATION_RESULT.md`](experiments/atomic-claim-binding-v0/QUALIFICATION_RESULT.md)

### 3. A correct relationship can remain operationally inert

A qualified binary reviewer correctly found a citation-support defect, yet the
builder immediately finalized the same candidate. Fresh reviewing editors
reacquired the artifact and evidence but also made no change. A relationship
represented in prose or a structured field is not automatically selected as
the next work obligation.

Evidence:

- [`experiments/binary-submission-review-v0/RESULTS.md`](experiments/binary-submission-review-v0/RESULTS.md)
- [`experiments/reviewer-seat-calibration-v0/RESULTS.md`](experiments/reviewer-seat-calibration-v0/RESULTS.md)

### 4. The active task/action frame can select among valid uses of evidence

In the first atomic edit calibration, each call received one exact claim, its
one correct supporting record, the prior `supports` result, the record's
declared citation handle, and the unchanged six-requirement task. Qwen used H2
to add a confidence interval and p-value and used H3 to add exact completeness
rates, but added none of the three missing citations.

The only model-facing addition in the adaptive follow-up was the task's
existing citation requirement marked as `active_local_obligation`. Qwen then
added H2, H1, and H3 exactly and preserved the already-correct H4 claim. The
pair carried defensible content; the active obligation selected what operation
to perform with it.

This is a strong known-fixture calibration, not transferred performance
evidence, because the obligation treatment was chosen after observing the
first failure.

Evidence:

- [`experiments/atomic-claim-edit-v0/RESULTS.md`](experiments/atomic-claim-edit-v0/RESULTS.md)
- [`experiments/atomic-claim-edit-focus-v0/RESULTS.md`](experiments/atomic-claim-edit-focus-v0/RESULTS.md)

### 5. Responsibility scope can change whether recognized information reaches mutation

On the independent heat-response fixture, whole-artifact reviewing editors
read the same complete information and finalized unchanged. Both editors
assigned responsibility only for Policy Implications reread and edited it.
The edits were partial, so this is an action-frame lead rather than a complete
solution. The earlier factorial showed a related but less stable interaction
with passed-check visibility.

Evidence:

- [`experiments/reviewer-frame-factorial-v0/RESULTS.md`](experiments/reviewer-frame-factorial-v0/RESULTS.md)
- [`experiments/reviewer-frame-factorial-v1/RESULTS.md`](experiments/reviewer-frame-factorial-v1/RESULTS.md)

### 6. Atomic semantic judgments can still be locally wrong

The prospective school-start transfer used the unchanged one-claim/one-record
matcher. It returned 15 of 16 frozen relations correctly but claimed that H2's
tardy-arrival outcome rates directly supported a claim about attendance-scan
completeness. H2 contained no completeness measure. The model invented a
plausible bridge between related domain concepts while also correctly
accepting H3's actual 74%/94% completeness data.

The frozen gate therefore made zero editor calls. Atomicity removed list and
cross-claim state, but it did not make the model-authored binding authoritative.

Evidence:

- [`experiments/atomic-work-item-transfer-v0/RESULTS.md`](experiments/atomic-work-item-transfer-v0/RESULTS.md)

### 7. Structured protocols preserve shape and custody, not semantic truth

Schema-constrained outputs have been valuable because they preserve exact IDs,
make rejections factual, and prevent transport ambiguity. They have also
carried incorrect labels, incomplete maps, and semantically wrong bindings
without a protocol error. Executability and semantic correctness remain
separate.

### 8. Correct bindings can support useful local action without an assigned obligation

The prospective street-dimming comparison supplied six task-author-correct
bindings on a new fixture. Both the full-task condition and the otherwise
identical active-obligation condition corrected the central defect in all five
flawed units and preserved the correct unit byte for byte. Both graded 3 pass /
3 partial / 0 fail. The obligation object changed two phrasings but no grade
and added 14.96% total tokens.

The result reverses the broad reading of the adaptive heat-response
calibration. An explicit active obligation can redirect one known failure, but
it did not transfer as a general local-action aid. Correct binding plus atomic
scope was the useful common input here. Even then, Qwen omitted secondary
pass-level qualifiers from three records, so local action remained incomplete.

Evidence:

- [`experiments/gold-bound-local-action-v0/RESULTS.md`](experiments/gold-bound-local-action-v0/RESULTS.md)

### 9. Pairwise discrimination can succeed after the pair is isolated

On a fresh 16-pair water-leak-alert family, the atomic producer recovered all
eight direct bindings and rejected all eight high-risk negatives. Its eight
positive quotes were literal and semantically adequate. The negatives covered
wrong measure, missing precision, subgroup/overall mismatch, absence presented
as no effect, superseded evidence, reversed bias direction, genuine no
support, and observational evidence presented as causal.

The producer did not search a corpus or decide which claims needed evidence.
It received one already-isolated claim and one complete candidate record. A
separately reset verifier received only correct proposals, corrected none, and
introduced the sole wrong decision. This supports atomic comparison as a
qualified primitive, not a model-authored evidence map or two-model truth
certificate.

Evidence:

- [`experiments/binding-source-qualification-v0/RESULTS.md`](experiments/binding-source-qualification-v0/RESULTS.md)

### 10. Exact artifact inventory supported candidate recall; subspan grounding remained separate

On a fresh six-claim/eight-record corpus, a model-owned selector received one
claim plus the complete unranked record artifact with document, version,
section, byte-range, status, and hash identities. It proposed exactly the five
gold pairs and no others. Correct record positions were nonmonotonic. The
unchanged atomic producer then classified all 48 relations correctly with zero
false positives.

The full producer contract still failed: one of five exact positive quotes
omitted the record's final-audited and heat-alert-day qualifiers. The whole
record supported the claim; the narrower selected span did not cover every
material element. Candidate formation, record-level relation, and supporting
subspan are therefore empirically separable.

Evidence:

- [`experiments/candidate-pair-recall-transfer-v0/RESULTS.md`](experiments/candidate-pair-recall-transfer-v0/RESULTS.md)

### 11. Record-level candidate formation and relation judgment replicated

On a fresh eight-claim/twelve-record family, the full-catalog selector recalled
all six direct records and proposed one extra record that explicitly said the
unsupported outcome was not measured. The separate record-relation producer
got all sixteen frozen pairs right—six direct and ten high-risk negative—and
rejected that extra. The joined candidate pipeline exactly matched the author
binding set.

The selector repeated all twelve records for every claim and consumed 26,096
tokens, so this is a small-corpus capability result rather than an economical
retrieval design. No quote was required. Because this was a fresh replication,
not a matched quote/no-quote comparison, it qualifies the simpler interface but
does not prove that quote removal caused the result.

Evidence:

- [`experiments/record-level-binding-replication-v0/RESULTS.md`](experiments/record-level-binding-replication-v0/RESULTS.md)

### 12. Obligation role did not make multi-clause local action exhaustive

On a fresh six-unit library-hours fixture, worker preparation and an
independent reviewer received byte-identical unit, evidence-binding, and task
catalog data. They selected the same requirement IDs for all six units and
matched the frozen assignment on all five flawed units. On the no-op, both
selected numerical fidelity R4 instead of preservation R1; direct review found
both requirements applicable, and both actor variants preserved the line
exactly.

The task-author control and both model-source mappings produced identical final
unit sets: 1 pass / 5 partial / 0 fail. Each flawed unit's central defect was
corrected, but one supplied qualifier was omitted despite an exact active
obligation that named it. The independent role supplied no advantage, and
obligation source did not explain the remaining local loss.

Evidence:

- [`experiments/obligation-source-comparison-v0/RESULTS.md`](experiments/obligation-source-comparison-v0/RESULTS.md)

### 13. Sequential clause actions were worse than one complete local frame

On a fresh six-unit mobile-clinic fixture, both conditions received the same
exact unit, record, binding, task-author clauses, prompt, schema, and model.
The compound condition saw all applicable clauses in one call and graded 5
pass / 1 partial / 0 fail. The sequential condition saw one clause at a time
against exact predecessor versions and graded 4 pass / 1 partial / 1 fail at
2.51 times the total tokens.

The micro path did not lose any clause after it first became satisfied. Instead,
it copied two late clause imperatives into the artifact and retained a source
contradiction while adding the requested disclaimer. Exact state succession
therefore preserved what happened without making repeated local construction
semantically safe. The strong compound result makes a complete local clause
packet a lead, but its incremental value over a no-packet input remains
unmeasured.

Evidence:

- [`experiments/versioned-clause-action-v0/RESULTS.md`](experiments/versioned-clause-action-v0/RESULTS.md)

### 14. Explicit semantic content reduced local loss; typed form did not explain it

On six fresh matched-world units, evidence-only selected every central pair
direction but satisfied only 12/22 required-content items. Adding a complete
task-author local payload as prose raised this to 20/22; supplying the exact
same payload as structured JSON reached 21/22. Both preserved the no-op and
made no unit worse.

Neither frame completed all six units. Both omitted the explicit U004
`does not exaggerate` contrast even though it was present in the frame. Four
of six prose/structured outputs were byte-identical, and structure improved
only U003. This makes explicit local semantic content a transfer lead while
leaving representation-specific value and guaranteed execution unproven.

Evidence:

- [`experiments/semantic-frame-representation-v0/RESULTS.md`](experiments/semantic-frame-representation-v0/RESULTS.md)

### 15. The prose semantic-content effect replicated, including its limit

On a new regional-asthma fixture with the prior prompt, schema, semantic
classes, and model policy held fixed, evidence-only produced 3 pass / 3 partial
and 13/22 items. Prose produced 5 pass / 1 partial and 21/22 items. It improved
two unit grades, added eight items, regressed none, preserved the no-op, and
retained all central pair directions.

The high-score missingness unit again omitted the explicit `does not
exaggerate` relation. Across both fixtures, prose added four passing units and
sixteen satisfied items without regression, but never completed all six units.
This prospectively replicates the upstream semantic-content effect while also
showing that visible itemization is not an execution guarantee.

Evidence:

- [`experiments/semantic-frame-content-replication-v0/RESULTS.md`](experiments/semantic-frame-content-replication-v0/RESULTS.md)

### 16. Broad semantic continuity altered behavior but did not improve action

The destructive-boundary study gave Phase A two complete three-record
dossiers while hiding the later claim. Qwen's notes retained 14/22 frozen
items, but lost exact qualifiers, W02 handles, negative contrasts, and
availability details. W01 also invented primary/secondary outcome labels.

After a fresh request boundary, retrieval-only produced 13/22 action items,
model-summary carryover 8/22, and complete oracle carryover 11/22. Oracle was
not inert: it cut reads from six to two, preserved one intended no-op, and
produced the only complete U004 action. It also induced immediate unchanged
submission on U001 despite visibly containing every needed relation. On U005
it converted a complete bias chain into the same gist-only claim as the other
arms. Model-summary U006 reread the exact source but then repeated the note's
omission.

This separates persistence from local framing. A broad carried note can alter
retrieval and sufficiency judgments without reconstructing the branch-local
action surface that produced the earlier 20/22 and 21/22 results. One frozen
no-op/action-item conflict limits U003, but the capture and oracle gates fail
independently.

Evidence:

- [`experiments/semantic-continuity-boundary-v0/RESULTS.md`](experiments/semantic-continuity-boundary-v0/RESULTS.md)

### 17. A complete adjacent relationship paragraph still collapsed to gist

The next experiment removed the destructive reset and broad dossier. Each
fresh action already had the exact task, one evidence record, current target,
task-author binding, and one adjacent relation object. Qwen first authored the
model relations in six separate calls. They preserved exact identities but
captured only 10/22 semantic items and falsely classified U001's observational
target as already aligned with randomized evidence.

Direct action reached 4/22 frozen items. Model-relation action reached 5/22 and
regressed U001; among flawed units, only one of seven correctly captured
relation items appeared in the next action. The stronger diagnostic is the
positive control: a complete 22-item task-author relationship paragraph still
reached 4/22, improved no unit, and regressed U006 by turning absent
measurement into an unsupported no-effect claim.

This stops the paragraph representation and prevents attributing the action
failure solely to model-authored capture. The earlier 20/22 and 21/22 local
frames were not ordinary paragraphs: they presented each required relation on
its own ID-bearing line. That makes action-time itemization/segmentation a
plausible representation lead, but only across different fixtures. It remains
to be isolated prospectively with content-equivalent arms.

Evidence:

- [`experiments/model-authored-local-relation-v0/RESULTS.md`](experiments/model-authored-local-relation-v0/RESULTS.md)

The content-equivalent factorial then attempted that isolation on a fresh
heat-pump family. It was mechanically clean but failed its prospective
interpretability gate: evidence-only represented only 3/5 central revision
directions. Paragraph, newline-delimited, and opaque-ID conditions each reached
7/22 conjunctive action items. Newline delimiting changed no grade or item over
the paragraph. Opaque IDs changed U001 from fail to partial, but added no
complete action-item group. Because the evidence-only control sometimes copied
the target across a direct evidence contradiction, the run cannot isolate
secondary-item retention from the more basic decision to revise.

This neither establishes nor refutes an itemization mechanism. It does remove
the basis for immediately advancing from the cross-fixture lead to
model-authored items. The exact behavior and failed gate are in
[`experiments/semantic-itemization-factorial-v0/RESULTS.md`](experiments/semantic-itemization-factorial-v0/RESULTS.md).

### 18. Action role and repeated identity did not recover exhaustive use

The follow-up held the same 22 ID-bearing item strings fixed across a fresh
eligible 2 x 2 experiment. It changed only whether they were declared exact
reference content or content every final unit must satisfy, and whether exact
artifact/version/evidence identities were repeated beside them.

Reference-unbound reached 10/22 items, reference-bound 9/22,
obligation-unbound 13/22, and obligation-bound 11/22. The obligation role made
the U006 measurement boundary operational in both binding states. It did not
prevent missingness-chain compression, did not make U001 complete, and with
repeated binding caused U001's incorrect observational target to be preserved
unchanged. Repetition improved no grade and added about 13% tokens.

This is stronger than an ineligible format null: the control instantiated the
planned failure regime. It means the older 20/22 and 21/22 gains cannot be
explained by a required-content label or repeated identity alone in this
representation. It does not identify the older frame's active ingredient, and
it provides no basis for inferring internal attention or obligation slots.

Evidence:

- [`experiments/action-role-binding-factorial-v0/RESULTS.md`](experiments/action-role-binding-factorial-v0/RESULTS.md)

### 19. Semantic possession, action expression, and world effect are separate

The local 1K/2K/4K creation ladder and adjacent Experiments 105-108 establish
a recurrent pre-candidate boundary. Added response allowance can turn an
otherwise truncated selected mutation into an admitted candidate. Once that
boundary is removed, represented requirements can still disappear from code,
visible-green artifacts can remain incomplete, and closure can still fail.

Staging did not supply a general bridge. Transactional previews were committed
unchanged, a correct precommit handoff was ignored by the next action, forced
operation selection repeated the same failed check, optional inspection was
never selected, and chunk assembly added rejection-driven recovery at high
cost. Exact section replacement did earn a narrower mechanical result:
protected bytes and candidate scope were preserved while the same semantic
binding remained missing in both section and whole-document conditions.

Adjacent Experiment 111 supplies the matching relation-to-action case. Exact
relation-plus-operand context enabled one conjunctive repair, but met its
benefit rule in only one of three prospective states; in another state a
richer frame accompanied an oversized action that never executed. This is
evidence for externally separate boundaries, not a claim that context caused
an internal overload.

The model and sampler profiles differ across the repositories, so these counts
are not pooled. The direct evidence map and qualifications are in
[`ACTION_SURFACE_EVIDENCE_RECONCILIATION.md`](ACTION_SURFACE_EVIDENCE_RECONCILIATION.md).

### 20. Mutation menus can change action organization without changing final quality

A direct `W/U/M` pilot held exact task, source, target, model settings, response
allowance, reads, checks, and submission fixed on a localized repair, coupled
repair, and moderate construction. Every cell ultimately passed. There was no
forced quality difference for a mixed policy to exploit.

The mixed model nevertheless chose bounded replacement for both repairs and
whole replacement for construction. That was not global cost optimization: the
coupled mixed path used 47,270 tokens while whole-only used 11,742. Conversely,
the construction choice tracked the efficient whole path. The action menu is
therefore visibly part of the decision environment, but one deterministic
choice per state cannot establish a stable selection policy.

The unit construction also separated first-action quality from terminal
quality. Its first complete candidate used `ValueError` instead of the literal
`TypeError` obligation and graded 10/13. One expected/observed check case made
the mismatch local; the next unit replacement fixed all three validation
cases. The whole-construction paths represented the exception class on their
first candidates.

One cost cell is mechanically qualified. Two unit bodies with a trailing
newline were rejected by a host rule absent from the declared tool contract.
The rejection was truthful and recoverable, but those calls are not evidence
of model difficulty or intrinsic unit cost.

Evidence:

- [`experiments/action-affordance-selection-v0/RESULTS.md`](experiments/action-affordance-selection-v0/RESULTS.md)

### 21. Edit density did not make mixed mutation selection adaptive

The matched successor fixed the prior undeclared newline rule and nested one,
three, and five defective units inside the same 1,385-byte candidate shape.
Every state retained identical W/U/M reads, checks, submission, response
allowance, and external grader. The first-check candidate was graded before
feedback.

Mixed chose unit replacement first at all three densities. First-check scores
tied within every state, while terminal W and U passed all three and mixed
failed the single-defect state. In that failure, Qwen reproduced all five
original unit bodies as admitted exact no-ops, received two literal
expected/observed mismatches and `passed: false`, then submitted C000 unchanged.
Forced U saw the same receipt and repaired; forced W had checked first and also
repaired.

The menu therefore affected how work was serialized and closed, not merely the
set of legal effects. It did not supply a density-sensitive selector. Whole was
cheapest in all three matched states, but the small candidate and easy whole
payload prevent a universal granularity conclusion.

Evidence:

- [`experiments/edit-density-affordance-v0/RESULTS.md`](experiments/edit-density-affordance-v0/RESULTS.md)

### 22. Operation labels did not create a substantive geometry interaction on one-to-one tasks

The first direct Track A screen crossed transfer, comparison, and construction
with source-led, integrated-relation, aligned-relation/object, and independent-
obligation views. All 36 one-shot calls admitted and replayed.

Direct review found all 216 substantive source-rule items and all 72 comparison
verdicts correct. Two transfer cells omitted their six required source handles,
and one obligation-framed construction appended a stray brace. The frozen
lexical scorer badly undercounted semantic-arm paraphrases; those scores are
retained as an instrument defect rather than model failure.

The deeper result is about task structure. “Construction” still meant six
independent source-to-sentence mappings, so Qwen could copy exact sources. It
did not require several facts to govern one output decision. Added semantic
views used 17.48% to 33.28% more tokens and often produced byte-identical
artifacts. No projection profile is earned. Information-operation studies must
vary the dependency graph, not merely name a different operation.

Evidence:

- [`experiments/information-operation-geometry-v0/RESULTS.md`](experiments/information-operation-geometry-v0/RESULTS.md)
- [`experiments/information-operation-geometry-v0/AUDIT.md`](experiments/information-operation-geometry-v0/AUDIT.md)

### 23. High-fan-in synthesis benefited from an oracle coverage specification; simple exact-object grouping did not form a profile

The dependency-topology successor held exact source and target bytes fixed
across natural documents, addressable records, task-author grouping, and
task-author output obligations. All 24 calls admitted and replayed, followed by
sealed human rubric review.

Aligned exact objects beat addressable records in only 1/3 conjunctive worlds,
so simple grouping of a decision's concrete objects was not a reliable
comparison geometry. This arm did not include an explicit governing relation
and therefore does not reject relation-plus-operands. In contrast, task-author
obligations beat aligned objects in both
eligible many-to-one synthesis worlds: 14/14 versus 9/14 and 13/14 versus
8/14. Obligations were semantically no worse across every eligible cell and
also improved exact provenance in several cells.

The treatment was not neutral. It added the correct semantic decomposition,
individuated clauses, exact `based_on` records, and an output-duty role at
once, effectively externalizing an oracle coverage set. It used 25.63% more
tokens than aligned objects and exceeded the
130-word synthesis limit in two worlds. Two obligation artifacts still cited
an unassigned distractor, and conjunctive outputs could still strengthen
`can` into certainty. The result supports a temporary local specification as a
positive control, not host-generated semantics or a runtime selector.

Evidence:

- [`experiments/dependency-topology-geometry-v0/RESULTS.md`](experiments/dependency-topology-geometry-v0/RESULTS.md)
- [`experiments/dependency-topology-geometry-v0/AUDIT.md`](experiments/dependency-topology-geometry-v0/AUDIT.md)

### 24. Content-equivalent clause geometry was not qualified; item and role wrappers showed no stable descriptive advantage

The next study held eight task-author clause strings, their IDs, order,
evidence bindings, exact source, current target, task, action, model profile,
and output allowance fixed. It varied only exact source, one integrated
semantic account, independent neutral items, and independent output
obligations. The neutral and obligation views differed in one declared `kind`.

All 16 calls admitted and replayed, and an independent condition-blind reviewer
scored all 144 semantic/provenance judgments. Only one of four exact-source
controls met the preregistered central-gist/secondary-loss phenotype. The
experiment is therefore formally ineligible and cannot establish any causal
view ordering.

The descriptive pattern still constrains the working model. Integrated
content scored 58/64 semantic points, independent items 55/64, obligations
56/64, and exact source 40/64. Independent items exceeded integration in one
world and obligations exceeded neutral items in one. Several semantic arms
still strengthened possibility into categorical bias language or cited a
weather distractor. This weakens the claim that separate containers or an
obligation label alone make correct semantic content operational. It leaves
correct external semantic decomposition as an oracle control, not a runtime
primitive.

Evidence:

- [`experiments/semantic-clause-geometry-v0/RESULTS.md`](experiments/semantic-clause-geometry-v0/RESULTS.md)
- [`experiments/semantic-clause-geometry-v0/AUDIT.md`](experiments/semantic-clause-geometry-v0/AUDIT.md)

### 25. Executed failure truth improved salience, but representative repair could break an unexecuted sibling

Five saved Qwen3.8 candidates received their complete task, exact source,
complete task-author packet catalog, and literal host-executed
expected-versus-observed receipts. All 37 responses were admitted schema
actions without truncation. Qwen made a related mutation for 11/12 disclosed
failures. On the frozen packet programs, 35/47 became 40/47.

Direct source/terminal review exposed a wider boundary. The broad packet
purposes sampled only some written sibling cases. A qualified offline audit
mapped the task contracts to 180 independently scored predicates, passed all
180 on the task-author goldens, and ran 307 matched source/terminal comparisons
across the five measured pairs. It found 11 fixes, five regressions, and a net change from
254/307 to 260/307. No terminal passed the complete audit.

Both Session actors fixed the observed empty-user case by changing a combined
wrong-type-or-empty branch to `ValueError`, thereby regressing wrong-type users
from `TypeError`. The seed-42 Config actor made the same exchange for keys in
two operations. Priority Catalog fixed one category-position behavior while
breaking replacement-established category order. The nominal 10/10 Session
candidate was therefore packet-complete, not task-complete.

This sharpens two existing observations. Exact executed truth can make the
relevant area operationally salient. It does not ensure preservation of the
local contrast or construction of a persistent history representation. It
also shows why grouped presentation and independently scored predicates must
remain separate: one efficient model call need not imply one aggregate truth
value.

Evidence:

- [`experiments/executed-receipt-correction-v0/RESULTS.md`](experiments/executed-receipt-correction-v0/RESULTS.md)
- [`experiments/executed-receipt-correction-v0/DIRECT_TRAJECTORY_AUDIT.md`](experiments/executed-receipt-correction-v0/DIRECT_TRAJECTORY_AUDIT.md)
- [`experiments/executed-receipt-correction-v0/contract_audit/RESULTS.md`](experiments/executed-receipt-correction-v0/contract_audit/RESULTS.md)

### 26. Opportunity, verification coverage, and verification uptake are separate boundaries

The Qwen3.8 Priority Catalog continuation resumed three call-10 checkpoints
with the exact prior messages and candidates. Only the disclosed total call
allowance changed.

The no-receipt branch submitted unchanged on call 11. Its narrow visible check
had already organized the trajectory around closure, so additional opportunity
was unused. The final-receipt branch was genuinely censored: it reread,
connected previously created order state to the public operations, repaired
the named temporal target, and submitted on call 17. Its saved contract audit
moved from 41/53 to 46/53, with one clear regression and one process-sensitive
ordering predicate. The trace branch remained active longer, but moved only
42/53 to 44/53 by call 20. Calls 21–26 consumed another 144,500 reported
tokens, changed no audited predicate, repeated the same visible failure twice,
and ended in submission despite `passed:false`.

This separates three externally observable states:

1. **opportunity-limited work**: a coherent mechanism is still being assembled
   when the apparatus stops;
2. **verification-coverage failure**: the model closes on a passing check that
   does not expose remaining task defects; and
3. **verification-uptake/action-binding failure**: an exact failed check is
   visible, but further actions do not implement the needed relation.

Additional calls can repair the first state. They do not mechanically reopen
the second and can prolong the third. At the original cutoff, trace appeared
to beat final-only on temporal targets 2/3 versus 1/3. At natural submission
they tied 2/3 versus 2/3, so the cutoff ranking was not a stable treatment
result. The model-facing information changed not only content but the pace and
organization of work.

Evidence:

- [`experiments/receipt-information-campaign-v0/continuation/RESULTS.md`](experiments/receipt-information-campaign-v0/continuation/RESULTS.md)
- [`experiments/receipt-information-campaign-v0/continuation/DIRECT_TRAJECTORY_AUDIT.md`](experiments/receipt-information-campaign-v0/continuation/DIRECT_TRAJECTORY_AUDIT.md)

## Operational model

For this class of work, the most useful current hypothesis is:

> Qwen behaves as a conditional local reasoner whose selected operation is
> influenced by the assigned comparison, responsibility boundary, and explicit
> local semantic content. An
> explicit obligation can redirect a known failure but is not reliably useful
> prospectively. A content-equivalent follow-up did not qualify enough
> untreated worlds to compare integrated, itemized, and obligation forms, and
> its descriptive results did not favor either wrapper consistently. When
> independently scoped oracle duties are local to a
> high-fan-in synthesis action, they can preserve substantially more secondary
> detail than exact source grouping alone, although they increase expression
> cost and do not eliminate provenance or modality errors. The model may
> recognize a fact without preserving an
> exhaustive relationship, preserve a relationship without acting on it, or
> make the central local correction while omitting secondary requirements from
> the same record. A literal failed receipt can focus mutation on the observed
> case while the resulting edit breaks an unexecuted sibling distinction. A
> complete local frame can support more exhaustive one-shot
> construction, while its typed serialization has not shown a distinct value
> and it can still lose an exact visible relation. Serializing clauses across
> actions can create instruction-copying and contradiction-preservation
> failures. Carrying broader semantic state across a reset can reduce source
> reopening while also causing premature sufficiency; it does not automatically
> recreate a focused local action frame. Even a complete relationship paragraph
> beside exact local operands can collapse to the same central gist. Separately
> itemized action-time views remain a bounded cross-fixture observation. A
> first representation factorial failed its untreated control gate; a second,
> eligible factorial found that neither a required-output role nor repeated
> exact scope recovered the earlier effect and that their combination could
> regress a central correction. When whole and bounded mutation are both
> available, it can select different forms across work shapes, but that
> selection has not shown a terminal-quality advantage or reliable global cost
> optimization. In a matched density family it instead remained unit-first at
> all three densities, performed exact no-op rewrites, and once submitted after
> literal failed-check truth. Construction form can still change the quality of
> the first complete candidate before verification repairs it. On small
> explicit one-source/one-output units, however, exact source content can be
> sufficient for complete transfer, comparison, and construction; richer
> semantic views may change provenance-handle compliance or expression noise
> without changing substantive content. An operation name is therefore not a
> useful proxy for the actual information-dependency structure. Action
> opportunity is another independent boundary: a useful mechanism may still
> be unfinished at a fixed cutoff, while an already-closing branch will ignore
> more opportunity and a stuck branch can spend it repeating an ineffective
> mechanism. Passing verification can induce false closure when coverage is
> narrow; failed verification can be exact yet remain operationally unused.
> In a later matched scout, replacing a four-case green receipt with complete
> task-derived execution results improved all three qualified false-closure
> candidates and fixed six of nine disclosed failures without regression.
> One actor still compressed five failures into two successful fixes plus one
> ineffective validation edit, then closed on the unchanged narrow check.
> A held-out replication then found a broader but weaker pattern: complete
> evidence activated mutation in 6/6 branches and gained seven predicates, but
> beat the narrow control in only 3/6 pairs, below its 4/6 gate, at 2.59 times
> the tokens. One apparent no-regression tie concealed two fixes and two
> regressions inside an already-failing grouped predicate. Automatic current
> complete audits then won only 1/5 common-prefix pairs and tied four at 3.05
> times the static condition's tokens. One branch progressed from 7/12 to
> 12/12 under successive exact audits, but another oscillated between
> type/value errors, one received an inert audit, and another authored the
> correct missing guards while repeatedly failing the exact patch-basis field.
> Current truth can improve selection without surviving action expression or
> effect, and repeated truth can sustain nonprogress.

This is more precise than “the model needs more context” or “truth is not
enough.” It identifies four separable semantic questions:

1. Was the relevant information available?
2. Was the claim–evidence relation formed correctly?
3. Was the intended task obligation selected?
4. Did the local action and final composition satisfy it without regression?

Every experiment must also report four interface/effect questions rather than
folding them into task quality:

5. What operation and scope did the model select?
6. Did the response fit, parse, validate, and become an admitted action?
7. What exact candidate or world effect did that action produce?
8. Did returned verification distinguish the remaining defect, and how did
   the model close afterward?
9. Was the endpoint chosen by the model or imposed by the apparatus?
10. Across additional opportunity, which predicates changed, which regressed,
    and where did marginal work become ineffective?

The current empirical decomposition is:

```text
claim inventory
→ candidate record generation / recall        [5/5 at 6 × 8; 6/6 at 8 × 12]
→ one-claim / one-record discrimination       [48/48 matrix; 16/16 fresh fixed set]
→ optional supporting subspan                 [4/5 complete on transfer]
→ active obligation selection                 [5/5 flawed-unit assignments; no role difference; no-op gold nonexclusive]
→ exact local action                           [single obligation: 0/5 strict edited-unit passes; prose semantic content: 5/6 on two fixtures; sequential micro: 4/6]
→ destructive semantic continuity             [model capture 14/22; retrieval 13/22 action items; model state 8/22; oracle 11/22]
→ adjacent relationship paragraph             [model capture 10/22; direct 4/22 action items; model 5/22; oracle 4/22]
→ content-equivalent item representation       [ineligible: evidence control only 3/5 central directions; paragraph/lines/IDs all 7/22]
→ action role x repeated binding                [eligible: 10/22, 9/22, 13/22, 11/22; neither factor qualified]
→ whole/unit/mixed mutation affordance          [9/9 terminal pass; 0/3 forced quality differences; mixed used both forms]
→ matched edit-density affordance               [mixed unit-first at 1/3/5; terminal W 3/3, U 3/3, M 2/3]
→ information-operation geometry                [36/36 admitted; 216/216 substantive items; no profile; one-to-one tasks at ceiling]
→ dependency-topology geometry                  [24/24 admitted; aligned conjunctive win 1/3; oracle obligations win 2/2 eligible synthesis]
→ content-equivalent semantic-clause geometry   [16/16 admitted; only 1/4 controls eligible; all causal contrasts ineligible]
→ executed receipt correction                    [packet 35/47→40/47; contract 254/307→260/307; 11 fixes, 5 regressions]
→ failed versus sibling-contrast receipt          [target 4/4 both; joint target+sibling 1/4→3/4; regressions 5→2]
→ final versus stepwise temporal receipt          [call-10 targets 1/3→2/3; natural-submit targets 2/3=2/3; trace advantage removed]
→ exact censored continuation                     [T1 41/53→46/53 by call 17; T2 42/53→44/53 by call 20, then 144,500 tokens for zero transitions]
→ complete-audit false-closure repair              [A0 24/33 unchanged; A1 30/33, 6/9 failures fixed, 0 regressions, 2/3 complete]
→ complete-audit held-out replication              [A0 55/70; A1 62/70; wins 3/6 < 4/6 gate; A1 mutated 6/6; 2.59× tokens]
→ automatic current complete audit                 [C1 wins 1/5, ties 4; 260/274 vs 256/274 subcases; 3.05× tokens; one non-submit]
→ submission-bound complete audit                  [4/5 first-submit endpoints improved; 245/274→256/274; 1/5 complete; post-submit 4.54× pre-submit tokens]
→ hash-bound whole-file expression                 [6/6 provider tests; live select/check/submit/replay; 57.6% of matched patch serialization]
→ three-phase transcript versus fresh world        [all 4 first code audits product-complete; research T/W B+C semantically complete; no checkpoint]
→ authentic verifier maintenance                   [fresh reentry continued 3×; first 3 phases saturated 25K; literal failing mutation preceded 8/8 submit]
→ basis/delta/structural-region maintenance         [target 100%→25%; projected no mutation at 25K; ordinary semantic 3 met/5 partial/2 missing]
→ recomposition / publication                 [not run: local inputs incomplete]
```

## Phase-continuity and diagnostic update

Qwen3.8 reconstructed task-conformant code behavior and complete research
semantics through two successive authority changes from only the complete
current task/purpose, exact current world, and ordinary tools. The literal
conversation was therefore not required durable state in these workflows.
History still functioned as a useful acquisition cache: it reduced rereads and
calls. Its cost was cumulative prompt occupancy; one transcript action reached
24,234 prompt tokens and was truncated after only 854 completion tokens at the
combined 25,088 boundary.

This supports a phase-local interpretation rather than either “keep all
history” or “always reset”:

```text
durable exact world outside context
    ↓
ordinary action-result history within one coherent phase
    ↓ meaningful authority/work boundary
fresh complete task/purpose + exact current world + ordinary reacquisition
```

The study also sharpened the verification boundary. Three product-correct code
artifacts retained one wrong model-authored assertion. The visible check told
Qwen only that model tests failed; it removed pytest's failing name, line,
expected value, and observed value. Later edits cannot therefore support a
claim that an exact diagnostic was present but unused. Availability applies to
feedback just as it applies to source: inspect the literal returned result
before inferring semantic binding or action failure.

The candidate systems rule is now: currentness, authority, and diagnostic
specificity are orthogonal. Current model-authored tests and memos remain
derivatives; a red receipt without its discriminating observation is not
complete repair information.

One later authentic maintenance trajectory qualified that rule more sharply.
Qwen received a complete task frame and exact current verifier, but the label
`malformed_manifest_identity` did not disclose which identity the acceptance
case had changed. It repeatedly reinforced per-file metadata checks. A fresh
phase that saw the literal setup—top-level `manifest_id` replaced by 64 zeroes
with entries and saved sources otherwise valid—added the missing canonical
manifest check, passed 8/8, and submitted. This is evidence about operand
availability at the check boundary, not a general benefit from longer or more
semantic feedback.

The same trajectory also limits the fresh-world story. Three consecutive
phases saturated 25K and the four phases consumed 629,610 successful tokens.
Fresh reentry preserved work and restored headroom, but broad reacquisition
rebuilt another large transcript each time. Reentry is therefore a recovery
surface at observed boundaries, not a free or automatically repeatable working-
set policy.

The subsequent mechanical-seed comparison did not make that policy more
complete. A custody-derived orientation packet reduced three calls relative to
bare fresh world across two workflows but increased total tokens 41.6%, did
not reduce operative-source reacquisition, and used essentially the same model
time. It earned no checkpoint, seed, or automatic phase policy. See the
[`results`](experiments/mechanical-reentry-seed-v0/RESULTS.md) and
[`direct audit`](experiments/mechanical-reentry-seed-v0/DIRECT_TRANSCRIPT_AUDIT.md).

One authentic repository-maintenance field study then exposed a more basic
working-set boundary. After whole reads and literal-search payloads were
mechanically capped, Qwen3.8 AD/q8/25K successfully tiled all 886 lines of a
51.7-KB target and all 620 lines of a 37.9-KB orientation document through
successive exact slices. It transferred 89,569 accepted bytes, used 211,468
successful inference tokens, and exhausted the next request before reading an
underlying result report or mutating. Sparse access did not create sparse
cognition: transfer was bounded, selection remained global, and ordinary
history retained every accepted page.

This does not establish that Qwen cannot select from a discriminating map. The
environment lacked the exact artifact basis, the complete changed-source set
since that basis, and a structural target map. The same audit found that the
task's apparent cutoff came from a stale date header: Git showed the target had
already been updated on August 17. The maintained artifact was therefore not a
trustworthy witness of its own source currency. This result concerns
navigation/acquisition and task-basis validity, not semantic integration. See
the
[`field results`](experiments/sparse-runtime-field-study-v0/RESULTS.md) and
[`literal transcript audit`](experiments/sparse-runtime-field-study-v0/DIRECT_TRANSCRIPT_AUDIT.md).

A sister-project Q3 XL study provides a cross-package qualification. With
14–18 separately addressable, decision-sized objects carrying stable identity,
version, authority, abstracts/tags, and locators, the model completed six tasks
with 6/6 correct central decisions, 25/26 semantic criteria passed (one
partial), zero duplicate accepted reads, and no consequential acquisition
failure. Accepted breadth ranged from 5/14 and 6/14 on code to 13/14 on both
research tasks. Direct inspection showed that some frozen “required” records
were already reproduced in the task or protected as untouched surfaces by
external checks. See the
[pinned sister-study result](https://github.com/ScrappyTom/custody-cards-experimental-workbench/blob/3c651b66d1f991b686b4ddcaf9cc4fb3df55dfd4/studies/authentic-working-set-assembly-baseline-v1/reports/RESULTS.md).

Because the package differs, this is not a Qwen3.8 replication. Together the
studies support a representation-conditioned hypothesis: the model can select
among meaningful conceptual objects, while file-level objects exposed only
through byte slices can induce global reconstruction. Addressability
granularity, conceptual breadth, materialization depth, and cumulative
residency must therefore be measured separately.

The direct Qwen3.8 follow-on then supplied the missing mechanical address
space. Both arms had the same corrected maintenance task and exact repository;
the projected arm additionally received the artifact basis, complete queryable
delta, and 33 nonsemantic target regions. It opened six regions / 219 lines /
12,906 bytes, while ordinary reconstructed all 886 lines / 51,678 bytes. Stable
structural identity therefore changed target selection on this development
anchor.

The inline method still failed. Its 21,242-byte task was 18,872 bytes larger
than ordinary's and added 8,401 first-prompt tokens. After four source objects,
the actor reached 25,062 prompt tokens and its next action was cut at the
25,088 combined boundary before any mutation. Ordinary submitted, but its one
new paragraph scored only 3 met / 5 partial / 2 missing: exact counts,
correction boundaries, quality distinctions, no-promotion scope, and links
collapsed into the central orientation-versus-content gist. See the
[`projection results`](experiments/incremental-maintenance-projection-v0/RESULTS.md)
and
[`direct audit`](experiments/incremental-maintenance-projection-v0/DIRECT_TRANSCRIPT_AUDIT.md).

This separates a useful external address space from a successful active
working set. Region identity can guide selection; a full registry retained in
every action request can consume the capacity the selected content was meant
to save. Selection, active residency, semantic construction, action
expression, verification, and closure remain separate boundaries.

## Design consequences

The laboratory should represent, custody, and test these objects separately:

| Object | Semantic owner in an experiment | What custody may validate |
|---|---|---|
| Artifact unit | Fixture/task author, or a separately tested model step | ID, exact bytes/range, version, provenance |
| Evidence binding | Task author control or model treatment | declared IDs, exact source bytes, proposal provenance |
| Supporting subspan | Optional model treatment only when a task requires a pinpoint | parent record, exact byte range/text, version, provenance |
| Active obligation | Task author control or model/role treatment | exact task ID/text/span, selection provenance |
| Executable predicate | Task author or independently reviewed adapter | exact setup/operation/observation/criterion bytes, execution result, candidate identity; never unexecuted sibling truth |
| Complete task audit | Task author or independently reviewed adapter | declared coverage of written requirements, complete predicate inventory, exact expected/observed results, candidate identity, and currentness; never a semantic readiness claim |
| Passing sibling control | Task author-selected experimental contrast over independently executed predicates | exact sibling program/result and candidate identity; no claim that the model must preserve it |
| Temporal trace | Task-author probe | exact program, step labels, expected/observed states, process result, and candidate identity; no inferred state mechanism |
| Artifact basis receipt | Host custody | exact artifact blob, last-changing/source-basis commit, source head, and derivation time; never an editable header's claim of currency |
| Mechanical delta map | Host custody | complete changed commits/paths/versions/hashes between exact heads; no declaration of semantic impact or relevant target section |
| Structural artifact map | Mechanical provider | stable region IDs, headings/symbol titles, exact ranges, hashes, and locators tied to one blob; no semantic ranking or recommended read |
| Addressable-object registry | Mechanical provider | stable ID, kind, authority, version, abstract/tags when mechanically sourced, and locator; known IDs remain directly readable without query admission |
| Active working set | Acting model plus literal provider | exact acquired objects/ranges, cumulative visible bytes, registry/task residency, overlap/reopens, prompt occupancy; never inferred from a per-read cap or selective-read count |
| Local action | Acting model | response schema, basis identities, exact replacement bytes |
| Recomposition | Mechanical applicator first; model integrator only as its own treatment | ordering, overlap, before/after identity, untouched bytes |
| Semantic grade | Precommitted rubric plus direct adjudication | binding to exact candidate and evidence used |

Custody must not silently promote a model-authored binding or obligation into
truth. A mechanically exact wrong map remains wrong.

## What is not yet known

- Whether productive but incomplete gold-bound local action replicates on
  another task without an active-obligation object.
- Whether exact full-corpus candidate recall and relation precision survive a
  larger, less synthetic corpus without repeating every full record per claim.
- Which model-owned or tool-mediated operation can materialize one exact
  branch-local working artifact at action time without asking the host to
  author semantic truth. Broad task-author oracle continuity and model-authored
  freeform continuity both failed, as did model-authored and complete task-
  author relationship paragraphs. A content-equivalent paragraph/line/ID
  comparison was attempted but was ineligible because its evidence-only
  control failed two central corrections. The itemization cause therefore
  remains unresolved. A later eligible factorial also found that neither a
  required-output role nor repeated exact scope qualified, so those two
  wrapper features do not explain the earlier gain. Typed structure,
  model-authored items, and staleness remain unearned.
- Whether any verifier design adds corrective value; the tested same-model
  accept/reject verifier did not and is stopped.
- Whether a latest-only closure audit can retain the completed submission-
  bound scout's repair activation while reducing historical audit
  accumulation. The tested whole method improved 4/5 first-submit endpoints
  but completed only 1/5; it is not promoted. This question must remain
  separate from how the model organizes repairs after the audit, because the
  first type/value conflation occurred when only one audit was present.
- Which bounded action organization, if any, helps after an exact failed check
  is already visible but repeated edits do not implement the governing
  invariant. The submission-bound trajectories now instantiate concrete
  examples: splitting type from empty-value validation and binding lifetime
  identity to successful insertion rather than claim. A future treatment must
  preserve the complete task frame and cannot infer the repair semantically in
  the host. Additional turns alone did not solve those states.
- How to choose a global resource ceiling that avoids censoring coherent work
  without rewarding ineffective loops. Current evidence supports reporting a
  quality/cost curve and exact continuation of active checkpoints, not one
  universal turn count.
- Whether a fresh actor receiving only predicates newly regressed by a common
  first-pass local-contrast repair can restore those siblings without undoing
  the target or creating new regressions. This must branch one exact saved
  first-pass candidate; separately rerunning the first pass would confound the
  re-verification effect. The first prospective attempt produced 8/8 clean
  one-patch repairs and no new regression, so no branch qualified and the
  causal question remains unanswered. Do not manufacture a harder version of
  those four fixtures; only a new authentic trunk with a mechanically observed
  regression can reopen it.
- Whether individually correct local edits remain coherent when recomposed;
  Stage 3 did not supply a complete set to test this cleanly.
- Whether the same unit works for code contracts and research synthesis rather
  than bounded paper claims.
- Whether presenting mutation scope as one neutral operation rather than two
  separately named tools changes the unit-first serial behavior on a fresh
  task. Edit density itself did not produce a crossover and should not be
  repeated as the selector hypothesis.
- Whether an integrated semantic account, neutral independent clauses, and
  action-facing obligations differ in a prospectively enriched set of worlds
  whose untreated outputs already meet the central-gist/secondary-loss
  phenotype. The first content-equivalent attempt held strings, IDs, bindings,
  source, target, and action fixed but qualified only 1/4 controls, so all
  causal contrasts were ineligible. Its descriptive pattern did not favor
  items or obligation role consistently. Only an untreated-baseline-first
  qualification design could justify reopening this question, and model or
  independent-reviewer authorship remains downstream of that result. Capture
  quality, evidence binding, later uptake, expression feasibility, and effect
  must remain separate; the stable host may custody these objects but may not
  declare their semantic truth.
- Whether another model package changes these boundaries.
- Whether a model-selected exact read set can become an actionable bounded
  window when the full mechanical registry and acquisition transcript are
  externally reopenable rather than permanently resident. The completed
  basis/delta/region comparison already showed selective target acquisition,
  but its inline registry exhausted the combined envelope before mutation. A
  continuation must derive its set mechanically from accepted model reads,
  preserve the complete task and current candidate, allow unrestricted further
  exact reads, and add no semantic recommendation or source cap. If it acts
  successfully, transfer to a fresh artifact/delta is still required before a
  runtime claim.

The older source-isolation questions remain routed through
[`SOURCE_ISOLATION_RESEARCH_PLAN.md`](SOURCE_ISOLATION_RESEARCH_PLAN.md).
The active incremental-maintenance question and its experiment boundary are
maintained in [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md).
