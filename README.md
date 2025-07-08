# 4ndr0prompts

Minimal prompt builder for Wayland systems. This tool assembles text prompts from predefined slots using `fzf` for selection and copies the result to the clipboard with `wl-copy`.

## Usage

```
$ bin/prompts.sh
```

Each slot is presented in order. Choose one option per slot and the final prompt is copied to your clipboard.

## Requirements

- `fzf`
- `wl-clipboard`
- Python 3.11+

Slots are defined in [promptlib.py](promptlib.py). Edit that file to customise available options.

Test suite can be run with:

```
$ make test
```
