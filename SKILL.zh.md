---
name: it-project-docs
title: 信息化项目文档生成
description: 为软件开发项目生成项目文档模板和填充内容
version: 1.0.0
author: Claude
category: documentation
tags: [documentation, project-management, software-development, templates]
---

# 信息化项目文档生成技能

一个用于生成和管理IT软件开发项目文档的技能。该技能为从立项到部署的所有项目阶段提供全面的模板支持。

## 能力

- **项目结构创建**：创建有序的项目文档结构
- **模板生成**：根据项目类型生成文档模板
- **智能内容填充**：交互式模板填充，支持变量替换
- **文档跟踪**：跟踪所有文档的完成状态
- **文档导出**：以多种格式导出文档包
- **模板验证**：验证模板结构和一致性

## 使用方法

### 创建新项目

```bash
python scripts/create_project.py "my-project" --type web-app --tech-stack "React,Node.js,PostgreSQL"
```

### 生成文档模板

```bash
python scripts/generate_template.py "需求规格说明书" --project "data/projects/my-project"
```

### 填充模板变量

```bash
python scripts/fill_template.py "data/projects/my-project/02-需求/需求规格说明书.md"
```

### 列出可用文档

```bash
python scripts/list_documents.py --category requirements
```

### 跟踪文档状态

```bash
python scripts/track_status.py --project "data/projects/my-project" --report
```

### 导出文档包

```bash
python scripts/export_bundle.py --project "data/projects/my-project" --format zip
```

## 项目类型

- `web-app` - Web应用
- `mobile-app` - 移动应用
- `desktop-app` - 桌面应用
- `api-service` - API服务
- `data-platform` - 数据平台

## 文档阶段

1. **立项阶段** - 立项申请书、可行性研究报告、项目章程
2. **需求阶段** - 需求规格说明书(SRS)、业务需求文档(BRD)、用户故事
3. **设计阶段** - 概要设计、详细设计、数据库设计、接口设计
4. **开发阶段** - 技术方案、开发计划、代码规范
5. **测试阶段** - 测试计划、测试用例、测试报告
6. **部署阶段** - 部署手册、用户手册、运维手册、培训材料
7. **管理阶段** - 项目计划、风险管理、周报、总结报告、变更记录

## 配置

所有配置存储在 `data/config/` 目录中：
- `document_catalog.json` - 文档类型定义
- `variable_registry.json` - 模板变量定义
- `project_metadata.json` - 项目元数据模板

## 输出格式

所有文档以Markdown格式生成，包含：
- YAML frontmatter 用于元数据
- 变量占位符便于填充
- 清晰的章节结构
- 写作指导注释
