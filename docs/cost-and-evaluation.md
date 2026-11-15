[Home](../README.md) · [Model rates](models-and-effort.md) · [When to delegate](when-to-delegate.md) · [Evaluation CSV](../templates/evaluation.csv)

# Cost, limits and evaluation

A team of subagents costs more tokens than one session doing the same work, because every subagent sends its own requests. It pays off when it keeps the lead's context small, runs independent work in parallel, or puts a cheaper model on checkable work. This page shows how to see the cost, cap it, and decide with measurements. Checked against official documentation on **15 November 2026**.

## Where the tokens go

- **Every subagent sends its own requests**, which count toward the same usage limits as your main conversation ([subagents](https://code.claude.com/docs/en/sub-agents)).
- **Results come back into the lead's context.** Many subagents that each return long reports can fill the main conversation ([subagents: run parallel research](https://code.claude.com/docs/en/sub-agents#run-parallel-research)). Ask for short, structured returns; see [handoff contracts](handoff-contracts.md).
- **A fresh subagent does not reuse the lead's prompt cache.** Its prefix differs, so it warms its own cache. A [fork](how-subagents-run.md#fresh-subagent-or-fork) shares the parent's system prompt and tools, so its first request reuses the parent's cache and costs less for work that needs the same context ([prompt caching](https://code.claude.com/docs/en/prompt-caching#subagents-and-the-cache)).
- **Subagent caches last five minutes by default, even on a subscription.** They sit outside the main conversation's cache lifetime. `subagentPromptCacheTtl` (`"5m"` or `"1h"`) or a subagent's `experimental.cacheTtl` frontmatter changes that; the API bills one-hour cache writes at a higher rate ([settings](https://code.claude.com/docs/en/settings-reference#subagentpromptcachettl)).
- **Agent teams cost the most.** Each teammate is a separate Claude instance with its own context window. Anthropic's cost guide says teams use approximately 7× more tokens than standard sessions when teammates run in plan mode ([costs](https://code.claude.com/docs/en/costs)).

## See the cost while you work

- **`/usage`** shows the session's token use. On Pro, Max, Ultra, Team and Enterprise plans it also attributes recent usage to subagents, skills, plugins and MCP servers as a percentage of the total, so you can see the subagent share directly.
- **`Prompt cache (main)`** in `/usage` shows the share of input tokens served from cache. It covers the main conversation only, not subagents.
- **`/tasks`** lists running subagents with the model each one runs on (and its effort, if set). Requires Claude Code v2.1.242 or later.

Source: [costs](https://code.claude.com/docs/en/costs), [subagents](https://code.claude.com/docs/en/sub-agents#check-a-subagents-model).

## Built-in limits and the caps you can set

| Limit | Default | Change it with | What happens at the limit |
|---|---|---|---|
| Nesting depth | Three layers of subagents below the main conversation | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (`1` turns nesting off) | The `Agent` tool is withheld, so the deepest subagent does its own work |
| Running at once | 20 subagents | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | Spawning fails with `Concurrent subagent limit reached` until the count drops |
| Total per session | No limit | — | — |
| Turns per subagent | None unless set | `maxTurns` in the agent file | Output returns marked as partial; Claude can resume the subagent |
| Spend per query (Agent SDK) | No limit | `max_budget_usd` (Python) or `maxBudgetUsd` (TypeScript) | No more subagents; running background subagents stop; the query ends with `error_max_budget_usd` |

Sources: [subagents](https://code.claude.com/docs/en/sub-agents#concurrent-subagent-limit), [Agent SDK: cap subagent depth, concurrency, and spend](https://code.claude.com/docs/en/agent-sdk/subagents). The concurrency limit needs Claude Code v2.1.217 or later. Agent-team teammates and workflow agents follow their own limits.

The agent descriptions themselves cost context in every session. Claude Code warns at startup when the combined descriptions of your custom subagents pass 15,000 tokens. Keep descriptions short and put detail in the body, which loads only when the subagent runs.

## A transparent arithmetic example

Suppose one request uses **10,000 uncached input tokens and 2,000 billable output tokens**, with no cache, tools, batch discount or fast mode. Using the standard rates in the [model guide](models-and-effort.md):

| Model | Input calculation | Output calculation | Hypothetical total |
|---|---|---|---|
| Haiku 5.5 | 10,000 / 1M × $0.10 | 2,000 / 1M × $0.50 | $0.002 |
| Sonnet 5.5 | 10,000 / 1M × $2.00 | 2,000 / 1M × $10.00 | $0.040 |
| Opus 5.5 | 10,000 / 1M × $4.00 | 2,000 / 1M × $20.00 | $0.080 |
| Fable 5.2 | 10,000 / 1M × $8.00 | 2,000 / 1M × $40.00 | $0.160 |

This is arithmetic, not a benchmark. Different models use different numbers of tokens for the same task, and thinking tokens bill as output. The Haiku row assumes the prompt stays at or under 100,000 tokens. Subscription limits cannot be derived from this table.

The example ignores caching, which matters a lot for agents. Claude Code caches automatically, and cache reads cost $0.20 per million on Opus 5.5 against $4.00 fresh.

## What Anthropic reports for Claude Code

Anthropic's cost guide reports that across enterprise deployments the average Claude Code cost is about **$13 per developer per active day** and $150 to $250 per developer per month, with 90% of users below $30 per active day ([costs](https://code.claude.com/docs/en/costs)). These are Anthropic's figures, not measurements by this guide.

The same guide recommends Sonnet for agent-team teammates, small teams, focused spawn prompts, shutting teammates down when done, and `model: haiku` for simple subagent tasks.

## Run a small, useful comparison

1. Pick five representative tasks: a small fix, a feature, a refactor, a hard bug and a review.
2. Fix the starting commit and write acceptance checks before running anything.
3. Run the same inputs through each candidate route, for example Opus 5.5 / medium alone versus Opus lead with Sonnet workers.
4. Record pass or fail, human rework, retries, elapsed time and billed usage, including failed runs.
5. Compare cost per **accepted** result. Keep the hard cases as regression checks.
6. Write down when the cheaper route must escalate.

The [evaluation worksheet](../templates/evaluation.csv) is intentionally empty. This guide has not invented any performance measurements.

## Keep the team efficient

- Prefer one session for short tasks or tightly ordered steps. See [when to delegate](when-to-delegate.md).
- Give each agent only the context it needs, and ask for a compact, evidence-backed return.
- Parallelize independent work when elapsed time matters, but count every agent's usage.
- Use `/clear` between unrelated tasks; stale context costs tokens on every message.
- Stop reviewing once the acceptance checks pass. Match verification to the remaining risk.
- In automation, set the depth, concurrency and spend caps above before the first run, not after the first bill.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
