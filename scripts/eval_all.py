"""algo-sage · 全链路自动化评估（T-A5 产出占位）。

遍历 40 题：调 /api/recommend → 比对 official_algorithm → 统计准确率，
生成 evidence/accuracy_report.json。
T-A5 完成后实现（依赖 T-B3 + T-A4）。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATASET = Path(__file__).resolve().parent.parent / "dataset" / "json"
EVIDENCE = Path(__file__).resolve().parent.parent / "evidence"


def eval_all() -> dict[str, Any]:
    """T-A5：跑 40 题自动评估，输出总体/分域准确率。"""
    raise NotImplementedError("T-A5 待实现")


def save_report(report: dict[str, Any]) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "accuracy_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


__all__ = ["eval_all", "save_report"]
