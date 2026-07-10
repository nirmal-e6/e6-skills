#!/usr/bin/env python3
"""Validate E6 skill metadata and the versioned routing-evaluation corpus."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


CORPUS_PATH = Path("evaluations/routing/v1.json")
CASE_TYPES = {"positive", "negative", "sibling-overlap"}
REQUIRED_CASE_FIELDS = {
    "id",
    "case_type",
    "prompt",
    "expected_routing",
    "allowed_composing_skills",
    "forbidden_skills",
    "expected_behavior_tags",
}
OPTIONAL_CASE_FIELDS = {"notes"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _frontmatter_scalar(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1].strip()
    return value


def _parse_frontmatter(skill_path: Path, root: Path, errors: list[str]) -> dict[str, str]:
    display_path = _display_path(skill_path, root)
    text = skill_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{display_path}: frontmatter must start on the first line")
        return {}

    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        errors.append(f"{display_path}: frontmatter has no closing '---' delimiter")
        return {}

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing_index], start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, separator, raw_value = stripped.partition(":")
        if not separator or key not in {"name", "description"}:
            continue
        if key in fields:
            errors.append(f"{display_path}:{line_number}: duplicate frontmatter field '{key}'")
            continue
        value = _frontmatter_scalar(raw_value)
        if value in {"|", "|-", ">", ">-"}:
            errors.append(
                f"{display_path}:{line_number}: frontmatter field '{key}' must be a single-line scalar"
            )
            value = ""
        fields[key] = value

    for required_field in ("name", "description"):
        if not fields.get(required_field, "").strip():
            errors.append(
                f"{display_path}: frontmatter field '{required_field}' must be non-empty"
            )
    return fields


def _markdown_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if destination.startswith("<"):
        closing_angle = destination.find(">", 1)
        if closing_angle == -1:
            return destination
        return destination[1:closing_angle]
    return destination.split(maxsplit=1)[0] if destination else ""


def _validate_relative_links(skill_path: Path, root: Path, errors: list[str]) -> None:
    text = skill_path.read_text(encoding="utf-8")
    display_path = _display_path(skill_path, root)
    for match in MARKDOWN_LINK.finditer(text):
        destination = _markdown_destination(match.group(1))
        if (
            not destination
            or destination.startswith(("#", "/", "//"))
            or URI_SCHEME.match(destination)
        ):
            continue
        relative_path = unquote(urlsplit(destination).path)
        if not relative_path:
            continue
        target = skill_path.parent / relative_path
        if not target.exists():
            errors.append(
                f"{display_path}: relative Markdown link does not resolve: {relative_path}"
            )


def validate_skills(root: Path, errors: list[str]) -> tuple[set[str], int]:
    skills_directory = root / "skills"
    if not skills_directory.is_dir():
        errors.append("skills: directory is missing")
        return set(), 0

    skill_paths = sorted(skills_directory.glob("*/SKILL.md"))
    if not skill_paths:
        errors.append("skills: no skills/*/SKILL.md files found")
        return set(), 0

    paths_by_name: dict[str, list[Path]] = {}
    for skill_path in skill_paths:
        text = skill_path.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        display_path = _display_path(skill_path, root)
        if line_count >= 500:
            errors.append(
                f"{display_path}: has {line_count} lines; SKILL.md must stay under 500 lines"
            )

        fields = _parse_frontmatter(skill_path, root, errors)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name:
            paths_by_name.setdefault(name, []).append(skill_path)
            if name != skill_path.parent.name:
                errors.append(
                    f"{display_path}: name '{name}' does not match directory "
                    f"'{skill_path.parent.name}'"
                )
        if description and not description.startswith("Use when"):
            errors.append(f"{display_path}: description must begin with 'Use when'")
        _validate_relative_links(skill_path, root, errors)

    for name, paths in sorted(paths_by_name.items()):
        if len(paths) > 1:
            locations = ", ".join(_display_path(path, root) for path in paths)
            errors.append(f"duplicate skill name '{name}': {locations}")

    return set(paths_by_name), len(skill_paths)


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(
    case: dict[str, object],
    field: str,
    case_label: str,
    errors: list[str],
    *,
    require_non_empty: bool = False,
) -> list[str]:
    value = case.get(field)
    if not isinstance(value, list) or (require_non_empty and not value):
        qualifier = "non-empty " if require_non_empty else ""
        errors.append(f"{case_label}: {field} must be a {qualifier}list")
        return []
    if any(not _non_empty_string(item) for item in value):
        errors.append(f"{case_label}: {field} must contain only non-empty strings")
        return []
    strings = [str(item) for item in value]
    if len(strings) != len(set(strings)):
        errors.append(f"{case_label}: {field} must not contain duplicates")
    return strings


def _validate_skill_references(
    references: list[str],
    skill_names: set[str],
    case_label: str,
    errors: list[str],
) -> None:
    for skill_name in references:
        if skill_name not in skill_names:
            errors.append(f"{case_label}: references unknown skill '{skill_name}'")


def _validate_routing(
    routing: object,
    skill_names: set[str],
    case_label: str,
    errors: list[str],
) -> tuple[str | None, str | None]:
    if not isinstance(routing, dict):
        errors.append(f"{case_label}: expected_routing must be an object")
        return None, None

    kind = routing.get("kind")
    if kind == "skill":
        if set(routing) != {"kind", "skill"}:
            errors.append(
                f"{case_label}: skill routing must contain exactly 'kind' and 'skill'"
            )
            return "skill", None
        skill_name = routing.get("skill")
        if not _non_empty_string(skill_name):
            errors.append(f"{case_label}: skill routing requires a non-empty skill")
            return "skill", None
        primary_skill = str(skill_name)
        _validate_skill_references([primary_skill], skill_names, case_label, errors)
        return "skill", primary_skill

    if kind == "no-specialized-skill":
        if set(routing) != {"kind"}:
            errors.append(
                f"{case_label}: no-specialized-skill routing must contain only the 'kind' field"
            )
        return "no-specialized-skill", None

    errors.append(
        f"{case_label}: expected_routing.kind must be 'skill' or 'no-specialized-skill'"
    )
    return None, None


def _validate_case(
    case: object,
    index: int,
    skill_names: set[str],
    case_ids: set[str],
    errors: list[str],
) -> None:
    fallback_label = f"routing case #{index + 1}"
    if not isinstance(case, dict):
        errors.append(f"{fallback_label}: case must be an object")
        return

    case_id = case.get("id")
    case_label = f"routing case '{case_id}'" if _non_empty_string(case_id) else fallback_label
    missing_fields = REQUIRED_CASE_FIELDS - set(case)
    for field in sorted(missing_fields):
        errors.append(f"{case_label}: missing required field '{field}'")
    unexpected_fields = set(case) - REQUIRED_CASE_FIELDS - OPTIONAL_CASE_FIELDS
    for field in sorted(unexpected_fields):
        errors.append(f"{case_label}: unexpected field '{field}'")

    if not _non_empty_string(case_id):
        errors.append(f"{case_label}: id must be a non-empty string")
    elif str(case_id) in case_ids:
        errors.append(f"duplicate case id '{case_id}'")
    else:
        case_ids.add(str(case_id))

    if case.get("case_type") not in CASE_TYPES:
        choices = ", ".join(sorted(CASE_TYPES))
        errors.append(f"{case_label}: case_type must be one of: {choices}")
    if not _non_empty_string(case.get("prompt")):
        errors.append(f"{case_label}: prompt must be a non-empty string")
    if "notes" in case and not _non_empty_string(case.get("notes")):
        errors.append(f"{case_label}: notes must be a non-empty string when present")

    routing_kind, primary_skill = _validate_routing(
        case.get("expected_routing"), skill_names, case_label, errors
    )
    allowed = _validate_string_list(
        case, "allowed_composing_skills", case_label, errors
    )
    forbidden = _validate_string_list(case, "forbidden_skills", case_label, errors)
    _validate_string_list(
        case,
        "expected_behavior_tags",
        case_label,
        errors,
        require_non_empty=True,
    )
    _validate_skill_references(allowed + forbidden, skill_names, case_label, errors)

    overlap = sorted(set(allowed) & set(forbidden))
    if overlap:
        errors.append(
            f"{case_label}: allowed_composing_skills and forbidden_skills overlap: "
            f"{', '.join(overlap)}"
        )
    if primary_skill in forbidden:
        errors.append(f"{case_label}: primary skill '{primary_skill}' cannot be forbidden")
    if primary_skill in allowed:
        errors.append(f"{case_label}: primary skill '{primary_skill}' cannot compose with itself")
    if routing_kind == "no-specialized-skill" and allowed:
        errors.append(f"{case_label}: no-specialized-skill routing cannot allow composing skills")


def _valid_skill_list(value: object) -> set[str]:
    if not isinstance(value, list) or any(not _non_empty_string(item) for item in value):
        return set()
    return {str(item) for item in value}


def _primary_skill(case: dict[str, object]) -> str | None:
    routing = case.get("expected_routing")
    if (
        not isinstance(routing, dict)
        or set(routing) != {"kind", "skill"}
        or routing.get("kind") != "skill"
        or not _non_empty_string(routing.get("skill"))
    ):
        return None
    return str(routing["skill"])


def _validate_skill_coverage(
    cases: list[object], skill_names: set[str], errors: list[str]
) -> None:
    positive_primary: set[str] = set()
    negative_forbidden: set[str] = set()
    sibling_involved: set[str] = set()

    for case in cases:
        if not isinstance(case, dict):
            continue
        case_type = case.get("case_type")
        primary_skill = _primary_skill(case)
        allowed = _valid_skill_list(case.get("allowed_composing_skills"))
        forbidden = _valid_skill_list(case.get("forbidden_skills"))

        if case_type == "positive" and primary_skill is not None:
            positive_primary.add(primary_skill)
        if case_type == "negative":
            negative_forbidden.update(forbidden)
        if case_type == "sibling-overlap":
            sibling_involved.update(allowed | forbidden)
            if primary_skill is not None:
                sibling_involved.add(primary_skill)

    for skill_name in sorted(skill_names):
        if skill_name not in positive_primary:
            errors.append(
                f"skill '{skill_name}' is missing a positive case where it is primary"
            )
        if skill_name not in negative_forbidden:
            errors.append(
                f"skill '{skill_name}' is missing a negative case where it is forbidden"
            )
        if skill_name not in sibling_involved:
            errors.append(
                f"skill '{skill_name}' is missing a sibling-overlap case where it is primary, "
                "allowed, or forbidden"
            )


def validate_routing_corpus(
    root: Path, skill_names: set[str], errors: list[str]
) -> int:
    corpus_path = root / CORPUS_PATH
    if not corpus_path.is_file():
        errors.append(f"{CORPUS_PATH}: routing corpus is missing")
        return 0

    try:
        corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{CORPUS_PATH}: routing corpus is not valid JSON: {error}")
        return 0

    if not isinstance(corpus, dict):
        errors.append(f"{CORPUS_PATH}: top level must be an object")
        return 0
    if type(corpus.get("schema_version")) is not int or corpus.get("schema_version") != 1:
        errors.append(f"{CORPUS_PATH}: schema_version must be 1")
    if set(corpus) - {"schema_version", "cases"}:
        errors.append(f"{CORPUS_PATH}: unexpected top-level fields")

    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{CORPUS_PATH}: cases must be a non-empty list")
        return 0

    case_ids: set[str] = set()
    for index, case in enumerate(cases):
        _validate_case(case, index, skill_names, case_ids, errors)
    _validate_skill_coverage(cases, skill_names, errors)
    return len(cases)


def validate_repository(root: Path) -> tuple[int, int, list[str]]:
    root = root.resolve()
    errors: list[str] = []
    skill_names, skill_count = validate_skills(root, errors)
    case_count = validate_routing_corpus(root, skill_names, errors)
    return skill_count, case_count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the script's parent repository)",
    )
    arguments = parser.parse_args()

    skill_count, case_count, errors = validate_repository(arguments.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {skill_count} skills and {case_count} routing cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
