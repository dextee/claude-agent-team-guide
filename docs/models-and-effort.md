[Home](../README.md) · [Task selector](task-selector.md) · [Cost and evaluation](cost-and-evaluation.md)

# Models, effort and practical defaults

Checked against official Anthropic documentation: **15 October 2026**.

<img src="../assets/images/model-team.png" alt="Four instruments on ivory plinths: a violet armillary sphere, terracotta dividers over a model, a sage balance scale and a sky-blue hourglass" width="420">

## The four current models

| | Claude Fable 5.1 | Claude Opus 5.5 | Claude Sonnet 5.5 | Claude Haiku 5.5 |
|---|---|---|---|---|
| Anthropic's description | For demanding reasoning and long-horizon agentic work | For long-running agentic coding and knowledge work | The best combination of speed and intelligence | For high-volume, latency-sensitive tasks such as classification, extraction, and routing |
| Claude API ID | `claude-fable-5-1` | `claude-opus-5-5` | `claude-sonnet-5-5` | `claude-haiku-5-5` |
| Claude Code alias | `fable` | `opus` | `sonnet` | `haiku` |
| Relative latency | Slower | Moderate | Fast | Fastest |
| Context window / max output | 1M / 128K | 1M / 128K | 1M / 128K | 1M / 128K |
| Thinking | Adaptive, always on | Adaptive, always on | Adaptive | Adaptive |
| Default effort, Claude API | `high` | `medium` | `high` | `medium` |
| Default effort, Claude Code | `high` | `medium` | `medium` | `medium` |
| Minimum Claude Code version | 2.1.257 | 2.1.280 | 2.1.284 | 2.1.293 |

