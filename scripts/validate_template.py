#!/usr/bin/env python3
"""
验证模板结构脚本
Usage: python validate_template.py <template_file> [options]
"""

import argparse
import json
import re
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


def parse_frontmatter(content):
    """解析文档的frontmatter"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            try:
                import yaml
                return yaml.safe_load(parts[1]) or {}
            except:
                pass
    return {}


def extract_variables(content):
    """从模板中提取变量"""
    # 匹配 {variable_name} 格式的变量
    pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
    variables = re.findall(pattern, content)
    return list(set(variables))


def validate_template_structure(template_path, verbose=False):
    """验证模板结构"""
    issues = []
    warnings = []

    if not template_path.exists():
        issues.append(f"文件不存在: {template_path}")
        return issues, warnings

    # 读取文件
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        issues.append(f"无法读取文件: {e}")
        return issues, warnings

    # 检查1: 文件是否为空
    if not content.strip():
        issues.append("文件为空")

    # 检查2: 是否有frontmatter
    frontmatter = parse_frontmatter(content)
    if not content.startswith('---'):
        warnings.append("缺少YAML frontmatter")
    else:
        # 检查frontmatter必需字段
        required_fields = ['title', 'project']
        for field in required_fields:
            if field not in frontmatter:
                warnings.append(f"frontmatter缺少字段: {field}")

    # 检查3: 变量格式
    variables = extract_variables(content)
    if verbose and variables:
        print(f"  发现变量: {', '.join(variables)}")

    # 检查变量格式是否正确
    invalid_vars = []
    for var in variables:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var):
            invalid_vars.append(var)

    if invalid_vars:
        issues.append(f"无效的变量名: {', '.join(invalid_vars)}")

    # 检查4: 变量是否在注册表中
    var_registry = load_config("variable_registry.json")
    if var_registry:
        unregistered = []
        for var in variables:
            found = False
            for cat_info in var_registry.get("categories", {}).values():
                if var in cat_info.get("variables", {}):
                    found = True
                    break
                # 检查自动变量
                if var in ["date", "time", "datetime", "year", "month", "day"]:
                    found = True
                    break

            if not found and not var.startswith("_"):  # 忽略私有变量
                unregistered.append(var)

        if unregistered:
            warnings.append(f"未在注册表中的变量: {', '.join(unregistered)}")

    # 检查5: 文件编码
    try:
        content.encode('utf-8').decode('utf-8')
    except:
        issues.append("文件编码问题 (非UTF-8)")

    # 检查6: 章节结构
    headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
    if not headings:
        warnings.append("未找到章节标题")

    # 检查标题层级
    for level, title in headings:
        if len(level) == 1 and title != "文档标题":
            # 一级标题通常只有一个
            if [t for l, t in headings if l == level].index(title) > 0:
                warnings.append(f"建议只有一个一级标题: {title}")

    return issues, warnings


def validate_consistency(template_path, var_registry):
    """验证模板变量一致性"""
    issues = []
    warnings = []

    # 读取文件
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    variables = extract_variables(content)

    # 检查变量使用
    if var_registry:
        for var in variables:
            var_info = None
            for cat_info in var_registry.get("categories", {}).values():
                if var in cat_info.get("variables", {}):
                    var_info = cat_info["variables"][var]
                    break

            if var_info:
                # 检查必填变量是否有提示
                if var_info.get("required") and content.find(f"{{{{{var}}}}}") >= 0:
                    pass  # 正常使用

    return issues, warnings


def fix_common_issues(template_path, verbose=False):
    """修复常见问题"""
    fixed = []

    # 读取文件
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 修复1: 添加frontmatter
    if not content.startswith('---'):
        # 尝试提取标题作为frontmatter
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else Path(template_path).stem

        new_frontmatter = f"""---
title: {title}
project: {{project_name}}
version: {{version}}
status: draft
author: {{author}}
date: {{date}}
---

