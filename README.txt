ZipCLI - Flexible ZIP Archiver
==============================

Version: 1.1.0
Build Date: 2025-06-13

Description:
------------
ZipCLI is a command-line utility that creates ZIP archives from folders with flexible include/exclude filtering. It supports custom date-stamped filenames, inventory listing, and configurable backup locations.

Installation:
-------------
No installation required. Just unzip the downloaded file and double-click `zip-cli-v1.0.0.exe` in the folder, or run it from the command line.

Usage:
------
<!-- USAGE_START -->
📦 ZipCLI Usage Instructions (Updated: 6/13/2025 MM)

Run the tool from the command line using Python or a bundled .exe.

    zip-cli-v1.0.0.exe <folder> [--options]

Available Options:

    --filter <pattern>         Include files matching one or more glob patterns (e.g. "*.txt").

    --exclude <pattern>        Exclude files matching one or more glob patterns.

    --include <pattern>        Same as --filter (takes precedence if both are used).

    --date-format <format>     Customize the timestamp format used in the ZIP filename.
                               Default: "%Y%m%dT%H%M"

    --inventory                Print a list of all files included in the archive.

    --backup-location <path>   Folder where the .zip file will be saved. Defaults to current directory.

Examples:

    zip-cli-v1.0.0.exe myfolder

    zip-cli-v1.0.0.exe data --filter "*.csv" --exclude "secret*"

    zip-cli-v1.0.0.exe reports --include "*.pdf" --date-format "%Y-%m-%d" --inventory

    zip-cli-v1.0.0.exe logs --filter "*.log" --backup-location P:\Backups
<!-- USAGE_END -->

ZIP Output:
-----------
Each run creates a ZIP file with a name like:
    foldername_20250613T1245.zip

The file is saved either in the current working directory or the provided `--backup-location`.

Documentation:
--------------
Generated Sphinx documentation is available online:
https://mikemmattinson.github.io/py-zip-cli-v1/

Or build it locally by running:
    sphinx-build -b html docs/source docs/

Configuration:
--------------
No external config required. All options are passed as CLI arguments.

Advanced users can edit `main.py` or integrate ZipCLI as a module in their own Python scripts.

Support:
--------
For more information, visit:
https://github.com/MikeMMattinson/py-zip-cli-v1

To report a bug, please open an issue on GitHub.

License:
--------
This utility is provided as-is for personal and professional use.
