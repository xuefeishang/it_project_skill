#!/usr/bin/env python3
"""
跟踪文档状态脚本
Usage: python track_status.py [options]
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# 添加项目根目录到Python路径
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))


# 默认配置
CONFIG_DIR = project_root / "data" / "config"

# 状态定义
STATUSES = {
    "not_started": {"label": "未开始", "icon": "🔴", "order": 0},
    "pending": {"label": "待处理", "icon": "🟡", "order": 1},
    "in_progress": {"label": "进行中", "icon": "🔵", "order": 2},
    "review": {"label": "审核中", "icon": "🟣", "order": 3},
    "completed": {"label": "已完成", "icon": "🟢", "order": 4},
    "archived": {"label": "已归档", "icon": "⚪", "order": 5}
}


def load_config(config_file):
    """加载配置文件"""
    config_path = CONFIG_DIR / config_file
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def load_catalog():
    """加载文档目录"""
    return load_config("document_catalog.json")


def parse_frontmatter(content):
    """解析文档的frontmatter"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            try:
                import yaml
                return yaml.safe_load(parts[1]) or {}
            except:
                return {}
    return {}


def get_document_status(file_path):
    """获取文档状态"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = parse_frontmatter(content)
        return frontmatter.get('status', 'not_started')
    except:
        return 'not_started'


def scan_project(project_path):
    """扫描项目目录，收集所有文档状态"""
    project_dir = Path(project_path)
    if not project_dir.exists():
        print(f"错误: 项目目录不存在: {project_path}")
        return None

    catalog = load_catalog()
    if not catalog:
        print("错误: 无法加载文档目录")
        return None

    result = {
        "project_name": project_dir.name,
        "phases": {},
        "summary": {
            "total": 0,
            "not_started": 0,
            "pending": 0,
            "in_progress": 0,
            "review": 0,
            "completed": 0,
            "archived": 0
        }
    }

    # 扫描各阶段目录
    phase_order = []

    for cat_id, cat_info in catalog.get("categories", {}).items():
        phase_name = cat_info.get("stage", cat_id)
        phase_order.append((phase_name, cat_id))

    # 按阶段名称排序
    phase_order.sort()

    for phase_name, cat_id in phase_order:
        phase_dir = project_dir / phase_name
        if not phase_dir.exists():
            continue

        phase_docs = []
        cat_info = catalog["categories"].get(cat_id, {})

        for doc_info in cat_info.get("documents", []):
            doc_file = phase_dir / f"{doc_info['name']}.md"
            status = "not_started"
            updated_at = "-"

            if doc_file.exists():
                status = get_document_status(doc_file)

                # 尝试获取更新时间
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    frontmatter = parse_frontmatter(content)
                    updated_at = frontmatter.get('updated_at', frontmatter.get('date', '-'))
                except:
                    pass

            phase_docs.append({
                "name": doc_info["name"],
                "id": doc_info["id"],
                "status": status,
                "updated_at": updated_at,
                "required": doc_info.get("required", False)
            })

            result["summary"]["total"] += 1
            result["summary"][status] += 1

        if phase_docs:
            result["phases"][phase_name] = phase_docs

    return result


def format_status_table(status_data):
    """格式化为表格输出"""
    if not status_data:
        return

    print("\n" + "="*100)
    print(f"项目: {status_data['project_name']} - 文档状态报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100)

    # 状态图例
    print("\n状态图例:")
    for status, info in STATUSES.items():
        print(f"  {info['icon']} {info['label']} ({status})")

    print("\n" + "-"*100)

    # 按阶段显示
    for phase_name, docs in status_data["phases"].items():
        print(f"\n[{phase_name}]")
        print("-"*100)
        print(f"{'文档名称':<30} {'状态':<15} {'更新时间':<20} {'必填':<6}")
        print("-"*100)

        for doc in docs:
            status_info = STATUSES.get(doc["status"], STATUSES["not_started"])
            print(f"{doc['name']:<30} {status_info['icon']} {status_info['label']:<13} {doc['updated_at']:<20} {'是' if doc['required'] else '否':<6}")

    # 汇总
    summary = status_data["summary"]
    print("\n" + "="*100)
    print("汇总:")
    print(f"  总文档数: {summary['total']}")
    for status, info in STATUSES.items():
        count = summary[status]
        if count > 0:
            percentage = (count / summary['total'] * 100) if summary['total'] > 0 else 0
            print(f"  {info['icon']} {info['label']}: {count} ({percentage:.1f}%)")
    print("="*100)

    # 进度条
    completed = summary["completed"]
    total = summary["total"]
    if total > 0:
        progress = completed / total
        bar_length = 40
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\n完成进度: [{bar}] {progress*100:.1f}% ({completed}/{total})")


def format_status_json(status_data):
    """格式化为JSON输出"""
    print(json.dumps(status_data, ensure_ascii=False, indent=2))


def format_status_markdown(status_data):
    """格式化为Markdown输出"""
    if not status_data:
        return

    output = []
    output.append(f"# {status_data['project_name']} 文档状态报告")
    output.append("")
    output.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")

    # 状态图例
    output.append("## 状态说明")
    output.append("")
    for status, info in STATUSES.items():
        output.append(f"- {info['icon']} **{info['label']}** - {status}")
    output.append("")

    # 按阶段显示
    for phase_name, docs in status_data["phases"].items():
        output.append(f"## {phase_name}")
        output.append("")
        output.append("| 文档名称 | 状态 | 更新时间 | 必填 |")
        output.append("|----------|------|----------|------|")

        for doc in docs:
            status_info = STATUSES.get(doc["status"], STATUSES["not_started"])
            required = "是" if doc["required"] else "否"
            output.append(f"| {doc['name']} | {status_info['icon']} {status_info['label']} | {doc['updated_at']} | {required} |")
        output.append("")

    # 汇总
    summary = status_data["summary"]
    output.append("## 汇总")
    output.append("")
    output.append(f"- **总文档数**: {summary['total']}")
    for status, info in STATUSES.items():
        count = summary[status]
        if count > 0:
            output.append(f"- {info['icon']} **{info['label']}**: {count}")
    output.append("")

    # 进度条
    completed = summary["completed"]
    total = summary["total"]
    if total > 0:
        progress = completed / total
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        output.append(f"## 完成进度")
        output.append("")
        output.append(f"`{bar}` {progress*100:.1f}% ({completed}/{total})")
        output.append("")

    print("\n".join(output))


def update_document_status(file_path, new_status):
    """更新文档状态"""
    status_values = list(STATUSES.keys())

    if new_status not in status_values:
        print(f"错误: 无效的状态 '{new_status}'")
        print(f"可用状态: {', '.join(status_values)}")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析frontmatter
        frontmatter = parse_frontmatter(content)

        # 更新状态
        frontmatter['status'] = new_status
        frontmatter['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 重建文档
        if content.startswith('---'):
            parts = content.split('---', 2)
            try:
                import yaml
                new_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
                new_content = f"---{new_frontmatter}---{parts[2]}"
            except:
                # 简单替换
                new_content = content
        else:
            # 添加frontmatter
            import yaml
            new_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{new_frontmatter}---\n{content}"

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ 已更新文档状态: {file_path}")
        print(f"  新状态: {STATUSES[new_status]['label']} ({new_status})")
        return True

    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='跟踪文档状态',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python track_status.py --project "data/projects/my-project" --report
  python track_status.py --document "data/projects/my-project/02-需求/需求规格说明书.md" --status completed
  python track_status.py --project "data/projects/my-project" --format json
  python track_status.py --list-statuses
        """
    )

    parser.add_argument('--project', '-p',
                        help='项目目录路径')
    parser.add_argument('--document', '-d',
                        help='更新单个文档状态')
    parser.add_argument('--status', '-s',
                        choices=list(STATUSES.keys()),
                        help='设置文档状态')
    parser.add_argument('--report', '-r',
                        action='store_true',
                        help='生成状态报告')
    parser.add_argument('--format', '-f',
                        choices=['table', 'json', 'markdown'],
                        default='table',
                        help='输出格式 (默认: table)')
    parser.add_argument('--list-statuses',
                        action='store_true',
                        help='列出所有可用状态')

    args = parser.parse_args()

    # 列出状态
    if args.list_statuses:
        print("\n可用状态:")
        print("-" * 40)
        for status, info in STATUSES.items():
            print(f"  {status:<15} {info['icon']} {info['label']}")
        print("-" * 40)
        return

    # 更新单个文档状态
    if args.document:
        if not args.status:
            print("错误: 使用 --document 时必须指定 --status")
            sys.exit(1)

        doc_path = Path(args.document)
        if not doc_path.exists():
            print(f"错误: 文档不存在: {doc_path}")
            sys.exit(1)

        update_document_status(doc_path, args.status)
        return

    # 生成报告
    if args.project:
        status_data = scan_project(args.project)

        if not status_data:
            sys.exit(1)

        if args.format == 'json':
            format_status_json(status_data)
        elif args.format == 'markdown':
            format_status_markdown(status_data)
        else:
            format_status_table(status_data)
        return

    # 默认：需要指定项目或文档
    print("错误: 请指定 --project 生成报告或 --document 更新单个文档")
    print("使用 --help 查看帮助信息")
    sys.exit(1)


if __name__ == "__main__":
    main()
