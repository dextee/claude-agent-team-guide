# Source register

[Home](README.md) · [Validation](VALIDATION.md)

**Every Anthropic source below was checked on 2026-11-15**, by fetching the page's Markdown and reading the passages the guide relies on. Technical statements come from official Anthropic documentation (platform.claude.com, which docs.claude.com and docs.anthropic.com point to; code.claude.com; support.claude.com) and Anthropic's GitHub organization. Model IDs, rates, effort defaults and Claude Code minimum versions are recorded once, in [templates/models.json](templates/models.json). Team designs, model-to-role assignments, patterns, recipes and failure-mode advice are the author's recommendations, inferred from those sources and from practice. They have not been benchmarked.

## Models and pricing

| Source | Checked on | Used to establish |
|---|---|---|
| [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | 2026-11-15 | The four current models (Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5), API IDs, descriptions, comparative latency, context and max output, thinking mode, API default effort, cache-read ratios, Anthropic's "start with Opus 5.5 … use Fable 5.2" recommendation; the list of older model names the validator accepts |
| [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | 2026-11-15 | Input, cache-read and output rates for Fable 5.2, Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5; Haiku 5.5's 100K-token threshold; batch discount; fast-mode rates ($16 / $80 Fable 5.2, $8 / $40 Opus 5.5) and API-side fast-mode platforms; tokenizer note |
| [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) | 2026-11-15 | Selection matrix ("subagent tasks" for Haiku 5.5, "multihour autonomous coding agents" for Opus 5.5), "Tuning effort is often a better lever than switching models" |
| [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) | 2026-11-15 | Effort levels and typical uses; per-model recommendations, including Fable 5.2 "start with `high`" and the advice to re-sweep rather than carry settings over from Fable 5.1 |
| [What's new in Claude Fable 5.2](https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2) | 2026-11-15 | Fable 5.2 positioning and that it is available to all Claude API customers. Release date not stated in the docs, so the guide states none |

## Claude Code: running subagents

| Source | Checked on | Used to establish |
|---|---|---|
| [Subagents](https://code.claude.com/docs/en/sub-agents) | 2026-11-15 | Every frontmatter field and its rules; skipped-file cases; file locations and precedence; plugin field restrictions; model resolution order, `inherit` for nested subagents, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`; per-invocation effort (v2.1.292); `/tasks` model display (v2.1.242); background-by-default, completion notifications, background tool filter, fork mode and `CLAUDE_CODE_FORK_SUBAGENT`; what loads at startup; resume, agent IDs, `SendMessage`, names and teammates; `maxTurns` partial output (v2.1.246); API errors in subagents; output scanning; depth (3) and concurrency (20) limits; worktree isolation and its checks; forks; "choose between subagents and main conversation" |
| [Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents) | 2026-11-15 | Context isolation; only the final message returns and the parent may summarize it; what a subagent receives; depth, concurrency and spend caps (`max_budget_usd` / `maxBudgetUsd`) and their effects |
| [Worktrees](https://code.claude.com/docs/en/worktrees) | 2026-11-15 | Subagent worktrees, cleanup and the sweep, locks, `worktree.baseRef` (`"fresh"` default, `"head"`), instruction files in worktrees |
| [Agent teams](https://code.claude.com/docs/en/agent-teams) | 2026-11-15 | Experimental status, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, comparison table with subagents, named subagents launching as teammates, subagent definitions as teammates, teammate model order, team hooks, limitations, 3 to 5 teammates, the anchoring quotation, teammate cache lifetime |
| [Hooks reference](https://code.claude.com/docs/en/hooks) | 2026-11-15 | `SubagentStart`, `SubagentStop` input (`last_assistant_message`, `stop_hook_active`) and decision control, exit-code-2 behavior per event, `SubagentHandback` caveat (v2.1.271), `TaskCreated`, `TaskCompleted`, hooks in agent files and workspace trust |
| [Tools reference](https://code.claude.com/docs/en/tools-reference) | 2026-11-15 | `ExitWorktree` and `EnterWorktree` behavior inside isolated subagents |
| [Prompt caching in Claude Code](https://code.claude.com/docs/en/prompt-caching) | 2026-11-15 | Subagents warm their own cache; five-minute default lifetime for subagents; forks reuse the parent's cache |
| [Settings reference](https://code.claude.com/docs/en/settings-reference) | 2026-11-15 | `subagentPromptCacheTtl` values and precedence |
| [Settings](https://code.claude.com/docs/en/settings) | 2026-11-15 | Settings files and `env` block used in examples |
| [Environment variables](https://code.claude.com/docs/en/env-vars) | 2026-11-15 | `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`, and the variables named on the subagents page |

## Claude Code: models, cost and surfaces

| Source | Checked on | Used to establish |
|---|---|---|
| [Model configuration](https://code.claude.com/docs/en/model-config) | 2026-11-15 | Aliases and per-provider mappings, including Claude Models on Google Cloud (Anthropic managed); `fable` resolving to Fable 5.2; minimum versions (Fable 5.2 v2.1.321, Haiku 5.5 v2.1.293, Sonnet 5.5 v2.1.284, Opus 5.5 v2.1.280, Fable 5.1 v2.1.257); Claude Code effort defaults (`medium` for Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5); effort resolution order and the user-settings `effortLevel` exception; subagent effort; Fable usage-credit consent and the `-p` exception |
| [Manage costs](https://code.claude.com/docs/en/costs) | 2026-11-15 | Average enterprise cost figures, `/usage` session block and plan-usage attribution to subagents, `Prompt cache (main)` (main conversation only), agent-team token multiple, Sonnet for teammates, `model: haiku` for simple subagents |
| [Fast mode](https://code.claude.com/docs/en/fast-mode) | 2026-11-15 | Fast mode available for Fable 5.2 and Opus 5.5, research preview only for Opus 5 and Opus 4.8; providers; Agent Platform conditions (Fable 5.2, v2.1.322); usage credits on subscription plans |
| [Advisor](https://code.claude.com/docs/en/advisor) | 2026-11-15 | Experimental status; Anthropic API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed), the last two from v2.1.300; not Bedrock, Agent Platform or Foundry; pairing table; subagents inherit the advisor |
| [Claude Code overview](https://code.claude.com/docs/en/overview) | 2026-11-15 | Surfaces, desktop app paid subscription, Slack, "connects to the same underlying Claude Code engine" |
| [GitHub Actions](https://code.claude.com/docs/en/github-actions) | 2026-11-15 | Quick setup works with the Claude API and Claude subscriptions; admin access required |
| [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces) | 2026-11-15 | `claude plugin marketplace add`, `claude plugin install name@marketplace`, `claude plugin validate` |
| [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference) | 2026-11-15 | `marketplace.json` naming rules, `"./"` root source |
| [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) | 2026-11-15 | Default `agents/` directory, agent namespacing (`agent-team:reviewer`) |
| [Change the model, effort and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings) | 2026-11-15 (reachable; content not re-read) | Model and effort menu in claude.ai chat |
| [Models, usage and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code) | 2026-11-15 (reachable; content not re-read) | `/model` as the source of truth for your account's models |
| [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | 2026-11-15 (reachable) | The Claude Code GitHub Action repository |

## Local evidence

| Check | Date | Result |
|---|---|---|
| `bash -c 'n=$(printf "abc\n" \| grep -c zzz \|\| echo 0); printf "[%s]\n" "$n"'` | 2026-11-15 | Printed `[0` and `0]` on two lines, as described in [failure modes](docs/failure-modes.md#4-gates-that-cannot-fail) |
| [templates/hooks/subagent-stop-gate.sh](templates/hooks/subagent-stop-gate.sh) fed a report without and with the return contract | 2026-11-15 | Exit 2 and exit 0; covered by `scripts/test_validate.py` |
| `claude plugin validate . --strict` and local plugin install | 2026-10-15 (Claude Code 2.1.300) | Passed then. Not re-run against the 3.0.0 agents at v2.1.321; see [validation](VALIDATION.md) |

## Other sources

| Source | Checked on | Used to establish |
|---|---|---|
| [VYR Agent OS](https://vyrwork.com/agent-os) | 2026-11-15 (overview page) | 14 workflow cards and their 3 / 1 / 10 status labels for the [atlas](docs/atlas/SOURCES.md) |
| [ChatGPT Agent Team Guide](https://github.com/dextee/chatgpt-agent-team-guide) and [Kimi Agent Team Guide](https://github.com/dextee/kimi-agent-team-guide) | 2026-10-15 | Sibling role assignments in the [trilogy mapping](docs/from-chatgpt-and-kimi.md), from their READMEs and setup pages |

## Claim boundaries

- "Recommended" means this guide's starting configuration unless a sentence attributes it to Anthropic.
- API list rates are date-specific. They do not establish subscription allowances or the cost of a finished task.
- A model ID in a file does not prove that an account can run that model.
- The average cost figures are Anthropic's reported numbers, not measurements by this guide.
- Local parsing, hook and installer tests do not evaluate model quality or team behavior in a live session.
- The note that cloud sessions on claude.ai/code do not see files in your local `~/.claude` folder is an inference, marked as such where it appears.
- `maxTurns: 40` on the worker is an editorial starting value, not an Anthropic number.
- Illustrations are conceptual artwork, not screenshots or measured diagrams.

## Could not verify

- The exact model-by-plan entitlement table for claude.ai (Free, Pro, Max, Team, Enterprise). The official pages say to check `/model` or the model menu for your account, so this guide makes no per-plan claim.
- A release date for Fable 5.2 on an Anthropic page. None is stated, so the guide gives none.
- What an isolated subagent's result reports about its worktree. The docs don't say, so the worker is told to report its own path, branch and commit.
- Whether `isolation: worktree` works outside a git repository. Not tested; the guide says so.
- The current major version tag of the Claude Code GitHub Action. This guide does not quote a tag.

## Keeping the guide current

Recheck the models overview, pricing, model configuration, subagent reference, worktrees and agent-teams pages when Anthropic releases a model or Claude Code changes its agent format. Update [templates/models.json](templates/models.json) first, then the agent files, the docs footers' check date and this register. Then run `python3 scripts/validate.py`.
