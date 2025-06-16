"""
Script:     test_keep_option.py
Version:    1.1.0-alpha
Author:     Mike & ChatGPT

Purpose:
    Integration test for --keep option in zipcli.main using test_utils.

Usage:
    pytest tests/test_keep_option.py --test-type alpha
"""

__version__ = "1.1.0-alpha"
__milestone__ = "v1.1.0"

import pytest
import time
from pathlib import Path
from types import SimpleNamespace

from zipcli.main import create_zip_archive
from lib import test_utils


@pytest.fixture(scope="module")
def test_config(pytestconfig):
    path = Path(__file__)
    config = SimpleNamespace()
    output_dir, test_name, log_file, logger = test_utils.setup_test_environment(path, pytestconfig)
    config.output_dir = output_dir
    config.logger = logger
    return config


def test_keep_rotation_removes_old_zips(test_config):
    # Setup test folders
    source_dir = test_config.output_dir / "input"
    backup_dir = test_config.output_dir / "backup"
    
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Clean leftover ZIPs and inventories from previous runs
    for f in backup_dir.glob("input_*.zip"):
        f.unlink()
    for f in backup_dir.glob("input_*_inventory.txt"):
        f.unlink()
    

    # Clean if somehow a file exists with same name as dir
    if source_dir.exists() and not source_dir.is_dir():
        source_dir.unlink()
    if backup_dir.exists() and not backup_dir.is_dir():
        backup_dir.unlink()

    source_dir.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Create sample input files
    for i in range(3):
        (source_dir / f"sample{i}.txt").write_text(f"Data {i}")

    # Run ZIP command 5 times with --keep=2
    for i in range(5):
        create_zip_archive(
            source_dir=source_dir,
            includes=["*.txt"],
            excludes=[],
            date_format="%Y%m%d%H%M%S",
            inventory=True,
            backup_location=backup_dir,
            keep=2
        )
        time.sleep(1.2)  # Ensure unique timestamp

    zip_files = list(backup_dir.glob("input_*.zip"))
    inventory_files = list(backup_dir.glob("input_*_inventory.txt"))

    test_config.logger.info(f"ZIPs found: {[f.name for f in zip_files]}")
    test_config.logger.info(f"Inventories found: {[f.name for f in inventory_files]}")

    assert len(zip_files) == 2, f"Expected 2 ZIPs kept, found {len(zip_files)}"
    assert len(inventory_files) == 2, f"Expected 2 inventories kept, found {len(inventory_files)}"
