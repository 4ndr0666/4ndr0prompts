# AGENTS

Sprinter for the [*4ndr0prompts*](https://www.github.com/4ndr0666/4ndr0prompts) project which aims to ensure that *“build a prompt → copy it → feed it to Hailuo/Sora”* works seamlessly on Arch Linux. 

---

## Work Tickets 

| ID         | Stream | Title                                      | Dependencies   | Priority | Est. hrs |
| ---------- | ------ | ------------------------------------------ | -------------- | -------- | -------- |
| **50-001** | SHE    | Align CLI with unified dataset format      | 10-005, 10-004 | P0       | 3        |
| **50-002** | DOC    | Complete README and usage docs             | 20-001         | P0       | 4        |
| **50-003** | SHE    | Cross-platform clipboard support (Win/Mac) | 30-001         | P1       | 4        |
| **50-004** | CI     | Add release workflow & container build     | 20-003, 10-007 | P1       | 5        |
| **50-005** | QA     | Integrate Bats & coverage in CI            | 10-006         | P1       | 2        |
| **50-006** | QA     | Generate SBOM and document threat model    | 10-007         | P2       | 3        |
| **50-007** | ARC    | ADR-0001: Plugin system guidelines         | 30-003         | P2       | 2        |
| **50-008** | PYL    | Schema validation for dataset config       | 30-002, 50-001 | P3       | 3        |

**50-001 SHE – “Align CLI with unified dataset format”**
*Goal:* Ensure the `prompts.sh` pipeline uses the single source of truth for templates/slots.
*Details:* Update `bin/prompts.sh` (and `choose_prompt.sh` if needed) to load data via the canonical JSON (`dataset/templates.json`) using the `prompt_config` module or by generating updated YAML on-the-fly. Remove or regenerate the YAML files if they are to be used. Standardize placeholder style (use either `{slot}` or `[slot]` across both shell and Python paths).
*Acceptance Criteria:*

* Running `bin/prompts.sh` produces the same prompt output as the Python library (`promptlib_cli`) for a given template (no divergence between JSON vs YAML data).
* The templates/slots exist in **only one format** in the repo (JSON or YAML), and all code references that format exclusively.
* The Bats tests for `prompts.sh` and `choose_prompt.sh` are adjusted (if needed) and all pass using the unified dataset.
* Document in README the location/format of the dataset (so users know where to edit prompts).

**50-002 DOC – “Complete README and usage docs”**
*Goal:* Bring documentation in line with the actual repo structure and usage, improving newcomer experience and compliance.
*Details:* Expand the README with accurate setup instructions (e.g., list required packages: `fzf`, `xclip`, Python libs; or provide a `make setup` script to install these). Include an **Architecture** section explaining the diagram in `docs/architecture.png` – covering how the shell and Python components interact (from template selection to clipboard copy). Add usage examples (e.g., how to run with `fzf`, what happens on different OS). Ensure the Quick-Start is functional or fix it (implement `make setup` or remove that line). Complete the man page `prompts.1.scd` with all commands, options (if any), environment variables, etc., and instructions on how to install the man page. Link the man page and ADR in the README.
*Acceptance Criteria:*

* **Quick-Start instructions can be followed verbatim** on a fresh system to get a working installation (including any missing steps like installing `fzf` or running pre-commit hooks).
* Architecture diagram is visible and accompanied by text explaining the prompt generation flow (shell picker → Python generator → clipboard) and how this achieves the Hailuo/Sora use-case.
* The README usage section covers Windows and Mac notes (e.g., “on Windows, ensure PowerShell 5+ is available”; “on Mac, install pbcopy or use stdout mode”).
* `man1/prompts.1.scd` is fully written and, when processed with scdoc, produces a man page that covers the CLI’s purpose, usage, and examples.
* All documentation references (README, ADR, man page) are up-to-date with the code (no references to non-existent commands or files).

**50-003 SHE – “Cross-platform clipboard support (Windows & Mac)”**
*Goal:* Extend the `prompts.sh` script (and any relevant CLI code) to support copying the prompt to clipboard on Windows and macOS, not just Linux.
*Details:* Implement detection of OS type in the shell script. For Windows, use PowerShell’s `Set-Clipboard` or `clip.exe` if available. For macOS, use the `pbcopy` command. Ensure that if those are not available, the script gracefully falls back to stdout (as it does now for missing `xclip`). This may involve calling `pwsh -c Set-Clipboard` from Git Bash or detecting the presence of PowerShell Core. Testing should be done on those platforms to verify functionality.
*Acceptance Criteria:*

* On a Windows machine, running `prompts.sh` copies text to the clipboard using PowerShell (verify by pasting afterwards). If PowerShell isn’t in PATH, it should print the prompt as fallback.
* On macOS, running `prompts.sh` uses `pbcopy` to copy to clipboard (verify by pasting). If `pbcopy` is unavailable, fallback works.
* Linux behavior with `xclip` remains unchanged.
* The solution does not introduce heavy dependencies – use native OS tools only, aligning with the minimal philosophy.
* Cross-platform checks are covered in documentation (README notes which OS are supported and what is needed) and, if possible, simple integration tests (maybe a dry-run flag to test selection logic on different OS).

**50-004 CI – “Add release workflow & container build”**
*Goal:* Automate the packaging and release of the CLI, producing reproducible artifacts (including a Docker image) and updating the changelog.
*Details:* Create a GitHub Actions workflow (e.g., `release.yml`) triggered on version tags. It should build a tarball or single-binary (if using something like PyInstaller or shc to bundle shell+python, though a tarball with script + data might suffice given minimal deps). Also build a minimal Docker image (as specified: Alpine base with `bash`, `fzf`, `python3`, `pyyaml`) that contains the tool in `/usr/local/bin`. Push this image to GHCR with the tag. Generate the CycloneDX SBOM as part of the release process (possibly using a tool like `cyclonedx-py` to list Python deps and including manual entries for `fzf`). Update CHANGELOG.md for the new version (perhaps enforce Conventional Commit messages to auto-generate it). Optionally, publish documentation via GitHub Pages if relevant (though not explicitly needed if README is sufficient).
*Acceptance Criteria:*

* Upon pushing a Git tag (e.g., `v0.1.0`), the GH Action runs and **produces a Release** on GitHub with: (a) a tar.gz of the CLI scripts, (b) a Docker image published to GHCR, and (c) a CycloneDX SBOM JSON attached to the release.
* The SBOM includes all relevant components (the Python environment, PyYAML, etc.) and is generated automatically. A manual security review (threat model) document is added to `docs/` or the release notes to satisfy the “threat-model” portion of 10-007.
* The CHANGELOG.md is updated with an entry for this release (date, version, highlights of tickets done) and is included in the release notes.
* Verification: installing the tool from the tarball or running the Docker container allows a user to invoke `prompts.sh` and generate a prompt identical to running from source (ensuring reproducibility of behavior across environments).

**50-005 QA – “Integrate Bats tests and coverage reporting in CI”**
*Goal:* Improve test automation by running shell tests and measuring coverage in CI, moving toward the 95% coverage goal.
*Details:* Update the CI workflow to run `bats` on the test files in `test/`. This might involve installing Bats (e.g., using a bats GH Action or `apt-get install bats`). Ensure that if `fzf` is needed for these tests, it’s available in the CI runner (may need to install `fzf` in the pipeline). Additionally, integrate a Python coverage tool (pytest-cov) to track test coverage. Enforce that coverage stays above a threshold (e.g., fail if coverage < 90%). The pre-commit could also be extended with a coverage check if desired.
*Acceptance Criteria:*

* The CI run invokes Bats and the existing shell tests execute, confirming that `choose_prompt.sh` and `prompts.sh` work as expected in the pipeline (headless environment with `FZF_DEFAULT_OPTS` trick). Any failures are fixed or tests adjusted.
* CI produces a coverage report for Python tests. The statement coverage is ≥ 95% or a justified lower threshold, as per the rubric. If current coverage is lower, tests are added (for example, tests for `prompt_config.generate_prompt` random behavior or `canonical_loader`) until the goal is met.
* The repository can include a badge or printed summary of coverage in the CI logs for transparency.
* All test jobs (lint, pytest, bats) must pass green for a PR to merge (ensuring regression safety across shell and Python code paths).

**50-006 QA – “Generate SBOM and document threat model”**
*Goal:* Satisfy the security and compliance requirements by producing an SBOM and performing a basic threat model.
*Details:* Use a tool to generate a CycloneDX SBOM of the project. For Python, the dependencies are minimal (possibly just PyYAML and prompt\_toolkit if using the advanced CLI). Include the OS-level components if relevant (fzf, bash). This can be done as part of 50-004’s release process, but here we ensure it’s tracked. Also, conduct a threat modeling exercise focusing on potential abuses (e.g., malicious prompt plugins, clipboard security, supply-chain attacks on dependencies). Document this in a `SECURITY.md` or in the wiki. Key points could include: the tool runs locally so primary threat is malicious plugin files or malicious prompts causing unwanted clipboard content; mitigation could be code scanning or sandboxing plugin parsing. Since no secrets are used (per AGENTS.md), the model can be brief.
*Acceptance Criteria:*

* An SBOM file (CycloneDX JSON) is present in the repository or attached to releases, listing all components and their versions. It should be generated by an automated process (script or CI job) to avoid human error.
* A short **Threat Model** document is added (could be an ADR or `SECURITY.md`). It identifies at least 3-4 potential threat scenarios and how the design mitigates them or plans to mitigate them (for example: plugin files are treated as data, but perhaps caution the user to only use trusted plugins; ensure the script doesn’t execute arbitrary code from templates, etc.).
* The SBOM and threat model meet the acceptance: the SBOM can be verified (e.g., using `cosign` if signed, per future scope), and there is evidence of a security review process for the project.

**50-007 ARC – “ADR-0001: Plugin system guidelines”**
*Goal:* Finalize the architecture decision record for plugin discovery and usage, to guide contributors and users in extending the prompt dataset.
*Details:* Write the ADR detailing how the plugin system is designed. This should cover the **rationale** (why allow plugins – to extend prompt options without modifying core dataset), the **approach** (file formats supported: YAML, JSON, Markdown; how files are loaded and merged by `plugin_loader`), and the **guidelines** for plugin authors (e.g., allowed category names and their normalization, avoiding duplicates, ensuring items are lists of strings, etc.). It should also mention any future considerations (like ADR-0002 placeholder in ideas for a plugin marketplace). Essentially, it explains how to correctly create a plugin pack and how the system incorporates it via `plugins/` directory.
*Acceptance Criteria:*

* `docs/ADR-0001.md` is updated from its current stub to a complete document that includes: Context, Decision, Status, and Consequences sections (standard ADR format). It specifically addresses plugin discovery guidelines as intended by ticket 30-003.
* The ADR content matches the implementation in `plugin_loader.py` (for example, it lists the supported file extensions and the fact that keys are normalized to lowercase underscored categories).
* It is reviewed and approved by the ARC role (or project maintainer) as accurately capturing the design. This ADR should make it possible for an outside developer to create a new plugin file and know it will be picked up correctly.
* Reference the ADR in README or CONTRIBUTING guide where plugin development is mentioned.

**50-008 PYL – “JSON Schema validation for dataset”**
*Goal:* Add an optional step to validate the prompt dataset (templates/slots) against a schema to catch errors early.
*Details:* Define a JSON Schema for the `templates.json` structure (or YAML equivalent if still used). The schema should enforce that `templates` is a map of string -> string, and `slots` is a map of string -> map of string -> list of strings. It can also enforce no dangling placeholders in templates that don’t have a corresponding slots list (and vice versa). Implement a check in `prompt_config.load_config()` or a separate validation function that runs in CI or on startup to validate the dataset. This could use Python’s `jsonschema` library (if adding is acceptable under simplicity constraints, otherwise a custom check). Since this is optional (P3), it could be behind a flag or only in test mode.
*Acceptance Criteria:*

* A JSON Schema file (e.g., `docs/dataset.schema.json`) is created, covering the structure of templates/slots. It should define required fields and basic types (string vs array).
* A test (or a pre-commit hook) is added that loads the schema and validates `dataset/templates.json` against it. If the data doesn’t conform, it should raise an error. For example, if a template contains `{name}` but the slots for that category don’t have `name`, that is a schema violation to catch.
* Intentionally introduce a small error (e.g., add a bad entry) to ensure the validation fails, then fix it – demonstrating it works.
* This validation does not significantly slow down the CLI (so maybe it runs only in CI or as a separate command, not every execution of `prompts.sh`). Possibly integrate it into the test suite or a `make validate` command.
* Documentation in ADR or README notes that the dataset format is schema-checked for integrity, improving reproducibility and trustworthiness of the prompt generation (no unexpected missing slots at runtime, etc.)
