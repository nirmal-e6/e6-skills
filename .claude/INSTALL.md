# Installing E6 Skills For Claude Code

This installs the shared `e6-skills` plugin for Claude Code. The plugin exposes
the root `skills/` directory from the shared checkout.

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

3. **Install the Claude Code plugin:**

   In Claude Code:

   ```text
   /plugin marketplace add ~/.e6/skills/e6-skills
   /plugin install e6-skills@e6-skills
   ```

4. **Reload plugins** after edits:
   ```text
   /reload-plugins
   ```

## Verify

In Claude Code, verify that the namespaced skills are available:

```text
/e6-skills:calcite-pr-handoff
```

From the shell, verify shared storage exists:

```bash
ls -d ~/.e6/skills/artifacts/calcite/issue-briefs
ls -d ~/.e6/skills/artifacts/calcite/pr-briefs
```

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

Then run `/reload-plugins` in Claude Code.

## Uninstalling

Use Claude Code's plugin manager to uninstall `e6-skills`. Optionally remove
the shared checkout and artifacts if no other agent uses them:

```bash
rm -rf ~/.e6/skills/e6-skills
rm -rf ~/.e6/skills/artifacts/calcite
```
