#!/usr/bin/env python3
"""
Script:     main.py
Version:    1.1.0
Author:     Mike & ChatGPT

Purpose:
    Command-line tool to create dated ZIP archives with flexible filters.

Example Usage:
    zip_cli.exe myfolder --filter ".txt" --exclude "secret" --date-format "%Y%m%d" --inventory --backup-location /backups --keep 3

Features:
    - Includes/excludes files via glob patterns
    - Customizable date format for filenames
    - Optional inventory report printed to console **and** saved as a text file
    - Backup location support
    - Retains only the last [n] ZIP archives per source folder (--keep)
    - Executable build via PyInstaller
"""

__version__ = "1.1.0"
__milestone__ = "v1.1.0"

import argparse
import fnmatch
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional


def should_include(file_path: Path, includes: List[str], excludes: List[str]) -> bool:
    name = file_path.name
    if includes and not any(fnmatch.fnmatch(name, pat) for pat in includes):
        return False
    if excludes and any(fnmatch.fnmatch(name, pat) for pat in excludes):
        return False
    return True


def collect_files(base_dir: Path, includes: List[str], excludes: List[str]) -> List[Path]:
    return [
        f for f in base_dir.rglob("*")
        if f.is_file() and should_include(f.relative_to(base_dir), includes, excludes)
    ]


def parse_timestamp_from_name(filename: str, prefix: str, date_format: str) -> Optional[datetime]:
    """
    Attempt to extract a datetime object from the filename using the given prefix and format.
    Returns None if parsing fails.
    """
    try:
        stem = Path(filename).stem
        if not stem.startswith(prefix + "_"):
            return None
        date_part = stem[len(prefix) + 1:]
        return datetime.strptime(date_part, date_format)
    except Exception:
        return None


def enforce_zip_retention(source_dir: Path, backup_location: Path, date_format: str, keep: int):
    """
    Retain only the most recent [keep] ZIP files and their inventories in backup_location.

    Args:
        source_dir (Path): The folder being zipped (used to match filename prefix).
        backup_location (Path): Where to search for old ZIPs.
        date_format (str): Format of the timestamp in the ZIP filename.
        keep (int): Number of ZIPs to retain.
    """
    zip_prefix = source_dir.name
    all_zips = list(backup_location.glob(f"{zip_prefix}_*.zip"))

    def zip_sort_key(p: Path):
        ts = parse_timestamp_from_name(p.name, zip_prefix, date_format)
        return ts if ts else datetime.fromtimestamp(p.stat().st_ctime)

    sorted_zips = sorted(all_zips, key=zip_sort_key, reverse=True)
    to_delete = sorted_zips[keep:]

    for zip_path in to_delete:
        try:
            zip_path.unlink()
            print(f"[INFO] Removed old ZIP: {zip_path.name}")

            # Also remove the matching inventory file
            inventory_path = zip_path.with_name(zip_path.stem + "_inventory.txt")
            if inventory_path.exists():
                inventory_path.unlink()
                print(f"[INFO] Removed inventory: {inventory_path.name}")

        except Exception as e:
            print(f"[WARN] Could not delete {zip_path.name}: {e}")



def create_zip_archive(
    source_dir: Path,
    includes: List[str],
    excludes: List[str],
    date_format: str,
    inventory: bool,
    backup_location: Path,
    keep: int = 1  # ← default value here
):
    timestamp = datetime.now().strftime(date_format)
    zip_name = f"{source_dir.name}_{timestamp}.zip"
    output_path = (backup_location or Path.cwd()) / zip_name

    files_to_zip = collect_files(source_dir, includes, excludes)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        inventory_lines = []
        for file_path in files_to_zip:
            arcname = file_path.relative_to(source_dir)
            zf.write(file_path, arcname)
            inventory_lines.append(f"{arcname}")
            if inventory:
                print(f"  [✓] {arcname}")

    if inventory:
        inventory_path = output_path.with_name(output_path.stem + "_inventory.txt")
        inventory_path.write_text("\n".join(inventory_lines), encoding="utf-8")
        print(f"[✓] Inventory report saved to: {inventory_path}")

    enforce_zip_retention(source_dir, output_path.parent, date_format, keep)


def main():
    parser = argparse.ArgumentParser(description="Zip CLI Utility")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to zip (default: current directory)")
    parser.add_argument("--filter", nargs="*", default=[], help="Glob patterns to include (e.g. *.txt *.csv)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Glob patterns to exclude (e.g. secret*.txt)")
    parser.add_argument("--include", nargs="*", default=[], help="Same as --filter (overrides if used together)")
    parser.add_argument("--date-format", default="%Y%m%dT%H%M", help="Timestamp format (default: %%Y%%m%%dT%%H%%M)")
    parser.add_argument("--inventory", action="store_true", help="List included files")
    parser.add_argument("--backup-location", type=Path, help="Folder to save the .zip file")
    parser.add_argument("--keep", type=int, default=1, help="Number of recent ZIPs to keep (default: 1)")

    args = parser.parse_args()

    include_patterns = args.include if args.include else args.filter
    exclude_patterns = args.exclude
    source_dir = Path(args.folder).resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"[FAIL] Invalid folder: {source_dir}")
        return

    if args.backup_location:
        args.backup_location.mkdir(parents=True, exist_ok=True)

    create_zip_archive(
        source_dir=source_dir,
        includes=include_patterns,
        excludes=exclude_patterns,
        date_format=args.date_format,
        inventory=args.inventory,
        backup_location=args.backup_location or Path.cwd(),
        keep=args.keep
    )


if __name__ == "__main__":
    main()
