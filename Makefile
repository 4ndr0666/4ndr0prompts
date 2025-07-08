.PHONY: test clean setup

test:
	pre-commit run --show-diff-on-failure --color always --files $(shell git ls-files '*.py' '*.sh')

clean:
	rm -rf __pycache__ *.pyc .coverage coverage.xml .pytest_cache tests/tmp

setup:
	pre-commit install
