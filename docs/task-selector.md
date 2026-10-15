[Home](../README.md) · [Models and effort](models-and-effort.md) · [Workflow recipes](workflows.md)

# Pick a model for the task

These **24 recommendations are working defaults**, inferred from Anthropic's documented model positioning and from the structure of each task. They are not Anthropic benchmark rankings. Effort is a starting value. For a tiny task, run one session and skip the agents.

| # | Task | Start with | Escalate when | Evidence of completion |
|---|---|---|---|---|
| 1 | Find files, symbols and call sites | Haiku 5.5 / medium (`explorer`) | The answer spans many systems: Sonnet 5.5 / high | Exact paths with line numbers |
| 2 | Extract fields from a clean document | Haiku 5.5 / low | Layout or meaning is ambiguous: Sonnet 5.5 / medium | Fields reconcile to the source |
| 3 | Classify or route support requests | Haiku 5.5 / low | Categories overlap or stakes rise: Sonnet 5.5 / medium | Held-out examples meet the error target |
| 4 | Apply a mechanical edit across files | Sonnet 5.5 / medium (`worker`) | Behavior changes, not just form: Opus 5.5 / medium | Intended diff only; tests pass |
| 5 | Summarize a meeting or thread | Haiku 5.5 / medium | Decisions conflict: Sonnet 5.5 / medium | Actions, owners and dates trace to the notes |
| 6 | Everyday feature implementation | Opus 5.5 / medium (`implementer`) | Architecture is unresolved: Fable 5.1 / high (`architect`) | Acceptance checks and relevant tests pass |
| 7 | Small reproduced bug | Opus 5.5 / medium | Several causes stay plausible: Opus 5.5 / high | The failing case now passes |
| 8 | Hard or intermittent bug | Opus 5.5 / high | Still unexplained after a focused attempt: Fable 5.1 / high | A causal explanation that predicts the failure |
| 9 | Production incident triage | Opus 5.5 / high | Evidence is missing: gather it before reasoning harder | Cause, recovery evidence and follow-up owner |
| 10 | Architecture or migration plan | Fable 5.1 / high (`architect`) | Constraints conflict: get a human decision | Dependencies, tradeoffs, rollback and checks |
| 11 | Large refactor split by file | Sonnet 5.5 / medium workers, Opus lead | Semantic changes emerge: Opus 5.5 / medium | Integrated result passes regression tests |
| 12 | Write or extend tests | Sonnet 5.5 / medium | The behavior under test is unclear: Opus 5.5 / medium | Tests fail before the fix and pass after |
| 13 | Routine code review | Sonnet 5.5 / high (`reviewer`) | Cross-system consequences: Fable 5.1 / high (`auditor`) | Findings with locations and repro steps |
| 14 | Security-sensitive change review | Fable 5.1 / high (`auditor`) | Specialist evidence is missing: involve a human expert | Threat assumptions and validated findings |
| 15 | Dependency or framework upgrade | Opus 5.5 / medium | Breaking changes cascade: Fable 5.1 / high to plan | Build, tests and changelog items checked |
| 16 | Research a narrow factual question | Sonnet 5.5 / high (`researcher`) | Sources disagree: Opus 5.5 / high | Current primary sources, dated |
| 17 | Synthesize a hard research question | Opus 5.5 / high | The decision is consequential: Fable 5.1 / high | Claim ledger and an uncertainty statement |
| 18 | Compare products or vendors | Sonnet 5.5 / high | The choice is costly to reverse: Fable 5.1 / high | Dated evidence against explicit criteria |
| 19 | Write docs, a README or release notes | Sonnet 5.5 / medium (`editor`) | The facts are not settled: research first | Every claim traces to code or sources |
| 20 | Draft a client proposal | Opus 5.5 / medium | Scope or delivery is unclear: Fable 5.1 / high | Scope, exclusions, costs and next step align |
| 21 | Reconcile spreadsheets or invoices | Sonnet 5.5 / high | Definitions or exceptions conflict: Opus 5.5 / high | Totals reconcile; exceptions are listed |
| 22 | Diagnose a metric change | Opus 5.5 / medium | Several explanations compete: Fable 5.1 / high | Reproducible calculations and caveats |
| 23 | Multi-hour autonomous build | Opus 5.5 / high | Evals at higher effort still fall short: Fable 5.1 | Explicit completion criteria met and verified |
| 24 | Frequent, bounded automation | Haiku 5.5 / low | Exception rate grows: Sonnet 5.5 / medium | Pass rate and per-task usage on a test set |

## Route by what makes the work hard

1. **Unclear result:** resolve requirements before dispatching anyone. The architect helps; a human decision may be needed.
2. **Clear result, repetitive work:** start small (Haiku or Sonnet) with an objective check.
3. **Several steps and judgment:** start with Opus 5.5 at `medium`.
4. **Ambiguity, hard tradeoffs, or a costly mistake:** use Fable 5.1 for the decision or the review.
5. **Missing permissions or evidence:** fix access or gather the evidence. A stronger model does not supply missing facts.

Basis: [models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) and [effort](https://platform.claude.com/docs/en/build-with-claude/effort), checked 15 October 2026. Anthropic's model selection matrix lists sub-agent tasks among Haiku 5.5's example uses and "multihour autonomous coding agents" among Opus 5.5's.
