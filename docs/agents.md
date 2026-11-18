[Home](../README.md) · [Setup](../SETUP.md) · [Models and effort](models-and-effort.md)

# The eight agents

Each file in [`agents/`](../agents) defines a subagent for one Claude Code session: YAML frontmatter configures the role, and the Markdown body supplies its instructions. The lead delegates and receives the result. No experimental Agent Teams setting is needed. [Subagent reference](https://code.claude.com/docs/en/sub-agents) · [Source checks, 18 November 2026](../SOURCES.md#18-november-2026-source-checks)

| Field | Used for | Notes from the official reference |
|---|---|---|
| `name` | The name you call, such as `explorer` | Required. Can't contain `:`, which is reserved for plugin-scoped names |
| `description` | When Claude should delegate to it | Required. Loaded into every session, so keep it short |
| `model` | Pinned model ID | Accepts `fable`, `opus`, `sonnet`, `haiku`, a full model ID, or `inherit` |
| `effort` | Role's default effort | A per-invocation level can override this field; `CLAUDE_CODE_EFFORT_LEVEL` takes precedence over both. See [effort settings](models-and-effort.md#where-to-set-it) |
| `tools` | Tool allowlist | Omit to inherit tools available to the subagent. All eight lists here omit `Agent`, so none of these roles can delegate through that tool. A custom list can include `Agent` to allow nesting within the depth limit |
| `color` | Display color in the task list | Cosmetic |

## Roster and reasoning

| Agent | Model / effort | Tools | Why this pairing |
|---|---|---|---|
| [architect](../agents/architect.md) | Fable 5.1 / high | Read, Glob, Grep, WebFetch, WebSearch | This edition keeps the explicit 5.1 pin for plans with competing constraints. It can inspect code and sources without editing the project |
| [implementer](../agents/implementer.md) | Opus 5.5 / medium | Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch | Anthropic's recommended starting model, described as "for long-running agentic coding and knowledge work." `medium` is its default |
| [worker](../agents/worker.md) | Sonnet 5.5 / medium | Read, Edit, Write, Glob, Grep, Bash | A scoped chunk with a clear check does not need Opus. Half the Opus price per token |
| [explorer](../agents/explorer.md) | Haiku 5.5 / medium | Read, Glob, Grep | Search is high-volume and easy to verify. Anthropic lists sub-agent tasks among Haiku 5.5's uses. No Bash keeps it strictly read-only |
| [reviewer](../agents/reviewer.md) | Sonnet 5.5 / high | Read, Glob, Grep, Bash | Routine review needs care more than raw capability. `high` gives it room to check edge cases |
| [auditor](../agents/auditor.md) | Fable 5.1 / high | Read, Glob, Grep, Bash | Reserved for consequential changes, where a missed defect costs more than the extra tokens |
| [researcher](../agents/researcher.md) | Sonnet 5.5 / high | Read, Glob, Grep, WebFetch, WebSearch | Source gathering is breadth work; `high` helps it reconcile conflicting claims |
| [editor](../agents/editor.md) | Sonnet 5.5 / medium | Read, Edit, Write, Glob, Grep | Writes from supplied evidence; no shell or web lookup. The lead still checks that every claim traces to a source |

These are this guide's recommendations, not Anthropic benchmarks. Quoted positioning comes from the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model).

## How Claude Code picks the model for a subagent

For an ordinary delegation, the [subagent reference](https://code.claude.com/docs/en/sub-agents#choose-a-model) gives this order:

1. A model alias Claude passes when it spawns the agent.
2. The agent file's `model` field (`inherit` uses the spawning conversation's model).
3. `CLAUDE_CODE_SUBAGENT_MODEL`.
4. The spawning conversation's model.

For these eight roles, setting `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` with `CLAUDE_CODE_SUBAGENT_MODEL` bypasses the first two choices. An organization allowlist can also cause a model substitution. Run `/tasks` while the agent works to see the actual model and configured effort.

## What “read-only” means here

The reviewer and auditor have Bash so they can run tests. They are **instructed not to edit**; Bash can still write, and a test can create files. A separate checkout keeps ordinary test artifacts out of your working copy, but does not make shell commands read-only. For a review limited to file reads, give the role only `Read, Glob, Grep` and have the lead supply the diff and test output. [Tool restrictions](https://code.claude.com/docs/en/sub-agents#restrict-which-tools-a-subagent-can-use)

## Use them as teammates

Use experimental [agent teams](https://code.claude.com/docs/en/agent-teams#compare-with-subagents) when separate sessions need to coordinate directly. Teams are off by default. If you enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in an interactive session, try “Spawn a teammate using the auditor agent type.” Enabling teams can also turn ordinary named delegations into teammates. A role's frontmatter does not transfer wholesale: for example, an in-process teammate uses its `effort` field and gets messaging tools; don't assume a split-pane teammate inherits that effort. See [which fields apply](https://code.claude.com/docs/en/agent-teams#use-subagent-definitions-for-teammates).

## Write your own

Copy [the role template](../templates/agent-template.md) into your own project's `.claude/agents/`. Give it one job, a description that says when to use it, and only the tools it needs. Make its final answer useful on its own: ask for the result, evidence and unresolved questions. To try that specific role, type `@` in Claude Code and select its agent entry. A plain-language request leaves the decision to delegate to Claude. [Explicit invocation](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly)
