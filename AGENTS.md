<!-- ────────────────────────────────────────────────────────────────────── -->
<!--  AGENTS.md  ·  Master Orchestration & Ticket Manifest                 -->
<!--  All variables have been resolved — no {{place-holders}} remain.      -->
<!-- ────────────────────────────────────────────────────────────────────── -->

# AGENTS — Prompts.sh Canonical Slot Expansion & Release Hardening

> **Mission Statement**  
> Deliver an audit-grade, automation-ready ticket ledger and architectural blueprint that brings **Prompts.sh** from its current *pre-release* state to a stable, production-ready release that satisfies modern Dev + Sec + Ops standards while honouring the project’s design principles (minimalism, reproducibility, composability).  
>
> **Non-negotiable constraint:** the file **`redteam_dataset.txt`** must be ingested *verbatim*.  
>   • No spell-checking or “corrections”.  
>   • No hidden normalisation (UTF-8 stays UTF-8; line-feeds stay LF).  
> Misspellings are deliberate and essential for red-team robustness tests.

Repository: <https://github.com/prompts-sh/prompts.sh>  
Generated: 2025-07-09  (America/New_York)  
Maintainer: Prompts.sh Core Maintainers  

---

## 0 · Table of Contents
1. [Executive Summary](#1--executive-summary)  
2. [Current File Tree Snapshot](#2--current-file-tree-snapshot)  
3. [Streams & Roles](#3--streams--roles)  
4. [Ticket Matrix](#4--ticket-matrix)  
5. [Detailed Ticket Specifications](#5--detailed-ticket-specifications)  
6. [Roadmap & Sprint Cadence](#6--roadmap--sprint-cadence)  
7. [Automation & Infrastructure Mandates](#7--automation--infrastructure-mandates)  
8. [Approval Rubric (Go/No-Go)](#8--approval-rubric--go-no-go)  
9. [Contribution Workflow](#9--contribution-workflow)  
10. [Further Enhancements (Post-Release)](#10--further-enhancements--post-release)  
11. [Glossary](#11--glossary)  
12. [Appendix A — Ticket YAML Stub](#appendix-a--ticket-yaml-stub)  
13. [Appendix B — ADR Template](#appendix-b--adr-template)  

---

## 1 · Executive Summary

Prompts.sh currently exposes a **SLOT_MAP** that is both incomplete (e.g., three `orientation` values) and polluted with legacy constructs (`policy_filter`, platform-specific gates, an explicit *redteam* category).  
Key gaps are summarised below.

| Area                           | Gap Summary |
| ------------------------------ | ----------- |
| **Slot Coverage**              | Under-represented options (`orientation`, `pose`, `action_sequence`, etc.). |
| **Dataset Assimilation**       | `redteam_dataset.txt` lines not mapped to canonical slots. |
| **Verbatim Guarantee**         | No automation to assert byte-level integrity of red-team data. |
| **Legacy Code**                | `policy_filter`, Sora/Hailuo conditionals, redundant red-team slot. |
| **CI & Coverage**              | No tests for dataset ingestion; unit coverage < 70 %. |
| **Release Automation**         | Missing SBOM, container image, signed release pipeline. |

The following tickets close every known gap and elevate the codebase to release quality.

---

## 2 · Current File Tree Snapshot
```

.
├── README.md
├── AGENTS.md              # (this file generated into repo root)
├── prompts.sh             # POSIX shell CLI
├── prompts1.md            # prompt pack (markdown)
├── redteam\_dataset.txt    # red-team prompts (must remain verbatim)
├── promptlib.py
├── canonical\_loader.py
├── plugin\_loader.py
├── test\_promptlib.py
├── 200-001.yaml
├── 200-002.yaml
├── 200-003.yaml
├── 200-004.yaml
├── 200-005.yaml
├── 200-006.yaml
├── 200-007.yaml
├── 200-008.yaml
├── 200-009.yaml
└── 200-010.yaml

````
> *The snapshot is authoritative for ticket scoping.*  
> Any file not listed here that appears during work must be justified in its ticket and added to the next snapshot.

---

## 3 · Streams & Roles

| Prefix | Stream / Role              | Core Responsibilities |
| ------ | -------------------------- | --------------------- |
| **ARC**| Architecture & Governance  | ADRs, high-level design, deviation control. |
| **SHE**| Shell Engineering          | POSIX scripts, `fzf` UX, ShellCheck compliance. |
| **PYL**| Python Library Engineering | Slot logic, dataset loaders, schema validation. |
| **CI** | CI/CD Automation           | GitHub Actions, release pipeline, SBOM signing. |
| **QA** | Quality & Security         | Tests, coverage, threat modelling. |
| **DOC**| Documentation              | README, man-pages, ADRs, diagrams. |
| **INF**| Infrastructure             | Makefile, Dockerfile, `.gitignore`, housekeeping. |

---

## 4 · Ticket Matrix

| ID       | Stream | Title                                                             | Dependencies | Priority | Est hrs |
| -------- | ------ | ----------------------------------------------------------------- | ------------ | -------- | ------- |
| **50-001** | PYL | Verbatim ingestion of `redteam_dataset.txt` into SLOT_MAP          | —            | P0       | 4 |
| **50-002** | PYL | Expand all option lists (`orientation`, `pose`, etc.)              | 50-001       | P0       | 3 |
| **50-003** | PYL | Remove `policy_filter`, Sora/Hailuo, red-team-slot code            | 50-001       | P0       | 2 |
| **50-004** | QA  | Unit tests: verify byte-exact integrity & slot counts              | 50-001       | P0       | 2 |
| **50-005** | SHE | Update CLI to consume expanded slot data                           | 50-002       | P1       | 3 |
| **50-006** | CI  | Add CI jobs (`lint`, `unit`, `dataset`, `coverage`)                | 50-004       | P1       | 2 |
| **50-007** | DOC | Rewrite README with new slot docs & quick-start                    | 50-002       | P1       | 2 |
| **50-008** | CI  | Release workflow: Docker image, SBOM, cosign signing               | 50-006       | P1       | 4 |
| **50-009** | INF | Makefile with `setup`, `validate`, `test`, `release` targets       | 50-006       | P1       | 2 |
| **50-010** | QA  | Coverage gate ≥ 95 % (pytest + coverage.py)                         | 50-004       | P1       | 2 |
| **50-011** | ARC | ADR-0001: Dataset ingestion architecture decision                  | 50-001       | P1       | 2 |
| **50-012** | DOC | Man-page `prompts.1.scd`                                           | 50-005       | P2       | 2 |
| **50-013** | QA  | End-to-end CLI ↔ library parity tests                              | 50-005       | P2       | 3 |
| **50-014** | INF | `.gitignore`, cleanup of `__pycache__` and orphan files            | 50-009       | P2       | 1 |

---

## 5 · Detailed Ticket Specifications

### 50-001  PYL  Verbatim ingestion of `redteam_dataset.txt`

**Goal**  
Parse the complete `redteam_dataset.txt` file **without altering any bytes** and map every unique prompt line into its appropriate slot list in `promptlib.SLOT_MAP`.

**Scope**  
* Implement `load_redteam_dataset()` in `promptlib.py`.  
* Deduplicate duplicates **only when byte-for-byte identical**.  
* Assign categories via heuristic mapping:  
  * Mentions of “turn around”, “back to camera” → `orientation_options`.  
  * Mentions of “lean forward”, “kneels”, etc. → `pose`.  
  * Mentions of “opens mouth”, “sucking” → `action_sequence`.  
  * All lines fallback into `action_sequence_options` if no better slot.  
* **Do not** create a separate *redteam* slot.

**Acceptance Criteria**  
1. SHA-256 of `redteam_dataset.txt` pre- and post-pipeline is unchanged.  
2. `promptlib.SLOT_MAP["orientation"]` contains ≥ 10 values, including misspelled ones.  
3. Unit test `test_redteam_verbatim.py` passes and asserts (a) byte-identical ingestion, (b) slot counts.

---

### 50-002  PYL  Expand all option lists

**Goal**  
Elevate every slot list so that real-world use cases are covered.

**Scope**  
* `orientation_options`: add “profile left”, “profile right”, “back view”, “worm’s-eye”, “bird’s-eye”, etc.  
* `pose`: merge new red-team phrases + dedupe.  
* `action_sequence`: append red-team lines.  
* Keep ordering deterministic (`_dedupe_preserve_order`).

**Acceptance Criteria**  
* At least 50 unique `pose` values, 20 `orientation` values, 100 `action_sequence` values.  
* No duplicates when `validate_slots()` runs.

---

### 50-003  PYL  Remove legacy policy/platform code

**Goal**  
Simplify codebase and eliminate dead paths.

**Scope**  
* Delete `policy_filter` function and all call-sites.  
* Strip Sora/Hailuo platform mentions from docstrings and templates.  
* Remove `redteam_cat*` genre keys from `ACTION_SEQUENCE_GENRE_MAP`.  
* Update tests.

**Acceptance Criteria**  
* `grep -R "policy_filter" .` returns 0.  
* `pytest` & `bats` pass.  

---

### 50-004  QA  Dataset integrity tests

**Goal**  
Protect against accidental mutation of `redteam_dataset.txt`.

**Scope**  
* Add `tests/test_dataset_integrity.py`.  
* Compute SHA-256 at import; fail if mismatch with committed value.  
* Parameterise tests to assert every mis-spelled term still present.

**Acceptance Criteria**  
* CI job `dataset` fails on any byte change.

---

### 50-005  SHE  CLI update for expanded slots

**Goal**  
Ensure the shell CLI (`prompts.sh`) reads the enlarged dataset.

**Scope**  
* Use `python -m promptlib.export --json` (new helper) to emit slot JSON to stdout.  
* Replace hard-coded `fzf` lists with dynamic JSON parsing (`jq`).  
* ShellCheck passes (`shellcheck -xo all prompts.sh`).

**Acceptance Criteria**  
* `prompts.sh --interactive` shows new options.  
* Unit snapshot test compares CLI output against library output.

---

### 50-006  CI  Add GitHub Actions pipeline

**Goal**  
Continuous verification on every push.

**Scope**  
* Jobs: `lint` (ruff + shellcheck), `unit` (pytest), `dataset` (integrity), `coverage`, `docker`, `sbom`.  
* Upload coverage to job summary.  
* Build lightweight Alpine image (`<10 MB`) and push to ghcr.io/prompts-sh/prompts.

**Acceptance Criteria**  
* CI green on main; branch protection rules active.

---

### 50-007  DOC  README overhaul

**Goal**  
Reflect new slot logic and provide quick-start.

**Scope**  
* Add architecture diagram (PlantUML).  
* Document dataset rules (verbatim, no corrections).  
* Provide copy-paste install commands for Linux, macOS, WSL2.

**Acceptance Criteria**  
* Markdown link check passes (`markdown-lint`).  
* `asciidoctor` preview builds without warnings.

---

### 50-008  CI  Release workflow, SBOM, signing

**Goal**  
Ship deterministic builds.

**Scope**  
* `release.yml` on tag push:  
  * Build wheel + sdist + Docker image.  
  * Generate CycloneDX JSON SBOM (`pip-licenses`).  
  * Sign assets with `cosign`.  

**Acceptance Criteria**  
* `gh release view` shows SBOM attachment and cosign signature notes.

---

### 50-009  INF  Makefile and repo hygiene

**Goal**  
Single entry point for tasks.

**Scope**  
* Targets: `setup`, `lint`, `test`, `coverage`, `release`, `clean`.  
* Add `.gitignore`, remove orphan `__pycache__` directories.

**Acceptance Criteria**  
* `make test` passes from a clean checkout.  

---

### 50-010  QA  Coverage gate ≥ 95 %

**Goal**  
Bring confidence level up.

**Scope**  
* Add tests for every new slot path.  
* Fail CI if coverage < 95 %.

**Acceptance Criteria**  
* Coverage job passes with ≥ 95 %.

---

### 50-011  ARC  ADR-0001 — Dataset ingestion decision

**Goal**  
Record architectural rationale.

**Scope**  
* Write markdown ADR (see template) explaining why ingestion is verbatim, how categories are mapped, why no spell-correction, and future migration strategy.

**Acceptance Criteria**  
* ADR merged and referenced from README.

---

### 50-012  DOC  Man-page `prompts.1.scd`

**Goal**  
Provide POSIX-style documentation.

**Scope**  
* Write man-page in `scdoc` flavour.  
* Document CLI flags, environment variables, examples.

**Acceptance Criteria**  
* `scdoc < prompts.1.scd > /dev/null` returns 0.

---

### 50-013  QA  End-to-end CLI ↔ library parity

**Goal**  
Prevent divergence.

**Scope**  
* Golden sample (#fixtures) containing user selection JSON and expected prompt output.  
* Run test via `pexpect` to drive CLI and compare to library.

**Acceptance Criteria**  
* `pytest tests/test_e2e_cli.py` passes.

---

### 50-014  INF  Clean ancillary files

**Goal**  
Tidy repo.

**Scope**  
* Purge stale caches, unused plugin YAML, dead symlinks.  
* Enforce via `make validate`.

**Acceptance Criteria**  
* `make validate` passes on CI.

---

## 6 · Roadmap & Sprint Cadence

| Sprint | Focus                                                    | Primary Tickets           | Duration |
| ------ | -------------------------------------------------------- | ------------------------- | -------- |
| **Sprint 1** | Verbatim ingestion, slot expansion, legacy removal      | 50-001 • 50-002 • 50-003 | 5 work-days |
| **Sprint 2** | Integrity tests, CI pipeline, README                      | 50-004 • 50-006 • 50-007 | 5 work-days |
| **Sprint 3** | CLI integration, ADR, Makefile, coverage gate            | 50-005 • 50-009 • 50-010 • 50-011 | 5 work-days |
| **Sprint 4** | Release workflow, man-page, E2E tests, repo cleanup      | 50-008 • 50-012 • 50-013 • 50-014 | 5 work-days |

---

## 7 · Automation & Infrastructure Mandates

| Domain            | Requirement                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| **Dataset Integrity** | CI job `check-redteam` calculates committed SHA-256; fails if changed.                           |
| **Spell-Lock**   | Linting excludes `redteam_dataset.txt` via `.ruff.toml` and `.codespellrc`.                         |
| **SBOM**          | CycloneDX JSON generated by `cyclonedx-python`.                                                   |
| **Docker**        | Alpine base, final image `<10 MB`, published to `ghcr.io/prompts-sh/prompts`.                     |
| **Pre-commit**    | Hooks: ruff, black, isort, shellcheck (`-x`), shfmt, pytest, bats, dataset-integrity.             |
| **Performance**   | Prompt generation pipeline <= 50 ms average on GitHub runner (`hyperfine`).                       |

---

## 8 · Approval Rubric (Go/No-Go)

| Area                      | Threshold / Condition                               | Verification           |
| ------------------------- | --------------------------------------------------- | ----------------------- |
| **Dataset Integrity**     | SHA-256 unchanged; tests pass.                      | `dataset` job          |
| **Slot Coverage**         | Orientation ≥ 10, Pose ≥ 50, ActionSequence ≥ 100.  | `validate_slots()`     |
| **Unit + Shell Tests**    | All pass; coverage ≥ 95 %.                          | `coverage` job         |
| **Static Analysis**       | 0 Ruff errors; 0 ShellCheck warnings (SC2000-SC2999).| `lint` job             |
| **Release Artefacts**     | Wheel, sdist, Docker image, SBOM, cosign signature. | `release` job          |
| **Documentation**         | README, man-page, ADR-0001 complete; diagrams render.| Maintainer review      |

A failure in any row results in **NO-GO** for release.

---

## 9 · Contribution Workflow

1. Fork → create feature branch (`feat/50-###-short-title`).  
2. Run `make setup` to install hooks.  
3. Code → commit using Conventional Commits (`feat:`, `fix:`, etc.) and `Signed-off-by`.  
4. `pre-commit run --all-files` passes locally (including dataset integrity).  
5. Push → open PR → assign reviewers by Stream tag (`ARC`, `SHE`, …).  
6. Address review → squash-merge.  
7. Maintainer triggers release when `main` hits a tag.

---

## 10 · Further Enhancements (Post-Release)

| Idea                             | Value Proposition                         | Effort |
| -------------------------------- | ----------------------------------------- | ------ |
| fzf *preview-pane* showing prompt diff | Easier debugging of prompt expansions   | Medium |
| Template versioning via SemVer tags     | Rollback / reproducibility              | Medium |
| Textual-based TUI web server             | GUI fallback for non-terminal users     | Large |

---

## 11 · Glossary

| Term / Acronym | Definition |
| -------------- | ---------- |
| **Verbatim**   | Byte-exact copy; no transformations, no re-encoding. |
| **SBOM**       | Software Bill of Materials, CycloneDX JSON. |
| **ADR**        | Architecture Decision Record. |
| **Bats**       | Bash Automated Testing System. |
| **Cosign**     | Tool for signing container images and artefacts. |

---

## Appendix A — Ticket YAML Stub
```yaml
id: 50-999
stream: SHE
title: Example Ticket Title
dependencies: []
priority: P3
est_hours: 2
description: |
  One-paragraph overview of the ticket goal.
acceptance_criteria:
  - Bullet list of measurable outcomes.
deliverables:
  - Code file(s) updated
  - Documentation updated
notes: |
  Optional free-form notes, context, or implementation hints.
````

## Appendix B — ADR Template

```md
# ADR-????  –  Short Decision Title
Status: Proposed
Date: 2025-07-09

## Context
Explain the forces at play, business or technical constraints, and why this decision matters now.

## Decision
Describe the specific choice made and the scope of that decision.

## Consequences
Positive and negative results, trade-offs, and future implications.

## Alternatives Considered
List other options and why they were not chosen.
```

---

<!-- END OF AGENTS.md -->
