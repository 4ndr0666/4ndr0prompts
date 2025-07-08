.PHONY: test clean

test:
	PYTHONPATH=. pytest -q
	bats -r tests/cli.bats

clean:
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
