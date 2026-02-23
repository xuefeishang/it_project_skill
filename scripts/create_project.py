#!/usr/bin/env python3
"""
创建新项目的目录结构脚本
Usage: python create_project.py <project_name> [options]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# 添加项目根目录到Python路径
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))


# 默认配置
CONFIG_DIR = project_root / "data" / "config"
PROJECTS_DIR = project_root / "data" / "projects"

# 项目类型定义
PROJECT_TYPES = {
    "web-app": "Web应用",
    "mobile-app": "移动应用",
    "desktop-app": "桌面应用",
    "api-service": "API服务",
    "data-platform": "数据平台"
}

# 阶段定义
PHASES = [
    {"id": "01-initiation", "name": "立项", "dir": "01-立项"},
    {"id": "02-requirements", "name": "需求", "dir": "02-需求"},
    {"id": "03-design", "name": "设计", "dir": "03-设计"},
    {"id": "04-development", "name": "开发", "dir": "04-开发"},
    {"id": "05-testing", "name": "测试", "dir": "05-测试"},
    {"id": "06-deployment", "name": "部署", "dir": "06-部署"},
    {"id": "07-management", "name": "管理", "dir": "07-管理"}
]


def load_config(config_file):
    """加载配置文件"""
    config_path = CONFIG_DIR / config_file
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def create_project_structure(project_name, project_type, tech_stack, output_dir):
    """创建项目目录结构"""
    project_path = Path(output_dir) / project_name

    # 创建项目主目录
    project_path.mkdir(parents=True, exist_ok=True)

    # 创建各阶段目录
    for phase in PHASES:
        phase_dir = project_path / phase["dir"]
        phase_dir.mkdir(exist_ok=True)

        # 创建README文件
        readme_path = phase_dir / "README.md"
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {phase['name']}阶段文档\n\n")
                f.write(f"本目录包含{project_name}项目{phase['name']}阶段的所有文档。\n\n")

    # 创建项目根目录文件
    create_project_files(project_path, project_name, project_type, tech_stack)

    return project_path


def create_project_files(project_path, project_name, project_type, tech_stack):
    """创建项目相关文件"""

    # 创建 project.md
    project_md_path = project_path / "project.md"
    project_md_content = f"""---
title: {project_name} 项目概览
type: {project_type}
version: 1.0.0
created_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# {project_name} 项目概览

## 项目基本信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {project_name} |
| 项目类型 | {PROJECT_TYPES.get(project_type, project_type)} |
| 项目版本 | 1.0.0 |
| 创建日期 | {datetime.now().strftime('%Y-%m-%d')} |

## 技术栈

{tech_stack if tech_stack else '待定'}

## 项目阶段

1. **01-立项** - 立项阶段
2. **02-需求** - 需求阶段
3. **03-设计** - 设计阶段
4. **04-开发** - 开发阶段
5. **05-测试** - 测试阶段
6. **06-部署** - 部署阶段
7. **07-管理** - 管理阶段

## 项目团队

| 角色 | 姓名 |
|------|------|
| 项目经理 |  |
| 技术负责人 |  |
| 产品负责人 |  |
| 开发人员 |  |
| 测试人员 |  |

## 里程碑

| 里程碑 | 计划日期 | 实际日期 | 状态 |
|--------|----------|----------|------|
| 项目启动 |  |  | 待定 |
| 需求完成 |  |  | 待定 |
| 设计完成 |  |  | 待定 |
| 开发完成 |  |  | 待定 |
| 测试完成 |  |  | 待定 |
| 项目上线 |  |  | 待定 |

## 备注

本文档记录项目的基本信息，请根据实际情况更新。
"""

    with open(project_md_path, 'w', encoding='utf-8') as f:
        f.write(project_md_content)

    # 创建 status.md
    status_md_path = project_path / "status.md"
    status_md_content = f"""---
title: {project_name} 文档状态
updated_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# {project_name} 文档状态

## 状态说明

- 🔴 未开始 (not_started) - 文档尚未开始编写
- 🟡 待处理 (pending) - 文档已创建，待填充内容
- 🔵 进行中 (in_progress) - 文档正在编写中
- 🟣 审核中 (review) - 文档已完成，等待审核
- 🟢 已完成 (completed) - 文档已审核通过
- ⚪ 已归档 (archived) - 文档已归档

## 立项阶段 (01-立项)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 立项申请书 | not_started |  |  |  |
| 可行性研究报告 | not_started |  |  |  |
| 项目章程 | not_started |  |  |  |

## 需求阶段 (02-需求)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 需求规格说明书 | not_started |  |  |  |
| 业务需求文档 | not_started |  |  |  |
| 用户故事 | not_started |  |  |  |

