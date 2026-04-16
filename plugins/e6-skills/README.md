# E6 Skills Plugin Adapter

This directory packages the root `skills/` namespace for plugin-aware agent
runtimes.

## Contents

- `.claude-plugin/plugin.json` exposes this repo as a Claude Code plugin named
  `e6-skills`. Claude invokes skills through namespaced commands such as
  `/e6-skills:calcite-pr-handoff`.
- `.codex-plugin/plugin.json` exposes the same skill namespace as a Codex
  plugin adapter.
- `skills` is a symlink to `../../skills`, the canonical skill source.

Do not edit skill bodies in this directory. Edit canonical skill files under
the repo-root `skills/` directory.

## Shared Runtime Artifacts

Issue and PR briefs are not stored inside the plugin. They live under:

```text
~/.e6/skills/artifacts/<repo-slug>/
```

That path is intentionally shared by Claude, Codex, and other coding agents.
