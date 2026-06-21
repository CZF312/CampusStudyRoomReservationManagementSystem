# 可选：将 start.bat 打包为单个 .exe（依赖 Windows 自带的 iexpress）
# 用法（在项目根目录）: .\scripts\build-launcher-exe.ps1
# 生成: dist\CSRRMS-Launcher.exe

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$bat = Join-Path $root "start.bat"
$vbs = Join-Path $root "start.vbs"
$dist = Join-Path $root "dist"
$outExe = Join-Path $dist "CSRRMS-Launcher.exe"

if (-not (Test-Path $bat)) { throw "missing start.bat" }

New-Item -ItemType Directory -Path $dist -Force | Out-Null

$sedPath = Join-Path $env:TEMP "csrrm_iexpress.sed"
$outEsc = $outExe -replace '\\', '\\'
$rootEsc = $root -replace '\\', '\\'

@"
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=0
HideExtractProgress=0
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=解压完成。请双击 start.bat 或 start.vbs 启动系统。
TargetName=%TargetName%
FriendlyName=CSRRMS Launcher
AppLaunched=cmd /c echo 请运行 start.bat
PostInstallCmd=<None>
AdminQuietInst=
UserQuietInst=
SourceFiles=SourceFiles
[Strings]
InstallPrompt=将解压校园自习室预约管理系统启动文件到当前目录，是否继续？
DisplayLicense=
TargetName=$outEsc
FriendlyName=CSRRMS
[SourceFiles]
SourceFiles0=$rootEsc
[SourceFiles0]
%FILE0%=start.bat
%FILE1%=start.vbs
"@ | Set-Content -Path $sedPath -Encoding ASCII

Write-Host "Building $outExe ..."
& iexpress /N $sedPath /Q
if ($LASTEXITCODE -ne 0) {
    Write-Host "iexpress failed. Use start.bat or start.vbs directly (double-click)." -ForegroundColor Yellow
    exit 1
}
Write-Host "OK: $outExe" -ForegroundColor Green
Write-Host "Note: JDK 21+ and MySQL 8 must still be installed on the target PC."
