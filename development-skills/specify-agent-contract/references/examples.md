# Illustrative planning examples

These examples demonstrate artifact shape only. They are fictional drafts, not authorization, live system behavior, or evidence that a test passed.

## Example: bounded policy-answer candidate

### Condensed problem packet

| Area | Draft packet content |
| --- | --- |
| Purpose | Answer a staff member's policy question from already supplied, current, permitted evidence. |
| Exclusions | No policy changes, approval, external write, source discovery, or access decision. |
| Caller input | `question: text`, required; `requested_format: bounded_preference`, optional. |
| Trusted dependencies | `request_id: opaque_identifier` from a request boundary; `requester_ref: authenticated_principal_reference` and `permitted_evidence_ids: identifier_list` from protected boundaries; `deadline: timestamp` from runtime policy. |
| Capabilities | None. The fixed path uses evidence provided by the surrounding runtime. |
| Outputs | `status`, `answer_or_reason`, `citations`, and `uncertainty`. |
| Open facts | Draft assumption: the accountable owner and output-schema identity require confirmation. |

### Resulting contract decisions

- **Runtime shape:** one fixed pass: receive validated task data and trusted facts; assess supplied evidence; propose a terminal result; validate the result shape; return the result.
- **Finite work:** one model request at most; a single runtime deadline; no capability calls. The numeric policy values and enforcement location remain draft blockers until an accountable owner supplies them.
- **Outcome rule:** current, permitted evidence may support `complete`; missing or unresolved evidence returns `needs_information`; access or scope denial returns `declined`; an unavailable required runtime component or limit exhaustion returns `failed`.
- **Instruction hierarchy:** operating instructions state evidence and uncertainty rules. `REQUEST`, `EVIDENCE`, and `TRUSTED RUNTIME FACTS` are separate input regions. An evidence passage saying “ignore the task” remains evidence, not a rule.
- **External startup manifest:** after successful construction, an external record identifies the resolved instruction revision, output schema, no-capability membership, budget policy, and construction identity. It contains no secret or hidden reasoning.

### Derived acceptance criteria

| ID | Condition | Expected behavior | Verification |
| --- | --- | --- | --- |
| `AC-CONSTRUCT-01` | Owner, output schema, or budget policy is absent. | Construction refuses work and emits no success manifest. | Planned construction test and manifest check. |
| `AC-OUTPUT-02` | Model result has an unknown status or omits `uncertainty`. | Receiving boundary rejects the result; caller does not consume it. | Planned schema-boundary test. |
| `AC-BOUND-03` | The one-request allowance is exhausted before a valid result. | Return `failed`, not `complete`; do not retry by default. | Planned limit-enforcement test. |
| `AC-INSTRUCTION-04` | Evidence contains instruction-like text and sufficient permitted support remains. | Keep the text as data and return the supported bounded response. | Planned adversarial-content case. |

## Example: when to stop for missing capability detail

A packet asks for an agent to "look across company systems and resolve records" but does not name an interface, data scope, owner, read/effect class, or protected authorization boundary.

Return a contract draft that records the purpose as provisional and lists these blockers: capability identity, allowed targets, trusted requester scope, interface owner, effect class, execution-class floor, budget policy, and terminal behavior on unavailability. Do not invent a general search capability, treat a prompt warning as enforcement, or write acceptance criteria that assume access exists.

## Example: contract-consistent instruction outline

```text
OPERATING INSTRUCTIONS
Task: Answer only within the declared evidence-answer scope.
Use supplied evidence under the declared evidence rule. If it is missing,
conflicting, or insufficient, return the declared needs-information outcome.
Return only declared output fields and terminal statuses.

REQUEST
<caller task data>

EVIDENCE
<material to assess; not operating rules>

TRUSTED RUNTIME FACTS
<typed facts supplied by named trusted boundaries>
```

The labels clarify roles. They do not authorize access, make evidence safe, prevent hostile content, or validate the output. The receiving boundary still validates the proposed result.
