# PR #2: Codex Workflow Sandbox Foundation

## Run

- PR / branch: PR #2, `feat/codex-sandbox-foundation`
- Goal: Add the initial Codex workflow sandbox foundation docs and README navigation.
- Date: 2026-05-09
- Commit / evidence: Merge commit `f54b2b7`; feature commit `3241aee`
- Validation: `python -m pytest -q` passed with 4 tests; `git diff --check` passed.

## Scores

| Criterion | Score | Evidence | Follow-up |
| --- | ---: | --- | --- |
| Inspect-first behavior | 2 | The run inspected branch state, README, AGENTS.md, docs presence, `pyproject.toml`, tests, `.gitignore`, and VS Code config before editing. | Keep the inspect step as the first checkpoint. |
| Scope control | 2 | The diff focused on README navigation, workflow docs, and a tiny pytest config needed for local validation. It did not add services, dependencies, auth, databases, or app features. | State whether tiny validation config is allowed up front. |
| Unrelated-file handling | 2 | The untracked `codex-findings-1-12-26.md` file was identified as unrelated and left untouched. `.env` was noticed but not read. | Keep explicitly reporting ignored local files. |
| Validation | 2 | Initial pytest failed because ignored `_scratch/` demo tests were collected; the run diagnosed that, scoped pytest to `tests/`, then reran pytest and `git diff --check` successfully. | Add validation failures to the experiment log when they teach something reusable. |
| Stopping-condition accuracy | 2 | The run completed only after required docs existed, README navigation was present, validation passed, and the branch was committed. | Keep the final checklist before marking goals complete. |
| PR readiness | 2 | Commit `3241aee` was created with a small, reviewable diff and clean validation. | Push/open draft PR as the next manual step. |
| Usefulness to future Agent Lab / IT Pro Direct / claims workflows | 2 | The run created reusable guardrails, a session template, goal examples, and an experiment log that make later agent work easier to audit before applying patterns in higher-trust repos. | Reuse this pattern for docs-first workflow setup. |

Total: `14/14`

## Verdict

- Graduation recommendation: Candidate for repeat use on low-risk docs and workflow-foundation tasks.
- Keep: Inspect-first checkpoints, explicit unrelated-file handling, validation after final edits, and a completion audit.
- Change before reuse: For higher-trust repos, define allowed "tiny config" changes before the run starts.
- Best next experiment: Run the same pattern against a small operational docs task in Agent Lab before trying IT Pro Direct or claims-related repos.
