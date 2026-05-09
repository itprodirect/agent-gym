from pathlib import Path

import pytest

from apps.repo_bootstrapper.plans import load_plan, save_plan
from apps.repo_bootstrapper.schemas import BootstrapFile, RepoBootstrapOutput


def _output() -> RepoBootstrapOutput:
    return RepoBootstrapOutput(
        files=[BootstrapFile(path="README.md", content="hello")],
        notes="Plan note.",
    )


def test_save_and_load_plan_roundtrip(tmp_path: Path):
    plan_path = tmp_path / "plan.json"

    result = save_plan(plan_path, _output(), force=False, dry_run=False)
    loaded = load_plan(plan_path)

    assert result.action == "create"
    assert loaded.files[0].path == "README.md"
    assert loaded.files[0].content == "hello"
    assert loaded.notes == "Plan note."


def test_save_plan_refuses_overwrite_without_force(tmp_path: Path):
    plan_path = tmp_path / "plan.json"
    save_plan(plan_path, _output(), force=False, dry_run=False)

    with pytest.raises(FileExistsError):
        save_plan(plan_path, _output(), force=False, dry_run=False)


def test_save_plan_dry_run_does_not_write(tmp_path: Path):
    plan_path = tmp_path / "plan.json"

    result = save_plan(plan_path, _output(), force=False, dry_run=True)

    assert result.action == "create"
    assert not plan_path.exists()


def test_load_plan_rejects_invalid_schema(tmp_path: Path):
    plan_path = tmp_path / "invalid.json"
    plan_path.write_text('{"files": [{"path": "README.md"}]}', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid plan schema"):
        load_plan(plan_path)
