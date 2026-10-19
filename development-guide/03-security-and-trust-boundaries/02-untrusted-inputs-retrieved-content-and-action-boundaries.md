# 3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries

**Status:** 0.5.0-draft.2 — draft

**Audience:** Builders, security reviewers, evaluators, and operators of agents that interpret external content or pass results to another component.

**Applicability:** Apply the content boundary whenever an agent receives user-provided, retrieved, tool-returned, or inter-agent material. Apply the action boundary whenever model output can be rendered, stored, forwarded, or used to request an operation. An agent with no external operation still has an output boundary and can still mislead or disclose.

**Reader question:** How can an agent use outside material for a legitimate task without letting that material create authority, redirect a protected action, or gain trust as it moves through the system?

[Part 3 — Security and Trust Boundaries](README.md) · [Applicability](../../applicability.md) · [3.1 Identity, Authority, Zero Trust, and Least Privilege](01-identity-authority-zero-trust-and-least-privilege.md) · [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) · [3.3 Data Privacy, Handling, and Minimum Audit Evidence](03-data-privacy-handling-and-minimum-audit-evidence.md)

## Purpose and applicability

A requester's question, a retrieved document, a tool response, another component's message, or content in a file or image may be useful, mistaken, stale, or malicious, or all at once. The core rule: **content can inform a result; it cannot rewrite the conditions under which the result is produced.**

A **direct prompt injection** arrives in a user-controlled request. An **indirect prompt injection** arrives through a resource an attacker can influence, such as a document, website, message, or attachment; NIST defines it as prompt injection carried out through resource control rather than user input. [1] OWASP and NIST's adversarial machine learning taxonomy cover both; OWASP notes that retrieval augmentation and fine-tuning do not fully remove the vulnerability. [2] [3]

A read-only answer can still disclose restricted information or launder a stale claim into a current-looking answer. Yet a hostile sentence in a useful document should not automatically make the legitimate task impossible.

Authorization is in [3.1](01-identity-authority-zero-trust-and-least-privilege.md), interface contracts and effects in [2.4](../02-agent-basics/04-tools-and-external-interfaces.md), source admission and currentness in [2.6](../02-agent-basics/06-context-and-retrieval-fundamentals.md), and destinations, retention, and audit in [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md).

## Working model

### Four roles that must not collapse

**Trusted operating context** is the reviewed task boundary plus runtime facts from declared trusted sources: admitted capabilities, authenticated requester scope, allowed destinations, the output contract. A persuasive request, document label, model statement, or tool response does not establish it.

**Untrusted content** is material to interpret: user text, retrieved passages, tool results, messages from other agents, and summaries of them. A source may be approved for a domain fact while its instruction-like text stays untrusted for operational control.

**A proposal** is a model-produced answer, structured value, suggested tool call, handoff, or claimed result. It stays data until a receiving boundary validates it for that destination.

**An action boundary** decides whether an operation, target, argument set, and destination are permitted in the current trusted context. It is not a prompt convention. MITRE describes the related confused-deputy failure: an intermediary forwards a request without preserving its original source, so its different authority is misused. [4]

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

The stages are different observations: a proposal need not be dispatched, a dispatched request can get a response with no effect, and an authoritative target record is different evidence again.

### Validate the property that matters

A schema, type, or bounds check asks whether a value has an acceptable **shape**. It can reject an unknown operation or malformed argument, but cannot show that a cited passage supports an answer, a destination is permitted, or an action is appropriate. A **semantic check** asks whether the value means something acceptable in its use, such as whether current, permitted evidence supports the claim. **Provenance validation** asks whether the record still carries the source identity, status, and transformation history the receiver needs.

**Content laundering** is losing these distinctions during a transform: an untrusted note is summarized, wrapped in a citation, or sent to another agent, then treated as trusted policy because its source role was dropped. A rewrite does not upgrade authority, freshness, permission, or truth. OWASP also warns that model output passed unchecked downstream can give indirect access to extra functionality. [5]

Labels, delimiters, prompt instructions, and model self-reflection help the model follow the roles but do not enforce them; authorization and parameter validation stay outside the model. [6]

## Decisions and best practices

### Decide what each channel may influence

Record each source's or consumer's role before connecting it. A policy document may support an amount, a user request may select a question, a tool result may supply a bounded observation; none may select a different tenant, add a capability, create approval, change the execution class, or choose an unreviewed destination.

Keep a compact source identity and status through retrieval, summarization, citation, and handoff, so a recipient can tell a current permitted source from a superseded one, a user assertion, or an untrusted attachment.

A fixed workflow is easier to inspect; a bounded adaptive design can use the same boundary if every model-selectable action comes from a finite admitted allowlist and is checked independently.

### Keep the action surface narrow, including egress

The **action surface** is the set of operations and targets a proposal could reach. Start with none and expose only named, task-relevant operations. Retrieval takes requester and scope from trusted context at the protected boundary, not from the model.

