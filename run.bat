@echo off
REM algo-sage · Windows 启动脚本
cd /d "%~dp0"

if not exist .env (
  echo 未找到 .env，已按 .env.example 提示。先执行: copy .env.example .env 并填入 AGH_API_KEY
)

if exist .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
)

python server\main.py
pause
