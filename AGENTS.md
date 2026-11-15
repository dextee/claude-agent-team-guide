# Maintaining this guide

Instructions for people and coding agents working on this repository. Claude Code can read this file in place of a `CLAUDE.md`.

## Ground rules

- Tie every product fact (model ID, price, effort level, frontmatter field, CLI flag, environment variable, plugin syntax) to an official Anthropic source and a "checked on" date in [SOURCES.md](SOURCES.md). If you can't verify a number, version or quote on a primary source, leave it out. Generic and true beats specific and unverified.
- Label model-to-role assignments as this guide's recommendation. Never invent benchmark results, customer outcomes or savings.
- Keep claude.ai chat, Claude Code, the Claude API and the Agent SDK distinct. Subagent files only work in Claude Code.
- Do not touch `assets/` except through the image workflow described in [assets/README.md](assets/README.md). Every image needs descriptive alt text and honest provenance.
- Keep secrets, personal data and client data out of the repository, issues and examples.
- Write in plain English. No hype words.

## Layout rules

- `agents/` holds only the eight agent files. The plugin loads every `.md` file in that folder as an agent, so do not add a README or other Markdown there.
- The repository root is the plugin root. Do not add a root `CLAUDE.md`, `skills/`, `commands/`, `hooks/` or `bin/` unless you intend them to ship in the plugin.
- Docs pages under `docs/` start with a breadcrumb line linking to `../README.md` and end with the independent-guide footer. Non-atlas pages state the check date from `templates/models.json` in that footer.
- Every recipe and pattern has a ```` ```text ```` prompt and a `**What proves it worked:**` line.
- Model IDs, rates, effort defaults and Claude Code minimum versions live in `templates/models.json`. The validator rejects model names that are not listed there.

## Before committing

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_installer.py
bash -n install.sh
claude plugin validate . --strict   # if Claude Code is installed
```

When a model or price changes, update `templates/models.json` first, then the agent files, `docs/models-and-effort.md`, `docs/cost-and-evaluation.md`, the README 30-second table, `docs/task-selector.md`, `install.sh` `MIN_VERSION`, the SOURCES dates, the docs footers and the README badges. The validator checks rates, cost arithmetic and the minimum version against `templates/models.json`.

When you add a check to `scripts/validate.py`, add a test to `scripts/test_validate.py` that feeds it a broken input and expects an error. A check that has never failed is not known to work.

## Open owner decisions

Record decisions here when the owner makes them, so the next maintainer does not re-raise them.

- Whether to tag releases. Until tags exist, docs pin by commit SHA and the validator rejects tag refs in download URLs.
