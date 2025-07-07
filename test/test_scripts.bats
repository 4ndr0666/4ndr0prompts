#!/usr/bin/env bats
# SPDX-License-Identifier: MIT

setup() {
  cd "$BATS_TEST_DIRNAME/.."
}

@test "choose_prompt.sh selects hello" {
  run env FZF_DEFAULT_OPTS="--filter=hello --select-1 --exit-0" bin/choose_prompt.sh
  [ "$status" -eq 0 ]
  [ "$output" = "hello" ]
}

@test "prompts.sh prints formatted prompt" {
  run env FZF_DEFAULT_OPTS="--filter=hello --select-1 --exit-0" bin/prompts.sh
  [ "$status" -eq 0 ]
  [ "$output" = "Hello World" ]
}
