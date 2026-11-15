# 一键打包 LiveThemeEditor 为单文件 exe（Windows / PowerShell）
# 用法：powershell -ExecutionPolicy Bypass -File tools\build.ps1

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot

# 1. 找一个带 tkinter 的 python
$candidates = @()
if ($env:PYTHON) { $candidates += $env:PYTHON }
$candidates += "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe"
$candidates += (Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -First 1)

$py = $null
foreach ($c in $candidates) {
    if (-not $c) { continue }
    if (-not (Test-Path -LiteralPath $c)) { continue }
    try {
        & $c -c "import tkinter" *> $null
        if ($LASTEXITCODE -eq 0) { $py = $c; break }
    } catch { }
}
if (-not $py) { throw "找不到带 tkinter 的 Python，请设置 PYTHON 环境变量指向它" }
Write-Host "using python: $py"

# 2. Microsoft Store 版 Python 关掉了 user site，需要手动把 user-site 加进 PYTHONPATH
$storeSite = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages"
if (Test-Path -LiteralPath $storeSite) { $env:PYTHONPATH = $storeSite }

# 3. 检查 PyInstaller
& $py -c "import PyInstaller" 2> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not found, installing..."
    & $py -m pip install --disable-pip-version-check pyinstaller
}

# 4. 打包
& $py -m PyInstaller --noconfirm --clean --onefile --windowed --name LiveThemeEditor `
    --icon (Join-Path $root 'assets\icon.ico') `
    --version-file (Join-Path $root 'tools\version_info.txt') `
    --distpath (Join-Path $root 'dist') `
    --workpath (Join-Path $root 'build') `
    --specpath (Join-Path $root 'build') `
    (Join-Path $root 'live_theme_editor.py')

Write-Host "`nDone: $(Join-Path $root 'dist\LiveThemeEditor.exe')"
