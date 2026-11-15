[Home](../README.md) · [Handoff contracts](handoff-contracts.md) · [Failure modes](failure-modes.md)

# Gates and hooks

An instruction in a prompt is a request. A hook is a mechanism: Claude Code runs it, and on the events that support blocking, an exit code of 2 stops the action. This page covers the hooks that matter for a subagent team, and how to make sure a gate can actually fail. Checked against the [hooks reference](https://code.claude.com/docs/en/hooks), the [subagent reference](https://code.claude.com/docs/en/sub-agents#define-hooks-for-subagents) and [agent teams](https://code.claude.com/docs/en/agent-teams) on **15 November 2026**.

## The events a team uses

| Event | Fires | Can it block? | Use it to |
|---|---|---|---|
| `PreToolUse` | Before any tool call, in the main conversation and in subagents | Yes: exit 2 blocks the call | Stop writes from a read-only role; block dangerous commands |
| `SubagentStart` | When a subagent is spawned or resumed | No, but it can add context with `additionalContext` | Inject a standing rule into every subagent of one type |
| `SubagentStop` | When a subagent finishes responding | Yes: exit 2 (or `decision: "block"` with a `reason`) keeps it running and delivers the message as its next instruction | Refuse to accept a report that lacks evidence |
| `PostToolUse` on the `Agent` tool | After a subagent returns | No | Add context to the parent after a result arrives |
| `TaskCreated` / `TaskCompleted` | When a task is created or marked complete (agent teams and Task tools) | Yes | Require passing tests before a task can close |
| `TeammateIdle` | When an agent-team teammate is about to go idle | Yes: keeps it working | Push a teammate to finish its checklist |

`SubagentStart` and `SubagentStop` matchers take the agent's `name`, or the plugin-scoped name such as `agent-team:worker` for plugin agents. A scoped name contains `:`, so it is treated as a regular expression; anchor it as `^agent-team:worker$`.

## Example: refuse reports without evidence

[templates/hooks/subagent-stop-gate.sh](../templates/hooks/subagent-stop-gate.sh) reads the `last_assistant_message` field that `SubagentStop` receives and exits 2 unless the report has a `STATUS:` line and a `CHECKS RUN:` section from the [return contract](../templates/return-contract.md). It honors `stop_hook_active`, which is `true` when the subagent is already continuing because of a stop hook, so it can't loop forever. It needs `jq`.

Install it for one project:

```bash
mkdir -p .claude/hooks
cp templates/hooks/subagent-stop-gate.sh .claude/hooks/
chmod +x .claude/hooks/subagent-stop-gate.sh
```

Then add to `.claude/settings.json`:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "^(implementer|worker)$",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/subagent-stop-gate.sh" }
        ]
      }
    ]
  }
}
```

With the plugin install, match `^agent-team:(implementer|worker)$` instead.

**Limit:** on Claude Code v2.1.271 or later, a subagent that reports through the `SubagentHandback` tool delivers its report as that tool call's `message`, and `last_assistant_message` then holds only its closing text. If your subagents report that way, check the report with a `PreToolUse` hook matched on `SubagentHandback`, which receives it as `tool_input.message`.

### Prove the gate can fail

Before trusting it, run it both ways:

```bash
G=.claude/hooks/subagent-stop-gate.sh
echo '{"stop_hook_active":false,"last_assistant_message":"All done, tests pass."}' | $G; echo "exit=$?"
printf '%s' '{"stop_hook_active":false,"last_assistant_message":"STATUS: done\nCHECKS RUN:\n- npm test -> 0 -> 12 passed"}' | $G; echo "exit=$?"
```

**What proves it worked:** the first prints the missing items and `exit=2`; the second prints `exit=0`. If both print `exit=0`, the gate can't fail and is not a gate. This repository's tests run exactly these two cases.

## Hooks inside an agent file

An agent file can carry its own `hooks:` block. They run only while that subagent is active, and a `Stop` hook there becomes `SubagentStop`. Three limits:

- **Project agents need workspace trust.** Frontmatter hooks in `.claude/agents/` run only after you accept the trust dialog for that folder. A `-p` session doesn't count as trusted. User agents in `~/.claude/agents/` and `--agents` definitions don't need this step.
- **Plugin agents ignore `hooks`** (and `mcpServers` and `permissionMode`).
- **The hook command must exist on every machine that runs the agent.**

For those reasons the eight agents here ship without hooks. Put team gates in `settings.json`, where they apply to every subagent and are visible in one place.

## Permission modes are gates too

A subagent's `permissionMode` can make it stricter, for example `plan` for read-only work. But the main conversation's mode can override it: when the lead runs in `bypassPermissions`, `acceptEdits` or auto mode, the subagent runs in that same mode and its own `permissionMode` is ignored. Don't rely on a subagent's `permissionMode` to restrain it while the lead runs permissively. A `PreToolUse` hook or a `permissions.deny` rule in settings applies regardless.

## A gate that cannot fail is not a gate

Every check, hook or script that says "pass" must be shown failing once on input that should fail. This repository applies that to itself: each check in `scripts/validate.py` has a test in `scripts/test_validate.py` that feeds it a broken input and expects an error. When you add a gate:

1. Break the thing it guards (delete the evidence line, change the version, add a typo'd field).
2. Run the gate and confirm it fails with a message that names the problem.
3. Restore, and confirm it passes.
4. Keep the broken case as a test.

See [failure modes](failure-modes.md#4-gates-that-cannot-fail) for the ways gates pass while checking nothing.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
