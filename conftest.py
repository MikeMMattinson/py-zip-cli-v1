# conftest.py

import sys
from pathlib import Path
import pytest
import logging

# Absolute path to project root and lib
ROOT_PATH = Path(__file__).resolve().parent
LIB_PATH = ROOT_PATH / "lib"

if str(LIB_PATH) not in sys.path:
    sys.path.insert(0, str(LIB_PATH))

# Track test outcomes and names
test_results = {
    "passed": [],
    "failed": [],
    "skipped": [],
    "total": 0,
}

def pytest_addoption(parser):
    parser.addoption(
        "--keep",
        type=int,
        default=2,
        help="Number of recent test runs to keep per test type folder (default: 2)"
    )

def pytest_runtest_logreport(report):
    """Track test outcomes with test node IDs."""
    if report.when == "call":
        test_results["total"] += 1
        if report.passed:
            test_results["passed"].append(report.nodeid)
        elif report.failed:
            test_results["failed"].append(report.nodeid)
        elif report.skipped:
            test_results["skipped"].append(report.nodeid)

def pytest_sessionfinish(session, exitstatus):
    """Write test summary and test name breakdown to test_summary.log."""
    try:
        output_dir = session.config.stash['output_dir']
    except KeyError:
        output_dir = Path(".")
        print("[WARN] output_dir not found in stash, writing summary to project root.")

    summary_file = output_dir / "test_summary.log"
    with summary_file.open("w", encoding="utf-8") as f:
        f.write("Test Session Summary\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"Passed:  {len(test_results['passed'])}\n")
        f.write(f"Failed:  {len(test_results['failed'])}\n")
        f.write(f"Skipped: {len(test_results['skipped'])}\n")
        f.write(f"Total:   {test_results['total']}\n\n")

        def write_list(title, items):
            if items:
                f.write(f"{title}\n")
                for item in items:
                    f.write(f"  - {item}\n")
                f.write("\n")

        write_list("Passed Tests:", test_results["passed"])
        write_list("Failed Tests:", test_results["failed"])
        write_list("Skipped Tests:", test_results["skipped"])

    print(f"\n[INFO] Test summary written to: {summary_file}")

@pytest.fixture(scope="session", autouse=True)
def create_logs_and_reports():
    """Create logs and reports folders at session start."""
    for folder in ["logs", "reports"]:
        path = ROOT_PATH / folder
        path.mkdir(parents=True, exist_ok=True)

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Ensure the stash has a fallback output_dir in case no test-specific one is set."""
    fallback = ROOT_PATH / ".test-fallback"
    fallback.mkdir(parents=True, exist_ok=True)
    config.stash['output_dir'] = fallback


