# AGENTS

Sprinter for the [*4ndr0prompts*](https://www.github.com/4ndr0666/4ndr0prompts) project which aims to ensure that *“build a prompt → copy it → feed it to Hailuo/Sora”* works seamlessly on **Arch Linux**.

---

## Work Tickets (Finalized for Production-Ready Deployment)

| ID         | Stream | Title                                                        | Dependencies   | Priority | Est. hrs |
| ---------- | ------ | ------------------------------------------------------------ | -------------- | -------- | -------- |
| **50-001** | SHE    | Align CLI with unified dataset format                        | 10-005,10-004  | P0       | 3        |
| **50-002** | DOC    | Complete README and usage docs                               | 20-001         | P0       | 4        |
| **50-003** | SHE    | Clipboard robustness on Arch (xclip & fallback)              | 30-001         | P1       | 2        |
| **50-004** | CI     | Add release workflow & container build                       | 20-003,10-007  | P1       | 5        |
| **50-005** | QA     | Integrate Bats & coverage in CI                              | 10-006         | P1       | 2        |
| **50-006** | QA     | Generate SBOM and document threat model                      | 10-007         | P2       | 3        |
| **50-007** | ARC    | ADR-0001: Plugin system guidelines                           | 30-003         | P2       | 2        |
| **50-008** | PYL    | Schema validation for dataset config                         | 30-002,50-001  | P3       | 3        |
| **60-001** | INF    | Add `.gitignore` and cleanup repository hygiene              | 10-001         | P1       | 1        |
| **60-002** | DOC    | Finalize Man-Page (`prompts.1.scd`)                          | 20-002,50-002  | P1       | 2        |
| **60-003** | INF    | Implement `make setup` and `Makefile`                        | 50-002         | P1       | 2        |
| **60-004** | INF    | Purge stale `__pycache__` directories                        | 50-001         | P1       | 1        |
| **60-005** | QA     | Complete integration tests (end-to-end flow)                 | 50-005         | P1       | 3        |
| **60-006** | DOC    | Finalize Architecture ADR (ADR-0001.md)                      | 50-007         | P1       | 2        |
| **60-007** | INF    | Clean dataset directory (remove `nsfwprompts.txt` if unused) | 50-001         | P2       | 1        |
| **60-008** | INF    | Standardize YAML/JSON dataset conversion script              | 50-001         | P2       | 2        |
| **70-001** | SHE    | Universal script-path resolution (`SCRIPT_DIR` fix)          | 60-001         | P0       | 2        |

---

## Detailed Finalization Tickets

### 50-001 SHE – Align CLI with unified dataset format
**Goal:** Single source of truth for templates & slots.
**Details:**
- Update `bin/prompts.sh` and `bin/choose_prompt.sh` to load from `dataset/templates.json` via `prompt_config` or `canonical_loader`.
- Remove or deprecate `data/templates.yaml` & `data/slots.yaml`.
- Standardize placeholder syntax (`[slot]`) across shell and Python.
**Acceptance Criteria:**
- `bin/prompts.sh` output matches `promptlib_cli.py` for a given template.
- Only one dataset format exists (JSON).
- Bats tests adjusted to pass with unified data.
- README documents dataset location and editing.

---

### 50-002 DOC – Complete README and usage docs
**Goal:** Bring documentation in line with actual repo structure and usage.
**Details:**
- Expand README with Quick-Start (`make setup`, dependencies).
- Add **Architecture** section explaining the flow (picker → generator → clipboard).
- Complete `man1/prompts.1.scd` content, include installation.
- Link to ADR-0001 in docs.
**Acceptance Criteria:**
- Quick-Start works verbatim on Arch Linux.
- Architecture diagram visible and explained.
- README covers Arch-only clipboard notes.
- `prompts.1.scd` builds via `scdoc` without errors.
- All references in docs match actual file names.

---

### 50-003 SHE – Clipboard robustness on Arch (xclip & fallback)
**Goal:** Guarantee prompt copy works reliably on Arch Linux.
**Details:**
- Detect `DISPLAY` and `command -v xclip`; if found, copy to clipboard; else print to stdout with a warning.
- Add Bats tests for both `xclip` present and absent cases.
- Document Arch-only clipboard expectation in README.
**Acceptance Criteria:**
- On Arch with `xclip`, prompt is copied.
- Without `xclip`, fallback prints cleanly.
- Tests cover both scenarios.
- README notes “Arch only: uses xclip; fallback to stdout”.

---

### 50-004 CI – Add release workflow & container build
**Goal:** Automate packaging & release.
**Details:**
- Create `release.yml` on Git tag: build tarball, Docker image (Alpine+bash+fzf+python3+pyyaml), push to GHCR.
- Generate CycloneDX SBOM with `cyclonedx-py`.
- Update `CHANGELOG.md` automatically via Conventional Commits.
**Acceptance Criteria:**
- On `vX.Y.Z` tag: Release created with tar.gz, Docker image, SBOM attached.
- SBOM includes all deps.
- Tarball + image reproduce prompt output.
- CHANGELOG entry present.

---

### 50-005 QA – Integrate Bats & coverage in CI
**Goal:** Improve test automation & coverage.
**Details:**
- Configure CI to install & run `bats` on `test/*.bats`.
- Integrate `pytest-cov` for Python, enforce ≥95% coverage.
- Ensure `fzf` is available in CI for shell tests.
**Acceptance Criteria:**
- CI runs Bats & pytest, all green.
- Coverage report shows ≥95% (or agreed threshold).
- Badge or summary added to README.

---

### 50-006 QA – Generate SBOM and document threat model
**Goal:** Produce SBOM & threat model for compliance.
**Details:**
- Use `cyclonedx-bom` to generate `sbom.json` in CI.
- Write a brief `SECURITY.md` or ADR section: identify plugin spoofing, clipboard risks, supply-chain threats.
**Acceptance Criteria:**
- SBOM JSON present in repo or attached to releases.
- Threat model doc identifies ≥4 scenarios & mitigations.
- Document reviewed by maintainer.

---

### 50-007 ARC – ADR-0001: Plugin system guidelines
**Goal:** Finalize ADR for plugin discovery & usage.
**Details:**
- Document rationale for plugins, supported formats (JSON/YAML/Markdown), category normalization (lowercase, underscores).
- Provide guidelines for plugin authors in ADR.
**Acceptance Criteria:**
- `docs/ADR-0001.md` has Context, Decision, Consequences, Alternatives.
- ADR matches `plugin_loader.py` implementation.
- README references ADR.

---

### 50-008 PYL – Schema validation for dataset config
**Goal:** Validate prompt dataset structure early.
**Details:**
- Define JSON Schema (`docs/dataset.schema.json`) enforcing `templates: map<string,string>`, `slots: map<string,map<string,array<string>>>`.
- Implement `make validate` to run `jsonschema` check.
- Optionally integrate into pre-commit.
**Acceptance Criteria:**
- Schema file exists & covers placeholders vs slots.
- `make validate` fails on schema violations.
- Tests demonstrate catch of mismatches.

---

### 60-001 INF – Add `.gitignore` and cleanup repository hygiene
**Goal:** Ensure proper repo hygiene.
**Details:**
- Add `.gitignore` for `__pycache__/`, `*.pyc`, editor swaps (`*.swp`, `*.bak`).
- Remove temporary files.
**Acceptance Criteria:**
- Fresh clone + `git status` shows no untracked caches.
- `.gitignore` covers all temp patterns.

---

### 60-002 DOC – Finalize Man-Page (`prompts.1.scd`)
**Goal:** Complete detailed man-page.
**Details:**
- Populate `man1/prompts.1.scd` with NAME, SYNOPSIS, DESCRIPTION, OPTIONS, EXAMPLES.
- Ensure scdoc builds it to man format.
**Acceptance Criteria:**
- `scdoc man1/prompts.1.scd > prompts.1` produces a valid man page.
- Contents match CLI functionality.

---

### 60-003 INF – Implement `make setup` and `Makefile`
**Goal:** Streamline environment setup.
**Details:**
- Add `Makefile` with `setup`, `validate`, `clean`, `test`, `bench`.
- `make setup` installs Python deps and Arch packages (`pacman -Sy fzf bats shellcheck`).
**Acceptance Criteria:**
- `make setup` completes without errors.
- README updated to use `make setup`.

---

### 60-004 INF – Purge stale `__pycache__` directories
**Goal:** Remove compiled bytecode clutter.
**Details:**
- `make clean` removes all `__pycache__` in repo.
- `.gitignore` entry prevents their tracking.
**Acceptance Criteria:**
- After `make clean`, no `__pycache__` remain.
- Git ignores them going forward.

---

### 60-005 QA – Complete integration tests (end-to-end flow)
**Goal:** Comprehensive end-to-end test coverage.
**Details:**
- Bats script (`test/test_scripts.bats`) runs `choose_prompt.sh` → `prompts.sh`, asserts expected prompt text.
- Include tests for fallback clipboard (stdout).
**Acceptance Criteria:**
- CI runs integration tests, all pass.
- Tests cover both clipboard and fallback.

---

### 60-006 DOC – Finalize Architecture ADR (`ADR-0001.md`)
**Goal:** Fully document architectural decisions.
**Details:**
- Expand `docs/ADR-0001.md` with plugin system rationale, discovery, normalization.
- Include future considerations (ADR-0002 placeholder).
**Acceptance Criteria:**
- ADR reviewed & approved.
- README links to ADR.

---

### 60-007 INF – Clean dataset directory (`dataset/`)
**Goal:** Remove redundant dataset files.
**Details:**
- Audit `dataset/`; remove `nsfwprompts.txt` if unused.
- Ensure only `rawdata.txt`, `templates.json`, `options.json` remain.
**Acceptance Criteria:**
- Post-clean, dataset dir contains only active files.
- `make validate` regenerates JSON from `rawdata.txt`.

---

### 60-008 INF – Standardize YAML/JSON dataset conversion script
**Goal:** Automate YAML ↔ JSON conversion.
**Details:**
- Provide `scripts/convert_dataset.py` that reads `templates.yaml` → writes `templates.json` and vice versa.
- Include tests in pytest suite.
**Acceptance Criteria:**
- Conversion script works idempotently.
- CI invokes conversion as part of `make validate`.

---

### 70-001 SHE – Universal script-path resolution (`SCRIPT_DIR` fix)
**Goal:** Make shell scripts location-agnostic.
**Details:**
- Add at top of each shell script:
  ```bash
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
````

* Use `$SCRIPT_DIR/...` and `$REPO_ROOT/...` for all relative references.
* Update tests to call scripts from multiple CWDs.
  **Acceptance Criteria:**
* All scripts run correctly from any working directory.
* Bats tests in CI cover both repo root and `bin/` invocations.
* README notes “Path-resolution best practices.”

---

## Roadmap for Production-Ready Deployment

| Sprint | Targets                                         | Tickets                                       |
| ------ | ----------------------------------------------- | --------------------------------------------- |
| **1**  | CLI alignment, Documentation, Initial CI setup  | 50-001,50-002,50-005,60-001,60-003,**70-001** |
| **2**  | Clipboard hardening, Release automation         | 50-003,50-004,50-006,60-002,60-005            |
| **3**  | Plugin & schema documentation, Architecture ADR | 50-007,50-008,60-006                          |
| **4**  | Final infra cleanup & dataset standardization   | 60-004,60-007,60-008                          |

---

## Infrastructure & Automation Overview

* **GitHub Actions**

  * `ci.yml`: lint (ruff), shellcheck, shfmt, pytest, bats, coverage.
  * `release.yml`: on tag → build tarball, Docker image, generate & upload SBOM.

* **Makefile**

  * `setup` (installs Arch packages + pip deps).
  * `validate` (schema & dataset regeneration).
  * `clean` (purges caches).
  * `test` (runs both pytest & bats).
  * `bench` (runs hyperfine).

* **Pre-commit Hooks**

  * Ruff, Black, ShellCheck, shfmt, pytest, bats, codex-merge-clean.

---

## Approval Rubric (Go/No-Go)

| Category      | Passing Threshold                      | Verification                |
| ------------- | -------------------------------------- | --------------------------- |
| Unit Tests    | ≥ 95% coverage                         | pytest-cov & bats coverage  |
| Static Lint   | 0 errors, ≤5 warnings                  | pre-commit checks           |
| Build         | Deterministic tarball & Docker image   | CI build digests comparison |
| Performance   | Prompt gen <50 ms avg                  | hyperfine benchmarks        |
| Security      | SBOM attached; threat model documented | CI SBOM step + SECURITY.md  |
| Documentation | README, ADR, man-page complete         | Maintainer review           |

---

## Contribution Workflow

1. Fork & branch off `main` (`feat/ID-short-title`).
2. `make setup` → install dependencies & hooks.
3. Develop & commit (Conventional Commits + `Signed-off-by`).
4. `pre-commit run --all-files` must pass.
5. Push & open PR → assign reviewers by Stream.
6. Merge on green CI & semantic-release tag.

