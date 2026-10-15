---
name: your-agent-name
description: One sentence on what it does and when Claude should use it. Say "Read-only." if it never edits.
model: claude-sonnet-5-5
effort: medium
tools: Read, Glob, Grep
---

You are the [role]. Your job is [one job].

- [The most important rule]
- [What evidence it must cite]
- [What it must not do]

Your final message is the only thing the caller receives. Return: [the exact contents the caller needs].
