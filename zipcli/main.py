#!/usr/bin/env python3
"""
Script:     main.py
Version:    1.0.0
Author:     Mike & ChatGPT

Purpose:
    Command-line tool to create dated ZIP archives with flexible filters.

Example Usage:
    zip_cli.exe myfolder --filter ".txt" --exclude "secret" --date-format "%Y%m%d" --inventory --backup-location /backups

Features:
    - Create ZIP archives with date-stamped filenames
    - Filter files using include/exclude patterns
    - Customizable timestamp formats
    - Optional inventory listing
    - Optional backup location
"""

__version__ = "1.0.0"
__milestone__ = "v1.0.0"

import argparse
import fnmatch
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List


def should_include(file_path: Path, includes: List[str], excludes: List[str]) -> bool:
    """
    Determine whether a file should be included in the ZIP archive
    based on inclusion and exclusion patterns.

    Args:
        file_path (Path): Path to the file to evaluate.
        includes (List[str]): List of glob patterns to include.
        excludes (List[str]): List of glob patterns to exclude.

    Returns:
        bool: True if the file should be included, False otherwise.
    """
    name = file_path.name
    if includes and not any(fnmatch.fnmatch(name, pat) for pat in includes):
        return False
    if excludes and any(fnmatch.fnmatch(name, pat) for pat in excludes):
        return False
    return True


def collect_files(base_dir: Path, includes: List[str], excludes: List[str]) -> List[Path]:
    """
    Recursively collect all files in a directory that match the given
    include and exclude filters.

    Args:
        base_dir (Path): The root directory to scan for files.
        includes (List[str]): Patterns of files to include.
        excludes (List[str]): Patterns of files to exclude.

    Returns:
        List[Path]: List of paths to include in the ZIP archive.
    """
    return [
        f for f in base_dir.rglob("*")
        if f.is_file() and should_include(f.relative_to(base_dir), includes, excludes)
    ]


def create_zip_archive(
    source_dir: Path,
    includes: List[str],
    excludes: List[str],
    date_format: str,
    inventory: bool,
    backup_location: Path
):
    """
    Create a ZIP archive of files from the given source directory, applying
    filtering rules and naming conventions.

    Args:
        source_dir (Path): Directory to zip.
        includes (List[str]): File patterns to include.
        excludes (List[str]): File patterns to exclude.
        date_format (str): Format for the timestamp to include in the ZIP filename.
        inventory (bool): Whether to print the list of included files.
        backup_location (Path): Output directory for the ZIP file. Defaults to current directory.
    """
    timestamp = datetime.now().strftime(date_format)
    zip_name = f"{source_dir.name}_{timestamp}.zip"
    output_path = (backup_location or Path.cwd()) / zip_name

    files_to_zip = collect_files(source_dir, includes, excludes)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in files_to_zip:
            arcname = file_path.relative_to(source_dir)
            zf.write(file_path, arcname)
            if inventory:
                print(f"  [✓] {arcname}")

    print(f"\n[✓] Created ZIP: {output_path}")


def main():
    """
    Parse command-line arguments and create a ZIP archive
    based on the provided options.
    """
    parser = argparse.ArgumentParser(description="Zip CLI Utility")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to zip (default: current directory)")
    parser.add_argument("--filter", nargs="*", default=[], help="Glob patterns to include (e.g. *.txt *.csv)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Glob patterns to exclude (e.g. secret*.txt)")
    parser.add_argument("--include", nargs="*", default=[], help="Same as --filter (overrides if used together)")
    parser.add_argument("--date-format", default="%Y%m%dT%H%M", help="Timestamp format (default: %%Y%%m%%dT%%H%%M)")
    parser.add_argument("--inventory", action="store_true", help="List included files")
    parser.add_argument("--backup-location", type=Path, help="Folder to save the .zip file")

    args = parser.parse_args()

    # Prefer --include if provided
    include_patterns = args.include if args.include else args.filter
    exclude_patterns = args.exclude

    source_dir = Path(args.folder).resolve()
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"❌ Invalid folder: {source_dir}")
        return

    if args.backup_location:
        args.backup_location.mkdir(parents=True, exist_ok=True)

    create_zip_archive(
        source_dir,
        includes=include_patterns,
        excludes=exclude_patterns,
        date_format=args.date_format,
        inventory=args.inventory,
        backup_location=args.backup_location
    )


if __name__ == "__main__":
    main()
