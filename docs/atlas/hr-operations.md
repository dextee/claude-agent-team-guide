[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/hr-flow)

# 08. HR Operations

**BUILT FOR YOU · Checked 27 September 2026**

Build-to-order onboarding and policy routing; Talenox or Payboy integration is scoped and tested.

> **Goal:** Make a new starter's onboarding complete, attributable and reviewable.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

HR approves a role, start date and onboarding owner.

The case agent fans work out to documents, task coordination and policy support. Completion joins their evidence; assigned tasks do not count as completed tasks.

```mermaid
flowchart LR
A["Case agent"]
B["Document agent"]
C["Task coordinator"]
D["Policy agent"]
E["Completion agent"]
H{"HR review"}
O(["Completed checklist with owner confirmations, or an explicit outstanding-items list"])
A --> B
A --> C
A --> D
B -->|document state| E
C -->|owner confirmations| E
D -->|supported policy context| E
B -->|missing evidence| H
D -->|sensitive question| H
H -->|resolved decision| E
E -->|all required evidence present| O
classDef agent fill:#f6f0e6,stroke:#9f7557,color:#222222
classDef human fill:#ffe8b6,stroke:#b57821,color:#222222
classDef outcome fill:#e3eee6,stroke:#4e775c,color:#222222
class A,B,C,D,E agent
class H human
class O outcome
```

## What each agent passes forward

| Role | Receives | Produces |
|---|---|---|
| Case agent | Approved starter brief | Role-specific onboarding checklist |
| Document agent | Checklist + submitted documents | Required-document status and gaps |
| Task coordinator | Checklist + named owners | Equipment, access and manager tasks |
| Policy agent | Employee question + approved policies | Supported answer draft or HR referral |
| Completion agent | Owner confirmations + HR decisions | Verified onboarding state |

**Human decision:** HR resolves missing evidence and sensitive exceptions, and retains all employment decisions.

**Boundary:** No autonomous salary, payroll, performance, discipline or termination decisions.

**Done means:** Completed checklist with owner confirmations, or an explicit outstanding-items list.

## Worked example

Fictional run: a new starter has supplied the required documents, but IT has not confirmed access. Completion leaves onboarding open and identifies IT as the owner. An unusual employment-term question goes to HR.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Track overdue ownership, falsely completed tasks, document-access boundaries and policy-source coverage.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
