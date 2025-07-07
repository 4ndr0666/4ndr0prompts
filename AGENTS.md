# AGENTS

Sprinter for the [*4ndr0prompts*](https://www.github.com/4ndr0666/4ndr0prompts) project which aims to ensure that *“build a prompt → copy it → feed it to Hailuo/Sora”* works seamlessly on Arch Linux.

---

## Work Tickets (Finalized for Production-Ready Deployment)

| ID         | Stream | Title                                                        | Dependencies   | Priority | Est. hrs |
| ---------- | ------ | ------------------------------------------------------------ | -------------- | -------- | -------- |
| **50-001** | SHE    | Align CLI with unified dataset format                        | 10-005, 10-004 | P0       | 3        |
| **50-002** | DOC    | Complete README and usage docs                               | 20-001         | P0       | 4        |
| **50-003** | SHE    | Cross-platform clipboard support (Win/Mac)                   | 30-001         | P1       | 4        |
| **50-004** | CI     | Add release workflow & container build                       | 20-003, 10-007 | P1       | 5        |
| **50-005** | QA     | Integrate Bats & coverage in CI                              | 10-006         | P1       | 2        |
| **50-006** | QA     | Generate SBOM and document threat model                      | 10-007         | P2       | 3        |
| **50-007** | ARC    | ADR-0001: Plugin system guidelines                           | 30-003         | P2       | 2        |
| **50-008** | PYL    | Schema validation for dataset config                         | 30-002, 50-001 | P3       | 3        |
| **60-001** | INF    | Add `.gitignore` and cleanup repository hygiene              | 10-001         | P1       | 1        |
| **60-002** | DOC    | Finalize Man-Page (`prompts.1.scd`)                          | 20-002, 50-002 | P1       | 2        |
| **60-003** | INF    | Implement `make setup` and `Makefile`                        | 50-002         | P1       | 2        |
| **60-004** | INF    | Purge stale `__pycache__` directories                        | 50-001         | P1       | 1        |
| **60-005** | QA     | Complete integration tests (end-to-end flow)                 | 50-005         | P1       | 3        |
| **60-006** | DOC    | Finalize Architecture ADR (ADR-0001.md)                      | 50-007         | P1       | 2        |
| **60-007** | INF    | Clean dataset directory (remove `nsfwprompts.txt` if unused) | 50-001         | P2       | 1        |
| **60-008** | INF    | Standardize YAML/JSON dataset conversion script              | 50-001         | P2       | 2        |

---

## Detailed Finalization Tickets

### 60-001 INF – Add `.gitignore` and cleanup repository hygiene

**Goal:** Ensure proper repository hygiene by creating a comprehensive `.gitignore` file and remove temporary/editor-generated files.
**Acceptance Criteria:**

* `.gitignore` includes entries for common temp files (`*.pyc`, `__pycache__`, editor-specific files like `*.swp`, `*.bak`).
* Running `git status` shows a clean working directory after a fresh clone and test run.

---

### 60-002 DOC – Finalize Man-Page (`prompts.1.scd`)

**Goal:** Complete the detailed man-page content for the `prompts` CLI tool.
**Acceptance Criteria:**

* `prompts.1.scd` fully documents usage examples, options, environment variables, and installation steps.
* Man-page builds cleanly with `scdoc` and matches current functionality exactly.

---

### 60-003 INF – Implement `make setup` and `Makefile`

**Goal:** Streamline environment setup for new contributors/users with a `Makefile`.
**Acceptance Criteria:**

* Executing `make setup` installs all necessary dependencies (Python packages, `fzf`, `shellcheck`, `bats`, etc.).
* The process is repeatable and documented in README.

---

### 60-004 INF – Purge stale `__pycache__` directories

**Goal:** Remove cached bytecode files that clutter the repository.
**Acceptance Criteria:**

* No `__pycache__` directories exist after repository cleanup.
* A `.gitignore` entry prevents future commits of these directories.

---

### 60-005 QA – Complete integration tests (end-to-end flow)

**Goal:** Finalize comprehensive end-to-end integration testing scripts.
**Acceptance Criteria:**

* Integration tests cover the full pipeline (`choose_prompt.sh` → `prompts.sh` → clipboard).
* Tests executed in CI and pass successfully, ensuring workflow consistency.

---

### 60-006 DOC – Finalize Architecture ADR (`ADR-0001.md`)

**Goal:** Fully document the architectural decisions about plugin handling and system interactions.
**Acceptance Criteria:**

* ADR clearly describes current architecture, decision rationale, status, consequences, and future implications.
* Reviewed and approved by the project maintainer.

---

### 60-007 INF – Clean dataset directory (`dataset/`)

**Goal:** Remove redundant or unused datasets from `dataset/`.
**Acceptance Criteria:**

* Confirm `nsfwprompts.txt` and related datasets (`rawdata.txt`, `slots_report.tsv`) are either used actively or removed.
* Final dataset directory contains only actively referenced files (`templates.json`, `options.json`).

---

### 60-008 INF – Standardize YAML/JSON dataset conversion script

**Goal:** Automate and standardize conversion between YAML and JSON dataset files.
**Acceptance Criteria:**

* Provide a clear Python or shell script (`scripts/convert_dataset.py`) that accurately converts between YAML ↔ JSON.
* The script is idempotent, well-tested, and integrated into CI for dataset consistency.

---

## Roadmap for Production-Ready Deployment

| Sprint | Targets                                         | Tickets                                |
| ------ | ----------------------------------------------- | -------------------------------------- |
| 1      | CLI alignment, Documentation, Initial CI setup  | 50-001, 50-002, 50-005, 60-001, 60-003 |
| 2      | Cross-platform support, Release automation      | 50-003, 50-004, 50-006, 60-002, 60-005 |
| 3      | Plugin & schema documentation, Architecture ADR | 50-007, 50-008, 60-006                 |
| 4      | Final infra cleanup & dataset standardization   | 60-004, 60-007, 60-008                 |

---

## Infrastructure & Automation Overview

* **GitHub Actions**

  * `ci.yml`: lint, shellcheck, pytest, bats, coverage.
  * `release.yml`: builds tarballs, Docker images, publishes SBOM.

* **Makefile**

  * `setup`: installs dependencies.
  * `validate`: dataset schema validation.
  * `clean`: removes caches and temp files.

* **Pre-commit hooks**

  * ShellCheck, shfmt, ruff, black, pytest, bats.

---

## Approval Rubric (Go/No-Go)

| Category         | Passing Threshold                           | Audit Method                |
| ---------------- | ------------------------------------------- | --------------------------- |
| Unit Tests       | ≥ 95% statements coverage                   | pytest-cov, bats coverage   |
| Static Lint      | 0 errors, ≤ 5 warnings                      | Pre-commit hooks            |
| CI Status        | All checks green                            | GitHub Checks               |
| SBOM Generation  | CycloneDX SBOM attached                     | Automated CI step           |
| Documentation    | Complete README, ADRs, Man-page             | Doc reviews                 |
| Artifact Quality | Reproducible tarball and Docker image <10MB | CI release validation       |
| Performance      | CLI startup and prompt gen <50ms            | Benchmarked via `hyperfine` |

---

## Contribution Workflow

1. Fork and branch off `main`.
2. Run `make setup`.
3. Develop, commit, run pre-commit hooks.
4. Open PR, assign reviewers by stream.
5. Merge with Conventional Commit messages.
