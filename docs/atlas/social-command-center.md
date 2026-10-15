[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/social-media-flow)

# 04. Social Command Center

**LIVE · Checked 27 September 2026**

Live FeedHive telemetry is read-only; new writes use a separate approval-bound publisher.

> **Goal:** Turn approved content into a controlled release and observe its actual delivery.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

A source item has permission for social repurposing.

Drafting and review prepare the release packet. A person approves the exact copy, image, accounts, labels and schedule. A separate publisher validates that binding; the observer only reads resulting telemetry.

```mermaid
flowchart LR
A["Source agent"]
B["Channel writer"]
C["Brand reviewer"]
D["Publisher service"]
E["Observer agent"]
H{"Named-human manifest approval"}
O(["Approved release receipt and a separate read-only delivery report"])
A -->|approved source| B
B -->|copy and image| C
C -->|exact release manifest| H
H -->|bound approval| D
D -->|separate write| F["FeedHive"]
F -->|read-only evidence| E
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
| Source agent | Approved owned content | Source packet and usage context |
| Channel writer | Source packet + platform rules | Channel-specific copy and image proposal |
| Brand reviewer | Proposed content + brand rules | Supported claims and release manifest |
| Publisher service | Named-human approval + exact manifest | Revalidated FeedHive write and receipt |
| Observer agent | Read-only FeedHive snapshots | Delivery state, audience and measurement report |

**Human decision:** Named-human approval binds the exact release manifest. Any changed field invalidates release.

**Boundary:** The command center itself cannot create, approve, edit, schedule or delete posts.

**Done means:** Approved release receipt and a separate read-only delivery report.

## Worked example

Fictional run: a reviewer approves Tuesday copy for one account. A later image swap makes the binding invalid, so the publisher holds. After a fresh approval, a release can proceed; the observer reports the returned delivery state without mutating it.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Test changed-manifest rejection, wrong-account rejection and receipt-to-telemetry reconciliation.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
