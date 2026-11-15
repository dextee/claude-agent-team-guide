[Home](../README.md) · [Task selector](task-selector.md) · [Cost and limits](cost-and-evaluation.md)

# Models, effort and practical defaults

Model routing is one lever in running a team: it decides what each role costs and how deeply it reasons. The other chapters cover how the team runs. Checked against official Anthropic documentation on **15 November 2026**. The numbers on this page come from [templates/models.json](../templates/models.json), which the validator checks against every page that repeats them.

<img src="../assets/images/model-team.png" alt="Four instruments on ivory plinths: a violet armillary sphere, terracotta dividers over a model, a sage balance scale and a sky-blue hourglass" width="420">

## The four current models

| | Claude Fable 5.2 | Claude Opus 5.5 | Claude Sonnet 5.5 | Claude Haiku 5.5 |
|---|---|---|---|---|
| Anthropic's description | For demanding reasoning and long-horizon agentic work | For long-running agentic coding and knowledge work | The best combination of speed and intelligence | For high-volume, latency-sensitive tasks such as classification, extraction, and routing |
| Claude API ID | `claude-fable-5-2` | `claude-opus-5-5` | `claude-sonnet-5-5` | `claude-haiku-5-5` |
| Claude Code alias | `fable` | `opus` | `sonnet` | `haiku` |
| Comparative latency | Moderate | Moderate | Fast | Fastest |
| Context window / max output | 1M / 128K | 1M / 128K | 1M / 128K | 1M / 128K |
| Thinking | Adaptive, always on | Adaptive, always on | Adaptive | Adaptive |
| Default effort, Claude API | `high` | `medium` | `high` | `medium` |
| Default effort, Claude Code | `medium` | `medium` | `medium` | `medium` |
| Minimum Claude Code version | 2.1.321 | 2.1.280 | 2.1.284 | 2.1.293 |

Anthropic's guidance: *"If you're unsure which model to use, start with Claude Opus 5.5 for most workloads. Use Claude Fable 5.2 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short."* ([models overview](https://platform.claude.com/docs/en/about-claude/models/overview)).

