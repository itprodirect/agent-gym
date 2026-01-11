from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import generate_repo_files, validate_output
from .schemas import RepoBootstrapRequest
from .writer import write_files


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="repo_bootstrapper",
        description="Generate a fresh repo scaffold using an Agents SDK agent.",
    )
    p.add_argument(
        "--out",
        required=True,
        help="Output directory to write the generated repo into.",
    )
    p.add_argument(
        "--repo-name",
        required=True,
        help="Repository name (human-friendly).",
    )
    p.add_argument(
        "--purpose",
        required=True,
        help="One-line purpose/description.",
    )
    p.add_argument(
        "--package",
        required=True,
        help="Python package name (e.g. demo_repo).",
    )
    p.add_argument(
        "--license",
        default="MIT",
        help="License identifier (default: MIT).",
    )

    p.add_argument(
        "--model",
        default=None,
        help="Optional model override (else OPENAI_MODEL or default set in agent.py).",
    )

    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files; just print what would happen.",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting existing files.",
    )
    return p


def _format_plan_lines(out_dir: Path, plans) -> list[str]:
    """
    plans are WritePlan objects from writer.py:
      - path: Path
      - bytes_len: int
      - action: str ("create" | "overwrite")
    """
    lines: list[str] = []
    for plan in sorted(plans, key=lambda p: str(p.path).lower()):
        try:
            rel = plan.path.relative_to(out_dir)
            rel_str = rel.as_posix()
        except Exception:
            rel_str = str(plan.path)

        action = getattr(plan, "action", "write")
        lines.append(f"- {rel_str} [{action}] ({plan.bytes_len} bytes)")
    return lines


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = Path(args.out).expanduser().resolve()

    req = RepoBootstrapRequest(
        repo_name=args.repo_name,
        purpose=args.purpose,
        package=args.package,
        license=args.license,
    )

    try:
        # 1) Ask the agent for structured output
        result = generate_repo_files(req, model=args.model)

        # 2) Validate required files are present (fail fast if model drifts)
        paths = {f.path for f in result.files}
        validate_output(req.package, paths)

        # 3) Safely write to disk (or dry-run)
        plans = write_files(out_dir, result.files,
                            force=args.force, dry_run=args.dry_run)

        # 4) Print a useful summary
        if args.dry_run:
            print(f"[dry-run] Would write {len(plans)} files into: {out_dir}")
        else:
            print(f"Wrote {len(plans)} files into: {out_dir}")

        for line in _format_plan_lines(out_dir, plans):
            print(line)

        if getattr(result, "notes", None):
            notes = (result.notes or "").strip()
            if notes:
                print("\nNotes from agent:")
                print(notes)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
