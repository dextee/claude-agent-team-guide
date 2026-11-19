# Delegated task brief

A new custom subagent starts without the lead's conversation history or the contents of files the lead already read. It gets its role instructions, the delegation prompt and applicable project instructions; in a Git repository it normally also gets a status snapshot. A fork is different: it inherits the parent conversation. Pass the decisions and evidence this role needs, and ask for a final answer the lead can use on its own. [What loads at startup](https://code.claude.com/docs/en/sub-agents#what-loads-at-startup)

## Outcome

The concrete result and who will use it.

## Context

The files, sources, base commit SHA, definitions and earlier decisions it needs. Paste paths and error messages; do not assume it can see the main conversation. If a CLAUDE.md rule must reach it and it starts without CLAUDE.md, restate the rule here.

## Owner and scope

The one agent responsible, and exactly which files, records or questions it may touch.

## Constraints

Authorized actions, time or usage budget, and anything it must not change.

## Acceptance

Observable evidence that would prove the task is done.

## Return

Use the [return contract](return-contract.md): STATUS, RESULT, EVIDENCE, CHECKS RUN with copied output, NOT CHECKED, CHANGED, OPEN.

## For verifiers only

Give a reviewer or auditor the original requirements and the artifact (diff, document, data), not the implementer's summary of its work.
