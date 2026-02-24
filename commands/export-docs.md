---
name: export-docs
description: 导出项目文档包
---

将项目文档导出为压缩包或其他格式。

## 用法

```
/export-docs --project <project-path> --format <format>
```

## 参数

- `--project` - 项目路径
- `--format` - 导出格式：zip, tar, pdf（可选，默认为 zip）

## 示例

```
/export-docs --project "data/projects/my-project" --format zip
```

此命令会生成包含所有项目文档的压缩包，便于共享和归档。
