// algo-sage · 前端逻辑（T-C1 占位）
document.getElementById("recommend-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    problem_text: document.getElementById("problem-text").value,
    domain: document.getElementById("domain").value,
    n: Number(document.getElementById("n").value),
  };
  try {
    const r = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await r.json();
    console.log("recommend:", data);
    alert("已提交（T-B3 完成后返回真实推荐）");
  } catch (err) {
    alert("请求失败：" + err);
  }
});