## 设计阶段 (03-设计)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 概要设计 | not_started |  |  |  |
| 详细设计 | not_started |  |  |  |
| 数据库设计 | not_started |  |  |  |
| 接口设计 | not_started |  |  |  |

## 开发阶段 (04-开发)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 技术方案 | not_started |  |  |  |
| 开发计划 | not_started |  |  |  |
| 代码规范 | not_started |  |  |  |

## 测试阶段 (05-测试)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 测试计划 | not_started |  |  |  |
| 测试用例 | not_started |  |  |  |
| 测试报告 | not_started |  |  |  |

## 部署阶段 (06-部署)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 部署手册 | not_started |  |  |  |
| 用户手册 | not_started |  |  |  |
| 运维手册 | not_started |  |  |  |
| 培训材料 | not_started |  |  |  |

## 管理阶段 (07-管理)

| 文档 | 状态 | 负责人 | 更新日期 | 备注 |
|------|------|--------|----------|------|
| 项目计划 | not_started |  |  |  |
| 风险管理 | not_started |  |  |  |
| 周报 | not_started |  |  |  |
| 总结报告 | not_started |  |  |  |
| 变更记录 | not_started |  |  |  |

---

**更新于**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    with open(status_md_path, 'w', encoding='utf-8') as f:
        f.write(status_md_content)


def create_project_metadata(project_path, project_name, project_type, tech_stack):
    """创建项目元数据JSON文件"""
    catalog = load_config("document_catalog.json")

    metadata = {
        "project": {
            "name": project_name,
            "type": project_type,
            "tech_stack": tech_stack,
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        "structure": {},
        "documents": {}
    }

    # 添加阶段结构
    for phase in PHASES:
        phase_id = phase["id"]
        phase_name = phase["name"]
        phase_dir = phase["dir"]

        metadata["structure"][phase_id] = {
            "name": phase_name,
            "directory": phase_dir,
            "documents": []
        }

        # 从catalog中获取该阶段的文档
        if catalog and "categories" in catalog:
            for cat_id, cat_info in catalog["categories"].items():
                if cat_id == phase_id.replace("-", "") or phase_id.startswith(cat_id):
                    for doc in cat_info.get("documents", []):
                        doc_info = {
                            "id": doc["id"],
                            "name": doc["name"],
                            "template": doc["template"],
                            "status": "not_started",
                            "created": False
                        }
                        metadata["structure"][phase_id]["documents"].append(doc_info)

    metadata_path = project_path / ".metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='创建新项目的目录结构',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python create_project.py my-web-app --type web-app
  python create_project.py api-project --type api-service --tech-stack "Node.js,Express,MongoDB"
  python create_project.py data-platform --type data-platform --output custom/path
        """
    )

    parser.add_argument('project_name', help='项目名称')
    parser.add_argument('--type', '-t',
                        choices=list(PROJECT_TYPES.keys()),
                        default='web-app',
                        help='项目类型 (默认: web-app)')
    parser.add_argument('--tech-stack', '-s',
                        default='',
                        help='技术栈描述')
    parser.add_argument('--output', '-o',
                        default=str(PROJECTS_DIR),
                        help='输出目录 (默认: data/projects)')
    parser.add_argument('--list-types',
                        action='store_true',
                        help='列出所有项目类型')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='显示详细信息')

    args = parser.parse_args()

    # 列出项目类型
    if args.list_types:
        print("可用项目类型:")
        for type_id, type_name in PROJECT_TYPES.items():
            print(f"  {type_id:15} - {type_name}")
        return

    # 验证项目名称
    if not args.project_name or len(args.project_name.strip()) < 2:
        print("错误: 项目名称至少需要2个字符")
        sys.exit(1)

    # 创建项目
    if args.verbose:
        print(f"创建项目: {args.project_name}")
        print(f"类型: {PROJECT_TYPES.get(args.type, args.type)}")
        print(f"技术栈: {args.tech_stack if args.tech_stack else '未指定'}")
        print(f"输出目录: {args.output}")

    try:
        project_path = create_project_structure(
            args.project_name,
            args.type,
            args.tech_stack,
            args.output
        )

        create_project_metadata(
            project_path,
            args.project_name,
            args.type,
            args.tech_stack
        )

        print(f"\n项目创建成功!")
        print(f"项目路径: {project_path}")
        print("\n项目结构:")
        print(f"  {project_path}/")
        for phase in PHASES:
            print(f"    {phase['dir']}/")

        print(f"\n下一步:")
        print(f"  1. 修改 {project_path}/project.md 填写项目基本信息")
        print(f"  2. 使用 generate_template.py 生成文档模板")
        print(f"  例如: python scripts/generate_template.py \"需求规格说明书\" --project \"{project_path}\"")

    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
