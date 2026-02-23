#!/usr/bin/env python3
"""
导出文档包脚本
Usage: python export_bundle.py [options]
"""

import argparse
import json
import shutil
import sys
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path


# 添加项目根目录到Python路径
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))


# 默认配置
CONFIG_DIR = project_root / "data" / "config"
EXPORTS_DIR = project_root / "exports"


def load_config(config_file):
    """加载配置文件"""
    config_path = CONFIG_DIR / config_file
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def create_index(project_path, status_data=None):
    """创建文档索引文件"""
    project_dir = Path(project_path)
    project_name = project_dir.name

    # 创建索引内容
    index_content = [
        f"# {project_name} 文档索引",
        "",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 文档目录",
        ""
    ]

    # 收集所有文档
    documents = []

    for phase_dir in sorted(project_dir.iterdir()):
        if not phase_dir.is_dir():
            continue

        for doc_file in sorted(phase_dir.glob("*.md")):
            if doc_file.name == "README.md":
                continue

            rel_path = doc_file.relative_to(project_dir)
            documents.append({
                "path": rel_path,
                "phase": phase_dir.name,
                "name": doc_file.stem
            })

    # 按阶段分组
    phases = {}
    for doc in documents:
        phase = doc["phase"]
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(doc)

    # 写入索引
    for phase_name in sorted(phases.keys()):
        index_content.append(f"### {phase_name}")
        index_content.append("")
        for doc in phases[phase_name]:
            index_content.append(f"- [{doc['name']}]({doc['path']})")
        index_content.append("")

    # 添加状态报告
    if status_data:
        index_content.append("## 完成状态")
        index_content.append("")
        summary = status_data.get("summary", {})
        total = summary.get("total", 0)
        completed = summary.get("completed", 0)

        if total > 0:
            progress = completed / total
            bar_length = 20
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            index_content.append(f"完成进度: `{bar}` {progress*100:.1f}% ({completed}/{total})")
        index_content.append("")

    return "\n".join(index_content)


def export_to_directory(project_path, output_path, include_index):
    """导出到目录"""
    project_dir = Path(project_path)
    output_dir = Path(output_path)

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 收集并复制文件
    for phase_dir in sorted(project_dir.iterdir()):
        if not phase_dir.is_dir():
            continue

        output_phase_dir = output_dir / phase_dir.name
        output_phase_dir.mkdir(exist_ok=True)

        for doc_file in sorted(phase_dir.glob("*.md")):
            shutil.copy2(doc_file, output_phase_dir / doc_file.name)

    # 创建索引
    if include_index:
        index_path = output_dir / "INDEX.md"
        index_content = create_index(project_path)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)

    # 复制项目概览文件
    project_md = project_dir / "project.md"
    if project_md.exists():
        shutil.copy2(project_md, output_dir / "PROJECT.md")

    return output_dir


def export_to_zip(project_path, output_path, include_index):
    """导出到ZIP文件"""
    project_dir = Path(project_path)
    output_file = Path(output_path)

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 创建ZIP文件
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加文档文件
        for phase_dir in sorted(project_dir.iterdir()):
            if not phase_dir.is_dir():
                continue

            for doc_file in sorted(phase_dir.glob("*.md")):
                arcname = str(doc_file.relative_to(project_dir))
                zipf.write(doc_file, arcname)

        # 添加索引
        if include_index:
            index_content = create_index(project_path)
            zipf.writestr("INDEX.md", index_content.encode('utf-8'))

        # 添加项目概览
        project_md = project_dir / "project.md"
        if project_md.exists():
            zipf.write(project_md, "PROJECT.md")

    return output_file


def export_to_tar(project_path, output_path, include_index):
    """导出到TAR文件"""
    project_dir = Path(project_path)
    output_file = Path(output_path)

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 创建TAR文件
    with tarfile.open(output_file, 'w:gz') as tarf:
        # 添加文档文件
        for phase_dir in sorted(project_dir.iterdir()):
            if not phase_dir.is_dir():
                continue

            for doc_file in sorted(phase_dir.glob("*.md")):
                arcname = str(doc_file.relative_to(project_dir))
                tarf.add(doc_file, arcname=arcname)

        # 添加索引
        if include_index:
            index_content = create_index(project_path)
            index_bytes = index_content.encode('utf-8')

            # 创建临时文件
            from io import BytesIO
            import tarfile

            info = tarfile.TarInfo(name="INDEX.md")
            info.size = len(index_bytes)
            info.mtime = datetime.now().timestamp()

            tarf.addfile(info, BytesIO(index_bytes))

        # 添加项目概览
        project_md = project_dir / "project.md"
        if project_md.exists():
            tarf.add(project_md, arcname="PROJECT.md")

    return output_file


def get_status_data(project_path):
    """获取项目状态数据"""
    # 简单实现，实际应该调用track_status的逻辑
    project_dir = Path(project_path)
    if not project_dir.exists():
        return None

    summary = {"total": 0, "completed": 0}

    for phase_dir in sorted(project_dir.iterdir()):
        if not phase_dir.is_dir():
            continue

        for doc_file in phase_dir.glob("*.md"):
            if doc_file.name == "README.md":
                continue
            summary["total"] += 1

    return {"summary": summary}


def main():
    parser = argparse.ArgumentParser(
        description='导出文档包',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python export_bundle.py --project "data/projects/my-project" --format zip
  python export_bundle.py --project "data/projects/my-project" --output "exports/my-docs.zip"
  python export_bundle.py --project "data/projects/my-project" --format directory --include-index
        """
    )

    parser.add_argument('--project', '-p',
                        required=True,
                        help='项目目录路径')
    parser.add_argument('--output', '-o',
                        help='输出文件/目录路径')
    parser.add_argument('--format', '-f',
                        choices=['zip', 'tar', 'directory'],
                        default='zip',
                        help='导出格式 (默认: zip)')
    parser.add_argument('--include-index',
                        action='store_true',
                        help='包含文档索引')
    parser.add_argument('--export-dir',
                        default=str(EXPORTS_DIR),
                        help='导出目录 (默认: exports/)')

    args = parser.parse_args()

    # 验证项目目录
    project_dir = Path(args.project)
    if not project_dir.exists():
        print(f"错误: 项目目录不存在: {project_dir}")
        sys.exit(1)

    # 获取状态数据
    status_data = get_status_data(args.project)

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_name = project_dir.name

        if args.format == 'zip':
            ext = '.zip'
        elif args.format == 'tar':
            ext = '.tar.gz'
        else:
            ext = ''

        output_path = Path(args.export_dir) / f"{project_name}_docs_{timestamp}{ext}"

    # 导出
    try:
        print(f"导出项目: {project_dir.name}")
        print(f"格式: {args.format}")

        if args.format == 'directory':
            result = export_to_directory(args.project, output_path, args.include_index)
            print(f"✓ 已导出到目录: {result}")
        elif args.format == 'zip':
            result = export_to_zip(args.project, output_path, args.include_index)
            print(f"✓ 已导出到ZIP: {result}")
        else:  # tar
            result = export_to_tar(args.project, output_path, args.include_index)
            print(f"✓ 已导出到TAR: {result}")

        # 统计信息
        if status_data:
            summary = status_data["summary"]
            print(f"\n导出统计:")
            print(f"  文档总数: {summary.get('total', 0)}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
