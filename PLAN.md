# algo-sage 项目执行计划（AlgoSage · 算法推荐与基准验证引擎）

> 团队 3 人 · 全 Agent 开发 · 3 天交付
> 目标赛事：2026 江苏省高校 AI+科学与工程创新实践黑客松
> 作品形态：本地 Web 应用（FastAPI 后端 + 静态前端）+ GitHub 公开仓库 + 演示视频 + 博客
> 本文档是后续 Agent 执行的唯一权威任务清单。每个任务编号（T-xx）均可独立验收。

## 目录

> **仓库与路径约定（定稿）**
> - GitHub 仓库：`https://github.com/Yrkxs/algo-sage.git`（目录/项目名统一写 `algo-sage`）
> - 本地脚手架根目录：`E:\Agnes_Hardness\algo-sage\`（独立子目录，自带 `.gitignore`，与外层 Agnes 主工程隔离，不继承外层 git）
> - 本计划文件：`E:\Agnes_Hardness\algo-sage-plan.md`（脚手架外的唯一权威任务清单）

## 0. 项目总览

### 0.1 一句话定义
输入竞赛题面或数据特征 → Agnes（agnes-3.0-flash，经 Agnes 官方 API）完成「题面解析 → 算法推荐+调参 → 代码实例化 → 失败诊断」4 段推理 → 本地算法库 + Benchmark 引擎实测验证 → 输出推荐结果与准确率量化报告。

### 0.2 核心指标（写入报告页，评委可见）
- 推荐准确率：推荐算法 == 官方题解算法 的比例（基于 40 题数据集）
- Benchmark 对比：推荐配置 vs 默认配置的运行时间差
- 调用链完整性：每道题产生 1 条完整 Agnes 调用日志

### 0.3 技术栈
- 后端：Python 3.10+，FastAPI，Pydantic
- 前端：静态 HTML + 原生 JS + Chart.js（免构建，免费好部署）
- 大模型：Agnes 官方 API（agnes-3.0-flash），OpenAI 兼容 HTTP 协议
- 数据：Codeforces API + 洛谷/CSP 真题汇总（人工精选）
- 版本控制：GitHub 公开仓库 `https://github.com/Yrkxs/algo-sage.git`（本地目录名 `algo-sage`）

### 0.4 三条硬依赖（必须最早解决）
1. Agnes API 连通性（M1，Day1 第一件事）
2. 40 题数据集落地（M3，Day2）
3. 全链路准确率跑通（M4，Day2）

### 0.5 交付边界（明确「做什么」与「不做什么」）
- 做：本地可运行的 Web 应用、40 题自动评估、3 类测试样例、完整日志证据
- 不做：云端部署（列为后续）、混合策略（保留接口不实现）、复杂动画


## 1. 系统架构

### 1.1 调用链（核心，对应赛事要求「≥1 条工具/设备调用链」）
1. 用户贴题面 / 选算法域 / 输入数据特征
2. 调 Agnes ① 题面解析 → {domain, n, constraints, key_features}
3. 调 Agnes ② 推荐+调参 → {algorithm, params, complexity, reason, risk}
4. 从本地算法库取对应模板
5. 调 Agnes ③ 按题面实例化可跑代码
6. Benchmark 引擎本地跑 3 类样例（正常/边界/失败）
7. 若失败 → 调 Agnes ④ 读日志诊断
8. 输出结果 + 全程日志落盘（JSONL）

每一步带时间戳与请求/响应快照，即「Agnes 参与核心任务证据」。

### 1.2 目录结构（Agent 必须按此建仓库）
```
algo-sage/
  README.md
  requirements.txt
  run.sh / run.bat
  api_test.py            # M1：API 连通性自测
  server/                # FastAPI 后端
    main.py              # 路由 + 挂载静态前端
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
    app.js style.js chart.js
  evidence/              # 运行证据（日志、截图占位）
```

