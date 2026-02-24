---
name: list-docs
description: 列出项目中的文档
---

列出项目中已创建或可用的文档。

## 用法

```
/list-docs --project <project-path> [--category <category>]
```

## 参数

- `--project` - 项目路径
- `--category` - 可选，按类别筛选：requirements, design, development, testing, deployment, management

## 示例

```
/list-docs --project "data/projects/my-project"
/list-docs --project "data/projects/my-project" --category requirements
```

此命令会显示项目的文档清单和完成状态。
