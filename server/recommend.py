"""algo-sage · 推荐编排（T-B3 产出占位）。

串联 ①→②→取模板→③→（失败则④），返回统一结果对象，
生成 task_id 并落日志（见 server.log）。
"""
from __future__ import annotations

import uuid
from typing import Any

from server import prompts
from server.agh_client import AgnesClient


def run_recommend(client: AgnesClient, task_id: str) -> dict[str, Any]:
    """T-B3 完成后实现完整 4 段编排；当前为接口占位。

    返回结构（T-B3 契约）：
    {algorithm, params, complexity, reason, risk,
     template_code, generated_code, task_id}
    """
    return {
        "note": "T-B3 待实现",
        "task_id": task_id,
        "prompts_loaded": bool(
            prompts.PARSE_SYSTEM and prompts.RECOMMEND_SYSTEM
            and prompts.CODEGEN_SYSTEM and prompts.DIAGNOSE_SYSTEM),
    }


def new_task_id() -> str:
    return uuid.uuid4().hex


__all__ = ["run_recommend", "new_task_id"]