### 1.3 后端 API 路由（前端调用）
- `GET /` 主页 · `GET /result` 结果页 · `GET /report` 报告页
- `POST /api/recommend` body={problem_text 或 domain+n+constraints} → 全链路结果
- `POST /api/benchmark` body={algorithm, params, sample_type} → 计时表
- `GET /api/dataset` 40 题列表 · `GET /api/log/{id}` 某条调用链日志

## 2. Agnes API 调用协议（AGH）

### 2.1 调用方式
- 端点：Agnes 官方 API，OpenAI 兼容（`/v1/chat/completions`）
- 协议：HTTP REST，`Authorization: Bearer <API_KEY>`
- 模型：`agnes-3.0-flash`（版本锁定，全程一致）
- 参数：`temperature` 推荐段 0.2（确定性优先），代码生成段 0.4
- 响应解析：要求 Agnes 返回 **严格 JSON**（prompt 中声明 schema + "只返回 JSON"）

### 2.2 端点验证（M1 必做）
- 若官方路径不确定，依次尝试：
  1. `https://agnes-ai.cn/v1/chat/completions`
  2. `https://api.agnes-ai.cn/v1/chat/completions`
  3. 从 API key 控制台页复制的 base_url
- 验证命令（T-A1 执行）：
```bash
curl -sS -X POST "<base_url>/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"agnes-3.0-flash","messages":[{"role":"user","content":"返回 JSON {\"ok":true}"}]}'
```
- 通过标准：返回 200 + 合法 JSON 响应。记录 base_url 到 `server/config.py` 的 `AGH_BASE_URL`。

### 2.3 统一客户端（T-A2 产出 `server/agh_client.py`）
```python
class AgnesClient:
    def __init__(self, api_key, base_url, model="agnes-3.0-flash")
    def chat_json(self, system, user, temperature=0.2, schema_hint="") -> dict
    # 内部：拼 messages → POST → 解析 JSON → 失败重试 2 次 → 仍失败抛 AGHError
```
- 每次调用记录：ts, segment, prompt_hash, response_json, latency_ms, retries
- 日志写 `evidence/logs/<task_id>.jsonl`（JSONL，一行一次调用）

### 2.4 4 段 Prompt（写在 `server/prompts.py`，Agent 按此生成）

**① 题面解析 SYSTEM**
```
你是算法题面解析器。读题面，判断算法域与规模约束。只返回 JSON：
{"domain":"sorting|search|dp|graph","n":<int>,"constraints":[str],"key_features":str}
```

**② 推荐+调参 SYSTEM**
```
你是算法推荐与调参专家。给定解析结果，从以下算法库选最优并给参数：
{ALGO_LIBRARY_SUMMARY}
只返回 JSON：
{"algorithm":str,"params":{...},"complexity":str,"reason":str,"risk":str}
```

**③ 代码实例化 SYSTEM**
```
你是竞赛代码生成器。基于算法库模板 {TEMPLATE_CODE} 与题面 {PROBLEM_TEXT}，
生成适配该题的完整可跑 Python 代码（含输入输出适配）。只输出代码块。
```

**④ 失败诊断 SYSTEM**
```
你是算法错误诊断器。给定运行日志 {RUN_LOG} 与期望 {EXPECTED}，
定位失败原因（TLE/越界/错答/参数不当）并给修复建议。只返回 JSON：
{"error_type":str,"root_cause":str,"fix":str}
```

## 3. 算法库 v1（20 个）

每个算法在 `algorithms/<category>.py` 中定义，并在 `algorithms/registry.py` 注册。
注册项必须含：`name, category, impl(callable), params(dict 默认值), complexity, applicable(str), template_code(str)`。

### 3.1 排序（5）
| 算法 | 默认参数 | 复杂度 | 适用特征 |
|---|---|---|---|
| 冒泡 | `{}` | O(n²) | n≤2000，教学 |
| 快排 | `pivot=median, recursion_limit=40` | O(n log n) 均 | 通用，随机数据 |
| 归并 | `merge_depth=0` | O(n log n) 稳 | 需稳定排序 |
| 堆排 | `{}` | O(n log n) | 内存受限 |
| 计数/桶 | `k=100` | O(n+k) | 值域小 |

