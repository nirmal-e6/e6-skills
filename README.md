# E6 Skills

E6 Skills is a versioned collection of repo-specific skill packs that layer on
top of Superpowers.

The first pack is Calcite. Future packs can live alongside it in this repo
without mixing their skill namespaces.

## How It Fits Together

- Superpowers provides the base process layer.
- E6 packs provide repo-specific routing, invariants, and durable artifacts.
- Install one shared checkout at `~/.e6/skills/e6-skills`.
- Agent-specific skill directories symlink to that checkout:
  - Codex: `~/.agents/skills/e6-calcite` points at the Calcite pack
    namespace.
  - Claude Code: each `calcite-*` skill is symlinked directly under
    `~/.claude/skills/`, because Claude Code expects a flat skill
    directory layout.
- Runtime briefs live in shared storage under `~/.e6/skills/artifacts/` so
  Codex and Claude sessions can hand work to each other without relying on chat
  history.

## Current Packs

- `calcite` -> Apache Calcite workflow and review skills

## Install

Install Superpowers first for the agent you plan to use.

Use one shared checkout for all agents:

```bash
mkdir -p ~/.e6/skills
if [ -d ~/.e6/skills/e6-skills/.git ]; then
  git -C ~/.e6/skills/e6-skills pull --ff-only
else
  git clone git@github.com:nirmal-e6/e6-skills.git ~/.e6/skills/e6-skills
fi
```

Then follow the agent-specific installer:

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
    skills/
shared/
  templates/
    calcite/
```

- `packs/<name>/skills/` contains installable skills.
- `shared/templates/<name>/` contains reusable templates and reference assets
  that are not tied to one agent runtime.
- Generated runtime artifacts do not live in git; they go under
  `~/.e6/skills/artifacts/<pack>/`.

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

Restart Codex or Claude Code after adding a new pack namespace. Existing
installed skills update through the same symlink.

## Local Development

This repository is the source of truth. For local development, point
`~/.e6/skills/e6-skills` at this checkout or push changes here and pull them
from the shared install checkout.
