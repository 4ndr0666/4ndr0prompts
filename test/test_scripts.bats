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

@test "scripts work from bin dir" {
	pushd bin >/dev/null
	run env FZF_DEFAULT_OPTS="--filter=insertion_oral_mouth --select-1 --exit-0" ./prompts.sh
	[ "$status" -eq 0 ]
	[ -n "$output" ]
	popd >/dev/null
}
