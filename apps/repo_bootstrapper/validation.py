from __future__ import annotations

REQUIRED_PATHS = {
    "README.md",
    "AGENTS.md",
    ".gitignore",
    "pyproject.toml",
    "ROADMAP.md",
    "tests/test_smoke.py",
}


def required_paths_for_package(package: str) -> set[str]:
    required = set(REQUIRED_PATHS)
    required.add(f"src/{package}/__init__.py")
    return required


def required_list_for_prompt(package: str) -> list[str]:
    return sorted(required_paths_for_package(package))


def validate_output(package: str, paths: set[str]) -> None:
    missing = sorted(required_paths_for_package(package) - paths)
    if missing:
        raise ValueError(
            "Output missing required files:\n- " + "\n- ".join(missing)
        )
