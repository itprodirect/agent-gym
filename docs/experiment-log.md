# Experiment Log

Use this log to track Codex workflow experiments. Keep entries short, factual, and tied to observable results.

## Current foundation checkpoint log

| Date | Checkpoint | Result |
| --- | --- | --- |
| 2026-05-09 | Inspect repo state | Existing `README.md` and `AGENTS.md`; missing `docs/`; empty `pyproject.toml`; tests directory present; unrelated untracked findings file left untouched. |
| 2026-05-09 | Scope foundation docs | Limit this PR to README navigation and workflow docs. No cloud services, auth, databases, dependencies, or app code changes. |
| 2026-05-09 | Add workflow docs | Created goal examples, experiment-log template, and session template; updated README navigation. |
| 2026-05-09 | Validation fix | Scoped pytest to committed `tests/` so ignored `_scratch/` demo repos do not break local validation. |
| 2026-05-09 | Validate foundation PR | `python -m pytest -q` passed with 4 tests; `git diff --check` passed. |

## Entry template

### YYYY-MM-DD - Experiment name

- Goal:
- Setup:
- Steps:
- Expected result:
- Actual result:
- Validation:
- Follow-up:

## Planned workflow experiments

### /goal behavior

- Goal: Confirm that goal mode preserves a concrete objective, reports progress, and stops only after the completion criteria are met.
- Setup: Start from a clean feature branch with a small docs-only task.
- Steps:
  - Start a goal with one clear deliverable and one validation command.
  - Ask Codex to read back the active goal.
  - Complete the deliverable.
  - Confirm the goal is marked complete only after validation.
- Validation: Record the final goal status, elapsed time, and any mismatch between requested and completed work.

### Memories

- Goal: Check whether stable repo preferences can be recalled without copying them into every prompt.
- Setup: Use non-secret preferences only, such as documentation tone or preferred validation commands.
- Steps:
  - Save a harmless preference.
  - Start a later session that should use it.
  - Verify whether the preference affects the session.
- Validation: Note whether behavior changed and whether the memory was useful, stale, or too broad.

### External migration

- Goal: Test whether a Codex session can be resumed or migrated with enough context to continue safely.
- Setup: Prepare a branch with a small unfinished docs task and a written checkpoint.
- Steps:
  - Stop after a checkpoint.
  - Resume in the migrated context.
  - Ask Codex to identify the latest state before editing.
- Validation: Confirm the resumed session does not redo completed work or overwrite unrelated changes.

### Terminal resize reflow

- Goal: Observe whether long command output stays readable after resizing the terminal.
- Setup: Use non-secret output, such as `git diff --stat` or a docs-only diff.
- Steps:
  - Run the command at one terminal width.
  - Resize the terminal.
  - Review whether wrapping and prompts remain usable.
- Validation: Record any readability issues and whether the command output needs shorter formatting.

### Prevent-sleep behavior

- Goal: Verify whether long Codex tasks continue when the machine would otherwise sleep.
- Setup: Use a safe long-running local command or manual timer, not a live API call.
- Steps:
  - Start the task.
  - Allow the normal idle period to pass.
  - Check whether the session and terminal remain active.
- Validation: Record whether the run completed, paused, or needed system-level sleep settings.