### 3.2 搜索（5）
| 算法 | 默认参数 | 复杂度 | 适用特征 |
|---|---|---|---|
| 二分 | `{}` | O(log n) | 有序 |
| BFS | `{}` | O(V+E) | 无权最短路 |
| DFS | `{}` | O(V+E) | 连通性/拓扑 |
| Dijkstra | `impl=heap` | O((V+E)logV) | 非负权 |
| A* | `heuristic=euclid, h_scale=1.0` | 依赖 h | 启发搜索 |

### 3.3 DP（5）
| 算法 | 默认参数 | 复杂度 | 适用特征 |
|---|---|---|---|
| 01 背包 | `optim=rolling` | O(n·C) | 容量 C 不大 |
| LIS | `variant=nlogn` | O(n log n) | 最长递增 |
| LCS | `{}` | O(nm) | 两序列 |
| 区间 DP | `{}` | O(n³) | 区间转移 |
| 状压 DP | `state=1<<m` | O(2^m·n) | m≤20 |

### 3.4 图（5）
| 算法 | 默认参数 | 复杂度 | 适用特征 |
|---|---|---|---|
| Kruskal | `union_path_compress=true` | O(E log E) | MST 稀疏 |
| Prim | `impl=heap` | O((V+E)logV) | MST 稠密 |
| Floyd | `{}` | O(V³) | 全源 V≤500 |
| Topo | `{}` | O(V+E) | DAG 排序 |
| Tarjan(SCC) | `{}` | O(V+E) | 强连通 |

### 3.5 参数调优实验矩阵（benchmark 用）
每个算法选 2-3 个关键参数，生成「默认 vs 调优」两列对比，证明「调参环节价值」。

## 4. 数据集与标注规范（40 题，方案 Z）

### 4.1 数据来源
- 主源：Codeforces API（带 tags，自动拉取）
  - tags：`sorting`、`binary-search`、`graphs`、`dp`、`shortest-path`、`graphs`、`dfs-and-similar`、`data-structures`
  - 难度过滤：`rating` 1600-2600（保证有明确最优算法）
- 辅源：洛谷 / CSP / ICPC 真题汇总站，人工精选 10-15 道经典题

### 4.2 目标分布（40 题）
| 算法域 | 题数 | 代表题 |
|---|---|---|
| 排序 | 8 | CF 常见 + 手工 |
| 搜索 | 8 | BFS/Dijkstra 经典 |
| DP | 10 | 背包/LIS/区间 |
| 图 | 8 | MST/拓扑/SCC |
| 综合 | 6 | 多算法组合 |

### 4.3 识别优先级（自动→人工）
1. CF tags 直接映射（自动，最高优先）
2. 题面 + 官方题解关键词匹配（"最短路"→Dijkstra，"背包"→01背包）
3. Agnes 批量读题解归类（`classify.py` 自动跑，给 confidence）
4. confidence<0.7 或无法映射 → 人工标（`annotate.py` 生成 CSV，人工 30-40 分钟标 15 道）

### 4.4 数据格式（`dataset/json/*.json`，每题一条）
```json
{"id":"CF-xxxx","domain":"graph","tags":["shortest-path"],
 "problem_text":"...","official_algorithm":"Dijkstra",
 "official_solution_summary":"...","n_max":2e5,"source":"codeforces",
 "ground_truth_verified":true}
```

### 4.5 双轨用途（Z）
- 自动评估轨：40 题全喂系统，统计「推荐==官方」准确率（报告页核心指标）
- 演示轨：现场贴新题走全链路

## 5. Web UI 规格（3 页面 + 1 静态）

### 5.1 主页 `index.html`
- 输入区：题面文本框（贴 CF/洛谷题面）
- 算法域选择（4 选 1 或自动）+ 数据规模 n 输入 + 约束标签（时间/空间）
- 「开始推荐」按钮 → `POST /api/recommend`
- 下方：算法域卡片（展示 20 算法库）

