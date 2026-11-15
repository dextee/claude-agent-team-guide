# Delegated task brief

A subagent starts with a fresh context: only this brief reaches it, and only its final message comes back. Include everything it needs.

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
