[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/seo-flow)

# 02. Content Operations

**LIVE · Checked 27 September 2026**

Live eleven-agent pipeline; new generation is currently paused behind an approval backlog.

> **Goal:** Prepare a sourced article and release only the version an editor approves.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

An approved topic becomes eligible in the keyword calendar.

Planner checks overlap before commissioning research. Writer consumes the evidence packet; reviewer returns specific revision requests to writer. Only the editor can move an accepted version to release. These five role groups explain the public seven-stage control path; they are not the exact eleven-agent roster.

```mermaid
flowchart LR
A["Planner agent"]
B["Research agent"]
C["Writer agent"]
D["Review agent"]
E["Release agent"]
H{"Editor approval"}
O(["Approved article, verified route and recorded review decision"])
A -->|cleared brief| B
B -->|evidence and outline| C
C -->|draft| D
D -->|revision request| C
D -->|review packet| H
H -->|exact version approved| E
E -->|route verified| O
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
| Planner agent | Keyword + audience + page inventory | Brief and search-intent overlap decision |
| Research agent | Cleared brief + public sources | Evidence packet and outline |
| Writer agent | Outline + evidence + house style | Draft with traceable claims |
| Review agent | Draft + page inventory | Metadata, link and claim findings |
| Release agent | Exact approved article + reviewer decision | Published route and verification receipt |

**Human decision:** A named editor approves, rejects or requests changes before publication.

**Boundary:** Backlog pause remains visible; a prepared draft is not a live page or a ranking result.

**Done means:** Approved article, verified route and recorded review decision.

## Worked example

Fictional run: the planner finds that a proposed article overlaps an existing page and holds the draft. After the editor selects a distinct intent, research and writing proceed; a missing source sends the draft back to research before approval.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Track revision causes, unsupported-claim rate, duplicate-intent holds and successful live-route verification.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
