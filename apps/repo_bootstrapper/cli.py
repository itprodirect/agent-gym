from __future__ import annotations

import argparse
from pathlib import Path

from .schemas import RepoBootstrapRequest


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="repo-bootstrapper")
    p.add_argument("--out", required=True,
                   help="Output directory to generate the repo into")
    p.add_argument("--repo-name", required=True)
    p.add_argument("--purpose", required=True)
    p.add_argument("--package", required=True)
    p.add_argument("--license", default="MIT")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # Next step: call agent + writer (we’ll wire this in next commit)
    _req = RepoBootstrapRequest(
        repo_name=args.repo_name,
        purpose=args.purpose,
        package=args.package,
        license=args.license,
    )

    out_dir = Path(args.out)
    if args.dry_run:
        print(f"[dry-run] Would generate repo into: {out_dir}")

    return 0
