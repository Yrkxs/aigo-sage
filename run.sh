#!/usr/bin/env bash
# algo-sage · Linux/macOS 启动脚本
set -euo pipefail
cd "$(dirname "$0")"

# 提示 .env 存在
if [ ! -f .env ]; then
  echo "未找到 .env，已按 .env.example 提示。先执行: cp .env.example .env 并填入 AGH_API_KEY"
fi

# 优先用 venv
if [ -d .venv ]; then
  source .venv/bin/activate
fi

python server/main.py
