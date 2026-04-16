# Shared E6 Skill Assets

This directory contains assets shared by every supported agent runtime.

## Templates

Templates live under `shared/templates/<pack>/` so skills can reference one
stable repo path regardless of whether the caller is Codex, Claude Code, or a
future agent.

## Runtime Artifacts

Generated briefs do not live in this repo. The canonical shared artifact root
is:

```text
~/.e6/skills/artifacts/<pack>/
```

For Calcite today:

```text
~/.e6/skills/artifacts/calcite/issue-briefs/
~/.e6/skills/artifacts/calcite/pr-briefs/
```

## Multi-Agent Rules

- Use one brief per candidate, branch, or PR slug.
- Update the existing brief instead of creating agent-specific copies.
- Re-read the current brief immediately before writing, then merge new
  notes into the latest content instead of replacing from a stale copy.
- Preserve prior notes unless they are explicitly obsolete and the replacement
  records why.
- Record active file or surface claims before splitting work across agents.
- Append timestamped coordination-log entries for claims, handoffs, blockers,
  and verification results.
- Do not rely on chat history as the handoff record.
