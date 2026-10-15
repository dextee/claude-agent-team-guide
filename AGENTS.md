# Maintaining this guide

Instructions for people and coding agents working on this repository. Claude Code can read this file in place of a `CLAUDE.md`.

## Ground rules

- Tie every product fact (model ID, price, effort level, frontmatter field, CLI flag, plugin syntax) to an official Anthropic source and a "checked on" date in [SOURCES.md](SOURCES.md).
- Label model-to-role assignments as this guide's recommendation. Never invent benchmark results, customer outcomes or savings.
- Keep claude.ai chat, Claude Code, the Claude API and the Agent SDK distinct. Subagent files only work in Claude Code.
- Do not touch `assets/` except through the image workflow described in [assets/README.md](assets/README.md). Every image needs descriptive alt text and honest provenance.
- Keep secrets, personal data and client data out of the repository, issues and examples.
- Write in plain English. No hype words.

## Layout rules

- `agents/` holds only the eight agent files. The plugin loads every `.md` file in that folder as an agent, so do not add a README or other Markdown there.
- The repository root is the plugin root. Do not add a root `CLAUDE.md`, `skills/`, `commands/`, `hooks/` or `bin/` unless you intend them to ship in the plugin.
- Docs pages under `docs/` start with a breadcrumb line linking to `../README.md`.

## Before committing

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_installer.py
bash -n install.sh
claude plugin validate . --strict   # if Claude Code is installed
```

When a model or price changes, update together: the agent files, `docs/models-and-effort.md`, `docs/cost-and-evaluation.md`, the README 30-second table, `docs/task-selector.md`, the SOURCES dates and the README badge. The validator cross-checks the rates and the cost arithmetic.
