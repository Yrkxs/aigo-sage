"""algo-sage · 拉题脚本（T-A4 产出占位）。

fetch_cf.py：按 tag + rating 拉 Codeforces 题，存 dataset/cf_raw/
classify.py：关键词 + Agnes 自动归类，写 confidence
annotate.py：导出 dataset/annotations.csv 待人工
T-A4 完成后实现。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RAW_DIR = Path(__file__).resolve().parent.parent / "dataset" / "cf_raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_cf(tags: list[str], rating_min: int = 1600,
             rating_max: int = 2600, limit: int = 40) -> list[dict[str, Any]]:
    """T-A4：调 CF API，按 tag+rating 过滤，返回题面 JSON。"""
    raise NotImplementedError("T-A4 待实现")


def classify(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """T-A4：对每题给 confidence（自动 tag/关键词 + Agnes）。"""
    raise NotImplementedError("T-A4 待实现")


def export_annotations_csv(items: list[dict[str, Any]],
                           out: str | None = None) -> str:
    """T-A4：导出 confidence<0.7 的题到 CSV，人工标注。"""
    raise NotImplementedError("T-A4 待实现")


def save_raw(items: list[dict[str, Any]]) -> None:
    for it in items:
        (RAW_DIR / f"{it.get('id','unknown')}.json").write_text(
            json.dumps(it, ensure_ascii=False, indent=2), encoding="utf-8")


__all__ = ["fetch_cf", "classify", "export_annotations_csv", "save_raw"]
