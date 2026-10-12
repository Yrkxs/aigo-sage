"""algo-sage · server.main

FastAPI 应用 + 静态前端挂载。
路由：GET /、/result、/report；POST /api/recommend、/api/benchmark；
GET /api/dataset、/api/log/{task_id}。
依赖 T-B3 完成后才有 /api/recommend 实质逻辑，当前为占位。
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from server import config

app = FastAPI(title="algo-sage", version="0.1.0")

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"


def _serve(name: str):
    p = FRONTEND / name
    return FileResponse(p) if p.exists() else FileResponse(FRONTEND / "index.html")


@app.get("/")
def home():
    return _serve("index.html")


@app.get("/result")
def result():
    return _serve("result.html")


@app.get("/report")
def report():
    return _serve("report.html")


@app.get("/api/health")
def health():
    return {"ok": True, "model": config.AGH_MODEL, "missing": config.validate()}


@app.get("/api/dataset")
def dataset():
    # T-A4 完成后返回 40 题列表
    return {"count": 0, "note": "dataset 未填充，见 T-A4"}


@app.post("/api/recommend")
async def recommend(payload: dict):
    # T-B3 完成后串联 4 段 Agnes 调用
    return {"note": "T-B3 待实现", "echo": payload}


@app.post("/api/benchmark")
async def benchmark(payload: dict):
    # T-A3 完成后跑计时
    return {"note": "T-A3 待实现", "echo": payload}


@app.get("/api/log/{task_id}")
def log(task_id: str):
    p = config.LOG_DIR / f"{task_id}.jsonl"
    if not p.exists():
        return {"task_id": task_id, "lines": 0}
    lines = [ln for ln in p.read_text().splitlines() if ln]
    return {"task_id": task_id, "lines": len(lines), "raw": lines}


# 静态资源
if FRONTEND.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host=config.HOST, port=config.PORT,
                reload=True)
