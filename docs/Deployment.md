# 部署与上线（让别人也能用）

> 重要：GitHub 本身只是托管代码。要让别人“打开链接就能用”，需要把 Demo 部署到一个能运行 Python Web 的平台。

---

## 0. 安全原则（必须）
- ✅ API Key 永远不要写进代码，也不要提交到 GitHub
- ✅ 使用 `.env`（本地）或平台的 Secrets（线上）
- ✅ 如果你担心别人用你的 Key 产生费用，建议：
  - 只开放本地运行（别人自己配置 key），或
  - 在线 Demo 开启“临时 key（BYOK）”模式

---

## 1. 上线方式 A：Streamlit Community Cloud（最推荐，最省事）
### 步骤
1) 把项目推到 GitHub（见下文）
2) 打开 Streamlit Cloud，连接你的 GitHub Repo
3) 选择入口文件：`app.py`
4) 在 Streamlit Cloud 的 **Secrets** 里配置：
```
SILICONFLOW_API_KEY=xxxx
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_CHAT_MODEL=Qwen/Qwen2.5-72B-Instruct
SILICONFLOW_EMBED_MODEL=BAAI/bge-m3
```
5) Deploy
6) 第一次打开页面时，点击“构建索引”即可使用

### 优点
- 0 运维、适合作品集
- 有公开链接，HR 一键体验

---

## 2. 上线方式 B：Hugging Face Spaces（也很常用）
### 步骤
1) 在 HuggingFace 创建 Space（选择 Streamlit）
2) 连接 GitHub 或直接上传代码
3) 在 Space 的 Secrets 配置环境变量（同上）
4) 运行即可

### 优点
- 社区常见、展示性强

---

## 3. 上线方式 C：Render / Railway / Fly.io（更像生产）
- 适合你想展示“工程交付能力”
- 需要你写 `Dockerfile`（可后续补充）
- 成本可能略高，但更灵活

---

## 4. 推到 GitHub（所有上线方式的前提）
### 初始化仓库
```bash
git init
git add .
git commit -m "init: AI PM KB RAG"
```

### 关联远端并推送
```bash
git remote add origin https://github.com/<yourname>/<repo>.git
git branch -M main
git push -u origin main
```

### 关键检查
- `.env` 没有被提交（已在 .gitignore）
- README 里没有写明文 key
