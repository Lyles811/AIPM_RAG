from __future__ import annotations
import os
import time
import csv
from pathlib import Path
import streamlit as st

from rag.config import settings
from rag.pipeline import RAGPipeline
from rag.chunking import load_kb_chunks
from rag.embeddings import embed_texts
from rag.index import save_index, load_index

st.set_page_config(page_title="AI 产品经理知识库 RAG", page_icon="📚", layout="wide")

st.title("📚 AI 产品经理基础知识库问答（RAG）")

# ===== Demo Access Control (optional but recommended) =====
demo_pass = None
demo_max = None
try:
    if "DEMO_PASSCODE" in st.secrets:
        demo_pass = str(st.secrets["DEMO_PASSCODE"])
    if "DEMO_MAX_QUESTIONS" in st.secrets:
        demo_max = int(st.secrets["DEMO_MAX_QUESTIONS"])
except Exception:
    pass

# fallback to env (local)
demo_pass = demo_pass or os.getenv("DEMO_PASSCODE")
demo_max = demo_max or int(os.getenv("DEMO_MAX_QUESTIONS", "3"))

if demo_pass:
    with st.sidebar:
        st.subheader("访问控制")
        entered = st.text_input("演示访问码", type="password", placeholder="HR 我会单独发你")
    if entered != demo_pass:
        st.info("请输入演示访问码后再使用（用于防止公共链接被滥用）。")
        st.stop()

if "q_count" not in st.session_state:
    st.session_state.q_count = 0


st.caption("回答会基于知识库片段，并强制给出引用。适合作品集展示：PRD/MVP/评估/上线闭环。")

with st.sidebar:
    st.header("运行设置")
    st.write("你可以使用：环境变量 key（推荐）或临时输入 key（BYOK）。")
    byok = st.toggle("使用临时 API Key（不保存）", value=False)
    api_key = None
    if byok:
        api_key = st.text_input("SiliconFlow API Key", type="password")
    st.divider()
    st.subheader("RAG 参数")
    top_k = st.slider("Top-K", min_value=2, max_value=10, value=settings.top_k, step=1)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=float(settings.temperature), step=0.05)
    st.caption("提示：如果回答变飘，temperature 调低；如果太死板，调高一点。")

    st.divider()
    st.subheader("索引管理")
    idx = load_index(settings.index_dir)
    if idx is None:
        st.warning("未发现索引：需要先构建索引（第一次运行必做）。")
        if st.button("一键构建索引（可能耗时/产生 token 成本）"):
            if not (api_key or settings.api_key):
                st.error("缺少 API Key：请在 .env 配置 SILICONFLOW_API_KEY 或临时输入 key。")
            else:
                with st.status("正在构建索引...", expanded=True) as status:
                    chunks = load_kb_chunks(settings.kb_dir, settings.chunk_size, settings.chunk_overlap)
                    st.write(f"Loaded {len(chunks)} chunks.")
                    batch_size = 32
                    embeddings = []
                    texts = [c.text for c in chunks]
                    import numpy as np
                    for i in range(0, len(texts), batch_size):
                        batch = texts[i:i+batch_size]
                        vecs = embed_texts(batch, api_key=api_key)
                        embeddings.append(vecs)
                        st.write(f"Embedded {min(i+batch_size, len(texts))}/{len(texts)}")
                    emb = np.vstack(embeddings)
                    save_index(settings.index_dir, emb, chunks)
                    status.update(label="索引构建完成 ✅", state="complete", expanded=False)
    else:
        st.success("索引已就绪 ✅")

    st.divider()
    st.subheader("知识库说明")
    st.write("知识库文件在 `data/kb/`，你可以自行增删改，然后重新构建索引。")

# Main Q&A
question = st.text_area("输入你的问题", placeholder="例如：PRD 应该包含哪些部分？MVP 怎么划分？AI PM 怎么做 RAG 的验收指标？", height=110)

col1, col2 = st.columns([1, 3])
with col1:
    ask = st.button(
    "问一下",
    type="primary",
    use_container_width=True,
    disabled=(st.session_state.q_count >= demo_max)
)
with col2:
    st.write("")

if ask:
    if not question.strip():
        st.warning("请先输入问题。")
    else:
        pipeline = RAGPipeline(api_key=api_key if byok else None)
        t0 = time.time()
        try:
            answer_md, retrieved = pipeline.answer(question.strip(), top_k=top_k, temperature=temperature)
        except Exception as e:
            st.error(str(e))
            st.stop()
        t1 = time.time()

        st.subheader("✅ 回答")
        st.markdown(answer_md)

        st.subheader("📌 引用片段（Top-K）")
        for r in retrieved:
            with st.expander(f"{r.chunk_id} | {r.title} | score={r.score:.3f}"):
                st.write(r.text)
                st.caption(f"source: {r.source_path}")

        st.caption(f"Latency: {t1 - t0:.2f}s")

        st.session_state.q_count += 1
        st.sidebar.caption(f"本次演示已用：{st.session_state.q_count}/{demo_max}")


        st.divider()
        st.subheader("🧾 反馈（帮助你做数据闭环）")
        c1, c2, c3 = st.columns([1, 1, 3])
        with c1:
            like = st.button("👍 有用")
        with c2:
            dislike = st.button("👎 没用")
        with c3:
            reason = st.selectbox("如果没用，主要原因是？", ["（可选）", "答非所问", "引用不对", "缺信息/覆盖不足", "表述不清/太啰嗦"])

        def log_feedback(label: str):
            Path(settings.feedback_dir).mkdir(parents=True, exist_ok=True)
            fp = Path(settings.feedback_dir) / "feedback.csv"
            new_file = not fp.exists()
            with fp.open("a", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                if new_file:
                    w.writerow(["ts", "question", "label", "reason", "top_k", "temperature"])
                w.writerow([time.time(), question.strip(), label, reason, top_k, temperature])
            st.success("已记录反馈 ✅（data/feedback/feedback.csv）")

        if like:
            log_feedback("like")
        if dislike:
            log_feedback("dislike")
