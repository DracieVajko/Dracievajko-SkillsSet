#Requires -Version 5.1
<#
.SYNOPSIS
Reproduce this machine's agent-skill layout on another Windows PC.

.DESCRIPTION
Reads sync/manifest.json and, for every skill it lists:
  * installs the folder once under its install root
      - source.type=repo   -> copied from this repository's skills/original
      - source.type=github -> fetched with git sparse-checkout from upstream
      - source.type=unresolved -> reported, never guessed
  * recreates the directory junctions listed in mirrors[] so OpenCode, Claude
    Code, Pi and Cindy all see the same folders without duplicate copies.

Existing skill folders are left alone unless -Force is given. node_modules is
never copied; pass -InstallNodeModules to run npm install afterwards.

Cindy plugins are not files: the script prints the checklist from
sync/cindy-plugins.json so each one can be installed from the marketplace and
re-authorized on the new machine.

.PARAMETER DryRun
Show what would happen without touching the disk.

.EXAMPLE
.\scripts\sync-skills.ps1 -DryRun

.EXAMPLE
.\scripts\sync-skills.ps1

.EXAMPLE
.\scripts\sync-skills.ps1 -Force -InstallNodeModules
#>
[CmdletBinding()]
param(
    [string]$Manifest,
    [string]$Cache,
    [switch]$Force,
    [switch]$DryRun,
    [switch]$NoMirrors,
    [switch]$InstallNodeModules
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $Manifest) { $Manifest = Join-Path $repoRoot 'sync\manifest.json' }
if (-not $Cache) { $Cache = Join-Path $env:LOCALAPPDATA 'skills-sync\cache' }

function Expand-ManifestPath([string]$path) {
    return $ExecutionContext.InvokeCommand.ExpandString($path.Replace('~', '$env:USERPROFILE'))
}

function Get-FileHashSafe([string]$path) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { return $null }
    # Hash with line endings normalised so CRLF and LF copies compare equal.
    $text = [IO.File]::ReadAllText($path, [Text.Encoding]::UTF8).Replace("`r`n", "`n")
    $bytes = [Text.Encoding]::UTF8.GetBytes($text)
    $sha = [Security.Cryptography.SHA256]::Create()
    return ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join ''
}

function Test-Mirror([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return $false }
    $item = Get-Item -LiteralPath $path -Force
    return [bool]($item.Attributes -band [IO.FileAttributes]::ReparsePoint)
}

if (-not (Test-Path -LiteralPath $Manifest -PathType Leaf)) {
    throw "Manifest not found: $Manifest"
}
$data = Get-Content -LiteralPath $Manifest -Raw | ConvertFrom-Json

$roots = @{}
foreach ($name in $data.roots.PSObject.Properties.Name) {
    $roots[$name] = Expand-ManifestPath $data.roots.$name
    if (-not (Test-Path -LiteralPath $roots[$name])) {
        if ($DryRun) {
            Write-Host "would create skill root $($roots[$name])"
        } else {
            New-Item -ItemType Directory -Path $roots[$name] -Force | Out-Null
        }
    }
}

Write-Host "Manifest: $Manifest"
Write-Host "Skills:   $($data.skills.Count)   Mirrors: $($data.mirrors.Count)"
Write-Host ""

$installed = 0
$present = 0
$failed = @()
$unresolved = @()
$drifted = @()

