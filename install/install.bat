@echo off

if exist "./TannerGame/game.py" (
  goto RUNGAME
)

where git 2>nul | findstr /i "git.exe"
if %errorlevel% == 0 (
  echo Git is installed.
  git.exe clone https://github.com/AmericanHuston/TannerGame.git
) else (
  echo Git is not installed or not in PATH, installing now
  winget install --id Git.Git -e --source winget
  git.exe clone https://github.com/AmericanHuston/TannerGame.git
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
  echo Python is installed.
  goto SKIP_PY
) else (
  echo Python is not installed, installing now
  winget install -e --id Python.Python.3.13
)
:SKIP_PY
pip install pygame
:RUNGAME
cd TannerGame/
python ./game.py
pause