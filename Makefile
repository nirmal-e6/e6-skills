.PHONY: validate validate-claude

JSON_FILES := \
	.agents/plugins/marketplace.json \
	.claude-plugin/marketplace.json \
	plugins/e6-skills/.claude-plugin/plugin.json \
	plugins/e6-skills/.codex-plugin/plugin.json

validate:
	@set -e; for file in $(JSON_FILES); do python3 -m json.tool "$$file" >/dev/null; done
	python3 -m unittest discover -s tests -v
	python3 scripts/validate_repository.py
	test -f skills/calcite-pr-handoff/SKILL.md
	test -f shared/templates/calcite/PR-BRIEF-TEMPLATE.md
	test "$$(readlink plugins/e6-skills/skills)" = "../../skills"

validate-claude: validate
	claude plugin validate plugins/e6-skills
	claude plugin validate .claude-plugin/marketplace.json
