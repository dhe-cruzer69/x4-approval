# X4 Approval

**Human-in-the-loop control** for high-impact agent actions.

## Risk → Autonomy Matrix

| Risk | Agent behavior |
|---|---|
| Read-only | Automatic |
| Low-impact reversible | Automatic |
| External communication | Approval depending on context |
| Financial transaction | Human approval |
| Production mutation | Human approval |
| Destructive operation | Explicit approval |
| Uncertain result | Stop + review |

## Features

- Short-lived approval tokens (never inferred from model text)
- Policy engine integration
- Audit trail of every decision
- Escalation to human when status is `UNKNOWN`

## Safety

Models cannot grant themselves permission.  
Approval is an external signal, not a model claim.

Part of the X4 7-capability architecture.

Apache-2.0
