# Source register

[Home](README.md) · [Validation](VALIDATION.md)

The original source review is dated **15 October 2026**. The November register below covers only the claims named in each row. Model-to-role assignments, team sizes and workflow prompts are the author's recommendations, not benchmark results.

## 18 November 2026 source checks

| Official source | Claim rechecked on 2026-11-18 |
|---|---|
| [Create plugins: load a directory for one session](https://code.claude.com/docs/en/plugins/create#load-a-directory-or-archive-for-one-session) · [CLI reference](https://code.claude.com/docs/en/cli-reference#cli-flags) | From this repository root, `claude --plugin-dir .` points at the local plugin directory. It loads the plugin for that session without a marketplace install. The flag alone does not prove that an agent ran. |
| [Invoke subagents explicitly](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly) · [Check a subagent's model](https://code.claude.com/docs/en/sub-agents#check-a-subagents-model) | Prose leaves delegation to Claude; an `@` agent mention requests the role explicitly. The manual forms are `@agent-explorer` for a local role and `@agent-agent-team:explorer` for this plugin. A named delegation row and `/tasks` identify the worker and its running model. |
| [What loads at startup](https://code.claude.com/docs/en/sub-agents#what-loads-at-startup) · [Restrict tools](https://code.claude.com/docs/en/sub-agents#restrict-which-tools-a-subagent-can-use) · [Nested subagents](https://code.claude.com/docs/en/sub-agents#let-subagents-spawn-their-own-subagents) | An ordinary custom subagent starts with its role, delegation message, applicable project instructions and normally a Git-status snapshot, not the lead's conversation history. A fork inherits the conversation. An explicit `tools` list is an allowlist; omitting `Agent` from that list prevents delegation through it. |
| [Compare teams with subagents](https://code.claude.com/docs/en/agent-teams#compare-with-subagents) · [Use subagent definitions for teammates](https://code.claude.com/docs/en/agent-teams#use-subagent-definitions-for-teammates) | Subagents work within one session. Experimental Agent Teams are disabled by default; enabling them can turn an ordinary named delegation into a teammate in interactive sessions. Teammates can communicate directly; which frontmatter applies depends on display mode. |
| [Choose a subagent model](https://code.claude.com/docs/en/sub-agents#choose-a-model) · [Choose subagent effort](https://code.claude.com/docs/en/sub-agents#choose-an-effort-level) · [Organization effort limits](https://code.claude.com/docs/en/model-config#organization-effort-limits) | A full model ID in frontmatter is a request, subject to invocation, force settings and organization restrictions. For non-fork subagents, an explicit environment effort level overrides invocation effort, which overrides frontmatter. Per-invocation effort is supported from v2.1.292; organization caps still apply. |
| [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) · [Model status](https://platform.claude.com/docs/en/about-claude/model-deprecations) · [Claude Code model configuration](https://code.claude.com/docs/en/model-config) | Fable 5.1 remains active. The current overview recommends 5.2 for demanding work beyond Opus 5.5. On current Claude Code the default `fable` alias resolves to 5.2 except on Claude apps gateway; 5.2 requires at least v2.1.321 and defaults to `medium`. The guide's 5.1 / `high` roles still use exact IDs. |
| [SDK budget headroom](https://code.claude.com/docs/en/agent-sdk/agent-loop#budget-headroom) · [SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking) · [Python SDK options](https://code.claude.com/docs/en/agent-sdk/python) | `max_budget_usd` / `maxBudgetUsd` is a per-query stop threshold checked after a response. That response and unfinished subagent requests can overshoot it. The Python parent's `allowed_tools` pre-approves tools; it does not restrict the parent to that list. |
| [Worktree base selection](https://code.claude.com/docs/en/worktrees#choose-the-base-branch) | New subagent worktrees use the repository's default branch by default; `worktree.baseRef: "head"` selects the current local commit. |
| [Provider alias mappings](https://code.claude.com/docs/en/model-config#model-aliases) · [Advisor availability](https://code.claude.com/docs/en/advisor) · [Fast-mode requirements](https://code.claude.com/docs/en/fast-mode#requirements) | Claude Models on Google Cloud (Anthropic managed) and Google's Agent Platform have different Sonnet aliases. Advisor support includes Claude Platform on AWS and Anthropic-managed Google Cloud from v2.1.300; Google's Agent Platform has conditional fast-mode support. |

## Models and pricing

| Source | Checked on | Used to establish |
|---|---|---|
| [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | 2026-10-15 | The four models selected for this edition, their API IDs, descriptions, latency, context (1M), max output (128K), thinking mode, default API effort, Bedrock / Google Cloud / Foundry IDs, and Anthropic's then-current "start with Opus 5.5" recommendation |
| [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | 2026-10-15 | Input, output and cache-read rates; Haiku 5.5's 100K-token price threshold; batch discount; Opus 5.5 fast-mode rates; tokenizer note; Sonnet 5 and Haiku 4.5 rates for the changelog |
| [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) | 2026-10-15 | Selection matrix, efficiency-first and capability-first approaches, "tuning effort is often a better lever than switching models" |
| [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) | 2026-10-15 | Effort levels and typical uses, per-model defaults and recommendations, `output_config.effort` |

## Claude Code

| Source | Checked on | Used to establish |
|---|---|---|
| [Claude Code overview](https://code.claude.com/docs/en/overview) | 2026-10-15 | Surfaces (terminal, VS Code, JetBrains, desktop, web), install commands, Slack and GitHub Actions integrations, Claude Code reading `AGENTS.md` in place of `CLAUDE.md` |
| [Model configuration](https://code.claude.com/docs/en/model-config) | 2026-10-15 | Aliases and their per-provider mappings, minimum versions (2.1.257 / 2.1.280 / 2.1.284 / 2.1.293), Claude Code effort defaults, effort precedence, `/model`, `/effort`, `--model`, `--effort`, Fable usage-credit consent and the `-p` exception, `opusplan`, `CLAUDE_CODE_SUBAGENT_MODEL`, provider pinning |
| [Subagents](https://code.claude.com/docs/en/sub-agents) | 2026-10-15 | Frontmatter fields (`name`, `description`, `tools`, `disallowedTools`, `model`, `effort`, `color`, `isolation` and others), model resolution order, `/tasks`, file locations and precedence, plugin namespacing, built-in Explore and Plan agents, nesting depth, `--agents` flag |
| [Agent teams](https://code.claude.com/docs/en/agent-teams) | 2026-10-15 | Experimental status, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, token cost, 3 to 5 teammate guidance, subagent definitions as teammates |
| [Advisor](https://code.claude.com/docs/en/advisor) | 2026-10-15 | Experimental status, Anthropic API only, accepted pairings, `/advisor` syntax, Fable consent, billing |
| [Fast mode](https://code.claude.com/docs/en/fast-mode) | 2026-10-15 | Supported models, $8 / $40 Opus 5.5 pricing, up to 2.5× speed, usage-credit billing, provider limits |
| [Manage costs](https://code.claude.com/docs/en/costs) | 2026-10-15 | Average enterprise cost figures, `/usage`, prompt-cache line, agent-team token multiple, Sonnet for teammates, subagent cost advice |
| [Environment variables](https://code.claude.com/docs/en/env-vars) | 2026-10-15 | `CLAUDE_CONFIG_DIR`, `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` |
| [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces) | 2026-10-15 | `claude plugin marketplace add owner/repo`, `claude plugin install name@marketplace`, `claude plugin validate`, relative-path sources. `marketplace update` and `plugin update` subcommands confirmed with `claude plugin --help` (2.1.300) |
| [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference) | 2026-10-15 | `marketplace.json` required fields, naming rules, reserved names, `"./"` root source |
| [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) | 2026-10-15 | `plugin.json` fields, default `agents/` directory, agent namespacing (`agent-team:reviewer`) |
| [Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents) | 2026-10-15 | `AgentDefinition` fields including `model` and `effort`, context isolation, final-message handoff, nesting limits, package names |
| [Change the model, effort and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings) | 2026-10-15 | Model and effort menu in claude.ai chat |
| [Models, usage and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code) | 2026-10-15 | `/model` as the source of truth for your account's models |
| [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | 2026-10-15 | `/install-github-app` setup and its requirements |

## Local evidence

| Check | Date | Result |
|---|---|---|
| `claude plugin validate . --strict` with Claude Code 2.1.300 | 2026-10-15 | Validation passed |
| Local marketplace add and plugin install in an isolated config folder | 2026-10-15 | Installed; `claude plugin details` listed `Agents (8)` and about 415 always-on tokens |
| `claude plugin uninstall` and `claude plugin marketplace remove` | 2026-10-15 | Both succeeded |
| HTTP check of docs.anthropic.com and docs.claude.com model pages | 2026-10-15 | 301 and 302 redirects to platform.claude.com |

## Other sources

| Source | Checked on | Used to establish |
|---|---|---|
| [VYR Agent OS](https://vyrwork.com/agent-os) | 2026-10-15 | 14 workflow cards and their 3 / 1 / 10 status labels for the [atlas](docs/atlas/SOURCES.md) |
| [ChatGPT Agent Team Guide](https://github.com/dextee/chatgpt-agent-team-guide) and [Kimi Agent Team Guide](https://github.com/dextee/kimi-agent-team-guide) | 2026-10-15 | Sibling role assignments in the [trilogy mapping](docs/from-chatgpt-and-kimi.md), as published in their READMEs |

## Claim boundaries

- "Recommended" means this guide's starting configuration unless a sentence attributes it to Anthropic.
- API list rates are date-specific. They do not establish subscription allowances or the cost of a finished task.
- A model ID in a file does not prove that an account can run that model.
- The average cost figures are Anthropic's reported numbers, not measurements by this guide.
- Local parsing and installer tests do not evaluate model quality.
- The note that cloud sessions on claude.ai/code do not see files in your local `~/.claude` folder is an inference, marked as such where it appears.
- Illustrations are conceptual artwork, not screenshots or measured diagrams.

## Could not verify

- The exact model-by-plan entitlement table for claude.ai (Free, Pro, Max, Team, Enterprise). The official pages say to check `/model` or the model menu for your account, so this guide makes no per-plan claim.
- The current major version tag of the Claude Code GitHub Action. The repository README links to a migration guide for "v1.0" but this guide does not quote a tag.

## Keeping the guide current

Recheck the models overview, pricing, model configuration and subagent reference when Anthropic releases a model or Claude Code changes its agent format. Update the agent files, the [selector](docs/task-selector.md), the [rates](docs/models-and-effort.md), this register's dates and the README badge together. Then run `python3 scripts/validate.py`.
