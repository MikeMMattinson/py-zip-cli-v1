import zipfile
from pathlib import Path
import tempfile
import shutil

import pytest

from zipcli.main import should_include, collect_files, create_zip_archive


def test_should_include_logic():
    assert should_include(Path("file.txt"), ["*.txt"], []) is True
    assert should_include(Path("file.log"), ["*.txt"], []) is False
    assert should_include(Path("secret.txt"), ["*.txt"], ["secret*"]) is False
    assert should_include(Path("notes.md"), [], ["*.md"]) is False
    assert should_include(Path("data.csv"), [], []) is True


def test_collect_files_with_filters(tmp_path: Path):
    # Setup test files
    (tmp_path / "a.txt").write_text("text file")
    (tmp_path / "b.log").write_text("log file")
    (tmp_path / "secret.txt").write_text("secret")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.txt").write_text("nested")

    included = collect_files(tmp_path, ["*.txt"], ["secret*"])
    relative_paths = sorted(f.relative_to(tmp_path).as_posix() for f in included)

    assert "a.txt" in relative_paths
    assert "sub/c.txt" in relative_paths
    assert "secret.txt" not in relative_paths
    assert "b.log" not in relative_paths


def test_create_zip_archive_creates_correct_zip(tmp_path: Path):
    # Create dummy files
    (tmp_path / "test.txt").write_text("Hello ZIP")
    (tmp_path / "skip.log").write_text("This should be excluded")

    # Call zip creation
    zip_output_dir = tmp_path / "out"
    zip_output_dir.mkdir()
    create_zip_archive(
        source_dir=tmp_path,
        includes=["*.txt"],
        excludes=["*.log"],
        date_format="%Y%m%d",
        inventory=False,
        backup_location=zip_output_dir
    )

    zip_files = list(zip_output_dir.glob("*.zip"))
    assert len(zip_files) == 1

    with zipfile.ZipFile(zip_files[0], 'r') as zf:
        names = zf.namelist()
        assert "test.txt" in names
        assert "skip.log" not in names


# Optional: Run this test directly if needed
if __name__ == "__main__":
    pytest.main(["-v", __file__])
