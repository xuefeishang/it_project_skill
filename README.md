# 信息化项目文档生成 (IT Project Documentation)

一个用于生成和管理IT软件开发项目文档的 Claude Code 插件，提供了从立项到部署全生命周期的文档管理功能。

## 插件结构

```
it-project-docs/
├── .claude-plugin/          # Claude Code 插件目录
│   └── plugin.json          # 插件清单
├── commands/                # Slash 命令
│   ├── create-project.md    # 创建项目
│   ├── generate-template.md # 生成模板
│   ├── fill-template.md     # 填充模板
│   ├── list-docs.md         # 列出文档
│   └── export-docs.md       # 导出文档
├── skills/                  # 技能
│   └── it-project-docs/
│       └── SKILL.md         # 技能文件
├── SKILL.md                 # 英文技能定义
├── SKILL.zh.md              # 中文技能定义
├── INSTALL.md               # 安装指南
├── README.md                # 本文件
│
├── scripts/                 # Python 可执行脚本
│   ├── create_project.py    # 创建项目结构
│   ├── generate_template.py # 生成文档模板
│   ├── fill_template.py     # 智能填充模板
│   ├── list_documents.py    # 列出文档类型
│   ├── track_status.py      # 跟踪文档状态
│   ├── export_bundle.py     # 导出文档包
│   └── validate_template.py # 验证模板结构
│
├── references/              # 参考文档
│   ├── workflow-guide.md    # 工作流程指南
│   ├── document_standards.md # 文档标准
│   ├── template_variables.md # 模板变量参考
│   ├── section_guides.md    # 章节写作指南
│   └── examples/            # 示例文档
│
├── assets/                  # 模板资源
│   └── templates/          # 文档模板
│       ├── initiation/      # 立项阶段
│       ├── requirements/    # 需求阶段
│       ├── design/          # 设计阶段
│       ├── development/     # 开发阶段
│       ├── testing/         # 测试阶段
│       ├── deployment/      # 部署阶段
│       └── management/      # 管理阶段
│
└── data/                    # 数据和项目
    ├── config/              # 配置文件
    │   ├── document_catalog.json
    │   ├── variable_registry.json
    │   └── project_metadata.json
    └── projects/            # 项目目录
```

## 快速开始

### 安装方式

#### 方式一：符号链接（推荐，开发中使用）

```bash
# Windows Git Bash
ln -s /path/to/it-project-docs ~/.claude/plugins/local/it-project-docs
```

#### 方式二：复制到本地插件目录

```bash
cp -r it-project-docs ~/.claude/plugins/local/it-project-docs
```

#### 方式三：从 GitHub 克隆

```bash
git clone https://github.com/xuefeishang/it_project_skill.git ~/.claude/plugins/local/it-project-docs
```

### 加载插件

1. 重启 Claude Code
2. 插件会自动加载

### 2. 创建新项目

在 Claude Code 中使用 `/create-project` 命令：

```
/create-project my-web-app --type web-app --tech-stack "React,Node.js,PostgreSQL"
```

或者使用 Python 脚本：

```bash
python scripts/create_project.py "my-web-app" --type web-app --tech-stack "React,Node.js,PostgreSQL"
```

### 3. 生成文档

#### 使用 Claude Code 命令

```
# 生成需求规格说明书
/generate-template 需求规格说明书 --project "data/projects/my-web-app"

# 填充模板
/fill-template "data/projects/my-web-app/02-需求/需求规格说明书.md"
```

#### 使用 Python 脚本

```bash
# 生成需求规格说明书
python scripts/generate_template.py "需求规格说明书" --project "data/projects/my-web-app"

# 填充模板
python scripts/fill_template.py "data/projects/my-web-app/02-需求/需求规格说明书.md"
```

### 4. 跟踪进度

#### 使用 Claude Code 命令

```
/list-docs --project "data/projects/my-web-app"
```

#### 使用 Python 脚本

```bash
# 查看文档状态
python scripts/track_status.py --project "data/projects/my-web-app" --report
```

### 5. 导出文档包

#### 使用 Claude Code 命令

```
/export-docs --project "data/projects/my-web-app" --format zip
```

#### 使用 Python 脚本

```bash
python scripts/export_bundle.py --project "data/projects/my-web-app" --format zip
```

## 支持的文档类型

### 立项阶段
- 立项申请书
- 可行性研究报告
- 项目章程

### 需求阶段
- 需求规格说明书 (SRS)
- 业务需求文档 (BRD)
- 用户故事

### 设计阶段
- 概要设计
- 详细设计
- 数据库设计
- 接口设计

### 开发阶段
- 技术方案
- 开发计划
- 代码规范

### 测试阶段
- 测试计划
- 测试用例
- 测试报告

### 部署阶段
- 部署手册
- 用户手册
- 运维手册
- 培训材料

### 管理阶段
- 项目计划
- 风险管理
- 周报
- 总结报告
- 变更记录

## 脚本使用说明

### create_project.py

创建新项目的目录结构。

