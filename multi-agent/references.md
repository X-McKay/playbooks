# References

These sources inform the draft. The [Core and Advanced references](../core/references.md)
remain applicable to every member agent and to inherited durable execution,
evaluation, observability, risk, and security requirements.

Protocol and specification details MUST be checked against the versions pinned
by an implementation. Documentation for specific SDKs, frameworks, and
products belongs with the implementations that use them.

## Interoperability

- [Agent2Agent Protocol](https://a2a-protocol.org/latest/specification/) — interoperable agent discovery, task, message, artifact, and communication contracts.
- [Model Context Protocol](https://modelcontextprotocol.io/specification/latest) — model and agent connections to tools, resources, and prompts.
- [Agent Skills specification](https://agentskills.io/specification) — portable procedural capability packages.

Interoperability is not authorization. Protocol discovery and metadata provide
inputs to deterministic admission and policy; they do not establish trust,
conformance, or permission to invoke a remote agent.

## Observability

- [OpenTelemetry generative-AI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — agent, model, tool, token, and workflow telemetry conventions.
- [OpenTelemetry messaging semantic conventions](https://opentelemetry.io/docs/specs/semconv/messaging/) — producer, consumer, message, context propagation, span links, and asynchronous trace structure.
- [OpenTelemetry trace semantic conventions](https://opentelemetry.io/docs/specs/semconv/general/trace/) — trace and span conventions.

Semantic conventions may be experimental or move between specification
locations. Pin the convention version emitted by instrumentation and avoid
unstable high-cardinality attributes in production metrics.

## Risk, security, and governance

- [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/)
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework)
- [ISO/IEC 23894:2023 — AI risk management](https://www.iso.org/standard/77304.html)
- [European Commission AI Act overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [OWASP Agentic AI threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- [OWASP Securing Agentic Applications Guide](https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/)

## Notes

- Agent runtimes and multi-agent APIs change quickly, especially before a
  stable major release. Pin dependencies and treat upgrades as behavioral
  changes.
- A2A, MCP, OpenTelemetry, and other protocol support does not remove the need
  for application-specific authorization, data governance, risk assessment,
  evaluation, and operational controls.
- NIST describes the AI RMF as voluntary guidance. Organizations remain
  responsible for applicable legal, regulatory, contractual, and internal
  requirements.
