from __future__ import annotations

from pydantic import BaseModel, Field


class BootstrapFile(BaseModel):
    path: str = Field(..., description="Relative path to write, e.g. README.md or src/pkg/__init__.py")
    content: str = Field(..., description="File contents as UTF-8 text")


class RepoBootstrapRequest(BaseModel):
    repo_name: str
    purpose: str
    package: str
    license: str = "MIT"


class RepoBootstrapOutput(BaseModel):
    files: list[BootstrapFile]
