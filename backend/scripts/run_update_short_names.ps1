# PowerShell 脚本：批量更新所有链接的 short_name

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "批量更新所有链接的 short_name" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# 切换到 backend 目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Split-Path -Parent $scriptDir
Set-Location $backendDir

# 激活虚拟环境
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "激活虚拟环境..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "警告：未找到虚拟环境，使用系统 Python" -ForegroundColor Yellow
}

# 运行脚本
Write-Host "开始运行更新脚本..." -ForegroundColor Green
Write-Host ""
python scripts\update_short_names.py

Read-Host "按 Enter 键退出"

