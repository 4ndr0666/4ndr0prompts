#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
hyperfine --warmup 1 -n prompts './bin/prompts.sh' --max-runs 3 --export-markdown test/benchmark.md
