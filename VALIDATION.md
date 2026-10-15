# Verification and limits

[Home](README.md) · [Sources](SOURCES.md)

Verification date: **2026-10-15**.

## Automated local checks

| Command | What it checks |
|---|---|
| `python3 scripts/validate.py` | Every local Markdown link, image and heading anchor; alt text on images; the eight required illustrations and the 1280 × 640 social preview; agent frontmatter (`name`, `description`, `model`, `effort`, `tools`) against current model IDs and effort levels; that `agents/` holds exactly the eight agents; the README agent table and the docs/agents.md roster against the files; the Claude Code minimum version across the installer and docs; installer agent list; published rates across three documents and the cost arithmetic; 24 selector rows and 12 recipes; docs breadcrumbs; JSON validity; plugin and citation versions; VYR campaign tags; leftover markers, hype words, credential patterns and unexpected email addresses |
| `python3 scripts/test_validate.py` | 19 regression tests that alter rates, totals, token counts, agent fields, the roster, version statements and text to confirm the validator rejects each inconsistency |
| `python3 scripts/test_installer.py` | 14 installer tests in temporary folders: dry run writes nothing, including over existing agents and settings; default install leaves settings alone; repeat install is a no-op; settings merge keeps existing values; `--force` replaces only preset keys; invalid JSON stops the merge; project install backs up a changed agent; symlinked files and folders are refused; uninstall keeps edited files; uninstall still works after a release change, using the manifest; the `curl \| bash` path, with a stub `curl` that copies local files |
| `bash -n install.sh` | Installer syntax |
| `claude plugin validate . --strict` | Marketplace and plugin manifests, using Claude Code 2.1.300 |

The same checks, except the Claude CLI one, run in the GitHub Actions workflow at [.github/workflows/validate.yml](.github/workflows/validate.yml) after publishing.

## Results on 2026-10-15

| Check | Result |
|---|---|
| `scripts/test_validate.py` | 19 tests passed |
| `scripts/test_installer.py` | 14 tests passed |
| `bash -n install.sh` | Passed |
| `bash install.sh --dry-run` in an empty config folder | Listed eight additions; wrote nothing |
| `claude plugin validate . --strict` | Validation passed |
| Local plugin install in an isolated config folder | `claude plugin details agent-team` listed `Agents (8)`; about 415 always-on tokens |
| `scripts/validate.py` (strict, with all illustrations present) | Passed |

## Independent agent review

On 15 October 2026 a separate Claude subagent running Fable 5.1 audited the repository read-only. It spot-checked minimum versions, effort defaults, the subagent model order, agent precedence, `-p` billing, advisor pairings and the cost arithmetic against code.claude.com and found them correct. Its findings that were fixed:

- Recipes asked the explorer, which has no shell, to read git history and logs. The lead now runs those commands.
- `--uninstall` compared files only with the current release, so it would have kept every file after a future release. The installer now writes a hash manifest and uninstalls against it; the `curl | bash -s -- --uninstall` form is documented.
- The installer body is wrapped in `main()` so a truncated download cannot run partially, child processes get `/dev/null` as stdin, and the settings write uses a private temp file.
- A contradiction about multi-hour runs (Fable in the README, Opus in the selector), a static "passing" badge, a "read first" step that did not read anything, the advisor consent side effect, a missing fallback for accounts without Fable, the effort precedence table and missing validator cross-checks.

Adding a test for the `curl | bash` path then exposed one more bug: the cleanup trap referenced a variable local to `main()`, so every piped install exited with status 1 under `set -u`. It is fixed and covered by that test.

This is an AI-assisted review with reproducible checks, not a third-party or human security audit.

## Source review

Every model ID, price, effort level and default, frontmatter field, plugin and marketplace command, CLI flag and environment variable in this guide was checked against the official pages listed in the [source register](SOURCES.md) on 15 October 2026. Statements that could not be confirmed were removed or are marked as inference.

## What these checks do not establish

- **No live model runs.** No agent was executed against a model. The checks prove file structure, configuration consistency and installer behavior, not that your account can run each model or that a role assignment improves your results.
- **No benchmarks.** Model-to-role assignments are recommendations. The cost table is arithmetic on a hypothetical request. The evaluation worksheet is empty for your own results.
- **Not a security audit.** The installer was reviewed and tested for safe file handling, but this is not a third-party or human security audit.
- **Point in time.** Model availability, prices and Claude Code behavior can change after the verification date.

Reproduce the checks with Python 3.10 or later:

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_installer.py
```
