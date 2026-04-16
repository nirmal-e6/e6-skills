# Installing E6 Skills For Codex

This installs the shared E6 skill namespace for Codex. Codex reads the root
`skills/` directory from the shared checkout.

This repository is private. Use a local checkout or clone with SSH or other
authenticated GitHub access.

## Codex Prompt

Tell Codex:

```text
Clone git@github.com:nirmal-e6/e6-skills.git into ~/.e6/skills/e6-skills and then follow ~/.e6/skills/e6-skills/.codex/INSTALL.md
```

## Prerequisites

- Git
- Superpowers already installed for Codex

If Superpowers is not installed yet, first tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
```

## Installation

1. **Clone or update the shared repo checkout:**
   ```bash
   mkdir -p ~/.e6/skills
   if [ -d ~/.e6/skills/e6-skills/.git ]; then
     git -C ~/.e6/skills/e6-skills pull --ff-only
   else
     git clone git@github.com:nirmal-e6/e6-skills.git ~/.e6/skills/e6-skills
   fi
   ```

2. **Prepare shared Calcite brief storage:**
   ```bash
   mkdir -p \
     ~/.e6/skills/artifacts/calcite/issue-briefs \
     ~/.e6/skills/artifacts/calcite/pr-briefs
   ```

3. **Expose E6 skills to Codex native skill discovery:**
   ```bash
   mkdir -p ~/.agents/skills
   rm -f ~/.agents/skills/e6-skills
   ln -s ~/.e6/skills/e6-skills/skills ~/.agents/skills/e6-skills
   ```

4. **Remove old E6 Calcite namespaces if present:**
   ```bash
   rm -f ~/.agents/skills/e6-calcite
   rm -f ~/.agents/skills/calcite-harness
   ```

5. **Restart Codex** so it re-discovers the installed skills.

## Verify

```bash
ls -la ~/.agents/skills/e6-skills
test -f ~/.agents/skills/e6-skills/calcite-pr-handoff/SKILL.md
ls -d ~/.e6/skills/artifacts/calcite/issue-briefs
ls -d ~/.e6/skills/artifacts/calcite/pr-briefs
```

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

Restart Codex after adding or renaming skills.

## Uninstalling

```bash
rm ~/.agents/skills/e6-skills
```

Optionally remove the shared checkout and artifacts if no other agent uses them:

```bash
rm -rf ~/.e6/skills/e6-skills
rm -rf ~/.e6/skills/artifacts/calcite
```
