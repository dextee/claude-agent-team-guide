[Home](../README.md) · [Parallel work](parallel-work-and-worktrees.md) · [Cost and limits](cost-and-evaluation.md)

# Agent teams (experimental) versus subagents

Agent teams are a separate, heavier feature. A lead session spawns **teammates**: full Claude Code instances that share a task list and message each other directly. Subagents, the main subject of this guide, report back to one session. Checked against [agent teams](https://code.claude.com/docs/en/agent-teams) and [costs](https://code.claude.com/docs/en/costs) on **15 November 2026**. Agent teams are **experimental and disabled by default**; behavior may change.

## Compare

| | Subagents | Agent teams |
|---|---|---|
| Context | Own context window; results return to the caller | Own context window; fully independent |
| Communication | Return a result to the caller; named subagents can also message each other | Teammates message each other directly |
| Coordination | The main agent manages all work | Messages plus a shared task list |
| Best for | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| Token cost | Lower: results summarized back to main context | Higher: each teammate is a separate Claude instance |

(From Anthropic's comparison table.) Anthropic's guidance: use subagents for quick, focused workers that report back; use agent teams when teammates need to share findings, challenge each other and coordinate on their own. For sequential tasks, same-file edits or work with many dependencies, a single session or subagents are more effective.

## Turn it on, and know what changes

```json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
}
```

Enabling teams **changes ordinary delegation**. Claude may name a subagent on its own, and while teams are enabled a subagent Claude names launches as a teammate, so a team can form when you didn't ask for one. A teammate launched this way ignores the agent file's `isolation: worktree` and runs in the main working directory. To get plain subagents back, set the variable to `0` in `settings.json`; the running session picks up the change when you save. Teams need an interactive session: with `-p` and in the Agent SDK, named subagents stay ordinary subagents.

## Using this guide's agents as teammates

You can name one of the eight agents as a teammate type:

```text
Spawn a teammate using the auditor agent type to review the auth module.
```

Claude Code applies the definition's `tools` and `model` in either display mode. For an in-process teammate it also applies `disallowedTools`, `effort` and `autoCompactWindow`, and appends the body to the teammate's default system prompt. It does **not** apply `skills`. The model order for a teammate is: a model named in your spawn prompt, then the definition's `model`, then `CLAUDE_CODE_SUBAGENT_MODEL` (unless set to `inherit`), then the lead's model.

## Gates for teams

Three hooks are made for teams, and each blocks with exit code 2 ([gates and hooks](gates-and-hooks.md)):

- `TeammateIdle`: keeps a teammate working instead of going idle.
- `TaskCreated`: rejects a task, for example one without a ticket number.
- `TaskCompleted`: refuses to mark a task complete, for example until tests pass.

## Limits to plan around

From Anthropic's list of current limitations:

- `/resume` and `/rewind` don't restore in-process teammates.
- Task status can lag, blocking dependent tasks.
- One team per session; teammates can't spawn their own teammates; the lead is fixed for the session's life.
- No per-teammate permission modes at spawn: teammates start in the lead's mode, including `bypassPermissions`.
- An in-process teammate's own subagents run in the foreground.

## Cost

Each teammate has its own context window, and usage scales with the number of active teammates. Anthropic's cost guide says teams use approximately 7× more tokens than standard sessions when teammates run in plan mode, and recommends Sonnet for teammates, small teams, focused spawn prompts, and shutting teammates down when their work is done. The agent-teams page suggests starting with 3 to 5 teammates. An in-process teammate's cache lasts five minutes by default; `subagentPromptCacheTtl: "1h"` extends it at a higher cache-write rate.

## Copy-paste: a review team

```text
Spawn three teammates to review [PR or branch], each with one lens:
security, performance, and test coverage. Give each the PR description and
the diff, not my summary. Each must report findings with file and line
evidence. Wait for all three to finish, then merge their findings into one
list, dropping duplicates and keeping the strongest evidence for each.
```

**What proves it worked:** three teammates appear in the agent panel, each finding in the merged list cites a file and line, and findings that only one teammate raised are still in the list.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
