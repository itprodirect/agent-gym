from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .schemas import RepoBootstrapOutput


@dataclass(frozen=True)
class PlanSaveResult:
    path: Path
    action: str


def _model_to_data(output: RepoBootstrapOutput) -> dict[str, Any]:
    if hasattr(output, "model_dump"):
        return output.model_dump(mode="json")
    return output.dict()


def validate_plan_data(data: Any) -> RepoBootstrapOutput:
    try:
        if hasattr(RepoBootstrapOutput, "model_validate"):
            return RepoBootstrapOutput.model_validate(data)
        return RepoBootstrapOutput.parse_obj(data)
    except (TypeError, ValueError, ValidationError) as exc:
        raise ValueError(f"Invalid plan schema: {exc}") from exc


def load_plan(path: Path) -> RepoBootstrapOutput:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Unable to read plan file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid plan JSON: {path}") from exc

    return validate_plan_data(data)


def save_plan(
    path: Path,
    output: RepoBootstrapOutput,
    *,
    force: bool,
    dry_run: bool,
) -> PlanSaveResult:
    action = "overwrite" if path.exists() else "create"
    if path.exists() and not force and not dry_run:
        raise FileExistsError(f"Refusing to overwrite existing plan: {path}")

    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = _model_to_data(output)
        path.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return PlanSaveResult(path=path, action=action)
