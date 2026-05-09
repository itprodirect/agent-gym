# Codex Session Template

Copy this template into a new Codex run when the task should stay small, auditable, and PR-ready.

## Objective

State the goal in one paragraph:

> Complete `<specific outcome>` by changing `<files or areas>`, validating with `<commands or checks>`, and stopping when `<completion criteria>`. Do not change `<out-of-scope areas>`.

## Scope

- In scope:
- Out of scope:
- Risky areas that require approval:

## Checkpoints

1. Inspect repo state, branch, relevant files, and existing docs.
2. Make the smallest useful diff.
3. Run validation.
4. Audit the result against the objective.
5. Summarize changed files, validation, risks, and next step.

## Validation

Record commands before the run:

```bash
git diff --check
```

Add project-specific commands when they exist:

```bash
python -m pytest -q
```

## Handoff summary

Use this shape at the end:

- Changed files:
- Validation:
- Not changed:
- Known gaps:
- Next recommended experiment:

## Stop conditions

Pause and ask before:

- Reading or printing secrets.
- Deleting, overwriting, or moving broad file sets.
- Adding dependencies, services, auth, databases, or build tooling.
- Expanding beyond the stated goal.
- Continuing after repeated validation failures.
