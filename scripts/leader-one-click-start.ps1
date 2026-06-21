# Legacy alias — forwards to unified launcher (do not use Invoke-Expression from .bat)
$ErrorActionPreference = "Stop"
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } elseif ($env:CSRRM_SCRIPT_ROOT) { $env:CSRRM_SCRIPT_ROOT } else { Join-Path (Get-Location) "scripts" }
$launcher = Join-Path $scriptRoot "start-system.ps1"
if (-not (Test-Path -LiteralPath $launcher)) {
    Write-Host "[ERROR] Missing start-system.ps1" -ForegroundColor Red
    exit 1
}
& $launcher
exit $LASTEXITCODE
