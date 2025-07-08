#!/usr/bin/env bats

setup() {
	TESTDIR="$BATS_TEST_TMPDIR"
	mkdir -p "$TESTDIR/bin"
	PATH="$TESTDIR/bin:$PATH"
	export PATH TESTDIR
	cat >"$TESTDIR/bin/fzf" <<SH
#!/usr/bin/env bash
readarray -t lines
echo "${lines[0]}"
SH
	chmod +x "$TESTDIR/bin/fzf"
	cat >"$TESTDIR/bin/wl-copy" <<SH
#!/usr/bin/env bash
cat >"$TESTDIR/clipboard"
SH
	chmod +x "$TESTDIR/bin/wl-copy"
	cat >"$TESTDIR/bin/wl-paste" <<SH
#!/usr/bin/env bash
cat "$TESTDIR/clipboard"
SH
	chmod +x "$TESTDIR/bin/wl-paste"
}

@test "interactive flow copies prompt" {
	run "$BATS_TEST_DIRNAME"/../bin/prompts.sh
	[ "$status" -eq 0 ]
	run wl-paste
	[ -n "$output" ]
}
