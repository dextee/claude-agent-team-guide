# Set up the Claude Code agent team

[Home](README.md) · [The eight agents](docs/agents.md) · [Product surfaces](docs/product-surfaces.md)

> **For humans:** on a new machine, open Claude Code and say:
>
> ```text
> Set up my Claude Code agent team by following
> https://github.com/dextee/claude-agent-team-guide/blob/main/SETUP.md
> ```
>
> Claude reads this file and walks through it with you. To do it yourself, run:
>
> ```bash
> curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh | bash
> ```

---

**Claude, when a user asks you to set up their agent team from this file, follow these steps in order. Show the user each command and its output. Do not skip the checks, and do not accept billing prompts on the user's behalf.**

## 1. Check the environment

```bash
claude --version
command -v curl python3
ls ~/.claude/agents 2>/dev/null
```

- The team needs **Claude Code v2.1.321 or later**. That is the first release with Fable 5.2, which the architect and auditor use. Haiku 5.5 needs v2.1.293, Sonnet 5.5 needs v2.1.284 and Opus 5.5 needs v2.1.280 ([model configuration](https://code.claude.com/docs/en/model-config)). Upgrade with `claude update`, then start a new session. If you can't upgrade, see step 5's fallback.
- If `CLAUDE_CONFIG_DIR` is set, Claude Code keeps its configuration there instead of `~/.claude`. The installer follows the same variable.
- Note any existing files named `architect.md`, `implementer.md`, `worker.md`, `explorer.md`, `reviewer.md`, `auditor.md`, `researcher.md` or `editor.md`. The installer backs them up before replacing them.
- `python3` is only needed for the optional settings merge.

## 2. Pick the install type

If the user has not said, use option A.

| Situation | Command |
|---|---|
| **A. Personal machine (default).** Agents for every project | `curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh \| bash` |
| **B. One project, shared through git.** Agents in `.claude/agents/` | `curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh \| bash -s -- --project .` |
| **C. Plugin.** Namespaced agents that update with the plugin | `claude plugin marketplace add dextee/claude-agent-team-guide` then `claude plugin install agent-team@dextee-guides` |
| **D. Amazon Bedrock, Google Cloud, Microsoft Foundry or Claude Platform on AWS** | Option A or B, then step 5 |

Add `--dry-run` first when the user wants a preview. Pass `--with-settings` only if the user asks for the optional preset below. Use `--force` only when the user explicitly wants to replace conflicting preset values.

Plugin agents appear with a prefix, such as `agent-team:auditor`. Pick one method. If the same name exists at more than one level, Claude Code uses the higher-priority copy: project `.claude/agents/` beats user `~/.claude/agents/`, which beats plugin agents ([subagent docs](https://code.claude.com/docs/en/sub-agents)).

### What the installer does

- Copies eight Markdown files. It skips identical files and saves a changed file as `<name>.md.bak-<timestamp>` before replacing it.
- Refuses to write through a symlinked agents folder or agent file.
- Leaves `settings.json` alone unless you pass `--with-settings`.
- Checks your Claude Code version and warns if it is older than the team's minimum. It does not call any model.
- Records the hash of each file it wrote in `.agent-team-manifest` in the agents folder, so `--uninstall` can tell your edits apart from its own files, even after later releases.
- Downloads from the `main` branch when run through `curl`. To pin an exact version, use a full commit SHA. Fetch the installer from that commit and set the same SHA on the `bash` side of the pipe, so the agent files come from it too:

```bash
SHA="$(git ls-remote https://github.com/dextee/claude-agent-team-guide.git refs/heads/main | cut -f1)"
echo "$SHA"    # record it; this is the version you are pinning
curl -fsSL "https://raw.githubusercontent.com/dextee/claude-agent-team-guide/$SHA/install.sh" | AGENT_TEAM_REF="$SHA" bash
```

The repository has no release tags yet, so pin by commit SHA rather than a tag name.

### Optional settings preset

`--with-settings` merges one key into your user `settings.json`, keeping any value you already set:

```json
{
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5-5" }
}
```

This makes subagents and agent-team teammates that have no model of their own default to Sonnet 5.5 instead of your main model. The eight agents here pin their own models, so it does not change them. Anthropic's cost guide recommends Sonnet for teammates ([costs](https://code.claude.com/docs/en/costs)). Skip it if you prefer subagents to inherit your main model.

## 3. Verify

```bash
AGENTS_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/agents"   # or <project>/.claude/agents for option B
ls "$AGENTS_DIR"
grep -H '^model:' "$AGENTS_DIR"/{architect,implementer,worker,explorer,reviewer,auditor,researcher,editor}.md
```

Expected models: architect and auditor `claude-fable-5-2`; implementer `claude-opus-5-5`; worker, reviewer, researcher and editor `claude-sonnet-5-5`; explorer `claude-haiku-5-5`. The worker also has `isolation: worktree` and `maxTurns: 40`; the explorer has `omitClaudeMd: true`.

For the plugin route, `claude plugin details agent-team` lists `Agents (8)`. To update later: `claude plugin marketplace update dextee-guides`, then `claude plugin update agent-team@dextee-guides`.

Then start a new session in a project and ask:

```text
Use the explorer agent to list this project's entry points and test commands.
Return file paths only. Make no edits.
```

Run `/tasks` while it works. Claude Code names each subagent's model there, and its effort if set; this needs v2.1.242 or later ([subagents](https://code.claude.com/docs/en/sub-agents#check-a-subagents-model)). The subagent starts in the background, so its report arrives in a later turn. Claude Code picks up new agent files within a few seconds; if the `agents` folder was created during the session, restart the session ([subagents](https://code.claude.com/docs/en/sub-agents#write-subagent-files)).

Installing files proves only that the files are in place. It does not prove your account can run each model.

## 4. Tell the user what is left

Report what was installed, what changed and where backups were saved. Then pass on these notes:

1. **Fable and usage credits.** On some plans and seat tiers, Fable usage bills to usage credits. Claude Code asks for consent in interactive sessions before the first such request. In non-interactive `claude -p` runs and Agent SDK apps that do not show the prompt, it bills without asking ([model configuration](https://code.claude.com/docs/en/model-config)). The architect and auditor run Fable. Do not accept this prompt for the user.
2. **Effort overrides.** If `CLAUDE_CODE_EFFORT_LEVEL` is set, it overrides the `effort` in every agent file. Unset it to use the per-agent levels.
3. **Model overrides.** `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes every subagent use `CLAUDE_CODE_SUBAGENT_MODEL`, overriding the pinned models.
4. **Worker worktrees.** The worker runs in its own git worktree, branched from the repository's default branch unless `worktree.baseRef` is `"head"` in settings. Users on feature branches should set it and commit before dispatching workers ([parallel work](docs/parallel-work-and-worktrees.md)).
5. **Agent teams.** If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set, a subagent Claude names can launch as a teammate instead, which ignores the worker's worktree isolation.
6. **How to use it:** start with [docs/start-here.md](docs/start-here.md), or: "Use the architect agent to plan X, the implementer to build it, then a fresh reviewer to check the diff against my request."

## 5. Third-party providers

The agent files use Anthropic API model IDs. On Amazon Bedrock and Google Cloud, Claude Code maps an Anthropic model ID to the provider's ID for that version when the provider supports it. On Microsoft Foundry, deployment names are your own ([model configuration](https://code.claude.com/docs/en/model-config)). For each agent:

- Confirm the pinned model is enabled in your account and region.
- If not, change the `model:` line to a model you can use, or use `modelOverrides` in settings to map the Anthropic ID to your provider ID.
- The advisor works on Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed) from Claude Code v2.1.300, but not on Amazon Bedrock, Google Cloud's Agent Platform or Microsoft Foundry. Fast mode in Claude Code is not available on Bedrock, Foundry or Claude Platform on AWS; on Google Cloud's Agent Platform it works for Fable 5.2 with conditions ([advisor](https://code.claude.com/docs/en/advisor), [fast mode](https://code.claude.com/docs/en/fast-mode)).

**No Fable 5.2?** If `/model` does not list Fable, or your Claude Code is older than v2.1.321 and can't be upgraded, change `model:` in `architect.md` and `auditor.md` to `claude-fable-5-1` (needs v2.1.257) or `claude-opus-5-5` (raise `effort` to `high` or `xhigh` if you need more depth).

## Optional: add an advisor

The [advisor tool](https://code.claude.com/docs/en/advisor) lets the main model consult a stronger model at decision points. It is experimental and adds usage. It works on the Anthropic API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed), the last two from Claude Code v2.1.300; not on Amazon Bedrock, Google Cloud's Agent Platform or Microsoft Foundry. With Opus 5.5 as the main model, accepted advisors are Fable or Opus 5 and later.

```text
/advisor opus      # a second Opus reviews key decisions
/advisor fable     # requires Fable access; see the note below
/advisor off
```

On plans where Fable bills to usage credits, `/advisor fable` first needs the one-time consent you give through `/model fable`. That also switches your main model to Fable 5.2, and a Fable 5.2 main model accepts only a Fable 5.2 advisor, so run `/model opus` afterwards to return to Opus 5.5. Subagents inherit the configured advisor when their own model allows the pairing, which adds advisor usage to delegated work too ([advisor](https://code.claude.com/docs/en/advisor)).

## Rollback

```bash
bash install.sh --uninstall            # user scope, from a clone
bash install.sh --uninstall --project /path/to/project

# without a clone
curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh | bash -s -- --uninstall
```

Uninstall removes only files whose content still matches what the installer wrote (from its manifest) or the current release. Edited files are kept and listed. Add `--dry-run` to preview. To restore a replaced file, rename its `.bak-<timestamp>` copy back to `<name>.md`. If you used `--with-settings`, restore `settings.json` from its `.bak-<timestamp>` copy or delete the `CLAUDE_CODE_SUBAGENT_MODEL` key.

For the plugin: `claude plugin uninstall agent-team@dextee-guides`, or `claude plugin marketplace remove dextee-guides` to remove the marketplace and its plugins.

## What was tested here

The installer's behavior is covered by [filesystem tests](scripts/test_installer.py) in temporary folders. No live model runs were part of these checks, and the 3.0.0 changes were not exercised in a Claude Code session at v2.1.321 or later. See [validation](VALIDATION.md).
