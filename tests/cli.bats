#!/usr/bin/env bats

setup() {
	mkdir -p "$BATS_TEST_TMPDIR/bin"
        cat <<'SH' >"$BATS_TEST_TMPDIR/bin/fzf"
#!/usr/bin/env bash
# pick first option
cat | head -n1
SH
        chmod +x "$BATS_TEST_TMPDIR/bin/fzf"

	cat <<'SH' >"$BATS_TEST_TMPDIR/bin/wl-copy"
#!/usr/bin/env bash
cat >"$BATS_TEST_TMPDIR/clipboard"
SH
	chmod +x "$BATS_TEST_TMPDIR/bin/wl-copy"

	PATH="$BATS_TEST_TMPDIR/bin:$PATH"
}

@test "interactive flow copies clipboard" {
	run "$BATS_TEST_DIRNAME/../prompts.sh" --interactive
	[ "$status" -eq 0 ]
	grep -q "Age" "$BATS_TEST_TMPDIR/clipboard"
}
