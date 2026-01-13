from __future__ import annotations
import json
import time
from pathlib import Path
from rag.pipeline import RAGPipeline
from rag.config import settings

def load_cases(path: str):
    cases = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            cases.append(json.loads(line))
    return cases

def simple_score(answer_md: str, must_include: list[str]) -> tuple[int, int]:
    hit = 0
    for k in must_include:
        if k.strip() and k.strip() in answer_md:
            hit += 1
    return hit, len(must_include)

def main():
    cases_path = Path("data/eval/golden.jsonl")
    if not cases_path.exists():
        raise RuntimeError("Missing data/eval/golden.jsonl")
    cases = load_cases(str(cases_path))
    pipe = RAGPipeline()

    total = 0
    hit_sum = 0
    start = time.time()
    for i, c in enumerate(cases, 1):
        q = c["question"]
        must = c.get("must_include", [])
        ans, _ = pipe.answer(q, top_k=settings.top_k, temperature=settings.temperature)
        hit, denom = simple_score(ans, must)
        hit_sum += hit
        total += denom
        print(f"[{i}/{len(cases)}] hit {hit}/{denom} | {q}")

    dur = time.time() - start
    score = (hit_sum / total) if total else 0.0
    report = f"""# 离线评测报告

- 用例数：{len(cases)}
- must_include 总数：{total}
- 命中数：{hit_sum}
- 命中率（粗略）：{score:.2%}
- 耗时：{dur:.1f}s

> 说明：这是一个最小可用的规则评测。你可以在 `docs/Evaluation.md` 按步骤逐步升级到更严谨的评测（结构化输出、引用正确性、人工评分等）。
"""
    Path("data/eval").mkdir(parents=True, exist_ok=True)
    Path("data/eval/report.md").write_text(report, encoding="utf-8")
    print("Saved: data/eval/report.md")

if __name__ == "__main__":
    main()
