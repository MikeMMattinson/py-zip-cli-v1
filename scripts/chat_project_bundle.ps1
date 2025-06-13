#chat_project_bundle.ps1

<#
.SYNOPSIS
    Bundles essential VS Code project files into a ZIP for ChatGPT 4o sharing.

.OUTPUTS
    Creates a zip archive in the current directory with today's date.

.NOTES
    Author: Mike & ChatGPT
    Date: 2025-06-03
#>

# === Set Output Name ===
$DateStr = Get-Date -Format "yyyyMMdd"
$ZipName = "chat_project_bundle_$DateStr.zip"
$ZipPath = Join-Path -Path "." -ChildPath $ZipName

# === Paths to Include ===
$includePaths = @(
    ".vscode",
    "config",
    "lib",
    "scripts",
    "tests",
    "securecli.py",
    "README.md",
    "README.txt",
    "USAGE.txt",
    "requirements.txt",
    "requirements-dev.txt",
    "setup.cfg",
    "pytest.ini",
    "LICENSE",
    "conftest.py",
    "tree.txt",
    "securecli.spec"
)

# === Exclude unwanted files ===
$excludePatterns = @(
    "*.log",
    "*.txt",
    ".gitkeep",
    ".coverage",
    "htmlcov",
    ".test-*",
    "*.spec"
)

# === Cleanup old zip if it exists ===
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# === Create ZIP ===
Add-Type -AssemblyName 'System.IO.Compression.FileSystem'
$zip = [System.IO.Compression.ZipFile]

# Temp folder to build minimal bundle
$tempFolder = Join-Path $env:TEMP "chat_project_bundle_$DateStr"
Remove-Item $tempFolder -Recurse -Force -ErrorAction SilentlyContinue
New-Item -Path $tempFolder -ItemType Directory | Out-Null

# Copy relevant files to temp
foreach ($item in $includePaths) {
    if (Test-Path $item) {
        Copy-Item -Path $item -Destination $tempFolder -Recurse -Force
    }
}

# Remove excluded patterns
foreach ($pattern in $excludePatterns) {
    Get-ChildItem -Path $tempFolder -Recurse -Include $pattern | Remove-Item -Force -ErrorAction SilentlyContinue
}

# Create zip archive from temp
[System.IO.Compression.ZipFile]::CreateFromDirectory($tempFolder, $ZipPath)

# Clean up temp
Remove-Item $tempFolder -Recurse -Force

Write-Host "✅ Project bundled to $ZipPath"
