from __future__ import annotations

import os
from textwrap import dedent

from agents import Agent, Runner

from .schemas import RepoBootstrapRequest, RepoBootstrapOutput

INSTRUCTIONS = dedent(
    """
    You are RepoBootstrapper.

    Goal: generate a minimal, clean Python repo scaffold.

    Output MUST match the provided schema exactly:
      RepoBootstrapOutput(files=[{path, content}, ...], notes?).

    HARD REQUIREMENTS (do not violate):
    - All paths must be RELATIVE (no leading "/") and must NOT include "..".
    - Use forward slashes in paths (POSIX style), even on Windows.
    - Text files only (no binaries, no base64).
    - Do not include secrets, tokens, API keys, or environment values.
    - Keep files small, practical, and runnable.

    You MUST include at least the required paths that the user provides in the prompt.
    Before returning, CHECK your own output and ensure every required path exists.
    If any are missing, ADD them before returning.
    """
).strip()

REQUIRED_PATHS = {
    "README.md",
    "AGENTS.md",
    ".gitignore",
    "pyproject.toml",
    "ROADMAP.md",
    "tests/test_smoke.py",
}


def validate_output(package: str, paths: set[str]) -> None:
    required = set(REQUIRED_PATHS)
    required.add(f"src/{package}/__init__.py")

    missing = sorted(required - paths)
    if missing:
        raise ValueError(
            "Agent output missing required files:\n- " + "\n- ".join(missing))


def _required_list_for_prompt(package: str) -> list[str]:
    # Explicit required paths we demand from the agent.
    req = sorted(REQUIRED_PATHS)
    req.append(f"src/{package}/__init__.py")
    return sorted(req)


def build_agent(model: str | None = None) -> Agent:
    chosen_model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    return Agent(
        name="RepoBootstrapper",
        instructions=INSTRUCTIONS,
        model=chosen_model,
        output_type=RepoBootstrapOutput,
    )


def build_prompt(req: RepoBootstrapRequest) -> str:
    required_paths = "\n".join(
        f"- {p}" for p in _required_list_for_prompt(req.package))

    return dedent(
        f"""
        Generate a repo scaffold with:

        repo_name: {req.repo_name}
        purpose: {req.purpose}
        package: {req.package}
        license: {req.license}

        REQUIRED PATHS (you MUST include EVERY item exactly as written):
        {required_paths}

        Content expectations:
        - README.md: brief overview + how to run tests + example usage blurb
        - .gitignore: include Python/venv ignores and _scratch/
        - pyproject.toml: minimal modern config (project metadata + pytest in dev deps)
        - tests/test_smoke.py: a tiny pytest smoke test
        - src/{req.package}/__init__.py: minimal package init

        Keep it minimal, clean, and consistent.
        """
    ).strip()


def build_repair_prompt(req: RepoBootstrapRequest, missing: list[str]) -> str:
    missing_block = "\n".join(f"- {m}" for m in missing)
    required_paths = "\n".join(
        f"- {p}" for p in _required_list_for_prompt(req.package))

    return dedent(
        f"""
        Your previous output was missing required files.

        Missing paths you MUST add:
        {missing_block}

        Return a COMPLETE RepoBootstrapOutput again that includes EVERY required path:
        {required_paths}

        Keep existing files minimal; do not add extras unless necessary.
        """
    ).strip()


def generate_repo_files(req: RepoBootstrapRequest, *, model: str | None = None) -> RepoBootstrapOutput:
    agent = build_agent(model=model)

    prompt = build_prompt(req)
    last: RepoBootstrapOutput | None = None
    missing: list[str] = []

    # Retry a couple times to handle occasional model “forgetfulness”
    for attempt in range(1, 4):
        run_prompt = prompt if attempt == 1 else build_repair_prompt(
            req, missing)
        result = Runner.run_sync(agent, run_prompt)
        last = result.final_output

        paths = {f.path for f in last.files}
        try:
            validate_output(req.package, paths)
            return last
        except ValueError:
            required = set(REQUIRED_PATHS) | {f"src/{req.package}/__init__.py"}
            missing = sorted(required - paths)

    # If we get here, retries failed.
    # Raise a clean error so the CLI prints a useful message.
    raise ValueError(
        "Agent output missing required files after retries:\n- " + "\n- ".join(missing))
