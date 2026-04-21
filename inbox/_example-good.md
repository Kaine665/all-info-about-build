---
title: "示例：COS 测试桶命名约定（虚构）"
status: draft
created: 2026-04-12
updated: 2026-04-12
owner: "待定"
tags:
  - cos
  - example
related:
  - "README.md"
---

## 上下文

本文件为 **格式样例**（内容虚构），供人类与 Agent 对照 `inbox/README.md` 与 `AGENT.md`；合仓库时一并受 CI 校验。

## 正文

- 测试环境桶名使用前缀 `myapp-test-`，后接区域缩写；**勿**在文档中写真实桶名若涉及未公开资源。
- 子账号权限边界另开条目记录。

## 待决

是否需要在 CI 中同步校验 [`docs/README.md`](../docs/README.md) 等元文档（本期不做）。
