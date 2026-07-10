from validation_test_support import REPOSITORY_ROOT, ValidatorTestCase, skill_document


class SkillValidationTest(ValidatorTestCase):
    def test_valid_skills_and_local_links_pass(self) -> None:
        self.create_valid_repository()
        reference = self.repository / "skills" / "alpha-skill" / "references" / "details.md"
        reference.parent.mkdir()
        reference.write_text("# Details\n", encoding="utf-8")
        self.write_skill(
            "alpha-skill",
            skill_document(
                "alpha-skill",
                body=(
                    "# Alpha\n\n"
                    "Read [details](references/details.md#scope). External [docs](https://example.com) "
                    "and [this section](#alpha) are not local-file targets.\n"
                ),
            ),
        )

        result = self.run_validator()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Validated 3 skills and 5 routing cases", result.stdout)

    def test_frontmatter_is_required(self) -> None:
        self.create_valid_repository()
        self.write_skill("alpha-skill", "# No frontmatter\n")

        self.assert_validation_error("frontmatter must start on the first line")

    def test_name_and_description_must_be_non_empty(self) -> None:
        for field, content in (
            ("name", skill_document('""')),
            ("description", skill_document("alpha-skill", description='""')),
        ):
            with self.subTest(field=field):
                self.create_valid_repository()
                self.write_skill("alpha-skill", content)
                self.assert_validation_error(f"frontmatter field '{field}' must be non-empty")

    def test_name_must_match_skill_directory(self) -> None:
        self.create_valid_repository()
        self.write_skill("alpha-skill", skill_document("different-skill"))

        self.assert_validation_error("name 'different-skill' does not match directory 'alpha-skill'")

    def test_description_must_begin_with_use_when(self) -> None:
        self.create_valid_repository()
        self.write_skill(
            "alpha-skill",
            skill_document("alpha-skill", description="Validates a fixture."),
        )

        self.assert_validation_error("description must begin with 'Use when'")

    def test_duplicate_skill_names_are_rejected(self) -> None:
        self.create_valid_repository()
        self.write_skill("alpha-skill", skill_document("shared-name"))
        self.write_skill("beta-skill", skill_document("shared-name"))

        self.assert_validation_error("duplicate skill name 'shared-name'")

    def test_skill_document_must_remain_under_500_lines(self) -> None:
        self.create_valid_repository()
        lines = [
            "---",
            "name: alpha-skill",
            "description: Use when testing the line limit.",
            "---",
        ] + ["body"] * 496
        self.assertEqual(500, len(lines))
        self.write_skill("alpha-skill", "\n".join(lines) + "\n")

        self.assert_validation_error("has 500 lines; SKILL.md must stay under 500 lines")

    def test_broken_relative_markdown_links_are_rejected(self) -> None:
        self.create_valid_repository()
        self.write_skill(
            "alpha-skill",
            skill_document(
                "alpha-skill",
                body="# Alpha\n\nRead [missing reference](references/missing.md).\n",
            ),
        )

        self.assert_validation_error("relative Markdown link does not resolve: references/missing.md")

    def test_repository_artifacts_pass_validation(self) -> None:
        result = self.run_validator(REPOSITORY_ROOT)

        self.assertEqual(0, result.returncode, result.stderr)
