# AGENTS.md (Best Practices/Guidelines Only)

---

* **Never introduce new files or imports for UX/color/style sharing; keep logic in the main CLI script.**
* **prompt\_toolkit** is required and must be present or auto-installed before any CLI runs.
* **All category and slot logic must be fully dynamic and loaded at runtime from dataset/templates.json.**
* **Menus and prompt logic must always use fuzzy completers for large datasets.**
* **Any data (including misspellings and adversarial samples) must be presented verbatim.**
* **All error messages must be colorized and actionable.**
* **No fallback modes, alternate flows, or TUI/GUI.**
* **All code must be ruff/black/shellcheck clean and pre-commit enforced.**
* **Documentation must be up-to-date, usage clear, entrypoint single.**
* **Tests must cover all dataset-driven UI paths.**
* **Any proposal to break monolithic structure must be justified with clear resource/performance gains.**
* **Security and adversarial research always take precedence over convenience.**

---
