# E6 Skills

E6 Skills is the shared source of repo-specific skills for E6 coding agents.

The repo intentionally has one install shape:

- One shared checkout at `~/.e6/skills/e6-skills`.
- One flat skill namespace under `skills/`.
- One plugin adapter named `e6-skills` for plugin-aware agents.
- Shared runtime briefs under `~/.e6/skills/artifacts/`.

## Current Skills

Calcite is the first supported repo. Its skills are root-level skill
directories with `calcite-` prefixes, for example:

```text
skills/calcite-pr-handoff/
skills/calcite-pr-intake/
skills/calcite-query-support-check/
```

Future repo skills should follow the same pattern with a repo prefix, for
example `query-optimizer-pr-handoff`.

## Install

Clone or update the shared checkout:

```bash
mkdir -p ~/.e6/skills
if [ -d ~/.e6/skills/e6-skills/.git ]; then
  git -C ~/.e6/skills/e6-skills pull --ff-only
else
  git clone git@github.com:nirmal-e6/e6-skills.git ~/.e6/skills/e6-skills
fi
```

Then follow the adapter for the agent:

- Claude Code: `~/.e6/skills/e6-skills/.claude/INSTALL.md`
- Codex: `~/.e6/skills/e6-skills/.codex/INSTALL.md`

The installed skill bodies always come from `~/.e6/skills/e6-skills/skills`.

## Shared Brief Storage

Generated issue and PR briefs do not live in this repo. They live under:

```text
~/.e6/skills/artifacts/<repo-slug>/
```

For Calcite today:

```text
~/.e6/skills/artifacts/calcite/issue-briefs/
~/.e6/skills/artifacts/calcite/pr-briefs/
```

When multiple agents work on the same item, update the existing brief, preserve
prior entries, and append timestamped coordination notes instead of relying on
chat history.

## Layout

```text
.agents/plugins/marketplace.json  # Codex development marketplace
.claude-plugin/marketplace.json   # Claude development marketplace
.claude/INSTALL.md                # Claude install adapter
.codex/INSTALL.md                 # Codex install adapter
Makefile                          # validation shortcuts
plugins/
  e6-skills/
    .claude-plugin/plugin.json
    .codex-plugin/plugin.json
    skills -> ../../skills
shared/
  templates/
    calcite/
skills/
  calcite-pr-handoff/
  calcite-pr-intake/
```

Use this rule for new repos:

- Add skill directories under `skills/` with a repo prefix.
- Add shared templates under `shared/templates/<repo-slug>/` when needed.
- Add runtime brief directories under `~/.e6/skills/artifacts/<repo-slug>/`.
- Do not create a new plugin per repo unless the repo genuinely needs separate
  install or permission boundaries.

## Validate

```bash
make validate
```

When Claude Code is installed, also run:

```bash
make validate-claude
```

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

Restart Codex after adding or renaming skills. In Claude Code, run
`/reload-plugins` after plugin changes.