```bash
python scripts/create_project.py <project_name> [options]

选项:
  --type TYPE          项目类型 (web-app, mobile-app, desktop-app, api-service, data-platform)
  --tech-stack STACK    技术栈描述
  --output DIR         输出目录 (默认: data/projects/<project_name>)
  --help               显示帮助信息
```

### generate_template.py

生成文档模板。

```bash
python scripts/generate_template.py <document_name> [options]

选项:
  --project DIR         项目目录
  --output FILE        输出文件路径
  --preview            预览模式（不写入文件）
  --var KEY=VALUE      自定义变量
  --help               显示帮助信息
```

### fill_template.py

智能填充模板变量。

```bash
python scripts/fill_template.py <template_file> [options]

选项:
  --batch              批量模式，自动填充已知变量
  --dry-run            预览填充结果
  --help               显示帮助信息
```

### list_documents.py

列出可用的文档类型。

```bash
python scripts/list_documents.py [options]

选项:
  --category CATEGORY  按类别/阶段过滤
  --search TERM        搜索文档名称
  --format FORMAT      输出格式 (table, json, list)
  --help               显示帮助信息
```

### track_status.py

跟踪文档完成状态。

```bash
python scripts/track_status.py [options]

选项:
  --project DIR        项目目录
  --document DOC       更新单个文档状态
  --status STATUS      设置状态 (pending, in_progress, completed)
  --report             生成状态报告
  --format FORMAT      输出格式 (table, json, markdown)
  --help               显示帮助信息
```

### export_bundle.py

导出文档包。

```bash
python scripts/export_bundle.py [options]

选项:
  --project DIR        项目目录
  --output FILE        输出文件
  --format FORMAT      导出格式 (zip, tar, directory)
  --include-index      包含文档索引
  --help               显示帮助信息
```

### validate_template.py

验证模板结构。

```bash
python scripts/validate_template.py <template_file> [options]

选项:
  --fix                自动修复常见问题
  --verbose            显示详细信息
  --help               显示帮助信息
```

## 配置文件

### document_catalog.json

定义所有文档类型的元数据，包括：
- 文档名称
- 所属阶段
- 模板路径
- 必填变量
- 相关文档

### variable_registry.json

定义模板变量，包括：
- 变量类型
- 是否必填
- 是否自动填充
- 描述说明

### project_metadata.json

项目元数据模板，包括：
- 项目基本信息
- 技术栈信息
- 团队信息
- 时间线信息

## 模板变量

模板使用 `{variable_name}` 语法表示变量占位符。常见变量包括：

- `{project_name}` - 项目名称
- `{company}` - 公司名称
- `{date}` - 当前日期
- `{year}` - 当前年份
- `{author}` - 作者姓名
- `{version}` - 文档版本

更多变量请参考 `references/template_variables.md`。

## 工作流程

1. **创建项目**：使用 `create_project.py` 创建项目结构
2. **生成模板**：使用 `generate_template.py` 生成所需文档模板
3. **填充内容**：使用 `fill_template.py` 填充文档内容
4. **跟踪进度**：使用 `track_status.py` 跟踪文档完成状态
5. **导出文档**：使用 `export_bundle.py` 导出完整文档包

详细工作流程请参考 `references/workflow-guide.md`。

## 文档标准

所有文档遵循统一的文档标准，包括：
- 文档格式规范
- 章节结构规范
- 命名规范
- 版本控制规范

详细标准请参考 `references/document_standards.md`。

## 常见问题

### 如何自定义模板？

1. 在 `assets/templates/` 目录下找到对应阶段的模板目录
2. 复制并修改现有模板
3. 更新 `data/config/document_catalog.json` 中的模板路径

### 如何添加新的文档类型？

1. 创建新的模板文件
2. 在 `data/config/document_catalog.json` 中添加文档定义
3. 在 `data/config/variable_registry.json` 中添加需要的变量

### 如何批量处理多个项目？

每个脚本都支持命令行参数，可以结合shell脚本进行批量处理。

## 贡献指南

欢迎贡献新的模板、改进脚本或修复bug。

## Claude Code 插件特性

### 自动技能激活

IT Project Docs 技能会在以下场景自动激活：
- 询问关于项目文档管理的问题
- 需要创建项目结构时
- 需要生成或填充文档模板时
- 跟踪文档状态时

### Slash 命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `/create-project` | 创建新项目文档结构 | `/create-project my-ecommerce --type web-app` |
| `/generate-template` | 生成文档模板 | `/generate-template 需求规格说明书 --project "data/projects/my-project"` |
| `/fill-template` | 填充模板变量 | `/fill-template "data/projects/my-project/02-需求/需求规格说明书.md"` |
| `/list-docs` | 列出项目文档 | `/list-docs --project "data/projects/my-project"` |
| `/export-docs` | 导出文档包 | `/export-docs --project "data/projects/my-project" --format zip` |

### 插件开发模式

当前项目支持两种使用模式：
1. **插件模式**：通过 Claude Code 的自动发现机制，集成 Slash 命令和自动技能
2. **独立脚本模式**：直接使用 Python 脚本，不依赖 Claude Code 环境

## 贡献指南

欢迎贡献新的模板、改进脚本或修复bug。

## 许可证

MIT License
