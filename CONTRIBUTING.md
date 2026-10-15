# Contributing

Claude models, prices and Claude Code features change often, so source-backed corrections are the most valuable contribution.

## Corrections

Open an issue with the **Outdated information** template, or a pull request that:

- names the affected file and passage;
- links the official source (platform.claude.com, code.claude.com, support.claude.com, anthropic.com or github.com/anthropics); and
- states the date you checked it.

## New agents, tasks or recipes

Explain the task boundary, the model and effort you chose, the escalation trigger, and the observable check that proves the task is done. Keep each agent to one job, the cheapest model that does it well, and only the tools it needs. See [docs/agents.md](docs/agents.md#write-your-own).

Do not present one good run as a benchmark. If you propose a measured claim, include representative cases and the failures.

## Before you submit

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_installer.py   # if you changed install.sh
```

These checks use temporary folders and never call a Claude model. Say separately whether you tested the change in a real Claude Code session.

Keep private prompts, customer information and credentials out of issues and patches.
