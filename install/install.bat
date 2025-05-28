@echo off

where git 2>nul | findstr /i "git.exe"
if %errorlevel% == 0 (
  echo Git is installed.
  git.exe clone https://github.com/AmericanHuston/TannerGame.git
) else (
  echo Git is not installed or not in PATH, installing now
  winget install --id Git.Git -e --source winget
  git.exe clone https://github.com/AmericanHuston/TannerGame.git
)
pause

cd TannerGame/

winget install -e --id Python.Python.3.13

pip install pygame

python ./game.py