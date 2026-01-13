# 架构说明（v0.1）

## 目标
用最小的工程复杂度，搭建一个可复现的 RAG Demo：
- 依赖少、部署简单
- 能做离线评测与迭代对比
- 适合作品集展示

## 模块
1) Ingest（离线/一次性）
- 读取 Markdown 文档
- 切分为 chunks（chunk_size + overlap）
- 调用 Embedding API 得到向量
- 保存 embeddings.npy + meta.json

2) Query（在线/每次问答）
- 计算 query embedding
- 余弦相似度 top-k 检索
- 组织 Prompt（系统约束：只根据片段回答）
- 调用 Chat Completion 生成结构化回答
- 展示引用片段

3) Feedback（在线）
- 记录 👍/👎 + 原因 到 CSV

4) Eval（离线）
- 用 golden.jsonl 对问答做回归评测，输出 report.md

## 为什么不用复杂向量库？
- 作品集阶段数据量小（几百个 chunk），O(N) 检索足够
- 少依赖、少坑，更容易部署到线上
- 后续可替换为 Chroma/FAISS/PGVector
