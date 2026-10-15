[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/fnb-flow)

# 10. F&B Supplier Reorder

**BUILT FOR YOU · Checked 27 September 2026**

Build-to-order operations blueprint; this case focuses on the detailed supplier-reorder path.

> **Goal:** Prepare the right stock replenishment for a manager's decision.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

An approved inventory or shift-handover signal crosses a reorder threshold.

Rules checks both inventory and open orders before supplier planning. The order draft carries assumptions into manager review. Receipt records the authorised release; it does not infer delivery.

```mermaid
flowchart LR
A["Stock agent"]
B["Rules agent"]
C["Supplier agent"]
D["Order agent"]
E["Receipt agent"]
H{"Manager approval"}
O(["Manager-approved order with traceable stock rationale"])
A -->|stock observation| B
P["Open orders and thresholds"] --> B
B -->|uncovered requirement| C
C -->|supplier proposal| D
D --> H
H -->|approved order| E
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
| Stock agent | Inventory + usage signal | Current stock observation and timestamp |
| Rules agent | Observation + thresholds + open orders | Reorder need or already-covered decision |
| Supplier agent | Needed items + approved supplier register | Quantity and supplier proposal |
| Order agent | Proposal + evidence | Draft purchase order and exceptions |
| Receipt agent | Manager-approved release | Order receipt and expected-delivery record |

**Human decision:** The manager owns supplier, quantity, substitution, price, spending and release.

**Boundary:** No unapproved spend or invented substitutions. Delivery remains unconfirmed until evidence arrives.

**Done means:** Manager-approved order with traceable stock rationale.

## Worked example

Fictional run: an ingredient appears below threshold, but an open order already covers tomorrow's need. Rules suppresses a duplicate reorder. A different item needs replenishment and proceeds as a manager-review draft.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Evaluate duplicate-order prevention, stock freshness, approval binding and order-receipt accuracy.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
