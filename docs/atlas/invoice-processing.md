[← All 14 workflows](README.md) · [Guide](../../README.md) · [Recipes](../workflows.md) · [VYR source](https://vyrwork.com/agent-os/invoice-flow)

# 06. Invoice Processing

**BUILT FOR YOU · Checked 27 September 2026**

Build-to-order invoice review and Xero draft integration; payment authority stays with finance.

> **Goal:** Convert an invoice into a reviewed accounting draft with explainable exceptions.

The role design, worked example and evaluation below are educational proposals. The status and workflow boundary come from the linked VYR page; these role names are not a claim about its exact deployed agent roster.

## Trigger and collaboration

A supplier invoice arrives as an approved attachment or scan.

Extraction attaches each field to its source. Matching compares independent records. Exceptions travel with the conflicting values, so finance can resolve them before the ledger agent prepares an approved draft.

```mermaid
flowchart LR
A["Capture agent"]
B["Extraction agent"]
C["Matching agent"]
D["Exception agent"]
E["Ledger agent"]
H{"Finance decision"}
O(["Reviewed ledger draft with source and exception history"])
A -->|source document| B
B -->|extracted fields| C
P["PO and receipt"] --> C
C -->|variance packet| D
D --> H
H -->|approved coding| E
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
| Capture agent | Invoice + original source | Source-preserved document record |
| Extraction agent | Document record | Supplier, amount, tax and line-item fields |
| Matching agent | Extracted fields + PO + receipt | Variance and possible-duplicate report |
| Exception agent | Mismatches + finance rules | Finance review packet |
| Ledger agent | Finance-approved coding | Draft Xero entry and integration receipt |

**Human decision:** Finance resolves mismatches and retains accounting decisions and payment authority.

**Boundary:** No bank access or automatic payment. Extraction confidence does not establish invoice validity.

**Done means:** Reviewed ledger draft with source and exception history.

## Worked example

Fictional run: an invoice lists 12 units but the receipt records 10. Matching passes both figures to finance. The draft remains held until the discrepancy is resolved; approval creates an accounting draft, never a bank transfer.

This is a fictional scenario, not a customer result or a performance claim.

## How to evaluate it

Test duplicate handling, arithmetic reconciliation, field-source traceability and exception routing.

Keep a run ID, dated source references, permitted actions, current state, unresolved questions and decision owner with every handoff. Confirm external writes from the receiving system before declaring them complete. See the [build playbook](BUILD_PLAYBOOK.md) for implementation and model-role guidance.
