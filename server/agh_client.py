"""algo-sage · Agnes API 客户端（T-B1 产出，此处为接口契约占位）。

契约：AgnesClient.chat_json(system, user, temperature=0.2, schema_hint="") -> dict
内部：拼 messages → POST → 解析 JSON → 失败重试 2 次 → 仍失败抛 AGHError。
每次调用记录：ts, segment, prompt_hash, response_json, latency_ms, retries，
写 evidence/logs/<task_id>.jsonl。
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone

from server import config


class AGHError(RuntimeError):
    pass


class AgnesClient:
    def __init__(self, api_key: str | None = None,
                 base_url: str | None = None,
                 model: str | None = None,
                 task_id: str | None = None):
        self.api_key = api_key or config.AGH_API_KEY
        self.base_url = (base_url or config.AGH_BASE_URL).rstrip("/")
        self.model = model or config.AGH_MODEL
        self.task_id = task_id

    def _post(self, system: str, user: str, temperature: float):
        import requests
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        t0 = time.time()
        r = requests.post(url, json=payload, headers=headers,
                          timeout=config.AGH_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        return content, time.time() - t0

    def chat_json(self, system: str, user: str,
                  temperature: float = 0.2, schema_hint: str = "") -> dict:
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                content, dt = self._post(system, user, temperature)
                text = content.strip()
                if text.startswith("```"):
                    text = text.strip("`")
                    if text.lower().startswith("json"):
                        text = text[4:]
                obj = json.loads(text)
                self._log("chat_json", system, user, obj, dt, attempt)
                return obj
            except Exception as e:  # noqa: BLE001
                last_err = e
        raise AGHError(f"chat_json 重试 3 次失败: {last_err}")

    def _log(self, segment: str, system: str, user: str, obj, dt: float,
             retries: int) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "segment": segment,
            "model": self.model,
            "prompt_hash": hashlib.sha1(
                (system + user).encode()).hexdigest()[:12],
            "response": obj,
            "latency_ms": round(dt * 1000, 1),
            "retries": retries,
            "task_id": self.task_id,
        }
        if self.task_id:
            path = config.LOG_DIR / f"{self.task_id}.jsonl"
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")


__all__ = ["AgnesClient", "AGHError"]