### 5.2 结果页 `result.html`
- 推荐算法 + 理由 + 复杂度 + risk 提示
- 参数面板（默认参数 vs 调优参数，可改后重新 benchmark）
- 代码区：① 算法库模板（稳，主展示）② 现场生成代码（标「实验性」，供演示）
- 3 类样例结果：正常/边界/失败（Chart.js 柱状图：推荐 vs 默认 vs 失败诊断）
- 「查看完整调用链日志」按钮 → `/log/{id}`

### 5.3 报告页 `report.html`
- 准确率仪表盘（40 题自动评估结果，按算法域分组）
- 调用链示例（可展开一条完整 JSONL）
- 截图占位区（提交时填）

### 5.4 通用
- 静态文件，免构建；Chart.js 用 CDN（免费）
- 全程日志：每次 `/api/recommend` 生成 `task_id`，写入 `evidence/logs/<task_id>.jsonl`

## 6. 三人任务清单（纯 Agent 开发，三人各盯一条线）

> 说明：三人不手写代码，全部由 Agent 生成；三人职责是「下指令 + 验收 + 拍板」。每个任务有【产出】【验收】两行，验收不过不进入下一个任务。

---

### 线 A · 工程线（盯 M1 / M2 / M4）——负责人 A

**T-A1 API 连通自测**
- 产出：`api_test.py`（读 `server/config.py` 的 AGH_BASE_URL/API_KEY/MODEL，发一条最小请求，打印响应与耗时）
- 验收：`python api_test.py` 返回 200 + 合法 JSON；base_url 已回写 config。【若不通，按 §2.2 顺序换 base_url，仍不通则上报】

**T-A2 算法库 20 模板 + 注册表**
- 产出：`algorithms/{sorting,search,dp,graph}.py`（每个算法可调用实现 + 默认参数 + 复杂度 + 适用特征）、`algorithms/registry.py`
- 验收：`python -c "from algorithms.registry import all_algorithms; print(len(all_algorithms()))"` 输出 20；随机取 3 个算法各跑一次不报错

**T-A3 Benchmark 引擎**
- 产出：`benchmark/engine.py`（计时、对拍、复杂度拟合）、`benchmark/datasets.py`（生成正常/边界/失败 3 类数据）
- 验收：对任意算法 × 3 类数据，输出计时表（默认参数 vs 调优参数）；边界数据能触发 risk 路径

**T-A4 拉题脚本**
- 产出：`scripts/fetch_cf.py`（按 tag+rating 拉题，存 `dataset/cf_raw/`）、`scripts/classify.py`（关键词+Agnes 自动归类，写 confidence）、`scripts/annotate.py`（导出 `dataset/annotations.csv` 待人工）
- 验收：`fetch_cf.py` 拉到 ≥40 题原始 JSON；`classify.py` 跑完每行有 confidence；导出 CSV 中需人工行 ≤15

**T-A5 全链路自动化评估**
- 产出：`scripts/eval_all.py`（遍历 40 题：调 `/api/recommend` → 比对 official_algorithm → 统计准确率）
- 验收：输出「总体准确率 X%，分域准确率表」，并生成 `evidence/accuracy_report.json`；全程日志落盘

---

### 线 B · Agent 线（盯 M1 / M4 / M5）——负责人 B

**T-B1 统一 Agnes 客户端**
- 产出：`server/agh_client.py`（AgnesClient.chat_json，含重试/超时/JSON 校验/日志落盘）
- 验收：单测 4 段调用各跑 1 次，均返回符合 schema 的 dict；`evidence/logs/` 生成 JSONL；断网时正确报 AGHError 而非崩

**T-B2 4 段 Prompt + JSON schema**
- 产出：`server/prompts.py`（§2.4 的 4 段 SYSTEM + 各段 schema 定义 + 校验器）
- 验收：每段 schema 能校验合法/非法 JSON；非法时给出明确字段错误；推荐段注入 ALGO_LIBRARY_SUMMARY（自动从 registry 生成）

