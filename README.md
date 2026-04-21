# all-info-about-build

这是一个存放信息的仓库。从软件的创意、开发、获客、销售，我们都会收集相关的信息。

## inbox 使用方法（收件箱）

`inbox/` 是**未整理信息的收件箱**（构建、分发、测试、环境等草稿），**不是**规范或产品的单一真相源；定稿内容应写入根目录 `README`、`SPEC`、`docs/` 等正式位置。

### 何时用、怎么用

1. **有零碎结论或待决问题**、还不适合直接改正式文档时，在 `inbox/` 下**新建一篇** Markdown 文件。  
2. **推荐文件名**：`YYYY-MM-DD-<主题短名>.md`（同日多篇可加 `-2` 等后缀）。  
3. **不在 inbox 做同主题合并**：多一篇就多一篇；去重与正式结构在**迁出到 `docs/` / SPEC 等**时由人类流程处理（委托 Agent 写入时见 [`inbox/AGENT.md`](inbox/AGENT.md)）。  
4. **每条文件须满足**（与 CI 校验一致，详见 [`inbox/README.md`](inbox/README.md)）：  
   - 仅 **`.md`**，UTF-8，文首 **YAML frontmatter**，至少含 `title`、`status`（`draft` | `open` | `absorbed` | `obsolete`）、`created`（`YYYY-MM-DD`）。  
   - 正文至少包含 **`## 上下文`**、**`## 正文`**。  
5. **复制模板**：[`inbox/_TEMPLATE.md`](inbox/_TEMPLATE.md)；合规样例：[`inbox/_example-good.md`](inbox/_example-good.md)。  
6. **吸收进正式文档后**：把该条 `status` 改为 **`absorbed`**，并在 **`## 吸收说明`**（或正文末）写明写入的**文件路径与章节**；不再适用则标 **`obsolete`**。  
7. **禁止**在仓库中放入真实密钥、令牌、带签名的私有 URL、客户隐私；用占位符或内部流程领取。

### 本地校验与 CI

与合并到 `main` 时的检查一致：

```bash
pip install -r requirements-ci.txt
python3 scripts/validate_inbox_frontmatter.py
```

- **Schema**：[`inbox/schema/frontmatter.schema.json`](inbox/schema/frontmatter.schema.json)  
- **GitHub Actions**：工作流显示名为 **`inbox-frontmatter-check`**；在 **Repository rulesets**（或分支保护）中请将 Required check 设为 PR 上实际绿勾名称，例如 **`inbox-frontmatter-check / validate (pull_request)`**，且勿重复添加同名检查。  
- **不参与条目校验的文件**：`inbox/README.md`、`inbox/AGENT.md`、`inbox/_TEMPLATE.md`。

更细的约定与生命周期表见 [`inbox/README.md`](inbox/README.md)。

## 构建与协作（索引）

- **`docs/`**：已整理的通用知识索引见 [`docs/README.md`](docs/README.md)（分发、支付与商店合规、Play 多语言上架等）。  
- **`inbox/`**：用法见上一节；目录内总说明见 [`inbox/README.md`](inbox/README.md)。  
- **CI**：修改 `inbox/` 或校验脚本时触发 **`inbox-frontmatter-check`**。  
- **Agent 写入**：见 [`inbox/AGENT.md`](inbox/AGENT.md)。