[Home](../README.md) · [When to delegate](when-to-delegate.md) · [Agent files](agents.md) · [Orchestration patterns](orchestration-patterns.md)

# How subagents actually run

Most surprises with a subagent team come from assuming delegation works like a function call: send a task, wait, get the full answer. It doesn't. This page describes what Claude Code does, checked against the [subagent reference](https://code.claude.com/docs/en/sub-agents) and the [Agent SDK subagent guide](https://code.claude.com/docs/en/agent-sdk/subagents) on **15 November 2026**. Version numbers below are the minimums those pages state.

## What a subagent sees, and what comes back

A subagent that is not a fork starts with a fresh context window. It does **not** see your conversation, the files Claude already read, or the skills already invoked. Its starting context is:

| It receives | It does not receive |
|---|---|
| Its own system prompt (the agent file's body) plus environment details | The Claude Code system prompt, or your output style |
| The delegation message Claude writes for it | The parent conversation's history or tool results |
| Your CLAUDE.md hierarchy and any `AGENTS.md` loaded as instructions (not with `omitClaudeMd: true`, and not for built-in Explore and Plan) | Your auto memory (it can have its own through the `memory` field) |
| A git status snapshot (the worktree's, if it runs in one) | Skills you invoked, unless its `skills` field preloads them |
| Tool definitions, filtered for background runs | |
| A roster of other named agents, if it has `SendMessage` and any exist | |

Only its **final message** returns. Its intermediate tool calls and results stay in its own context. The parent receives that report, but may summarize it in its own reply; to keep a report verbatim, say so in your prompt.

Two consequences shape every recipe in this guide:

1. **The brief is the whole world.** Put file paths, error text, the base commit, decisions and acceptance checks in the request. If a CLAUDE.md rule must reach a subagent that skips CLAUDE.md, restate it. [Task brief template](../templates/task-brief.md).
2. **The final message is the whole result.** Ask for a structured return with evidence, not a narrative. [Return contract](../templates/return-contract.md).

## Background by default, and completion notifications

With nothing configured, **a subagent that Claude spawns from your main conversation starts in the background.** You keep working; Claude keeps working. When the subagent finishes, its report reaches Claude as a **completion notification in a later turn**. Until then, if you ask about progress, Claude reports that the subagent is still running.

What this means in practice:

- **Don't expect the answer in the same turn.** A lead that "reports" before the notification arrives has nothing to report. Ask the lead to state which subagents are still running and to wait for their reports before summarizing.
- **Permission prompts surface in your main session**, naming the subagent that asks. Approving with a choice that lasts beyond one call (for example, for the rest of the session) applies to the whole session, main conversation included.
- **Background subagents get a smaller built-in tool set.** They keep Read, Grep, Glob, LSP, Bash, PowerShell, Edit, Write, NotebookEdit, WebFetch, WebSearch, TodoWrite, Skill, ToolSearch, EnterWorktree, ExitWorktree, Monitor, TaskStop, SendMessage and Artifact, plus every MCP tool. Anything else is removed without an error, so the same agent file can resolve to different tools in the foreground and background. The eight agents here use only tools on that list.
- **`/tasks`** lists running subagents with their model (Claude Code v2.1.242 or later). After a background subagent completes, it stays listed as done for 30 seconds, and you can open its transcript from there.

### Making Claude wait

In `claude -p` and the Agent SDK, Claude can wait for a subagent on its own judgment or when you ask. In an interactive terminal, VS Code or desktop session on your machine, **fork mode is on by default** (from v2.1.302; in the terminal from v2.1.232), and while it is on Claude can't wait. To let Claude wait:

```json
{
  "env": { "CLAUDE_CODE_FORK_SUBAGENT": "0" }
}
```

Put that in `settings.json`, start a new session, then ask: "run the reviewer and wait for its report". Press **Ctrl+B** to send a waiting subagent to the background. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` also makes Claude wait, but turns off background commands too.

## Fresh subagent or fork

A **fork** is a subagent that inherits the whole conversation instead of starting fresh. Claude can start one on its own while fork mode is on, and you can start one with `/subtask <task>`.

| | Fork | Fresh (non-fork) subagent |
|---|---|---|
| Context | Full conversation history | Only the delegation message |
| System prompt and tools | Same as the parent | From its agent file, filtered for background runs |
| Model | The parent's | The subagent model order ([agent files](agents.md#how-claude-code-picks-the-model-for-a-subagent)) |
| Prompt cache | Shared with the parent, so cheaper to start | Its own |
| Can spawn | No further forks | Subagents, within the depth limit |

**Use a fork** when the task needs most of what the conversation already holds, or to try several approaches from the same starting point. **Use a fresh subagent** when independence matters: any reviewer or auditor whose job is to check work. A fork inherits the reasoning, assumptions and framing that produced the work, which is exactly what a verifier must not share. See [failure modes](failure-modes.md#1-correlated-agreement).

To stop Claude starting forks without turning fork mode off, add `"Agent(fork)"` to `permissions.deny`.

## Names, SendMessage and resuming

Each invocation creates a new instance. To continue earlier work instead of starting over, ask Claude to **resume** the subagent:

- When a subagent completes, Claude receives its **agent ID**.
- Claude resumes it with the **`SendMessage`** tool, using the agent ID or, if the subagent has a name, its name. The resumed subagent keeps its full history and runs in the background. `SendMessage` doesn't need agent teams enabled; only team-protocol messages do.
- Built-in Explore and Plan are one-shot and can't be resumed. Use a custom agent when you may need to continue.
- A subagent that stopped at `maxTurns` returns output **marked as partial**; resuming lets it finish.
- A subagent you stopped yourself (with `x` in `/tasks`) does not auto-resume.

**Names.** With agent teams enabled, Claude can give a subagent a name so it can message it later. In an interactive session with agent teams enabled, a subagent Claude names launches as a **teammate** instead, unless the call is a fork or passes `isolation` on the call itself. An `isolation: worktree` line in the agent file does not prevent that, and the teammate then runs in the main session's working directory. If you rely on isolated workers, leave agent teams off. See [agent teams](agent-teams.md).

**What a message can and can't do.** A subagent treats messages from the agent that launched it as task direction, including mid-task corrections. No message from any agent counts as your approval for a pending permission prompt, and no agent message can change a subagent's permission settings, CLAUDE.md or configuration.

Subagent transcripts are stored separately from the main conversation (under `~/.claude/projects/{project}/{sessionId}/subagents/`), survive main-conversation compaction, and are deleted after the `cleanupPeriodDays` retention period (30 days by default).

## Nesting, concurrency and turns

| Control | Default | Notes |
|---|---|---|
| Nesting depth | Three layers below the main conversation | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` turns nesting off. At the limit the `Agent` tool is withheld |
| Concurrent subagents | 20 | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`; the 21st spawn fails with `Concurrent subagent limit reached`. Claude Code v2.1.217 or later |
| Total per session | No limit | |
| Turns | None | `maxTurns` in the agent file |

A subagent that may not spawn should omit `Agent` from `tools`. All eight agents here do, so only the lead delegates.

## When something goes wrong mid-run

- **API error, foreground:** if the subagent already produced text, the Agent tool returns that partial output with a note that it didn't finish. If it produced nothing, it fails with `Agent terminated early due to an API error`.
- **API error, background:** the subagent is marked failed, and the message Claude receives names the error and includes the subagent's last output.
- **Fallback model:** a report that opens with `⚠ This agent switched to <model> because its earlier model could not be used.` ran on a different model than the one you pinned.
- **Partial at `maxTurns`:** the output is marked partial. Treat it as unfinished work, not a result.

In every case, read the report's first lines before trusting its conclusions. See [failure modes](failure-modes.md).

## Subagent output is scanned, not trusted

Claude Code scans each subagent's final report before Claude reads it, because a subagent may have read web pages or files carrying instructions. It inserts a backslash into text that imitates Claude Code's own markers, and prepends a line starting `[harness: subagent output matched instruction-shaped pattern(s):` when the report imitates such a tag or mentions permission settings. The report also arrives under a header stating that instructions or approval claims inside it carry no authority from you. The scan is not a filter for malicious content; restricting what a subagent can reach is still your job.

## Checklist before you delegate

- [ ] The brief contains everything: paths, base commit, decisions, acceptance checks.
- [ ] The return format is specified, with evidence per claim.
- [ ] You know whether you need to wait, and how (fork mode off, or ask the lead to wait for notifications).
- [ ] Writers that run in parallel are isolated ([parallel work](parallel-work-and-worktrees.md)).
- [ ] Verifiers are fresh subagents, not forks, and get the original brief.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