**T-B3 推荐编排**
- 产出：`server/recommend.py`（串联 ①→②→取模板→③→（失败则④），返回统一结果对象；生成 task_id 并落日志）
- 验收：对 1 道 Dijkstra 题，输出 {algorithm,params,complexity,reason,risk,template_code,generated_code,task_id}；调用链日志 4 段齐全

**T-B4 失败诊断闭环**
- 产出：`recommend.py` 中 ④ 段接入 + `benchmark/engine.py` 暴露运行日志给 Agnes
- 验收：构造一个 TLE 样例，④ 段返回 {error_type:"TLE", root_cause, fix}；失败证据写入日志

**T-B5 日志与证据规范**
- 产出：`server/log.py`（JSONL 写入、task_id 索引、导出单条调用链 markdown/截图）
- 验收：`/api/log/{task_id}` 返回一条完整调用链（含 4 段 prompt/响应/时间戳）；可一键导出为提交材料

---

### 线 C · 交付线（盯 M3 / M5 / M6）——负责人 C

**T-C1 前端 3 页面**
- 产出：`frontend/{index,result,report}.html` + `app.js` + `chart.js` 集成（按 §5 规格）
- 验收：浏览器三页可导航；主页提交 → 结果页展示推荐/参数/图表/代码/调用链；报告页展示准确率仪表盘；无控制台报错

**T-C2 人工标注 40 题**
- 产出：`dataset/annotations.csv` 填完（对 confidence<0.7 的 15 题补 ground_truth_verified）
- 验收：40 题 JSON 全部 `ground_truth_verified:true`；与官方题解抽检 5 道一致

**T-C3 演示视频脚本 + 录屏**
- 产出：3-5 分钟视频脚本（§8 模板）+ 录屏 + 剪辑；主链接（B站/YouTube 免费）+ 备用链接（GitHub 仓库存 raw）
- 验收：时长 3-5min；展示完整链路 + 准确率 + 调用链；评委无需登录个人账号可看

**T-C4 仓库与 README**
- 产出：`README.md`（§9 模板：安装/运行/架构/证据/测试样例/复现）、`run.sh`+`run.bat`、`.gitignore`（排除 API_KEY、evidence 日志）
- 验收：干净机器 `git clone` → `pip install -r requirements.txt` → `python run` 一次跑通

**T-C5 博客/知乎 + 提交文档**
- 产出：1 篇公开技术博客（含平台、有效链接、截图、发布日期）、`submission.md`（§8 提交材料对照表逐项填）
- 验收：博客已发布（截止前 1 天）；`submission.md` 每项必填都有对应产出物路径；三类测试样例各 ≥2 条

<!-- SECTION:AGENTB -->
（线 B 任务已并入 §6；此标记保留以便后续分拆）
<!-- SECTION:AGENTC -->
（线 C 任务已并入 §6；此标记保留以便后续分拆）
## 7. 里程碑（3 天 6 个，全部可验收）

### Day 1
**M1 Agnes 链路打通**（最高优先，卡住全停）
- 完成 T-A1 + T-B1
- 验收：`python api_test.py` 通过，4 段调用各返回合法 JSON

**M2 算法库 + Benchmark 引擎**
- 完成 T-A2 + T-A3
- 验收：20 算法注册，随机 3 个能跑，3 类数据计时表输出

### Day 2
**M3 拉题 + 自动/人工归类 40 题**
- 完成 T-A4 + T-C2
- 验收：`dataset/` 40 条，全部 ground_truth_verified

**M4 全链路跑通（推荐+调参+代码+benchmark+准确率）**
- 完成 T-B3 + T-B4 + T-B5 + T-A5
- 验收：`eval_all.py` 输出准确率报告；演示轨可现场贴题；调用链日志 4 段齐全

### Day 3
**M5 Web UI 3 页面 + 全程日志落盘**
- 完成 T-C1
- 验收：浏览器走完整流程；日志目录完整

