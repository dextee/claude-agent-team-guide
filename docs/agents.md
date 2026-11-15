[Home](../README.md) · [Setup](../SETUP.md) · [How subagents run](how-subagents-run.md) · [Models and effort](models-and-effort.md)

# Agent files: the eight roles and every frontmatter field

Each file in [`agents/`](../agents) is a standard Claude Code subagent: YAML frontmatter, then a Markdown body that becomes the subagent's system prompt. The subagent receives that prompt plus basic environment details, not the Claude Code system prompt. Every field below is from the official [subagent reference](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields), checked 15 November 2026.

## Roster and reasoning

| Agent | Model / effort | Tools | Why this pairing |
|---|---|---|---|
| [architect](../agents/architect.md) | Fable 5.2 / high | Read, Glob, Grep, WebFetch, WebSearch | Planning mistakes are the most expensive to fix later. Anthropic positions Fable for "demanding reasoning and long-horizon agentic work." Read-only by design. `high` is the API default; Claude Code's own default for Fable 5.2 is `medium` |
| [implementer](../agents/implementer.md) | Opus 5.5 / medium | Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch | Anthropic's recommended starting model, described as "for long-running agentic coding and knowledge work." `medium` is its default. Works in your checkout, for sequential work |
| [worker](../agents/worker.md) | Sonnet 5.5 / medium | Read, Edit, Write, Glob, Grep, Bash | A scoped chunk with a clear check does not need Opus. Half the Opus price per token. Runs in its own git worktree (`isolation: worktree`) with `maxTurns: 40`, so parallel workers cannot overwrite each other |
| [explorer](../agents/explorer.md) | Haiku 5.5 / medium | Read, Glob, Grep | Search is high-volume and easy to verify. Anthropic lists subagent tasks among Haiku 5.5's uses. No Bash keeps it strictly read-only. `omitClaudeMd: true`, like the built-in Explore agent, keeps each search cheap |
| [reviewer](../agents/reviewer.md) | Sonnet 5.5 / high | Read, Glob, Grep, Bash | Routine review needs care more than raw capability. `high` gives it room to check edge cases |
| [auditor](../agents/auditor.md) | Fable 5.2 / high | Read, Glob, Grep, Bash | Reserved for consequential changes, where a missed defect costs more than the extra tokens. Told never to rely on the implementer's own account |
| [researcher](../agents/researcher.md) | Sonnet 5.5 / high | Read, Glob, Grep, WebFetch, WebSearch | Source gathering is breadth work; `high` helps it reconcile conflicting claims |
| [editor](../agents/editor.md) | Sonnet 5.5 / medium | Read, Edit, Write, Glob, Grep | Clear writing from settled facts. No Bash and no web, so it can't add new claims from outside |

These are this guide's recommendations, not Anthropic benchmarks. `maxTurns: 40` on the worker is this guide's starting cap, not an Anthropic number: raise it if workers often return partial results. Quoted positioning comes from the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model).

None of the eight lists the `Agent` tool. Omitting `Agent` from `tools` means the agent can't spawn subagents of its own, which keeps the team one level deep and the lead in charge of every handoff.

## Frontmatter reference

Only `name` and `description` are required. Field names are camelCase and must match exactly: **Claude Code ignores a field it doesn't recognize, without an error.** `python3 scripts/validate.py` rejects unknown fields in this repository's agents for that reason.

