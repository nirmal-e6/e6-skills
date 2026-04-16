# E6 Skills

E6 Skills is a versioned collection of repo-specific skill packs that layer on
top of Superpowers.

The first pack is Calcite. Future packs can live alongside it in this repo
without mixing their skill namespaces.

## How It Fits Together

- Superpowers provides the base process layer.
- E6 packs provide repo-specific routing, invariants, and durable artifacts.
- Canonical skills live under `packs/<name>/skills/` using the Agent Skills
  directory format.
- Plugin-aware agents consume thin plugin adapters under `plugins/<name>/`.
  The adapters point back to the canonical skill source instead of duplicating
  `SKILL.md` files.
- Runtime briefs live in shared storage under `~/.e6/skills/artifacts/` so
  Claude, Codex, and other coding-agent sessions can hand work to each other
  without relying on chat history.

## Current Packs

- `calcite` -> Apache Calcite workflow and review skills

## Recommended Install Model

Install one shared checkout for all agents:

```bash
mkdir -p ~/.e6/skills
if [ -d ~/.e6/skills/e6-skills/.git ]; then
  git -C ~/.e6/skills/e6-skills pull --ff-only
else
  git clone git@github.com:nirmal-e6/e6-skills.git ~/.e6/skills/e6-skills
fi
```

Then use the platform adapter for your agent:

- Claude Code: install `e6-calcite` from the repo marketplace in
  `.claude-plugin/marketplace.json`; skills are invoked as
  `/e6-calcite:<skill-name>`.
- Codex: use native skill discovery via `~/.agents/skills/e6-calcite`, or use
  the Codex plugin metadata at `plugins/e6-calcite/.codex-plugin/plugin.json`
  when running through a plugin marketplace flow.
- Other Agent Skills-compatible tools: point them at
  `packs/calcite/skills/` or the `plugins/e6-calcite/skills` adapter,
  depending on whether they support plugin namespaces.

The plugin adapters are additive. They do not change the canonical
`packs/calcite/skills/` source or Codex's native `~/.agents/skills/e6-calcite`
install path.

Agent-specific instructions:

- Codex: `~/.e6/skills/e6-skills/.codex/INSTALL.md`
- Claude Code: `~/.e6/skills/e6-skills/.claude/INSTALL.md`

## Shared Brief Storage

Calcite issue and PR briefs are shared runtime artifacts, not Codex-only or
Claude-only memory. Installers create:

```text
~/.e6/skills/artifacts/calcite/issue-briefs/
~/.e6/skills/artifacts/calcite/pr-briefs/
```

Briefs should be named by candidate, branch, or PR slug. When multiple agents
work on the same item, update the existing brief, preserve prior entries, and
append timestamped coordination notes instead of relying on chat history.

## Layout

```text
packs/
  calcite/
    skills/                       # canonical Agent Skills source
plugins/
  e6-calcite/
    .claude-plugin/plugin.json    # Claude Code plugin adapter
    .codex-plugin/plugin.json     # Codex plugin adapter
    skills -> ../../packs/calcite/skills
shared/
  templates/
    calcite/
.claude-plugin/marketplace.json   # Claude development marketplace
.agents/plugins/marketplace.json  # Codex development marketplace
```

- `packs/<name>/skills/` contains canonical installable skills.
- `plugins/<name>/` contains platform plugin manifests and symlinks back to the
  canonical skill source.
- `shared/templates/<name>/` contains reusable templates and reference assets
  that are not tied to one agent runtime.
- Generated runtime artifacts do not live in git; they go under
  `~/.e6/skills/artifacts/<pack>/`.

For a published, standalone plugin artifact, materialize the `skills` directory
inside the artifact instead of shipping a symlink that depends on this checkout.
For local development, the symlink keeps the plugin adapter and native skill
install pointed at the same source files.

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

Restart Codex after adding a new native skill namespace. In Claude Code, run
`/reload-plugins` after plugin changes, or restart Claude Code if the plugin was
newly installed.

## Local Development

This repository is the source of truth. For local development, point
`~/.e6/skills/e6-skills` at this checkout or push changes here and pull them
from the shared install checkout.
