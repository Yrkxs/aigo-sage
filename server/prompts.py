"""algo-sage · 4 段 prompt + JSON schema（T-B2 产出占位）。

对应 plan §2.4。T-B2 完成时按此生成可校验 schema 与注入 ALGO_LIBRARY_SUMMARY。
"""
from __future__ import annotations

import json

# ── ① 题面解析 ──────────────────────────────────────────────
PARSE_SYSTEM = """你是算法题面解析器。读题面，判断算法域与规模约束。只返回 JSON：
{"domain":"sorting|search|dp|graph","n":<int>,"constraints":[str],"key_features":str}
"""

# ── ② 推荐 + 调参 ────────────────────────────────────────────
RECOMMEND_SYSTEM = """你是算法推荐与调参专家。给定解析结果，从以下算法库选最优并给参数：
{ALGO_LIBRARY_SUMMARY}
只返回 JSON：
{"algorithm":str,"params":{...},"complexity":str,"reason":str,"risk":str}
"""

# ── ③ 代码实例化 ────────────────────────────────────────────
CODEGEN_SYSTEM = """你是竞赛代码生成器。基于算法库模板 {TEMPLATE_CODE} 与题面 {PROBLEM_TEXT}，
生成适配该题的完整可跑 Python 代码（含输入输出适配）。只输出代码块。
"""

# ── ④ 失败诊断 ──────────────────────────────────────────────
DIAGNOSE_SYSTEM = """你是算法错误诊断器。给定运行日志 {RUN_LOG} 与期望 {EXPECTED}，
定位失败原因（TLE/越界/错答/参数不当）并给修复建议。只返回 JSON：
{"error_type":str,"root_cause":str,"fix":str}
"""


def algo_library_summary() -> str:
    """T-A2 完成后，从 algorithms.registry 生成算法库摘要注入 ②。"""
    try:
        from algorithms.registry import all_algorithms
        lines = []
        for a in all_algorithms():
            lines.append(f"- {a['name']} [{a['category']}] {a['complexity']} "
                         f"{a['applicable']} 默认参数={a['params']}")
        return "\n".join(lines) or "(算法库未填充)"
    except Exception:  # noqa: BLE001
        return "(算法库未填充)"


def build_recommend_user(parse_result: dict) -> str:
    return "解析结果：" + json.dumps(parse_result, ensure_ascii=False)


__all__ = [
    "PARSE_SYSTEM", "RECOMMEND_SYSTEM", "CODEGEN_SYSTEM", "DIAGNOSE_SYSTEM",
    "algo_library_summary", "build_recommend_user",
]
