# Team rules for delegating to subagents

Paste this section into your project's CLAUDE.md (or AGENTS.md) and edit it to fit. Subagents load CLAUDE.md too (except the explorer here, which sets `omitClaudeMd: true`), so these rules reach most of the team.

## How we use the agent team

- Lead on Opus 5.5 at medium effort. Delegate only when the output will change the next action.
- Subagents start in the background. Wait for every subagent's report before summarizing, and say which are still running.
- Every brief includes the outcome, the files, the base commit SHA and the acceptance check. A subagent sees only its brief.
- Every report ends with the return contract: STATUS, RESULT, EVIDENCE, CHECKS RUN (with real output), NOT CHECKED, CHANGED, OPEN.
- Map before editing: use the explorer agent to find the relevant files. Restate path rules in its request.
- Use the architect agent only for ambiguous, multi-file or hard-to-reverse work.
- One owner per file. Parallel writers use the worker agent, which runs in its own git worktree. Commit before dispatching workers. The lead merges their branches and runs the full suite.
- Reviewers and auditors are fresh subagents, never forks or resumes of the agent that did the work. Give them the original requirements and the diff, not the implementer's summary.
- For consequential changes, run the three-stage loop: auditor, implementer, then a different fresh auditor with the original brief.
- A summary is not proof. Before saying a task is done, re-run the acceptance check and show its actual output.
- A report marked partial, or that names a fallback model, is unfinished or needs re-checking.
- Escalate (higher effort, then a stronger model) only after a reproduced failure, conflicting evidence or a costly consequence.