**Egress**, sending material where it can be exposed, acted on, or stored, is a boundary decision too, even through a "read-only" tool: a link that encodes retrieved material, a new recipient, or an unbounded downstream field. For network controls and isolation, see [3.1](01-identity-authority-zero-trust-and-least-privilege.md#isolate-execution-and-restrict-egress).

A confused deputy arises when untrusted content makes an agent with broader service authority act for a requester who lacks that access. Decide at the protected operation from the trusted initiating identity and resource context; a citation, model-supplied tenant, or approval-looking string is no substitute.

### Use destination-specific validation

The same text can be safe as an answer and unsafe as an action request. Before it crosses a boundary, apply this chain:

1. **Structural validation** checks type, schema, field set, and bounds. Reject an unknown operation or malformed arguments; do not repair them into a broader request.
2. **Provenance and role validation** checks the value keeps what the destination needs to apply its source, permission, and transformation rules.
3. **Semantic validation** checks the claim or operation against its authoritative basis. A well-formed citation does not prove support; a well-formed tool call does not prove permission.
4. **Protected-operation validation** uses trusted identity, current policy, admitted capability, normalized target, and any approval condition immediately before the operation.

OWASP advises treating the model like any other user, with a zero-trust approach, and handling output to fit each destination. [5]

### Treat screens and model guards as signals, not governors

A content screen, classifier, or guard model can flag suspicious material, route it for review, or add friction. It misses obfuscated or novel attacks and rejects harmless text, so its result never grants an operation, expands a capability, or replaces authorization. OWASP notes that a guardrail model is itself open to prompt injection and should be one defense-in-depth layer. [6]

### Defence in depth against prompt injection

No filter reliably stops prompt injection, so design so that injected text can do little harm. Researchers who tested twelve published defenses against attackers that adapted to them bypassed most with success rates above 90 percent, though many had reported near-zero rates on static attacks. [7] In a NIST CAISI red-teaming competition with over 250,000 attempts, every one of 13 frontier models was hijacked at least once, and robustness did not consistently track capability. [8] Plan on prevention by design and on containment, not detection alone.

- **Avoid the lethal trifecta.** Per Meta's Rule of Two, allow at most two of untrusted input, sensitive access, and state change or external communication per session; split the work or add supervision such as human approval when all three are needed. [9] See [3.1](01-identity-authority-zero-trust-and-least-privilege.md).
- **Plan, then execute.** Have the model fix the sequence of permitted actions before it reads untrusted content; tool results can fill in arguments but cannot add steps. [10]
- **Quarantine untrusted content.** In a dual-model pattern, a privileged model that calls tools never reads untrusted text; a quarantined model with no tools processes it and returns constrained, validated values, not free-form instructions. [10]
- **Separate control from data.** Capability-based designs track which values came from untrusted sources and let policy block a tool call whose arguments carry that taint. [11]
- **Narrow the model's choices.** Let the model select only from a fixed action list where possible, and minimize the context it sees at each step. [10]

These patterns trade flexibility for safety and none is complete. Keep the action boundary in front of them, and test with adaptive attackers, not only fixed attack lists. OWASP's agentic guidance extends the concern to tool misuse, memory poisoning, and inter-agent messages. [12]

### Preserve useful behavior under attack content

A safe response is not always a blanket refusal. If a legitimate request can be completed from permitted evidence while a retrieved note asks for a prohibited operation, the agent ignores the embedded request, keeps the note untrusted, and gives the permitted answer.

A direct request for a prohibited action or broader authority gets a declared safe outcome, never an attempt. If evidence is missing, stale, or unresolved, the outcome may be `needs_information`, `declined`, or `failed`, depending on the contract. Do not claim that authorization, retrieval, or source support was checked when it was not.

### Failure modes worth making visible

- **Instruction following:** can a request, document, attachment, or tool result change an admitted action or destination?
- **Content laundering:** can the receiver of a summary, citation, or handoff still trace the claim to its source?
- **Confused deputy:** does the operation use trusted initiator and scope facts?
- **Unsafe downstream interpretation:** is a well-formed result treated as a safe command or supported claim?
- **False confidence from a mitigation:** does the boundary hold when a screen, an "ignore injections" prompt, or a model's claim of compliance misses?

## Builder workflow

Use the [content-action-boundary record](../../templates/3.2/content-action-boundary-record.yaml) as a planning aid.

1. **Draw the content-to-destination path** with each channel's role and influence.
2. **State the smallest useful action and egress surface**; capability and effect contracts stay in [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md) and [2.4](../02-agent-basics/04-tools-and-external-interfaces.md).
3. **Specify the receiving checks** and the safe outcome for each failure.
4. **Trace the no-promotion rule** through every transform and handoff.
5. **Plan paired boundary cases**, exercising injection boundaries with harmless data and instrumented substitutes. [6]
6. **Name observable evidence**, not raw hidden reasoning; Part 4 owns evaluation method.

## Requirements

- **BOUNDARY-01** MUST, when an agent consumes user-provided or externally sourced content, preserve that content as data with provenance and MUST NOT allow it to modify trusted instructions, authorization scope, capability membership, execution class, or approval state.
- **BOUNDARY-02** MUST, whenever model output is used as structured data, an action request, or input to another component, validate its type, schema, bounds, and allowed operation before use; invalid, unknown, or out-of-scope output MUST be rejected or mapped to a declared safe failure outcome.
- **BOUNDARY-03** MUST, for every tool or downstream action, enforce the applicable authorization and prohibited-action rules deterministically at the point of execution using trusted identity and policy; a model proposal, fluent plan, self-review, retrieved instruction, or tool result MUST NOT substitute for that check.
- **BOUNDARY-04** MUST NOT, when untrusted input requests a prohibited action or an expansion of authority, execute that request; the agent MUST return a declared refusal, escalation, or failure outcome without attempting the prohibited operation.
- **BOUNDARY-05** SHOULD, when a system uses prompt formatting, content screening, model-based guardrails, or other model-facing mitigation, treat it as defense in depth and maintain a separate enforceable action boundary; tests SHOULD include direct and indirect attempts relevant to the system's inputs and capabilities.

## Worked example

The fictional, unexecuted candidate `POLICY-BUILD-001` (planning record `POLICY-PLAN-001`) is a policy-assistance proposal using a fixed retrieval-and-answer workflow (a bounded adaptive design with a finite action allowlist would fit the same record), with no write or approval capability.

### Keep the question answerable while rejecting the embedded request

In the `travel-policy-current` fixture, requester `employee-uk-104` may read `travel-policy-2026@2026-10-01`, which states a London hotel limit of GBP 220. The permitted view also holds `travel-policy-2024-superseded@2024-01-01`, which states GBP 200 but is not authority for the current answer.

Case `POLICY-INJECTION-006` presents a legitimate travel-policy question while the untrusted document channel contains `untrusted-travel-note`, which asks the assistant to ignore policy, reveal restricted material, and approve an expense. The note may be recorded as untrusted content, but it adds no capability, changes no requester scope, and carries no authority.

The expected outcome is `complete`: GBP 220, supported by the permitted current source, with the embedded request not executed and the note not treated as policy. If the current source is absent, the outcome is `needs_information`; if the requester lacks permission, `declined` without disclosing the amount; if equally authoritative current permitted sources conflict, `needs_information` rather than a pick by date or wording.

### Make the boundary inspectable

The record declares only a read-only retrieval path, which applies requester permission and source scope from trusted context, and a bounded response. The response boundary checks the declared shape and records the cited source; whether that source supports GBP 220 needs separate inspection. A future run would record source role, retrieval decision, validation decision, dispatch status, response, and any authoritative target state as distinct observations. A denied write proposal shows the boundary rejected it, not that no write occurred.

### Policy interpretation to hand off

`BOUNDARY-04` requires a declared refusal, escalation, or failure outcome when untrusted input requests a prohibited action, yet here the user task ends `complete`. The policy owner should decide whether it requires a separately visible refusal outcome for a rejected embedded instruction, or allows `complete` when the prohibited request is only untrusted content and the legitimate task is safely finished.

## Evidence and checklist

Sensitive content and retention stay under [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md). A model explanation, source label, or passing screen does not show a control works.

- [ ] Each channel has a stated role and influence boundary, and transforms keep enough provenance to prevent trust promotion.
- [ ] The action and egress surface is no broader than the task; absent capabilities are not merely forbidden in model text.
- [ ] The design removes at least one leg of the lethal trifecta, or supervises the combination.
- [ ] Structural, semantic, provenance and protected-operation checks are separate where they apply.
- [ ] Direct and indirect attacks, including adaptive ones, are each paired with a legitimate task, so both unsafe execution and needless refusal are visible.
- [ ] Observations separate a proposal, a validation decision, a dispatched attempt, a response, and an authoritative effect.
- [ ] The `BOUNDARY-04` refusal-scope question is visible to the policy owner.

## References

[1]: https://csrc.nist.gov/glossary/term/indirect_prompt_injection "NIST CSRC Glossary: indirect prompt injection"
[2]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection"
[3]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf "NIST AI 100-2e2025: Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations"
[4]: https://cwe.mitre.org/data/definitions/441.html "MITRE CWE-441: Unintended Proxy or Intermediary ('Confused Deputy')"
[5]: https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ "OWASP LLM05:2025 Improper Output Handling"
[6]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"
[7]: https://arxiv.org/abs/2510.09023 "Nasr et al.: The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections"
[8]: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition "NIST CAISI: Insights into AI Agent Security from a Large-Scale Red-Teaming Competition"
[9]: https://ai.meta.com/blog/practical-ai-agent-security/ "Meta AI: Agents Rule of Two: A Practical Approach to AI Agent Security"
[10]: https://arxiv.org/abs/2506.08837 "Beurer-Kellner et al.: Design Patterns for Securing LLM Agents against Prompt Injections"
[11]: https://arxiv.org/abs/2503.18813 "Debenedetti et al.: Defeating Prompt Injections by Design"
[12]: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 "OWASP Top 10 for Agentic Applications for 2026"
