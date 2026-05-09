# Handoff Packet: Claims Demo Data Factory Plan

## Runner

- Intended runner: Codex or Claude Code
- Source ticket or prompt: Create or replay a safe claims demo bootstrap plan
- Target branch: `feat/<short-claims-demo-task>`
- Scorecard: [claims demo data factory plan experiment](../../docs/goal-scorecards/claims-demo-data-factory-plan-experiment.md)

## Objective

Replay or extend the Claims Demo Data Factory bootstrap plan as a fake-only demo-data seed for Agent Lab, IT Pro Direct, `claims-intelligence-foundation`, policy-dispute tools, or Merlin-style demos.

## Context

Agent Gym now has reproducible bootstrap plans. The claims demo plan is committed at `examples/plans/claims-demo-data-factory.plan.json` and has already been replayed without calling the agent. The sample project must remain local-only and must not become a production claims application.

## Inspect First

- `README.md`
- `AGENTS.md`
- `docs/current-state.md`
- `docs/goal-scorecards/claims-demo-data-factory-plan-experiment.md`
- `examples/plans/README.md`
- `examples/plans/claims-demo-data-factory.plan.json`
- `apps/repo_bootstrapper/cli.py`
- `apps/repo_bootstrapper/plans.py`

## Constraints And Non-Goals

- In scope: fake demo fixtures, local replay instructions, docs, tests for any code changes.
- Out of scope: production app code, real claims workflows, claim outcome recommendations, legal advice.
- Do not add: cloud services, auth, databases, external integrations, GitHub API calls, or Agent Lab coupling.
- Data/safety boundaries: use fake, non-sensitive demo data only; no real client, claimant, policy, medical, financial, or legal data.

## Validation Commands

```bash
python -m apps.repo_bootstrapper --out _scratch/claims-demo-data-factory-replay --package claims_demo_data_factory --load-plan examples/plans/claims-demo-data-factory.plan.json
python -m pytest -q
git diff --check
```

If the replayed sample is changed, also run:

```bash
python -m pytest -q
```

from inside the replayed `_scratch/claims-demo-data-factory-replay` directory.

## Stopping Condition

Stop only when the plan or docs are updated, the offline replay still works, validation results are recorded, and the branch contains only the intended local files.

## Pause Conditions

- Real client data, secrets, or identifying claim details appear.
- The task starts requiring legal advice or claim-handling guidance.
- The work needs cloud services, auth, databases, external integrations, or Agent Lab production APIs.
- Validation fails repeatedly.
- The diff grows beyond the stated demo-plan scope.

## Expected PR Summary

- Changed files: plan/docs/tests touched by the specific task.
- Validation: replay command, repo tests, `git diff --check`, and generated-project tests if applicable.
- Not changed: production Agent Lab code, external integrations, secrets, real claims data.
- Known risks: generated content needs human safety review before reuse in claims-related repos.
- Next recommended step: create or update the goal scorecard for the run.

## Review Checklist

- [ ] The agent inspected the listed files before editing.
- [ ] The diff keeps fake-data boundaries clear.
- [ ] No real client data, legal advice, cloud services, auth, databases, or external integrations were added.
- [ ] Offline replay worked without relying on a live agent call.
- [ ] Validation commands ran and results are recorded.
- [ ] Scorecard link is present or a new scorecard was added.
