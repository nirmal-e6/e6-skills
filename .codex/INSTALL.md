# Installing E6 Calcite Skills For Codex

This installs the Calcite pack from `e6-skills` using Codex native skill
discovery.

This repository is private. Use a local checkout or clone with SSH or other
authenticated GitHub access.

## Codex Prompt

Tell Codex:

```text
Clone git@github.com:nirmal-e6/e6-skills.git into ~/.codex/e6-skills and then follow ~/.codex/e6-skills/.codex/INSTALL.md
```

## Prerequisites

- Git
- Superpowers already installed for Codex

If Superpowers is not installed yet, first tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
```

## Installation

1. **Clone or update the repo:**
   ```bash
   if [ -d ~/.codex/e6-skills/.git ]; then
     git -C ~/.codex/e6-skills pull --ff-only
   else
     git clone git@github.com:nirmal-e6/e6-skills.git ~/.codex/e6-skills
   fi
   ```

2. **Prepare local Calcite brief storage:**
   ```bash
   mkdir -p \
     ~/.codex/memories/e6-skills/calcite/issue-briefs \
     ~/.codex/memories/e6-skills/calcite/pr-briefs
   ```

3. **Expose the Calcite pack to Codex:**
   ```bash
   mkdir -p ~/.agents/skills
   rm -f ~/.agents/skills/e6-calcite
   ln -s ~/.codex/e6-skills/packs/calcite/skills ~/.agents/skills/e6-calcite
   ```

4. **Remove the old Calcite namespace if you previously used it:**
   ```bash
   rm -f ~/.agents/skills/calcite-harness
   ```

5. **Restart Codex** so it re-discovers the installed skills.

## Verify

```bash
ls -la ~/.agents/skills/e6-calcite
ls -d ~/.codex/memories/e6-skills/calcite/issue-briefs
ls -d ~/.codex/memories/e6-skills/calcite/pr-briefs
```

## Updating

```bash
git -C ~/.codex/e6-skills pull --ff-only
```

## Uninstalling

```bash
rm ~/.agents/skills/e6-calcite
```

Optionally remove the clone:

```bash
rm -rf ~/.codex/e6-skills
```
