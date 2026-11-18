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

- The team needs **Claude Code v2.1.293 or later**. That is the first release with Haiku 5.5. Opus 5.5 needs v2.1.280, Sonnet 5.5 needs v2.1.284 and Fable 5.1 needs v2.1.257 ([model configuration](https://code.claude.com/docs/en/model-config)). Upgrade with `claude update`, then start a new session.
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

- Copies eight Markdown files. It skips identical files and saves a changed file under a unique `<name>.md.bak-*` name before replacing it.
- Refuses to write through a symlinked agents folder or agent file.
- Leaves `settings.json` alone unless you pass `--with-settings`.
- Checks your Claude Code version and warns if it is older than v2.1.293. It does not call any model.
- Records the hash of each file it wrote in `.agent-team-manifest` in the agents folder, so `--uninstall` can tell your edits apart from its own files, even after later releases.
- Downloads from the moving `main` branch when run through `curl`. For a reproducible install, use a checkout: the script and all eight definitions then come from the same commit. Record the full commit ID during review. The commands below stop if cloning or checkout fails:

```bash
git clone https://github.com/dextee/claude-agent-team-guide.git pinned-agent-team &&
(
  cd pinned-agent-team &&
  ref=$(git rev-parse --verify HEAD) &&
  git switch --detach "$ref" &&
  printf 'Record this commit: %s\n' "$ref" &&
  bash install.sh --dry-run
)
```

After reviewing the preview, run `bash pinned-agent-team/install.sh`. On another machine, check out the recorded full commit ID before running the script.

### Optional settings preset

`--with-settings` merges one key into your user `settings.json`, keeping any value you already set:

```json
{
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5-5" }
}
```

This makes subagents and agent-team teammates that have no model of their own default to Sonnet 5.5 instead of your main model. The eight agents here pin their own models, so it does not change them. Anthropic's cost guide recommends Sonnet for teammates ([costs](https://code.claude.com/docs/en/costs)). Skip it if you prefer subagents to inherit your main model.

## 3. Verify

For a **user or project file install**, check the files at that scope:

```bash
AGENTS_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/agents"   # or <project>/.claude/agents for option B
ls "$AGENTS_DIR"
grep -H '^model:' "$AGENTS_DIR"/{architect,implementer,worker,explorer,reviewer,auditor,researcher,editor}.md
```

Expected models: architect and auditor `claude-fable-5-1`; implementer `claude-opus-5-5`; worker, reviewer, researcher and editor `claude-sonnet-5-5`; explorer `claude-haiku-5-5`.

For a **marketplace plugin install**, skip the file checks above. Use `claude plugin details agent-team` to check the eight agents; use the qualified name `agent-team:explorer` rather than a bare `explorer` that could resolve to a separate file install. To update later: `claude plugin marketplace update dextee-guides`, then `claude plugin update agent-team@dextee-guides`.

Then start a new session in a project and ask:

```text
Use the explorer agent to find the project's test command in a file.
Quote the command and cite its file and line, or say you could not find it.
Do not run it or edit anything.
```

Run `/tasks` while it works. Claude Code names each subagent's model and effort there (v2.1.242 or later). Claude Code picks up new agent files within a few seconds; if the `agents` folder was created during the session, restart the session ([Agent SDK troubleshooting](https://code.claude.com/docs/en/agent-sdk/subagents)).

For the plugin route use `agent-team:explorer` in the prompt above. Check the named delegation as well as the answer. The [two-agent exercise](README.md#your-agent-team-in-60-seconds) has known answers you can compare against the source. A successful explorer run does not establish access to the other pinned models.

## 4. Tell the user what is left

Report what was installed, what changed and where backups were saved. Then pass on these notes:

1. **Fable and usage credits.** On some plans and seat tiers, Fable usage bills to usage credits. Claude Code asks for consent in interactive sessions before the first such request. In non-interactive `claude -p` runs and Agent SDK apps that do not show the prompt, it bills without asking ([model configuration](https://code.claude.com/docs/en/model-config)). The architect and auditor run Fable. Do not accept this prompt for the user.
2. **Effort overrides.** If `CLAUDE_CODE_EFFORT_LEVEL` is set, it overrides the `effort` in every agent file. Unset it to use the per-agent levels.
3. **Model overrides.** `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes every subagent use `CLAUDE_CODE_SUBAGENT_MODEL`, overriding the pinned models.
4. **How to use it:** "Use the architect agent to plan X, the implementer to build it, then the reviewer to check the diff."

## 5. Third-party providers

The agent files use Anthropic API model IDs. On Amazon Bedrock and Google Cloud, Claude Code maps an Anthropic model ID to the provider's ID for that version when the provider supports it. On Microsoft Foundry, deployment names are your own ([model configuration](https://code.claude.com/docs/en/model-config)). For each agent:

- Confirm the pinned model is enabled in your account and region.
- If not, change the `model:` line to a model you can use, or use `modelOverrides` in settings to map the Anthropic ID to your provider ID.
- Neither advisor nor fast mode is required. Check [provider-specific support](docs/product-surfaces.md#third-party-providers) if you want to use them.

**No Fable access on any provider?** If `/model` does not list Fable, change `model:` to `claude-opus-5-5` in `architect.md` and `auditor.md`.

## Optional: add an advisor

The [advisor tool](https://code.claude.com/docs/en/advisor) lets the main model consult another model at decision points. It is experimental, adds usage and requires a supported provider and model pairing.

```text
/advisor opus      # a second Opus reviews key decisions
/advisor fable     # requires Fable access; see the note below
/advisor off
```

On plans where Fable bills to usage credits, `/advisor fable` first needs the one-time consent you give through `/model fable`. That also switches your main model to Fable, and a Fable main model accepts only a Fable advisor, so run `/model opus` afterwards to return to Opus 5.5. Subagents inherit the configured advisor when their own model allows the pairing, which adds advisor usage to delegated work too ([advisor](https://code.claude.com/docs/en/advisor)).

## Rollback

```bash
bash install.sh --uninstall            # user scope, from a clone
bash install.sh --uninstall --project /path/to/project

# without a clone
curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh | bash -s -- --uninstall
```

Uninstall removes only files recorded in its manifest that still match their recorded hash. Edited files and unowned files are kept. Without a manifest it leaves the agents alone. Add `--dry-run` to preview. To restore a replaced file, rename its `.bak-*` copy back to `<name>.md`. If you used `--with-settings`, compare your current `settings.json` with its backup before restoring the previous value.

Upgrading from the October installer? Its manifest could include identical files you already owned. Preview uninstall and keep a copy of any such file before removing that older installation.

For the plugin: `claude plugin uninstall agent-team@dextee-guides`, or `claude plugin marketplace remove dextee-guides` to remove the marketplace and its plugins.

## What was tested here

The installer's behavior is covered by [filesystem tests](scripts/test_installer.py) in temporary folders. Claude Code discovered all eight plugin roles, and a live run returned source evidence from the explorer and reviewer. See [validation](VALIDATION.md) for the checks and limits.
