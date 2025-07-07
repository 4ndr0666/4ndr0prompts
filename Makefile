.PHONY: setup test bats validate clean

setup:
python3 -m pip install --upgrade pip
pip install -r requirements.txt pre-commit
sudo apt-get update -y
sudo apt-get install -y fzf shellcheck bats
pre-commit install

test:
PYTHONPATH=. pytest -q --cov=.

bats:
bats -r test/test_scripts.bats

validate:
python scripts/parse_rawdata.py --write

clean:
find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

