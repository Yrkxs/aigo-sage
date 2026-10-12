"""algo-sage · 算法注册表（T-A2 产出占位）。

v1 核心 4 域 20 算法 + v2 扩展 5 域 40 算法（共 60，见 PLAN.md §3）。
注册项：name, category, impl, params, complexity, applicable, template_code。

扩展性：_REGISTRY 是 dict-of-lists，register() 用 setdefault，任意新 category
自动可用；ALGO_LIBRARY_SUMMARY 遍历 all_algorithms() 生成，加域不改 ② 段逻辑。
T-A2 在 sorting/search/dp/graph/nt/ds/string/geo/flow/greedy 中填充实现并注册。
"""
from __future__ import annotations

from typing import Callable, Any

# 注册表：category → list[registry entry]
# v1 前 4 域 + v2 预留 5 域，加新域直接 setdefault 即可
_REGISTRY: dict[str, list[dict[str, Any]]] = {
    "sorting": [], "search": [], "dp": [], "graph": [],
    # v2 扩展域（PLAN.md §3.5-§3.10）
    "nt": [], "ds": [], "string": [], "geo": [], "flow": [], "greedy": [],
}

# domain 代号 → 中文名（前端卡片/报告分组用）
DOMAIN_LABELS: dict[str, str] = {
    "sorting": "排序", "search": "搜索", "dp": "DP", "graph": "图",
    "nt": "数论", "ds": "数据结构", "string": "字符串",
    "geo": "计算几何", "flow": "网络流", "greedy": "贪心/博弈",
}


def register(entry: dict[str, Any]) -> None:
    """entry: {name, category, impl, params, complexity, applicable, template_code}"""
    cat = entry["category"]
    _REGISTRY.setdefault(cat, []).append(entry)


def categories() -> list[str]:
    return list(_REGISTRY.keys())


def all_algorithms() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for entries in _REGISTRY.values():
        out.extend(entries)
    return out


def get(name: str) -> dict[str, Any] | None:
    for e in all_algorithms():
        if e["name"] == name:
            return e
    return None


def impl_map() -> dict[str, Callable[..., Any]]:
    return {e["name"]: e["impl"] for e in all_algorithms()}


__all__ = ["register", "categories", "all_algorithms", "get", "impl_map", "DOMAIN_LABELS"]
