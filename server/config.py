"""algo-sage · 中央配置

从环境变量 / .env 读取 Agnes API 与运行参数。
T-A1 验收：api_test.py 通过且 base_url 回写实际值。
"""
from __future__ import annotations

import os
from pathlib import Path

_BASE = Path(__file__).resolve().parent.parent
_ENV_FILE = _BASE / ".env"

# 读取 .env（简单实现，无第三方依赖）
def _load_env_file() -> None:
    if not _ENV_FILE.exists():
        return
    for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())

_load_env_file()

# Agnes 官方 API（OpenAI 兼容 HTTP）
AGH_API_KEY: str = os.environ.get("AGH_API_KEY", "")
AGH_BASE_URL: str = os.environ.get("AGH_BASE_URL", "https://agnes-ai.cn")
AGH_MODEL: str = os.environ.get("AGH_MODEL", "agnes-3.0-flash")
AGH_TEMPERATURE: float = float(os.environ.get("AGH_TEMPERATURE", "0.2"))
AGH_TIMEOUT: int = int(os.environ.get("AGH_TIMEOUT", "60"))

# 服务
HOST: str = os.environ.get("HOST", "0.0.0.0")
PORT: int = int(os.environ.get("PORT", "8000"))

# 日志
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
LOG_DIR: Path = _BASE / "evidence" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def validate() -> list[str]:
    """返回缺失项清单（T-A1 用）。"""
    missing = []
    if not AGH_API_KEY or AGH_API_KEY.startswith("your_api_key"):
        missing.append("AGH_API_KEY")
    return missing


if __name__ == "__main__":
    print(f"model      = {AGH_MODEL}")
    print(f"base_url   = {AGH_BASE_URL}")
    print(f"key        = {'set' if AGH_API_KEY and not AGH_API_KEY.startswith('your_api_key') else 'MISSING'}")
    miss = validate()
    if miss:
        print(f"missing: {', '.join(miss)}")
    else:
        print("config OK")
