# 🚦 **AGENTS.md — Monolithic Best Practices and Operating Policy**

```markdown
# AGENTS.md (Best Practices / Guidelines)

---

* **Single-Entry Workflow**: All CLI, UX, and dataset logic centralized in one script (promptlib_cli.py); entry via prompts.sh only.
* **No extraneous files/imports for UX/color/style—logic remains in the main CLI.**
* **prompt_toolkit is required and auto-installed before any CLI runs.**
* **All category and slot logic must be fully dynamic, loaded at runtime from dataset/templates.json.**
* **Menus and prompt logic must always use fuzzy completers for large datasets.**
* **Verbatim Data Policy**: All data, including misspellings/adversarial content, is preserved and displayed exactly as found in dataset.
* **All error messages are colorized and actionable; fatal errors halt execution.**
* **No fallback modes, alternate flows, TUI, or GUI (strict monolithic model).**
* **Codebase must always be ruff/black/shellcheck clean, with pre-commit hooks enforced.**
* **Documentation (README, CHANGELOG) must reflect current entrypoints, workflows, and test coverage.**
* **Tests must cover all dataset-driven UI paths and error flows.**
* **No structural refactor or new modules/files unless justified by resource, security, or research needs (document justification in PR).**
* **Security, research, and adversarial rigor always take precedence over convenience or visual polish.**
* **All team communication and PRs should reference AGENTS.md and CODEX.md for acceptance.**

---

**This document remains the authoritative guide for policy, best practice, and compliance. All new development and reviews must be aligned to these principles.**
```

---

## **How to Use**

* **CODEX.md:** For project management, sprint planning, technical work orders, and cross-team delegation.
* **AGENTS.md:** As the standing operating procedure and policy anchor—reference for every PR, commit, or onboarding.
