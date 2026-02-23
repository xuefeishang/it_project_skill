#!/usr/bin/env python3
"""
列出可用文档类型脚本
Usage: python list_documents.py [options]
"""

import argparse
import json
import sys
from pathlib import Path


# 添加项目根目录到Python路径
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))


# 默认配置
CONFIG_DIR = project_root / "data" / "config"


def load_config(config_file):
    """加载配置文件"""
    config_path = CONFIG_DIR / config_file
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def format_documents_table(catalog, category=None, search=None):
    """格式化为表格输出"""
    if not catalog or "categories" not in catalog:
        print("无法加载文档目录")
        return

    # 过滤类别
    if category:
        categories = {k: v for k, v in catalog["categories"].items()
                     if k == category or category in v.get("stage", "")}
    else:
        categories = catalog["categories"]

    print("\n" + "="*80)
    print("文档类型列表")
    print("="*80)

    total_docs = 0

    for cat_id, cat_info in categories.items():
        docs = cat_info.get("documents", [])

        # 搜索过滤
        if search:
            if search.lower() not in cat_info["name"].lower():
                docs = [d for d in docs if search.lower() in d["name"].lower()]
            if not docs:
                continue

        if docs:
            print(f"\n[{cat_info['stage']}] {cat_info['name']}")
            print("-" * 80)
            print(f"{'ID':<20} {'文档名称':<30} {'必填':<6} {'优先级':<8}")
            print("-" * 80)

            for doc in docs:
                required = "是" if doc.get("required") else "否"
                priority = doc.get("priority", "-")
                print(f"{doc['id']:<20} {doc['name']:<30} {required:<6} {priority:<8}")
                total_docs += 1

    print("\n" + "-" * 80)
    print(f"共 {total_docs} 个文档类型")
    print("="*80)


def format_documents_json(catalog, category=None, search=None):
    """格式化为JSON输出"""
    if not catalog or "categories" not in catalog:
        return {}

    result = {}

    for cat_id, cat_info in catalog["categories"].items():
        # 搜索过滤
        docs = cat_info.get("documents", [])
        if search:
            if search.lower() not in cat_info["name"].lower():
                docs = [d for d in docs if search.lower() in d["name"].lower()]

        if not docs:
            continue

        # 类别过滤
        if category and category not in cat_id and category not in cat_info.get("stage", ""):
            continue

        result[cat_id] = {
            "stage": cat_info["stage"],
            "name": cat_info["name"],
            "documents": docs
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


def format_documents_list(catalog, category=None, search=None):
    """格式化为简单列表输出"""
    if not catalog or "categories" not in catalog:
        print("无法加载文档目录")
        return

    for cat_id, cat_info in catalog["categories"].items():
        docs = cat_info.get("documents", [])

        # 搜索过滤
        if search:
            if search.lower() not in cat_info["name"].lower():
                docs = [d for d in docs if search.lower() in d["name"].lower()]

        # 类别过滤
        if category and category not in cat_id and category not in cat_info.get("stage", ""):
            continue

        if docs:
            print(f"\n{cat_info['stage']}")
            for doc in docs:
                required = "*" if doc.get("required") else ""
                print(f"  {required} {doc['name']}")


def list_categories(catalog):
    """列出所有类别"""
    if not catalog or "categories" not in catalog:
        print("无法加载文档目录")
        return

    print("\n可用类别:")
    print("-" * 40)

    for cat_id, cat_info in catalog["categories"].items():
        doc_count = len(cat_info.get("documents", []))
        print(f"  {cat_id:<20} {cat_info['name']:<15} ({doc_count} 个文档)")

    print("-" * 40)


def main():
    parser = argparse.ArgumentParser(
        description='列出可用文档类型',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python list_documents.py
  python list_documents.py --category requirements
  python list_documents.py --search "测试"
  python list_documents.py --format json
  python list_documents.py --list-categories
        """
    )

    parser.add_argument('--category', '-c',
                        help='按类别/阶段过滤')
    parser.add_argument('--search', '-s',
                        help='搜索文档名称')
    parser.add_argument('--format', '-f',
                        choices=['table', 'json', 'list'],
                        default='table',
                        help='输出格式 (默认: table)')
    parser.add_argument('--list-categories',
                        action='store_true',
                        help='列出所有类别')

    args = parser.parse_args()

    # 加载配置
    catalog = load_config("document_catalog.json")

    # 列出类别
    if args.list_categories:
        list_categories(catalog)
        return

    # 根据格式输出
    if args.format == 'json':
        format_documents_json(catalog, args.category, args.search)
    elif args.format == 'list':
        format_documents_list(catalog, args.category, args.search)
    else:
        format_documents_table(catalog, args.category, args.search)


if __name__ == "__main__":
    main()
