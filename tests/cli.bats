#!/usr/bin/env bats

setup() {
  cd "$BATS_TEST_DIRNAME/.."
  mkdir -p tmp
  export PATH="$PWD/tmp:$PATH"
  printf '#!/bin/sh\ncat > /dev/null' > tmp/wl-copy
  printf '#!/bin/sh\nhead -n1' > tmp/fzf
  chmod +x tmp/wl-copy tmp/fzf
}

teardown() {
  rm -rf tmp
}

@test "prompts.sh interactive flow" {
  run env FZF_DEFAULT_OPTS="--select-1 --exit-0" bin/prompts.sh
  [ "$status" -eq 0 ]
  first_line=$(echo "$output" | head -n1)
  [ "$first_line" = "cat runs quickly" ]
}
