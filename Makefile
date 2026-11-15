PYTHON ?= python3

.PHONY: test benchmark clean

test:
	$(PYTHON) -m pytest tests/ -q

benchmark:
	$(PYTHON) scientific_outcomes.py

clean:
	rm -rf results .pytest_cache __pycache__ */__pycache__
