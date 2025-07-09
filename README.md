# prompts.sh

Interactive prompt builder for Sora/Hailuo workflows. The script asks for each slot in sequence and copies the final prompt to the clipboard using `wl-copy`.

## Usage

```bash
./prompts.sh --interactive
```

The script requires:
- `fzf` for menu selections
- `wl-clipboard` for clipboard support

Install on Arch Linux:

```bash
sudo pacman -S fzf wl-clipboard
```

The CLI supports Wayland only and exits if `wl-copy` is missing.
