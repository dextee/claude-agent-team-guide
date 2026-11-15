[Home](../README.md) · [Start here](start-here.md) · [How subagents run](how-subagents-run.md) · [Cost and limits](cost-and-evaluation.md)

# When to delegate, and when not to

The default is **one session**. Add a subagent when it changes the outcome, the cost or the elapsed time enough to pay for the brief, the extra requests and the handback. Checked against the [subagent reference](https://code.claude.com/docs/en/sub-agents#choose-between-subagents-and-main-conversation) and [agent teams](https://code.claude.com/docs/en/agent-teams) on **15 November 2026**.

## What Anthropic says

Use the **main conversation** when:

- the task needs frequent back-and-forth or iterative refinement;
- several phases share significant context, such as planning, implementation and testing;
- you're making a quick, targeted change;
- latency matters. A subagent that isn't a fork starts fresh and may need time to gather context.

Use **subagents** when:

- the task produces verbose output you don't need in your main context;
- you want to enforce specific tool restrictions or permissions;
- the work is self-contained and can return a summary.

For a question about something already in the conversation, `/btw` answers without tools and without adding to history. For a reusable prompt that should run in the main context, use a skill instead of a subagent.

Agent teams add coordination overhead and use significantly more tokens than a single session. Anthropic says that for sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective.

## This guide's rules of thumb

These are editorial, not Anthropic guidance.

| Delegate when… | Keep it in the lead when… |
|---|---|
| The output is large and you need only the conclusion (searches, test logs, doc fetches) | You need to see the intermediate evidence yourself to decide the next step |
| The parts are independent and can run at the same time | Each step depends on the last one's result |
| A cheaper model can do it and the result is easy to check | The work is short; a brief would take longer than doing it |
| You need a fresh, independent view (review, audit) | Several writers would touch the same files |
| A role needs restricted tools (read-only reviewer) | The task needs frequent questions to you |

**Three tests before you spawn anything:**

1. **Can I write the acceptance check now?** If not, the work is not ready to hand off. Plan first (yourself or with the architect).
2. **Will the result change my next action?** If not, skip it.
3. **Can I verify the return without redoing the work?** If not, the subagent saved you nothing.

## Pick the smallest team

| Situation | Arrangement |
|---|---|
| Small, clear edit | One Opus 5.5 session. No subagents |
| Everyday feature | Opus lead; explorer to map; reviewer to check |
| Complex feature or migration | Opus lead; architect first; workers in worktrees on separate files; independent auditor last |
| Hard bug | Opus lead at `high`; explorer for evidence; architect if hypotheses compete |
| Research decision | Opus lead; researchers split by question; editor once facts are settled |
| Large mechanical change | Architect splits by file; workers in parallel worktrees; lead integrates; reviewer on the integrated result |
| Release gate | Auditor on the final diff; you verify the real user flow |

Team sizes are hypotheses to test. Anthropic's agent-teams guidance is to start with 3 to 5 teammates for most workflows; the same caution applies to parallel subagents, because every result lands back in the lead's context.

## Copy-paste: ask the lead to decide

```text
Before delegating anything, tell me in three lines: which parts of this task
are independent, which need my input, and whether a subagent would save time
or tokens compared with doing it yourself. Only delegate the parts where the
answer is yes, and say why for each.
```

**What proves it worked:** the lead's answer names specific parts and gives a reason per delegation, and the parts it kept are ones that needed your input or shared context.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
