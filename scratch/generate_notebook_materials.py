#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_notebook_materials.py — Central automation script for GEMS v8.0
========================================================================
Automates:
  1. Parsing lesson query and matching with LESSON_MAP
  2. Resolving existing Notebook ID or creating a new one on NotebookLM
  3. Uploading GEMS markdown source files (cleaning duplicate sources if any)
  4. Generating Slide Deck and Infographics with strict Vietnamese rules
  5. Smart Polling every 5 minutes (300 seconds) for Cloud processing
  6. Auto-downloading Slide PPTX, Slide PDF, and Infographic PNG
  7. Restructuring folders and running quality checks
"""

import os
import sys

# Set stdout encoding to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import json
import re
import argparse
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Add engine directory to path to import notebooklm_executor
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "engine"))

from notebooklm_executor import execute_notebooklm_pipeline, run_command_live

console = Console()

LESSON_MAP = {
    "bai1": {"name": "Bài 1 - Cấu trúc của chất", "slug": "bai1_cau_truc_chat", "num": 1},
    "bai2": {"name": "Bài 2 - Sự chuyển thể", "slug": "bai2_su_chuyen_the", "num": 2},
    "bai3": {"name": "Bài 3 - Nội năng, nhiệt lượng", "slug": "bai3_noi_nang_nhiet_luong", "num": 3},
    "bai4": {"name": "Bài 4 - Nhiệt dung riêng", "slug": "bai4_nhiet_dung_rieng", "num": 4},
    "bai5": {"name": "Bài 5 - Nhiệt độ, thang nhiệt độ, nhiệt kế", "slug": "bai5_nhiet_do_nhiet_ke", "num": 5},
    "bai6": {"name": "Bài 6 - Nhiệt nóng chảy riêng", "slug": "bai6_nhiet_nong_chay_rieng", "num": 6},
    "bai7": {"name": "Bài 7 - Nhiệt hóa hơi riêng", "slug": "bai7_nhiet_hoa_hoi_rieng", "num": 7},
}

def clean_no_accent_vietnamese(text: str) -> str:
    """Loại bỏ dấu tiếng Việt để đưa về dạng không dấu chuẩn."""
    unicode_map = {
        'a': 'áàảãạăắằẳẵặâấầẩẫậ',
        'A': 'ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ',
        'd': 'đ',
        'D': 'Đ',
        'e': 'éèẻẽẹêếềểễệ',
        'E': 'ÉÈẺẼẸÊẾỀỂỄỆ',
        'i': 'íìỉĩị',
        'I': 'ÍÌỈĨỊ',
        'o': 'óòỏõọôốồổỗộơớờởỡợ',
        'O': 'ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ',
        'u': 'úùủũụưứừửữự',
        'U': 'ÚÙỦŨỤƯỨỪỬỮỰ',
        'y': 'ýỳỷỹỵ',
        'Y': 'ÝỲỶỸỴ'
    }
    res = text
    for k, v in unicode_map.items():
        for char in v:
            res = res.replace(char, k)
    return res

def find_lesson(query):
    query_clean = clean_no_accent_vietnamese(query.lower().strip())
    # Check by number
    match_num = re.search(r'\d+', query_clean)
    if match_num:
        num = match_num.group(0)
        key = f"bai{num}"
        if key in LESSON_MAP:
            return LESSON_MAP[key]
            
    # Check by name/slug match
    for k, v in LESSON_MAP.items():
        name_no_accent = clean_no_accent_vietnamese(v["name"].lower())
        if query_clean in name_no_accent or query_clean in v["slug"].lower():
            return v
    return None

def main():
    parser = argparse.ArgumentParser(description="GEMS Unified NotebookLM Automation Script")
    parser.add_argument("--lesson", "-l", required=True, help="Tên hoặc số bài học (ví dụ: 'Bài 4' hoặc 'Nhiệt dung riêng')")
    parser.add_argument("--notebook-id", "-n", help="Notebook ID (nếu có, để bỏ qua bước tìm kiếm/tạo mới)")
    parser.add_argument("--force-create", action="store_true", help="Bắt buộc tạo Notebook mới")
    args = parser.parse_args()

    # 1. Match lesson
    lesson = find_lesson(args.lesson)
    if not lesson:
        console.print(f"[red]❌ Không tìm thấy bài học tương ứng với truy vấn: '{args.lesson}'[/red]")
        sys.exit(1)
        
    slug = lesson["slug"]
    title = lesson["name"]
    num = lesson["num"]
    
    console.print(Panel(
        f"[bold cyan]QUY TRÌNH TỰ ĐỘNG HÓA SOẠN HỌC LIỆU NOTEBOOKLM — GEMS v8.0[/bold cyan]\n"
        f"Bài học: [yellow]{title}[/yellow]\n"
        f"Slug: [yellow]{slug}[/yellow]\n"
        f"Thư mục làm việc: [yellow]output/{slug}[/yellow]",
        title="GEMS Pipeline",
        border_style="cyan"
    ))

    # 2. Check source directory
    output_dir = os.path.join(str(BASE_DIR), "output", slug)
    md_dir = os.path.join(output_dir, "md")
    
    if not os.path.isdir(md_dir):
        console.print(f"[red]❌ Thư mục md nguồn không tồn tại: {md_dir}[/red]")
        console.print("[yellow]Vui lòng chạy pipeline sinh học liệu (engine/main.py) trước tiên.[/yellow]")
        sys.exit(1)

    # 3. Check nlm CLI Authentication
    code, stdout, stderr = run_command_live("nlm login --check")
    if code != 0:
        console.print("[red]❌ Chưa đăng nhập nlm CLI. Vui lòng chạy lệnh 'nlm login' trên terminal trước.[/red]")
        sys.exit(1)
    console.print("[green]✓ Đã đăng nhập nlm CLI thành công.[/green]")

    # 4. Resolve Notebook ID
    notebook_id = args.notebook_id
    if not notebook_id and not args.force_create:
        console.print("[cyan]🔍 Đang quét danh sách Notebook hiện có để tìm notebook phù hợp...[/cyan]")
        code, stdout, stderr = run_command_live("nlm list notebooks --json")
        if code == 0:
            try:
                notebooks = json.loads(stdout)
                for nb in notebooks:
                    nb_title_no_accent = clean_no_accent_vietnamese(nb.get("title", "").lower())
                    target_name_no_accent = clean_no_accent_vietnamese(title.lower())
                    # Check if matching "Bai X" and part of lesson name
                    if f"bai {num}" in nb_title_no_accent or (f"bai{num}" in nb_title_no_accent) or (target_name_no_accent in nb_title_no_accent):
                        notebook_id = nb["id"]
                        console.print(f"   [green]✓ Tái sử dụng Notebook hiện có: \"{nb['title']}\" (ID: {notebook_id})[/green]")
                        break
            except Exception as e:
                console.print(f"[yellow]⚠ Không thể phân tích danh sách Notebook: {e}. Sẽ tạo mới.[/yellow]")
        else:
            console.print("[yellow]⚠ Lỗi khi lấy danh sách Notebook. Sẽ tạo mới.[/yellow]")

    if not notebook_id:
        console.print(f"[cyan]➕ Đang tạo Notebook mới: \"GEMS Vat ly 12 - {title}\"...[/cyan]")
        code, stdout, stderr = run_command_live(f'nlm create notebook "GEMS Vat ly 12 - {title}"')
        if code == 0:
            try:
                res = json.loads(stdout)
                notebook_id = res.get("notebook_id")
                console.print(f"   [green]✓ Đã tạo Notebook mới thành công. ID: {notebook_id}[/green]")
            except Exception as e:
                console.print(f"[red]❌ Lỗi khi giải mã ID Notebook mới: {e}[/red]")
                sys.exit(1)
        else:
            console.print(f"[red]❌ Không thể tạo Notebook mới: {stderr or stdout}[/red]")
            sys.exit(1)

    # 5. Upload source files
    console.print("\n[bold]📤 Tải tài liệu nguồn lên NotebookLM...[/bold]")
    # Find matching files
    files_to_upload = []
    core_suffixes = [
        "phieu_hoc_tap.md",
        "ke_hoach_bai_day.md",
        "huong_dan_slide.md",
        "dac_ta_gems.md"
    ]
    
    for fname in os.listdir(md_dir):
        if not fname.endswith(".md"):
            continue
        for suffix in core_suffixes:
            if fname.endswith(suffix):
                files_to_upload.append(os.path.join(md_dir, fname))
                break
                
    if not files_to_upload:
        console.print("[red]❌ Không tìm thấy các file markdown nguồn cốt lõi trong thư mục md/![/red]")
        sys.exit(1)

    # List existing sources to avoid duplication
    code, stdout, stderr = run_command_live(f"nlm list sources {notebook_id} --json")
    existing_sources = []
    if code == 0:
        try:
            existing_sources = json.loads(stdout)
        except Exception:
            pass
            
    existing_titles = {src["title"]: src["id"] for src in existing_sources}

    for fpath in files_to_upload:
        fname = os.path.basename(fpath)
        # Check if already uploaded
        if fname in existing_titles:
            src_id = existing_titles[fname]
            console.print(f"   [yellow]🔄 Đã có nguồn \"{fname}\". Đang tiến hành xóa nguồn cũ (ID: {src_id})...[/yellow]")
            run_command_live(f"nlm delete source {src_id} -y")
            
        console.print(f"   [cyan]Đang upload: {fname}...[/cyan]")
        up_code, up_stdout, up_stderr = run_command_live(f'nlm source add {notebook_id} -f "{fpath}" --wait')
        if up_code == 0:
            console.print(f"     [green]✓ Thành công[/green]")
        else:
            console.print(f"     [red]✗ Thất bại: {up_stderr or up_stdout}[/red]")

    # 6. Execute NotebookLM Pipeline
    console.print("\n[bold]⚙️ Khởi động quy trình sinh Slide & Infographic...[/bold]")
    success = execute_notebooklm_pipeline(output_dir, slug, title, notebook_id)
    
    if not success:
        console.print("[red]❌ Quy trình tự động hóa NotebookLM gặp lỗi trong quá trình thực thi.[/red]")
        sys.exit(1)

    # 7. Restructure Output
    console.print("\n[bold]📂 Đang chuẩn hóa và sắp xếp cây thư mục học liệu...[/bold]")
    restructure_script = os.path.join(str(BASE_DIR), "engine", "restructure_output.py")
    res_code, res_stdout, res_stderr = run_command_live(f'python "{restructure_script}" "{output_dir}"')
    if res_code == 0:
        console.print("[green]✓ Đã hoàn thành sắp xếp thư mục và cập nhật metadata.json.[/green]")
        console.print(res_stdout)
    else:
        console.print(f"[yellow]⚠ Lỗi khi chạy restructure_output: {res_stderr or res_stdout}[/yellow]")

    # 8. Print Directory Structure and Output Locations
    console.print(Panel(
        f"[bold green]🎉 HOÀN THÀNH TOÀN BỘ TIẾN TRÌNH SOẠN HỌC LIỆU CHO BÀI {num}![/bold green]\n\n"
        f"[bold]Cấu trúc thư mục đầu ra cực kỳ rõ ràng, trực quan:[/bold]\n"
        f"output/{slug}/\n"
        f"├── md/             # Các tệp Markdown nguồn đã soạn\n"
        f"│   ├── {slug}_dac_ta_gems.md\n"
        f"│   ├── {slug}_phieu_hoc_tap.md\n"
        f"│   ├── {slug}_huong_dan_slide.md\n"
        f"│   └── {slug}_ke_hoach_bai_day.md\n"
        f"├── notebooklm/     # Tệp Prompt tập trung gửi cho Cloud\n"
        f"│   └── {slug}_notebooklm_prompt.md\n"
        f"├── ready/          # Thành phẩm học liệu sẵn sàng xuất bản\n"
        f"│   ├── {slug}_phieu_hoc_tap.docx        # Phiếu học tập chuẩn in ấn\n"
        f"│   ├── {slug}_ke_hoach_bai_day.docx      # Giáo án chuẩn CV5512\n"
        f"│   ├── {slug}_slide_deck.pptx           # Slide PowerPoint bài giảng\n"
        f"│   ├── {slug}_slide_deck.pdf            # Slide bài giảng dạng PDF\n"
        f"│   └── {slug}_infographic.png           # Infographic hướng dọc tự học\n"
        f"└── metadata.json   # Chỉ mục quản lý tài nguyên của bài học\n\n"
        f"👉 Bạn hãy mở thư mục [yellow]output/{slug}/ready/[/yellow] để kiểm duyệt thành phẩm.",
        title="Summary Report",
        border_style="green"
    ))

if __name__ == "__main__":
    main()
