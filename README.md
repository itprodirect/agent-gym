# agent-gym

A small, practical repo for building **hello-world agents** with the OpenAI Agents SDK and turning them into **trustworthy CLI tools**.

This repo is intentionally built in **sessions** (feature branch → tests → PR → merge) so each increment is reviewable and reproducible.

---

## What we built in Session 1

### Repo Bootstrapper Agent (MVP)

We built a working CLI that uses an Agents SDK agent to generate a **minimal repo scaffold** (as structured `{path, content}` files) and then writes it safely to disk.

**Key features:**

- **Structured output** (Pydantic schema) so the agent returns a deterministic file list
- **Required-file validation** (fails fast if the agent forgets files)
- **Retry/repair loop** when required files are missing
- **Safe file writing**

  - blocks path traversal (`../`)
  - refuses overwrite unless `--force` (but **dry-run never errors**; it reports `[create]` / `[overwrite]`)

- **Offline tests** (no API calls in unit tests)
- Repo guardrails via **AGENTS.md**

---

## Codex workflow sandbox foundation

This repo also serves as a lightweight sandbox for practicing repeatable Codex sessions before adding more app surface area.

Use these docs when preparing a run:

- [AGENTS.md](AGENTS.md): repository guardrails for safety, scope, testing, and file writes.
- [docs/codex-goals.md](docs/codex-goals.md): examples of specific, reviewable Codex goals and vague goals to avoid.
- [docs/experiment-log.md](docs/experiment-log.md): template for recording `/goal`, memories, external migration, terminal resize reflow, and prevent-sleep experiments.
- [docs/goal-scorecards/README.md](docs/goal-scorecards/README.md): practical scorecards for judging whether a `/goal` run was trustworthy enough to reuse.
- [docs/session-template.md](docs/session-template.md): copyable checklist for future Codex sessions.
- [examples/plans/README.md](examples/plans/README.md): reusable bootstrap plans, including the claims demo data factory plan.

For this foundation PR, keep changes limited to docs and local workflow notes. Do not add cloud services, auth, databases, dependencies, or unrelated app code.

---

## Quickstart

### 1) Create & activate a virtual environment

(Example for Windows Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -U pip
```

### 2) Install dependencies

```bash
python -m pip install -U pytest
# plus whatever you use to install the Agents SDK in this env
```

### 3) Set environment variables

Make sure your OpenAI credentials are available in the shell where you run the CLI.

```bash
# Example (set however you prefer)
export OPENAI_API_KEY="..."
export OPENAI_MODEL="gpt-4o-mini"  # optional override
```

---

## Repo Bootstrapper Agent

### Dry run (shows plan, doesn’t write)

```bash
python -m apps.repo_bootstrapper \
  --out ./_scratch/demo_repo \
  --repo-name demo-repo \
  --purpose "Example repo scaffold" \
  --package demo_repo \
  --dry-run
```

### Save a generated plan

Use `--save-plan` to keep the exact validated file list returned by the agent.

```bash
python -m apps.repo_bootstrapper \
  --out ./_scratch/demo_repo \
  --repo-name demo-repo \
  --purpose "Example repo scaffold" \
  --package demo_repo \
  --save-plan ./_scratch/demo_repo.plan.json
```

The generated repo is written to `--out`, and the reusable JSON plan is written to the `--save-plan` path. Existing plan files are not overwritten unless you also pass `--force`.

### Load a saved plan without calling the agent

Use `--load-plan` to apply a saved plan offline. The plan is parsed with the same `RepoBootstrapOutput` schema and still must include the required files for `--package`.

```bash
python -m apps.repo_bootstrapper \
  --out ./_scratch/demo_repo_from_plan \
  --package demo_repo \
  --load-plan ./_scratch/demo_repo.plan.json
```

This writes the plan contents to `--out` without requiring OpenAI credentials.

### Write a new repo scaffold

```bash
python -m apps.repo_bootstrapper \
  --out ./_scratch/demo_repo_v2 \
  --repo-name demo-repo \
  --purpose "Example repo scaffold" \
  --package demo_repo
```

### Overwrite existing files (explicit)

```bash
python -m apps.repo_bootstrapper \
  --out ./_scratch/demo_repo_v2 \
  --repo-name demo-repo \
  --purpose "Example repo scaffold" \
  --package demo_repo \
  --force
```

### Validate the generated repo works

```bash
cd _scratch/demo_repo_v2
python -m pytest -q
```

---

## Project layout

```text
agent-gym/
  apps/
    repo_bootstrapper/
      __main__.py
      agent.py
      cli.py
      plans.py
      schemas.py
      validation.py
      writer.py
  src/
    agent_gym/
  tests/
    conftest.py
    test_cli_smoke.py
    test_plans.py
    test_writer.py
  docs/
    codex-goals.md
    experiment-log.md
    goal-scorecards/
      README.md
      pr-2-codex-workflow-sandbox-foundation.md
      pr-3-reproducible-bootstrap-plans.md
      template.md
    session-template.md
  examples/
    plans/
      claims-demo-data-factory.plan.json
      README.md
  AGENTS.md
  pyproject.toml
  README.md
  .gitignore
```

Notes:

- `_scratch/` is ignored (generated outputs live here).
- `.env` is ignored (never commit secrets).

---

## Development workflow

We use a simple, repeatable flow:

1. Create a feature branch: `feat/###-short-name`
2. Make small commits
3. Keep tests green (`python -m pytest -q`)
4. Open a PR → review diff → merge into `main`
5. Clean up local branches after merge

---

## Future sessions

### Session 2 (recommended): Reproducible plans

- [x] Add `--save-plan plan.json` (save the exact generated file list)
- [x] Add `--load-plan plan.json` (apply a saved plan without calling the agent)
- [x] Add tests for save/load and validation

### Session 3: Template & CI options

- [ ] Add `--style minimal|standard|enterprise`
- [ ] Optional: `--ci github-actions` to generate a simple test workflow

### Session 4: Next hello-world agents

- [ ] (Pick the next mini-project and repeat the same branch/PR discipline)

---

## Guardrails

See **AGENTS.md** for repo-level rules (safety, small diffs, no secrets, avoid destructive commands, tests-first discipline).
