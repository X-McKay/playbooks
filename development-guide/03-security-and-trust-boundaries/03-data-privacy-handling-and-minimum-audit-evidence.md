# 3.3 Data Privacy, Handling, and Minimum Audit Evidence

**Status:** 0.5.0-draft.2 — draft

**Audience:** Builders, operators, privacy and security reviewers, and accountable owners who need an agent's information flows and review evidence to be inspectable.

**Applicability:** The data-handling requirements apply when a production agent processes non-public or personal data. The audit requirement applies only when its event trigger is present. Every production agent should still consider its information flows: a read-only response can disclose information or cause privacy harm without changing a record.

**Reader question:** What information may enter, move through, or remain around this agent, and what is the least content needed to inspect an important decision or consequential event?

[Part 3 — Security and Trust Boundaries](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · [Initial risk, data, ownership, and delivery plan](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md)

## Purpose and applicability

An agent can expose sensitive information without a write tool. A model request, a retrieved passage, a generated answer, a diagnostic trace, an evaluation fixture, a support export, or a backup can each become a new copy with a different audience and lifecycle. NIST describes data actions broadly: collection, retention, logging, generation, transformation, use, disclosure, sharing, transmission, and disposal. [1]

This chapter is **not** a legal-compliance checklist or a retention schedule. NIST describes its Privacy Framework as a voluntary tool for identifying and managing privacy risk across the data lifecycle, the system lifecycle, and the organizations that process data. [2] Legal, contractual, sector, or geographic duties need their own interpretation.

Privacy is not only secrecy. A confidentiality failure can cause privacy harm, and so can an authorized design that collects, infers, retains, or shares more than people expect, or uses data in ways that affect them. NIST distinguishes privacy problems arising from authorized processing from the security model's focus on unauthorized activity and loss of confidentiality, integrity, or availability. [3] Screen for both; an access-control decision alone does not settle the privacy question.

Authorization is in [3.1](01-identity-authority-zero-trust-and-least-privilege.md), content-to-action boundaries in [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md), retrieval provenance and answer support in [2.6](../02-agent-basics/06-context-and-retrieval-fundamentals.md), and detailed privacy, isolation, and assurance method in [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md).

## Working model

Treat handling as a **lifecycle and copies** decision, not a switch called "logging." Follow each data category (a requester's question, an identity attribute, a source excerpt, a model output, an embedding, a cache value, a tool result, a diagnostic field, a fixture, an audit binding, a support bundle) from its origin through each copy, transformation, destination, and disposal path. It can stay sensitive after being summarized or moved.

```text
purpose and task boundary
  → necessary data categories and allowed sources
  → permitted destinations, access, and transformations
  → response, diagnostic, audit, evaluation, support, and backup copies
  → purpose-specific retention, deletion, and integrity decisions
  → inspectable evidence and unresolved policy handoff
```

The arrows are questions to make visible, not proof that a destination is safe, a deletion occurred, or an audit record is complete.

### Keep the terms separate

A **data category** is a decision unit, such as requester content or source metadata; fields within it can differ in sensitivity. A **copy** is a transmitted, stored, or derived representation of a category; caches, indexes, evaluation exports, and backups are copies even when they are not the system of record.

A **destination** is a component, organization, or audience to which a category may be disclosed or persisted. "The service is approved" is too coarse: a destination decision names the purpose, category, access boundary, and planned handling. Access may be allowed at one point while disclosure to a model, index, diagnostic store, or support audience is out of scope.

**Diagnostic telemetry** helps an operator understand execution (timing, retries, safe error categories, version identities) and can be sampled or short-lived. **Audit evidence** preserves documentary evidence of a decision or event for later accountability; NIST describes an audit log as evidence of specific events and a chronological record of accesses and operations. [4] A convenient trace is not automatically the record needed to reconstruct a consequential event.

A **non-content binding**, such as a canonical argument hash, relates an event to a protected artifact without putting the artifact in the record. It can show whether a later artifact matches, but does not make a low-variation input secret or anonymous, and cannot show the event happened or was permitted.

### Privacy, security, and transformation limits

Purpose-first minimization asks whether a field is needed for the declared task, not whether it might be useful later. UK regulator guidance states it in UK GDPR terms: personal data must be adequate, relevant, and limited to what is necessary for a stated purpose. [5] That is jurisdiction-specific, but the design habit is general: name the purpose before deciding what a model, retrieval component, tool, or support path receives.

Do not call transformed data anonymous because direct identifiers were removed. Under the ICO's guidance, pseudonymised data remains personal data for a party holding the additional information, and pseudonymisation is not anonymisation. [6] Encryption, hashing, token replacement, and safe bindings reduce risk, but their value depends on the data, surrounding information, and access boundary.

The ICO pages cited here are under review following the Data (Use and Access) Act 2025. The EU GDPR has parallel provisions: data minimisation (Art. 5(1)(c)), storage limitation (Art. 5(1)(e)), pseudonymisation (Art. 4(5) and Recital 26), data protection by design and by default (Art. 25), automated decision-making (Art. 22), and data protection impact assessment (Art. 35). [10]

## Decisions and best practices

### Map the complete path before choosing a control

Start from the bounded task and list the categories it needs. Then follow each through the places agent systems create copies:

- request assembly, including attachments and conversation history;
- model context and generated response;
- retrieval queries, source excerpts, indexes, summaries, and caches;
- tool requests, results, and errors;
- memory or other state that persists across tasks, if enabled;
- diagnostics, metrics attributes, audit records, evaluation fixtures and observations;
- support material, exported bundles, and backups.

Split categories finely enough to expose differences: source identifiers and a retrieved document body usually need different exposure and retention, and a citation can be useful without keeping the whole prompt.

Make the model destination explicit. A final-output filter does not undo a disclosure that happened when a question or source excerpt entered model context, nor remove copies in a cache, evaluation capture, or support export. Permission-filter sources before assembling model context, with the trusted requester and tenant boundary available to retrieval; resource-side authorization stays with 3.1.

### Minimize at the boundary that creates each copy

At each boundary ask: **what is the smallest representation sufficient for this purpose?** A model may need one policy passage, not a whole employee record; a diagnostic, an outcome category and size, not free text; an audit record, a version identity and a non-content binding, not the full action payload.

Minimization has limits: removing context can make an answer misleading, block investigation of a safety incident, or make a required audit impossible. Do not keep everything by default; state the missing purpose and the evidence that justifies the extra copy. Content capture is a narrow exception that needs every DATA-02 field.

Derived forms need their own review. A retrieval index, summary, cache key, vector representation, fixture export, or support bundle can retain source content or reveal an inference about a person or tenant. Record each derived store and its source so deletion or access changes do not leave an unexamined copy.

### Separate diagnostics from audit evidence

Use diagnostics for bounded operational questions: which version handled a run, whether a request reached a component, whether an authorization boundary allowed or denied access, which source identifiers were eligible, which safe error category occurred. NIST SP 800-92 (2006; a revision is in draft) is a high-level guide to log management, and NIST SP 800-53 has an audit and accountability family for record content, protection, and retention. [7] [9] Neither is agent-specific or sets a retention schedule.

For a read-only assistant, a proportionate record can often attribute a run without body content: a run reference, configuration identity, trusted requester or tenant reference, allowed source identifiers or boundary outcome, terminal outcome, and time. It does not show the answer was correct (Part 4).

For a consequential operation, the audit record supports the DATA-05 event, separate from debug traces. An append-only or tamper-evident store helps detect record changes but does not prove all events were emitted, the action was authorized, or the target accepted the request. Keep proposal, authorization, dispatch, and authoritative effect as separate facts when they differ.

### Design redaction and export as a single boundary

Redaction after a bundle reaches an operator, vendor, or broad queue is too late. Decide where sensitive fields are detected or excluded before the boundary, including structured fields and error details: credentials, headers, tokens, signed links, personal identifiers, customer content, tool payloads, workflow data, and exception text can all appear outside the obvious fields.

A redaction label is not evidence that redaction ran; that takes a declared rule, an observable boundary, and negative cases showing an export lacks the excluded category. If redaction leaves a support artifact too thin, return to the exceptional-capture decision instead of quietly exporting the original body.

### Set retention and deletion by purpose, not by a universal clock

Retention decides why a copy stays useful, what ends that purpose, who may access it meanwhile, and what happens to derived copies. Diagnostics, audit evidence, caches, indexes, evaluation exports, and backups have different purposes that a single "keep all logs" rule hides.

ICO storage-limitation guidance treats the question as purpose-specific, gives no fixed period for every type of personal data, and says offline storage and backups still need consideration. [8] This chapter sets no duration. The handling record names the organization's rule or leaves it unresolved for the decision owner; unresolved is not permission to retain or send the data.

Deletion and evidence preservation can conflict. An audit record with unnecessary content can make a deletion request hard to honor, so avoid unnecessary content first. For a genuine preservation duty, record the affected copies, the legal or policy basis if known, access limits, and the open decision, rather than quietly turning an integrity need into indefinite retention.

### Screen harms beyond disclosure

A request may reveal health, employment, location, family, financial, or other sensitive circumstances; a system may infer a category never provided; retention or support access may expose a group disproportionately even when each call is authorized. Describe the plausible pathway, affected people or groups, consequence, and uncertainty. This is a planning screen, not a finding of harm or a specialized assessment, and an encryption claim or completed form does not resolve a privacy concern.

### Builder workflow

1. **Bound the task** from the planning record, uses, sources, and capabilities.
2. **Inventory categories and copies,** marking uncertain paths instead of assuming they do not exist.
3. **Decide purpose and destination** for each copy.
4. **Choose the least revealing useful representation,** recording why any body capture is needed.
5. **Separate diagnostic and audit lanes.**
6. **Plan export and lifecycle behavior:** the redaction boundary, derived and backup copies, and what triggers re-review.
7. **Hand off unresolved decisions** (owner, legal applicability, retention period, preservation conflict, specialized assessment) instead of inventing a role, time limit, or approval.

The companion [data-handling and audit record](../../templates/3.3/data-handling-audit-record.yaml) is a planning template for these steps.

## Requirements

- **DATA-01** Production agents that process non-public or personal data **MUST** maintain a data-handling record identifying the data categories, purpose, model/retrieval/tool destinations, access roles, and retention/deletion rule for each relevant copy. If a category or destination is not approved, the agent **MUST NOT** send it there.
- **DATA-02** Production agents **MUST** minimize information sent to models, tools, and retrieval components to what is needed for the declared task, and **MUST** keep prompt, completion, and tool-payload capture disabled by default. Any production content capture **MUST** have a documented purpose, classification, approval, redaction-before-export, access restriction, sampling scope, retention, and deletion plan.
- **DATA-03** Systems that export diagnostic or audit data **MUST** redact or exclude credentials, personal identifiers, customer content, sensitive tool/workflow payloads, and sensitive exception details before export. Where content is not retained, the record **MAY** use safe hashes and metadata, but a hash **MUST NOT** be treated as anonymization or as a substitute for access controls.
- **DATA-04** Production systems **MUST** define and enforce access and retention/deletion rules separately for diagnostic content and audit records, including relevant derived stores. A change to a data destination, category, or retention purpose **MUST** trigger review of the handling record. Stronger deletion, isolation, or integrity controls apply when required by the risk assessment or Part 10.
- **DATA-05** When an agent performs a consequential operation, approval, authorization override, policy change, production promotion, manual workflow intervention, data export, or compensation, its audit record **MUST** identify the actor, action, target, time, agent/run identity, applicable approval and policy references, a canonical argument hash or equivalent non-content binding, and the result. Such records **SHOULD** be append-only or tamper-evident. Audit evidence **MUST NOT** require raw hidden reasoning, and sampled debug traces **MUST NOT** be the sole evidence of a consequential event.
- **DATA-06** Before production use, the accountable owner **MUST** screen data handling for plausible privacy harms and disparate impact, record affected groups and material uncertainties, and route material concerns to the appropriate Part 10 assessment. The resulting material scenarios **MUST** inform the applicable Part 4 tests; this screening does not replace detailed domain assessment or testing.

## Worked example

The fictional, unexecuted record concerns `POLICY-BUILD-001`, the `internal-policy-assistance` candidate: a fixed retrieval-and-answer workflow that returns a cited policy answer or a bounded uncertainty outcome, with no write, approval, export, or compensation capability.

For `employee-uk-104`, the controlled `travel-policy-2026@2026-10-01` fixture says the London hotel limit is GBP 220; the superseded `travel-policy-2024-superseded@2024-01-01` fixture says GBP 200. `contractor-uk-204` may not access the named sources. The category map separates the request body, trusted requester and permission context, source identity and status, the selected policy passage, the answer and citation, diagnostic metadata, potential support material, and derived retrieval or cache copies. It does not assume a source identifier or citation is harmless for every support audience.

The model gets only the permitted passage and source metadata, not a whole document collection. The read-only diagnostic lane holds a run reference, configuration identity, source identifiers and currentness state, the retrieval allow or deny outcome, terminal outcome, and safe error category, not the full question or source body. It does not show the GBP 220 answer was semantically supported; Part 4 assesses that.

Suppose the candidate is reported to cite the superseded source. Before reaching for global prompt and retrieval-body capture, check whether the allowed source set, source status, retrieval boundary, configuration identity, and citation identifier distinguish a stale-admission defect from an answer-use defect; these may be enough. If not, scope an exceptional-capture decision with every DATA-02 field, and reproduce first with a synthetic fixture.

The baseline has no consequential action, so no DATA-05 record. A future data export or other consequential capability would reopen the handling record and need the DATA-05 fields; encryption, a hash, or a diagnostic field would not authorize it or settle its privacy impact.

## Evidence and checklist

A review package can include the handling record, copy inventory, destination and access descriptions, capture and export configuration, a retention and deletion map covering derived stores, an audit record format, and Part 4 cases for permission scope, redaction, source handling, harmful inference, and lifecycle changes. Mark each item planned, inspected, or observed; a trace, redaction rule, or passing synthetic fixture does not prove a control works elsewhere.

- [ ] Copies are identified across prompts, tools, retrieval, memory, indexes, caches, outputs, diagnostics, evaluation material, support exports, and backups.
- [ ] Permission filtering happens before sensitive source material reaches model context.
- [ ] The export boundary covers structured fields and error details, with negative cases.
- [ ] Retention covers derived and backup copies.
- [ ] Legal applicability, retention duration, owner identity, and preservation conflicts are visibly unresolved when no authorized decision exists.

Continue with [4.3 Evaluation Types and Dimensions](../04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) for test design and [10.3 Advanced Privacy, Isolation, and Auditability](../../engineering-reference/10-risk-privacy-and-specialized-assurance/03-advanced-privacy-isolation-and-auditability.md) for specialized controls.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf "NIST Privacy Framework Version 1.0"
[2]: https://www.nist.gov/privacy-framework/using-privacy-framework-11 "Using NIST Privacy Framework 1.1 (draft)"
[3]: https://nvlpubs.nist.gov/nistpubs/ir/2017/NIST.IR.8062.pdf "NISTIR 8062: An Introduction to Privacy Engineering and Risk Management in Federal Systems"
[4]: https://csrc.nist.gov/glossary/term/audit_log "NIST CSRC Glossary Audit Log"
[5]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/ "ICO Data Minimisation Guidance (under review)"
[6]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/ "ICO Pseudonymisation Guidance"
[7]: https://csrc.nist.gov/pubs/sp/800/92/final "NIST SP 800-92 Guide to Computer Security Log Management (2006)"
[8]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ "ICO Storage Limitation Guidance (under review)"
[9]: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final "NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations"
[10]: https://eur-lex.europa.eu/eli/reg/2016/679/oj "Regulation (EU) 2016/679 (General Data Protection Regulation)"
