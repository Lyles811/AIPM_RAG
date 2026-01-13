# MVP 拆分（v0.1）

## Must（必须闭环）
- [ ] 知识库：读取 data/kb/*.md
- [ ] 索引：chunking → embedding → index 存储
- [ ] 问答：检索 top-k → 生成结构化回答
- [ ] 引用：答案中列出 chunk_id + 摘录依据
- [ ] 反馈：点赞/点踩 + 原因，写入 CSV
- [ ] 离线评测：golden.jsonl + 一键生成 report.md

## Nice-to-have（有更好）
- [ ] 支持 PDF 导入
- [ ] rerank（重排）
- [ ] 更严格的引用正确性评测
- [ ] “Bring Your Own Key” 模式更友好（多模型选择）

## Won’t（明确不做）
- [ ] 登录权限、多租户
- [ ] 支付/收费
- [ ] SLA、高并发
