# Verification and limits

[Home](README.md) · [Sources](SOURCES.md)

Latest verification: **2026-11-18**. The October checks are preserved below.

## November audit: did two named agents actually run?

Claude Code **2.1.327** loaded the local plugin with `--plugin-dir`. A disposable working folder contained just copies of [the explorer definition](agents/explorer.md) and [the CI workflow](.github/workflows/validate.yml). The lead had `Agent`, `Read`, `Glob` and `Grep`; it asked the explorer and reviewer separate questions. The CLI event stream contained both named `Agent` calls:

| Delegation observed | Evidence returned, checked against the source |
|---|---|
| `agent-team:explorer` | `agents/explorer.md` → `tools: Read, Glob, Grep` |
| `agent-team:reviewer` | `.github/workflows/validate.yml` → `run: python3 scripts/validate.py` |

The CLI returned `subtype: success`, `is_error: false`, with `claude-sonnet-5-5` and `claude-haiku-5-5` in model usage. The [first-run exercise](README.md#your-agent-team-in-60-seconds) reproduces the task interactively. Discovery and execution are different checks: `claude plugin validate . --strict --profile directory --json` returned **eight** qualified agents and **zero** directory findings. Only the two roles above were exercised against live models.

The installer audit found that the old uninstall could remove an identical file it never wrote, two writes in one second could collide on a backup, and invalid settings could leave a partial agent install. Regression tests now cover those cases, missing Python, offline removal of a retired role, and malformed or symlinked manifests. A clean-clone install no longer depends on the nonexistent `v2.0.0` tag.

## Automated local checks

| Command | What it checks |
|---|---|
| `python3 scripts/validate.py` | Every local Markdown link, image and heading anchor; alt text on images; the eight required illustrations and the 1280 × 640 social preview; agent frontmatter (`name`, `description`, `model`, `effort`, `tools`) against current model IDs and effort levels; that `agents/` holds exactly the eight agents; the README agent table and the docs/agents.md roster against the files; the Claude Code minimum version across the installer and docs; installer agent list; published rates across three documents and the cost arithmetic; 24 selector rows and 12 recipes; docs breadcrumbs; JSON validity; plugin and citation versions; VYR campaign tags; leftover markers, hype words, credential patterns and unexpected email addresses |
| `python3 scripts/test_validate.py` | 19 regression tests that alter rates, totals, token counts, agent fields, the roster, version statements and text to confirm the validator rejects each inconsistency |
| `python3 scripts/test_installer.py` | 22 installer tests in temporary folders, including ownership on uninstall, offline rollback, unique backups and settings validation before agent installation |
| `bash -n install.sh` | Installer syntax |
| `claude plugin validate . --strict --profile directory --json` | Marketplace and plugin discovery; eight qualified IDs and the directory-profile checks, using Claude Code 2.1.327 |

The [CI workflow](.github/workflows/validate.yml) runs the repository validator, both Python test suites and the shell syntax check. The strict Claude CLI discovery check and live delegation exercise were run separately. To repeat the discovery check without sending a model request:

```bash
claude plugin validate . --strict --profile directory --json
```

Look for `success: true`, an empty `directory.findings` list, and `provides.agents` containing exactly `agent-team:` followed by each of `architect`, `auditor`, `editor`, `explorer`, `implementer`, `researcher`, `reviewer` and `worker`.

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

- **Limited live coverage.** The November run exercised explorer and reviewer on a two-file reading task. It does not establish availability on another account, behavior of the other six roles or performance on a complex task.
- **No benchmarks.** Model-to-role assignments are recommendations. The cost table is arithmetic on a hypothetical request. The evaluation worksheet is empty for your own results.
- **Not a security audit.** The installer was reviewed and tested for safe file handling, but this is not a third-party or human security audit.
- **Point in time.** Model availability, prices and Claude Code behavior can change after the verification date.

Reproduce the checks with Python 3.10 or later:

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_installer.py
```
