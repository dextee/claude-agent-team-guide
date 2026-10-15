[Home](../README.md) · [Setup](../SETUP.md) · [Models and effort](models-and-effort.md)

# The eight agents

Each file in [`agents/`](../agents) is a standard Claude Code subagent: YAML frontmatter followed by a system prompt. The frontmatter fields used here are all documented in the [subagent reference](https://code.claude.com/docs/en/sub-agents), checked 15 October 2026.

| Field | Used for | Notes from the official reference |
|---|---|---|
| `name` | The name you call, such as `explorer` | Required. Can't contain `:`, which is reserved for plugin-scoped names |
| `description` | When Claude should delegate to it | Required. Loaded into every session, so keep it short |
| `model` | Pinned model ID | Accepts `fable`, `opus`, `sonnet`, `haiku`, a full model ID, or `inherit` |
| `effort` | Pinned effort level | `low` to `max`. Overrides the session level, but not `CLAUDE_CODE_EFFORT_LEVEL` |
| `tools` | Allowed tools | Omit to inherit all tools. A list also excludes the `Agent` tool, so the agent can't spawn subagents |
| `color` | Display color in the task list | Cosmetic |

## Roster and reasoning

| Agent | Model / effort | Tools | Why this pairing |
|---|---|---|---|
| [architect](../agents/architect.md) | Fable 5.1 / high | Read, Glob, Grep, WebFetch, WebSearch | Planning mistakes are the most expensive to fix later. Anthropic positions Fable for "demanding reasoning and long-horizon agentic work." Read-only by design |
| [implementer](../agents/implementer.md) | Opus 5.5 / medium | Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch | Anthropic's recommended starting model, described as "for long-running agentic coding and knowledge work." `medium` is its default |
| [worker](../agents/worker.md) | Sonnet 5.5 / medium | Read, Edit, Write, Glob, Grep, Bash | A scoped chunk with a clear check does not need Opus. Half the Opus price per token |
| [explorer](../agents/explorer.md) | Haiku 5.5 / medium | Read, Glob, Grep | Search is high-volume and easy to verify. Anthropic lists sub-agent tasks among Haiku 5.5's uses. No Bash keeps it strictly read-only |
| [reviewer](../agents/reviewer.md) | Sonnet 5.5 / high | Read, Glob, Grep, Bash | Routine review needs care more than raw capability. `high` gives it room to check edge cases |
| [auditor](../agents/auditor.md) | Fable 5.1 / high | Read, Glob, Grep, Bash | Reserved for consequential changes, where a missed defect costs more than the extra tokens |
| [researcher](../agents/researcher.md) | Sonnet 5.5 / high | Read, Glob, Grep, WebFetch, WebSearch | Source gathering is breadth work; `high` helps it reconcile conflicting claims |
| [editor](../agents/editor.md) | Sonnet 5.5 / medium | Read, Edit, Write, Glob, Grep | Clear writing from settled facts. No Bash and no web, so it can't add new claims from outside |

These are this guide's recommendations, not Anthropic benchmarks. Quoted positioning comes from the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model).

## How Claude Code picks the model for a subagent

From the [subagent reference](https://code.claude.com/docs/en/sub-agents), first match wins:

1. A `model` Claude passes when it spawns the agent.
2. The agent file's `model` field (`inherit` uses the main conversation's model).
3. `CLAUDE_CODE_SUBAGENT_MODEL`.
4. The main conversation's model.

`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes the environment variable win over everything. Run `/tasks` to see the model actually in use.

## Permissions are prompts, not a sandbox

The reviewer and auditor have Bash so they can run tests. Bash can also write files. Their instructions forbid edits, but that is a behavioral instruction. For hard limits, use Claude Code [permission settings](https://code.claude.com/docs/en/settings) or run the review in a separate checkout. The architect, explorer and researcher have no Bash, Edit or Write tools at all.

## Use them as teammates

With experimental agent teams enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), you can spawn a teammate from one of these definitions, for example "Spawn a teammate using the auditor agent type to review the auth module." The definition's `tools` and `model` apply ([agent teams](https://code.claude.com/docs/en/agent-teams)). Enabling teams also changes ordinary delegation: a subagent Claude names launches as a teammate.

## Write your own

Copy [templates/agent-template.md](../templates/agent-template.md). Give it one job, a description that says when to use it, the cheapest model that does that job well, and only the tools it needs. End the body by reminding it that its final message is the only thing the caller receives. Run `python3 scripts/validate.py` before committing.
