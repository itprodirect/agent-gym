# Handoff Packet: Agent Lab Issue #65 - Runs Records Page

## Runner

- Intended runner: Codex or Claude Code
- Repo: `itprodirect/agent-lab`
- Issue: [#65 Records Browser: add runs records page](https://github.com/itprodirect/agent-lab/issues/65)
- Target branch: `feat/records-runs-page`
- Scorecard: `<add Agent Gym scorecard link after the implementation run>`

## Objective

Add a records page for saved runs so run history can be browsed outside the Workbench Run Log section.

The first slice should add a `/records/runs` route, or the simplest equivalent route that matches Agent Lab's existing routing conventions.

## Context

Agent Lab already has workbench run logging. This issue asks for a separate records browsing surface for saved runs, not a new run execution workflow. The implementation should reuse existing data access, UI, and navigation patterns wherever possible.

This packet is local to Agent Gym. It is meant to be copied into a Codex or Claude Code session opened in the Agent Lab repo. Do not implement Agent Lab changes inside Agent Gym.

## Inspect First

- `README.md`
- `AGENTS.md`
- `package.json`
- app route/layout files
- records browser routes/pages
- Workbench Run Log components or routes
- saved run data access helpers
- navigation/sidebar definitions
- existing table/list/detail components
- tests for workbench, records pages, routing, or saved runs

Useful local searches inside Agent Lab:

```bash
rg -n "Workbench Run Log|Run Log|saved runs|run history"
rg -n "records|Records Browser|/records"
rg -n "branch|pull request|PR|project|idea"
rg -n "tool|result|logged|createdAt|created_at|date"
rg --files | rg "(app|routes|pages|components|records|workbench|tests)"
```

## Implementation Constraints

- Add a `/records/runs` route or equivalent simple records route.
- List saved runs newest first.
- Show tool, result, project/idea context when available, branch/PR, and logged date.
- Link back to the Workbench context when possible.
- Follow Agent Lab's existing UI, routing, data loading, and test conventions.
- Keep the first slice small and reviewable.

## Non-Goals

- No edit/delete/archive.
- No schema changes unless unavoidable.
- No GitHub API or external integrations.
- No complex filtering in the first slice.
- No broad records browser redesign.
- No unrelated Workbench behavior changes.

## Validation Commands

Run these in the Agent Lab repo after implementation, not from Agent Gym:

```bash
corepack pnpm test
corepack pnpm typecheck
corepack pnpm build
corepack pnpm test:e2e
git diff --check
```

If a command is unavailable or blocked by local setup, record the exact failure and the nearest completed validation.

## Stopping Condition

Stop only when the runs records page is reachable, saved runs are listed newest first, the requested run fields render when available, Workbench context links are present where possible, validation results are recorded, and the diff is limited to issue #65.

## Pause Conditions

- Saved runs do not have a clear local data source.
- The route cannot be added without schema changes.
- Workbench context links require a larger routing or data model change.
- The implementation would require GitHub API calls, external integrations, new auth, or new infrastructure.
- Validation fails repeatedly and the cause is not isolated.
- The diff grows into unrelated records browser or Workbench changes.

## Expected PR Summary

- Changed files: route/page, navigation wiring, focused components, and tests needed for the runs records page.
- Behavior: saved runs can be browsed outside Workbench Run Log; newest runs appear first; tool, result, project/idea context, branch/PR, logged date, and Workbench links appear when data is available.
- Validation: include results for `corepack pnpm test`, `corepack pnpm typecheck`, `corepack pnpm build`, `corepack pnpm test:e2e`, and `git diff --check`.
- Not changed: edit/delete/archive, schema, GitHub API, external integrations, complex filtering, unrelated Workbench behavior.
- Open questions: note any missing field or link that the current saved-run model cannot support.

## Review Checklist

- [ ] The implementation agent inspected the listed Agent Lab files before editing.
- [ ] The route follows existing Agent Lab routing and records UI patterns.
- [ ] Runs are sorted newest first.
- [ ] Tool, result, project/idea context, branch/PR, and logged date render when available.
- [ ] Workbench context links are present where possible.
- [ ] Empty, loading, and error states match local conventions.
- [ ] No edit/delete/archive behavior was added.
- [ ] No schema changes were made unless clearly justified.
- [ ] No GitHub API calls, external integrations, new auth, or unrelated behavior were added.
- [ ] Validation commands ran or exact blockers were recorded.
- [ ] A scorecard link was added or a scorecard follow-up was opened.

## Copy Into Codex Or Claude Code

Use this as the opening prompt in an Agent Lab workspace:

```text
Use the handoff packet in examples/handoff-packets/agent-lab-issue-65-runs-records-page.md as the task brief. Implement Agent Lab issue #65: "Records Browser: add runs records page." Start by inspecting the files and searches listed under "Inspect First". Keep the first slice scoped to a /records/runs route or local equivalent. List saved runs newest first; show tool, result, project/idea context when available, branch/PR, logged date, and Workbench context links when possible. Do not add edit/delete/archive, schema changes unless unavoidable, GitHub API calls, external integrations, or complex filtering. Run the expected Agent Lab validation commands and end with changed files, validation results, and open questions.
```
