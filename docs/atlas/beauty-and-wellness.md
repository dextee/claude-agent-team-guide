[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/beauty-flow)

# 14. Beauty & Wellness

**BUILT FOR YOU · Checked 27 September 2026**

Build-to-order salon booking and package-reference workflow; no running salon deployment is claimed.

> **Goal:** Coordinate service, therapist, room and package information into a valid booking.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

A customer requests a service at a preferred time and location.

Concierge requests roster and package checks in parallel. Booking joins their results without inventing entitlement. Staff resolve treatment, pricing or package exceptions before the permitted outcome is recorded.

```mermaid
flowchart LR
A["Concierge agent"]
B["Roster agent"]
C["Package agent"]
D["Booking agent"]
E["Follow-up agent"]
H{"Salon staff review"}
O(["Valid appointment and permitted follow-up, or a staff-owned exception"])
A -->|service constraints| B
A -->|permitted package query| C
B -->|feasible slots| D
C -->|balance reference| D
D -->|exception| H
H -->|staff decision| D
D -->|confirmed booking| E
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
| Concierge agent | Service + preferences | Booking constraints and minimum details |
| Roster agent | Therapist + room + duration calendar | Feasible appointment slots |
| Package agent | Permitted customer package record | Balance reference and applicable session rules |
| Booking agent | Valid slot + package context + acceptance | Approved appointment proposal |
| Follow-up agent | Confirmed booking + reminder policy | Permitted reminder or rebooking task |

**Human decision:** Staff own suitability, refunds, price changes, package disputes and exceptional bookings.

**Boundary:** Package lookup is not refund authority. No treatment advice or unsupported availability.

**Done means:** Valid appointment and permitted follow-up, or a staff-owned exception.

## Worked example

Fictional run: a requested therapist is free but the required room is occupied. Roster offers a later slot. If the package record is disputed, staff resolve it before any package-based booking promise.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Evaluate multi-resource conflicts, package-reference accuracy, staff routing and confirmation consistency.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
