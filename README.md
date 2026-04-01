# E6 Skills

E6 Skills is a versioned collection of repo-specific skill packs that layer on
top of Superpowers.

The first pack is Calcite. Future packs can live alongside it in this repo
without mixing their skill namespaces.

## How It Fits Together

- Superpowers provides the base process layer.
- E6 packs provide repo-specific routing, invariants, and durable artifacts.
- Each pack is exposed to Codex through its own symlinked namespace, for example
  `e6-calcite` today and `e6-planner` later.

## Current Packs

- `calcite` -> Apache Calcite workflow and review skills

## Codex Install

Install Superpowers first, then tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/nirmal-e6/e6-skills/refs/heads/main/.codex/INSTALL.md
```

That bootstrap installs the repo at `~/.codex/e6-skills`, exposes the Calcite
pack as `~/.agents/skills/e6-calcite`, and prepares the local memory
directories used by the Calcite brief workflows.

## Layout

```text
packs/
  calcite/
    skills/
    templates/
```

- `packs/<name>/skills/` contains installable Codex skills
- `packs/<name>/templates/` contains reusable templates or reference assets
- Generated runtime artifacts do not live in git; they go under
  `~/.codex/memories/e6-skills/<pack>/`

## Updating

```bash
git -C ~/.codex/e6-skills pull --ff-only
```

Restart Codex after adding a new pack namespace. Existing installed skills
update through the same symlink.

## Local Development

This repository is the source of truth. The installed Codex path is
`~/.codex/e6-skills`; local development can point that path at this checkout.
