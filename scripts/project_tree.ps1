# scripts/tree.ps1
param (
    [string]$Path = ".",
    [string]$Output = "tree.txt",
    [string[]]$Exclude = @(".venv", "__pycache__", ".pytest_cache", ".git", "build", "dist"),
    [int]$Indent = 0
)

function Show-Tree {
    param (
        [string]$Path,
        [int]$Indent
    )

    Get-ChildItem -Path $Path -Force | ForEach-Object {
        if ($Exclude -contains $_.Name) {
            return
        }

        $prefix = " " * $Indent + "├── "
        $line = "$prefix$($_.Name)"
        $line | Out-File -Append -Encoding UTF8 $Output

        if ($_.PSIsContainer) {
            Show-Tree -Path $_.FullName -Indent ($Indent + 4)
        }
    }
}

# Clear output and start fresh
"📁 Project Tree: $Path" | Out-File -Encoding UTF8 $Output
Show-Tree -Path $Path -Indent $Indent
