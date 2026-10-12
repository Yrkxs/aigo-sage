"""algo-sage · 测试占位。

T-A1/T-B1 完成后补：
- test_config.py：validate() 缺失/完整
- test_agh_client.py：chat_json mock（不真调网络）
- test_registry.py：20 算法注册
"""
from __future__ import annotations


def test_scaffold_runs() -> None:
    """地基完整性：确保各模块可导入。"""
    import importlib
    for mod in [
        "server.config", "server.main", "server.agh_client",
        "server.prompts", "server.recommend", "server.log",
        "algorithms.registry", "benchmark.engine", "benchmark.datasets",
    ]:
        importlib.import_module(mod)


if __name__ == "__main__":
    test_scaffold_runs()
    print("scaffold import OK")
