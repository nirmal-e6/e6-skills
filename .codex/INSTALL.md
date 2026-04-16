# Installing E6 Calcite Skills For Codex

This installs the Calcite pack from `e6-skills` using Codex native skill
discovery while sharing the same source checkout and brief artifacts used by
Claude Code and other agents.

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

3. **Expose the Calcite pack to Codex native skill discovery:**
   ```bash
   mkdir -p ~/.agents/skills
   rm -f ~/.agents/skills/e6-calcite
   ln -s ~/.e6/skills/e6-skills/packs/calcite/skills ~/.agents/skills/e6-calcite
   ```

4. **Remove the old Calcite namespace if you previously used it:**
   ```bash
   rm -f ~/.agents/skills/calcite-harness
   ```

5. **Restart Codex** so it re-discovers the installed skills.

## Codex Plugin Adapter

The same pack is also packaged as a Codex plugin at:

```text
~/.e6/skills/e6-skills/plugins/e6-calcite/.codex-plugin/plugin.json
```

The repo includes a development marketplace at:

```text
~/.e6/skills/e6-skills/.agents/plugins/marketplace.json
```

Use the native skill symlink above for day-to-day local work. Use the plugin
adapter when testing Codex plugin or marketplace flows.

## Verify

```bash
ls -la ~/.agents/skills/e6-calcite
ls -d ~/.e6/skills/artifacts/calcite/issue-briefs
ls -d ~/.e6/skills/artifacts/calcite/pr-briefs
test -f ~/.e6/skills/e6-skills/plugins/e6-calcite/.codex-plugin/plugin.json
```

## Updating

```bash
git -C ~/.e6/skills/e6-skills pull --ff-only
```

## Uninstalling

```bash
rm ~/.agents/skills/e6-calcite
```

Optionally remove the shared clone and artifacts if no other agent uses them:

```bash
rm -rf ~/.e6/skills/e6-skills
rm -rf ~/.e6/skills/artifacts/calcite
```
