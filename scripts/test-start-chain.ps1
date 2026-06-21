# Non-interactive self-test for start.bat chain (import + verify only)
# Usage: .\scripts\test-start-chain.ps1 [-Password pwd]

param([string]$Password = "123456")

$ErrorActionPreference = "Stop"
$scriptRoot = $PSScriptRoot
$root = Split-Path -Parent $scriptRoot
Set-Location $root
$env:CSRRM_SCRIPT_ROOT = $scriptRoot

Write-Host "=== CSRRMS start chain self-test ===" -ForegroundColor Cyan

$setup = Join-Path $scriptRoot "setup-after-clone.ps1"
& $setup -MySqlPassword $Password -SkipStart -NoBrowser
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] setup-after-clone exit $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

Write-Host "[PASS] setup-after-clone completed" -ForegroundColor Green
exit 0
