#!/usr/bin/env bats
# SPDX-License-Identifier: MIT

setup() {
	cd "$BATS_TEST_DIRNAME/.." || exit
}

@test "choose_prompt.sh selects category" {
	run env FZF_DEFAULT_OPTS="--filter=insertion_oral_mouth --select-1 --exit-0" bin/choose_prompt.sh
	[ "$status" -eq 0 ]
	[ "$output" = "insertion_oral_mouth" ]
}

@test "prompts.sh prints formatted prompt" {
        run env FZF_DEFAULT_OPTS="--filter=insertion_oral_mouth --select-1 --exit-0" bin/prompts.sh
        [ "$status" -eq 0 ]
        [ -n "$output" ]
}

@test "prompts.sh matches python implementation" {
        seed=42
        run env PROMPT_SEED=$seed FZF_DEFAULT_OPTS="--filter=insertion_oral_mouth --select-1 --exit-0" bin/prompts.sh
        [ "$status" -eq 0 ]
        shell_out="$output"
        python_out=$(env PROMPT_SEED=$seed PYTHONPATH=. python - <<'PY'
import os, random
from canonical_loader import load_canonical
from prompt_config import generate_prompt

seed = os.environ.get("PROMPT_SEED")
if seed is not None:
    random.seed(int(seed))
templates, slots, _ = load_canonical()
template = templates["insertion_oral_mouth"]
slotset = slots["insertion_oral_mouth"]
print(generate_prompt(template, slotset))
PY
)
        [ "$shell_out" = "$python_out" ]
}

@test "scripts work from bin dir" {
	pushd bin >/dev/null
	run env FZF_DEFAULT_OPTS="--filter=insertion_oral_mouth --select-1 --exit-0" ./prompts.sh
	[ "$status" -eq 0 ]
	[ -n "$output" ]
	popd >/dev/null
}
