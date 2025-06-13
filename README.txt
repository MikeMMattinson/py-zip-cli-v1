SecureCLI - Secure Password Generator
=====================================

Version: 1.10.3
Build Date: 2025-05-30

Description:
------------
SecureCLI is a command-line utility that helps you generate secure, customizable passwords for different accounts. It supports per-account configuration, password history, and safety checks like repeated character limits and excluded symbols.

Installation:
-------------
No installation required. Just unzip the downloaded file and double-click `secure-cli-v1.10.0.exe` in the folder, or run it from the command line.

Usage:
------
<!-- USAGE_START -->
🔐 SecureCLI Usage Instructions

Run the tool from the command line using Python or a bundled .exe.
    secure-cli-v1.10.x.exe [--options]

Available Options:

    --account <name>       Generate and save a password for the given account.
                           Will create a new config based on default if missing.

    --update               Only generate new password if config is newer than saved file.

    --recover              Recover missing config from an existing password file.

    --report               Generate a summary report of all accounts and their last password.

    --verbose              Include extra details in the report.

Examples:

    secure-cli-v1.10.x.exe --account gmail

    secure-cli-v1.10.x.exe --account github --update

    secure-cli-v1.10.x.exe --recover --account gmail

    secure-cli-v1.10.x.exe --report --verbose

    secure-cli-v1.10.x.exe  # Runs the quick password generator with no arguments an
                            returns a single password.
<!-- USAGE_END -->


Password File Output:
---------------------
Each account has its own text file saved in the `passwords/` folder.

Format includes:
- Account name
- Metadata (username, email, notes)
- Manually added notes section
- Password generation history with timestamp

Configuration:
--------------
To customize settings, edit the `config/default.config` or create a new one like `config/github.config`.

Each config can define:
- min_length, max_length
- contain_upper, contain_lower, contain_number, contain_special
- exclude_special_characters
- max_repeating
- username, email, etc.

Support:
--------
For more information, visit:
https://github.com/MikeMMattinson/py-secure-cli-v1

To report a bug, please open an issue on GitHub.

License:
--------
This utility is provided as-is for personal and professional use.
