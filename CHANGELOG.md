# Changelog

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
