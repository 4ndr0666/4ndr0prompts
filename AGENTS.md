<!-- ────────────────────────────────────────────────────────────────────── -->
<!--  AGENTS.md  ·  Minimal Orchestration Manifest (Post-Simplification)   -->
<!--  For 4ndr0prompts: Pure FZF, Pure Slot-by-Slot, Pure Arch/Wayland     -->
<!-- ────────────────────────────────────────────────────────────────────── -->

# AGENTS — 4ndr0prompts

> **Mission:**  
> Build the world’s simplest, production-grade prompt builder for Sora/Hailuo.  
> Launching `prompts.sh` starts the only supported mode: slot-by-slot prompt creation, with each canonical category handled via fzf, output preview, and instant clipboard copy via wl-copy.  
> All logic, categories, slot order, and options are defined and enforced in promptlib.py—no other data source exists.

*Repository*: <https://github.com/4ndr0666/4ndr0prompts>  
*Generated*: 2025-07-07  
*Maintainer*: 4ndr0666  

---

## 0 · Table of Contents
1. Executive Summary  
2. Canonical File Tree Snapshot  
3. Roles & Streams  
4. Ticket Matrix  
5. Detailed Ticket Specifications  
6. Approval Rubric  
7. Contribution Workflow  
8. Further Enhancements  
9. Glossary  

---

## 1 · Executive Summary

All prior modes, flags, or platform compatibility are removed.  
`prompts.sh` is the only interface; it always launches the interactive builder.

- **Single command**: `./prompts.sh`
- **Flow**: For each slot (in the order defined in promptlib.py), present options via fzf; require explicit selection.
- **Output**: Preview assembled prompt.  
- **Clipboard**: Copy final prompt to clipboard with `wl-copy` (Wayland-only).
- **No fallback**: If `wl-copy` not found, exit with error and colored message.
- **No plugins, no YAML/JSON, no shell flags, no alternate code paths.**

---

## 2 · Canonical File Tree Snapshot

```

.
├── AGENTS.md
├── bin/
│   └── prompts.sh
├── promptlib.py
├── tests/
│   ├── cli.bats
│   └── test\_promptlib.py
├── README.md
├── man1/
│   └── prompts.1.scd
├── .gitignore
└── Makefile

```

---

## 3 · Roles & Streams

| Prefix | Stream           | Responsibilities                                         |
|--------|------------------|---------------------------------------------------------|
| SHE    | Shell Engineering| POSIX script, slot-by-slot fzf flow, clipboard copy     |
| PYL    | Python Library   | Maintain promptlib.py, slot/category canonicalization   |
| QA     | Quality Assurance| End-to-end test harness, bats/expect automation         |
| DOC    | Documentation    | README, man-page, usage instructions                    |
| INF    | Infrastructure   | Repo hygiene, Makefile, .gitignore, test runner         |

---

## 4 · Ticket Matrix

| ID       | Stream | Title                                            | Prio | Est. hrs |
|----------|--------|--------------------------------------------------|------|----------|
| 100-001  | SHE    | Pure slot-by-slot interactive prompts.sh         | P0   | 3        |
| 100-002  | SHE    | Enforce wl-copy only; error if missing           | P0   | 1        |
| 100-003  | PYL    | Canonicalize slot list/order in promptlib.py     | P0   | 2        |
| 100-004  | QA     | Bats/expect: test slot sequence and clipboard    | P0   | 2        |
| 100-005  | DOC    | Trim README/man-page to minimal usage flow       | P0   | 1        |
| 100-006  | INF    | Purge legacy files and .gitignore cleanup        | P0   | 1        |

---

## 5 · Detailed Ticket Specifications

---

### 100-001 · SHE · Pure slot-by-slot interactive prompts.sh

**Goal:**  
Rewrite `bin/prompts.sh` so it always performs slot-by-slot prompting, with no optional flags or modes.

**Scope:**  
- When invoked, prompts user for each slot (in order from promptlib.py) using fzf.
- Each slot's options are extracted directly from promptlib.py (via python call).
- Assembles prompt, displays preview, copies via wl-copy.
- If user aborts, exit with code 130 and display warning.

