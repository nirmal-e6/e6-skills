import importlib.util
import tarfile
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "plugin_repo.py"

spec = importlib.util.spec_from_file_location("plugin_repo", MODULE_PATH)
plugin_repo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin_repo)


class PluginRepoTests(unittest.TestCase):
    def test_validate_repo_accepts_current_plugin_shape(self):
        checked_paths = plugin_repo.validate_repo(REPO_ROOT, "e6-calcite")

        self.assertIn(
            REPO_ROOT / "plugins/e6-calcite/.claude-plugin/plugin.json",
            checked_paths,
        )
        self.assertIn(
            REPO_ROOT / "plugins/e6-calcite/.codex-plugin/plugin.json",
            checked_paths,
        )
        self.assertIn(
            REPO_ROOT / "plugins/e6-calcite/skills/calcite-pr-handoff/SKILL.md",
            checked_paths,
        )

    def test_package_plugin_materializes_self_contained_artifact(self):
        source_skills = REPO_ROOT / "plugins/e6-calcite/skills"
        self.assertTrue(source_skills.is_symlink())

        with tempfile.TemporaryDirectory() as tmp:
            artifact = plugin_repo.package_plugin(
                REPO_ROOT,
                "e6-calcite",
                Path(tmp),
                clean=True,
            )

            self.assertEqual("e6-calcite-0.1.0", artifact.name)
            self.assertTrue((artifact / ".claude-plugin/plugin.json").is_file())
            self.assertTrue((artifact / ".codex-plugin/plugin.json").is_file())
            self.assertTrue(
                (artifact / "skills/calcite-pr-handoff/SKILL.md").is_file()
            )
            self.assertFalse((artifact / "skills").is_symlink())

            symlinks = [
                path.relative_to(artifact)
                for path in artifact.rglob("*")
                if path.is_symlink()
            ]
            self.assertEqual([], symlinks)

    def test_archive_plugin_preserves_full_versioned_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact = plugin_repo.package_plugin(
                REPO_ROOT,
                "e6-calcite",
                Path(tmp),
                clean=True,
            )

            archive = plugin_repo.archive_plugin(artifact)

            self.assertEqual("e6-calcite-0.1.0.tar.gz", archive.name)
            with tarfile.open(archive, "r:gz") as tar:
                names = set(tar.getnames())

            self.assertIn(
                "e6-calcite-0.1.0/skills/calcite-pr-handoff/SKILL.md",
                names,
            )


if __name__ == "__main__":
    unittest.main()
