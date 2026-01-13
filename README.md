# AI 产品经理基础知识库 RAG（开源作品集项目）

> 一个“可复现、可评估、可部署”的 RAG 作品集项目：用你自己维护的 **AI 产品经理基础知识库（Markdown）** 做检索增强问答（RAG），回答时强制给出 **引用来源**，并支持 **反馈回流 + 离线评测**。

---

## 你能用这个项目证明什么能力（给 HR 看）
- 会写 **PRD / MVP / 验收口径**（见 `docs/PRD.md`）
- 会做 **RAG 闭环产品**：知识库→索引→问答→引用→反馈→评估→迭代
- 会做 **上线交付**：本地可运行、别人可复现、可部署到线上（见 `docs/Deployment.md`）

---

## 功能一览（MVP）
- ✅ 从 `data/kb/` 读取 Markdown 文档，自动切分 chunk 并建立向量索引  
- ✅ 输入问题后：检索相关片段 → 生成答案 → **列出引用来源**  
- ✅ 反馈按钮：👍/👎 + 原因（答非所问/引用不对/缺信息/表述不清）  
- ✅ 离线评测：用 `data/eval/golden.jsonl` 一键跑回归评测并生成报告（见 `docs/Evaluation.md`）

---

## 快速开始（本地运行，10 分钟以内）
### 1) 准备环境
```bash
# Python 3.10+ 推荐
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

### 2) 配置 SiliconFlow Key（不要提交到 GitHub）
复制并编辑 `.env`：
```bash
cp .env.example .env
# 把 SILICONFLOW_API_KEY 填成你的 key
```

### 3) 构建索引（第一次必须执行）
```bash
python ingest.py
```

### 4) 启动 Demo
```bash
streamlit run app.py
```

---

## 项目结构
```text
.
├─ app.py                 # Streamlit Web Demo
├─ ingest.py              # 知识库索引构建脚本（embedding + 向量索引）
├─ rag/                   # RAG 核心逻辑
├─ data/
│  ├─ kb/                 # ✅ 你的 AI 产品经理知识库（Markdown）
│  ├─ eval/               # 离线评测集（golden.jsonl）
│  └─ index/              # 生成的索引（默认不提交）
└─ docs/                  # PRD / MVP / 架构 / 评估 / 部署文档
```

---

## 部署到线上（让别人也能用）
GitHub 只是代码托管，要让别人“点开就能用”，需要把 Demo 部署到平台：
- Streamlit Community Cloud（推荐，最简单）
- Hugging Face Spaces（也很常见）
- Render / Railway / Fly.io（更像生产）
详见：`docs/Deployment.md`

---

## 知识库怎么扩展？
把你的 Markdown 放到 `data/kb/`，然后重新运行：
```bash
python ingest.py
```

---

## 免责声明
- 本项目用于学习与作品集展示，不提供法律/医疗等高风险建议。
- 线上 Demo 如使用你的 API Key，会产生 token 成本，请自行做好限流与风控。
