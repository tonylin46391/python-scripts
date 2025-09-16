@echo off
setlocal enabledelayedexpansion

REM 進入腳本所在目錄
cd /d "%~dp0"

REM 使用目前已安裝的 Python 與 pip
set PYEXE=python
%PYEXE% --version >nul 2>&1 || set PYEXE=py

echo === 檢查並安裝依賴 ===
%PYEXE% -m pip install --upgrade pip
%PYEXE% -m pip install streamlit gTTS pandas pyinstaller

echo === 以 PyInstaller 打包 ===
set NAME=WordPractice
set ENTRY=run_word_practice.py

REM 清除先前 build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist %NAME%.spec del /q %NAME%.spec

%PYEXE% -m PyInstaller ^
  --noconfirm ^
  --name %NAME% ^
  --onefile ^
  --windowed ^
  --add-data "word_practice_app.py;." ^
  "%ENTRY%"

if errorlevel 1 (
  echo 打包失敗。
  exit /b 1
)

echo.
echo 打包完成：dist\%NAME%.exe
echo 你可以將該檔案複製到桌面或建立捷徑。
exit /b 0


