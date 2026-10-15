[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/spa-demo)

# 01. AI Receptionist

**DEMO · Checked 27 September 2026**

Working voice software using sample business data; no live booking connection.

> **Goal:** Turn an inbound call into a correct sample booking or a useful staff handoff.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

A caller asks for a Saturday appointment in their preferred language.

The concierge dispatches a factual enquiry to knowledge and a booking enquiry to availability. It joins their findings before asking the caller to choose. Sensitive or unsupported requests branch directly to a person.

```mermaid
flowchart LR
A["Concierge agent"]
B["Knowledge agent"]
C["Availability agent"]
D["Booking agent"]
E["Handoff agent"]
H{"Staff handoff"}
O(["Sample booking plus read-back, or a staff-ready handoff"])
A -->|factual question| B
A -->|booking request| C
B -->|supported answer| D
C -->|sample options| D
D -->|caller confirms| O
A -->|unsupported or sensitive| E
D -->|exception| E
E --> H
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
| Concierge agent | Call + supported-language list | Intent, language and minimum contact details |
| Knowledge agent | Intent + approved sample FAQs | Supported answer with a source reference |
| Availability agent | Service + requested time | Valid options from the sample calendar |
| Booking agent | Selected sample slot + caller confirmation | Sample booking record and read-back |
| Handoff agent | Unsupported request + conversation summary | Reason, unresolved question and staff queue item |

**Human decision:** Staff own sensitive requests, policy exceptions and unsupported questions.

**Boundary:** Every booking is a simulation. Do not represent a sample slot as a real appointment.

**Done means:** Sample booking plus read-back, or a staff-ready handoff.

## Worked example

Fictional run: a caller requests a 60-minute appointment on Saturday. Availability returns 14:00 and 16:00 from the demo calendar. The caller chooses 16:00; the booking agent repeats the date and time and records a sample booking. A refund question is transferred with its context.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Evaluate slot accuracy, handoff completeness, language handling and response latency against scripted calls.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
