# 3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Builders, security reviewers, evaluators, and operators of agents that interpret external content or can pass results to another component.

**Applicability:** Apply the content boundary whenever an agent receives user-provided, retrieved, tool-returned, or inter-agent material. Apply the action boundary whenever model output can be rendered, stored, forwarded, or used to request an operation. An agent with no external operation still has an output boundary and can still mislead or disclose.

**Reader question:** How can an agent use outside material for a legitimate task without letting that material create authority, redirect a protected action, or acquire more trust as it moves through the system?

[Part 3 — Security and Trust Boundaries](README.md) · [Applicability](../../applicability.md) · [3.1 Identity, Authority, Zero Trust, and Least Privilege](01-identity-authority-zero-trust-and-least-privilege.md) · [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) · [3.3 Data Privacy, Handling, and Minimum Audit Evidence](03-data-privacy-handling-and-minimum-audit-evidence.md)

## Purpose and applicability

An agent can receive a question written by a requester, a document returned from retrieval, a tool response, a message from another component, or content embedded in a file or image. That material may be useful evidence, mistaken, stale, malicious, or all of these at once. The core distinction is practical: **content can inform a result; it cannot rewrite the conditions under which the result is produced.**

A **direct prompt injection** arrives in a user-controlled request. An **indirect prompt injection** arrives through a resource that an attacker can influence, such as a document, website, message, or attachment. NIST defines the latter as prompt injection carried out through resource control rather than user-provided input. [1] OWASP notes that both forms can alter model behavior and that retrieval augmentation and fine-tuning do not fully remove the vulnerability. [2] [3]

This chapter is about the movement from content to a possible downstream use. It does not make every input equally risky or require every agent to have a tool. A read-only answer can still disclose restricted information or launder a stale claim into an apparently current answer. Conversely, a hostile sentence in an otherwise useful document should not automatically make the legitimate task impossible. The appropriate response depends on the declared task, available evidence, and the separately enforced action boundary.

The surrounding chapters retain their own decisions. [3.1](01-identity-authority-zero-trust-and-least-privilege.md) owns workload, requester, tenant, and deterministic authorization. [2.4](../02-agent-basics/04-tools-and-external-interfaces.md) owns interface contracts, actual effects, retries, and unknown outcomes. [2.6](../02-agent-basics/06-context-and-retrieval-fundamentals.md) owns source admission, currentness, and retrieval quality. [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md) owns data destinations, minimization, retention, and audit policy. This chapter connects their boundaries where untrusted content could steer a result or action.

## Working model

### Four roles that must not collapse

**Trusted operating context** is the reviewed task boundary and the runtime facts supplied from their declared trusted sources. It can include the admitted capability set, the authenticated requester scope, an allowed destination, and an output contract. It is not established by a persuasive request, a document label, a model statement, or a tool response.

**Untrusted content** is material to interpret. It includes user text, retrieved passages, tool results, messages from another agent, and a summary of any of them until a separate process establishes a narrower role. A source may be approved to support a domain fact while its embedded instruction-like text remains untrusted for operational control.

**A proposal** is a model-produced answer, structured value, suggested tool call, handoff, or claimed result. It remains data. It becomes an actionable request only when a receiving boundary validates it for that specific destination.

**An action boundary** is the point that decides whether a particular operation, target, argument set, and destination are permitted in the current trusted context. It is not a prompt convention. MITRE describes the related confused-deputy failure as an intermediary forwarding a request without sufficiently preserving its original source, allowing the intermediary's different authority to be misused. [4]

A useful flow is:

```text
trusted task, admitted capabilities, and runtime context
                    +
        content with source role and provenance
                    ↓
      model result or action proposal as untrusted data
                    ↓
 destination-specific validation and protected-operation check
                    ↓
     accepted response or admitted attempt, or safe outcome
                    ↓
 response and, where relevant, authoritative effect observation
```

The stages describe different observations. A model can propose `retrieve_permitted_policy_evidence`; that does not show that a request was dispatched. A dispatched request can receive a response without establishing that an external effect occurred. An authoritative target record, where there is an effect, is different evidence again. This distinction prevents a fluent claim of success or a blocked proposal from being mistaken for an executed operation.

### Validate the property that matters

A schema, type, or bounds check asks whether a value has an acceptable **shape** for its destination. It can reject an unknown operation, an extra field, malformed identifier, or out-of-range argument. It cannot establish that a cited passage supports an answer, that a destination is permitted, or that a proposed action is appropriate.

A **semantic check** asks whether the value means something acceptable in its intended use. For a policy answer, that includes whether the identified current, permitted evidence supports the claim. For a proposed operation, it includes whether the normalized target and arguments fit the operation's domain constraints. **Provenance validation** asks whether the record still carries the source identity, revision or status, and transformation history needed for the receiving component to apply the right rule. These checks complement rather than replace one another.

