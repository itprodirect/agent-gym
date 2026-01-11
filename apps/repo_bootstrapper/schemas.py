from __future__ import annotations

from pydantic import BaseModel, Field


class BootstrapFile(BaseModel):
    """A single UTF-8 text file to write to disk."""

    path: str = Field(
        ...,
        description="Relative path inside the generated repo (POSIX style), e.g. README.md or src/pkg/__init__.py",
        examples=["README.md", "src/demo_repo/__init__.py"],
    )
    content: str = Field(..., description="UTF-8 text content for the file")


class RepoBootstrapRequest(BaseModel):
    repo_name: str
    purpose: str
    package: str
    license: str = "MIT"


class RepoBootstrapOutput(BaseModel):
    files: list[BootstrapFile]
    notes: str | None = None
