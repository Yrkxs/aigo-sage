"""algo-sage · 算法注册表（T-A2 产出占位）。

20 算法注册：name, category, impl, params, complexity, applicable, template_code。
T-A2 完成后在 sorting.py / search.py / dp.py / graph.py 中填充实际实现，
并在此注册。
"""
from __future__ import annotations

from typing import Callable, Any

# 注册表：module → list[registry entry]
_REGISTRY: dict[str, list[dict[str, Any]]] = {
    "sorting": [], "search": [], "dp": [], "graph": [],
}


def register(entry: dict[str, Any]) -> None:
    """entry: {name, category, impl, params, complexity, applicable, template_code}"""
    cat = entry["category"]
    _REGISTRY.setdefault(cat, []).append(entry)


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


__all__ = ["register", "all_algorithms", "get", "impl_map"]
