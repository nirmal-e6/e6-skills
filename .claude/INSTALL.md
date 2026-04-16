# Installing E6 Calcite Skills For Claude Code

This installs the Calcite pack from `e6-skills` as a Claude Code plugin while
sharing the same source checkout and brief artifacts used by Codex and other
agents.

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

   In Claude Code, add this repo as a local marketplace and install the plugin:

   ```text
   /plugin marketplace add ~/.e6/skills/e6-skills
   /plugin install e6-calcite@e6-skills
   ```

   For local development without marketplace installation, you can start Claude
   Code with the plugin directory directly:

   ```bash
   claude --plugin-dir ~/.e6/skills/e6-skills/plugins/e6-calcite
   ```

4. **Reload plugins** after edits:
   ```text
   /reload-plugins
   ```

## Verify

In Claude Code, verify that namespaced skills are available, for example:

```text
/e6-calcite:calcite-pr-handoff
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

## Legacy Personal-Skill Fallback

For quick local testing without plugin namespacing, you can symlink skills into
Claude Code's personal skill directory:

```bash
mkdir -p ~/.claude/skills
for skill in ~/.e6/skills/e6-skills/packs/calcite/skills/*; do
  name=$(basename "$skill")
  rm -rf "$HOME/.claude/skills/$name"
  ln -s "$skill" "$HOME/.claude/skills/$name"
done
```

This exposes flat commands such as `/calcite-pr-handoff`. The plugin install is
preferred for shared/team usage because it provides the `e6-calcite:` namespace.

## Uninstalling

Use Claude Code's plugin manager to uninstall the plugin. If you used the
legacy personal-skill fallback, remove those symlinks separately:

```bash
rm -f ~/.claude/skills/calcite-*
```

Optionally remove the shared clone and artifacts if no other agent uses them:

```bash
rm -rf ~/.e6/skills/e6-skills
rm -rf ~/.e6/skills/artifacts/calcite
```
