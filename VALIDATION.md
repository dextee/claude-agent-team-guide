# Verification and limits

[Home](README.md) · [Sources](SOURCES.md)

Verification date: **2026-11-15** (guide 3.0.0).

## Automated local checks

| Command | What it checks |
|---|---|
| `python3 scripts/validate.py` | Every local Markdown link, image and heading anchor; alt text on images; the eight required illustrations and the 1280 × 640 social preview; agent frontmatter, parsed by a strict line parser and, when PyYAML is installed, by `yaml.safe_load` as a cross-check (field names against the official reference, `name` rules, model IDs against `templates/models.json`, effort, colour, `isolation`, `maxTurns`, booleans); that `agents/` holds exactly the eight agents; the README agent table and the docs/agents.md roster against the files; the installer's `MIN_VERSION` against the highest minimum among the pinned models in `templates/models.json`, and every stated team minimum against the installer; rates in three documents and the cost arithmetic against `templates/models.json`; 24 selector rows; 12 recipes and 6 patterns, each with a copy-paste prompt and a "What proves it worked" line; docs breadcrumbs, the independent-guide footer and its check date; download URLs that pin a tag instead of `main` or a commit SHA; Claude model names not listed in `templates/models.json`; JSON validity; plugin, citation and changelog versions; VYR campaign tags; leftover markers, hype words, credential patterns and unexpected email addresses |
| `python3 scripts/test_validate.py` | 39 regression tests. Each validator check is fed a broken input (wrong rate, previous Fable ID, misspelled field, bad value, invalid YAML, tag ref, invented model name, missing footer, stale date, recipe without a proof line, pattern without a prompt) and must report it. Also runs the example `SubagentStop` gate both ways (needs `jq`) |
| `python3 scripts/test_installer.py` | 14 installer tests in temporary folders: dry run writes nothing; default install leaves settings alone; repeat install is a no-op; settings merge keeps existing values; `--force` replaces only preset keys; invalid JSON stops the merge; project install backs up a changed agent; symlinked files and folders are refused; uninstall keeps edited files and still works after a release change; the `curl \| bash` path |
| `bash -n install.sh` | Installer syntax |
| `claude plugin validate . --strict` and `claude plugin validate ./agents` | Marketplace manifest and agent files, with the locally installed Claude Code |

The same checks, except the Claude CLI ones, run in the GitHub Actions workflow at [.github/workflows/validate.yml](.github/workflows/validate.yml).

## Results on 2026-11-15

| Check | Result |
|---|---|
| `scripts/validate.py` | PASS: 54 Markdown files, 367 local links and anchors, 19 image references, 8 agents (line and PyYAML parse), minimum version 2.1.321 |
| `scripts/test_validate.py` | 39 tests passed |
| `scripts/test_installer.py` | 14 tests passed |
| `bash -n install.sh` | Passed |
| `bash install.sh --dry-run` with an empty `HOME` | Listed eight additions; wrote nothing; warned that the local Claude Code 2.1.284 is below 2.1.321 |
| `claude plugin validate . --strict` (Claude Code 2.1.284) | Validation passed |
| `claude plugin validate ./agents` (Claude Code 2.1.284) | Validation passed |
| Mutation test of each new validator check, on a copy of the repository | Each of 15 deliberate breakages failed the validator with a message naming the problem; each restore passed |
| Example `SubagentStop` gate | Exit 2 on a report without the return contract, exit 0 with it, exit 0 when `stop_hook_active` is true |

## Review record, 15 November 2026

A read-only audit of 2.0.0 found that the guide taught model selection well but not how to run a team of subagents, and that several product facts had moved since 15 October: Fable 5.2 had replaced Fable 5.1 as the Fable the models overview recommends; advisor and fast-mode availability had changed; the `effortLevel` fallback no longer applied to newer models from user settings; a pinned-install example used a tag that does not exist. 3.0.0 restructures the guide around orchestration and corrects each fact against the pages in the [source register](SOURCES.md). The audit confirmed that Haiku 5.5 and the existing rates, cost figures and frontmatter fields were correct; those were kept.

This is an AI-assisted review with reproducible checks, not a third-party or human audit. A separate verification pass is expected before release.

## Earlier review, 15 October 2026

A separate Claude subagent running Fable 5.1 audited 2.0.0 read-only. Its fixed findings included recipes that asked the shell-less explorer to run git, an uninstall that ignored earlier releases, installer robustness for `curl | bash`, and missing validator cross-checks. Adding a test for the `curl | bash` path then exposed a cleanup-trap bug under `set -u`, which was fixed and is covered by that test.

## What these checks do not establish

- **No live model runs.** No agent was executed against a model, and the 3.0.0 agents were not exercised in a Claude Code session at v2.1.321 or later (the verification host ran 2.1.284). The checks prove file structure, configuration consistency and installer behavior, not that your account can run each model or that a team design improves your results.
- **No benchmarks.** Model-to-role assignments, team shapes and `maxTurns: 40` are recommendations. The cost table is arithmetic on a hypothetical request. The evaluation worksheet is empty for your own results.
- **Not a security audit.** The installer and the hook example were reviewed and tested for safe file handling, but this is not a third-party or human security audit.
- **Point in time.** Model availability, prices and Claude Code behavior can change after the verification date.

Reproduce the checks with Python 3.10 or later (PyYAML optional, `jq` for the hook test):

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_installer.py
bash -n install.sh
```
