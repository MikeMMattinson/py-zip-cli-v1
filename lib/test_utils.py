"""
Script:     test_utils.py
Version:    1.1.0
Author:     Mike & ChatGPT

Purpose:
    Provide utility functions for test configuration and output directory management.
    Includes CLI support to dynamically route test outputs based on test type:
        - --test-type alpha  → tests/.test-alpha/
        - --test-type beta   → tests/.test-beta/
        - --test-type final  → tests/.test-final/

Usage:
    Called automatically during pytest test execution. Use the --test-type argument to specify the test output group.

Example:
    pytest tests/test_data_utils_unit.py --test-type beta
"""

from pathlib import Path
from datetime import datetime
import argparse
from typing import Tuple
import logging
__version__ = "1.1.0-alpha"



def parse_test_args():
    """
    Returns the test-type CLI argument passed to pytest.
    Defaults to 'alpha' if not provided.
    """
    import pytest
    from _pytest.config import Config

    config: Config = pytest.config  # This doesn't work directly
    # Better approach is to get it from the current request context in a fixture.
    raise NotImplementedError("This pattern must be replaced. See below.")



def create_test_output_dir_by_type(test_name: str, test_type: str, keep: int = 2) -> Path:
    """
    Create an output directory under .test-[type]/<test_name>_<timestamp> and
    delete older folders exceeding the 'keep' count.

    Args:
        test_name (str): The test filename stem.
        test_type (str): One of 'alpha', 'beta', or 'final'.
        keep (int): Number of recent folders to retain.
    """
    test_type_folder = Path(f".test-{test_type}")
    test_type_folder.mkdir(parents=True, exist_ok=True)

    # Clean up old folders matching this test name
    matching_folders = sorted(
        [p for p in test_type_folder.glob(f"{test_name}_*") if p.is_dir()],
        key=lambda p: p.name,
        reverse=True
    )

    for old_folder in matching_folders[keep:]:
        for item in old_folder.rglob("*"):
            item.unlink()
        old_folder.rmdir()

    # Create new folder
    timestamp = datetime.now().strftime("%Y%m%d")
    test_dir = test_type_folder / f"{test_name}_{timestamp}"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir

def extract_version_and_type(test_path: Path) -> Tuple[str, str]:
    """
    Extract the __version__ from the test file and return version and test_type (alpha, beta, final).
    """
    version = "v0.0.0"
    suffix = "alpha"
    for line in test_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("__version__"):
            version_raw = line.split("=")[-1].strip().strip('"').strip("'")
            version = f"v{version_raw}"
            if "-" in version_raw:
                suffix = version_raw.split("-")[-1]
            elif version_raw.replace(".", "").isdigit():
                suffix = "final"
            break
    return version, suffix


def setup_test_environment(test_path: Path, config, keep: int = 2):
    """
    Generalized setup for test environment. Returns output_dir, test_name, log_file, logger.
    """
    from test_utils import create_test_output_dir_by_type

    version, test_type = extract_version_and_type(test_path)
    test_name = test_path.stem

    output_dir = create_test_output_dir_by_type(f"{test_name}_{version}", test_type, keep)
    config.stash['output_dir'] = output_dir

    log_file = output_dir / f"{test_name}.log"
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)

    logger.info(f"Test output directory created at {output_dir}")
    return output_dir, test_name, log_file, logger


