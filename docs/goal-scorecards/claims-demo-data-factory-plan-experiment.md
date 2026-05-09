# Claims Demo Data Factory Plan Experiment

## Run

- PR / branch: Draft PR, `feat/claims-demo-plan-experiment`
- Goal: Create and test a reusable bootstrap plan for a fake, non-sensitive insurance claims demo data factory.
- Date: 2026-05-09
- Commit / evidence: `examples/plans/claims-demo-data-factory.plan.json`, replayed into `_scratch/claims-demo-data-factory-replay-verified`
- Validation: live `--save-plan` succeeded with the local virtualenv; offline `--load-plan` succeeded with system Python; generated sample tests passed with 3 tests; repo tests passed with 10 tests; `git diff --check` passed.

## Scores

| Criterion | Score | Evidence | Follow-up |
| --- | ---: | --- | --- |
| Inspect-first behavior | 2 | The run inspected README, AGENTS.md, `apps/repo_bootstrapper`, scorecard docs, recent merge context, and repo state before generating or editing artifacts. | Keep this for business-adjacent demos. |
| Scope control | 1 | The committed artifact stayed scoped, but the raw live seed suggested a future external API item and lacked useful fixture content, so safety curation was required. | Do not graduate raw live output without review. |
| Unrelated-file handling | 2 | The pre-existing untracked findings file stayed untouched and was not staged. Scratch outputs stayed under ignored `_scratch/`. | Keep explicit staging. |
| Validation | 2 | Live generation exercised `--save-plan`; replay used system Python without the Agents SDK; generated sample tests and repo tests passed; `git diff --check` passed. | Add a repeatable fixture replay check if this pattern moves to CI. |
| Stopping-condition accuracy | 2 | The run did not stop at plan creation; it replayed the committed plan, tested the generated project, documented evidence, and added this scorecard before commit. | Keep requiring replay evidence for committed plans. |
| PR readiness | 2 | The branch contains a small docs-plus-example-plan diff and no production app code. | Open as a draft PR for review of the fixture content. |
| Usefulness to future Agent Lab / IT Pro Direct / claims workflows | 2 | The curated plan provides a safe fake-data seed for Agent Lab, IT Pro Direct, `claims-intelligence-foundation`, policy-dispute tools, and Merlin-style demos. | Use only as demo fixture infrastructure, not claims guidance. |

Total: `13/14`

## Verdict

- Graduation recommendation: Candidate for controlled reuse with mandatory safety review of generated plans.
- Keep: Replayable plan artifacts, fake-only fixture constraints, generated-project tests, and no-agent replay verification.
- Change before reuse: Strengthen the generator prompt or add a review checklist so unsafe roadmap ideas are caught before commit.
- Best next experiment: Add a small verifier that scans replayed plans for banned terms such as real client data, cloud services, auth, databases, and external integrations.
