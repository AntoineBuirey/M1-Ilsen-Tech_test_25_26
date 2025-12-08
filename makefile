
.PHONY: test unit_test perf_test coverage lint doc

test:
	@pytest --no-summary

unit_test:
	@pytest -m "not performance"

perf_test:
	@pytest -m "performance"

coverage:
	@-coverage run -m pytest -m "not performance"
	@coverage report -m

lint:
	@ruff check

doc:
	@pdoc3 --output-dir docs --force --html triangulator