from pathlib import Path

from apps.repo_bootstrapper import cli
from apps.repo_bootstrapper.plans import load_plan, save_plan
from apps.repo_bootstrapper.schemas import BootstrapFile, RepoBootstrapOutput


def _sample_output(package: str = "demo_pkg") -> RepoBootstrapOutput:
    return RepoBootstrapOutput(
        files=[
            BootstrapFile(path="README.md", content="# Demo\n"),
            BootstrapFile(path="AGENTS.md", content="# Guardrails\n"),
            BootstrapFile(path=".gitignore", content="_scratch/\n"),
            BootstrapFile(path="pyproject.toml", content="[project]\nname='demo'\n"),
            BootstrapFile(path="ROADMAP.md", content="# Roadmap\n"),
            BootstrapFile(
                path="tests/test_smoke.py",
                content="def test_smoke():\n    assert True\n",
            ),
            BootstrapFile(path=f"src/{package}/__init__.py", content=""),
        ],
        notes="Generated for testing.",
    )


def test_cli_save_plan_writes_valid_plan(monkeypatch, tmp_path: Path, capsys):
    output = _sample_output()

    def fake_generate(req, *, model):
        assert req.package == "demo_pkg"
        assert model is None
        return output

    monkeypatch.setattr(cli, "_generate_repo_files", fake_generate)
    out_dir = tmp_path / "repo"
    plan_path = tmp_path / "plan.json"

    rc = cli.main(
        [
            "--out",
            str(out_dir),
            "--repo-name",
            "demo",
            "--purpose",
            "Demo repo",
            "--package",
            "demo_pkg",
            "--save-plan",
            str(plan_path),
        ]
    )

    assert rc == 0
    assert "Saved plan to:" in capsys.readouterr().out
    assert (out_dir / "README.md").read_text(encoding="utf-8") == "# Demo\n"
    assert load_plan(plan_path).files[0].path == "README.md"


def test_cli_load_plan_applies_without_calling_agent(
    monkeypatch,
    tmp_path: Path,
    capsys,
):
    plan_path = tmp_path / "plan.json"
    save_plan(plan_path, _sample_output(), force=False, dry_run=False)

    def fail_generate(req, *, model):
        raise AssertionError("agent generation should not be called")

    monkeypatch.setattr(cli, "_generate_repo_files", fail_generate)
    out_dir = tmp_path / "repo"

    rc = cli.main(
        [
            "--out",
            str(out_dir),
            "--package",
            "demo_pkg",
            "--load-plan",
            str(plan_path),
        ]
    )

    assert rc == 0
    output = capsys.readouterr().out
    assert "Loaded plan from:" in output
    assert "Notes from plan:" in output
    assert (out_dir / "src" / "demo_pkg" / "__init__.py").exists()
