"""
Script:     demo_zip_creator.py
Version:    2.1.0
Author:     Mike & ChatGPT

Purpose:
    Demonstrate the use of shared library functions to zip a folder
    and generate a separate inventory report.

Usage:
    python demo_zip_creator.py "P:/Photos/2024" "O:/Backups"

Dependencies:
    - zip_utils.py (from O:/Scripts/lib)
"""

import sys
from pathlib import Path

# Add path to the shared library
LIB_PATH = Path("O:/Scripts/lib")
sys.path.append(str(LIB_PATH))

# Import functions
from zip_utils import create_zip_with_timestamp, create_zip_inventory

def main():
    if len(sys.argv) != 3:
        print("Usage: python demo_zip_creator.py <source_folder> <output_folder>")
        sys.exit(1)

    source_folder = Path(sys.argv[1])
    output_folder = Path(sys.argv[2])

    if not source_folder.exists() or not source_folder.is_dir():
        print(f"❌ Source folder not found or not a directory: {source_folder}")
        sys.exit(1)

    if not output_folder.exists():
        print(f"⚠️ Output folder does not exist. Creating: {output_folder}")
        output_folder.mkdir(parents=True, exist_ok=True)

    # Step 1: Create the ZIP file and keep only the latest 2
    zip_path = create_zip_with_timestamp(source_folder, output_folder, keep_zips=2)

    # Step 2: Generate inventory and keep only latest 2 reports
    create_zip_inventory(zip_path, keep_reports=2)


if __name__ == "__main__":
    main()
