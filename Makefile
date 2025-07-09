PYTHON=python3
BATS=bats

.PHONY: test clean setup

test:
	$(PYTHON) -m pytest -q --cov=.
	$(BATS) -r tests/cli.bats

clean:
	rm -rf __pycache__ */__pycache__ *.pyc .pytest_cache coverage.xml htmlcov

setup:
	pip install -r requirements.txt || true
