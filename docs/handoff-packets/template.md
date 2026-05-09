# Handoff Packet: <Project Or Repo Name>

## Runner

- Intended runner: Codex / Claude Code / human reviewer
- Source ticket or prompt:
- Target branch:
- Scorecard:

## Objective

<State the concrete outcome in one paragraph.>

## Context

<Summarize what the next agent needs to know before touching files. Include links to prior PRs, docs, plans, or scorecards.>

## Inspect First

- `README.md`
- `AGENTS.md`
- `<relevant docs or source files>`

## Constraints And Non-Goals

- In scope:
- Out of scope:
- Do not add:
- Data/safety boundaries:

## Validation Commands

```bash
python -m pytest -q
git diff --check
```

## Stopping Condition

<Describe exactly when the run is complete and what evidence must exist.>

## Pause Conditions

- Secrets, credentials, or real client data appear.
- Scope expands beyond the packet.
- Validation fails repeatedly.
- The task requires cloud services, auth, databases, external integrations, or destructive commands.
- The expected PR summary no longer matches the diff.

## Expected PR Summary

- Changed files:
- Validation:
- Not changed:
- Known risks:
- Next recommended step:

## Review Checklist

- [ ] The agent inspected the listed files before editing.
- [ ] The diff matches the objective and non-goals.
- [ ] No unrelated files, secrets, generated caches, or local scratch outputs are included.
- [ ] Validation commands ran and results are recorded.
- [ ] The stopping condition was met.
- [ ] A scorecard was linked or created.
