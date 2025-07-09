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

* All agent logic **MUST** use dynamic slot/category assignment from the current canonical dataset at runtime (see `promptlib.py`, plugin YAML/MD, or datasets).
* Agent slot options and categories (pose, lighting, lens, camera_move, environment, shadow, detail, etc.) **MUST** be loaded programmatically and never hard-coded in the CLI.
* Agent parameters **MUST** hot-reload if any dataset file is modified, added, or removed.
* **Redteam data integrity:** All prompts from `redteam_dataset.txt` **MUST** be ingested and presented verbatim—including all misspellings, malformed words, nonstandard grammar, and adversarial constructs. **No spellcheck, grammar correction, or content “cleanup” is permitted at any step.**  
  *This is a foundational security requirement: the dataset’s adversarial and edge-case authenticity must never be compromised or normalized by automation or agent.*

### 2.2 **Interface and CLI Automation**

* Only the main CLI script (e.g., `prompts.sh` or `canonical_cli.py`) is permitted to instantiate agents.
* **prompt_toolkit** or equivalent interactive libraries **MUST** be required and auto-installed by the CLI prior to interactive use.
* **Menus and slot completion** must always use fuzzy completers (WordCompleter or equivalent) for all slot/category prompts to support large datasets and arbitrary plugin packs.
* All prompts and slot data (including misspellings, adversarial samples, or malformed entries) **MUST** be presented verbatim.
* All errors must be colorized and actionable, using project-wide color/style constants (cf. `#15FFFF` highlight).
* All CLI automation logic **MUST** remain in the main script. Never move style/UI logic to new files or imports.

---

## 3. **Security and Policy Compliance**

* No prompt, slot, or action may contain a restricted or forbidden policy term (as defined in `promptlib.py` and any OpenAI compliance references).
* Agents **MUST** enforce all subject-reference, policy, and platform rules at the point of prompt construction.
* Security research and adversarial robustness **ALWAYS** take precedence over user convenience or feature expedience.
* All error and policy violation messages must be explicit, colorized, and halt downstream actions.

---

## 4. **Testing, Validation, and Quality Gates**

* All UI and menu flows must be covered by tests (see `test_promptlib.py`).
* **Tests MUST validate:**

  * Each slot/category is present, dynamically loaded, and reflects all current dataset/plugin entries
  * Fuzzy completion, input, and error handling logic
  * Policy compliance for all user and plugin data
  * Edge case handling (malformed data, plugin hot-reload, dataset mutation)
* All code and documentation **MUST** be ruff/black (Python) and shellcheck (Bash) clean.
* **Pre-commit hooks** are required to enforce style, import order, and policy gating.

---

## 5. **Work Ticketing and Review Process**

### 5.1 **Workstream Requirements**

* All new features, refactors, or bugfixes must be logged as tickets referencing relevant AGENTS.md sections.
* Tickets **MUST** include:

  * Clear statement of intent (e.g., “Add new action_sequence slot from plugin ingestion”)
  * Affected modules/files/scripts
  * Testing and validation steps
  * Expected user or agent experience change

### 5.2 **Review and Audit**

* No PR/merge is permitted without automated and peer validation against this contract.
* All review comments and tickets **MUST** use section references for traceability.
* Deviation from canonical workflow **MUST** be justified in the ticket and approved by majority review.

---

## 6. **Production Release Checklist**

A version is “production-ready” only if:

* [ ] All slot/category options hot-reload at runtime from any updated dataset, YAML, MD, or plugin file (see `canonical_loader.py`)
* [ ] The main CLI enforces colorized, actionable errors, with no fallback or silent failure
* [ ] All prompt generation, category/slot ingestion, and menu flows are **100% automated** from current datasets and tested for adversarial input
* [ ] All test suites pass on a clean container environment (CI/CD gating)
* [ ] README and help/usage docs reflect actual live options and agent behaviors
* [ ] Security and compliance tests pass with no forbidden content or subject-reference violations
* [ ] No duplicate, stale, or hard-coded values remain in the codebase
* [ ] Ticket log and AGENTS.md cross-reference all recent changes for audit traceability

---

## 7. **Escalation and Exception Handling**

* Any new CLI mode, slot, or UI/UX workflow **MUST** be justified and approved with measurable security or performance gain.
* Any change to agent dynamic loading, dataset structure, or plugin interface **MUST** update this contract and trigger a full test pass before deployment.
* Proposals to break monolithic structure **MUST** be documented with clear benchmarks, profiling output, and audit log references.

---

## 8. **Further Enhancements & Roadmap**

* **Plugin pack registry:** Support for auto-discovering and registering new slot/category packs from external sources.
* **Dataset audit trail:** Full logging of dataset/plugin ingestion events with before/after diffs and policy filter results.
* **Contextual slot validation:** Runtime user hints if input does not match canonical slot values (without blocking exploration/edge cases).
* **Metrics:** CLI-level metrics/logging for menu performance, plugin reload times, and error rates.
* **Multi-agent orchestration:** Blueprint for parallel agent workflows for batch prompt construction, red team attack vector synthesis, and slot mutation testing.

---

## 9. **Governance, Amendments, and Living Document Status**

This AGENTS.md is a living technical contract.

* All contributors are responsible for reviewing and updating relevant sections with each substantive change.
* All tickets, PRs, and issues must reference AGENTS.md by section and paragraph number.
* Major amendments must be reviewed, signed off, and versioned in the repo log.

---

### **Current File Tree Snapshot**

```

/mnt/data/
├── redteam\_dataset.txt           # Full edge/adversarial prompt set (category headers, many body/camera/action/orientation details; must be transcribed VERBATIM)
├── promptlib.py                  # Canonical promptlib (SLOT\_MAP categories, but with limited options for some slots)
├── canonical\_loader.py           # Loader for canonical slot data, hot-reload capable
├── test\_promptlib.py             # Test harness for slot validation/order
├── plugin\_loader.py              # Plugin extractor for MD files
├── README.md                     # Usage overview for scripts and workflow
├── prompts1.md                   # Additional prompt block definitions
├── prompts.sh                    # CLI prompt builder script (Wayland/clipboard)
├── (plus: \*.yaml plugins, possibly more prompt blocks)

```

---

**MANDATORY REDTEAM CLAUSE:**  
> **At no point may automation, agent, or human contributors modify, spellcheck, normalize, or “improve” any prompt text from `redteam_dataset.txt`. All misspellings, grammar errors, and adversarial content must remain 100% verbatim throughout all ingestion, slotting, and CLI output. Any deviation breaks the core security research and project contract, and must trigger an immediate escalation and ticket review.**
