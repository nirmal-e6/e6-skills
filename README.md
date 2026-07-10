# E6 Skills

E6 Skills is the shared source of capability-oriented query-engine and Calcite
skills for E6 coding agents.

The repo intentionally has one install shape:

- One shared checkout at `~/.e6/skills/e6-skills`.
- One flat skill namespace under `skills/`.
- One plugin adapter named `e6-skills` for plugin-aware agents.
- Shared runtime briefs under `~/.e6/skills/artifacts/`.

## Current Skills

The broad E6 query-engine portfolio is:

- `e6-query-engine-context` for bounded, current-code context discovery
- `e6-query-engine-pr-review` for coherent existing change-set review
- `e6-query-engine-diagnosis` for unknown or cross-engine symptoms
- `e6-query-engine-optimization` for evidenced performance investigation and design
- `e6-query-engine-coordination` for dependent outcomes needing reconciliation

The context skill progressively discloses code-grounded references for the
planner/Calcite seam, plan lowering, executor consumers, state, generation,
topology, and evidence handling. Workflow skills compose with it only when the
current mechanism crosses those boundaries.

Existing Calcite skills remain the deeper specialized lenses for proven Calcite
work. They are root-level directories with `calcite-` prefixes, for example:

```text
skills/calcite-pr-handoff/
skills/calcite-pr-intake/
skills/calcite-query-support-check/
```

Skills are named for repeatable capabilities and lifecycle outcomes, not split
repositories or monorepo paths. When no specialized skill clearly applies, use
native reasoning instead of forcing the nearest workflow.

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
  e6-query-engine-context/
    references/
  e6-query-engine-diagnosis/
  e6-query-engine-pr-review/
  calcite-pr-handoff/
  calcite-pr-intake/
```

Use these rules for future additions:

- Add a skill only for a distinct, recurring capability with routing evidence.
- Keep detailed shared context behind selectively loaded references.
- Add shared templates under `shared/templates/<repo-slug>/` when needed.
- Add runtime brief directories under `~/.e6/skills/artifacts/<repo-slug>/`.
- Do not create a new plugin per repo unless the repo genuinely needs separate
  install or permission boundaries.

## Validate

```bash
make validate
```

This checks the plugin JSON and skill symlink, runs the standard-library
validator tests, validates every `skills/*/SKILL.md`, and validates the
versioned routing corpus at `evaluations/routing/v1.json`. The corpus records
realistic prompts with expected primary or no-specialized-skill routing,
allowed composition, forbidden collisions, and expected behavior tags for
semantic evaluation.

Run only the focused validator tests with:

```bash
python3 -m unittest discover -s tests -v
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
