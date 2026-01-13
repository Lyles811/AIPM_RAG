SYSTEM_PROMPT = """你是一名资深 AI 产品经理教练。你将基于【检索到的知识库片段】回答用户问题。
要求：
1) 只根据片段回答；如果片段不足以支撑结论，请明确说“知识库未覆盖/信息不足”，并给出你需要的补充信息。
2) 输出必须结构化，包含：结论、解释、可执行清单（如果适用）、引用来源。
3) 严禁编造来源；引用只来自提供的片段。
"""

def build_user_prompt(question: str, contexts: list[dict]) -> str:
    # contexts: [{"chunk_id","title","text"}]
    ctx_lines = []
    for i, c in enumerate(contexts, start=1):
        ctx_lines.append(f"[片段{i}] {c['chunk_id']} | {c['title']}\n{c['text']}\n")
    ctx_block = "\n".join(ctx_lines)
    return f"""问题：
{question}

检索到的知识库片段：
{ctx_block}

请按如下格式输出（Markdown）：
## 结论
...

## 解释
...

## 可执行清单
- ...

## 引用来源
- chunk_id：...
  - 关键依据：...（摘录 1-2 句即可）
"""
