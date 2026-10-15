[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/nurture-flow)

# 12. Lead Nurture

**BUILT FOR YOU · Checked 27 September 2026**

Build-to-order HubSpot follow-up workflow; there is no claimed live client deployment.

> **Goal:** Prepare a relevant next contact for the deal owner's approval.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

A scoped HubSpot deal meets an agreed inactivity rule.

Monitor selects eligible cases; context checks the actual history before drafting. The owner edits or rejects the proposal. Activity runs only after the approved release condition is satisfied.

```mermaid
flowchart LR
A["Monitor agent"]
B["Context agent"]
C["Drafting agent"]
D["Review coordinator"]
E["Activity agent"]
H{"Deal owner approval"}
O(["Approved follow-up with an activity record, or an explicit hold"])
A -->|eligible deal| B
B -->|actual history| C
C -->|draft and rationale| D
D --> H
H -->|revise| C
H -->|exact message approved| E
E --> O
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
| Monitor agent | Deal stage + inactivity rule | Eligible follow-up case |
| Context agent | Permitted CRM notes + prior contact | Relationship summary and missing-context flags |
| Drafting agent | Context + message policy | Suggested next touch and rationale |
| Review coordinator | Draft + recipient + timing | Deal-owner approval packet |
| Activity agent | Approved exact message | Send receipt and scoped CRM update |

**Human decision:** The sales owner controls recipient, copy, timing and send.

**Boundary:** A CRM record alone is not contact permission. Do not fabricate relationship history.

**Done means:** Approved follow-up with an activity record, or an explicit hold.

## Worked example

Fictional run: a proposal has been inactive for a week. Context finds a note that the buyer is away; the draft proposes waiting. The owner sets an appropriate date, and only the approved message becomes a send task.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Evaluate context accuracy, permission checks, changed-draft holds and CRM reconciliation.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
