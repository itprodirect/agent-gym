from pathlib import Path

import pytest

from apps.repo_bootstrapper.schemas import BootstrapFile
from apps.repo_bootstrapper.writer import write_files


def test_write_files_creates_files(tmp_path: Path):
    files = [BootstrapFile(path="README.md", content="hi")]
    plans = write_files(tmp_path, files, force=False, dry_run=False)
    assert (tmp_path / "README.md").exists()
    assert plans[0].bytes_len == 2


def test_write_files_refuses_overwrite_without_force(tmp_path: Path):
    (tmp_path / "README.md").write_text("old", encoding="utf-8")
    files = [BootstrapFile(path="README.md", content="new")]
    with pytest.raises(FileExistsError):
        write_files(tmp_path, files, force=False, dry_run=False)


def test_path_traversal_blocked(tmp_path: Path):
    files = [BootstrapFile(path="../oops.txt", content="nope")]
    with pytest.raises(ValueError):
        write_files(tmp_path, files, force=True, dry_run=True)
