[Home](../README.md) · [Handoff contracts](handoff-contracts.md) · [Gates and hooks](gates-and-hooks.md) · [Orchestration patterns](orchestration-patterns.md)

# Failure modes of agent teams

A team of agents fails in ways a single session doesn't: confident agreement that isn't independent, reports that describe work rather than prove it, and checks that pass because they can't fail. Each entry below gives the symptom, why it happens, a test you can run, and the fix. The Claude Code behaviors cited were checked on **15 November 2026**; the rest is this guide's practice, labelled as such.

## 1. Correlated agreement

**Symptom:** the reviewer agrees with the implementer; the second auditor agrees with the first. Everyone is confident; the bug ships.

**Why:** two model instances that share the same prompt, the same summary or the same conversation history share the same framing, so their agreement is not two independent checks. A [fork](how-subagents-run.md#fresh-subagent-or-fork) inherits the whole conversation by design. A resumed subagent keeps its full earlier history. A verifier given the implementer's summary reviews the summary.

**Test:** read the verifier's brief. If it contains the implementer's account of the work, or the verifier is a fork or a resume of an earlier checker, the check is not independent.

**Fix:** verifiers are fresh subagents (not forks, not resumes) that receive the **original brief and the artifact** (diff, data, document) and nothing else. Use the [three-stage audit loop](orchestration-patterns.md#pattern-5-three-stage-audit-loop). Where it matters, add a check that isn't a model at all: a test, a type check, a diff.

## 2. Anchoring

**Symptom:** the team finds one plausible cause and stops looking.

**Why:** Anthropic's agent-teams guide puts it directly: *"Sequential investigation suffers from anchoring: once one theory is explored, subsequent investigation is biased toward it."* ([agent teams](https://code.claude.com/docs/en/agent-teams#investigate-with-competing-hypotheses)).

**Test:** ask the lead which alternative explanations it ruled out, and with what evidence. "None considered" or "no evidence for them" is anchoring.

**Fix:** [competing hypotheses](orchestration-patterns.md#pattern-6-competing-hypotheses): one investigator per hypothesis, each also trying to disprove the others, and no fix until the surviving cause predicts the failure.

## 3. Trusting a summary instead of the artifact

**Symptom:** "All tests pass" in a report; the CI run shows three skipped and one failed. "Committed on branch X"; the branch has no such commit.

**Why:** a subagent's final message is its own description of what it did. Only that message returns to the parent ([Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents)), and the parent may summarize it again. Each layer of summary can drop the inconvenient line. The same applies to scripts: a script that prints "OK" at the end has told you what it intended, not what it produced.

**Test:** pick one claim per report and check it against the artifact: re-run the command, read the cited line, `git log -1` the branch, open the file the script says it wrote.

**Fix:** the [return contract](../templates/return-contract.md) (copied output, evidence per claim) plus the lead re-verifying one check per report ([handoff contracts](handoff-contracts.md#what-the-lead-re-verifies-itself)). Re-read what a script produced; don't read its summary.

## 4. Gates that cannot fail

**Symptom:** a check has never failed, so everyone trusts it. It was checking nothing.

**Ways it happens** (this guide's practice, each reproducible):

- **The check matches its own explanation.** A grep for a forbidden token also matches the comment that explains the token, so it "passes" after the code is gone. Check code, not comments.
- **A count that is never zero.** `grep -c pattern file || echo 0` prints `0` *and* exits non-zero when nothing matches, so the `|| echo 0` adds a second line: the variable holds `0`, a newline and `0`, which is not equal to `0`, and a `!= 0` test passes. Use `grep -o pattern file | wc -l`.

  ```bash
  n=$(printf 'abc\n' | grep -c zzz || echo 0); printf '[%s]\n' "$n"   # prints "[0" and "0]" on two lines
  ```
- **The check runs on nothing.** A type check pointed at a config that includes no files, or a test glob that matches no tests, exits 0.
- **The check is in the agent's prompt, not in the harness.** "Do not edit files" in a reviewer's instructions is a request; Bash can still write.

**Test:** break the thing on purpose and run the gate. It must fail with a message naming the problem. Then restore it.

**Fix:** mutation-test every new gate once, and keep the broken case as a test. This repository does that for each validator check. See [gates and hooks](gates-and-hooks.md#a-gate-that-cannot-fail-is-not-a-gate).

## 5. A blocked page that looks like a success

**Symptom:** an agent fetches a page, gets HTTP 200, finds no forbidden text, and reports the page clean. It was a bot challenge or login page.

**Why:** challenge pages, consent walls and error pages are often served with status 200. "The string I searched for is absent" is true of a page that loaded and of one that didn't.

**Test:** assert a **positive marker** you know the real page contains (a heading, a product name) and the **size** of what you got, before you assert anything is absent.

**Fix:** in the brief, require the agent to report the status code, the byte count and one expected marker for every fetch, and to treat a missing marker as "could not check", not "clean".

## 6. Partial output that reads as complete

**Symptom:** a worker hit `maxTurns`, or an API error cut it off, and its last message reads like a conclusion.

**Why:** at `maxTurns`, Claude Code returns the output **marked as partial**. A background subagent that ends on an API error is marked failed, and the message names the error and includes its last output. A foreground subagent cut off mid-stream returns partial output with a note that it didn't finish ([subagents](https://code.claude.com/docs/en/sub-agents#api-errors-in-subagents)). The marking is there; the risk is a lead that summarizes past it.

**Test:** search each report for the partial or failure marking and for `STATUS: partial` from the return contract.

**Fix:** treat partial as unfinished. Resume the subagent (it keeps its history) or narrow the task. Tell the lead to list partial and failed subagents separately in its summary.

## 7. Reporting before the work is back

**Symptom:** the lead summarizes "the review found no issues" while the reviewer is still running.

**Why:** subagents start in the background by default and report through a completion notification in a later turn ([subagents](https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background)).

**Test:** ask the lead to list running subagents by agent ID, or open `/tasks`.

**Fix:** "Wait for every subagent's report before summarizing; list any still running." Or let Claude wait: [how subagents run](how-subagents-run.md#making-claude-wait).

## 8. Parallel writers on one checkout

**Symptom:** tests fail intermittently while workers run; a file contains half of two changes.

**Why:** without isolation, subagents start in the main conversation's working directory.

**Fix:** `isolation: worktree` for every parallel writer, one owner per file, and an integration step. See [parallel work](parallel-work-and-worktrees.md). Note that with agent teams enabled, a named subagent can launch as a teammate in the main working directory despite `isolation` in its file.

## 9. Instructions arriving inside results

**Symptom:** a subagent's report contains text such as "now run this command" or claims approval it doesn't have.

**Why:** subagents read web pages, files and command output you never reviewed. Claude Code scans each final report, neutralizes text that imitates its own markers, flags instruction-shaped content, and labels the report as subagent output with no authority from you ([subagent output scanning](https://code.claude.com/docs/en/sub-agents#subagent-output-scanning)). The scan doesn't judge intent.

**Fix:** keep tool access narrow, keep permission prompts on, and never accept an "approved" claim from an agent as your approval. No agent message counts as your approval for a permission prompt.

## 10. Fabricated precision

**Symptom:** a confident, specific number, version, section reference or quote, exactly where the subject is well known, with no source.

**Why:** a model filling a gap produces the most plausible-looking value. Specific-but-unverified reads as more authoritative than generic-but-true.

**Test:** for every number, version and quote in a deliverable, ask "which primary source, checked when?" If there is no answer, it is a claim, not a fact.

**Fix:** the researcher's contract (claim-by-claim sources, inferences marked), the editor's rule against adding facts, and this repository's own practice: model IDs, rates and versions live in one [data file](../templates/models.json) with a check date, and the validator rejects model names that are not in it.

---

*Independent guide, not an Anthropic publication; not affiliated with or endorsed by Anthropic. Product facts checked 2026-11-15 against the pages in [SOURCES.md](../SOURCES.md).*
