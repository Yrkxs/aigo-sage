"""algo-sage · 日志与证据规范（T-B5 产出占位）。

JSONL 写入、task_id 索引、导出单条调用链（markdown/截图）。
"""
from __future__ import annotations

import json
from pathlib import Path

from server import config


def append(task_id: str, entry: dict) -> None:
    path = config.LOG_DIR / f"{task_id}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load(task_id: str) -> list[dict]:
    path = config.LOG_DIR / f"{task_id}.jsonl"
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text().splitlines() if ln]


def export_markdown(task_id: str, out: str | None = None) -> str:
    """导出单条调用链为 markdown（提交材料用）。"""
    lines = load(task_id)
    md = [f"# 调用链 {task_id}", ""]
    for i, e in enumerate(lines, 1):
        md += [f"## 步骤 {i} · {e.get('segment')} · {e.get('ts')}"]
        md += [f"- latency_ms: {e.get('latency_ms')}",
               f"- retries: {e.get('retries')}",
               "```json",
               json.dumps(e.get("response"), ensure_ascii=False, indent=2),
               "```", ""]
    text = "\n".join(md)
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return text


__all__ = ["append", "load", "export_markdown"]
