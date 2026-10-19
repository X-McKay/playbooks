# 3.3 Data Privacy, Handling, and Minimum Audit Evidence

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Builders, operators, privacy and security reviewers, and accountable owners who need to make a proposed agent's information flows and review evidence inspectable.

**Applicability:** The data-handling requirements apply when a production agent processes non-public or personal data. The consequential-event audit requirement applies only when its stated event trigger is present. Every proposed production agent should still consider its information flows: a read-only response can disclose information or cause a privacy harm without changing an external record.

**Reader question:** What information may enter, move through, or remain around this proposed agent, and what is the least content needed to inspect an important decision or consequential event?

[Part 3 — Security and Trust Boundaries](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · [Initial risk, data, ownership, and delivery plan](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md)

## Purpose and applicability

An agent can expose sensitive information without invoking a write tool. A request sent to a model, a retrieved passage, a generated answer, a diagnostic trace, an evaluation fixture, a support export, or a backup can each become a new copy with a different audience and lifecycle. NIST describes the data lifecycle broadly: data actions include collection, retention, logging, generation, transformation, use, disclosure, sharing, transmission, and disposal.[1] That breadth is useful here because focusing only on the request database or the final answer leaves many agent data paths invisible.

This chapter helps a builder make those paths reviewable. It owns the proposed local requirements for data handling and minimum audit evidence in this draft. It is **not** a legal-compliance checklist, a retention schedule, a certification, or evidence that an organization has adopted the draft. NIST describes its Privacy Framework as a voluntary tool for identifying and managing privacy risk; its guidance connects the data lifecycle, the system lifecycle, and the organizations that process data.[2] A project may also have legal, contractual, sector, or geographic duties that need their own authorized interpretation.

Privacy is related to security but is not only secrecy. A confidentiality failure can create a privacy harm. So can an authorized design that collects, infers, retains, or shares more information than people reasonably expect, or uses it in a way that affects them. NIST distinguishes privacy problems arising from authorized processing from the security model's focus on unauthorized activity and loss of confidentiality, integrity, or availability.[3] Screen both kinds of concern; an access-control decision alone does not settle the privacy question.

This chapter does not replace neighboring owners. [3.1 Identity, Authority, Zero Trust, and Least Privilege](01-identity-authority-zero-trust-and-least-privilege.md) owns protected-operation authorization. [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](02-untrusted-inputs-retrieved-content-and-action-boundaries.md) owns content-to-action boundaries. [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) owns retrieval provenance, source status, and answer support. Part 4 owns evaluation design and interpretation. [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md) owns the detailed method when the initial screen identifies a specialized privacy, isolation, human-impact, or assurance concern.

## Working model

Treat handling as a **lifecycle and copies** decision, not as a switch called “logging.” A handling record follows a category from its origin through each meaningful copy, transformation, destination, and disposal path. The category might be a requester’s free-text question, an identity attribute, a source excerpt, a model output, an embedding or index entry, a cache value, a tool result, a diagnostic field, a fixture, an audit binding, or a support bundle. It may remain sensitive after it has been summarized, transformed, or placed in a different store.

A compact model is:

```text
purpose and task boundary
  → necessary data categories and allowed sources
  → permitted destinations, access, and transformations
  → response, diagnostic, audit, evaluation, support, and backup copies
  → purpose-specific retention, deletion, and integrity decisions
  → inspectable evidence and unresolved policy handoff
```

The arrows show questions a builder must make visible. They do not prove that a destination is safe, that a deletion occurred, or that an audit record is complete.

### Keep the terms separate

A **data category** is a useful decision unit, such as requester content or source metadata. It is not a claim that all fields in that category have the same sensitivity. A **copy** is a transmitted, stored, or derived representation of a category. A cache, index, evaluation export, and backup can be copies even when they are not presented as the system of record.

A **destination** is a component, organization, or audience to which a category may be disclosed or persisted. “The service is approved” is too coarse for this record. A destination decision identifies the purpose, category, relevant access boundary, and planned handling. Access may be allowed at one point while disclosure to a model, index, diagnostic store, or support audience is still out of scope.

**Diagnostic telemetry** helps an operator understand execution: timing, retries, safe error categories, version identities, and other bounded observations. It can be sampled or short-lived because its question is operational. **Audit evidence** preserves documentary evidence of a decision or event that later needs accountability. NIST describes an audit log as evidence of specific events and as a chronological record of accesses and operations.[4] In this draft, the distinction is purpose-driven: a convenient trace is not automatically the record required to reconstruct a consequential event.

A **non-content binding** is a reference that lets a reviewer relate an event to a protected artifact without putting the artifact body into the event record. A canonical argument hash is one example. It can help identify whether a later artifact matches the recorded representation, but it does not make a low-variation input secret, anonymous, or authorized. It also cannot establish that an event really happened or that the underlying argument was permitted.

### Privacy, security, and transformation limits

Purpose-first minimization asks whether a specific category or field is needed for the declared task, rather than whether it might be useful later. UK regulator guidance illustrates the point within the UK GDPR context: personal data must be adequate, relevant, and limited to what is necessary for a stated purpose.[5] That is a jurisdiction-specific legal explanation, not a universal legal conclusion in this playbook. It supports a practical design habit: name the task purpose before deciding what a model, retrieval component, tool, or support path receives.

Do not call transformed data anonymous merely because direct identifiers are removed. Under the ICO's UK GDPR guidance, pseudonymised data remains personal data for a party that holds the additional information, and pseudonymisation is not the same as anonymisation.[6] Encryption, hashing, token replacement, and safe bindings can be valuable safeguards, but their value depends on the data, surrounding information, and access boundary. Treat them as risk-reduction measures until the applicable context establishes a stronger conclusion.

## Decisions and best practices

### Map the complete path before choosing a control

Start with the candidate's bounded task and write down the categories it needs. Then follow each through the places where agent systems commonly create copies:

- request assembly, including attachments and conversation history;
- model context and generated response;
- retrieval queries, source excerpts, indexes, summaries, and caches;
- tool requests, tool results, and errors;
- memory or other state that persists across tasks, if enabled;
- diagnostics, metrics attributes, audit records, evaluation fixtures and observations;
- support investigation material, exported bundles, and backups or recovery copies.

For every relevant copy, record the purpose, permitted destination, access roles, and retention/deletion decision. Use a category that is fine-grained enough to expose a meaningful difference. For example, source identifiers and a retrieved document body often have different exposure and retention needs; an answer citation can be useful without retaining the whole prompt.

Make the model destination explicit. A final-output filter does not undo a disclosure that already occurred when a question or source excerpt entered model context. Likewise, filtering the visible answer does not remove a copy in a cache, an evaluation capture, or a support export. Permission-filter sources before assembling model context, and keep the trusted requester and tenant boundary available to the protected retrieval path. This chapter names the handling decision; the resource-side authorization remains the responsibility of 3.1.

### Minimize at the boundary that creates each copy

Ask a concrete question at each boundary: **What smallest representation is sufficient for this purpose?** A model may need the narrowly selected policy passage rather than an entire employee record. An aggregate diagnostic may need an outcome category and size rather than free text. An audit record may need an immutable version identity and a non-content binding rather than the full action payload.

Minimization has limits. Removing material context can make an answer misleading, can prevent investigation of a safety incident, or can make a required audit impossible. The answer is not to retain everything by default. State the missing purpose and the evidence required to justify the additional copy. A proposed exception for content capture should be narrow in purpose and scope, classified before capture, accessible only to the defined readers, redacted before export, and paired with a retention and deletion plan. The proposed local requirement below makes those fields mandatory when production content capture occurs.

Derived forms need their own review. A retrieval index, summary, cache key, vector representation, fixture export, or support bundle can retain source content or reveal an inference about a person or tenant. A safe reference can reduce needless content exposure, but it does not remove the access, retention, or deletion question. Record the derived store and the relationship to its source so that deletion or access changes do not leave an unexamined copy behind.

### Separate diagnostics from audit evidence

Use diagnostics to answer bounded operational questions: which candidate/version handled a run, whether a request reached a component, whether an authorization boundary allowed or denied access, which source identifiers were eligible, and which safe error category occurred. NIST SP 800-92 provides high-level guidance for enterprise log-management processes; it does not supply a universal, agent-specific retention schedule or prove that a particular trace is adequate audit evidence.[7]

For a read-only assistant, a proportionate record can often attribute the run without retaining body content: run or request reference, candidate/configuration identity, trusted requester/tenant reference where applicable, allowed source identifiers or boundary outcome, terminal outcome, and time. This is a design pattern, not proof that the answer was correct or that a control worked. Part 4 supplies the cases and judgments needed for those claims.

For a consequential operation, the audit record must support the specific event described in DATA-05. Keep its content purpose separate from debug trace content. An append-only or tamper-evident store can help detect an unauthorized record change; it does not prove that all events were emitted, that the action was authorized, or that the external target accepted the request. Preserve observable proposal, protected-operation authorization, dispatch, and authoritative effect as separate facts when they differ. Do not request or retain raw hidden reasoning to fill this gap.

### Design redaction and export as a single boundary

Redaction after a bundle reaches an operator, a vendor, or a broad queue is too late for the export path. Decide where sensitive fields are detected or excluded before the boundary, and include structured fields and error details as well as visible prompt text. Credentials, headers, tokens, signed links, personal identifiers, customer content, tool payloads, workflow data, and exception text can all appear outside the obvious request/response fields.

A redaction label is not evidence that redaction ran. A reviewer needs a declared rule, an observable boundary, and relevant negative cases showing that an export does not contain the sensitive category it was designed to exclude. Redaction also needs a limit: removing content can make a support artifact insufficient for the stated investigation. In that case, return to the exceptional-capture decision rather than quietly exporting the original body.

### Set retention and deletion by purpose, not by a universal clock

Retention is a decision about why a copy remains useful, what makes that purpose end, who may access it while it exists, and what happens to derived copies. Diagnostic content, audit evidence, source caches, indexes, evaluation exports, and backups can legitimately have different purposes. A single “keep all logs” rule hides those differences.

The ICO's UK GDPR storage-limitation guidance illustrates the purpose-specific nature of this question, notes that it supplies no fixed period for every type of personal data, and treats offline storage and relevant backups as still needing consideration.[8] This chapter therefore sets no numeric duration. The handling record should instead name the organization-specific retention/deletion rule or leave it unresolved for the appropriate decision owner; unresolved is not permission to retain or send the data.

Deletion and evidence preservation can conflict. A durable audit record that contains unnecessary content may make an otherwise ordinary deletion request difficult to honor. Design the audit record to avoid unnecessary content first. When a genuine preservation duty conflicts with a deletion requirement, keep the conflict visible: identify the affected copies, legal or policy basis if known, access limits, and unresolved decision. Do not quietly convert a planned integrity need into indefinite retention.

### Screen harms beyond disclosure

Consider who can be affected by collection, inference, retrieval, retention, or a misleading absence of information. A request may reveal health, employment, location, family, financial, or other sensitive circumstances. A system may infer a category that was never explicitly provided. Repeated retention or support access may create a disproportionate exposure for a group even when individual calls are authorized.

Describe the plausible pathway, affected people or groups, consequence, and uncertainty. This is a planning screen, not a finding that harm will occur and not a substitute for specialized assessment. Route material issues to Part 10 and connect the resulting scenarios to Part 4 cases. Avoid using a favorable aggregate result, an encryption claim, or a completed form as proof that a privacy concern has been resolved.

### Builder workflow

1. **Bound the proposed task.** Start from the planning record, intended use, prohibited uses, sources, and candidate capabilities. Mark the handling record as a proposed local review unit rather than an operating system description.
2. **Inventory categories and copies.** Follow requester input, trusted context, retrieved evidence, outputs, diagnostics, audit evidence, evaluation materials, support exports, indexes, caches, memory, and backups. Mark uncertain paths rather than guessing they do not exist.
3. **Decide purpose and destination.** For each relevant copy, state the task purpose, proposed destination, access boundary, and whether the category is approved for that destination. If the category or destination is unresolved, keep it out of that path under DATA-01.
4. **Choose the least revealing useful representation.** Prefer selected fields, metadata, source IDs, safe error categories, or non-content bindings where they meet the stated need. Record why body capture is necessary before proposing it.
5. **Separate diagnostic and audit lanes.** State the question each lane answers, its access audience, and its independent retention/deletion rule. For any consequential trigger, map the DATA-05 fields without placing raw hidden reasoning or unneeded personal content in the record.
6. **Plan export and lifecycle behavior.** Identify the redaction-before-export boundary and all derived/backup copies. Record how a change in destination, category, source, capture purpose, or retention purpose returns the handling record for review.
7. **Plan inspectable evidence.** Identify the configuration, record, boundary observation, and adverse case that a reviewer would examine. Planned evidence is not an observation; label it accordingly.
8. **Hand off unresolved decisions.** Leave owner identity, legal applicability, retention period, deletion-versus-preservation conflict, or specialized assessment as unresolved when the draft has no authorized answer. Do not add an invented role, time limit, or approval to make the record look complete.

The companion [data-handling and audit record](../../templates/3.3/data-handling-audit-record.yaml) is a neutral planning/build template for these steps. It contains fictional, unexecuted example values and no adoption or release claim.

## Requirements

- **DATA-01** Production agents that process non-public or personal data **MUST** maintain a data-handling record identifying the data categories, purpose, model/retrieval/tool destinations, access roles, and retention/deletion rule for each relevant copy. If a category or destination is not approved, the agent **MUST NOT** send it there.
- **DATA-02** Production agents **MUST** minimize information sent to models, tools, and retrieval components to what is needed for the declared task, and **MUST** keep prompt, completion, and tool-payload capture disabled by default. Any production content capture **MUST** have a documented purpose, classification, approval, redaction-before-export, access restriction, sampling scope, retention, and deletion plan.
- **DATA-03** Systems that export diagnostic or audit data **MUST** redact or exclude credentials, personal identifiers, customer content, sensitive tool/workflow payloads, and sensitive exception details before export. Where content is not retained, the record **MAY** use safe hashes and metadata, but a hash **MUST NOT** be treated as anonymization or as a substitute for access controls.
- **DATA-04** Production systems **MUST** define and enforce access and retention/deletion rules separately for diagnostic content and audit records, including relevant derived stores. A change to a data destination, category, or retention purpose **MUST** trigger review of the handling record. Stronger deletion, isolation, or integrity controls apply when required by the risk assessment or Part 10.
- **DATA-05** When an agent performs a consequential operation, approval, authorization override, policy change, production promotion, manual workflow intervention, data export, or compensation, its audit record **MUST** identify the actor, action, target, time, agent/run identity, applicable approval and policy references, a canonical argument hash or equivalent non-content binding, and the result. Such records **SHOULD** be append-only or tamper-evident. Audit evidence **MUST NOT** require raw hidden reasoning, and sampled debug traces **MUST NOT** be the sole evidence of a consequential event.
- **DATA-06** Before production use, the accountable owner **MUST** screen data handling for plausible privacy harms and disparate impact, record affected groups and material uncertainties, and route material concerns to the appropriate Part 10 assessment. The resulting material scenarios **MUST** inform the applicable Part 4 tests; this screening does not replace detailed domain assessment or testing.

## Worked example

This illustrative planning record concerns `POLICY-BUILD-001`, the fictional `internal-policy-assistance` candidate. It is a proposed fixed retrieval-and-answer workflow: a requester asks about a travel policy, the candidate consults permitted current policy evidence, and it returns a cited answer or a bounded uncertainty outcome. It has no write, approval, export, or compensation capability enabled. The example is **illustrative and unexecuted**; it does not describe an assembled, admitted, approved, deployed, or evaluated system.

For the permitted requester `employee-uk-104`, the controlled `travel-policy-2026@2026-10-01` fixture says the fictional London hotel limit is GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` fixture says GBP 200. The requester may access the named controlled sources; `contractor-uk-204` may not. The category map distinguishes the request body, trusted requester/permission context, source identity and status, narrowly selected policy passage, answer/citation, diagnostic metadata, potential support material, and derived retrieval/cache copies. It does not assume that a source identifier or a citation is harmless in every support audience.

The proposed record gives the model only the task-needed permitted passage and source metadata, not an unrestricted document collection. It plans a read-only diagnostic lane with a run reference, candidate/configuration identity, source identifiers and currentness state, protected retrieval allow/deny outcome, terminal outcome, and safe error category. It explicitly does **not** treat that record as proof that the GBP 220 answer was semantically supported; Part 4 would assess that claim separately. It also does not retain the full question or source body merely to make an audit trail more convenient.

Consider a hypothetical report that the candidate cited the superseded source. The tempting change would be global prompt and retrieval-body capture. The proposed investigation instead first asks whether the allowed source set, source status, retrieval boundary, candidate identity, and citation identifier distinguish a stale-admission defect from an answer-use defect. Those non-body observations may be sufficient. If they are not, the planning record requires a separately scoped exceptional-capture decision with purpose, classification, approval, access restriction, sampling scope, redaction-before-export, retention, and deletion decisions. A synthetic controlled fixture is the preferred first reproduction path. Nothing in this example claims that such capture occurred.

The baseline has no consequential action, so it does not fabricate a DATA-05 approval or tool-effect audit record. If a future proposal added a data export or another consequential capability, that new destination and event trigger would return the handling record for review. The future record would need the applicable DATA-05 binding and result fields, while keeping raw hidden reasoning and unnecessary request/source bodies out of the audit record. Adding an encryption, a hash, or a new diagnostic field would not by itself authorize the capability or settle the privacy impact.

## Evidence and checklist

A useful review package makes the proposed choices inspectable without claiming that paper artifacts prove behavior. It can include a completed handling record; a declared data/copy inventory; permitted-destination and access-boundary descriptions; capture and export configuration intent; a retention/deletion map that includes derived stores; a record format for applicable audit events; and Part 4 cases for permission scope, redaction, source handling, harmful inference, and lifecycle changes. The evidence should identify what is planned, inspected, or observed. A trace, a redaction rule, an audit schema, or a passing synthetic fixture does not by itself prove control effectiveness in a different environment.

Use the following review questions to find omissions rather than to declare the candidate approved:

- [ ] Does the record identify each relevant category and its copies across prompts, tools, retrieval, memory/indexes/caches, outputs, diagnostics, evaluation material, support exports, and backups?
- [ ] Is the task purpose and permitted destination explicit for each category, with unresolved destinations kept out of the path?
- [ ] Is permission filtering applied before sensitive source material reaches model context, with authorization still enforced at the protected operation?
- [ ] Is production prompt, completion, and tool-payload capture disabled by default, and does any proposed exception contain every DATA-02 decision field?
- [ ] Does an export boundary redact or exclude structured and unstructured sensitive content before the data leaves its restricted context?
- [ ] Are diagnostic and audit lanes separately purposed, access-controlled, retained, and deleted, including relevant derived and backup copies?
- [ ] Where a consequential trigger exists, does the proposed audit record contain the DATA-05 fields without raw hidden reasoning or unnecessary body content?
- [ ] Does the privacy-harm screen name affected groups, uncertainties, and the Part 4/Part 10 handoff where material?
- [ ] Are legal applicability, retention duration, owner identity, or preservation conflicts visibly unresolved when no authorized decision exists?

Continue with [4.3 Evaluation Types and Dimensions](../04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) for claim-fit test design and [10.3 Advanced Privacy, Isolation, and Auditability](../../engineering-reference/10-risk-privacy-and-specialized-assurance/03-advanced-privacy-isolation-and-auditability.md) for specialized controls.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf "NIST Privacy Framework Version 1.0"
[2]: https://www.nist.gov/privacy-framework/using-privacy-framework-11 "Using NIST Privacy Framework 1.1"
[3]: https://nvlpubs.nist.gov/nistpubs/ir/2017/NIST.IR.8062.pdf "NIST IR 8062 Privacy Engineering and Risk Management"
[4]: https://csrc.nist.gov/glossary/term/audit_log "NIST CSRC Glossary Audit Log"
[5]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/ "ICO Data Minimisation Guidance"
[6]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/ "ICO Pseudonymisation Guidance"
[7]: https://csrc.nist.gov/pubs/sp/800/92/final "NIST SP 800-92 Guide to Computer Security Log Management"
[8]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ "ICO Storage Limitation Guidance"
