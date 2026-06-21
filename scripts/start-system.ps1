# 【F1-1·环境启动】功能链实例：组长双击 `start.bat` → PowerShell 导入 `database-full.sql` 建库 `study_room_reservation` → Spring Boot 监听 8080 → 浏览器打开登录页 → `… 本处职责：start.bat 调用本脚本，检测 Java/MySQL 并导入 database-full.sql
# Campus Study Room Reservation Management System - one-click launcher // 【行】执行本行语句，推进功能链中的当前步骤
# Environment check -> MySQL password -> DROP database -> import database-full.sql // 【行】执行本行语句，推进功能链中的当前步骤
# -> verify schema -> write local config -> start backend -> open browser // 【行】执行本行语句，推进功能链中的当前步骤

$ErrorActionPreference = "Stop" // 【行】执行本行语句，推进功能链中的当前步骤
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } elseif ($env:CSRRM_SCRIPT_ROOT) { $env:CSRRM_SCRIPT_ROOT } else { Join-Path (Get-Location) "scripts" }
$root = Split-Path -Parent $scriptRoot
Set-Location $root

$AppTitle = "Campus Study Room Reservation System"

function Write-Title {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " $AppTitle" -ForegroundColor Cyan
    Write-Host " One-Click Setup and Launch" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
}

function Write-Step([string]$message) {
    Write-Host ""
    Write-Host $message -ForegroundColor Yellow
}

function Require-Command([string]$name, [string]$hint) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        Write-Host "[ERROR] Command not found: $name" -ForegroundColor Red
        Write-Host "        $hint" -ForegroundColor Red
        exit 1
    }
}