Sources: [models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), [Claude Code model configuration](https://code.claude.com/docs/en/model-config). On the Anthropic API the `opus`, `sonnet` and `haiku` aliases resolve to these versions. On other providers they can resolve to older versions; see [product surfaces](product-surfaces.md).

## Standard API rates

USD per million tokens, Claude API, standard speed. These are not subscription allowances.

| Model | Input | Cache read | Output |
|---|---|---|---|
| `claude-fable-5-1` | $10.00 | $0.25 | $50.00 |
| `claude-opus-5-5` | $4.00 | $0.20 | $20.00 |
| `claude-sonnet-5-5` | $2.00 | $0.10 | $10.00 |
| `claude-haiku-5-5` | $0.10 | $0.01 | $0.50 |

- **Haiku 5.5 is priced by prompt length.** The row above applies to prompts up to 100,000 tokens. Above that, the whole request is billed at $0.50 input, $0.05 cache read and $2.50 output. An explorer working through a very large codebase can cross that line.
- **Cache reads are discounted more than usual** on Fable 5.1 (2.5% of input), Opus 5.5 and Sonnet 5.5 (5%). Other models use 10%.
- **Batch API** requests are 50% off input and output.
- **Fast mode** for Opus 5.5 is $8 input and $40 output, a research preview with up to 2.5× faster output. It is available on the Claude API and on subscription plans through usage credits, not on Bedrock, Google Cloud, Foundry or Claude Platform on AWS ([fast mode](https://code.claude.com/docs/en/fast-mode)).
- The 4.7-and-later tokenizer produces about 30% more tokens for the same text than older models. Compare per-task cost, not per-token rates alone.

Source: [pricing](https://platform.claude.com/docs/en/about-claude/pricing).

## Choose capability, then tune effort

Effort controls how many tokens Claude spends on a response, including thinking, text and tool calls. Lower effort means fewer, more consolidated tool calls and terser output. Anthropic's guidance: *"Tuning effort is often a better lever than switching models."*

| Level | Anthropic's typical use | This guide's starting use |
|---|---|---|
| `low` | Simpler tasks that need the best speed and lowest costs, such as subagents | Chat, one clear transformation, simple classification |
| `medium` | Agentic tasks that balance speed, cost and performance | Everyday building; explorer and worker agents |
| `high` | Complex reasoning, difficult coding, agentic tasks | Review, investigation, Fable planning and audits |
| `xhigh` | Long-running agentic and coding tasks, over 30 minutes | Multi-hour autonomous runs, when measured |
| `max` | The deepest possible reasoning | Frontier problems, when measured |

Per-model notes from the [effort guide](https://platform.claude.com/docs/en/build-with-claude/effort):

- **Fable 5.1:** start at `high`. Step up for the most capability-sensitive work; step down for routine work once evals show quality holds.
- **Opus 5.5:** `medium` is the default, one level below Opus 5. Thinking can't be turned off; effort is the main control. Run an effort sweep instead of carrying old settings forward.
- **Sonnet 5.5:** levels are recalibrated from Sonnet 5. For agentic coding start at `medium` for well-specified tasks and `high` for harder ones.
- **Haiku 5.5:** start at `medium`. At `low`, in long agent prompts, it is more likely to skip a search, stop early or skip a check. That is why the explorer here runs at `medium`.

### Where to set it

Highest precedence first:

| Scope | How |
|---|---|
| Everything, including agent files | `CLAUDE_CODE_EFFORT_LEVEL=high` |
| One agent while it runs | `effort: high` in its frontmatter (overrides the session level) |
| One session | `claude --effort high` or `/effort high` |
| Saved per-model level | `/effort` saves it under `modelSettings` in user settings; `effortLevel` is the fallback for models without one |
| Model default | Nothing set |

Source: [model configuration](https://code.claude.com/docs/en/model-config). `/effort auto` clears your saved level for the active model.

## Set the model in the right place

```bash
claude --model opus             # one session, alias
claude --model claude-fable-5-1 # one session, exact ID
```

Inside a session, `/model` switches the model and saves it as your default for new sessions. Subagents that inherit the main model follow the switch; the eight agents in this guide do not, because they pin their own model.

Fable is never the account default. Select it with `/model fable` or `claude --model fable`. On some plans Fable bills to usage credits, and the `/model` picker shows "Requires usage credits" on its row.

## Other ways to combine models

| Approach | When the stronger model runs | Notes |
|---|---|---|
| Subagent with `model` set | For the whole delegated task | This guide's main pattern |
| [Advisor](https://code.claude.com/docs/en/advisor) | At decision points, when Claude chooses to consult it | Experimental; Anthropic API only; adds usage |
| `opusplan` | During plan mode, then Sonnet executes | A model alias, set with `/model opusplan` |
| [Agent teams](https://code.claude.com/docs/en/agent-teams) | Each teammate is a full session | Experimental; significantly more tokens; start with 3 to 5 teammates |
| `/model` | From the next request onward | Simple; affects inheriting subagents too |

## What changed from the previous edition

The earlier guide (v1.1.0, 27 September 2026) used Sonnet 5 and Haiku 4.5.

| | v1.1.0 | v2.0.0 (this guide) |
|---|---|---|
| Worker model | `claude-sonnet-5` | `claude-sonnet-5-5`, same $2 / $10, cache read $0.20 → $0.10 |
| Explorer model | `claude-haiku-4-5-20251001`, no effort control, 200K context | `claude-haiku-5-5`, effort `medium`, 1M context, $1 / $5 → $0.10 / $0.50 up to 100K-token prompts |
| Auditor effort | `xhigh` | `high`, Fable's default. Raise it for a specific audit when evidence calls for it |
| Agents | Five | Eight: adds reviewer, researcher and editor |
| Settings preset | Merged by default; set model, effort and a Fable advisor | Opt-in with `--with-settings`; sets only the default subagent model |

Claude Code already defaults to Opus 5.5 at `medium` on paid plans, so the preset no longer repeats it.

## A useful escalation packet

When you move a task to a stronger model or higher effort, send: the objective, the relevant evidence, approaches already tried, the observed failure, and the decision you need. Return the resolved decision to the original agent where practical.
