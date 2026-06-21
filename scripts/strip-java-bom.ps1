# 去掉 Java 源文件开头的 UTF-8 BOM（\ufeff），避免 javac 报「非法字符」
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$fixed = 0
Get-ChildItem -Path (Join-Path $root "src") -Recurse -Filter "*.java" | ForEach-Object {
    $bytes = [IO.File]::ReadAllBytes($_.FullName)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        [IO.File]::WriteAllBytes($_.FullName, $bytes[3..($bytes.Length - 1)])
        Write-Host "[OK] removed BOM: $($_.FullName.Replace($root + '\', ''))" -ForegroundColor Green
        $fixed++
    }
}
if ($fixed -eq 0) {
    Write-Host "[OK] no BOM in Java sources" -ForegroundColor Green
} else {
    Write-Host "Fixed $fixed file(s). Re-run mvnw compile or start.bat." -ForegroundColor Yellow
}
