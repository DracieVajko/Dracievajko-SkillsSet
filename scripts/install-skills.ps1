<#
.SYNOPSIS
Install every original skill into an OpenCode skills directory.

.DESCRIPTION
Copies the folders under skills/original/ into the target directory. If a
skill folder already exists, it is moved to a timestamped backup first.

.PARAMETER Target
Destination skills directory. Defaults to ~/.config/opencode/skills.

.PARAMETER BackupRoot
Directory for replaced skill folders. Defaults to
~/.config/opencode/skill-backups.

.EXAMPLE
.\scripts\install-skills.ps1

.EXAMPLE
.\scripts\install-skills.ps1 -Target .agents\skills

.EXAMPLE
.\scripts\install-skills.ps1 -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Target = (Join-Path $env:USERPROFILE '.config\opencode\skills'),
    [string]$BackupRoot = (Join-Path $env:USERPROFILE '.config\opencode\skill-backups')
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = Join-Path $repoRoot 'skills\original'

if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
    throw "Skill source directory not found: $sourceDir"
}

$skills = Get-ChildItem -LiteralPath $sourceDir -Directory | Sort-Object Name
if ($skills.Count -eq 0) {
    throw "No skills found under: $sourceDir"
}

if (-not (Test-Path -LiteralPath $Target -PathType Container)) {
    if ($PSCmdlet.ShouldProcess($Target, 'Create skills directory')) {
        New-Item -ItemType Directory -Path $Target -Force | Out-Null
    }
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$installed = 0

foreach ($skill in $skills) {
    $destination = Join-Path $Target $skill.Name

    if (Test-Path -LiteralPath $destination) {
        $backup = Join-Path (Join-Path $BackupRoot $timestamp) $skill.Name
        if ($PSCmdlet.ShouldProcess($destination, "Back up existing folder to $backup and replace")) {
            $backupParent = Split-Path -Parent $backup
            New-Item -ItemType Directory -Path $backupParent -Force | Out-Null
            Move-Item -LiteralPath $destination -Destination $backup
        }
    }

    if ($PSCmdlet.ShouldProcess($destination, "Install $($skill.Name)")) {
        Copy-Item -LiteralPath $skill.FullName -Destination $destination -Recurse -Force
        Write-Host "Installed $($skill.Name) -> $destination"
        $installed++
    }
}

if ($PSCmdlet.ShouldProcess($Target, "Installed $installed skill(s)")) {
    Write-Host "Done: $installed skill(s) installed in $Target"
}
