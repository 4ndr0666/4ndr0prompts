# AGENTS.md (Best Practices / Project Guidelines)

---

- **prompt_toolkit** is mandatory; must be present or auto-installed before CLI runs.
- **Monolithic policy:** Never introduce new files or external imports for UX, color, or style. All logic must be inline in the CLI.
- **Color scheme:** All prompt_toolkit elements must use #15FFFF (neon cyan) for maximum visibility, accessibility, and adversarial review. No deviation.
- **Fuzzy completion everywhere:** Menus, prompts, and all selection logic must always use fuzzy completers for large datasets.
- **Dynamic data only:** All category and slot logic must be loaded live at runtime from dataset/templates.json. No static or hardcoded lists.
- **Slot randomization:** Each prompt generated must randomize slot values, never static or repeated unless requested.
- **Auditability:** All prompts, errors, and outputs must be saved/audit-logged with clear timestamps and traceability for research/review.
- **Colorized error messages:** All errors must be visible, actionable, and use the project color scheme for immediate user feedback.
- **No fallback/TUI/GUI:** Absolutely no alternate modes or UI. If prompt_toolkit is not available, the shell wrapper must install it or exit with error.
- **Automation:** All code must be ruff, black, and shellcheck clean, enforced by pre-commit hooks before any merge.
- **Test coverage:** Automated tests must cover every UI path, error, and audit output, simulating all dataset-driven flows.
- **Documentation:** README and code comments must be up to date, clear, and reflect CLI, data, and style logic.
- **Change management:** Any proposal to break the monolith or add new UI/config files requires explicit written resource/performance justification.
- **Security & research:** Misspellings and adversarial samples in data must never be autocorrected; they must be shown verbatim.
- **Accessibility:** All UI colors and flows must remain accessible to all users, especially for vision and color sensitivity.

---

*All contributors must review AGENTS.md and CODEX.md before any implementation or PR. All major changes require cross-team audit and explicit project lead approval.*
