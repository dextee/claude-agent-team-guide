[Home](../README.md) · [How subagents run](how-subagents-run.md) · [Orchestration patterns](orchestration-patterns.md) · [Failure modes](failure-modes.md)

# Handoff contracts: brief in, evidence out

A subagent starts with only the message Claude writes for it, and only its final message comes back ([Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents), checked **15 November 2026**). Everything that matters crosses those two boundaries. This page defines what goes in each direction and what the lead must check itself.

## In: the brief

Use [templates/task-brief.md](../templates/task-brief.md). The short form:

```text
Outcome: [the result required, and who uses it]
Context: [file paths, base commit SHA, error text, decisions already made]
Owner: [one agent, one writable area]
Scope: [what is in and out]
Constraints: [authorized actions, budget, what must not change]
Acceptance: [observable checks that prove it is done]
Return: [use the return contract below]
```

Brief rules:

- **Paste, don't refer.** "The bug we discussed" means nothing to a fresh subagent. Paste the error and the reproduction.
- **Name the base.** For anything that edits code, give the commit SHA the work starts from.
- **Give verifiers the original brief.** A reviewer or auditor gets the requirements and the artifact (diff, document, data), not the implementer's account of it.
- **Restate rules that must reach it.** A subagent with `omitClaudeMd: true` (like this guide's explorer) doesn't see your CLAUDE.md.

## Out: the return contract

Use [templates/return-contract.md](../templates/return-contract.md). It asks for a status, a result, an evidence line per claim, the exact checks run with their output, what was not checked, what changed, and what is left for a person.

Why this shape:

- **Evidence per claim** lets the lead spot-check one line instead of redoing the work.
- **"Not checked"** makes coverage visible. "No issues found" without a list of what was checked is not a result.
- **Copied output, not paraphrase**: a model summarizing a test run can turn "3 skipped" into "all passed". The decisive lines, copied, can be checked.
- **Status** separates finished work from work that ran out of turns.

## What the lead re-verifies itself

A summary is a claim about evidence, not the evidence. Before the lead reports "done" to you, it should re-run or re-read at least:

| The subagent says | The lead checks |
|---|---|
| "Tests pass" | Runs the test command and reads the result |
| "Fixed in file X" | Reads the diff at the cited lines |
| "Committed on branch B" | `git log -1 B` |
| "No other callers" | Runs the search itself, or asks a second explorer with a different query |
| "Source says Y" | Opens the source and finds Y |

### Copy-paste: make the lead verify

```text
For every subagent report: quote its STATUS line, then re-run one command
from its CHECKS RUN and show me the real output next to its claim. If a
report has a claim with no evidence line, list it under "unverified".
Do not tell me the task is done until every acceptance check has output
you produced in this session.
```

**What proves it worked:** the lead's final message shows command output it produced itself, beside each subagent's claim, and lists unverified claims separately.

## Escalation packet

When a subagent is stuck, or you move the task to a stronger model or a person, send: the objective, the evidence so far, approaches already tried, the observed failure, and the one decision needed. Ask for the decision back, not a new plan.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
