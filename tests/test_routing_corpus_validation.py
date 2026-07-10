from validation_test_support import ValidatorTestCase, valid_corpus


class RoutingCorpusValidationTest(ValidatorTestCase):
    def setUp(self) -> None:
        super().setUp()
        for name in ("alpha-skill", "beta-skill", "gamma-skill"):
            self.write_skill(name)

    def test_corpus_must_be_valid_json_with_supported_schema_version(self) -> None:
        self.write_corpus("not json\n")
        self.assert_validation_error("routing corpus is not valid JSON")

        self.write_corpus({"schema_version": 2, "cases": []})
        self.assert_validation_error("schema_version must be 1")

    def test_case_requires_all_schema_fields(self) -> None:
        corpus = valid_corpus()
        del corpus["cases"][0]["prompt"]
        self.write_corpus(corpus)

        self.assert_validation_error("missing required field 'prompt'")

    def test_case_identifiers_must_be_unique(self) -> None:
        corpus = valid_corpus()
        corpus["cases"][1]["id"] = corpus["cases"][0]["id"]
        self.write_corpus(corpus)

        self.assert_validation_error("duplicate case id 'primary-skill'")

    def test_case_type_must_be_supported(self) -> None:
        corpus = valid_corpus()
        corpus["cases"][0]["case_type"] = "future-category"
        self.write_corpus(corpus)

        self.assert_validation_error("case_type must be one of")

    def test_every_referenced_skill_must_exist(self) -> None:
        mutations = (
            ("primary", lambda case: case["expected_routing"].update(skill="missing-skill")),
            ("composing", lambda case: case["allowed_composing_skills"].append("missing-skill")),
            ("forbidden", lambda case: case["forbidden_skills"].append("missing-skill")),
        )
        for field, mutate in mutations:
            with self.subTest(field=field):
                corpus = valid_corpus()
                mutate(corpus["cases"][0])
                self.write_corpus(corpus)
                self.assert_validation_error("references unknown skill 'missing-skill'")

    def test_no_specialized_skill_form_cannot_name_a_skill(self) -> None:
        corpus = valid_corpus()
        corpus["cases"][1]["expected_routing"]["skill"] = "alpha-skill"
        self.write_corpus(corpus)

        self.assert_validation_error(
            "no-specialized-skill routing must contain only the 'kind' field"
        )

        corpus = valid_corpus()
        corpus["cases"][1]["allowed_composing_skills"].append("alpha-skill")
        self.write_corpus(corpus)
        self.assert_validation_error(
            "no-specialized-skill routing cannot allow composing skills"
        )

    def test_skill_form_requires_exactly_one_skill(self) -> None:
        corpus = valid_corpus()
        del corpus["cases"][0]["expected_routing"]["skill"]
        self.write_corpus(corpus)

        self.assert_validation_error("skill routing must contain exactly 'kind' and 'skill'")

    def test_expected_behavior_tags_must_be_non_empty_unique_strings(self) -> None:
        corpus = valid_corpus()
        corpus["cases"][0]["expected_behavior_tags"] = []
        self.write_corpus(corpus)
        self.assert_validation_error("expected_behavior_tags must be a non-empty list")

        corpus = valid_corpus()
        corpus["cases"][0]["expected_behavior_tags"] = ["same-tag", "same-tag"]
        self.write_corpus(corpus)
        self.assert_validation_error("expected_behavior_tags must not contain duplicates")

    def test_routing_sets_must_not_contradict_each_other(self) -> None:
        corpus = valid_corpus()
        corpus["cases"][0]["forbidden_skills"].append("beta-skill")
        self.write_corpus(corpus)
        self.assert_validation_error("allowed_composing_skills and forbidden_skills overlap")

        corpus = valid_corpus()
        corpus["cases"][0]["forbidden_skills"].append("alpha-skill")
        self.write_corpus(corpus)
        self.assert_validation_error("primary skill 'alpha-skill' cannot be forbidden")

    def test_every_skill_requires_a_positive_case_where_it_is_primary(self) -> None:
        corpus = valid_corpus()
        corpus["cases"] = [
            case for case in corpus["cases"] if case["id"] != "beta-primary"
        ]
        self.write_corpus(corpus)

        self.assert_validation_error(
            "skill 'beta-skill' is missing a positive case where it is primary"
        )

    def test_every_skill_requires_a_negative_case_where_it_is_forbidden(self) -> None:
        corpus = valid_corpus()
        corpus["cases"][1]["forbidden_skills"].remove("beta-skill")
        self.write_corpus(corpus)

        self.assert_validation_error(
            "skill 'beta-skill' is missing a negative case where it is forbidden"
        )

    def test_every_skill_requires_involvement_in_a_sibling_overlap_case(self) -> None:
        corpus = valid_corpus()
        sibling_case = corpus["cases"][2]
        sibling_case["expected_routing"] = {"kind": "skill", "skill": "alpha-skill"}
        sibling_case["allowed_composing_skills"] = ["gamma-skill"]
        sibling_case["forbidden_skills"] = []
        self.write_corpus(corpus)

        self.assert_validation_error(
            "skill 'beta-skill' is missing a sibling-overlap case where it is primary, "
            "allowed, or forbidden"
        )

    def test_no_specialized_case_is_valid_without_notes(self) -> None:
        corpus = valid_corpus()
        self.assertNotIn("notes", corpus["cases"][1])
        self.write_corpus(corpus)

        result = self.run_validator()

        self.assertEqual(0, result.returncode, result.stderr)