**M6 交付物**
- 完成 T-C3 + T-C4 + T-C5 + Ubuntu 复现录屏
- 验收：视频 3-5min；干净 Ubuntu 克隆跑通；博客已发布；`submission.md` 完整

### 每日 17:00 同步会（10 分钟）
- 三人各报「已完成 T-xx + 验收状态 + 明日阻塞」
- 任何 M 级未达成 → 当日必须上报，不得隐瞒

## 8. 提交材料对照表（赛事必填逐项）

| 赛事必填项 | 我们的产出 | 任务 | 状态 |
|---|---|---|---|
| 项目名称 | AlgoSage——算法推荐与基准验证引擎 | T-C5 | ☐ |
| 参考方向 | 数学AI、算法发现（可多选） | T-C5 | ☐ |
| 项目摘要 | 输入题面→Agnes 推荐+调参+生成代码→benchmark 验证，准确率量化 | T-C5 | ☐ |
| 问题来源 | CF/ICPC/CSP 40 题 + 官方题解 | T-A4 | ☐ |
| AGH 作用 | Agnes 官方 API 做 4 段推理核心 | T-B1 | ☐ |
| Agnes 名称/版本/环节/调用 | agnes-3.0-flash / 解析·推荐·代码·诊断 4 环节 / HTTP REST | T-B1 | ☐ |
| 数据/代码/软件/环境 | Python+FastAPI、算法库 20、CF API、Win 开发 / Ubuntu 复现 | T-C4 | ☐ |
| 可运行作品 | GitHub 仓库 + 本地复现说明（在线部署列后续） | T-C4 | ☐ |
| 演示视频 | 3-5min，主链接=B站/YouTube，备用=GitHub raw | T-C3 | ☐ |
| 运行证据 | 日志目录 + ≥1 条完整调用链截图 + 准确率结果 | T-B5 | ☐ |
| 测试样例 | 正常/边界/失败 各 2-3 | T-C5 | ☐ |
| 成员声明 | 三人 + 全 agent 开发说明 | T-C5 | ☐ |
| 公开内容 | GitHub 仓库 + 知乎/博客（截止前 1 天发，含截图+日期） | T-C5 | ☐ |

## 9. 风险与对策

| 风险 | 对策 | 责任 |
|---|---|---|
| Agnes endpoint 路径不确定（最大） | Day1 M1 先试 `/v1/chat/completions`，不通换 base_url；卡死降级为通用 OpenAI 兼容协议 | A |
| 40 题人工标注超时 | 仅 15 道人工，其余靠 tag+关键词；准确率按「可标注子集」算 | C |
| Web UI 做不完 | 降级为单页 + 结果折叠，核心保功能 | C |
| 现场生成代码 bug | 默认展示算法库模板（稳），生成代码标「实验性」不入准确率 | B |
| Ubuntu 复现依赖 | 写死 requirements.txt，M6 录一次 pip install | C |
| 日志证据不完整 | T-B5 统一规范，`/api/log/{id}` 一键导出 | B |

## 10. 提交前清单（Go / No-Go）
- [ ] `python api_test.py` 通过
- [ ] 20 算法注册通过
- [ ] 40 题全部 verified
- [ ] `eval_all.py` 准确率报告存在
- [ ] 3 页面无报错，调用链可查
- [ ] 视频 3-5min 已上传（评委免登录可看）
- [ ] GitHub 公开仓库 + README 干净机跑通
- [ ] 博客已发布（截止前 1 天）
- [ ] 三类测试样例各 ≥2，写入 submission.md
- [ ] Ubuntu 复现录屏

## 11. 每日站会 / 验收模板

```
线 [A/B/C] · [姓名] · [日期]
完成：T-xx 验收=通过/未通过/阻塞
产出物：[路径]
明日：T-xx
阻塞：[无 / 描述 + 需要的支持]
```

（风险/提交/站会模板已并入 §8-§11）
（风险/提交/站会模板已并入 §8-§11）