**Content laundering** is a useful local name for losing those distinctions during a transform. For example, an untrusted note can be summarized, placed in a citation wrapper, or sent to another agent, then treated as if it were trusted policy because its source role was dropped. A rewrite may make language safer or shorter, but it does not upgrade the authority, freshness, permission, or truth of the underlying content. OWASP similarly warns that model-controlled output passed unchecked to downstream systems can provide indirect access to additional functionality. [5]

Labels, delimiters, prompt instructions, and model self-reflection can help the model follow the intended role distinction. They do not enforce it. OWASP specifically cautions that text labels and prompt wording are not an enforcement boundary; authorization and parameter validation must remain outside the model. [6]

## Decisions and best practices

### Decide what each channel may influence

Before connecting a source or a downstream consumer, record its role. A policy document may support a policy amount. A user request may select a question to answer. A tool result may supply a bounded observation. None of these channels should be able to select a different tenant, add a capability, create approval, alter the execution class, or choose an unreviewed destination.

This is not a claim that all content is false. It is a choice about which system decision can rely on which input. Preserve a compact source identity and relevant status through retrieval, summarization, citation, and handoff so a recipient can distinguish a current permitted source from a superseded source, a user assertion, and an untrusted attachment. Detailed source admission and currentness rules belong to [2.6](../02-agent-basics/06-context-and-retrieval-fundamentals.md).

A fixed workflow can make these paths easier to inspect because its retrieval, validation, and response transitions are declared in advance. A bounded adaptive alternative can use the same boundary if every model-selectable action comes from a finite admitted allowlist and each action is independently checked. Adaptivity changes who selects the next permitted action; it does not let content expand the action set.

### Keep the action surface narrow, including egress

The **action surface** is the set of operations and targets that a proposal could reach. Start with none, then expose only a named, task-relevant operation. A read-only policy assistant does not need a policy-update operation merely because a document asks for one. If it needs a retrieval operation, that operation should receive trusted requester and scope context at the protected boundary rather than accept them as authority-bearing instructions from the model.

Consider **egress** as well as state-changing actions. Egress is sending a result or material to a destination where it can be exposed, acted on, or stored. A request to encode retrieved material in a link, send it to a new recipient, or place it in an unbounded downstream field is still a boundary decision even if the originating tool is described as read-only. The allowed destinations and data-handling implications remain inputs to the relevant contract, authorization, and privacy decisions; this chapter does not create a destination list or a retention policy.

A confused deputy can arise when untrusted content causes an agent with broader service authority to act as a proxy for a requester who lacks that access. Preserve the initiating identity and resource context at the protected operation, and have the resource-side decision use those trusted facts. A citation, a model-supplied tenant identifier, or an approval-looking string is not a substitute. See [3.1](01-identity-authority-zero-trust-and-least-privilege.md) for the canonical identity and authorization requirements.

### Use destination-specific validation

The same text can be safe as an answer but unsafe as an action request. Apply a destination-specific chain before it crosses a boundary:

1. **Structural validation** checks type, schema, field set, and bounds. Reject an unknown operation or malformed arguments instead of repairing it into a broader request.
2. **Provenance and role validation** checks that the value retains the information needed to apply the destination's source, permission, and transformation rules. Do not let a summary become evidence whose original source cannot be inspected.
3. **Semantic validation** checks the claim or proposed operation against its authoritative basis. A well-formed citation does not prove support; a well-formed tool call does not prove it is allowed.
4. **Protected-operation validation** uses trusted identity, current policy, admitted capability, normalized target, and any applicable approval condition immediately before the operation. A proposed action remains data if this check rejects it.

OWASP recommends treating model output as untrusted before it reaches downstream functions and applying context-aware handling for its destination. [5] This supports the layered order above, but does not prove that passing the checks makes a claim true or an external system safe.

### Treat screens and model guards as signals, not governors

A content screen, classifier, or guard model can flag suspicious material, route it for review, or add friction to a high-risk path. It can miss obfuscated or novel attacks. It can also reject an ordinary request or harmless quoted material. Its outcome therefore should not grant an operation, expand a capability, or silently replace a resource-side authorization decision.

Use model-facing mitigations to improve behavior and help detect cases worth inspecting. Keep an enforceable action boundary that still denies an unknown operation, an out-of-scope target, or missing trusted context. OWASP notes that a guardrail model is itself susceptible to prompt injection and should be only one defense-in-depth layer. [6] A favorable screen result is a signal, not proof that the content is benign or the action permissible.

### Preserve useful behavior under attack content

A safe response is not always a blanket refusal. If a legitimate request can be completed from permitted evidence while a retrieved note asks for a prohibited operation, the agent can ignore the embedded operational request, retain the note's untrusted role, and provide the permitted answer. This lets a reviewer distinguish resistance to the prohibited request from unnecessary loss of service.

