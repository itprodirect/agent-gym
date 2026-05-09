# Codex Goals

Use goals when a Codex run needs a clear end state, validation gate, and stopping rule. A good goal should be small enough for one PR and specific enough that another contributor can audit it from the diff.

## Goal shape

A practical goal usually includes:

- The exact artifact or behavior to create.
- The files or areas that are in scope.
- The files, systems, or decisions that are out of scope.
- The validation command or manual check that proves completion.
- The stopping condition, including when to pause and ask.

## Good goals

These goals are specific, reviewable, and testable:

- "Create `docs/session-template.md` with a checklist for future Codex runs, update `README.md` to link it, and run `git diff --check`. Do not edit application code."
- "Harden `apps/repo_bootstrapper/writer.py` so dry-run performs no writes and path traversal is rejected. Add offline tests for overwrite, absolute paths, and `..` segments. Run `python -m pytest -q`."
- "Add `--save-plan` and `--load-plan` to the repo bootstrapper CLI. Keep live API calls out of tests, document the flags in `README.md`, and stop if the schema needs a new dependency."
- "Review PR comments on the current branch, implement only actionable doc comments, run `git diff --check`, and summarize any comments left unresolved."

## Bad goals

These goals are too broad, unclear, or risky:

- "Make the repo production ready."
- "Fix all security issues and improve the architecture."
- "Add cloud deployment, auth, and persistence so this becomes a full platform."
- "Clean up the project however you think is best."
- "Use the latest best practices everywhere."

## Better rewrites

Turn broad requests into bounded work:

- Instead of "make docs better", use "add a README section linking AGENTS.md and the three workflow docs, then run `git diff --check`."
- Instead of "fix the bootstrapper", use "change file writing so `--dry-run` makes no filesystem changes, add one regression test, and avoid dependency changes."
- Instead of "prepare for CI", use "document the current local validation command and list CI as a future experiment without adding workflow files."

## Completion checklist

Before closing a goal, verify:

- The requested files exist and contain the requested content.
- The diff excludes unrelated app code, credentials, generated caches, and dependency changes.
- Validation ran, or the reason it could not run is recorded.
- Remaining risks and next experiments are explicit.
