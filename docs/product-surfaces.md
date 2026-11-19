[Home](../README.md) · [Setup](../SETUP.md) · [Workflow recipes](workflows.md)

# Which Claude product are you using?

Checked against official documentation: **15 November 2026**. The agent files in this repository are **Claude Code subagents**. They work wherever Claude Code reads `.claude/agents/`. Ordinary Claude chat does not load them.

| Surface | What this guide means there | What to check |
|---|---|---|
| **Claude Code CLI** (terminal) | Full support: install the agents, use `/model`, `/effort`, `/tasks`, plugins | Version v2.1.321 or later: `claude --version` |
| **Claude Code in VS Code** | The extension runs Claude Code in the editor, with the same project files | Agents load from the same folders; confirm with a test delegation |
| **Claude Code in JetBrains IDEs** | The plugin uses the Claude Code CLI, installed separately | CLI version as above |
| **Claude desktop app, Code tab** | Includes Claude Code; no separate CLI install. Requires a paid subscription | Confirm the agents appear by asking Claude to list available subagents |
| **Claude Code on the web** ([claude.ai/code](https://claude.ai/code)) | Cloud sessions run on a repository | Commit agents to the repo's `.claude/agents/`; files in your laptop's `~/.claude` are not on the cloud machine |
| **claude.ai chat** (web, desktop, mobile) | Use the [recipes](workflows.md) as staged prompts. Choose the model and effort from the menu next to the send button | No subagent files. Run stages one after another and review between them |
| **Claude API** | One model per request; set `output_config.effort` | Build your own orchestration or use the Agent SDK |
| **Claude Agent SDK** | Define role agents in code with a model and effort per agent | API credentials and billing; tool permissions |

Sources: [Claude Code overview](https://code.claude.com/docs/en/overview), [subagents](https://code.claude.com/docs/en/sub-agents), [Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents), [change the model, effort and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings). The note about cloud sessions and `~/.claude` is this guide's inference from how cloud sessions work on a repository; check your own setup.

Claude Code says each surface "connects to the same underlying Claude Code engine, so your repo's CLAUDE.md files, settings, and MCP servers work across all of them." Committing project agents to the repository is the most portable choice.

## claude.ai chat: a staged prompt

```text
Help me with [task] in three stages, and stop after each one for my review.
1. Map: list what you need to know and what you can infer from what I gave you.
2. Build: produce [deliverable] using only that material.
3. Prove: check the result against these acceptance criteria: [criteria].
   List anything you could not verify.
```

In chat, these are stages of one conversation, not independent agents. Pick a stronger model or higher effort for the stage that needs it.

## Claude Agent SDK: the same team in code

The SDK accepts the same model aliases and IDs as the agent files, and an `effort` per agent.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Agent"],
    agents={
        "explorer": AgentDefinition(
            description="Fast read-only codebase search.",
            prompt="Find code and return file paths with line numbers. Do not edit.",
            tools=["Read", "Grep", "Glob"],
            model="claude-haiku-5-5",
            effort="medium",
        ),
        "auditor": AgentDefinition(
            description="Evidence-only review before merge.",
            prompt="Review the change. Every finding must cite a file and line.",
            tools=["Read", "Grep", "Glob", "Bash"],
            model="claude-fable-5-2",
            effort="high",
        ),
    },
)
```

Pass `options` to `query()` with your prompt. The role's `tools` list restricts that agent; the parent's `allowed_tools` list names tools approved without prompting, **not** the only tools the parent can use. [AgentDefinition](https://code.claude.com/docs/en/agent-sdk/subagents) · [Python options](https://code.claude.com/docs/en/agent-sdk/python). Python package `claude-agent-sdk`; TypeScript `@anthropic-ai/claude-agent-sdk`.

Fable requests from SDK apps that do not show the consent prompt can bill usage credits on plans where Fable uses them ([model configuration](https://code.claude.com/docs/en/model-config#fable-and-usage-credits)). `max_budget_usd` is a **per-query stop threshold**, not a hard spending ceiling. Claude Code checks after a model response arrives. That response and work already in flight from parallel subagents can push the total past the threshold. Leave headroom. [SDK budget behavior](https://code.claude.com/docs/en/agent-sdk/agent-loop#budget-headroom)

In the SDK, as in the CLI, only a subagent's final message returns to the parent, and the parent may summarize it. To pass a subagent's report through verbatim, say so in the prompt you give the main `query()` call ([Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents)).

## Third-party providers

How the Claude Code aliases resolve, and where the advisor and fast mode work in Claude Code:

| | Anthropic API | Claude Platform on AWS | Claude Models on Google Cloud (Anthropic managed) | Amazon Bedrock, Google Cloud's Agent Platform | Microsoft Foundry |
|---|---|---|---|---|---|
| `opus` alias resolves to | Opus 5.5 | Opus 5.5 | Opus 5.5 | Opus 5.5 | Opus 4.6 |
| `sonnet` alias resolves to | Sonnet 5.5 | Sonnet 4.6 | Sonnet 5.5 | Sonnet 4.5 | Sonnet 4.5 |
| `haiku` alias resolves to | Haiku 5.5 | Haiku 4.5 | Haiku 4.5 | Haiku 4.5 | Haiku 4.5 |
| Advisor (experimental) | Yes | Yes, from v2.1.300 | Yes, from v2.1.300 | No | No |
| Fast mode in Claude Code | Yes (Console, or usage credits on subscription plans) | No | Not stated on the fast mode page | Bedrock: no. Agent Platform: Fable 5.2 only, with conditions, from v2.1.322 | No |

The `fable` alias resolves to Fable 5.2 everywhere except Claude apps gateway sessions. Sources: [model configuration](https://code.claude.com/docs/en/model-config#model-aliases), [advisor](https://code.claude.com/docs/en/advisor), [fast mode](https://code.claude.com/docs/en/fast-mode). On the Claude API side (not Claude Code), the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) lists further fast-mode platforms, such as Claude Models on Google Cloud (Anthropic managed) for Opus 5.5 and Fable 5.2.

This is why the agent files pin full model IDs instead of aliases: an alias can mean an older model on another provider. A pinned ID makes the intended version explicit, so check that each one is enabled in your account. Anthropic recommends pinning model versions with `ANTHROPIC_DEFAULT_OPUS_MODEL` and related variables before rolling out on third-party providers.

## CI and chat integrations

- **GitHub Actions:** run `/install-github-app` inside Claude Code to set up the [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action). Quick setup works with the Claude API and Claude subscriptions; Bedrock, Google Cloud's Agent Platform and Foundry use a separate cloud-provider setup. Either path needs admin access to the repository ([GitHub Actions](https://code.claude.com/docs/en/github-actions)).
- **Non-interactive runs:** `claude -p "..."` runs one prompt and exits. Fable billing consent is not requested in this mode.
- **Slack:** Claude Code can take tasks from Slack mentions ([overview](https://code.claude.com/docs/en/overview)).

Check that the CI runner actually discovers the project agents before relying on a named delegation.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
