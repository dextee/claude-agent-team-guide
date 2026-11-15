[Home](../README.md) · [Setup](../SETUP.md) · [When to delegate](when-to-delegate.md) · [How subagents run](how-subagents-run.md)

# Start here: one task, end to end, in ten minutes

This walks one real change through the whole loop: map, plan, build, prove, then verify it yourself. You need Claude Code **v2.1.321 or later** (Fable 5.2 needs it) and a git repository with tests. Checked against official documentation on **15 November 2026**.

## 1. Install and check (2 minutes)

```bash
claude --version          # 2.1.321 or later; otherwise: claude update
curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh | bash
ls "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/agents"
```

You should see the eight agent files. Installing proves the files are in place, not that your account can run each model. [Full setup and rollback](../SETUP.md).

## 2. Pick a small, real change (1 minute)

Choose something with a test you can run: a bug with a reproduction, or a small feature with a clear acceptance check. Write the check down before you start. If you can't, the task isn't ready to delegate ([when to delegate](when-to-delegate.md)).

## 3. Paste one prompt (5 minutes of agent time)

Start `claude` in the repository and paste:

```text
Task: [change]. Acceptance check: [command or observable behavior].

1. Use the explorer agent to find the files and tests involved. Wait for
   its report.
2. If the approach is not obvious from those files, use the architect agent
   to plan it with acceptance checks, and show me the plan before building.
3. Have the implementer build it and run the tests. Its final message must
   list files changed, the exact commands run, and their real output.
4. Start the reviewer agent fresh. Give it my task, the acceptance check
   and the diff, not the implementer's summary. Findings need file and
   line evidence.
5. Wait for every subagent to report before you summarize. Then re-run the
   acceptance check yourself and show me its output.
```

While it runs, open `/tasks` to see each subagent and the model it runs on.

## 4. Read the handback like an auditor (2 minutes)

- Did each subagent finish, or is any report marked **partial** or failed?
- Does the implementer's report show **command output**, or only a claim that tests passed?
- Did the reviewer get the **diff and your task**, or the implementer's summary?
- Did the lead re-run the acceptance check **itself**, after the reports arrived?

## 5. Verify it yourself

```bash
git diff --stat
[your acceptance check]
```

**What proves it worked:** your own run of the acceptance check passes, the diff touches only the files the explorer found (or the plan named), and the reviewer's findings cite lines in that diff.

## Where to go next

| You want to… | Read |
|---|---|
| Know why the lead had to "wait" | [How subagents run](how-subagents-run.md) |
| Run several workers at once without collisions | [Parallel work and worktrees](parallel-work-and-worktrees.md) |
| Make review independent | [Orchestration patterns: three-stage audit loop](orchestration-patterns.md#pattern-5-three-stage-audit-loop) |
| Stop accepting reports without evidence | [Handoff contracts](handoff-contracts.md), [gates and hooks](gates-and-hooks.md) |
| See what goes wrong | [Failure modes](failure-modes.md) |
| Pick models and effort | [Models and effort](models-and-effort.md), [task selector](task-selector.md) |

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
