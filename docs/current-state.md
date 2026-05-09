# Current State: Agent Gym Goal Experiments

Agent Gym is now a small, reviewable sandbox for turning Codex `/goal` runs into reproducible agent workflow patterns. It is a proving ground for reusable plans, handoff packets, scorecards, and safe docs/examples that can later support Agent Lab and business workflows.

## Completed PRs

- PR #2: Added the Codex workflow sandbox foundation: goal examples, session template, experiment log, README navigation, and pytest scoping.
- PR #3: Added reproducible bootstrap plans with `--save-plan` and `--load-plan`, schema validation, offline replay tests, and README usage.
- PR #4: Added Goal Behavior Scorecards to judge whether `/goal` runs were trustworthy enough to reuse.
- PR #5: Added and tested the Claims Demo Data Factory plan as a fake-only, replayable example for claims-adjacent demos.
- PR #7: Added the handoff packet foundation for Codex, Claude Code, and future Agent Lab runs.
- PR #8: Added a handoff packet for Agent Lab issue #65, "Records Browser: add runs records page".
- Agent Lab PR #101: Used the handoff packet to implement the saved run records browser.
- PR #9: Added the Agent Gym scorecard for Agent Lab PR #101.

See [session-closeout-2026-05-09.md](session-closeout-2026-05-09.md) for the concise full-loop checkpoint.

## What `/goal` Proved

The runs showed that `/goal` is useful when the prompt has a concrete artifact, explicit scope boundaries, validation commands, and a stopping condition. The strongest pattern was:

1. Inspect the repo first.
2. Make a small diff.
3. Validate with real commands.
4. Commit only intended files.
5. Audit the result against the original goal before stopping.

The scorecards also showed a practical weakness: raw live generation should not be trusted directly for business-adjacent artifacts. PR #5 needed human safety curation before the generated plan was appropriate to commit.

The full loop now has stronger evidence: a handoff packet drove a real Agent Lab implementation, Agent Lab PR #101 merged, Claude Code post-reviewed the merged implementation, and an Agent Gym scorecard captured the reuse verdict.

## What Reproducible Plans Enable

Saved plans make agent-generated scaffolds reviewable, replayable, and testable without another agent call. They are useful for:

- Replaying a known-good scaffold offline.
- Reviewing generated files before writing them.
- Building fixture seeds for demos and experiments.
- Comparing live generation against curated committed output.
- Moving from "the agent made something once" to "we can rerun this safely."

## Why the Claims Demo Plan Matters

The Claims Demo Data Factory plan is the first business-adjacent proof point. It uses fake, non-sensitive insurance claims fixtures only and explicitly avoids real client data, legal advice, cloud services, auth, databases, and external integrations.

That makes it a safe seed for:

- Agent Lab experiments that need realistic-but-fake claim records.
- IT Pro Direct workflow demos with controlled fixture data.
- `claims-intelligence-foundation` prototypes that should start from demo data, not client data.
- policy-dispute tools that need test fixtures before domain logic.
- Merlin-style sales demos that need repeatable local examples.

## Next Highest-Alpha Feature

Come back fresh and use the same handoff packet -> Codex implementation -> review -> scorecard loop for Agent Lab issue #64: saved ideas search/sort.

Keep Claude's PR #101 minor follow-ups as optional cleanup/test follow-ups, not blockers:

- remove redundant `projectDisplayName` handling in run records mapping
- add deterministic same-`createdAt` ordering coverage for run records
- plan for pagination when records pages need scale

After that, add a lightweight plan verifier.

The verifier should load a plan and check for:

- schema validity
- required files
- path safety
- fake-data constraints for demo plans
- banned scope indicators such as real client data, legal advice, cloud services, auth, databases, and external integrations

This is higher-alpha than adding more templates because it turns the lessons from PR #5 into a reusable quality gate for future Agent Lab, IT Pro Direct, and claims-related work.
