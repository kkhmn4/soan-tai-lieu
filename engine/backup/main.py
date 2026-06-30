"""
main.py — GEMS Engine Orchestrator (DOCX Pipeline)
===================================================
Replaces the LaTeX/PDF pipeline with python-docx exports.

Workflow:
  1. Phân tích YCCĐ → gems_analyzer
  2. Tạo PHT .md → worksheet_generator
  3. Tạo homework .md → homework_generator
  4. **NEW**: Xuất DOCX → pht_exporter, khbd_exporter, homework_exporter
  5. QA → quality_checker

NOTE: LaTeX/PDF compile step (compile_tikz, pdflatex) has been removed.
      Backup of original code is in engine/backup/.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables
load_dotenv()

console = Console()

# --- DOCX pipeline imports ---
from pht_exporter import export_pht
from khbd_exporter import export_khbd
from homework_exporter import export_homework


def export_docx_pipeline(output_dir: str, lesson_label: str = None):
    """
    Export all markdown files in output_dir/md/ to DOCX in output_dir/ready/.

    Looks for these patterns:
      - *_phieu_hoc_tap.md   → *_phieu_hoc_tap.docx   (PHT)
      - *_ke_hoach_bai_day.md → *_ke_hoach_bai_day.docx (KHBD)
      - *_bai_tap_ve_nha.md  → *_bai_tap_ve_nha.docx   (Homework)
    """
    md_dir = os.path.join(output_dir, "md")
    ready_dir = os.path.join(output_dir, "ready")
    os.makedirs(ready_dir, exist_ok=True)

    results = []

    if not os.path.isdir(md_dir):
        console.print(f"[yellow]Thư mục md/ không tồn tại: {md_dir}[/yellow]")
        return results

    for fname in sorted(os.listdir(md_dir)):
        if not fname.endswith('.md'):
            continue

        src = os.path.join(md_dir, fname)
        base = fname[:-3]  # strip .md

        # --- PHT ---
        if 'phieu_hoc_tap' in fname:
            dest = os.path.join(ready_dir, base + '.docx')
            try:
                export_pht(src, dest, lesson_label)
                console.print(f"  [green]✓ PHT → {dest}[/green]")
                results.append(('PHT', dest, True))
            except Exception as e:
                console.print(f"  [red]✗ PHT export failed: {e}[/red]")
                results.append(('PHT', dest, False))

        # --- KHBD ---
        elif 'ke_hoach_bai_day' in fname:
            dest = os.path.join(ready_dir, base + '.docx')
            try:
                export_khbd(src, dest)
                console.print(f"  [green]✓ KHBD → {dest}[/green]")
                results.append(('KHBD', dest, True))
            except Exception as e:
                console.print(f"  [red]✗ KHBD export failed: {e}[/red]")
                results.append(('KHBD', dest, False))

        # --- Homework ---
        elif 'bai_tap_ve_nha' in fname or 'homework' in fname:
            dest = os.path.join(ready_dir, base + '.docx')
            try:
                export_homework(src, dest)
                console.print(f"  [green]✓ Homework → {dest}[/green]")
                results.append(('HW', dest, True))
            except Exception as e:
                console.print(f"  [red]✗ Homework export failed: {e}[/red]")
                results.append(('HW', dest, False))

    return results


def run_full_pipeline(yccd_path, output_dir, lesson_label=None, skip_ai=False):
    """
    Full GEMS pipeline:
      B1: Phân tích YCCĐ (Gemini) → dac_ta_gems.md
      B2: Tạo nội dung MD (Gemini) → phieu_hoc_tap.md, ke_hoach_bai_day.md, bai_tap_ve_nha.md
      B3: Xuất DOCX (local) → ready/*.docx
    """
    console.print(Panel(
        f"[bold cyan]GEMS PIPELINE — {lesson_label or 'Auto'}[/bold cyan]\n"
        f"YCCĐ: {yccd_path}\n"
        f"Output: {output_dir}\n"
        f"Mode: {'DOCX (no LaTeX)' if skip_ai else 'Full AI + DOCX'}",
        title="GEMS Engine v8.0 — DOCX Pipeline",
        border_style="cyan"
    ))

    os.makedirs(os.path.join(output_dir, "md"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "ready"), exist_ok=True)

    # --- B1 & B2: AI generation (only if not skip) ---
    if not skip_ai:
        try:
            from gems_analyzer import GEMSAnalyzer
            analyzer = GEMSAnalyzer()
            console.print("\n[bold]B1: Phân tích YCCĐ...[/bold]")
            yccd_text = open(yccd_path, 'r', encoding='utf-8').read() if os.path.exists(yccd_path) else yccd_path
            matrix = analyzer.analyze(yccd_text)
            spec_path = os.path.join(output_dir, "md", "dac_ta_gems.md")
            with open(spec_path, 'w', encoding='utf-8') as f:
                if hasattr(matrix, 'to_markdown'):
                    f.write(matrix.to_markdown())
                else:
                    f.write(str(matrix))
            console.print(f"  [green]✓ Spec → {spec_path}[/green]")

            console.print("\n[bold]B2: Tạo nội dung MD...[/bold]")
            from worksheet_generator import WorksheetGenerator
            from homework_generator import HomeworkGenerator

            wg = WorksheetGenerator()
            wg.generate(matrix, output_dir)

            hg = HomeworkGenerator()
            hg.generate(matrix, output_dir)

        except ImportError as e:
            console.print(f"[yellow]AI modules not available ({e}). Skipping B1/B2.[/yellow]")
            console.print("[yellow]Using existing MD files in md/ directory.[/yellow]")
        except Exception as e:
            console.print(f"[red]AI pipeline error: {e}[/red]")

    # --- B3: DOCX export (always runs) ---
    console.print("\n[bold]B3: Xuất DOCX...[/bold]")
    results = export_docx_pipeline(output_dir, lesson_label)

    # --- Summary ---
    ok = sum(1 for _, _, s in results if s)
    total = len(results)
    console.print(Panel(
        f"[bold green]Hoàn thành! {ok}/{total} files xuất thành công.[/bold green]\n" +
        "\n".join(f"  {'✓' if s else '✗'} {t}: {os.path.basename(p)}" for t, p, s in results)
        if results else "Không tìm thấy file MD nào để xuất.",
        title="KẾT QUẢ",
        border_style="green" if ok == total else "yellow"
    ))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="GEMS Engine — DOCX Pipeline (Vật lý 12)"
    )
    parser.add_argument("--yccd", type=str, help="Đường dẫn file YCCĐ hoặc chuỗi trực tiếp")
    parser.add_argument("--output-dir", "-o", type=str, required=True,
                        help="Thư mục output (cần có md/ con thư mục)")
    parser.add_argument("--label", "-l", type=str, default=None,
                        help="Tên bài (VD: 'Bài 4 — Nhiệt dung riêng')")
    parser.add_argument("--docx-only", action="store_true",
                        help="Chỉ xuất DOCX từ MD có sẵn (skip AI generation)")

    args = parser.parse_args()

    if args.docx_only:
        if not os.path.isdir(os.path.join(args.output_dir, "md")):
            console.print(f"[red]Không tìm thấy thư mục {args.output_dir}/md/[/red]")
            sys.exit(1)
        results = export_docx_pipeline(args.output_dir, args.label)
        ok = sum(1 for _, _, s in results if s)
        console.print(f"\n[bold]{ok}/{len(results)} files exported successfully.[/bold]")
    else:
        if not args.yccd:
            console.print("[red]Cần truyền --yccd khi chạy full pipeline.[/red]")
            sys.exit(1)
        run_full_pipeline(args.yccd, args.output_dir, args.label)


if __name__ == "__main__":
    main()
