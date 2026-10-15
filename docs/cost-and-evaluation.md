[Home](../README.md) · [Model rates](models-and-effort.md) · [Evaluation CSV](../templates/evaluation.csv)

# Choose by completed-task cost

The useful comparison is the cost of reaching an accepted result, including failed attempts and rework. A cheap first response can still lead to an expensive task.

## A transparent arithmetic example

Suppose one request uses **10,000 uncached input tokens and 2,000 billable output tokens**, with no cache, tools, batch discount or fast mode. Using the standard rates in the [model guide](models-and-effort.md):

| Model | Input calculation | Output calculation | Hypothetical total |
|---|---|---|---|
| Haiku 5.5 | 10,000 / 1M × $0.10 | 2,000 / 1M × $0.50 | $0.002 |
| Sonnet 5.5 | 10,000 / 1M × $2.00 | 2,000 / 1M × $10.00 | $0.040 |
| Opus 5.5 | 10,000 / 1M × $4.00 | 2,000 / 1M × $20.00 | $0.080 |
| Fable 5.1 | 10,000 / 1M × $10.00 | 2,000 / 1M × $50.00 | $0.200 |

This is arithmetic, not a benchmark. Different models use different numbers of tokens for the same task, and thinking tokens bill as output. The Haiku row assumes the prompt stays at or under 100,000 tokens. Subscription limits cannot be derived from this table.

The example ignores caching, which matters a lot for agents. Claude Code caches automatically, and cache reads cost $0.20 per million on Opus 5.5 against $4.00 fresh. Measure your own hit rate: `/usage` shows a `Prompt cache (main)` line with the share of input tokens served from cache ([costs](https://code.claude.com/docs/en/costs)).

## What Anthropic reports for Claude Code

Anthropic's cost guide reports that across enterprise deployments the average Claude Code cost is about **$13 per developer per active day** and $150 to $250 per developer per month, with 90% of users below $30 per active day ([costs](https://code.claude.com/docs/en/costs)). These are Anthropic's figures, not measurements by this guide. Your numbers depend on model choice, codebase size and how many agents you run.

The same guide notes:

- Agent teams use roughly 7× more tokens than standard sessions when teammates run in plan mode.
- Delegating verbose work (test runs, log processing, documentation fetches) to subagents keeps that output out of the main context; the subagent's own requests still count.
- For simple subagent tasks, it suggests a smaller model such as `haiku`.

## Run a small, useful comparison

1. Pick five representative tasks: a small fix, a feature, a refactor, a hard bug and a review.
2. Fix the starting commit and write acceptance checks before running anything.
3. Run the same inputs through each candidate route, for example Opus 5.5 / medium alone versus Opus lead with Sonnet workers.
4. Record pass or fail, human rework, retries, elapsed time and billed usage, including failed runs.
5. Compare cost per **accepted** result. Keep the hard cases as regression checks.
6. Write down when the cheaper route must escalate.

The [evaluation worksheet](../templates/evaluation.csv) is intentionally empty. This guide has not invented any performance measurements.

## Keep the team efficient

- Give each agent only the context it needs, and ask for a compact, evidence-backed return.
- Parallelize independent work when elapsed time matters, but count every agent's usage.
- Prefer one agent for short tasks or tightly ordered steps.
- Use `/clear` between unrelated tasks; stale context costs tokens on every message.
- Stop reviewing once the acceptance checks pass. Match verification to the remaining risk.
- In automation, cap spend. The Agent SDK supports `max_budget_usd` (Python) or `maxBudgetUsd` (TypeScript), and limits on subagent depth and concurrency ([Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents)).
