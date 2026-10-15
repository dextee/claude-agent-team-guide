[Home](../README.md) · [Task selector](task-selector.md) · [Delegation template](../templates/task-brief.md)

# Twelve workflows with useful handoffs

These recipes are editorial starting points that use [the eight installed agents](agents.md). With the plugin install, prefix names with `agent-team:`, for example `agent-team:reviewer`. Outside Claude Code, run the stages one after another ([product surfaces](product-surfaces.md)).

Illustrations are conceptual artwork, not screenshots or evidence of completed work. [Provenance](../assets/README.md).

## 1. Deliver a feature

<img src="../assets/images/workflow-coding.png" alt="Ivory and terracotta blocks being assembled into a modular structure, with a brass jig placing a charcoal block and a spirit level beside it" width="100%">

**Lead:** Opus 5.5 / medium. **Team:** explorer, implementer, reviewer; architect only if the design is unresolved.

```text
Build [feature]. Success means [observable behavior].
Use the explorer agent to find the responsible files and existing tests.
If the approach is unclear, use the architect agent to plan it with
acceptance checks. Have the implementer build it and run the tests, then
ask the reviewer to check the diff against the plan. Fix material findings.
Return the changed files, the checks run and any remaining limits.
```

**Done means:** the requested behavior works, nearby behavior still works, and verification covers the actual change. A passing build alone does not show the user flow works.

## 2. Investigate a hard bug

**Lead:** Opus 5.5 / high. **Team:** explorer for evidence; architect when hypotheses compete.

```text
Investigate [failure]. Reproduction: [steps]. Expected: [behavior].
Separate observations from hypotheses. Use the explorer agent to collect
evidence for each hypothesis. If two or more remain plausible, ask the
architect agent which evidence would distinguish them. Fix only the proven
cause. Show the reproduction now passes and check the closest regression.
```

**Handoff:** the evidence must explain why the cause predicts the observed failure. Do not keep a speculative patch because unrelated tests passed.

## 3. Run a large refactor

**Lead:** Opus 5.5 / medium. **Team:** architect splits work; workers own disjoint files; reviewer checks the integrated result.

```text
Refactor [area] while preserving [public behavior]. Record the base commit
and the acceptance tests. Use the architect agent to split the work into
chunks with no shared files. Run one worker agent per chunk in parallel.
Integrate the results yourself, run the full test suite, then ask the
reviewer agent to check the combined diff.
```

