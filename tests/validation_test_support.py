import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate_repository.py"


def skill_document(
    name: str,
    *,
    description: str = "Use when a focused validation fixture is needed.",
    body: str = "# Fixture Skill\n",
) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"{body}"
    )


def routing_case(
    case_id: str,
    *,
    expected_routing: dict[str, str],
    case_type: str = "positive",
    allowed: list[str] | None = None,
    forbidden: list[str] | None = None,
    tags: list[str] | None = None,
    notes: str | None = None,
) -> dict[str, object]:
    case: dict[str, object] = {
        "id": case_id,
        "case_type": case_type,
        "prompt": f"Prompt for {case_id}",
        "expected_routing": expected_routing,
        "allowed_composing_skills": allowed or [],
        "forbidden_skills": forbidden or [],
        "expected_behavior_tags": tags or ["inspect-current-evidence"],
    }
    if notes is not None:
        case["notes"] = notes
    return case


def valid_corpus() -> dict[str, object]:
    return {
        "schema_version": 1,
        "cases": [
            routing_case(
                "primary-skill",
                expected_routing={"kind": "skill", "skill": "alpha-skill"},
                allowed=["beta-skill"],
                forbidden=["gamma-skill"],
                notes="Optional notes are accepted.",
            ),
            routing_case(
                "no-specialized-skill",
                expected_routing={"kind": "no-specialized-skill"},
                case_type="negative",
                forbidden=["alpha-skill", "beta-skill", "gamma-skill"],
            ),
            routing_case(
                "sibling-overlap",
                expected_routing={"kind": "skill", "skill": "beta-skill"},
                case_type="sibling-overlap",
                allowed=["gamma-skill"],
                forbidden=["alpha-skill"],
            ),
            routing_case(
                "beta-primary",
                expected_routing={"kind": "skill", "skill": "beta-skill"},
            ),
            routing_case(
                "gamma-primary",
                expected_routing={"kind": "skill", "skill": "gamma-skill"},
            ),
        ],
    }


class ValidatorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.repository = Path(self._temporary_directory.name)

    def tearDown(self) -> None:
        self._temporary_directory.cleanup()

    def write_skill(self, directory_name: str, content: str | None = None) -> Path:
        skill_directory = self.repository / "skills" / directory_name
        skill_directory.mkdir(parents=True, exist_ok=True)
        skill_path = skill_directory / "SKILL.md"
        skill_path.write_text(content or skill_document(directory_name), encoding="utf-8")
        return skill_path

    def write_corpus(self, corpus: dict[str, object] | str | None = None) -> Path:
        corpus_path = self.repository / "evaluations" / "routing" / "v1.json"
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(corpus, str):
            corpus_path.write_text(corpus, encoding="utf-8")
        else:
            corpus_path.write_text(
                json.dumps(corpus or valid_corpus(), indent=2) + "\n",
                encoding="utf-8",
            )
        return corpus_path

    def create_valid_repository(self) -> None:
        for name in ("alpha-skill", "beta-skill", "gamma-skill"):
            self.write_skill(name)
        self.write_corpus()

    def run_validator(self, repository: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(repository or self.repository)],
            check=False,
            capture_output=True,
            text=True,
        )

    def assert_validation_error(self, expected_message: str) -> None:
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn(expected_message, result.stderr)
