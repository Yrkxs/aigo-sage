"""algo-sage · api_test.py

T-A1 验收脚本：最小连通性自测。
运行：python api_test.py
通过标准：返回 200 + 合法 JSON。
"""
from __future__ import annotations

import json
import sys
import time

import requests

from server import config


def main() -> int:
    miss = config.validate()
    if miss:
        print(f"[FAIL] 配置缺失: {', '.join(miss)}")
        print("请先 cp .env.example .env 并填入 AGH_API_KEY")
        return 1

    url = f"{config.AGH_BASE_URL.rstrip('/')}/v1/chat/completions"
    payload = {
        "model": config.AGH_MODEL,
        "temperature": config.AGH_TEMPERATURE,
        "messages": [{"role": "user", "content": '返回 JSON {"ok":true}'}],
    }
    headers = {
        "Authorization": f"Bearer {config.AGH_API_KEY}",
        "Content-Type": "application/json",
    }

    print(f"[POST] {url}")
    print(f"model  = {config.AGH_MODEL}")
    t0 = time.time()
    try:
        r = requests.post(url, json=payload, headers=headers,
                          timeout=config.AGH_TIMEOUT)
    except requests.RequestException as e:
        print(f"[FAIL] 网络异常: {e}")
        return 1

    dt = time.time() - t0
    print(f"status = {r.status_code}  ({dt:.2f}s)")
    print("body   = " + (r.text[:500] if r.text else "(empty)"))

    if r.status_code != 200:
        print("[FAIL] 非 200，按 plan §2.2 顺序换 base_url 重试")
        return 1

    try:
        data = r.json()
        # 仅做基本结构检查，不校验模型内容
        print("[OK] 收到合法 JSON，连通成功")
        return 0
    except json.JSONDecodeError:
        print("[FAIL] 响应非 JSON")
        return 1


if __name__ == "__main__":
    sys.exit(main())