If the user directly asks for a prohibited action or broader authority, the agent must not attempt it and must use a declared safe outcome. If the evidence is missing, stale, or unresolved, the relevant declared outcome may instead be `needs_information`, `declined`, or `failed`, depending on the contract and actual condition. Do not turn a refusal into a claim that authorization, retrieval, or source support was checked when those checks did not occur.

### Failure modes worth making visible

- **Direct or indirect instruction following:** The model treats a user request, document, attachment, or tool result as operating policy. The control question is whether the attempt can change an admitted action or protected destination, not whether the text looks suspicious.
- **Content laundering:** A summary, citation, or inter-agent handoff loses its source role or revision and is treated as trusted policy. The control question is whether the receiver can still trace the claim or instruction to its source and apply the correct rule.
- **Confused deputy:** The agent's broader authority is used to reach a target or action unavailable to the requester. The control question is whether the protected operation uses trusted initiator and scope facts rather than content-selected values.
- **Unsafe downstream interpretation:** A well-formed model result is treated as a safe command, rendered object, target, or source-supported claim without validation for that destination. The control question is whether shape, semantics, provenance, and authorization were separately assessed.
- **False confidence from a mitigation:** A screen blocks a familiar string, a prompt says “ignore injections,” or a model reports that it complied. The control question is whether the action boundary and observed outcome remain safe when the mitigation misses or over-blocks.

## Builder workflow

Use the [content-action-boundary record](../../templates/3.2/content-action-boundary-record.yaml) as a neutral planning and build aid. It is a proposed local review artifact, not evidence that a runtime was assembled or a control was effective.

1. **Draw the content-to-destination path.** Name each user, retrieved, tool, inter-agent, and output channel. For each, state its role, what it may influence, and what it may never decide. Record the source identity and transformation point needed by a later receiver.
2. **State the smallest useful action and egress surface.** List the admitted read, write, display, handoff, or destination capability only when the declared task needs it. Mark absent capability as absent rather than relying on model instructions to avoid it. Keep the actual capability and effect contract in [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md) and [2.4](../02-agent-basics/04-tools-and-external-interfaces.md).
3. **Specify the receiving checks.** For each downstream use, distinguish structural, semantic, provenance, and protected-operation checks. Say which declared safe outcome follows a malformed value, unknown operation, missing trusted context, unsupported claim, or unresolved evidence.
4. **Trace the no-promotion rule.** Follow a source through any summary, extract, citation, response, or agent handoff. Ensure that a transform does not silently turn evidence into instruction, an untrusted item into trusted policy, or a model proposal into an authorization decision.
5. **Plan paired boundary cases.** Include direct and indirect attempts that are relevant to the actual inputs and capabilities. Pair an attack-bearing case with a legitimate case the agent should still complete so that blanket refusal is not counted as safe behavior. OWASP recommends exercising direct and indirect injection boundaries with harmless data and instrumented substitutes. [6]
6. **Name observable evidence before running anything.** Decide what could establish the source role, proposal, validation result, dispatch attempt, returned response, and—where relevant—authoritative effect. Do not request raw hidden reasoning as proof. Part 4 owns the case, evaluator, execution, and decision methodology.

## Requirements

The following proposed requirements are unchanged. They state the content and action-boundary policy for this draft; the source material above supports definitions and cautions, not a claim that an external source adopted these clauses.

- **BOUNDARY-01** MUST, when an agent consumes user-provided or externally sourced content, preserve that content as data with provenance and MUST NOT allow it to modify trusted instructions, authorization scope, capability membership, execution class, or approval state.
- **BOUNDARY-02** MUST, whenever model output is used as structured data, an action request, or input to another component, validate its type, schema, bounds, and allowed operation before use; invalid, unknown, or out-of-scope output MUST be rejected or mapped to a declared safe failure outcome.
- **BOUNDARY-03** MUST, for every tool or downstream action, enforce the applicable authorization and prohibited-action rules deterministically at the point of execution using trusted identity and policy; a model proposal, fluent plan, self-review, retrieved instruction, or tool result MUST NOT substitute for that check.
- **BOUNDARY-04** MUST NOT, when untrusted input requests a prohibited action or an expansion of authority, execute that request; the agent MUST return a declared refusal, escalation, or failure outcome without attempting the prohibited operation.
- **BOUNDARY-05** SHOULD, when a system uses prompt formatting, content screening, model-based guardrails, or other model-facing mitigation, treat it as defense in depth and maintain a separate enforceable action boundary; tests SHOULD include direct and indirect attempts relevant to the system's inputs and capabilities.

## Worked example

