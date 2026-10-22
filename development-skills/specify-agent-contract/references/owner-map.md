# Canonical owner map

Use this map to locate the normative source before drafting or reviewing a contract. This package translates the listed groups into planning outputs; it does not replace their authority.

| Group ID | Canonical chapter-relative path | Immutable source | Package use |
| --- | --- | --- | --- |
| `ANATOMY` (`ANATOMY-01`–`ANATOMY-05`) | `development-guide/02-agent-basics/01-agent-anatomy-runtime-loop-and-project-organization.md` | [2.1 requirements](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/02-agent-basics/01-agent-anatomy-runtime-loop-and-project-organization.md#requirements) | Map responsibilities, bounded loop, proposal/enforcement separation, terminal handling, output boundary, and shared-capability ownership into the draft contract. |
| `CONTRACT` (`CONTRACT-01`–`CONTRACT-06`) | `development-guide/02-agent-basics/02-agent-contracts-and-configuration.md` | [2.2 requirements](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/02-agent-basics/02-agent-contracts-and-configuration.md#requirements) | Define typed interfaces, fail-closed construction, capability admission and bounds, trusted dependencies, validated outcomes, and effective-configuration manifest planning. |
| `PROMPT` (`PROMPT-01`–`PROMPT-05`) | `development-guide/02-agent-basics/03-prompts-and-instructions.md` | [2.3 requirements](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/02-agent-basics/03-prompts-and-instructions.md#requirements) | Define reviewable instructions, roles for request and evidence, contract-consistent exemplars, output alignment, and revision/evaluation identity. |

## Boundary handoffs

The planning output must name, but not reproduce or decide, issues owned outside these groups. A protected identity, authorization, content/action boundary, external interface, source/retrieval, evaluation, or execution decision needs its canonical owner and an explicit later handoff. Do not imply that this package invokes another package, grants a capability, or completes a downstream review.

## Source identity

The immutable source commit is `151fca01fbc609c5550c563c902946db540c2f4c`. The local requirement index is a navigation aid; the linked chapter requirements remain the authoritative source for these groups.
