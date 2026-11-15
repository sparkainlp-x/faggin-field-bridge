PYTHON ?= python3

.PHONY: test coverage benchmark clean

test:
	$(PYTHON) -m pytest tests/ -vv

coverage:
	$(PYTHON) -m coverage run -m pytest tests/ -vv
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage xml -o coverage.xml
	$(PYTHON) -m coverage html -d coverage_html

benchmark:
	$(PYTHON) scientific_outcomes.py

clean:
	rm -rf results coverage_html coverage.xml .coverage .pytest_cache __pycache__ */__pycache__
