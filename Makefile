.PHONY: test validate validate-claude package

test:
	python3 -m unittest discover -s tests

validate: test
	python3 scripts/plugin_repo.py validate

validate-claude: validate
	python3 scripts/plugin_repo.py validate --with-claude

package: validate
	python3 scripts/plugin_repo.py package --clean --archive
