[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/tuition-flow)

# 11. Tuition Trial Booking

**BUILT FOR YOU · Checked 27 September 2026**

Build-to-order enquiry and trial-class booking workflow; placement stays with centre staff.

> **Goal:** Match a parent's enquiry to a genuinely available trial class.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

A parent specifies subject, level, location and preferred time.

Schedule supplies actual capacity to options. The parent chooses a valid slot. Placement or special-arrangement questions branch to staff; booking records only the accepted, permitted outcome.

```mermaid
flowchart LR
A["Enquiry agent"]
B["Schedule agent"]
C["Options agent"]
D["Staff handoff agent"]
E["Booking agent"]
H{"Centre staff"}
O(["Accepted trial booking or a staff-owned placement question"])
A -->|parent constraints| B
B -->|available capacity| C
C -->|parent accepts permitted slot| E
C -->|placement exception| D
D --> H
H -->|staff decision| E
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
| Enquiry agent | Parent-supplied constraints | Structured trial request |
| Schedule agent | Timetable + capacity + trial rules | Available classes meeting the constraints |
| Options agent | Valid classes | Clear options for parent acceptance |
| Staff handoff agent | Placement or child-specific question | Contextual centre-staff referral |
| Booking agent | Accepted slot + applicable approval | Trial record and permitted follow-up |

**Human decision:** Centre staff own placement, assessments, special arrangements, fee exceptions and progress discussions.

**Boundary:** No assessment of a child's ability or invented class capacity.

**Done means:** Accepted trial booking or a staff-owned placement question.

## Worked example

Fictional run: a parent wants a weekday maths trial near home. Two valid classes are offered. A request to move the child to a higher level pauses that decision for centre staff before the booking is finalised.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Test capacity accuracy, acceptance capture, child-specific escalation and follow-up permissions.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
