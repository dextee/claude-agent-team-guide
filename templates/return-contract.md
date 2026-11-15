# Return contract

Paste this at the end of a delegation brief, or at the end of an agent file's body. A subagent's final message is the only thing the caller receives, so the format of that message is the contract.

```text
End with a final message in exactly this shape. Nothing after it.

STATUS: done | partial | blocked
RESULT: one or two sentences.
EVIDENCE:
- <claim> :: <file:line you read, or the command you ran> :: <what it showed>
- ...
CHECKS RUN:
- <exact command> -> <exit code> -> <the decisive lines of output, copied, not paraphrased>
NOT CHECKED: <what you could not verify, and why>. Write "none" only if you list what you did check above.
CHANGED: <files, branch and commit SHA, or "nothing">
OPEN: <decisions only a person can make, or "none">
```

Rules the caller applies when reading it:

- `STATUS: partial` or a report marked partial by Claude Code means unfinished work, even if the text sounds complete.
- A claim without an evidence line is a lead to check, not a finding.
- `CHECKS RUN` with a command but no output is not a check. Re-run it yourself before acting.
- A report that opens with "This agent switched to <model>" ran on a fallback model. Weigh it accordingly.
