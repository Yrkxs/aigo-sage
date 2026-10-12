"""algo-sage · 基准引擎（T-A3 产出占位）。

计时、对拍、复杂度拟合。
T-A3 完成后：run(algorithm, params, sample_type) -> 计时表。
"""
from __future__ import annotations

import time
from typing import Any, Callable


def time_fn(fn: Callable[..., Any], *args, **kwargs) -> float:
    t0 = time.perf_counter()
    fn(*args, **kwargs)
    return time.perf_counter() - t0


def run_benchmark(algorithm: str, params: dict, sample_type: str) -> dict:
    """T-A3 完成后实现：生成 sample_type 数据 → 默认参数 vs 调优参数计时。"""
    return {
        "note": "T-A3 待实现",
        "algorithm": algorithm, "params": params, "sample_type": sample_type,
    }


__all__ = ["time_fn", "run_benchmark"]
