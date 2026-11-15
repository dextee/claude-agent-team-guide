#!/usr/bin/env bash
# Example SubagentStop gate for the Claude Code Agent Team Guide.
# https://github.com/dextee/claude-agent-team-guide/blob/main/docs/gates-and-hooks.md
#
# Claude Code runs this when a subagent finishes and passes JSON on stdin.
# Exit 0 lets the subagent stop. Exit 2 keeps it running and delivers stderr
# to the subagent as its next instruction (hooks reference, SubagentStop).
#
# This gate refuses to let a subagent stop until its final message follows
# templates/return-contract.md: a STATUS line and a CHECKS RUN section.
# Requires jq.
#
# Wire it up in settings.json (see docs/gates-and-hooks.md):
#   "hooks": { "SubagentStop": [ { "matcher": "^(implementer|worker)$",
#     "hooks": [ { "type": "command",
#       "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/subagent-stop-gate.sh" } ] } ] }

set -euo pipefail

input="$(cat)"

# Loop guard: stop_hook_active is true when the subagent is already continuing
# because of a stop hook. Let it stop rather than block forever.
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi

message="$(printf '%s' "$input" | jq -r '.last_assistant_message // ""')"

missing=()
printf '%s\n' "$message" | grep -Eq '^STATUS: (done|partial|blocked)' || missing+=("a STATUS line")
printf '%s\n' "$message" | grep -Eq '^CHECKS RUN:' || missing+=("a CHECKS RUN section with commands and their output")

if [ "${#missing[@]}" -gt 0 ]; then
  {
    printf 'Your final message is missing:'
    printf ' %s;' "${missing[@]}"
    printf '\n'
    printf 'End with the return contract: STATUS, RESULT, EVIDENCE, CHECKS RUN, NOT CHECKED, CHANGED, OPEN.\n'
  } >&2
  exit 2
fi

exit 0
