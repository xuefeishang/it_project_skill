#!/usr/bin/env python3
"""
生成文档模板脚本
Usage: python generate_template.py <document_name> [options]
"""

import argparse
import json
import os
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
ASSETS_DIR = project_root / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"


def load_config(config_file):
    """加载配置文件"""
    config_path = CONFIG_DIR / config_file
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def load_template(template_path):
    """加载模板文件"""
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def load_project_metadata(project_path):
    """加载项目元数据"""
    metadata_path = Path(project_path) / ".metadata.json"
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def load_project_info(project_path):
    """加载项目信息（从project.md）"""
    project_md_path = Path(project_path) / "project.md"

    # 尝试从.md文件读取
    if project_md_path.exists():
        with open(project_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析frontmatter
        frontmatter = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except:
                    pass

        # 提取项目名称
        project_name = frontmatter.get('title', '').replace(' 项目概览', '')
        if not project_name:
            # 从文件内容中提取
            match = re.search(r'# (.+) 项目概览', content)
            if match:
                project_name = match.group(1)

        return {
            "project_name": project_name or Path(project_path).name,
            "project_type": frontmatter.get('type', 'web-app'),
            "version": frontmatter.get('version', '1.0.0')
        }

    # 回退到目录名
    return {
        "project_name": Path(project_path).name,
        "project_type": "web-app",
        "version": "1.0.0"
    }


def find_document(document_name, catalog):
    """在目录中查找文档"""
    if not catalog or "categories" not in catalog:
        return None, None

    # 按名称精确匹配
    for cat_id, cat_info in catalog["categories"].items():
        for doc in cat_info.get("documents", []):
            if doc["name"] == document_name:
                return doc, cat_info

    # 按ID匹配
    for cat_id, cat_info in catalog["categories"].items():
        for doc in cat_info.get("documents", []):
            if doc["id"] == document_name:
                return doc, cat_info

    # 模糊匹配
    for cat_id, cat_info in catalog["categories"].items():
        for doc in cat_info.get("documents", []):
            if document_name in doc["name"] or doc["name"] in document_name:
                return doc, cat_info

    return None, None


def get_auto_variables():
    """获取自动变量"""
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "year": now.strftime("%Y"),
        "month": now.strftime("%m"),
        "day": now.strftime("%d")
    }


def substitute_variables(content, variables):
    """替换模板中的变量"""
    # 使用正则表达式替换 {variable_name} 格式的变量
    pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'

    def replacer(match):
        var_name = match.group(1)
        if var_name in variables:
            return str(variables[var_name])
        return match.group(0)  # 保持原样

    return re.sub(pattern, replacer, content)


def generate_document(document_name, project_path, output_file, custom_vars, preview=False):
    """生成文档"""

    # 加载配置
    catalog = load_config("document_catalog.json")

    # 查找文档
    doc_info, cat_info = find_document(document_name, catalog)

    if not doc_info:
        print(f"错误: 未找到文档 '{document_name}'")
        print("\n可用的文档:")
        list_documents(catalog)
        return None

    # 构建模板路径
    template_path = project_root / doc_info["template"]

    # 加载模板
    template = load_template(template_path)
    if not template:
        print(f"错误: 模板文件不存在: {template_path}")
        return None

    # 加载项目信息
    project_info = load_project_info(project_path)

    # 构建变量
    variables = {
        # 项目信息
        "project_name": project_info.get("project_name", ""),
        "project_type": project_info.get("project_type", "web-app"),
        "version": project_info.get("version", "1.0.0"),

        # 自动变量
        **get_auto_variables(),

        # 自定义变量
        **custom_vars
    }

    # 替换变量
    content = substitute_variables(template, variables)

    # 确定输出路径
    if output_file:
        output_path = Path(output_file)
    else:
        # 根据文档类别确定输出目录
        if cat_info and "stage" in cat_info:
            stage_dir = cat_info["stage"]
        else:
            stage_dir = "00-其他"

        output_path = Path(project_path) / stage_dir / f"{doc_info['name']}.md"

    # 预览或写入
    if preview:
        print("=" * 80)
        print(f"文档: {doc_info['name']}")
        print(f"输出路径: {output_path}")
        print("=" * 80)
        print(content)
        print("=" * 80)
        return content

    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 文档已生成: {output_path}")

    # 更新元数据
    update_metadata(project_path, doc_info["id"], output_path)

    return output_path