**Done means:** the merged state passes. Separate chunk checks do not prove the integrated result works. If a worker runs with `isolation: worktree`, its branch starts from your default branch, not your current `HEAD` ([subagent docs](https://code.claude.com/docs/en/sub-agents)).

## 4. Review before merge

<img src="../assets/images/workflow-review.png" alt="A finished model bridge on a pedestal beside a separate inspection table with a brass loupe, calipers and evidence cards" width="100%">

**Lead:** Opus 5.5 / medium. **Team:** reviewer for routine changes; auditor for consequential ones.

```text
Review [branch or PR] against [requirements]. Use the reviewer agent for a
routine pass. If the change touches authentication, payments, data
deletion, migrations or public APIs, use the auditor agent instead.
Report only findings with a file and line or a reproducing command.
Then tell me which requirements were verified and which were not checked.
```

**Done means:** every requirement has evidence at the candidate commit. "No issues found" is not the same as full coverage.

## 5. Ship a security-sensitive change

**Lead:** Opus 5.5 / high. **Team:** architect states threat assumptions; implementer builds; auditor reviews.

```text
Change [component] to [goal]. First, use the architect agent to list the
threat assumptions, trust boundaries and abuse cases, with a test for each.
Have the implementer build the change and those tests. Then use the
auditor agent to review the diff against the threat list. Do not mark this
done until every listed abuse case has a passing test or a stated reason.
```

**Done means:** the abuse cases are tested. An AI review is not a substitute for a human security review where your policy requires one.

## 6. Produce a research decision brief

<img src="../assets/images/workflow-research.png" alt="Open books and loose papers feeding gold threads through a brass reading lens toward a small tied stack of finding cards" width="100%">

**Lead:** Opus 5.5 / high. **Team:** researchers split by question, then the editor.

```text
Research [decision] for [audience], judged on [criteria]. Split it into
independent questions and run one researcher agent per question in
parallel. Each must return dated primary sources and mark inferences.
Reconcile conflicts yourself. Then have the editor agent write a one-page
brief: recommendation, strongest alternative, and what evidence would
change the choice.
```

**Done means:** each criterion is covered, key claims have reachable citations, and the brief separates evidence from inference.

## 7. Write documentation from the code

<img src="../assets/images/workflow-docs.png" alt="An open blank book with a terracotta spine, gathered paper signatures, finished books, thread and a brass fountain pen" width="100%">

**Lead:** Sonnet 5.5 / medium, or Opus 5.5 for large systems. **Team:** explorer, then editor.

```text
Write [README / setup guide / API reference] for [audience]. Use the
explorer agent to collect the real commands, configuration keys, defaults
and file paths. Have the editor agent write from that evidence only. Run
every command in the document that is safe to run, and list any you could
not verify.
```

**Done means:** every command and setting traces to the code, and the safe ones were run.

## 8. Prepare release notes

**Lead:** Sonnet 5.5 / medium. **Team:** the lead gathers git history; explorer reads changed files; editor writes.

```text
Draft release notes for [version] from [base tag] to [head]. Run
`git log --oneline [base]..[head]` and `git diff --stat [base]..[head]`
yourself. Pass the output to the explorer agent and have it read the
changed files to group changes as features, fixes, breaking changes and
security. Have the editor agent write user-facing notes. Mark any change
whose impact you could not confirm from the code.
```

The explorer has Read, Glob and Grep only, so it cannot run git. The lead runs commands and hands over the output.

**Done means:** every line maps to a commit, and breaking changes include the migration step.

## 9. Triage an incident

<img src="../assets/images/workflow-ops.png" alt="Brass gauges with blank faces, a terracotta valve wheel, coiled cable and a rack of checklist cards on a charcoal console" width="100%">

**Lead:** Opus 5.5 / high. **Team:** explorer for code and config in the repo; reviewer for read-only commands; one owner for remediation.

```text
Users report [symptom] since [time]. Export the relevant logs to
[path] first. In parallel, use the explorer agent to read [path] and the
config files changed recently, and the reviewer agent to run read-only
commands such as `git log --since="[time]"`. Build a timeline. Propose the most likely cause and the cheapest safe mitigation.
Do not change production. List the commands you would run and wait for my
approval before any of them.
```

**Ownership:** one agent or person owns each live system. Parallel agents gather evidence; they do not act on production at the same time.

## 10. Upgrade a dependency

**Lead:** Opus 5.5 / medium. **Team:** researcher reads the upgrade notes; implementer upgrades; reviewer checks.

```text
Upgrade [package] from [old] to [new]. Use the researcher agent to collect
the official migration notes and breaking changes. Use the explorer agent
to find every affected call site. Have the implementer make the upgrade and
fix breakages, then run the full test suite. Ask the reviewer to check for
behavior changes the tests would not catch.
```

**Done means:** build and tests pass, and each breaking change in the notes is either handled or shown not to apply.

## 11. Reconcile data or invoices

**Lead:** Sonnet 5.5 / high. **Team:** Haiku extraction for clean fields; Opus 5.5 if definitions conflict.

```text
Reconcile [source A] and [source B]. Keep the originals unchanged. State
the matching keys and definitions. Separate confirmed matches, duplicates,
missing records and unresolved differences. Recalculate totals from the
underlying records. Explain every remaining difference; never treat
missing data as zero.
```

**Done means:** totals reconcile, or every difference is explained. A formatted spreadsheet is not the verification.

## 12. Cut the cost of a recurring workflow

**Lead:** Opus 5.5 / medium for evaluation design. **Candidate:** Sonnet 5.5 or Haiku 5.5 at lower effort.

```text
Compare [current route] with [cheaper route] on the same [N] representative
cases. Write acceptance checks before running. Record pass or fail,
retries, elapsed time and token usage for each case. Keep the cheaper
route only if it meets the quality bar, and define which cases must still
go to the stronger model.
```

**Done means:** the choice rests on measured, completed-task results. Include the current model at a lower effort as one candidate; Anthropic notes that tuning effort is often a better lever than switching models. [Evaluation worksheet](../templates/evaluation.csv) · [Cost guide](cost-and-evaluation.md).
