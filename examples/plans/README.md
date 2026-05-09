# Example Bootstrap Plans

This directory stores reusable `RepoBootstrapOutput` plans that can be replayed with the repo bootstrapper.

## Claims Demo Data Factory

Plan: [claims-demo-data-factory.plan.json](claims-demo-data-factory.plan.json)

Target sample repo:

- repo name: `claims-demo-data-factory`
- package: `claims_demo_data_factory`
- purpose: generate fake, non-sensitive insurance claims demo fixtures for AI workflow demos, legal/claims education, and product prototypes

Safety boundaries:

- Fake demo data only.
- No real client, claimant, policy, medical, financial, or legal data.
- No legal advice or claim outcome recommendations.
- No cloud services, auth, databases, or external integrations.

### Generate with `--save-plan`

The live seed plan was generated with the Agents SDK path:

```powershell
.\.venv\Scripts\python.exe -m apps.repo_bootstrapper `
  --out _scratch/claims-demo-data-factory-live `
  --repo-name claims-demo-data-factory `
  --purpose "generate fake, non-sensitive insurance claims demo fixtures for AI workflow demos, legal/claims education, and product prototypes" `
  --package claims_demo_data_factory `
  --save-plan examples/plans/claims-demo-data-factory.plan.json
```

The raw live seed proved `--save-plan` worked, then the committed plan was safety-reviewed and curated. The review removed an unsafe future external-API roadmap idea and added deterministic fake fixture files and tests.

### Replay with `--load-plan`

Replay the committed plan without calling the agent:

```powershell
python -m apps.repo_bootstrapper `
  --out _scratch/claims-demo-data-factory-replay-verified `
  --package claims_demo_data_factory `
  --load-plan examples/plans/claims-demo-data-factory.plan.json
```

Replay evidence: this command succeeded with system Python after system Python had already failed the live path with `No module named 'agents'`. That makes the replay a useful check that `--load-plan` can apply the plan without importing or calling the agent.

### Generated files

The committed plan replays into these files:

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `pyproject.toml`
- `src/claims_demo_data_factory/__init__.py`
- `src/claims_demo_data_factory/fixtures.py`
- `tests/test_smoke.py`
- `tests/test_fixtures.py`

### Validation

Latest validation for this experiment:

- Live `--save-plan`: succeeded with the local virtualenv after network approval.
- Offline `--load-plan`: succeeded with system Python and wrote 9 files.
- Generated sample tests: `python -m pytest -q` passed with 3 tests from `_scratch/claims-demo-data-factory-replay-verified`.
- Repo tests: `python -m pytest -q` passed with 10 tests.
- Whitespace: `git diff --check` passed.

### Future workflow use

This plan can later support Agent Lab, IT Pro Direct, `claims-intelligence-foundation`, policy-dispute tools, or Merlin-style demos as a safe fixture seed. Treat it as demo data infrastructure, not a production claims app.
