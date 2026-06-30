#!/usr/bin/env python3
"""
GEMS Pipeline Dry Run v7.1 — KHÔNG cần API key.
Mô phỏng 6 bước, dùng fixture có sẵn, render DOCX từ Markdown, compile TikZ.
"""
import os, sys, json, shutil, re, random, hashlib
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track

sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
console = Console()

# === CONFIG ===
BASE_DIR = Path(r"C:\Users\Admin\.antigravity-ide\soạn tài liệu")
ENGINE_DIR = BASE_DIR / "engine"
OUTPUT_DIR = BASE_DIR / "output"
GENERATED_DIR = OUTPUT_DIR / "generated_docs"
sys.path.insert(0, str(ENGINE_DIR))


def step_log(step, msg, status="⚡"):
    """Hiển thị bước pipeline với màu sắc."""
    colors = {"⚡": "cyan", "✓": "green", "⚠": "yellow", "❌": "red"}
    console.print(f"  [{colors.get(status,'white')}] {status} BƯỚC {step}: {msg}[/{colors.get(status,'white')}]")


def load_fixture(lesson_slug: str) -> dict:
    """Load tất cả fixture có sẵn từ thư mục output."""
    lesson_dir = OUTPUT_DIR / lesson_slug
    if not lesson_dir.exists():
        return {}
    
    fixtures = {}
    for f in lesson_dir.glob("*"):
        if f.suffix in (".md", ".json", ".docx", ".pptx", ".png") and f.stat().st_size > 0:
            key = f.stem
            fixtures[key] = str(f)
    
    # Thêm các file từ generated_docs nếu có
    if (GENERATED_DIR / f"{lesson_slug}_phieu_hoc_tap.md").exists():
        fixtures["worksheet_md"] = str(GENERATED_DIR / f"{lesson_slug}_phieu_hoc_tap.md")
    if (GENERATED_DIR / f"{lesson_slug}_huong_dan_slide.md").exists():
        fixtures["slide_guide_md"] = str(GENERATED_DIR / f"{lesson_slug}_huong_dan_slide.md")
    
    return fixtures


def read_file_safe(path: str) -> str:
    """Đọc file, trả về rỗng nếu không có."""
    path = Path(path)
    if path.exists() and path.stat().st_size > 0:
        return path.read_text(encoding="utf-8")
    return ""


def step1_2_pedagogical_analysis(yccd: str, fixtures: dict) -> dict:
    """Bước 1 & 2: Mô phỏng phân tích sư phạm và ma trận."""
    step_log("1 & 2", "Phân tích sư phạm & Thiết lập ma trận (Dry Run)")
    
    # Load từ fixture nếu có
    dacta_path = OUTPUT_DIR / "bai4_nhiet_dung_rieng" / "nhiet_dung_rieng_dac_ta_gems.md"
    if dacta_path.exists():
        content = dacta_path.read_text(encoding="utf-8")
        console.print("[dim]  → Đã load đặc tả GEMS từ file.[/dim]")
        return {"spec": content, "lesson_name": "Bài 4 - Nhiệt dung riêng"}
    
    # Fallback: tạo mock dựa trên YCCĐ
    lines = yccd.strip().split("\n")
    return {
        "spec": f"# PHÂN TÍCH SƯ PHẠM (Dry Run)\n\n## YCCĐ\n{yccd}",
        "lesson_name": lines[0][:50] if lines else "Bài học"
    }


def step3_worksheet(fixtures: dict) -> str:
    """Bước 3: Phiếu học tập."""





















































































































































































































        "[white]Không cần API key • Dùng fixture có sẵn • Mô phỏng 6 bước[/white]",
        border_style="cyan"
    ))
    
    # Đọc YCCĐ
    yccd_path = BASE_DIR / "yccd_bai4.txt"
    if yccd_path.exists():
        yccd = yccd_path.read_text(encoding="utf-8").strip()
        console.print(f"\n[bold]📝 YCCĐ từ file:[/bold] [white]{yccd_path}[/white]")
    else:
        yccd = "Phát biểu được định nghĩa nhiệt dung riêng (c). Viết được hệ thức Q=mcΔT. Mô tả phương án thí nghiệm đo nhiệt dung riêng. Vận dụng Q=mcΔT giải bài tập."
        console.print(f"\n[bold]📝 YCCĐ (mặc định):[/bold]")
    
    for line in yccd.split("\n"):
        console.print(f"  [dim]• {line.strip()}[/dim]")
    
    # Load fixture
    lesson_slug = "bai4_nhiet_dung_rieng"
    fixtures = load_fixture(lesson_slug)
    
    if not fixtures:
        console.print("[yellow]⚠ Không tìm thấy fixture. Dùng generated_docs làm nguồn.[/yellow]")
    
    console.print(f"\n[bold]📊 Pipeline 6 bước:[/bold]\n")
    
    # === BƯỚC 1 & 2 ===
    analysis = step1_2_pedagogical_analysis(yccd, fixtures)
    lesson_name = analysis.get("lesson_name", "Bài 4 - Nhiệt dung riêng")
    
    # === BƯỚC 3 ===
    worksheet = step3_worksheet(fixtures)
    
    # === BƯỚC 4 ===
    homework = step4_homework(fixtures)
    
    # === BƯỚC 5 ===
    step5_tikz_images()
    
    # === BƯỚC 6 ===
    qa_report = step6_quality_check(fixtures)
    
    # === COPY THÀNH PHẨM ===
    copy_to_generated(lesson_slug)
    
    # === SUMMARY ===
    print_summary(lesson_name, yccd)


if __name__ == "__main__":
    main()