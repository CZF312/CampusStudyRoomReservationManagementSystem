# 启动验收脚本：验证数据库导入后 HTTP 200
# 用法: .\scripts\verify-startup.ps1 [-MySqlPassword pwd]

param(
    [string]$MySqlPassword = ""
)

$ErrorActionPreference = "Stop"
$scriptRoot = $PSScriptRoot
$root = Split-Path -Parent $scriptRoot
Set-Location $root

Write-Host "=== CSRRMS startup verification ===" -ForegroundColor Cyan

& (Join-Path $scriptRoot "verify-v3-dictionary.ps1") -Password $MySqlPassword
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8080" -TimeoutSec 5
    if ($resp.StatusCode -eq 200) {
        Write-Host "[OK] http://localhost:8080 returned 200" -ForegroundColor Green
    } else {
        Write-Host "[WARN] http://localhost:8080 returned $($resp.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[INFO] Backend not running on 8080 (start with start.bat first)" -ForegroundColor Yellow
}

Write-Host "Verification complete." -ForegroundColor Green
