# IT Project Docs Plugin - 安装指南

## 插件概述

本插件为软件开发项目提供完整的文档生成和管理能力，覆盖从立项到部署的全生命周期。

## 插件结构

```
it-project-docs/
├── .claude-plugin/
│   └── plugin.json          # 插件清单
├── commands/                # Slash 命令
│   ├── create-project.md
│   ├── generate-template.md
│   ├── fill-template.md
│   ├── list-docs.md
│   └── export-docs.md
├── skills/                  # 技能
│   └── it-project-docs/
│       └── SKILL.md
├── scripts/                 # Python 脚本
│   ├── create_project.py
│   ├── generate_template.py
│   ├── fill_template.py
│   ├── list_documents.py
│   ├── track_status.py
│   ├── export_bundle.py
│   └── validate_template.py
├── data/                    # 数据和配置
│   ├── config/
│   └── projects/
└── references/              # 参考文档
```

## 安装方式

### 方式一：符号链接（推荐，开发中使用）

```bash
# Windows Git Bash
ln -s /e/it-project-docs ~/.claude/plugins/local/it-project-docs
```

### 方式二：复制到本地插件目录

```bash
cp -r /e/it-project-docs ~/.claude/plugins/local/it-project-docs
```

## 加载插件

1. 重启 Claude Code
2. 插件会自动加载

## 可用命令

| 命令 | 描述 |
|------|------|
| `/create-project` | 创建新的IT项目文档结构 |
| `/generate-template` | 生成项目文档模板 |
| `/fill-template` | 填充文档模板变量 |
| `/list-docs` | 列出项目中的文档 |
| `/export-docs` | 导出项目文档包 |

## 使用示例

```bash
# 创建一个 Web 应用项目
/create-project my-ecommerce --type web-app --tech-stack "React,Node.js,PostgreSQL"

# 生成需求规格说明书
/generate-template 需求规格说明书 --project "data/projects/my-ecommerce"

# 填充模板
/fill-template "data/projects/my-ecommerce/02-需求/需求规格说明书.md"

# 列出文档
/list-docs --project "data/projects/my-ecommerce"

# 导出文档包
/export-docs --project "data/projects/my-ecommerce" --format zip
```

## 项目类型支持

- `web-app` - Web 应用
- `mobile-app` - 移动应用
- `desktop-app` - 桌面应用
- `api-service` - API 服务
- `data-platform` - 数据平台

## 文档阶段

1. **立项阶段** - 立项申请书、可行性研究报告、项目章程
2. **需求阶段** - 需求规格说明书(SRS)、业务需求文档(BRD)、用户故事
3. **设计阶段** - 概要设计、详细设计、数据库设计、接口设计
4. **开发阶段** - 技术方案、开发计划、代码规范
5. **测试阶段** - 测试计划、测试用例、测试报告
6. **部署阶段** - 部署手册、用户手册、运维手册、培训材料
7. **管理阶段** - 项目计划、风险管理、周报、总结报告、变更记录

## 版本历史

- **1.0.0** - 初始版本
  - 基础文档结构
  - 模板生成功能
  - 5 个核心命令