| Field | What it does | Notes from the reference | Used here |
|---|---|---|---|
| `name` | The identifier you and Claude use | Required. At most 256 characters. Can't start with `-` or contain `:`, which is reserved for plugin-scoped names. Hooks receive it as `agent_type` | All |
| `description` | When Claude should delegate to it | Required. Loaded into every session; a startup warning appears when your custom subagents' descriptions together pass 15,000 tokens. "Use proactively" encourages automatic delegation | All |
| `tools` | Allowlist of tools | Omit to inherit every tool available to subagents. Omitting `Agent` from the list stops the agent spawning subagents | All |
| `disallowedTools` | Denylist | Applied before `tools`. An entry like `Bash(git push *)` still removes the whole tool; block single commands with a `permissions.deny` rule instead | — |
| `model` | Which model runs it | `fable`, `opus`, `sonnet`, `haiku`, a full ID such as `claude-opus-5-5`, or `inherit` (the main conversation's model, or the spawning subagent's model for a nested subagent) | All |
| `effort` | Effort while it runs | `low` to `max`, depending on the model. Overrides the session level, not `CLAUDE_CODE_EFFORT_LEVEL` | All |
| `permissionMode` | Its permission mode | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` (`manual` = `default`). The main conversation's mode can override it: under `bypassPermissions`, `acceptEdits` or auto mode the subagent runs in that mode. Ignored for plugin subagents | — |
| `maxTurns` | Cap on agentic turns | At the cap, output returns marked as partial (Claude Code v2.1.246 or later) and Claude can resume the subagent | worker |
| `isolation` | `worktree` runs it in a temporary git worktree | Branches from your default branch, not your current `HEAD`, unless `worktree.baseRef` is `"head"`. Removed automatically if the subagent changes nothing. See [parallel work](parallel-work-and-worktrees.md) | worker |
| `background` | `true` keeps it in the background even when Claude asks to wait | Subagents Claude spawns from the main conversation already start in the background | — |
| `omitClaudeMd` | Start without user, project and local CLAUDE.md | Managed policy files still load. Use when the delegation prompt carries everything. Claude Code v2.1.271 or later | explorer |
| `memory` | Persistent memory directory: `user`, `project` or `local` | Turns on Read, Write and Edit so it can manage its memory files, which would break a read-only role. Has no effect when auto memory is off | — |
| `skills` | Skills to preload | Injects full skill content at startup. The subagent can still invoke unlisted skills unless `Skill` is withheld | — |
| `mcpServers` | MCP servers for this subagent only | A name reference or an inline definition. Inline servers from project agent files need folder trust. Ignored for plugin subagents | — |
| `hooks` | Hooks while it runs | A `Stop` hook here becomes `SubagentStop`. Project agent files need workspace trust; a `-p` session doesn't count. Ignored for plugin subagents. See [gates and hooks](gates-and-hooks.md) | — |
| `autoCompactWindow` | Compact earlier | A plain integer from `100000` to `1000000` (`200k` reads as 200). Claude Code v2.1.296 or later | — |
| `color` | Colour in the task list and transcript | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` | All |
| `initialPrompt` | First user turn when the agent runs as the whole session (`--agent`) | Ignored for plugin subagents | — |
| `experimental` | Map of experimental options | `cacheTtl: 5m` or `1h` sets this subagent's prompt-cache lifetime. Claude Code v2.1.248 or later | — |

To find a misspelled field in a subagent that loaded, run `claude --debug` and search the debug log for `does not recognize or apply` (Claude Code v2.1.296 or later). A file with no `name`, a bad `name`, a `name` without `description`, or YAML that doesn't parse is skipped without a message in the session.

### Plugin installs drop three fields

When these agents load from the plugin (`agent-team:worker` and so on), Claude Code ignores `hooks`, `mcpServers` and `permissionMode`. The eight agents use none of them, so the plugin and file installs behave the same. If you add those fields, install with `install.sh` instead.

## Where agent files live

When two files share a `name`, the higher-priority location wins:

| Priority | Location | Scope |
|---|---|---|
| 1 | Managed settings | Organization |
| 2 | `claude --agents '<json>'` | Current session only |
| 3 | `.claude/agents/` | Current project; commit it to share |
| 4 | `~/.claude/agents/` | All your projects |
| 5 | A plugin's `agents/` folder | Where the plugin is enabled; names are prefixed, such as `agent-team:auditor` |

Claude Code scans `.claude/agents/` and `~/.claude/agents/` recursively and picks up edits within a few seconds. Restart the session when you created the first agent in a new `agents` folder during the session, or after editing agents in a folder added with `--add-dir`.

## How Claude Code picks the model for a subagent

First match wins ([subagent reference](https://code.claude.com/docs/en/sub-agents#choose-a-model)):

1. A `model` Claude passes when it spawns the agent. On an Agent tool call this is an alias, not a full ID.
2. The agent file's `model` field (`inherit` means the main conversation's model, or the spawning subagent's model for a nested subagent).
3. `CLAUDE_CODE_SUBAGENT_MODEL`.
4. The main conversation's model, or the spawning subagent's model for a nested subagent.

`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes `CLAUDE_CODE_SUBAGENT_MODEL` win over every agent file and spawn parameter (forks still run on the parent's model). Run `/tasks` to see the model actually in use.

## Permissions are prompts, not a sandbox

The reviewer and auditor have Bash so they can run tests. Bash can also write files. Their instructions forbid edits, but that is a behavioral instruction. For hard limits, use Claude Code [permission rules](https://code.claude.com/docs/en/settings), a `PreToolUse` hook ([gates and hooks](gates-and-hooks.md)), or run the review in a separate checkout. The architect, explorer and researcher have no Bash, Edit or Write tools at all.

## Write your own

Copy [templates/agent-template.md](../templates/agent-template.md). Give it one job, a description that says when to use it, the cheapest model that does that job well, and only the tools it needs. End the body with the [return contract](../templates/return-contract.md) it must follow, since its final message is the only thing the caller receives. Run `python3 scripts/validate.py` before committing.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
