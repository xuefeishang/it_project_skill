# 信息化项目文档工作流程指南

本文档描述了使用本技能进行项目文档管理的标准工作流程。

## 目录

1. [项目启动](#项目启动)
2. [文档生成](#文档生成)
3. [内容填充](#内容填充)
4. [审核与批准](#审核与批准)
5. [状态跟踪](#状态跟踪)
6. [文档导出](#文档导出)
7. [维护与更新](#维护与更新)

## 项目启动

### 1.1 创建项目

使用 `create_project.py` 创建新的项目结构：

```bash
python scripts/create_project.py "my-web-app" \
  --type web-app \
  --tech-stack "React, Node.js, PostgreSQL"
```

**参数说明：**

- `project_name`: 项目名称（必需）
- `--type`: 项目类型（web-app, mobile-app, desktop-app, api-service, data-platform）
- `--tech-stack`: 技术栈描述
- `--output`: 输出目录（默认：data/projects/项目名）

**创建内容：**

- 项目根目录
- 7个阶段目录（立项、需求、设计、开发、测试、部署、管理）
- project.md - 项目概览
- status.md - 文档状态跟踪表
- .metadata.json - 项目元数据

### 1.2 配置项目信息

编辑 `project.md` 填写项目基本信息：

```markdown
## 项目基本信息
- 项目名称
- 项目类型
- 技术栈
- 创建日期

## 项目团队
- 项目经理
- 技术负责人
- 团队成员

## 里程碑
- 定义项目关键里程碑
```

## 文档生成

### 2.1 查看可用文档

使用 `list_documents.py` 查看所有可用文档类型：

```bash
# 列出所有文档
python scripts/list_documents.py

# 按类别过滤
python scripts/list_documents.py --category requirements

# 搜索文档
python scripts/list_documents.py --search "测试"
```

### 2.2 生成文档模板

使用 `generate_template.py` 生成文档模板：

```bash
python scripts/generate_template.py "需求规格说明书" \
  --project "data/projects/my-web-app"
```

**输出：**

- 文档保存在对应的阶段目录
- 模板包含变量占位符 `{variable_name}`
- YAML frontmatter 包含元数据

### 2.3 自定义变量

使用 `--var` 参数预定义变量值：

```bash
python scripts/generate_template.py "测试计划" \
  --project "data/projects/my-web-app" \
  --var author="张三" \
  --var version="2.0"
```

### 2.4 预览模式

使用 `--preview` 预览生成的文档：

```bash
python scripts/generate_template.py "需求规格说明书" \
  --project "data/projects/my-web-app" \
  --preview
```

## 内容填充

### 3.1 交互式填充

使用 `fill_template.py` 交互式填充模板：

```bash
python scripts/fill_template.py \
  "data/projects/my-web-app/02-需求/需求规格说明书.md"
```

**工作流程：**

1. 脚本扫描模板中的变量
2. 查询变量注册表获取变量信息
3. 逐个提示输入变量值
4. 自动填充日期、年份等变量
5. 替换模板中的占位符
6. 写入文件

### 3.2 批量填充

使用 `--batch` 模式自动填充已知变量：

```bash
python scripts/fill_template.py \
  "data/projects/my-web-app/02-需求/需求规格说明书.md" \
  --batch \
  --var project_name="客户管理系统" \
  --var company="XX科技有限公司"
```

### 3.3 批量处理整个项目

使用 `--batch-project` 处理整个项目的所有文档：

```bash
python scripts/fill_template.py "data/projects/my-web-app" --batch-project
```

**优势：**

- 首先询问公共变量（项目名称、公司等）
- 后续文档复用已输入的值
- 减少重复输入

### 3.4 预览填充结果

使用 `--dry-run` 预览而不修改文件：

```bash
python scripts/fill_template.py "template.md" --dry-run
```

## 审核与批准

### 4.1 文档状态

文档状态定义：

| 状态 | 图标 | 说明 |
|------|------|------|
| not_started | 🔴 | 未开始 |
| pending | 🟡 | 待处理 |
| in_progress | 🔵 | 进行中 |
| review | 🟣 | 审核中 |
| completed | 🟢 | 已完成 |
| archived | ⚪ | 已归档 |

### 4.2 提交审核

使用 `track_status.py` 更新文档状态为审核中：

```bash
python scripts/track_status.py \
  --document "data/projects/my-web-app/02-需求/需求规格说明书.md" \
  --status review
```

### 4.3 审核流程

1. **审核中 (review)** - 文档提交给审核人员
2. **审核反馈** - 根据反馈修改文档
3. **批准 (completed)** - 审核通过，文档定稿

### 4.4 批准文档

审核通过后更新状态：

```bash
python scripts/track_status.py \
  --document "data/projects/my-web-app/02-需求/需求规格说明书.md" \
  --status completed
```

## 状态跟踪

### 5.1 生成状态报告

使用 `track_status.py` 生成完整的状态报告：

```bash
python scripts/track_status.py \
  --project "data/projects/my-web-app" \
  --report
```

**输出格式：**

- 表格格式（默认）
- JSON格式：`--format json`
- Markdown格式：`--format markdown`

### 5.2 监控进度

定期运行状态报告以跟踪项目进度：

```bash
# 每周运行一次
python scripts/track_status.py --project "data/projects/my-web-app" --report --format markdown > reports/status_$(date +%Y%m%d).md
```

### 5.3 更新 status.md

状态报告内容可用于更新 `status.md` 文件。

## 文档导出

### 6.1 导出文档包

使用 `export_bundle.py` 导出完整文档包：

```bash
# 导出为ZIP
python scripts/export_bundle.py \
  --project "data/projects/my-web-app" \
  --format zip

# 导出为TAR
python scripts/export_bundle.py \
  --project "data/projects/my-web-app" \
  --format tar

# 导出到目录
python scripts/export_bundle.py \
  --project "data/projects/my-web-app" \
  --format directory
```

### 6.2 包含文档索引

使用 `--include-index` 生成文档索引：

```bash
python scripts/export_bundle.py \
  --project "data/projects/my-web-app" \
  --format zip \
  --include-index
```

### 6.3 自定义输出路径

使用 `--output` 指定输出位置：

```bash
python scripts/export_bundle.py \
  --project "data/projects/my-web-app" \
  --output "exports/customer-system-v1.0.zip"
```

## 维护与更新

### 7.1 模板验证

使用 `validate_template.py` 验证模板结构：

```bash
# 验证单个模板
python scripts/validate_template.py "assets/templates/requirements/需求规格说明书.md"

# 验证所有模板
python scripts/validate_template.py --all

# 验证并自动修复
python scripts/validate_template.py "template.md" --fix
```

### 7.2 变量管理

查看可用变量：

```python
# 查看 variable_registry.json
cat data/config/variable_registry.json
```

添加新变量：

1. 编辑 `data/config/variable_registry.json`
2. 添加变量定义
3. 在模板中使用 `{new_variable}`

### 7.3 更新文档目录

修改文档类型或结构：

1. 编辑 `data/config/document_catalog.json`
2. 更新文档定义
3. 创建对应的模板文件

### 7.4 版本控制

建议将项目文档纳入版本控制：

```bash
# 初始化git仓库
cd data/projects/my-web-app
git init

# 添加文档
git add .

# 提交
git commit -m "初始文档提交"
```

## 最佳实践

### 8.1 文档命名

- 使用统一的命名规范
- 文件名与文档名称保持一致
- 包含版本号（如：需求规格说明书_v1.0.md）

### 8.2 变量使用

- 使用有意义的变量名
- 在 variable_registry.json 中注册所有变量
- 为必填变量提供默认值

### 8.3 状态更新

- 及时更新文档状态
- 定期生成状态报告
- 标记已完成的文档

### 8.4 备份与归档

- 定期导出文档包
- 归档已完成的项目
- 保留历史版本

### 8.5 团队协作

- 使用版本控制系统
- 明确文档负责人
- 建立审核流程

## 常见问题

### Q1: 如何恢复被覆盖的文档？

从导出的文档包或版本控制历史中恢复。

### Q2: 如何批量更新变量？

使用 `--batch` 模式或编辑模板源文件。

### Q3: 如何自定义模板？

1. 复制现有模板
2. 根据需要修改
3. 更新 document_catalog.json

### Q4: 如何处理多语言文档？

为每种语言创建单独的文档，使用变量指定语言。

## 相关资源

- [文档标准](document_standards.md)
- [模板变量参考](template_variables.md)
- [章节写作指南](section_guides.md)