**Acceptance:**  
- [ ] Running `./prompts.sh` presents each slot in canonical order.
- [ ] All values are user-selected via fzf; default selection is first entry.
- [ ] Final prompt shown in terminal, then copied to clipboard with wl-copy.

---

### 100-002 · SHE · Enforce wl-copy only; error if missing

**Goal:**  
Remove all clipboard tool detection except wl-copy.

**Scope:**  
- Only support wl-copy for clipboard copy.
- If not found, exit with `[ERROR]` in red and suggest `sudo pacman -S wl-clipboard`.

**Acceptance:**  
- [ ] Final prompt copied if wl-copy exists.
- [ ] If not, script aborts with clear message; nothing is written to clipboard.

---

### 100-003 · PYL · Canonicalize slot list/order in promptlib.py

**Goal:**  
Enforce one and only one slot/category list/order in promptlib.py.

**Scope:**  
- All slot names, allowed values, and order defined in a single list or OrderedDict in promptlib.py.
- No YAML/JSON/data files needed for runtime.

**Acceptance:**  
- [ ] `promptlib.py` exports the full slot list (e.g., `SLOTS = [...]`).
- [ ] All slot option lists are unique, complete, and validated at import.

---

### 100-004 · QA · Bats/expect: test slot sequence and clipboard

**Goal:**  
Automate slot-by-slot flow in test harness.

**Scope:**  
- Bats or expect script simulates answering each fzf prompt (use first entry).
- Verifies that output matches expected slot ordering and is copied to clipboard.
- If `wl-paste` is available, test confirms clipboard content matches prompt.

**Acceptance:**  
- [ ] `make test` or CI run passes all tests, including clipboard assertion.

---

### 100-005 · DOC · Trim README/man-page to minimal usage flow

**Goal:**  
No fluff, just minimal usage.

**Scope:**  
- Remove all reference to non-Arch, non-Wayland, non-wl-copy setups.
- Show one usage example: `./prompts.sh` (interactive).
- Document each slot and its possible values, referencing promptlib.py.

**Acceptance:**  
- [ ] README and man-page have ≤ 200 lines each.
- [ ] No irrelevant or out-of-date info present.

---

### 100-006 · INF · Purge legacy files and .gitignore cleanup

**Goal:**  
Clean as the code: only keep what’s essential.

**Scope:**  
- Remove all unneeded JSON/YAML, legacy scripts, test artefacts, or cross-platform helpers.
- Add .gitignore lines for pycache, logs, editor backups, and venvs.

**Acceptance:**  
- [ ] Only AGENTS.md, bin/prompts.sh, promptlib.py, README.md, man1/prompts.1.scd, tests/, .gitignore, Makefile remain.
- [ ] Repo is clean after `make clean`.

---

## 6 · Approval Rubric

| Area          | Threshold                | Audit Method      |
|---------------|-------------------------|-------------------|
| Flow          | Only slot-by-slot mode  | Manual/test run   |
| Clipboard     | Only wl-copy; no xclip  | CLI + bats/expect |
| Slot Options  | Only from promptlib.py  | Code review       |
| Tests         | ≥95% coverage           | CI                |
| Docs          | Minimal and accurate    | Doc review        |

---

## 7 · Contribution Workflow

1. Branch (`feat/<id>-short-title`)
2. `make test` before commit
3. PR with `[SHE]`, `[PYL]`, `[QA]`, etc. in title
4. Pass code-owner review and CI
5. Merge

---

## 8 · Further Enhancements

- If you need “plugins”/“packs”, add a single future ticket:  
  **Support plugin pack loading from a single Markdown or Python module.**
- If Sora/Hailuo API integration needed, new ticket:  
  **Add HTTP endpoint for direct Sora upload (optional, after slot-by-slot is rock solid).**

---

## 9 · Glossary

- **Slot:** Category/question (e.g., Age, Gender, Lighting)
- **fzf:** Command-line fuzzy finder
- **wl-copy:** Wayland clipboard utility
- **promptlib.py:** The only source of slot/category logic and allowed values
- **Bats:** Bash Automated Testing System

---

<!-- END OF AGENTS.md -->
