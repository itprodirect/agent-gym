# AGENTS.md

This repository uses AI assistants (Codex/agents) to help build code.  
These are the **non-negotiable guardrails** for any automated tool and any human contributor.

---

## 1) Safety & trust (highest priority)

### Secrets / sensitive data

- **Never** print, log, paste, or exfiltrate secrets (API keys, tokens, cookies, auth headers).
- Treat the following as secret by default:
  - `.env`, `*.env`, `**/.env*`
  - `~/.codex/config.toml`, `~/.ssh/*`, cloud credentials, browser session data
- If a secret is discovered in the repo history or output:
  - **Stop** and say so.
  - Recommend rotation + removal steps (do not paste the secret back).

### Destructive operations (explicit approval required)

Do **not** run or suggest commands that can delete/overwrite broadly or damage a system without asking first.
Examples (non-exhaustive):

- `rm -rf`, `del /s`, `rmdir /s`, `format`, `diskpart`, `dd`, `mkfs`
- `git reset --hard`, `git clean -fdx`, `git push --force`
- Any command that rewrites history or deletes lots of files

### Network access

- Don’t curl/wget arbitrary scripts or run “pipe to shell” installers.
- Avoid unnecessary network calls. If a task truly needs them, state **what** and **why** before doing it.

---

## 2) How to work in this repo (expected workflow)

### Plan → small diff → test → commit

- Start by stating a short plan (3–7 bullets).
- Prefer **small, reviewable diffs** over big refactors.
- Keep changes scoped to the requested feature/fix.
- Add or update tests for each change where reasonable.

### Keep `main` stable

- Work on feature branches (e.g. `feat/001-repo-bootstrapper`).
- Don’t assume you can merge; make changes in a PR-friendly way.

---

## 3) Code quality standards (Python)

### General

- Favor clarity over cleverness.
- Use type hints where it helps readability.
- Prefer deterministic behavior and explicit errors over “best effort” magic.

### Dependencies

- Keep dependencies minimal.
- If adding a dependency, justify it in the PR/commit message and use the lightest tool that solves the problem.

### Cross-platform

- Assume contributors may run Windows, macOS, Linux.
- Avoid shell-only assumptions; prefer Python implementations for file operations.

---

## 4) Testing rules (important)

### Unit tests must be offline

- **Do not call live APIs** (OpenAI or otherwise) from unit tests.
- Use fakes/mocks and deterministic fixtures.
- If you add “integration” tests, keep them:
  - opt-in (skipped by default)
  - clearly labeled (e.g. `tests/integration/`)
  - documented with required env vars

### Minimum expectation per feature

- At least one basic test verifying the core behavior (smoke test is fine).
- If you introduce file-writing logic, tests must cover:
  - “no overwrite without force”
  - path traversal protection

---

## 5) File writing / repo bootstrapper-specific guardrails

Any code that writes files to disk must:

- Default to **no overwrite**
- Provide a `--force` override (explicit)
- Provide `--dry-run` (no writes)
- Prevent path traversal:
  - Reject paths containing `..` segments or absolute paths
  - Ensure final resolved paths stay under the intended output directory
- Never write outside the requested target directory

---

## 6) Documentation expectations

- Update `README.md` when you add or change user-facing behavior.
- If a command exists, document:
  - example usage
  - flags
  - expected output / where files go

---

## 7) When unsure, stop and ask

If you’re uncertain about:

- deleting/moving lots of files
- changing build tooling
- adding dependencies
- anything touching credentials/security

…pause and ask for explicit approval with options and tradeoffs.
