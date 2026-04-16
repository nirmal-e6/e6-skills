# Installing E6 Calcite Skills For Claude Code

This installs the Calcite pack from `e6-skills` using Claude Code skill
discovery while sharing the same source checkout and brief artifacts used by
Codex.

This repository is private. Use a local checkout or clone with SSH or other
authenticated GitHub access.

## Claude Prompt

Tell Claude Code:

```text
Clone git@github.com:nirmal-e6/e6-skills.git into ~/.e6/skills/e6-skills and then follow ~/.e6/skills/e6-skills/.claude/INSTALL.md
```

## Prerequisites

- Git
- Superpowers already installed for Claude Code

If Superpowers is not installed yet, install it for Claude Code first using the
upstream Superpowers Claude instructions.

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

3. **Expose each Calcite skill to Claude Code:**
   ```bash
   mkdir -p ~/.claude/skills
   rm -f ~/.claude/skills/e6-calcite
   for skill in ~/.e6/skills/e6-skills/packs/calcite/skills/*; do
     name=$(basename "$skill")
     rm -rf "$HOME/.claude/skills/$name"
     ln -s "$skill" "$HOME/.claude/skills/$name"
   done
   ```

4. **Restart Claude Code** so it re-discovers the installed skills.

## Verify

```bash
ls -la ~/.claude/skills/calcite-pr-handoff
ls -d ~/.e6/skills/artifacts/calcite/issue-briefs
ls -d ~/.e6/skills/artifacts/calcite/pr-briefs
```

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

## Uninstalling

```bash
rm -f ~/.claude/skills/calcite-*
```

Optionally remove the shared clone and artifacts if no other agent uses them:

```bash
rm -rf ~/.e6/skills/e6-skills
rm -rf ~/.e6/skills/artifacts/calcite
```
