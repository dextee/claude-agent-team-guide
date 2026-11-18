[Home](../README.md) · [Task selector](task-selector.md) · [Cost and evaluation](cost-and-evaluation.md)

# Models, effort and practical defaults

The model and price tables describe this edition's **15 October 2026** choices. Fable routing and subagent effort were rechecked on **18 November 2026**; see the [source register](../SOURCES.md#18-november-2026-source-checks).

<img src="../assets/images/model-team.png" alt="Four instruments on ivory plinths: a violet armillary sphere, terracotta dividers over a model, a sage balance scale and a sky-blue hourglass" width="420">

## The four models this edition pins

The architect and auditor deliberately request `claude-fable-5-1` at `high`. Anthropic still lists [5.1 as active](https://platform.claude.com/docs/en/about-claude/model-deprecations), but its [current model overview](https://platform.claude.com/docs/en/about-claude/models/overview) recommends **Fable 5.2** for demanding work beyond Opus 5.5. These are distinct choices: Fable 5.2 requires at least v2.1.321 and defaults to `medium` in Claude Code.

| | Claude Fable 5.1 | Claude Opus 5.5 | Claude Sonnet 5.5 | Claude Haiku 5.5 |
|---|---|---|---|---|
| Anthropic's description | For demanding reasoning and long-horizon agentic work | For long-running agentic coding and knowledge work | The best combination of speed and intelligence | For high-volume, latency-sensitive tasks such as classification, extraction, and routing |
| Claude API ID | `claude-fable-5-1` | `claude-opus-5-5` | `claude-sonnet-5-5` | `claude-haiku-5-5` |
| Claude Code selector | Use the exact 5.1 ID | `opus` | `sonnet` | `haiku` |
| Relative latency | Slower | Moderate | Fast | Fastest |
| Context window / max output | 1M / 128K | 1M / 128K | 1M / 128K | 1M / 128K |
| Thinking | Adaptive, always on | Adaptive, always on | Adaptive | Adaptive |
| Default effort, Claude API | `high` | `medium` | `high` | `medium` |
| Default effort, Claude Code | `high` | `medium` | `medium` | `medium` |
| Minimum Claude Code version | 2.1.257 | 2.1.280 | 2.1.284 | 2.1.293 |

Sources: [models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), [Claude Code model configuration](https://code.claude.com/docs/en/model-config). On the Anthropic API the `opus`, `sonnet` and `haiku` aliases resolve to these versions. On other providers they can resolve to older versions; see [product surfaces](product-surfaces.md).

## Standard API rates

USD per million tokens, Claude API, standard speed, for the pinned versions as checked in October. These are not subscription allowances.

| Model | Input | Cache read | Output |
|---|---|---|---|
| `claude-fable-5-1` | $10.00 | $0.25 | $50.00 |
| `claude-opus-5-5` | $4.00 | $0.20 | $20.00 |
| `claude-sonnet-5-5` | $2.00 | $0.10 | $10.00 |
| `claude-haiku-5-5` | $0.10 | $0.01 | $0.50 |

- **Haiku 5.5 is priced by prompt length.** The row above applies to prompts up to 100,000 tokens. Above that, the whole request is billed at $0.50 input, $0.05 cache read and $2.50 output. An explorer working through a very large codebase can cross that line.
- **Cache reads are discounted more than usual** on Fable 5.1 (2.5% of input), Opus 5.5 and Sonnet 5.5 (5%). Other models use 10%.
- **Batch API** requests are 50% off input and output.
- **Fast mode** for Opus 5.5 is $8 input and $40 output per million tokens at Anthropic's rates. Check the [fast-mode requirements](https://code.claude.com/docs/en/fast-mode#requirements) for your provider.
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

For a **non-fork subagent**, check these in order:

1. `CLAUDE_CODE_EFFORT_LEVEL` set to a level such as `high` overrides both the invocation and the file.
2. An `effort` passed when Claude starts the subagent overrides its file for that run, including when resumed. Per-invocation effort is supported from v2.1.292.
3. The role's `effort:` field sets its usual level. All eight roles here set one.

If none is set, a subagent on the lead's model follows the lead's selected session effort. On a different model, the lead's session selection does not carry over. Organization effort caps still apply. Check `/tasks` while the agent is running. [Subagent effort](https://code.claude.com/docs/en/sub-agents#choose-an-effort-level) · [Organization effort limits](https://code.claude.com/docs/en/model-config#organization-effort-limits)

For the **lead session**, use `claude --effort high` at launch or `/effort high` in the session. `/effort auto` clears the saved level for the active model. [Model configuration](https://code.claude.com/docs/en/model-config#set-the-effort-level)

## Set the model in the right place

```bash
claude --model opus             # one session, alias
claude --model claude-fable-5-1 # one session, exact ID
```

Inside an interactive session, `/model` selects the lead model. A new subagent with `model: inherit` follows its parent. These eight roles request their own model unless an [override or an organization restriction](agents.md#how-claude-code-picks-the-model-for-a-subagent) applies.

To reproduce this edition's Fable choice, select `/model claude-fable-5-1`. To follow the provider's alias instead, select `/model fable`: by default on current Claude Code it resolves to 5.2, except in Claude apps gateway sessions where it resolves to Fable 5. `ANTHROPIC_DEFAULT_FABLE_MODEL` can change the mapping. On plans where Fable bills to usage credits, the `/model` picker labels it “Requires usage credits.” [Model aliases](https://code.claude.com/docs/en/model-config#model-aliases)

## Other ways to combine models

| Approach | When the stronger model runs | Notes |
|---|---|---|
| Subagent with `model` set | For the whole delegated task | This guide's main pattern |
| [Advisor](https://code.claude.com/docs/en/advisor) | At decision points, when Claude chooses to consult it | Experimental; adds usage. See [provider availability](product-surfaces.md#third-party-providers) |
| `opusplan` | During plan mode, then Sonnet executes | A model alias, set with `/model opusplan` |
| [Agent teams](https://code.claude.com/docs/en/agent-teams) | Each teammate is a full session | Experimental; significantly more tokens; start with 3 to 5 teammates |
| `/model` | From the next request onward | Simple; affects inheriting subagents too |

## What changed from the previous edition

The earlier guide (v1.1.0, 27 September 2026) used Sonnet 5 and Haiku 4.5.

| | v1.1.0 | v2.0.0 (this guide) |
|---|---|---|
| Worker model | `claude-sonnet-5` | `claude-sonnet-5-5`, same $2 / $10, cache read $0.20 → $0.10 |
| Explorer model | `claude-haiku-4-5-20251001`, no effort control, 200K context | `claude-haiku-5-5`, effort `medium`, 1M context, $1 / $5 → $0.10 / $0.50 up to 100K-token prompts |
| Auditor effort | `xhigh` | `high`, the pinned Fable 5.1 default. Raise it for a specific audit when evidence calls for it |
| Agents | Five | Eight: adds reviewer, researcher and editor |
| Settings preset | Merged by default; set model, effort and a Fable advisor | Opt-in with `--with-settings`; sets only the default subagent model |

Claude Code already defaults to Opus 5.5 at `medium` on paid plans, so the preset no longer repeats it.

## A useful escalation packet

When you move a task to a stronger model or higher effort, send: the objective, the relevant evidence, approaches already tried, the observed failure, and the decision you need. Return the resolved decision to the original agent where practical.
