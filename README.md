# Bedrock Threat Model

Securing an AWS Bedrock (GenAI) application by doing real threat modeling first — not just wrapping the API call in IAM and calling it "secure."

## Why this exists

Most "secure AI app" projects mean: added authentication, used HTTPS, maybe added a WAF. That's basic hygiene, not security engineering. This project starts from a threat model — identifying trust boundaries, data flows, and attacker goals specific to an LLM-backed application — and then implements controls that trace back to a specific identified threat.

## The application

A minimal AWS Bedrock-backed application (describe your actual app here: e.g., a document Q&A assistant, a customer support bot, etc.) used as the subject of the threat model.

## Threat modeling process

1. **System decomposition** — data flow diagram showing user input, application layer, Bedrock API, any retrieval/knowledge base, and output
2. **Trust boundary identification** — where untrusted input crosses into privileged context (e.g., user prompt → model → downstream action)
3. **STRIDE analysis** — applied per component, with LLM-specific extensions:
   - Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege
   - Plus GenAI-specific threats: prompt injection, jailbreaking, training/context data leakage, excessive agency (over-permissioned tool use), output handling vulnerabilities
4. **Threat prioritization** — likelihood × impact, informed by [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
5. **Control mapping** — every implemented control ties back to a specific threat ID, documented in a traceability table

## Threat model artifact

See [`/threat-model/`](./threat-model) for:
- Data flow diagram
- STRIDE table (threat → likelihood → impact → mitigation)
- Threat-to-control traceability matrix

## Key threats addressed

| Threat | Risk | Mitigation implemented |
|---|---|---|
| Prompt injection via user input | High | Input sanitization + system prompt isolation |
| Excessive agency (model triggers unintended actions) | High | Least-privilege IAM scoping on any tool/action the model can invoke |
| Sensitive data leakage in model output | Medium | Output filtering / PII redaction before response returned |
| Unbounded cost / DoS via prompt flooding | Medium | Rate limiting + request size caps |

*(Fill in with your actual implemented controls — this table is the heart of the project.)*

## Architecture

```
app/              # Application code calling Bedrock
threat-model/     # DFD, STRIDE table, traceability matrix
controls/         # Implemented mitigations (IAM policies, filters, rate limits)
docs/             # Write-up of process and decisions
```

## Getting started

```bash
git clone https://github.com/<your-username>/bedrock-threat-model.git
cd bedrock-threat-model
pip install -r requirements.txt
# configure AWS credentials with Bedrock access
python app.py
```

## What I'd add next

- Automated red-teaming against the deployed app (adversarial prompt test suite)
- Continuous monitoring for prompt injection attempts in production logs

## Limitations

This threat model covers the application as scoped; it does not cover the underlying foundation model's training data or Bedrock's own infrastructure security, which is AWS's responsibility under the shared responsibility model.

## License

MIT
