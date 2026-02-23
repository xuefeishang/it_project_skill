# 模板变量参考

本文档列出了所有可在文档模板中使用的变量及其说明。

## 目录

1. [项目信息变量](#项目信息变量)
2. [组织信息变量](#组织信息变量)
3. [人员信息变量](#人员信息变量)
4. [日期时间变量](#日期时间变量)
5. [内容变量](#内容变量)
6. [技术相关变量](#技术相关变量)
7. [风险管理变量](#风险管理变量)
8. [文档元数据变量](#文档元数据变量)
9. [阶段特定变量](#阶段特定变量)
10. [自动填充规则](#自动填充规则)

## 项目信息变量

| 变量名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| `{project_name}` | string | 是 | 无 | 项目名称 | 客户管理系统 |
| `{project_code}` | string | 否 | 无 | 项目编号 | PRJ-2024-001 |
| `{project_type}` | string | 否 | web-app | 项目类型 | web-app |
| `{tech_stack}` | string | 否 | 无 | 技术栈 | React, Node.js, PostgreSQL |
| `{version}` | string | 否 | 1.0.0 | 项目/文档版本 | 1.0.0 |

### 使用示例

```markdown
# {project_name} 需求规格说明书

项目类型: {project_type}
技术栈: {tech_stack}
文档版本: {version}
```

## 组织信息变量

| 变量名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| `{company}` | string | 是 | 无 | 公司名称 | XX科技有限公司 |
| `{department}` | string | 否 | 信息技术部 | 部门名称 | 信息技术部 |
| `{sponsor}` | string | 否 | 无 | 项目发起人 | 张三 |
| `{manager}` | string | 否 | 无 | 项目经理 | 李四 |
| `{team}` | string | 否 | 无 | 团队成员 | 王五, 赵六, 孙七 |

### 使用示例

```markdown
## 项目组织

**公司**: {company}
**部门**: {department}
**项目经理**: {manager}
**团队成员**: {team}
```

## 人员信息变量

| 变量名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| `{author}` | string | 否 | 无 | 文档作者 | 张三 |
| `{reviewer}` | string | 否 | 无 | 审核人员 | 李四 |
| `{approver}` | string | 否 | 无 | 批准人员 | 王五 |

### 使用示例

```markdown
**作者**: {author}
**审核**: {reviewer}
**批准**: {approver}
```

## 日期时间变量

| 变量名 | 类型 | 必填 | 自动 | 格式 | 说明 | 示例 |
|--------|------|------|------|------|------|------|
| `{date}` | string | 否 | 是 | YYYY-MM-DD | 当前日期 | 2024-01-15 |
| `{time}` | string | 否 | 是 | HH:MM:SS | 当前时间 | 14:30:00 |
| `{datetime}` | string | 否 | 是 | YYYY-MM-DD HH:MM:SS | 当前日期时间 | 2024-01-15 14:30:00 |
| `{year}` | string | 否 | 是 | YYYY | 当前年份 | 2024 |
| `{month}` | string | 否 | 是 | MM | 当前月份 | 01 |
| `{day}` | string | 否 | 是 | DD | 当前日期 | 15 |
| `{start_date}` | string | 否 | 否 | YYYY-MM-DD | 项目开始日期 | 2024-01-01 |
| `{end_date}` | string | 否 | 否 | YYYY-MM-DD | 项目结束日期 | 2024-12-31 |
| `{duration}` | string | 否 | 否 | 自定义 | 项目周期 | 12个月 |

### 使用示例

```markdown
**创建日期**: {date}
**最后更新**: {datetime}

项目时间线:
- 开始日期: {start_date}
- 结束日期: {end_date}
- 项目周期: {duration}
```

## 内容变量

| 变量名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `{background}` | text | 是 | 项目背景 | 公司现有系统存在XX问题，需要开发新系统... |
| `{objectives}` | text | 是 | 项目目标 | 1. 提高工作效率 2. 降低成本 3. 改善用户体验 |
| `{scope}` | text | 是 | 项目范围 | 包含：用户管理、订单管理；不包含：支付功能 |
| `{budget}` | string | 否 | 项目预算 | 500万元 |
| `{timeline}` | string | 否 | 项目时间线 | 2024年1月-2024年12月 |

### 使用示例

```markdown
## 项目背景

{background}

## 项目目标

{objectives}

## 项目范围

{scope}

**预算**: {budget}
**时间线**: {timeline}
```

## 技术相关变量

| 变量名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| `{architecture}` | text | 是 | 无 | 系统架构描述 | 采用微服务架构，前后端分离... |
| `{modules}` | text | 是 | 无 | 功能模块列表 | 用户管理、订单管理、商品管理... |
| `{interfaces}` | text | 是 | 无 | 接口列表 | REST API共50个接口... |
| `{database_type}` | string | 否 | PostgreSQL | 数据库类型 | PostgreSQL |
| `{api_list}` | text | 是 | 无 | API接口列表 | GET /api/users, POST /api/orders... |

### 使用示例

```markdown
## 系统架构

{architecture}

## 功能模块

{modules}

## 接口设计

{interfaces}

**数据库类型**: {database_type}
```

## 风险管理变量

| 变量名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `{risk_assessment}` | text | 是 | 风险评估 | 技术风险：新技术应用；人员风险：核心人员离职... |
| `{risk_identification}` | text | 是 | 风险识别 | 1. 需求变更风险 2. 技术实现风险 3. 进度延期风险 |
| `{mitigation_plan}` | text | 是 | 缓解计划 | 1. 建立变更管理流程 2. 技术预研... |

### 使用示例

```markdown
## 风险评估

{risk_assessment}

## 风险识别

{risk_identification}

## 缓解措施

{mitigation_plan}
```

## 文档元数据变量

| 变量名 | 类型 | 必填 | 自动 | 说明 | 示例 |
|--------|------|------|------|------|------|
| `{doc_id}` | string | 否 | 是 | 文档ID | DOC-001 |
| `{doc_status}` | string | 否 | 否 | 文档状态 | draft |
| `{confidentiality}` | string | 否 | 否 | 保密级别 | internal |

### 使用示例

```markdown
---
doc_id: {doc_id}
doc_status: {doc_status}
confidentiality: {confidentiality}
---
```

## 阶段特定变量

| 变量名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| `{week}` | string | 否 | 无 | 周次 | 第1周 |
| `{milestones}` | text | 是 | 无 | 里程碑列表 | 1. 需求分析完成 2. 设计完成... |
| `{deliverables}` | text | 是 | 无 | 交付物列表 | 1. 需求规格说明书 2. 设计文档... |

### 使用示例

```markdown
## 项目里程碑

{milestones}

## 交付物

{deliverables}

**报告周期**: {week}
```

## 自动填充规则

以下变量会自动填充，无需手动输入：

### 日期时间变量

```python
# 当前日期
{date} -> 2024-01-15

# 当前时间
{time} -> 14:30:00

# 当前日期时间
{datetime} -> 2024-01-15 14:30:00

# 当前年份
{year} -> 2024

# 当前月份
{month} -> 01

# 当前日期
{day} -> 15
```

### 文档ID

```python
{doc_id} -> DOC-uuid-generated-id
```

## 变量注册

### 添加新变量

1. 编辑 `data/config/variable_registry.json`
2. 在对应类别下添加变量定义
3. 在模板中使用新变量

### 变量定义格式

```json
{
  "variable_name": {
    "type": "string",
    "required": true,
    "default": "",
    "description": "变量描述",
    "example": "示例值",
    "placeholder": "输入提示"
  }
}
```

### 变量类型

| 类型 | 说明 | 示例 |
|------|------|------|
| string | 字符串 | 项目名称 |
| text | 多行文本 | 项目背景 |
| number | 数字 | 预算金额 |
| date | 日期 | 2024-01-15 |
| boolean | 布尔值 | true/false |
| array | 数组 | [项1, 项2] |

## 使用技巧

### 1. 变量复用

```markdown
<!-- 定义一次，多次使用 -->
项目名称: {project_name}
文档: {project_name}需求规格说明书
```

### 2. 默认值

```markdown
<!-- 使用默认值 -->
版本: {version}  <!-- 默认 1.0.0 -->
```

### 3. 可选变量

```markdown
<!-- 可选变量使用占位符 -->
部门: {department|信息技术部}
```

### 4. 变量组合

```markdown
<!-- 组合使用变量 -->
文档标题: {project_name} {document_type} v{version}
```

## 常见问题

### Q1: 如何处理必填变量没有值的情况？

使用 `fill_template.py` 交互式填充时会提示输入。

### Q2: 如何批量设置变量值？

使用 `--var` 参数：

```bash
python scripts/generate_template.py "需求规格说明书" \
  --var project_name="客户管理系统" \
  --var company="XX科技有限公司"
```

### Q3: 如何添加自定义变量？

1. 在 `variable_registry.json` 中注册变量
2. 在模板中使用 `{variable_name}`

### Q4: 变量名有哪些限制？

- 必须以字母或下划线开头
- 只能包含字母、数字和下划线
- 不区分大小写（推荐使用小写）

## 变量验证

使用 `validate_template.py` 验证变量使用：

```bash
python scripts/validate_template.py template.md
```

验证内容：
- 变量名格式是否正确
- 变量是否已注册
- 必填变量是否有值

## 相关资源

- [document_catalog.json](../data/config/document_catalog.json)
- [variable_registry.json](../data/config/variable_registry.json)
- [文档标准](document_standards.md)