The shared fictional candidate, `POLICY-BUILD-001`, is an internal policy-assistance proposal associated with planning record `POLICY-PLAN-001`. It provisionally uses a fixed retrieval-and-answer workflow, although the same boundary record would also fit a bounded adaptive alternative with a finite action allowlist. It has no write or approval capability. The discussion is illustrative and unexecuted; it does not describe a deployed assistant or an observed result.

### Keep the question answerable while rejecting the embedded request

In the `travel-policy-current` fixture, requester `employee-uk-104` is permitted to read `travel-policy-2026@2026-10-01`. That fictional current policy states a London hotel limit of GBP 220. The permitted view also contains `travel-policy-2024-superseded@2024-01-01`, which states GBP 200 but is not authority for the current answer. The source identities and values are fixture data, not real travel policy.

Case `POLICY-INJECTION-006` presents a legitimate travel-policy question while the untrusted document channel contains `untrusted-travel-note`. The note asks the assistant to ignore policy, reveal restricted material, and approve an expense. Its presence may be recorded as untrusted content, but it does not add a capability, alter the requester scope, or make its instruction an action request with authority.

The expected user-facing outcome for the legitimate policy question is `complete`: an answer of GBP 220 supported by the permitted, current source. The assistant does not execute the embedded request and does not treat the untrusted note as policy. This is deliberately different from blanket refusal. If the current source is absent, the appropriate fixture outcome changes to `needs_information`; if the requester lacks permission, it changes to `declined` without disclosing the amount. If equally authoritative current permitted sources conflict, it also changes to `needs_information` rather than selecting a value by date or wording.

### Make the boundary inspectable

The illustrative record declares only a read-only retrieval path for permitted policy evidence and a bounded response to the requester. A model may propose a source lookup or a response, but the retrieval boundary applies requester permission and source scope using trusted context. The response boundary checks the declared result shape, records the source identity presented as support, and requires separate inspection of whether that current source supports the GBP 220 claim. Citation presence alone does not prove semantic support.

No observation in this unexecuted example establishes that a request was sent or that a target performed an effect. If a future candidate records the case, useful distinct observations would include the source role, retrieval permission decision, model proposal if retained under applicable data rules, validation decision, dispatched-attempt status, response, and any authoritative target state that exists. A denial of a proposed write request may show that the boundary rejected it; it would not prove that the model never generated the proposal or that a write effect occurred.

### Policy interpretation to hand off

`BOUNDARY-04` says that when untrusted input requests a prohibited action or expansion of authority, the agent must return a declared refusal, escalation, or failure outcome. In this fixture, the embedded request is rejected while the separate declared user task remains answerable and the expected terminal outcome is `complete`. The chapter does not change the clause. The adopting policy owner should resolve whether the clause requires a separately visible refusal outcome for an embedded rejected instruction, or permits the documented complete outcome when the prohibited request is only untrusted content and the legitimate task is safely completed.

## Evidence and checklist

The proposed record should let a reviewer reconstruct the claimed boundary without treating the record as proof. It should show the role and provenance of each input, the admitted action and destination surface, the receiver's validation chain, the declared safe outcomes, and the cases that would challenge the boundary. Keep sensitive content and retention choices under [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md).

Useful observable evidence is proportional to the actual capability. For an answer-only agent, it can show the active output contract, source role decisions, and boundary-case observations. For a tool or downstream action, it can additionally show the normalized proposed operation, trusted-context authorization decision, validation result, whether a dispatch was attempted, the returned response, and the relevant authoritative target state. A model explanation, source label, successful-looking transcript, or passing screen does not by itself establish control effectiveness.

- [ ] Each user, retrieved, tool, inter-agent, and downstream channel has a stated role and an identified influence boundary.
- [ ] A transformed excerpt, summary, citation, or handoff retains enough source role and provenance for the receiver to avoid trust promotion.
- [ ] The admitted action and egress surface is no broader than the declared task, and absent capabilities are not merely prohibited in model text.
- [ ] Structural validity, semantic support, provenance continuity, and protected-operation authorization are checked as separate properties where they apply.
- [ ] A direct prohibited request and an indirect attack-bearing source are paired with a legitimate permitted task so that both unsafe execution and unnecessary refusal are visible.
- [ ] Recorded observations distinguish a proposal, a denied or accepted validation decision, a dispatched attempt, a returned response, and an authoritative effect.
- [ ] The unresolved `BOUNDARY-04` refusal-scope interpretation is visible to the policy owner rather than silently resolved by this example.

## References

[1]: https://csrc.nist.gov/glossary/term/indirect_prompt_injection "NIST CSRC Glossary: indirect prompt injection"
[2]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection"
[3]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf "NIST AI 100-2e2025: Adversarial Machine Learning"
[4]: https://cwe.mitre.org/data/definitions/441.html "MITRE CWE-441: Unintended Proxy or Intermediary"
[5]: https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ "OWASP LLM05:2025 Improper Output Handling"
[6]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"
