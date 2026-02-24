---
name: fill-template
description: 填充文档模板变量
---

交互式填充文档模板中的变量占位符。

## 用法

```
/fill-template <document-path>
```

## 参数

- `document-path` - 文档文件路径

## 示例

```
/fill-template "data/projects/my-project/02-需求/需求规格说明书.md"
```

此命令会识别模板中的变量占位符，并引导用户逐步填写每个变量的值，然后生成最终文档。
