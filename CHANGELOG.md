# Changelog

## 3.0.0 — 2026-11-15

The guide is re-centred on running a team of subagents. Model routing becomes one chapter. Checked against official Anthropic documentation on 15 November 2026.

- **New chapters:** [start here](docs/start-here.md), [when to delegate](docs/when-to-delegate.md), [how subagents run](docs/how-subagents-run.md) (background by default, completion notifications, final-message handback, forks, `SendMessage`, resume, limits), [orchestration patterns](docs/orchestration-patterns.md) (six patterns including the three-stage audit loop), [handoff contracts](docs/handoff-contracts.md), [parallel work and worktrees](docs/parallel-work-and-worktrees.md), [gates and hooks](docs/gates-and-hooks.md), [failure modes](docs/failure-modes.md) and [agent teams](docs/agent-teams.md).
- **Agent files:** [docs/agents.md](docs/agents.md) now documents every frontmatter field in the official reference.
- **Models:** architect and auditor move from `claude-fable-5-1` to `claude-fable-5-2` (the Fable the models overview now recommends; $8 / $40 against $10 / $50). They keep `effort: high`, which is now an explicit raise over Claude Code's `medium` default for Fable 5.2. Fable 5.1 is documented as the older option.
- **Claude Code minimum:** v2.1.321 or later, the first release with Fable 5.2. The installer, README, SETUP and docs agree.
- **Agents:** the worker gains `isolation: worktree` and `maxTurns: 40`, and must report its worktree, branch and commit. The explorer gains `omitClaudeMd: true`. The auditor must check against the original brief, not the implementer's account.
- **Templates:** new [return contract](templates/return-contract.md), an example [SubagentStop gate](templates/hooks/subagent-stop-gate.sh), and [templates/models.json](templates/models.json) as the single source for model IDs, rates, effort defaults and minimum versions. Team rules, the task brief and the agent template updated.
- **Recipes:** all twelve now say what proves they worked; the refactor recipe uses worktrees and an integration step; the security recipe uses the three-stage audit loop.
- **Corrections:** advisor availability (not "Anthropic API only"), fast mode (available, not a research preview, for Opus 5.5 and Fable 5.2), the `effortLevel` fallback (does not apply from user settings to Opus 5.5 and later), `inherit` for nested subagents, the provider alias table (adds Claude Models on Google Cloud, Anthropic managed), GitHub Action quick setup (also subscriptions). The `/tasks` version note is now sourced.
- **Pinning:** the setup page pins by commit SHA. The `v2.0.0` tag example returned 404 because the repository has no tags.
- **Validator:** reads `templates/models.json`; parses agent frontmatter with a strict line parser and, when installed, PyYAML; rejects undocumented frontmatter fields and bad values; derives the minimum version from the pinned models; rejects tag refs in download URLs; rejects model names not in `templates/models.json`; checks docs footers and check dates, and that every recipe and pattern has a prompt and a proof line. Each new check has a regression test.
- **Docs:** every docs page ends with the independent-guide footer (one atlas page excepted, pending an owner decision). The atlas status labels were rechecked. A "Savings examples" row that pointed to nothing was removed from WORK_WITH_VYR.md.

## 2.0.0 — 2026-10-15

New home: `dextee/claude-agent-team-guide`. The previous repository, `dextee/claude-code-agent-team-guide`, was renamed to `dextee/vyr-agent-os-workflows` on 27 September 2026 and its guide content removed. This release restores the guide and restructures it to match the ChatGPT and Kimi guides.

- **Models:** worker moves from Sonnet 5 to Sonnet 5.5; explorer moves from Haiku 4.5 to Haiku 5.5 with `medium` effort. Architect and auditor stay on Fable 5.1; implementer stays on Opus 5.5 at `medium`.
- **Agents:** eight instead of five. Adds `reviewer`, `researcher` and `editor`. Every agent now declares an explicit `tools` list. The auditor now starts at `high` effort, Fable's default.
- **Framework:** the Quartet: map, plan, build, prove. Start in the middle, escalate on evidence.
- **Installer:** settings are untouched by default (`--with-settings` opts in). The preset now sets only `CLAUDE_CODE_SUBAGENT_MODEL`. Adds `--uninstall` backed by a hash manifest, symlink refusal, an advisory version check and a `main()` wrapper for safe piping. Requires Claude Code v2.1.293+.
- **Plugin:** the repository root is now the plugin. Marketplace renamed to `dextee-guides`: install with `claude plugin install agent-team@dextee-guides`.
- **Docs:** new 24-task selector, models and effort guide, 12 workflow recipes, cost and evaluation guide, product surfaces, and trilogy role mapping. The 14-workflow atlas moves to `docs/atlas/` with refreshed VYR status labels.
- **Checks:** `scripts/validate.py` (links, images, agent frontmatter, counts, cost arithmetic, leftover markers, credential patterns) with 19 regression tests, and 14 installer tests.
- **Removed:** unexecuted image-prompt files from the atlas and the old cover artwork.

## 1.1.0 — 2026-09-27 (previous repository)

- Upgraded lead and implementer to Opus 5.5 with `medium` effort; pinned all five agent models.
- Added the 14-workflow atlas, a model decision table and an upgrade checklist.

## 1.0.0 — 2026-09-22 (previous repository)

- Initial guide: Fable 5.1, Opus 5, Sonnet 5 and Haiku 4.5; five agents, an installer and a plugin marketplace.