function ConvertFrom-SecureStringPlain([securestring]$secure) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { [Runtime.InteropServices.Marshal]::PtrToStringAuto($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

function Get-LocalIPv4Addresses {
    try {
        @(Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop |
            Where-Object {
                $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" -and
                $_.IPAddress -notlike "198.18.*" -and
                $_.InterfaceAlias -notmatch "VMware|VirtualBox|Loopback|vEthernet"
            } | Select-Object -ExpandProperty IPAddress -Unique)
    } catch {
        @(ipconfig | Select-String "IPv4" | ForEach-Object { ($_ -split ":\s*", 2)[1].Trim() } |
            Where-Object { $_ -and $_ -notlike "127.*" -and $_ -notlike "169.254.*" } | Select-Object -Unique)
    }
}

function Test-MysqlLogin([string]$password) {
    $oldPwd = $env:MYSQL_PWD
    try {
        if ($password) { $env:MYSQL_PWD = $password } else { Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue }
        & mysql -uroot -h 127.0.0.1 -P 3306 -e "SELECT 1;" > $null 2> $null
        return ($LASTEXITCODE -eq 0)
    } finally {
        if ($null -ne $oldPwd) { $env:MYSQL_PWD = $oldPwd } else { Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue }
    }
}

function Get-ConfiguredMysqlPassword {
    $localProps = Join-Path $root "src\main\resources\application-local.properties"
    if (-not (Test-Path $localProps)) { return "" }
    $line = Get-Content -LiteralPath $localProps -Encoding UTF8 |
        Where-Object { $_ -match '^\s*spring\.datasource\.password\s*=' } | Select-Object -First 1
    if ($line -match '=\s*(.*)$') { return $Matches[1].Trim() }
    ""
}

Write-Title

# 编辑 Java 时若存成 UTF-8 BOM，javac 会报非法字符 \ufeff；启动前自动清理
$stripBom = Join-Path $scriptRoot "strip-java-bom.ps1"
if (Test-Path $stripBom) { & $stripBom | Out-Null }

if (-not (Test-Path (Join-Path $root "pom.xml"))) {
    Write-Host "[ERROR] pom.xml not found. Run start.bat from the project root." -ForegroundColor Red
    exit 1
}

Write-Step "[1/5] Check Java, MySQL client and static assets"
Require-Command "java" "Install JDK 21 or newer."
Require-Command "mysql" "Install MySQL 8 and add bin directory to PATH."

$javaVersionLine = (cmd /c "java -version 2>&1" | Select-Object -First 1)
Write-Host "Java: $javaVersionLine" -ForegroundColor Green
Write-Host "mysql: $((Get-Command mysql).Source)" -ForegroundColor Green

$staticIndex = Join-Path $root "src\main\resources\static\index.html"
if (-not (Test-Path $staticIndex)) {
    Write-Host "[ERROR] Prebuilt frontend missing: $staticIndex" -ForegroundColor Red
    Write-Host "        Re-download the full release package." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Frontend static bundle found" -ForegroundColor Green

$javaMajor = 0
if ($javaVersionLine -match '"(\d+)') { $javaMajor = [int]$Matches[1] }
$mvnJavaArg = ""
if ($javaMajor -eq 20) { $mvnJavaArg = "-Djava.version=20" }
elseif ($javaMajor -gt 0 -and $javaMajor -lt 21) {
    Write-Host "[WARN] JDK 21+ recommended. Current: $javaMajor" -ForegroundColor Yellow
}

Write-Step "[2/5] Check MySQL service"
$mysqlServices = @(Get-Service -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match 'mysql|mariadb' -or $_.DisplayName -match 'mysql|mariadb' } |
    Sort-Object Status, Name -Descending)
if ($mysqlServices.Count -eq 0) {
    Write-Host "[ERROR] No MySQL/MariaDB Windows service found." -ForegroundColor Red
    exit 1
}
$mysqlService = $mysqlServices | Where-Object { $_.Status -eq "Running" } | Select-Object -First 1
if (-not $mysqlService) {
    $mysqlService = $mysqlServices | Select-Object -First 1
    Write-Host "Starting MySQL service: $($mysqlService.Name)" -ForegroundColor Yellow
    Start-Service -Name $mysqlService.Name -ErrorAction Stop
    Start-Sleep -Seconds 3
    $mysqlService = Get-Service -Name $mysqlService.Name
}
if ($mysqlService.Status -ne "Running") {
    Write-Host "[ERROR] MySQL service is not running: $($mysqlService.Name)" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] MySQL service: $($mysqlService.Name)" -ForegroundColor Green

Write-Step "[3/5] Database password (saved to application-local.properties)"
$password = if ($env:CSRRM_MYSQL_PASSWORD) { $env:CSRRM_MYSQL_PASSWORD } else { Get-ConfiguredMysqlPassword }
if ($password -and (Test-MysqlLogin $password)) {
    Write-Host "[OK] Connected with saved password." -ForegroundColor Green
} elseif (Test-MysqlLogin "") {
    $password = ""
    Write-Host "[OK] Connected with empty root password." -ForegroundColor Green
} else {
    do {
        $secure = Read-Host "Enter local MySQL root password" -AsSecureString
        $password = ConvertFrom-SecureStringPlain $secure
        if (-not (Test-MysqlLogin $password)) {
            Write-Host "Password rejected. Try again." -ForegroundColor Red
            $password = $null
        }
    } while ($null -eq $password)
}

Write-Step "[4/5] Reset database and import database-full.sql"
$setupScript = Join-Path $scriptRoot "setup-after-clone.ps1"
& $setupScript -MySqlPassword $password -SkipStart -NoBrowser
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Step "[5/5] Start application server"
$listen = netstat -ano | Select-String ":8080\s+.*LISTENING"
if ($listen) {
    $alreadyUp = $false
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8080" -TimeoutSec 3
        if ($resp.StatusCode -eq 200) { $alreadyUp = $true }
    } catch { }
    if ($alreadyUp) {
        Write-Host "[OK] Port 8080 already serving the app (skip second instance)." -ForegroundColor Green
        if (-not $env:CSRRM_NONINTERACTIVE) {
            try { Start-Process "http://localhost:8080" } catch { }
        }
    } else {
        Write-Host "[WARN] Port 8080 in use but app not responding. Close the blocking process and retry." -ForegroundColor Yellow
        Write-Host "       netstat -ano | findstr :8080" -ForegroundColor Yellow
    }
} else {
    $mvnw = Join-Path $root "mvnw.cmd"
    $mvnLine = if ($mvnJavaArg) { "$mvnJavaArg spring-boot:run" } else { "spring-boot:run" }
    $cmdInner = "title CSRRMS-Backend && cd /d `"$root`" && `"$mvnw`" $mvnLine"
    Start-Process -FilePath "cmd.exe" -ArgumentList "/k", $cmdInner -WorkingDirectory $root
    Write-Host "[OK] Backend starting in window CSRRMS-Backend (keep it open)" -ForegroundColor Green

    $started = $false
    for ($i = 1; $i -le 60; $i++) {
        Start-Sleep -Seconds 1
        try {
            $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8080" -TimeoutSec 2
            if ($resp.StatusCode -eq 200) { $started = $true; break }
        } catch { }
        if ($i % 5 -eq 0) { Write-Host "." -NoNewline }
    }
    Write-Host ""
    if (-not $started) {
        Write-Host "[WARN] http://localhost:8080 not ready yet. Check CSRRMS-Backend window." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Access URL: http://localhost:8080" -ForegroundColor Green
foreach ($ip in (Get-LocalIPv4Addresses)) {
    Write-Host "LAN URL:    http://${ip}:8080" -ForegroundColor Green
}
Write-Host ""
Write-Host "Demo accounts:" -ForegroundColor Cyan
Write-Host "  Student: 202225220101 / 123456"
Write-Host "  Admin:   admin / admin123"
Write-Host ""
Write-Host "Do NOT close the CSRRMS-Backend window while using the system." -ForegroundColor Yellow

if (-not $env:CSRRM_NONINTERACTIVE) {
    try { Start-Process "http://localhost:8080" } catch { }
    Read-Host "Press Enter to close this setup window"
}
