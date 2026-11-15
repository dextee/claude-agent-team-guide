[Home](../README.md) · [Orchestration patterns](orchestration-patterns.md) · [Agent teams](agent-teams.md)

# Parallel work and worktrees

Parallel **readers** are easy: explorers and researchers can't step on each other. Parallel **writers** are where teams break. Two agents editing one checkout can overwrite each other, run tests against each other's half-finished changes, and leave a diff no one can attribute. This page shows how to isolate writers and how to integrate their work. Checked against the [subagent reference](https://code.claude.com/docs/en/sub-agents) and [worktrees](https://code.claude.com/docs/en/worktrees) on **15 November 2026**.

## The rule: one owner per file, one checkout per writer

1. **Split by file ownership.** Ask the architect for chunks that share no files. If two chunks must touch one file, run them in sequence, not in parallel.
2. **Give each parallel writer its own worktree.** A prompt instruction such as "only edit your files" is a request; a separate checkout is a mechanism.
3. **The lead integrates and runs the full suite.** Per-chunk checks passing does not show the merged result works.

## How `isolation: worktree` behaves

This guide's [worker](../agents/worker.md) has `isolation: worktree` in its frontmatter. Claude Code then:

- runs it in a **temporary git worktree**, an isolated copy of the repository on its own branch;
- branches that worktree **from your repository's default branch, not from your current `HEAD`**, unless you set `worktree.baseRef` to `"head"`;
- runs its Bash commands inside the worktree. A command whose working directory resolves to your main checkout fails with an error, and Bash commands that redirect git into the main checkout are blocked;
- **removes the worktree automatically if the subagent made no changes.** A worktree with changes, untracked files or unpushed commits stays until a periodic sweep can remove it without losing work (after `cleanupPeriodDays`);
- loads the instruction files (CLAUDE.md and so on) from your main conversation, not from the worktree's branch.

Forks can be isolated too: when Claude spawns a fork through the Agent tool, it can pass `isolation: "worktree"` on the call.

Worktrees need a git repository. This guide has not tested the worker outside one; for a non-git project, use the implementer, or see the worktrees page on `WorktreeCreate` hooks.

### Branch from your work, not from main

If you are on a feature branch, workers that branch from `main` won't have your changes. Set this in `settings.json` (user or project):

```json
{
  "worktree": { "baseRef": "head" }
}
```

`"head"` branches from your current local `HEAD`, including unpushed commits. Uncommitted changes are not in `HEAD`, so **commit before you dispatch workers.** `worktree.baseRef` accepts only `"fresh"` (the default) or `"head"`, not a branch name.

The worker's instructions make it print its branch and last commit first, and stop if `HEAD` is not the base commit named in its brief. That turns a silent wrong base into a visible report.

## The integration step

Each worker commits in its worktree and reports its worktree path, branch and commit SHA. The lead then:

```bash
git status                       # your checkout is clean
git merge --no-ff <worker-branch-1>
git merge --no-ff <worker-branch-2>
# stop at the first conflict: it means two chunks shared a file
<your full test command>         # on the integrated result
```

Then a reviewer or a fresh auditor checks the **combined** diff against the original brief. Once merged, remove leftover worktrees with `git worktree remove <path>`; Claude Code holds a lock on a worktree while its agent runs.

### Copy-paste: dispatch and integrate

```text
Check that my working tree is clean and that worktree.baseRef is "head"
(tell me if it is not). Record HEAD as the base SHA. Use the architect
agent to split [change] into chunks that share no files. Run one worker per
chunk in parallel, each given the base SHA, its files and its check. Wait
for every worker. List each worker's branch and commit, and any that
stopped early. Merge the branches one at a time with --no-ff, stop on the
first conflict, run the full test suite, and show me the real output.
```

**What proves it worked:** `git log --oneline --graph` shows one merge per worker on top of the base SHA, no file appears in two workers' diffs, and the full suite output (not a summary of it) shows a pass on the merged commit.

## Things that defeat isolation

| Situation | What happens | Do this |
|---|---|---|
| Agent teams enabled and Claude **names** the worker | In an interactive session it launches as a teammate; frontmatter `isolation` does not prevent that, and the teammate runs in the main working directory | Leave `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` off for worktree-isolated work, or check `/tasks` |
| Worker shows the wrong base | Its branch started from `main` | Set `worktree.baseRef` to `"head"` and commit first |
| Two chunks need the same file | Merge conflict, or one change silently wins | Re-split, or run those chunks in sequence |
| Worker cannot finish within `maxTurns` | Output returns marked partial; commits may be missing | Resume it, or narrow the chunk |
| A worker edits shared config or lockfiles | Conflicts at integration | Give config and lockfiles to one owner, usually the lead |

## Subagents, agent teams, or separate sessions?

| | Subagents with worktrees | Agent teams (experimental) | Separate sessions with `--worktree` |
|---|---|---|---|
| Who coordinates | The lead session | A lead plus a shared task list; teammates message each other | You |
| Isolation | `isolation: worktree` per agent | Avoid file conflicts by splitting files; no per-teammate worktree from frontmatter | One worktree per session |
| Cost | Lower: results return to the lead | Higher: every teammate is a full instance | One full session each |
| Best for | Bounded chunks that report back | Work that needs discussion and challenge | Long-running independent streams |

Sources: [agent teams](https://code.claude.com/docs/en/agent-teams), [worktrees](https://code.claude.com/docs/en/worktrees). More in [agent teams](agent-teams.md).

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
