# 给 Agent 的契约（写入 inbox）

人类发现需要记录的信息后，可能委托你写入本目录。下列规则**优先于**你自己的默认格式习惯。

## 输入假设

- 用户可能提供：片段说明、聊天记录摘录、链接、待决列表。你必须整理为清晰的 **`## 上下文`** 与 **`## 正文`**，不得仅粘贴未标注来源的冗长 raw 转储（除非用户明确要求「原文存档」）。
- 若用户粘贴了疑似 **Access Key、Secret Key、Bearer token、带签名的私有 URL、客户隐私**，**不得**写入仓库；改为占位符（如 `REDACTED`）或拒绝写入并请用户脱敏后重试。

## 输出要求

1. **只新增或修改** `inbox/` 下扩展名为 **`.md`** 的文件；编码 **UTF-8**。
2. **文件头** 使用 YAML frontmatter，字段须通过 `inbox/schema/frontmatter.schema.json`（由 CI 校验）：
   - **必填**：`title`（非空字符串）、`status`、`created`（`YYYY-MM-DD`）。
   - **`status`** 只能是：`draft` | `open` | `absorbed` | `obsolete`。新建条目默认 **`draft`**；除非用户明确说「已对齐 / 已写入正式文档」，否则不要标为 `absorbed`。
3. **正文** 必须包含二级标题 **`## 上下文`** 与 **`## 正文`**（与 `inbox/README.md` 一致）。
4. **不要修改** `inbox/README.md`、`inbox/AGENT.md`、`inbox/_TEMPLATE.md` 来绕开校验；新条目应使用新文件名。
5. **文件名**：推荐 `YYYY-MM-DD-<主题短名>.md`；同日多篇可加 `-2` 等后缀。

## 收件箱边界（不做「同主题去重」）

`inbox/` 只作**收件箱**：新信息默认**新建一篇** `YYYY-MM-DD-<主题短名>.md` 即可，**不在此目录**做「同一主题合并到旧文件」或目录级去重；去重、归类、正式结构在迁入 **`docs/`** / **`SPEC.md`** 等正式位置时由人类流程完成。

- **例外**：仅当用户**明确说**「改某条 inbox 文件」或给出具体路径时，才更新已有 `inbox` 文件。

## 自检（提交前）

本地可运行（需 Python 依赖见仓库 `requirements-ci.txt`）：

```bash
pip install -r requirements-ci.txt
python3 scripts/validate_inbox_frontmatter.py
```

与 CI 使用相同校验逻辑；通过后再建议用户提交或代其提交。

## 正式文档关系

`inbox/` 不是规范单一真相源；吸收进根目录 `README.md` / `SPEC.md` / `docs/` 后，将对应条目的 `status` 改为 **`absorbed`**，并在 **`## 吸收说明`** 中写明目标路径与章节。
