## 1. **Purpose and Scope**

This document governs all agent-based, automation, and dynamic CLI orchestration logic for this project.
It defines:

* Canonical agent behavior and design principles
* Slot/category-driven workflow requirements
* Dataset ingestion and runtime parameterization
* Security, audit, and compliance mandates
* Testing, validation, and review protocols
* Ticket structure, workstream, and escalation
* Explicit deviation/extension protocol for future contributions

This is a **living project contract**: all tickets, pull requests, and changes must reference relevant sections herein.

---

## 2. **Agent Design and Behavior**

### 2.1 **Modality and Dynamic Loading**

* All slot/category lists (pose, lighting, lens, camera_move, environment, shadow, detail, etc.) **MUST** be dynamically loaded at runtime from the current canonical dataset (`promptlib.py`, plugin YAML/MD, or datasets), never hard-coded.
* Any change to dataset, plugin, or slot definitions **MUST** be hot-reloaded in the CLI.
* **Critical:**  
    - **`redteam_dataset.txt` must be ingested and slotted verbatim.**
    - **No spellchecking, typo correction, or normalization is allowed.**  
      Misspellings, malformed words, and adversarial entries **must** be preserved as-is for adversarial testing integrity.

### 2.2 **CLI Automation & Slot Assignment**

* Only the main CLI script (e.g., `prompts.sh` or `canonical_cli.py`) is permitted to instantiate agents.
* Interactive slot/category menus **MUST** use dynamic fuzzy completers that reflect current, live slot values.
* All prompt data from any dataset or plugin, including malformed and misspelled entries, **MUST** be shown verbatim to users/agents—no cleaning or formatting.
* CLI errors and messages must be colorized using `#15FFFF` or the project highlight.
* All slot and prompt assignment logic **MUST** reside in the main script; do not offload to plugins or submodules.

---

## 3. **Security and Policy Compliance**

* **Policy Enforcement:**  
    - No prompt, slot, or action may contain a restricted or forbidden term (see `promptlib.py` and policy docs).
    - Policy and subject-reference rules **MUST** be enforced at prompt assembly.
* **Redteam Integrity:**  
    - At every stage, the integrity of redteam/adversarial prompts is **paramount**—no normalization, correction, or filtering of content from `redteam_dataset.txt` is allowed.
* All errors and violations must be colorized, explicit, and must prevent further processing.

---

## 4. **Testing, Validation, and Quality Gates**

* **Tests required for:**
    - Dynamic slot loading
    - Menu/input flows
    - Policy/subject reference compliance
    - Fuzzy completion and input handling
    - Edge cases (malformed data, hot-reload, dataset mutation)
* **All slot lists must be unique, deduped, and reflect 100% of all current dataset/plugin entries.**
* All code must pass `ruff` and `black` (Python) and `shellcheck` (Bash).
* **Pre-commit hooks are required** for style and compliance gating.

---

## 5. **Work Ticketing and Review Process**

### 5.1 **Ticketing**

* All new features, changes, or bugfixes **MUST** be logged as tickets referencing AGENTS.md by section and clause.
* Each ticket must state:
    - Purpose and impact (e.g. “Slot expansion for action_sequence from new plugins”)
    - Affected scripts/files
    - Validation and testing plan
    - Expected agent/user change

### 5.2 **Review & Audit**

* No merge/PR is allowed without automated and peer validation against AGENTS.md.
* Deviations from canonical workflow must be explained in ticket, approved by majority, and cross-referenced here.

---

## 6. **Production Release Checklist**

A version is “production-ready” only if:

* [ ] All slots/categories load and reload dynamically from all datasets, plugins, and MD/YAML files
* [ ] The CLI enforces colorized, actionable errors with no fallback or silent failure
* [ ] Prompt generation, menu flows, and slot assignment are **100% automated** and reflect all adversarial/test input
* [ ] All tests pass in CI/CD on a clean container
* [ ] All documentation (README/help) matches current code and agent behavior
* [ ] Security and compliance tests pass
* [ ] No stale/hardcoded/duplicate slot values exist in codebase
* [ ] Tickets/PRs reference this AGENTS.md for traceability

---

## 7. **Escalation and Exception Handling**

* Any CLI, slot, or workflow change must have measurable security or performance gain, documented and reviewed here.
* Any change to dynamic loading, dataset/plugin interface, or slot structure must update AGENTS.md and trigger full re-test.
* Any proposal to break structure must include profiling/benchmarking and audit references.

---

## 8. **Further Enhancements & Roadmap**

* Plugin registry for auto-discovery of slot/category packs
* Full dataset/plugin audit logs, with before/after diffs
* Runtime slot validation hints for user input (without blocking adversarial entries)
* CLI-level metrics for performance and reloads
* Multi-agent orchestration for batch prompt building and attack vector synthesis

---

## 9. **Governance, Amendments, and Living Document Status**

* All contributors must update this contract with any substantive project change.
* All PRs/issues must reference AGENTS.md section/paragraph.
* Major amendments must be signed off and versioned in the repo.

---

## 10. **Machine-Actionable Slot Expansion Protocol**

### **Dynamic Slot Expansion**

- All canonical slots are defined in `promptlib.py:SLOT_MAP`.  
- On ingestion, **every unique prompt from `redteam_dataset.txt` and other sources** must be assigned to one or more slots **verbatim**.
    - Example:  
      - If a prompt describes “back to camera,” add it to `orientation` (even if misspelled).
      - If a prompt is an action sequence, assign to `action_sequence`.
      - If ambiguous, assign to `detail` as a catch-all.
- For slots like `orientation`, **expand options beyond current three values**.  
    - Slot must contain every real orientation found in the data (e.g., "side profile", "overhead", "from behind", etc.).

### **VERBATIM DATA INTEGRITY CLAUSE**

- **Every prompt from `redteam_dataset.txt` must be transcribed and slotted exactly as-is, without spellcheck, correction, or normalization.**
    - *Any agent or human who normalizes or corrects redteam content breaks the adversarial test pipeline and must be removed from the merge/review process.*
    - This is a “break glass” escalation event.

---

## 11. **Current File Tree Snapshot**

```

/mnt/data/
├── redteam\_dataset.txt           # Full adversarial prompt set (all prompts must be slotted verbatim)
├── promptlib.py                  # Canonical slot and prompt definitions (must be exhaustively expanded from all sources)
├── canonical\_loader.py           # Loader/hot-reload logic
├── test\_promptlib.py             # Test harness
├── plugin\_loader.py              # Plugin/MD extractor
├── README.md                     # Usage/docs
├── prompts1.md                   # Additional prompt blocks
├── prompts.sh                    # CLI prompt builder (Wayland/clipboard)
├── \*.yaml                        # Plugin packs

```

---

**MANDATORY REDTEAM CLAUSE:**  
> **At no point may any automation, agent, or human contributor modify, spellcheck, normalize, or “improve” any prompt text from `redteam_dataset.txt`. All misspellings, grammar errors, and adversarial content must remain 100% verbatim throughout ingestion, slotting, and CLI output. Violation triggers immediate escalation and removal from the workflow.**
