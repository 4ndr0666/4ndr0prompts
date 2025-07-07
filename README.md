# 4ndr0prompts

SPDX-License-Identifier: MIT

## Quick-Start

```bash
make setup
bin/prompts.sh
```

## Usage

The `prompts.sh` wrapper allows you to generate prompts from the canonical
dataset located in `dataset/templates.json`. Select a category when prompted and the resulting text will be copied
to your clipboard (if `xclip` is available).
If `xclip` is missing the prompt will simply be printed to the terminal.

## Setup

Run `make setup` to install Python requirements and common tooling such as
`bats`, `fzf` and `shellcheck`. Pre-commit hooks are installed automatically.

## Dataset Editing

All prompt templates live in `dataset/templates.json`. Edit this file directly or
use `scripts/parse_rawdata.py --write` to regenerate it from `dataset/rawdata.txt`.
Both shell and Python paths read this JSON, so changes take effect consistently.


## Architecture

![architecture](docs/architecture.png)

The system is composed of shell wrappers that call into Python utilities for
loading the dataset and plugins. Each script resolves its own directory using
`SCRIPT_DIR="$(cd "$(dirname \"${BASH_SOURCE[0]}\")" && pwd)"` ensuring
location agnostic execution. See `docs/ADR-0001.md` for full design
decisions. Once installed run `man prompts` to read the full manual.

## Extending with Plugins

Additional option packs can be dropped into `plugins/` as JSON, YAML or
Markdown files. Refer to `docs/ADR-0001.md` for plugin design guidelines.

