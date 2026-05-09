from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .plans import load_plan, save_plan
from .schemas import RepoBootstrapRequest
from .validation import validate_output
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
        default=None,
        help="Repository name (human-friendly). Required unless --load-plan is used.",
    )
    p.add_argument(
        "--purpose",
        default=None,
        help="One-line purpose/description. Required unless --load-plan is used.",
    )
    p.add_argument(
        "--package",
        default=None,
        help="Python package name (e.g. demo_repo). Required to validate required files.",
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
    p.add_argument(
        "--save-plan",
        default=None,
        help="Write the validated generated file list to a JSON plan file.",
    )
    p.add_argument(
        "--load-plan",
        default=None,
        help="Load a JSON plan file and apply it without calling the agent.",
    )
    return p


def _generate_repo_files(req: RepoBootstrapRequest, *, model: str | None):
    from .agent import generate_repo_files

    return generate_repo_files(req, model=model)


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
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.save_plan and args.load_plan:
        parser.error("--save-plan and --load-plan cannot be used together.")
    if args.load_plan:
        if not args.package:
            parser.error("--package is required with --load-plan.")
    else:
        if not args.repo_name:
            parser.error("--repo-name is required unless --load-plan is used.")
        if not args.purpose:
            parser.error("--purpose is required unless --load-plan is used.")
        if not args.package:
            parser.error("--package is required.")

    out_dir = Path(args.out).expanduser().resolve()

    try:
        if args.load_plan:
            plan_path = Path(args.load_plan).expanduser().resolve()
            result = load_plan(plan_path)
            print(f"Loaded plan from: {plan_path}")
        else:
            req = RepoBootstrapRequest(
                repo_name=args.repo_name,
                purpose=args.purpose,
                package=args.package,
                license=args.license,
            )
            result = _generate_repo_files(req, model=args.model)

        # Validate required files are present (fail fast if model or plan drifts)
        paths = {f.path for f in result.files}
        validate_output(args.package, paths)

        if args.save_plan:
            plan_path = Path(args.save_plan).expanduser().resolve()
            saved = save_plan(
                plan_path,
                result,
                force=args.force,
                dry_run=args.dry_run,
            )
            if args.dry_run:
                print(f"[dry-run] Would save plan to: {saved.path} [{saved.action}]")
            else:
                print(f"Saved plan to: {saved.path} [{saved.action}]")

        # Safely write to disk (or dry-run)
        plans = write_files(
            out_dir,
            result.files,
            force=args.force,
            dry_run=args.dry_run,
        )

        # Print a useful summary
        if args.dry_run:
            print(f"[dry-run] Would write {len(plans)} files into: {out_dir}")
        else:
            print(f"Wrote {len(plans)} files into: {out_dir}")

        for line in _format_plan_lines(out_dir, plans):
            print(line)

        if getattr(result, "notes", None):
            notes = (result.notes or "").strip()
            if notes:
                label = "plan" if args.load_plan else "agent"
                print(f"\nNotes from {label}:")
                print(notes)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
