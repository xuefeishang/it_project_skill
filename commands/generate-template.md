---
name: generate-template
description: 生成项目文档模板
---

为指定项目生成文档模板。

## 用法

```
/generate-template <document-name> --project <project-path>
```

## 参数

- `document-name` - 文档名称，例如：需求规格说明书、测试计划、部署手册等
- `--project` - 项目路径，例如："data/projects/my-project"

## 示例

```
/generate-template 需求规格说明书 --project "data/projects/my-project"
```

此命令会生成包含变量占位符的文档模板，方便后续填充内容。
