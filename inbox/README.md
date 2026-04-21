# inbox（未整理信息信箱）

本目录用于**临时存放**与构建、分发、测试、环境相关的原始笔记、会议结论草稿、待决问题清单等。内容在整理并写入根目录 `README.md`、`SPEC.md` 或团队**外部知识库**前，先落在此处，避免散落在 issue 或个人笔记里。本仓库的 **`docs/` 目录仅用于维护 all-info-about-build 自身的说明**（见 [`docs/README.md`](../docs/README.md)），**不**作为收集体知识的正式落点。

**本信箱里存放的主要是文档**：以 Markdown 文件为主，结构见下文「文档结构」。

- **人类说明**：本文件。  
- **Agent 写入契约**：[`AGENT.md`](./AGENT.md)。  
- **Frontmatter 机器校验**：[`schema/frontmatter.schema.json`](./schema/frontmatter.schema.json)；合并前由 GitHub Actions 运行 [`scripts/validate_inbox_frontmatter.py`](../scripts/validate_inbox_frontmatter.py)（见仓库根目录 `requirements-ci.txt`）。  
- **格式样例**：[`_example-good.md`](./_example-good.md)。

---

## 文档格式（必须）

- **只支持 Markdown**：`inbox/` 内仅使用扩展名为 `.md` 的文件承载条目；不将本目录作为图片、PDF、二进制附件的存放处（若需配图，用外链或正式文档仓库策略另行约定）。
- **编码**：UTF-8。
- **元数据**：每条文档**必须**在文件最开头包含 YAML frontmatter（见下节「必要结构」）。

---

## 文档结构

### 必要结构（必须）

1. **YAML frontmatter**（`---` 与 `---` 之间），且至少包含：
   - `title`：短标题，与正文一级标题语义一致即可。  
   - `status`：`draft` | `open` | `absorbed` | `obsolete`（含义见「生命周期」）。  
   - `created`：创建日期，格式 `YYYY-MM-DD`。

2. **正文**（frontmatter 之后），且至少包含两个二级标题区块：
   - `## 上下文`：用一两句话说明**为何**现在写这条（背景、触发事件、要解决的问题）。  
   - `## 正文`：实质内容（事实、选项、结论草稿、清单等均可）；避免仅有标题无正文。

### 推荐结构（可选，但利于对齐与吸收）

- **Frontmatter 扩展字段**：`updated`、`owner`、`tags`、`sources`、`related`（将吸收到的正式文档路径等）。  
- **正文可选小节**（按需加二级标题）：
  - `## 选项或事实`：并列信息。  
  - `## 推荐`：若有倾向方案，写清推荐项与简要依据。  
  - `## 待决`：需谁拍板、依赖条件。  
  - `## 吸收说明`：`status` 为 `absorbed` 时写明已写入的**文件路径与章节**，便于追溯。

---

## 其它契约（必须）

1. **不放密钥与真实凭证**  
   禁止提交 Access Key、Secret Key、会话令牌、私有 URL 带签名参数、客户真实数据。可写「占位符名」或「从何处领取（内部链接用文字描述，不放可点击含秘文）」。

2. **每条记录自洽、可检索**  
   单文件尽量只谈一个主题；文件名见下文「文件命名」。避免只有碎片词、无 `正文` 信息量。

3. **与正式文档的关系**  
   inbox 不是规范来源；**以仓库根目录的正式文档为准**（及团队约定的外部知识库）。inbox 与正式文档冲突时，以正式文档为准，并应修正 inbox 或标记 `obsolete`。勿将「收集体」的正文默认迁入本仓库的 `docs/`（该目录含义见 [`docs/README.md`](../docs/README.md)）。

---

## 生命周期（`status`）

| 值 | 含义 |
|----|------|
| `draft` | 刚写入，尚未评审。 |
| `open` | 仍有效，待决或待跟踪。 |
| `absorbed` | 要点已写入 SPEC/README 等；正文或「吸收说明」中注明目标位置。 |
| `obsolete` | 被替代或不再适用；正文简短说明原因。 |

---

## 文件命名

推荐：

```text
YYYY-MM-DD-<主题短名>.md
```

示例：`2026-04-12-cos-test-bucket.md`。同一天多文件时在短名后加后缀：`-2`、`-adb-install`。

---

## 模板

复制 `_TEMPLATE.md` 新建文件，填好**必要** frontmatter 与 `上下文` / `正文` 后再按需补充推荐小节。

---

## 本地校验（与 CI 相同）

```bash
pip install -r requirements-ci.txt
python3 scripts/validate_inbox_frontmatter.py
```

`README.md`、`AGENT.md`、`_TEMPLATE.md` 不参与条目校验；其余 `inbox/**/*.md` 均须符合 schema 且包含 `## 上下文` 与 `## 正文`。

### 在 GitHub 上把 CI 变成「合并前必须过」

1. 打开仓库 **Settings** → **Branches** → **Branch protection rules**，编辑（或新增）针对 `main` 的规则。  
2. 勾选 **Require status checks to pass before merging**。  
3. 在检查列表中勾选 **`inbox-frontmatter-check / validate (pull_request)`**（与 PR 页 **Checks** 里绿勾名称一致）。  
   - 若曾添加过旧名 **`inbox validate / …`**，请从规则中**移除**，避免与同名「幽灵」检查冲突。  
4. 保存后：PR 在未通过该校验前无法合并（即此前所说的「硬约束」依赖此设置）。
