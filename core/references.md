# References

These sources informed the standard. They are conceptual guidance, open specifications, and risk frameworks; implementation-specific documentation belongs with the implementation that uses it, and framework behavior should be checked against the versions an implementation pins.

## Open standards and specifications

- [Agent Skills specification](https://agentskills.io/specification) — portable package structure, frontmatter rules, progressive disclosure, bundled resources, examples, and validation.
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification) — client-server protocol for exposing tools, resources, and prompts to models.
- [OpenTelemetry semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — span, metric, and event conventions for model and agent operations.
- [JSON Schema](https://json-schema.org/specification) — vocabulary for describing and validating typed data contracts.

## Risk and security

- [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/)
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [ISO/IEC 23894:2023 — AI risk management](https://www.iso.org/standard/77304.html)
- [European Commission AI Act overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [OWASP Agentic AI threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- [OWASP Securing Agentic Applications Guide](https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/)

## Notes

- Agent frameworks and SDKs may change while on pre-1.0 releases. Pin dependencies and treat upgrades as behavioral changes.
- NIST describes the AI RMF as voluntary guidance. Organizations remain responsible for applicable legal, regulatory, contractual, and internal requirements.
