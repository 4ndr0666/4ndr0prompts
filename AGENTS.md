# AGENTS.md — 4ndr0prompts Best Practices & General Policy

---

## Agentic Principles

* **Single-Path UI/UX:**  
  No fallback, alternate, or legacy TUI/GUI code. All interface logic, style, and menus exist in `promptlib_cli.py` alone.

* **No Redundant I/O or Imports:**  
  Never introduce new files or imports solely for UX, color, style, or data-sharing. Any style, color, or prompt logic must be in the main CLI script.

* **Dynamic, Verbatim Dataset:**  
  All category and slot logic must be fully dynamic—always loaded at runtime from `dataset/templates.json`.  
  Data must be presented **verbatim**, including misspellings and adversarial examples. No sanitization.

* **prompt_toolkit is Mandatory:**  
  The CLI must depend on prompt_toolkit and auto-install it if missing before any user interaction.  
  No alternative interface or dependency allowed.

* **Fuzzy Search is Required:**  
  All menus and prompt logic must use prompt_toolkit’s fuzzy completer for category and slot selection, especially for large datasets.

* **Colorized, Actionable Errors:**  
  All errors, prompts, and status outputs must be colorized using a centralized style block. Messages must be actionable and logged.

* **Auditability:**  
  Every prompt generation, slot choice, and error must be audit-logged with timestamp, category, and text. Logs must be append-only and protected.

* **Strict Lint/Automation:**  
  All code must be `ruff`/`black`/`shellcheck` clean, enforced by pre-commit on every file.  
  All scripts require a shebang and pass shellcheck/shfmt.

* **Documentation Currency:**  
  The README and --help must always describe only the canonical workflow (no reference to TUI or fallback), and list all dynamic categories from the dataset.

* **Test Coverage:**  
  All dataset-driven UI paths must be covered in tests (pytest/CI).  
  Tests must be updated if dataset/templates.json or CLI paths change.

* **No Unjustified Refactor:**  
  Any proposal to break the monolithic structure or add new files/modules must include a clear technical rationale (performance, scalability, research necessity) and must be approved by project lead before implementation.

* **Security & Adversarial First:**  
  Security research and adversarial use-cases always take priority over user convenience or aesthetic. Never compromise verbatim data or audit trails for UI polish.

---

## General Notes

- Use only `prompts.sh` as the CLI entrypoint.  
- Any ambiguity or non-trivial architectural decision must be escalated to the project lead before execution.
- All team members are expected to enforce these policies during review and QA.

---
