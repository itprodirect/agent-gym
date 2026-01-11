from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .schemas import BootstrapFile


@dataclass(frozen=True)
class WritePlan:
    path: Path
    bytes_len: int


def _safe_join(out_dir: Path, rel_path: str) -> Path:
    # Normalize slashes early
    rel_path = rel_path.replace("\\", "/").lstrip("/")

    candidate = (out_dir / rel_path).resolve()
    out_dir_resolved = out_dir.resolve()

    # Block path traversal / absolute paths by ensuring target stays under out_dir
    if out_dir_resolved not in candidate.parents and candidate != out_dir_resolved:
        raise ValueError(f"Unsafe path (escapes output dir): {rel_path}")

    return candidate


def plan_writes(out_dir: Path, files: list[BootstrapFile]) -> list[WritePlan]:
    plans: list[WritePlan] = []
    for f in files:
        p = _safe_join(out_dir, f.path)
        plans.append(
            WritePlan(path=p, bytes_len=len(f.content.encode("utf-8"))))
    return plans


def write_files(out_dir: Path, files: list[BootstrapFile], *, force: bool, dry_run: bool) -> list[WritePlan]:
    out_dir.mkdir(parents=True, exist_ok=True)
    plans = plan_writes(out_dir, files)

    for plan, f in zip(plans, files):
        plan.path.parent.mkdir(parents=True, exist_ok=True)

        if plan.path.exists() and not force:
            raise FileExistsError(
                f"Refusing to overwrite existing file: {plan.path}")

        if not dry_run:
            plan.path.write_text(f.content, encoding="utf-8")

    return plans