foreach ($skill in $data.skills) {
    $name = $skill.name
    $dest = Join-Path $roots[$skill.root] $name
    $type = $skill.source.type

    if ($type -eq 'unresolved') {
        $unresolved += $name
        continue
    }

    $exists = Test-Path -LiteralPath $dest
    if ($exists -and -not $Force) {
        $hash = Get-FileHashSafe (Join-Path $dest 'SKILL.md')
        if ($hash -and $hash -ne $skill.sha256) {
            $drifted += $name
        }
        $present++
        continue
    }

    if ($DryRun) {
        Write-Host ("would install {0,-34} <- {1}" -f $name, $(if ($type -eq 'repo') { $skill.source.path } else { "$($skill.source.repo)/$($skill.source.path)" }))
        $installed++
        continue
    }

    try {
        if ($type -eq 'repo') {
            $sourceDir = Join-Path $repoRoot ($skill.source.path -replace '/', '\')
            if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
                throw "repository folder missing: $sourceDir"
            }
            if ($exists) { Remove-Item -LiteralPath $dest -Recurse -Force }
            Copy-Item -LiteralPath $sourceDir -Destination $dest -Recurse -Force
        }
        else {
            $repoName = ($skill.source.repo -replace '/', '__')
            $cloneDir = Join-Path $Cache $repoName
            if (-not (Test-Path -LiteralPath (Join-Path $cloneDir '.git'))) {
                New-Item -ItemType Directory -Path $Cache -Force | Out-Null
                Write-Host "  cloning $($skill.source.repo) (blobless)"
                & git clone --quiet --depth 1 --filter=blob:none --no-checkout "https://github.com/$($skill.source.repo).git" $cloneDir
                if ($LASTEXITCODE -ne 0) { throw "git clone failed for $($skill.source.repo)" }
            }
            & git -C $cloneDir sparse-checkout init --cone 2>$null | Out-Null
            & git -C $cloneDir sparse-checkout set $skill.source.path 2>$null | Out-Null
            & git -C $cloneDir checkout --quiet $skill.source.ref 2>$null | Out-Null
            if ($LASTEXITCODE -ne 0) {
                & git -C $cloneDir checkout --quiet 2>$null | Out-Null
            }
            $sourceDir = Join-Path $cloneDir ($skill.source.path -replace '/', '\')
            if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
                throw "upstream folder not found after checkout: $($skill.source.repo)/$($skill.source.path)"
            }
            if ($exists) { Remove-Item -LiteralPath $dest -Recurse -Force }
            Copy-Item -LiteralPath $sourceDir -Destination $dest -Recurse -Force -Exclude 'node_modules'
        }

        $hash = Get-FileHashSafe (Join-Path $dest 'SKILL.md')
        if ($hash -and $hash -ne $skill.sha256) {
            $drifted += $name
            Write-Host ("  installed {0} (SKILL.md differs from the reference machine)" -f $name)
        } else {
            Write-Host ("  installed {0}" -f $name)
        }
        $installed++
    }
    catch {
        $failed += "$name : $($_.Exception.Message)"
    }
}

if (-not $NoMirrors) {
    Write-Host ""
    Write-Host "Mirrors (directory junctions)"
    $linked = 0
    foreach ($rule in $data.mirrors) {
        $dir = Expand-ManifestPath $rule.dir
        if (-not $DryRun -and -not (Test-Path -LiteralPath $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        foreach ($name in $rule.only) {
            $link = Join-Path $dir $name
            $skill = $data.skills | Where-Object { $_.name -eq $name } | Select-Object -First 1
            if (-not $skill) { continue }
            $target = Join-Path $roots[$skill.root] $name
            if (-not (Test-Path -LiteralPath $target -PathType Container)) { continue }
            if (Test-Mirror $link) { continue }
            if (Test-Path -LiteralPath $link) {
                Write-Host ("  skipped {0} (real folder present)" -f $link)
                continue
            }
            if ($DryRun) {
                Write-Host ("  would link {0} -> {1}" -f $link, $target)
                $linked++
                continue
            }
            & cmd /c mklink /J "`"$link`"" "`"$target`"" | Out-Null
            if ($LASTEXITCODE -ne 0) { Write-Host ("  FAILED link {0}" -f $link) } else { $linked++ }
        }
    }
    Write-Host ("  {0} junction(s) {1}" -f $linked, $(if ($DryRun) { 'would be created' } else { 'created' }))
}

if ($InstallNodeModules -and -not $DryRun) {
    foreach ($skill in $data.skills) {
        if (-not $skill.needsNodeModules) { continue }
        $dest = Join-Path $roots[$skill.root] $skill.name
        if (-not (Test-Path -LiteralPath (Join-Path $dest 'package.json'))) { continue }
        Write-Host "  npm install in $($skill.name)"
        & npm install --omit=dev --prefix $dest 2>&1 | Out-Null
    }
}

$pluginsPath = Join-Path $repoRoot 'sync\cindy-plugins.json'
Write-Host ""
Write-Host "Summary: $installed installed, $present already present, $($failed.Count) failed, $($unresolved.Count) unresolved"
if ($drifted.Count -gt 0) {
    Write-Host "Upstream drift (SKILL.md hash differs): $($drifted -join ', ')"
}
if ($unresolved.Count -gt 0) {
    Write-Host "No identified upstream, copy by hand: $($unresolved -join ', ')"
}
if ($failed.Count -gt 0) {
    Write-Host "Failures:"
    $failed | ForEach-Object { Write-Host "  $_" }
}

if ((Test-Path -LiteralPath $pluginsPath -PathType Leaf)) {
    $plugins = Get-Content -LiteralPath $pluginsPath -Raw | ConvertFrom-Json
    Write-Host ""
    Write-Host "Cindy plugins to install from the marketplace ($($plugins.plugins.Count)):"
    $plugins.plugins | ForEach-Object {
        $ns = if ($_.namespace) { $_.namespace } else { 'public' }
        Write-Host ("  - {0}  (namespace: {1}; {2})" -f $_.id, $ns, $_.setup)
    }
    if ($plugins.opencodePlugins.Count -gt 0) {
        Write-Host "OpenCode plugins to keep in opencode.jsonc:"
        $plugins.opencodePlugins | ForEach-Object { Write-Host "  - $_" }
    }
}

if ($failed.Count -gt 0) { exit 1 }
exit 0
