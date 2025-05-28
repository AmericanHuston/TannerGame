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

cd TannerGame/
where python 2>nul | findstr /i "python.exe"
if %errorlevel% == 0(
  echo Python is installed.
  goto RUNGAME
) else (
  winget install -e --id Python.Python.3.13
)
:RUNGAME

pip install pygame

python ./game.py