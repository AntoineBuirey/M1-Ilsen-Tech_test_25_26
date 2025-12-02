

test:
	pytest

unit_test:
	python -m "not performance"

perf_test:
	python -m performance

coverage:
	-coverage run -m pytest
	coverage report -m

lint:
	ruff check

doc:
	pdoc3 --output-dir docs --force --html triangulator