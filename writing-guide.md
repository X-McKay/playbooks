# Writing guide for draft mini-books

**Status:** 0.5.0-draft.2 assembled draft — editorial guidance, not a conformance standard  
**Audience:** New-draft contributors, editors, and reviewers  
**Purpose:** Help a Part become a coherent, navigable mini-book while preserving one canonical owner for every normative requirement.

This guide records the editorial pattern piloted by Part 4. It does **not** require an identical chapter count, title sequence, or rewrite of existing Parts. Other Parts remain available for later, separately scoped adoption of the pattern.

## The flexible six-function pattern

A finished mini-book normally provides the following functions. A single chapter may serve more than one function, and a function may be brief when the subject does not need a separate treatment.

1. **Orientation.** An unnumbered Part README explains purpose, why the Part matters, audience, applicability, prerequisites, outputs, routes, canonical chapters, and practical reference.
2. **Foundations.** Define the concepts and distinctions readers need before applying methods. Point the whole-book glossary to the local canonical explanation rather than creating competing definitions.
3. **Domain methods.** Explain the topic-specific choices, boundaries, techniques, and common misuse near the decision they support.
4. **Application workflow.** Show how a builder turns a bounded claim or need into records, steps, evidence, and handoff. Use an illustrative worked example, not a claim of real execution.
5. **Standards and evidence.** State what is required, when it applies, what observable evidence demonstrates it, and who owns its interpretation. Keep universal and independently triggered coverage distinct.
6. **Practical reference.** Offer unnumbered, reusable reference pages, templates, examples, and troubleshooting that connect the workflow without becoming a second normative standard.

> The pattern is **functional, not formulaic**. Do not create empty chapters merely to make six headings, and do not force all Parts to use seven numbered chapters.

## Place guidance beside the decision

Put a practice where the reader makes the choice it governs:

- Put definitions and relationship distinctions in foundations.
- Put a technique’s suitable use, limitation, and small example beside the technique—not in a remote global checklist.
- Put case/fixture or operating workflow rules beside the records a builder produces.
- Put applicability, cadence, and evidence obligations in the chapter that owns those requirements.
- Put interpretation, thresholds, and conclusions in the decision chapter, not in the chapter that merely gathers observations.

Link to a nearby owner instead of copying it. For example, a workflow can say that a claim needs a fit-for-purpose evaluator and link to the evaluator chapter; it should not restate the evaluator’s normative group. A coverage catalogue can identify a triggered profile and link to the relevant security, execution, context, or composition owner without inventing a replacement policy.

## One canonical requirement owner

A canonical normative group appears **only** in the owning chapter’s `## Requirements` section. Give every group one stable ID, a descriptive name, clear applicability, explicit strength, and observable evidence. Other chapters may explain the same concept descriptively and link to the owner, but they must not copy, paraphrase into a competing mandate, or create an alias ID.

Keep the [requirement index](requirement-index.md) mechanical and navigational: it points to canonical groups and does not reproduce their normative prose. If a requirement moves, update its sole owner, the index, applicable Part navigation, glossary pointers, and migration notes together.

## Write for the actual reader and scope

Every numbered chapter should begin with compact metadata:

- **Status** that honestly identifies the draft and does not claim organizational adoption;
- **Audience** that names readers who act on the material;
- **Applicability** that states the trigger and avoids making optional mechanisms universal; and
- a **Reader question** that says what the chapter enables.

Use independent triggers. Do not infer stored memory from retrieval, a model judge from routing, an approval flow from durable read-only work, or external effects from a queue. Record `N/A` only when the specific trigger is absent; do not use it to obscure missing evidence or an unimplemented control.

## Make evidence inspectable

A worked example should use stable identities for the subject, case, fixture, source/state, evaluator, and trial or run. It must distinguish expected criteria from observations and from the evaluator’s judgment. Do not turn source metadata into semantic support, a transcript into proof of an effect, or a repeated success into a population reliability claim.

For changing semantic inputs or decisions, describe reviewed invariance and relevant-change sensitivity relations when applicable. For variable material claims, retain fresh-trial and actual retry/selection/fallback context; never silently rerun until green. Make `pass`, `fail`, `invalid`, `inconclusive`, and missing required valid evidence visible according to the canonical owner’s definitions.

Examples must be labelled illustrative when they are not executed. Do not imply benchmark results, live-agent runs, approval, deployment, or production adequacy. Use neutral YAML, JSON, or plain text; do not add named-product mandates or executable framework code.

## Use practical reference deliberately

A practical reference is a companion, not a parallel policy book. It can provide templates, a connected fictional walkthrough, diagnostic guidance, and field explanations. It should link back to the chapters that own requirements, methods, evidence, and decisions. It owns no normative IDs unless its expressly scoped role is to own a requirement chapter—which is generally clearer as a numbered chapter instead.

## Navigation, citations, and migrations

Use repository-relative links with visible chapter numbers and titles. Update affected indexes, overview routes, glossary owners, and applicability pointers when a chapter path or title changes. When a page moves or is renamed, update every link to it; do not leave redirect pages behind.

Support factual claims with chapter-local numbered references in the repository’s citation format. State draft policy as a proposed playbook decision; do not attribute it to an external source or claim that an organization adopted it. Do not add private paths, task records, or `.work` links to portable book material.

## Editorial review questions

Before handing a mini-book to validation, ask:

- Does the overview let a learner, builder, and reviewer choose a route?
- Does each requirement ID have exactly one owner and a direct index link?
- Are audience, applicability, evidence, and decision boundaries visible where needed?
- Are universal obligations separated from independently triggered profiles?
- Do examples preserve the shared constants and avoid claiming execution?
- Does practical reference support the owners rather than duplicate them?
- Do all links to moved or renamed pages point at their new location?

Use this guide for new-draft editorial work only. It does not retroactively restructure other Parts or migrate the legacy compatibility directories or skills.
