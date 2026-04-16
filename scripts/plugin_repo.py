#!/usr/bin/env python3
"""Validate and package E6 plugin adapters."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Iterable


DEFAULT_PLUGIN = "e6-calcite"


class ValidationError(RuntimeError):
    """Raised when the plugin repo shape is invalid."""


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def marketplace_entry(marketplace: dict, plugin_name: str, path: Path) -> dict:
    plugins = marketplace.get("plugins")
    expect(isinstance(plugins, list), f"{path}: plugins must be a list")
    matches = [entry for entry in plugins if entry.get("name") == plugin_name]
    expect(len(matches) == 1, f"{path}: expected exactly one {plugin_name} entry")
    return matches[0]


def skill_frontmatter(skill_file: Path) -> dict[str, str]:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    expect(lines and lines[0] == "---", f"{skill_file}: missing frontmatter")

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')

    raise ValidationError(f"{skill_file}: unterminated frontmatter")


def skill_dirs(skills_path: Path) -> list[Path]:
    return sorted(path for path in skills_path.iterdir() if path.is_dir())


def validate_repo(
    repo_root: Path | str,
    plugin_name: str = DEFAULT_PLUGIN,
    *,
    with_claude: bool = False,
) -> list[Path]:
    """Validate the repo plugin adapter shape and return checked paths."""

    repo_root = Path(repo_root).resolve()
    plugin_dir = repo_root / "plugins" / plugin_name
    checked: list[Path] = []

    expect(plugin_dir.is_dir(), f"{plugin_dir}: missing plugin directory")
    checked.append(plugin_dir)

    claude_manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    codex_manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    for path in (claude_manifest_path, codex_manifest_path):
        expect(path.is_file(), f"{path}: missing manifest")
        checked.append(path)

    claude_manifest = load_json(claude_manifest_path)
    codex_manifest = load_json(codex_manifest_path)
    expect(claude_manifest.get("name") == plugin_name, f"{claude_manifest_path}: name mismatch")
    expect(codex_manifest.get("name") == plugin_name, f"{codex_manifest_path}: name mismatch")
    expect(
        claude_manifest.get("version") == codex_manifest.get("version"),
        "Claude and Codex plugin versions must match",
    )
    expect(codex_manifest.get("skills") == "./skills/", f"{codex_manifest_path}: skills must be ./skills/")

    skills_path = plugin_dir / "skills"
    expect(skills_path.exists(), f"{skills_path}: missing skills adapter")
    expect(skills_path.is_dir(), f"{skills_path}: must resolve to a directory")
    checked.append(skills_path)

    frontmatter_names: set[str] = set()
    dirs = skill_dirs(skills_path)
    expect(dirs, f"{skills_path}: expected at least one skill directory")
    for skill_dir in dirs:
        skill_file = skill_dir / "SKILL.md"
        expect(skill_file.is_file(), f"{skill_file}: missing SKILL.md")
        fields = skill_frontmatter(skill_file)
        expect(fields.get("name") == skill_dir.name, f"{skill_file}: name must match directory")
        expect(fields.get("description", "").startswith("Use when "), f"{skill_file}: description must start with 'Use when '")
        expect(fields["name"] not in frontmatter_names, f"{skill_file}: duplicate skill name {fields['name']}")
        frontmatter_names.add(fields["name"])
        checked.append(skill_file)

    claude_marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    codex_marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    for path in (claude_marketplace_path, codex_marketplace_path):
        expect(path.is_file(), f"{path}: missing marketplace")
        checked.append(path)

    version = claude_manifest["version"]
    claude_marketplace = load_json(claude_marketplace_path)
    claude_entry = marketplace_entry(claude_marketplace, plugin_name, claude_marketplace_path)
    expect(claude_entry.get("version") == version, f"{claude_marketplace_path}: version mismatch")
    expect(claude_entry.get("source") == f"./plugins/{plugin_name}", f"{claude_marketplace_path}: source mismatch")

    codex_marketplace = load_json(codex_marketplace_path)
    codex_entry = marketplace_entry(codex_marketplace, plugin_name, codex_marketplace_path)
    source = codex_entry.get("source")
    expect(isinstance(source, dict), f"{codex_marketplace_path}: source must be an object")
    expect(source.get("source") == "local", f"{codex_marketplace_path}: source.source must be local")
    expect(source.get("path") == f"./plugins/{plugin_name}", f"{codex_marketplace_path}: source.path mismatch")
    policy = codex_entry.get("policy")
    expect(isinstance(policy, dict), f"{codex_marketplace_path}: missing policy")
    expect(policy.get("installation") == "AVAILABLE", f"{codex_marketplace_path}: installation policy mismatch")
    expect(policy.get("authentication") == "ON_INSTALL", f"{codex_marketplace_path}: authentication policy mismatch")

    if with_claude:
        run_claude_validation(repo_root, plugin_dir, claude_marketplace_path)

    return checked


def copy_ignore(_directory: str, names: Iterable[str]) -> set[str]:
    ignored = {".DS_Store", "__pycache__"}
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def ensure_no_symlinks(path: Path) -> None:
    symlinks = [entry.relative_to(path) for entry in path.rglob("*") if entry.is_symlink()]
    expect(not symlinks, f"{path}: packaged artifact contains symlinks: {symlinks}")


def package_plugin(
    repo_root: Path | str,
    plugin_name: str = DEFAULT_PLUGIN,
    output_root: Path | str | None = None,
    *,
    clean: bool = False,
) -> Path:
    """Build a self-contained plugin directory with materialized skills."""

    repo_root = Path(repo_root).resolve()
    validate_repo(repo_root, plugin_name)

    plugin_dir = repo_root / "plugins" / plugin_name
    manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
    version = manifest["version"]

    output_root = Path(output_root) if output_root is not None else repo_root / "dist" / "plugins"
    output_root = output_root.resolve()
    target = output_root / f"{plugin_name}-{version}"

    if target.exists():
        expect(clean, f"{target}: already exists; pass --clean to replace it")
        shutil.rmtree(target)

    output_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plugin_dir, target, symlinks=False, ignore=copy_ignore)
    ensure_no_symlinks(target)
    return target


def archive_plugin(artifact: Path) -> Path:
    archive = artifact.parent / f"{artifact.name}.tar.gz"
    if archive.exists():
        archive.unlink()
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(artifact, arcname=artifact.name)
    return archive


def run_claude_validation(repo_root: Path, plugin_dir: Path, marketplace_path: Path) -> None:
    for path in (plugin_dir, marketplace_path):
        subprocess.run(
            ["claude", "plugin", "validate", str(path.relative_to(repo_root))],
            cwd=repo_root,
            check=True,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plugin", default=DEFAULT_PLUGIN)

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate repo plugin layout")
    validate.add_argument("--with-claude", action="store_true", help="also run claude plugin validate")

    package = subparsers.add_parser("package", help="build a self-contained plugin artifact")
    package.add_argument("--output-root", type=Path, default=None)
    package.add_argument("--clean", action="store_true")
    package.add_argument("--archive", action="store_true", help="also create a .tar.gz archive")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            checked = validate_repo(args.repo_root, args.plugin, with_claude=args.with_claude)
            print(f"validated {len(checked)} paths for {args.plugin}")
            return 0

        if args.command == "package":
            artifact = package_plugin(args.repo_root, args.plugin, args.output_root, clean=args.clean)
            print(artifact)
            if args.archive:
                print(archive_plugin(artifact))
            return 0
    except (ValidationError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
