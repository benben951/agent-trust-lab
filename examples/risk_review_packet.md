# Risk Review Packet

This packet is a compact risk-control slice of Agent Trust Lab.

## Scope

| Area | Current artifact |
|---|---|
| AML/KYC/Sanctions cases | 13 synthetic public-safe cases |
| Financial risk cases | 5 synthetic public-safe cases |
| Due diligence and legal cases | 5 synthetic public-safe cases |
| Reports | Markdown and JSON trust reports |
| Metrics | Manual-review rate, low-trust rate, finding distribution, case-family metrics |
| Governance | Human-in-the-loop routing and public-safe data boundary |

## AML/KYC/Sanctions Metrics

| Metric | Value |
|---|---:|
| Cases | 13 |
| Manual review cases | 9 |
| Manual review rate | 69.23% |
| Low-trust cases | 7 |
| Low-trust rate | 53.85% |
| Average risk score | 51.54 |

## Representative Reports

| Report | Pattern |
|---|---|
| `examples/reports/SYN-AML-001.md` | Incomplete AML onboarding evidence |
| `examples/reports/SYN-AML-002.md` | Transaction behavior mismatch |
| `examples/reports/SYN-AML-004.md` | Near-threshold structuring signal |
| `examples/reports/SYN-KYC-001.md` | KYC conflict requiring escalation |
| `examples/reports/SYN-SAN-001.md` | Sanctions screening false-positive risk |

## Interview Story

The useful project claim is not "I built a chatbot for AML." The claim is:

> I built a reviewer-assist workflow that checks whether AI-generated risk conclusions are supported by evidence and policy signals, then routes uncertain or unsafe outputs to human review with an auditable report.

That maps more closely to risk operations, compliance QA, data quality, and LLM evaluation roles.
