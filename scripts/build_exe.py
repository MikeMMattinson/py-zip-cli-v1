#!/usr/bin/env python3
"""
Script:     build_exe.py
Purpose:    Builds versioned .exe from main.py, updates README.txt with usage section,
            and organizes everything into versioned folders. Also creates a .zip and copies
            it to /mnt/zipcli (Samba share) or Windows network share for distribution.
"""

import re
import shutil
import platform
from pathlib import Path
import subprocess

SOURCE = Path("main.py")
README = Path("README.txt")
USAGE = Path("USAGE.txt")
SHARE_MOUNT_PATH = Path("/mnt/zipcli")  # Mounted Samba share (Linux)

# Extract version from main.py
MATCH = re.search(r'__version__\s*=\s*"(.+?)"', SOURCE.read_text(encoding="utf-8"))
version = MATCH.group(1) if MATCH else "0.0.0"
base_name = f"zip-cli-v{version}"
exe_name = f"{base_name}.exe"

def extract_usage_from_docstring(source_path: Path) -> str:
    text = source_path.read_text(encoding="utf-8")
    match = re.search(r'"""(.*?)"""', text, re.DOTALL)
    if match:
        doc = match.group(1)
        usage_lines = []
        capture = False
        for line in doc.splitlines():
            if "example usage" in line.lower() or "usage" in line.lower():
                capture = True
            if capture:
                usage_lines.append(line)
        return "\n".join(usage_lines).strip()
    return "[Usage section not found in main.py]"

def update_readme_usage(readme_path: Path, usage_text: str):
    content = readme_path.read_text(encoding="utf-8")
    if "<!-- USAGE_START -->" not in content or "<!-- USAGE_END -->" not in content:
        print("⚠️  README.txt is missing USAGE markers. Skipping usage injection.")
        return

    before = content.split("<!-- USAGE_START -->")[0]
    after = content.split("<!-- USAGE_END -->")[-1]
    new_section = f"<!-- USAGE_START -->\n{usage_text}\n<!-- USAGE_END -->"
    updated = f"{before}{new_section}{after}"
    readme_path.write_text(updated.strip() + "\n", encoding="utf-8")
    print("📝 Injected usage section into README.txt")

# Step 1: Build the .exe with PyInstaller
subprocess.run([
    "pyinstaller",
    "--onefile",
    "--paths=lib",
    "--name", base_name,
    "main.py"
], check=True)

# Step 2: Move .exe to versioned subfolder under dist/
dist_dir = Path("dist")
target_folder = dist_dir / base_name
target_folder.mkdir(exist_ok=True)

shutil.move(str(dist_dir / exe_name), str(target_folder / exe_name))
print(f"📦 Moved {exe_name} to {target_folder}")

# Step 3: Inject usage section and copy README
if README.exists():
    if USAGE.exists():
        usage = USAGE.read_text(encoding="utf-8").strip()
        print("📘 Using USAGE.txt content")
    else:
        usage = extract_usage_from_docstring(SOURCE)
        print("📘 Extracted usage from main.py docstring")
    update_readme_usage(README, usage)
    shutil.copy(README, target_folder)
    print(f"📄 Copied updated README.txt to {target_folder}")
else:
    print("⚠️ README.txt not found. Skipping.")

# Step 4: Create ZIP of versioned folder
zip_path = dist_dir / f"{base_name}.zip"
shutil.make_archive(str(zip_path.with_suffix('')), 'zip', target_folder)
print(f"📦 Created ZIP archive: {zip_path}")


# Step 5: Deploy ZIP to network share
if platform.system() == "Windows":
    win_share_path = Path(r"\\oscar\Zip-CLI")  # Adjust for your actual network path
    if win_share_path.exists() and win_share_path.is_dir():
        shutil.copy(zip_path, win_share_path)
        print(f"🌍 Deployed ZIP to Windows network share: {win_share_path / zip_path.name}")
    else:
        print(f"❌ Windows network share not found: {win_share_path}")
else:
    if SHARE_MOUNT_PATH.exists() and SHARE_MOUNT_PATH.is_dir():
        shutil.copy(zip_path, SHARE_MOUNT_PATH)
        print(f"🌍 Deployed ZIP to Linux mount: {SHARE_MOUNT_PATH / zip_path.name}")
    else:
        print(f"❌ Linux mount path not found: {SHARE_MOUNT_PATH}")
