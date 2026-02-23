#!/usr/bin/env python3
"""
智能填充模板脚本
Usage: python fill_template.py <template_file> [options]
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


def load_config(config_file):
    """加载配置文件"""
    config_path = CONFIG_DIR / config_file
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


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


def extract_variables(content):
    """从模板中提取变量"""
    # 匹配 {variable_name} 格式的变量
    pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
    variables = re.findall(pattern, content)
    return list(set(variables))  # 去重


def get_variable_info(var_registry, var_name):
    """获取变量信息"""
    if not var_registry:
        return None

    for cat_id, cat_info in var_registry.get("categories", {}).items():
        if var_name in cat_info.get("variables", {}):
            return cat_info["variables"][var_name]

    return None


def get_variable_value(var_name, var_registry, known_values):
    """获取变量值"""
    # 检查已知值
    if var_name in known_values:
        return known_values[var_name]

    # 检查自动变量
    auto_vars = get_auto_variables()
    if var_name in auto_vars:
        return auto_vars[var_name]

    # 获取变量信息
    var_info = get_variable_info(var_registry, var_name)

    # 获取用户输入
    default_value = var_info.get("default", "") if var_info else ""
    placeholder = var_info.get("placeholder", "") if var_info else ""
    description = var_info.get("description", var_name) if var_info else var_name

    if default_value:
        prompt = f"{description} [{default_value}]: "
    else:
        prompt = f"{description}: "

    value = input(prompt).strip()

    return value if value else default_value


def fill_template(template_file, known_values=None, dry_run=False, interactive=True):
    """填充模板"""

    # 读取模板
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取变量
    variables = extract_variables(content)

    if not variables:
        print("未找到需要填充的变量")
        return content

    # 加载变量注册表
    var_registry = load_config("variable_registry.json")

    # 获取自动变量
    auto_vars = get_auto_variables()

    # 合并已知值
    if known_values is None:
        known_values = {}

    # 填充变量
    filled_values = {}
    for var_name in variables:
        # 跳过自动变量
        if var_name in auto_vars:
            filled_values[var_name] = auto_vars[var_name]
            continue

        # 已有值
        if var_name in known_values:
            filled_values[var_name] = known_values[var_name]
            continue

        # 交互式输入
        if interactive:
            value = get_variable_value(var_name, var_registry, filled_values)
        else:
            value = ""

        filled_values[var_name] = value

    # 替换变量
    filled_content = content
    for var_name, value in filled_values.items():
        # 使用正则表达式确保精确替换 {var_name}
        pattern = r'\{' + re.escape(var_name) + r'\}'
        filled_content = re.sub(pattern, str(value), filled_content)

    return filled_content, filled_values


def update_frontmatter_status(file_path, status="in_progress"):
    """更新文档的frontmatter状态"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否有frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                # 尝试解析YAML
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except:
                    frontmatter = {}

                # 更新状态
                frontmatter['status'] = status
                frontmatter['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 重建frontmatter
                new_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
                new_content = f"---{new_frontmatter}---{parts[2]}"

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                return True
    except:
        pass

    return False


def fill_batch(project_path):
    """批量填充项目中的所有文档"""
    project_dir = Path(project_path)
    if not project_dir.exists():
        print(f"错误: 项目目录不存在: {project_path}")
        return

    # 加载项目元数据
    metadata_path = project_dir / ".metadata.json"
    known_values = {}

    # 首先询问项目基本信息
    print("\n=== 项目基本信息 ===")
    project_name = input(f"项目名称 [{project_dir.name}]: ").strip() or project_dir.name
    company = input("公司名称: ").strip()
    department = input("部门名称 [信息技术部]: ").strip() or "信息技术部"
    author = input("作者姓名: ").strip()
    version = input("项目版本 [1.0.0]: ").strip() or "1.0.0"

    known_values.update({
        "project_name": project_name,
        "company": company,
        "department": department,
        "author": author,
        "version": version
    })

    # 遍历所有阶段目录
    for phase_dir in sorted(project_dir.iterdir()):
        if not phase_dir.is_dir():
            continue

        # 查找.md文件
        for md_file in phase_dir.glob("*.md"):
            if md_file.name == "README.md":
                continue

            print(f"\n{'='*60}")
            print(f"处理文档: {md_file.relative_to(project_dir)}")
            print('='*60)

            try:
                filled_content, filled_vars = fill_template(
                    md_file,
                    known_values=known_values,
                    dry_run=False,
                    interactive=True
                )

                # 写入文件
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(filled_content)

                print(f"✓ 文档已更新")

                # 更新frontmatter状态
                update_frontmatter_status(md_file, "in_progress")

            except KeyboardInterrupt:
                print("\n\n已取消")
                return
            except Exception as e:
                print(f"错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='智能填充模板变量',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fill_template.py "data/projects/my-project/02-需求/需求规格说明书.md"
  python fill_template.py "template.md" --batch
  python fill_template.py "template.md" --dry-run
  python fill_template.py "data/projects/my-project" --batch-project
        """
    )

    parser.add_argument('template_file',
                        nargs='?',
                        help='模板文件路径或项目目录')
    parser.add_argument('--batch', '-b',
                        action='store_true',
                        help='批量模式，自动填充已知变量')
    parser.add_argument('--batch-project',
                        action='store_true',
                        help='批量填充整个项目')
    parser.add_argument('--dry-run',
                        action='store_true',
                        help='预览填充结果，不写入文件')
    parser.add_argument('--var',
                        action='append',
                        help='预定义变量 (格式: key=value)')
    parser.add_argument('--non-interactive',
                        action='store_true',
                        help='非交互模式，使用默认值')

    args = parser.parse_args()

    # 批量处理整个项目
    if args.batch_project:
        if not args.template_file:
            print("错误: 请指定项目目录")
            sys.exit(1)
        fill_batch(args.template_file)
        return

    # 验证参数
    if not args.template_file:
        print("错误: 请指定模板文件或使用 --batch-project 处理整个项目")
        sys.exit(1)

    template_path = Path(args.template_file)
    if not template_path.exists():
        print(f"错误: 文件不存在: {template_path}")
        sys.exit(1)

    # 解析预定义变量
    known_values = {}
    if args.var:
        for var in args.var:
            if '=' in var:
                key, value = var.split('=', 1)
                known_values[key] = value
            else:
                print(f"警告: 忽略无效的变量格式: {var}")

    try:
        print(f"\n处理文件: {template_path}")
        print(f"发现变量: {', '.join(extract_variables(template_path.read_text(encoding='utf-8')))}")

        filled_content, filled_values = fill_template(
            template_path,
            known_values=known_values,
            dry_run=args.dry_run,
            interactive=not args.non_interactive
        )

        if args.dry_run:
            print("\n" + "="*60)
            print("预览结果:")
            print("="*60)
            print(filled_content)
            print("="*60)
            print("\n预览模式: 文件未写入磁盘")
        else:
            # 写入文件
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(filled_content)

            print(f"\n✓ 文件已更新: {template_path}")

            # 更新frontmatter状态
            update_frontmatter_status(template_path, "in_progress")

    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
