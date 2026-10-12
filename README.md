# algo-sage

> AlgoSage · 算法推荐与基准验证引擎
> 2026 江苏省高校 AI+科学与工程创新实践黑客松参赛作品

输入竞赛题面或数据特征 → Agnes（`agnes-3.0-flash`，经 Agnes 官方 API）完成
「题面解析 → 算法推荐+调参 → 代码实例化 → 失败诊断」4 段推理 →
本地算法库 + Benchmark 引擎实测验证 → 输出推荐结果与准确率量化报告。

## 核心指标

- **推荐准确率**：推荐算法 == 官方题解算法的比例（基于 40 题数据集）
- **Benchmark 对比**：推荐配置 vs 默认配置的运行时间差
- **调用链完整性**：每道题产生 1 条完整 Agnes 调用日志（JSONL）

## 技术栈

- 后端：Python 3.10+，FastAPI，Pydantic
- 前端：静态 HTML + 原生 JS + Chart.js（免构建）
- 大模型：Agnes 官方 API（`agnes-3.0-flash`），OpenAI 兼容 HTTP 协议
- 数据：Codeforces API + 洛谷/CSP 真题汇总
- 版本控制：GitHub 公开仓库 `algo-sage`

## 目录结构

```
algo-sage/
  README.md
  requirements.txt
  run.sh / run.bat
  api_test.py            # M1：API 连通性自测（stub，待 T-A1 实现）
  server/                # FastAPI 后端
    main.py              # 路由 + 挂载静态前端
    config.py            # API_KEY / AGH_BASE_URL / MODEL（读环境变量）
    agh_client.py        # Agnes API 客户端（统一封装 4 段调用）
    prompts.py           # 4 段 prompt 模板 + JSON schema
    recommend.py         # 推荐编排（串联 4 段）
    log.py               # JSONL 日志落盘
  algorithms/            # 20 算法模板
    __init__.py
    registry.py          # 算法注册表（name→实现+参数+复杂度）
    sorting.py search.py dp.py graph.py
  benchmark/             # 基准引擎
    engine.py            # 计时、对拍、复杂度拟合
    datasets.py          # 生成正常/边界/失败数据
  dataset/               # 40 题 JSON + ground truth
    cf_raw/ json/ annotations.csv
  scripts/               # 工具脚本
    fetch_cf.py classify.py annotate.py eval_all.py
  frontend/              # 静态前端
    index.html result.html report.html
    app.js style.css
  evidence/              # 运行证据（日志、截图占位）
  tests/                 # 单元 / 集成测试
```

## 安装

```bash
# 1. 克隆仓库
git clone <repo-url>
cd algo-sage

# 2. 创建虚拟环境
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# Linux/macOS:
#   source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key（复制 .env.example 为 .env，填入你的 key）
cp .env.example .env
# 编辑 .env：AGH_API_KEY=你的key

# 5. 运行
bash run.sh      # Windows: run.bat
# 或
python server/main.py
```

服务默认监听 `http://localhost:8000`，前端 3 页面：

- `http://localhost:8000/` 主页（输入题面/选算法域）
- `http://localhost:8000/result` 推荐结果页
- `http://localhost:8000/report` 准确率报告页

## 调用链（对应赛事「≥1 条工具/设备调用链」）

1. 用户贴题面 / 选算法域 / 输入数据特征
2. 调 Agnes ① 题面解析 → `{domain, n, constraints, key_features}`
3. 调 Agnes ② 推荐+调参 → `{algorithm, params, complexity, reason, risk}`
4. 从本地算法库取对应模板
5. 调 Agnes ③ 按题面实例化可跑代码
6. Benchmark 引擎本地跑 3 类样例（正常/边界/失败）
7. 若失败 → 调 Agnes ④ 读日志诊断
8. 输出结果 + 全程日志落盘（`evidence/logs/<task_id>.jsonl`）

## 测试样例（正常 / 边界 / 失败 三类）

| 类型 | 例 | 预期 |
|---|---|---|
| 正常 | 标准 Dijkstra 稀疏图题 | 推荐 Dijkstra，跑通，准确率 ✓ |
| 边界 | n=1 / 全相等 / 负权 | 触发 risk 提示，换 Bellman-Ford，跑通 |
| 失败 | 数据超理论上限 / 错数据 | 第④段 Agnes 诊断出"超范围，建议…" |

## 证据与提交

- 运行证据：`evidence/` 下的 JSONL 日志 + 截图
- 提交文档：`submission.md`（赛事 13 项必填对照）
- 演示视频：3-5min，主链接 B站/YouTube，备用 GitHub raw

## 状态

**项目地基阶段**：目录骨架、配置、依赖、启动脚本已就绪。
业务实现（算法库 20 模板、Agnes 4 段编排、benchmark 引擎、Web UI）待后续
按 `../algo-sage-plan.md` 中的任务清单（T-A1 ~ T-C5）推进。

## License

MIT