"""

        content = new_frontmatter + content
        fixed.append("添加YAML frontmatter")

    # 修复2: 规范化变量格式
    # 替换可能的错误格式
    content = re.sub(r'\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}', r'{\1}', content)

    if content != original_content:
        # 写回文件
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)

        if verbose:
            print(f"\n已修复问题:")
            for item in fixed:
                print(f"  ✓ {item}")

    return len(fixed) > 0


def main():
    parser = argparse.ArgumentParser(
        description='验证模板结构',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python validate_template.py "assets/templates/requirements/需求规格说明书.md"
  python validate_template.py "template.md" --fix
  python validate_template.py "template.md" --verbose
        """
    )

    parser.add_argument('template_file',
                        nargs='?',
                        help='模板文件路径')
    parser.add_argument('--fix',
                        action='store_true',
                        help='自动修复常见问题')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='显示详细信息')
    parser.add_argument('--all',
                        action='store_true',
                        help='验证所有模板')

    args = parser.parse_args()

    # 加载变量注册表
    var_registry = load_config("variable_registry.json")

    # 验证所有模板
    if args.all:
        templates_dir = project_root / "assets" / "templates"
        if not templates_dir.exists():
            print(f"错误: 模板目录不存在: {templates_dir}")
            sys.exit(1)

        all_issues = 0
        all_warnings = 0

        print("\n验证所有模板文件...")
        print("="*60)

        for template_path in templates_dir.rglob("*.md"):
            rel_path = template_path.relative_to(project_root)
            print(f"\n{rel_path}:")

            issues, warnings = validate_template_structure(template_path, args.verbose)
            cons_issues, cons_warnings = validate_consistency(template_path, var_registry)

            all_issues += len(issues) + len(cons_issues)
            all_warnings += len(warnings) + len(cons_warnings)

            if issues or cons_issues:
                print(f"  错误: {len(issues) + len(cons_issues)}")
                for issue in issues + cons_issues:
                    print(f"    ✗ {issue}")
            else:
                print(f"  ✓ 无错误")

            if warnings or cons_warnings:
                print(f"  警告: {len(warnings) + len(cons_warnings)}")
                for warning in warnings + cons_warnings:
                    print(f"    ⚠ {warning}")

        print("\n" + "="*60)
        print(f"总计: {all_issues} 个错误, {all_warnings} 个警告")
        print("="*60)
        return

    # 验证单个模板
    if not args.template_file:
        print("错误: 请指定模板文件或使用 --all 验证所有模板")
        sys.exit(1)

    template_path = Path(args.template_file)
    if not template_path.exists():
        print(f"错误: 文件不存在: {template_path}")
        sys.exit(1)

    print(f"\n验证模板: {template_path}")
    print("="*60)

    # 自动修复
    if args.fix:
        print("\n尝试修复常见问题...")
        if fix_common_issues(template_path, args.verbose):
            print("\n已应用修复，重新验证...")
        else:
            print("\n无需修复或无法自动修复")

    # 验证结构
    issues, warnings = validate_template_structure(template_path, args.verbose)

    # 验证一致性
    cons_issues, cons_warnings = validate_consistency(template_path, var_registry)

    # 显示结果
    all_issues = issues + cons_issues
    all_warnings = warnings + cons_warnings

    if all_issues:
        print(f"\n发现 {len(all_issues)} 个错误:")
        for issue in all_issues:
            print(f"  ✗ {issue}")

    if all_warnings:
        print(f"\n发现 {len(all_warnings)} 个警告:")
        for warning in all_warnings:
            print(f"  ⚠ {warning}")

    print("\n" + "="*60)

    if not all_issues and not all_warnings:
        print("✓ 模板验证通过")
        sys.exit(0)
    elif not all_issues:
        print("⚠ 模板有警告，但可使用")
        sys.exit(0)
    else:
        print("✗ 模板验证失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