**Fable 5.1** is the previous Fable. It is still selectable by ID (`claude-fable-5-1`, Claude Code v2.1.257 or later, $10 / $50) and Claude Code runs it at `high` effort by default. Use it only if your account or Claude Code version cannot run Fable 5.2; see [no Fable 5.2](#if-you-cannot-run-fable-52).

Sources: [models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), [Claude Code model configuration](https://code.claude.com/docs/en/model-config). On the Anthropic API the `fable`, `opus`, `sonnet` and `haiku` aliases resolve to these versions. On other providers `opus`, `sonnet` and `haiku` can resolve to older versions; see [product surfaces](product-surfaces.md).

## Standard API rates

USD per million tokens, Claude API, standard speed. These are not subscription allowances.

| Model | Input | Cache read | Output |
|---|---|---|---|
| `claude-fable-5-2` | $8.00 | $0.20 | $40.00 |
| `claude-opus-5-5` | $4.00 | $0.20 | $20.00 |
| `claude-sonnet-5-5` | $2.00 | $0.10 | $10.00 |
| `claude-haiku-5-5` | $0.10 | $0.01 | $0.50 |

- **Fable 5.2 costs twice Opus 5.5 per token** ($8 against $4 input, $40 against $20 output). Fable 5.1 cost $10 / $50.
- **Haiku 5.5 is priced by prompt length.** The row above applies to prompts up to 100,000 tokens. Above that, the whole request bills at $0.50 input, $0.05 cache read and $2.50 output. An explorer working through a very large codebase can cross that line.
- **Cache reads are discounted more than usual** on Fable 5.2 and Fable 5.1 (2.5% of input) and on Opus 5.5 and Sonnet 5.5 (5%). Other models use 10%.
- **Batch API** requests are 50% off input and output.
- **Fast mode** on the Claude API costs $16 / $80 for Fable 5.2 and $8 / $40 for Opus 5.5, for up to 2.5× higher output speed. Fast mode is available for Fable 5.2 and Opus 5.5; the research-preview label now applies only to Opus 5 and Opus 4.8. Where Claude Code can use it is in [product surfaces](product-surfaces.md#third-party-providers).
- The tokenizer used by Claude 4.7 and later models produces about 30% more tokens for the same text than older models. Compare per-task cost, not per-token rates alone.

Source: [pricing](https://platform.claude.com/docs/en/about-claude/pricing), [fast mode in Claude Code](https://code.claude.com/docs/en/fast-mode).

## Choose capability, then tune effort

Effort controls how many tokens Claude spends on a response, including thinking, text and tool calls. Anthropic's guidance: *"Tuning effort is often a better lever than switching models"* ([choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)).

| Level | Anthropic's typical use | This guide's starting use |
|---|---|---|
| `low` | Simpler tasks that need the best speed and lowest costs, such as subagents | Chat, one clear transformation, simple classification |
| `medium` | Agentic tasks that require a balance of speed, cost, and performance | Everyday building; explorer and worker agents |
| `high` | Complex reasoning, difficult coding problems, agentic tasks | Review, investigation, Fable planning and audits |
| `xhigh` | Long-running agentic and coding tasks (over 30 minutes) with token budgets in the millions | Multi-hour autonomous runs, when measured |
| `max` | Tasks requiring the deepest possible reasoning and most thorough analysis | Frontier problems, when measured |

Per-model notes from the [effort guide](https://platform.claude.com/docs/en/build-with-claude/effort):

- **Fable 5.2:** the API default is `high`, and Anthropic says to start there. Run a fresh effort sweep instead of carrying settings over from Fable 5.1. **Claude Code defaults Fable 5.2 to `medium`**, so the `effort: high` in this guide's architect and auditor is a deliberate raise to the API default, not a restatement of Claude Code's default.
- **Opus 5.5:** `medium` is the default, one level below Opus 5. Thinking can't be turned off; effort is the main control. Run an effort sweep instead of carrying old settings forward.
- **Sonnet 5.5:** levels are recalibrated from Sonnet 5. For agentic coding start at `medium` for well-specified tasks and `high` for harder or longer ones.
- **Haiku 5.5:** start at `medium`. At `low`, in long agent prompts, it is more likely to skip a search, stop early or skip a check. That is why the explorer here runs at `medium`.

### Where effort is set

Claude Code resolves the session's level in this order, first match wins ([model configuration](https://code.claude.com/docs/en/model-config)):

| Order | Source |
|---|---|
| 1 | `CLAUDE_CODE_EFFORT_LEVEL` environment variable. It also overrides the `effort` field in agent files |
| 2 | A level you pick in the session with `/effort` or the `/model` picker |
| 3 | Launching with `--effort` |
| 4 | Your settings: a saved per-model level (`modelSettings`) or an `effortLevel` key |
| 5 | The model's default effort, or your organization's default for its default model |

**The `effortLevel` exception.** A top-level `effortLevel` in your *user* settings file no longer applies to Opus 5.5 or to models released after it, which includes Fable 5.2, Sonnet 5.5 and Haiku 5.5. It still applies to Opus 5, Fable 5.1 and earlier. Those newer models start at their own default until you choose a level with `/effort` or the `/model` picker. A top-level `effortLevel` in project, local or managed settings, or passed with `--settings`, applies to every model.

**Subagents.** An agent file's `effort` overrides the session level, but not `CLAUDE_CODE_EFFORT_LEVEL`. Claude can also pass an `effort` for one invocation (Claude Code v2.1.292 or later), which overrides the file. A subagent with no `effort` of its own runs at your session level only when it runs on your session's model; on another model, that level does not apply ([subagents](https://code.claude.com/docs/en/sub-agents#choose-an-effort-level)).

## Set the model in the right place

```bash
claude --model opus             # one session, alias
claude --model claude-fable-5-2 # one session, exact ID
```

Inside a session, `/model` switches the model and saves it as your default for new sessions. Subagents that inherit the main model follow the switch; the eight agents in this guide do not, because they pin their own model.

No Fable model is the account default on any plan. `/model fable` or `claude --model fable` selects Fable 5.2 (except in Claude apps gateway sessions, where the alias resolves differently). Fable 5.1 is selected by ID. On some plans Fable bills to usage credits, and the `/model` picker shows "Requires usage credits" on its row.

### If you cannot run Fable 5.2

The architect and auditor pin `claude-fable-5-2`, which needs Claude Code v2.1.321 or later and Fable access. If either is missing:

1. Upgrade with `claude update` (preferred).
2. Or edit `model:` in `architect.md` and `auditor.md` to `claude-fable-5-1` (Claude Code v2.1.257 or later, higher price), or to `claude-opus-5-5` and raise `effort` to `high` or `xhigh`.

## Other ways to combine models

| Approach | When the stronger model runs | Notes |
|---|---|---|
| Subagent with `model` set | For the whole delegated task | This guide's main pattern |
| [Advisor](https://code.claude.com/docs/en/advisor) | At decision points, when Claude chooses to consult it | Experimental. Anthropic API, Claude Platform on AWS, or Claude Models on Google Cloud (Anthropic managed); not Bedrock, Google Cloud's Agent Platform or Foundry. Adds usage |
| `opusplan` | During plan mode, then Sonnet executes | A model alias, set with `/model opusplan` |
| [Agent teams](agent-teams.md) | Each teammate is a full session | Experimental; significantly more tokens |
| `/model` | From the next request onward | Simple; affects inheriting subagents too |

## Changes in guide 3.0.0

| | 2.0.0 | 3.0.0 |
|---|---|---|
| Architect and auditor | `claude-fable-5-1`, $10 / $50 | `claude-fable-5-2`, $8 / $40, cache read $0.25 → $0.20 |
| Team minimum Claude Code | Set by Haiku 5.5 | v2.1.321 or later, set by Fable 5.2 |
| Worker | Edited your checkout | `isolation: worktree` and `maxTurns: 40` |
| Explorer | Loaded CLAUDE.md | `omitClaudeMd: true`, like the built-in Explore agent |

The full history is in the [changelog](../CHANGELOG.md).

## A useful escalation packet

When you move a task to a stronger model or higher effort, send: the objective, the relevant evidence, approaches already tried, the observed failure, and the decision you need. Return the resolved decision to the original agent where practical. [Handoff contracts](handoff-contracts.md) has the full format.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
