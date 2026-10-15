# Team rules for delegating to subagents

Paste this section into your project's CLAUDE.md (or AGENTS.md) and edit it to fit.

## How we use the agent team

- Lead on Opus 5.5 at medium effort. Delegate only when the output will change the next action.
- Map before editing: use the explorer agent to find the relevant files.
- Use the architect agent only for ambiguous, multi-file or hard-to-reverse work.
- Give each worker agent its own files. Never let two agents edit the same file.
- Use the reviewer agent for routine changes and the auditor agent for security-sensitive, data-handling or release-blocking changes.
- A summary is not proof. Before saying a task is done, run the checks and report their actual output.
- Escalate (higher effort, then a stronger model) only after a reproduced failure, conflicting evidence or a costly consequence.
