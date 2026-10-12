"""algo-sage · 题解算法识别与归类（T-A4 产出占位）。

优先级：CF tags → 题面/题解关键词 → Agnes 读题解 → 人工。
confidence<0.7 的题走 annotate.py 人工标注。
T-A4 完成后实现。
"""
from __future__ import annotations

from typing import Any

# 关键词 → 算法域映射（自动识别第二级）
KEYWORD_HINTS: dict[str, str] = {
    "排序": "sorting", "sort": "sorting", "bubble": "sorting",
    "quicksort": "sorting", "归并": "sorting", "堆排": "sorting",
    "二分": "search", "binary search": "search", "二分查找": "search",
    "最短路": "search", "shortest": "search", "bfs": "search",
    "dfs": "search", "dijkstra": "search",
    "背包": "dp", "knapsack": "dp", "lis": "dp", "lcs": "dp",
    "动态规划": "dp", "区间dp": "dp", "状压": "dp",
    "mst": "graph", "kruskal": "graph", "prim": "graph",
    "floyd": "graph", "拓扑": "graph", "topo": "graph",
    "强连通": "graph", "sc