"""algo-sage · 测试样例数据生成（T-A3 产出占位）。

生成「正常 / 边界 / 失败」三类数据，供 benchmark 引擎使用。
T-A3 完成后按算法域填充。
"""
from __future__ import annotations

import random
from typing import Any


def gen_normal(n: int = 1000, seed: int = 42) -> dict[str, Any]:
    rng = random.Random(seed)
    return {"n": n, "data": [rng.randint(0, 10**9) for _ in range(n)],
            "type": "normal"}


def gen_boundary(n: int = 1, seed: int = 7) -> dict[str, Any]:
    """边界：n=1 / 全相等 / 负权等触发 risk 路径。"""
    return {"n": n, "data": [0] * n, "type": "boundary"}


def gen_failure(n: int = 10**6, seed: int = 1) -> dict[str, Any]:
    """失败：超理论上限 / 错数据，触发 Agnes ④ 诊断。"""
    rng = random.Random(seed)
    return {"n": n, "data": [rng.randint(0, 10**18) for _ in range(n)],
            "type": "failure", "note": "超出默认参数范围"}


__all__ = ["gen_normal", "gen_boundary", "gen_failure"]
