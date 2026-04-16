# E6 Calcite Plugin Adapter

This directory packages the canonical Calcite skill pack for plugin-aware agent
runtimes.

## Contents

- `.claude-plugin/plugin.json` exposes the pack as a Claude Code plugin named
  `e6-calcite`. Claude invokes skills through namespaced commands such as
  `/e6-calcite:calcite-pr-handoff`.
- `.codex-plugin/plugin.json` exposes the same pack as a Codex plugin.
- `skills` is a symlink to `../../packs/calcite/skills`, the canonical skill
  source.

Do not edit skill bodies in this directory. Edit the canonical files under
`packs/calcite/skills/`.

The symlink is for local development from the shared checkout. If this plugin is
published as a standalone artifact later, copy the canonical skill directories
into the artifact so the plugin is self-contained.

## Shared Runtime Artifacts

Issue and PR briefs are not stored inside the plugin. They live under:

```text
~/.e6/skills/artifacts/calcite/
```

That path is intentionally shared by Claude, Codex, and other coding agents.