def update_metadata(project_path, doc_id, output_path):
    """更新项目元数据"""
    metadata_path = Path(project_path) / ".metadata.json"

    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # 更新文档状态
        for phase_id, phase_info in metadata.get("structure", {}).items():
            for doc in phase_info.get("documents", []):
                if doc["id"] == doc_id:
                    doc["created"] = True
                    doc["status"] = "pending"
                    doc["path"] = str(output_path)
                    doc["created_at"] = datetime.now().isoformat()

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)


def list_documents(catalog, category=None, search=None):
    """列出可用文档"""
    if not catalog or "categories" not in catalog:
        print("无法加载文档目录")
        return

    if category:
        categories = {k: v for k, v in catalog["categories"].items() if k == category or category in v.get("stage", "")}
    else:
        categories = catalog["categories"]

    print("\n可用文档:")
    print("-" * 60)

    for cat_id, cat_info in categories.items():
        # 搜索过滤
        if search and search.lower() not in cat_info["name"].lower():
            docs_filtered = [d for d in cat_info.get("documents", []) if search.lower() in d["name"].lower()]
            if not docs_filtered:
                continue
            docs = docs_filtered
        else:
            docs = cat_info.get("documents", [])

        if docs:
            print(f"\n[{cat_info['stage']}] {cat_info['name']}")
            for doc in docs:
                required = " [必填]" if doc.get("required") else ""
                print(f"  • {doc['name']}{required}")

    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='生成文档模板',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_template.py "需求规格说明书" --project "data/projects/my-project"
  python generate_template.py srs --project "data/projects/my-project" --var author="张三"
  python generate_template.py --list
  python generate_template.py "测试计划" --project "data/projects/my-project" --preview
        """
    )

    parser.add_argument('document_name',
                        nargs='?',
                        help='文档名称或ID')
    parser.add_argument('--project', '-p',
                        required=False,
                        help='项目目录路径')
    parser.add_argument('--output', '-o',
                        help='输出文件路径')
    parser.add_argument('--preview',
                        action='store_true',
                        help='预览模式（不写入文件）')
    parser.add_argument('--var',
                        action='append',
                        help='自定义变量 (格式: key=value)')
    parser.add_argument('--list', '-l',
                        action='store_true',
                        help='列出所有可用文档')
    parser.add_argument('--category', '-c',
                        help='按类别过滤')
    parser.add_argument('--search', '-s',
                        help='搜索文档')

    args = parser.parse_args()

    # 列出文档
    if args.list or (not args.document_name and not args.project):
        catalog = load_config("document_catalog.json")
        list_documents(catalog, args.category, args.search)
        return

    # 验证参数
    if not args.document_name:
        print("错误: 请指定文档名称，或使用 --list 查看可用文档")
        sys.exit(1)

    if not args.project and not args.output:
        print("错误: 请指定项目目录或输出文件")
        print("提示: 使用 --project 指定项目目录，或 --output 指定输出文件")
        sys.exit(1)

    # 解析自定义变量
    custom_vars = {}
    if args.var:
        for var in args.var:
            if '=' in var:
                key, value = var.split('=', 1)
                custom_vars[key] = value
            else:
                print(f"警告: 忽略无效的变量格式: {var}")

    # 生成文档
    try:
        result = generate_document(
            args.document_name,
            args.project,
            args.output,
            custom_vars,
            args.preview
        )

        if result:
            if args.preview:
                print("\n预览模式: 文件未写入磁盘")
            else:
                print(f"\n下一步: 使用 fill_template.py 填充文档内容")
                print(f"  例如: python scripts/fill_template.py \"{result}\"")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
