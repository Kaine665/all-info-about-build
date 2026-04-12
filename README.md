# all-info-about-build

这是一个存放信息的仓库。从软件的创意、开发、获客、销售，我们都会收集相关的信息。

## 构建与协作

- **`inbox/`**：未整理的构建/分发/测试相关笔记；格式与校验见 [`inbox/README.md`](inbox/README.md)。  
- **CI**：修改 `inbox/` 或校验脚本时，GitHub Actions 会运行 `inbox validate`；本地可 `pip install -r requirements-ci.txt` 后执行 `python3 scripts/validate_inbox_frontmatter.py`。  
- **Agent 写入**：见 [`inbox/AGENT.md`](inbox/AGENT.md)。