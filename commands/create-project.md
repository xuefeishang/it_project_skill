---
name: create-project
description: 创建新的IT项目文档结构
---

创建新的IT项目文档结构。

## 用法

```
/create-project <project-name> --type <type> --tech-stack <stack>
```

## 参数

- `project-name` - 项目名称
- `--type` - 项目类型：web-app, mobile-app, desktop-app, api-service, data-platform
- `--tech-stack` - 技术栈（可选），例如："React,Node.js,PostgreSQL"

## 示例

```
/create-project my-ecommerce --type web-app --tech-stack "React,Node.js,PostgreSQL"
```

此命令会在 `data/projects/<project-name>` 目录下创建完整的项目文档结构，包括立项、需求、设计、开发、测试、部署和管理各阶段的文档目录。
