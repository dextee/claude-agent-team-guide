[Home](../README.md) · [The eight agents](agents.md) · [Models and effort](models-and-effort.md)

# Across the trilogy: ChatGPT, Kimi and Claude

This guide is one of three that share a role spine: architect, implementer, worker, explorer, reviewer and auditor. If you already use the [ChatGPT Agent Team Guide](https://github.com/dextee/chatgpt-agent-team-guide) or the [Kimi Agent Team Guide](https://github.com/dextee/kimi-agent-team-guide), these tables map their roles and controls onto Claude Code.

The ChatGPT and Kimi columns are taken from those guides' own READMEs (checked by their authors on 6 October and 10 October 2026). The Claude column was checked on 15 October 2026. Model assignments in all three are editorial starting points. **No equivalence between vendors' models is claimed.**

## Role mapping

| Role | ChatGPT guide (Codex) | Kimi guide (Kimi Code) | This guide (Claude Code) |
|---|---|---|---|
| Architect | GPT-6 Astra / high | K3 / max | Fable 5.1 / high |
| Implementer | GPT-6.1 Sol / medium | kimi-for-coding / high | Opus 5.5 / medium |
| Worker | GPT-6 Luna / medium | kimi-for-coding-highspeed loop | Sonnet 5.5 / medium |
| Explorer | GPT-6 Luna / high | kimi-for-coding / low | Haiku 5.5 / medium |
| Reviewer | GPT-6.1 Sol / high | kimi-for-coding / high | Sonnet 5.5 / high |
| Auditor | GPT-6 Astra / high | K3 / max | Fable 5.1 / high |
| Researcher | GPT-6.1 Sol / high | kimi-for-coding / high | Sonnet 5.5 / high |
| Editor | GPT-6.1 Sol / medium | kimi-for-coding / low | Sonnet 5.5 / medium |
| Visual director | GPT-6.1 Sol / medium + image tool | Not ported | Not ported; Claude models do not generate images |
| Everyday lead | Sol / medium | kimi-for-coding / high | Opus 5.5 / medium |

## Lever mapping

| Concept | ChatGPT guide (Codex) | Kimi guide (Kimi Code) | Claude Code |
|---|---|---|---|
| Agent file | TOML custom agent | Markdown with YAML frontmatter | Markdown with YAML frontmatter |
| Per-agent model pin | `model` field | Not supported; session `/model` and a model pool | `model` field: alias or full ID |
| Per-agent reasoning control | `model_reasoning_effort` | Per session, not per file | `effort` field: `low` to `max` |
| Session model switch | `codex -m` | `/model` | `/model`, `claude --model` |
| Session effort | `-c model_reasoning_effort=…` | Thinking effort `low` / `high` / `max` | `/effort`, `claude --effort` |
| Tool permissions per agent | Sandbox setting | `tools` / `disallowedTools` | `tools` / `disallowedTools` |
| Project install path | `.codex/agents/` | `.kimi-code/agents/` | `.claude/agents/` |
| User install path | `~/.codex/agents/` | `~/.kimi-code/agents/` | `~/.claude/agents/` |
| Packaged distribution | Installer script | Copy files | Installer script or plugin marketplace |
| See which model ran | `/agent` in the CLI | See the Kimi guide | `/tasks` |
| Second-opinion pattern | Delegate to the architect | Read-only reviewer agents | Experimental `/advisor`, or the auditor agent |
| Many full sessions | Not covered | Not covered | Experimental agent teams |

## What changes conceptually

**From Codex:** the closest match. Both pin a model and a reasoning level per file. Two differences: Claude Code agent files use YAML frontmatter plus a Markdown prompt body, and a model that Claude passes when it spawns an agent outranks the file's `model` field. Check `/tasks` to see what actually ran.

**From Kimi Code:** Claude Code agent files *can* pin a model, so the "promote the architect to the flagship by convention" step becomes a single `model:` line. Kimi's built-in `explore` and `plan` sub-agents correspond to Claude Code's built-in Explore and Plan agents, which inherit the main conversation's model. This guide's `explorer` pins Haiku 5.5 instead.

**Shared spine:** all three guides keep the same discipline. Define the outcome and acceptance checks first, explore before editing, escalate on ambiguity or consequence, and verify the actual result rather than an agent's summary of it.

## Links to update when sharing

The earlier Claude guide lived at `dextee/claude-code-agent-team-guide`. That name now redirects to the [VYR Agent OS showcase](https://github.com/dextee/vyr-agent-os-workflows), and the guide content was removed there. This repository is its replacement. Link to `https://github.com/dextee/claude-agent-team-guide`.
