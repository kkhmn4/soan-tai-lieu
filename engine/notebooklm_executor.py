"""
notebooklm_executor.py — Automate Google NotebookLM CLI (nlm) for Slide & Infographic generation
========================================================================================
Handles:
  1. Generating the focus prompt file at output/hermes/[slug]/notebooklm/[slug]_notebooklm_prompt.md
  2. Executing `nlm` CLI commands to create slides and infographics if notebook_id is provided.
  3. Downloading the generated assets automatically into output/hermes/[slug]/ready/.
"""

import os
import re
import subprocess
import time
import json
from rich.console import Console

console = Console()


def parse_pht_for_prompt(pht_path):
    """
    Phân tích file Phiếu học tập để trích xuất các ĐVKT và chi tiết nhiệm vụ
    nhằm sinh mô tả Infographic chi tiết cho NotebookLM.
    """
    if not pht_path or not os.path.exists(pht_path):
        return []
        
    try:
        with open(pht_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
        
    # Tách theo ĐVKT (pattern: ## 📍 ĐVKT X: Tên)
    dvkt_blocks = re.split(r'##\s*(?:📍\s*)?(?:ĐVKT|Đơn vị Kiến thức)\s*\d+[:\s-]*', content)
    dvkt_list = []
    
    # Block đầu tiên thường là tiêu đề phiếu học tập, bỏ qua
    for block in dvkt_blocks[1:]:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        title = lines[0].strip()
        
        # Tìm nhiệm vụ khám phá
        nhiem_vu = "Khám phá hiện tượng"
        nv_match = re.search(r'Nhiệm vụ\s*\d+[:\s-]*([^\)]+)', block)
        if nv_match:
            nhiem_vu = nv_match.group(1).strip()
        else:
            # Fallback nếu không có nhãn Nhiệm vụ cụ thể
            nv_match_simple = re.search(r'###\s*1\.\s*Khám phá\s*\(([^)]+)\)', block)
            if nv_match_simple:
                nhiem_vu = nv_match_simple.group(1).strip()
            
        # Tìm từ khóa gợi ý điền khuyết
        keywords_match = re.search(r'Gợi ý từ khóa[:\s-]*(.*)', block, re.IGNORECASE)
        keywords = ""
        if keywords_match:
            keywords = keywords_match.group(1).strip()
            
        dvkt_list.append({
            "title": title,
            "nhiem_vu": nhiem_vu,
            "keywords": keywords
        })
    return dvkt_list


def parse_slide_guide_for_prompt(guide_path):
    """
    Phân tích file hướng dẫn slide để trích xuất các thông tin thiết kế đặc thù.
    """
    info = {
        "gv": "Kha Khung Hiệp",
        "truong_phai": "GEMS v8.0",
        "font": "Times New Roman",
        "rules": []
    }
    if not guide_path or not os.path.exists(guide_path):
        return info
        
    try:
        with open(guide_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return info
        
    # Trích xuất Giáo viên
    gv_match = re.search(r'\*?Giáo viên thực hiện:\*?\s*([^\n\r]+)', content)
    if gv_match:
        info["gv"] = gv_match.group(1).strip().replace('*', '')
        
    # Trích xuất Trường phái thiết kế
    tp_match = re.search(r'\*?Trường phái thiết kế:\*?\s*([^\n\r]+)', content)
    if tp_match:
        info["truong_phai"] = tp_match.group(1).strip().replace('*', '')
        
    # Trích xuất Phông chữ chủ đạo
    font_match = re.search(r'\*?Phông chữ chủ đạo:\*?\s*([^\n\r]+)', content)
    if font_match:
        info["font"] = font_match.group(1).strip().replace('*', '')
        
    # Trích xuất các quy tắc bắt buộc
    rules_block = re.search(r'##\s*QUY TẮC THIẾT KẾ BẮT BUỘC(.*?)##', content, re.DOTALL)
    if not rules_block:
        rules_block = re.search(r'##\s*QUY TẮC THIẾT KẾ BẮT BUỘC(.*?)---', content, re.DOTALL)
        
    if rules_block:
        rule_lines = rules_block.group(1).strip().split('\n')
        for rline in rule_lines:
            rline = rline.strip()
            if rline.startswith('-') or rline.startswith('*') or (rline and rline[0].isdigit() and '. ' in rline[:5]):
                cleaned_rule = re.sub(r'^[\-\*\d\.\)\s]+', '', rline).strip()
                if cleaned_rule:
                    info["rules"].append(cleaned_rule)
                
    return info


def generate_notebooklm_prompt(output_dir, lesson_slug, lesson_title):
    """
    Generate the focus prompt files for slide deck and infographics separately for GEMS v8.0.
    Creates three files:
      - [slug]_notebooklm_prompt.md (General/Shared)
      - [slug]_notebooklm_slide_prompt.md (Slide-specific)
      - [slug]_notebooklm_info_prompt.md (Infographic-specific)
    Returns:
      (prompt_path_slide, prompt_path_info, prompt_path)
    """
    notebooklm_dir = os.path.join(output_dir, "notebooklm")
    os.makedirs(notebooklm_dir, exist_ok=True)
    
    prompt_path = os.path.join(notebooklm_dir, f"{lesson_slug}_notebooklm_prompt.md")
    prompt_path_slide = os.path.join(notebooklm_dir, f"{lesson_slug}_notebooklm_slide_prompt.md")
    prompt_path_info = os.path.join(notebooklm_dir, f"{lesson_slug}_notebooklm_info_prompt.md")
    
    # Tìm file PHT để trích xuất thông tin ĐVKT
    import glob
    pht_files = glob.glob(os.path.join(output_dir, "md", "*_phieu_hoc_tap.md"))
    pht_path = pht_files[0] if pht_files else None
    
    # Tìm file Hướng dẫn slide để trích xuất quy chuẩn thiết kế
    guide_files = glob.glob(os.path.join(output_dir, "md", "*_huong_dan_slide.md"))
    guide_path = guide_files[0] if guide_files else None
    
    dvkt_list = parse_pht_for_prompt(pht_path)
    guide_info = parse_slide_guide_for_prompt(guide_path)
    
    # Xây dựng nội dung cho Nhiệm vụ 2 (Infographic)
    infographic_rules = ""
    if dvkt_list:
        infographic_rules += f"Hãy đề xuất thiết kế chi tiết cho bộ {len(dvkt_list)} ảnh Infographic học tập độc lập hướng dọc tương ứng với {len(dvkt_list)} Đơn vị Kiến thức (ĐVKT) của bài học. Các Infographic phải bám sát cấu trúc của Phiếu học tập số 1 và đồng bộ về giao diện (màu chủ đạo Navy `#1E3A5F`, màu bổ trợ Mint `#E8F5E9`, phông chữ {guide_info['font']}).\n\n"
        infographic_rules += "1. **Nguyên tắc \"Đục lỗ trống\" (No Pre-filled Answers):**\n"
        infographic_rules += "   - Tuyệt đối không viết sẵn đáp án hoặc giải thích chi tiết trên ảnh Infographic.\n"
        infographic_rules += "   - Sử dụng các bong bóng thoại trống, bệ đỡ vẽ nét đứt hoặc ô chứa nhãn đi kèm ký hiệu dấu hỏi chấm `?` hoặc số thứ tự `(1)`, `(2)`, `(3)` để học sinh tự điền khuyết bằng bút vào phiếu học tập.\n\n"
        
        for idx, dv in enumerate(dvkt_list, 1):
            infographic_rules += f"{idx+1}. **Infographic {idx}: {dv['title']} (Đồng bộ với ĐVKT {idx} trong PHT)**\n"
            infographic_rules += f"   - **Tiêu đề:** \"{dv['title'].upper()}\" (Font {guide_info['font']}, màu Navy `#1E3A5F`).\n"
            infographic_rules += f"   - **Nội dung & Bố cục:**\n"
            infographic_rules += f"     * Nhánh bên trái/trên (Khám phá): Minh họa trực quan tình huống liên quan đến nhiệm vụ \"{dv['nhiem_vu']}\". Trỏ mũi tên ra ô trống đục lỗ: `[ ? ]`.\n"
            infographic_rules += f"     * Nhánh bên phải/dưới (Trọng tâm): Sơ đồ tóm tắt lý thuyết đục lỗ điền khuyết."
            if dv['keywords']:
                infographic_rules += f" Đục lỗ các từ khóa quan trọng và cung cấp hộp gợi ý ở góc dưới chứa các từ: {dv['keywords']}.\n"
            else:
                infographic_rules += " Đục lỗ các từ khóa định nghĩa quan trọng nhất.\n"
            infographic_rules += "\n"
    else:
        infographic_rules += "1. **Nguyên tắc thiết kế:**\n"
        infographic_rules += f"   - Mỗi Đơn vị Kiến thức (ĐVKT) trong Phiếu học tập tương ứng với 1 Infographic độc lập hướng dọc (Quy tắc: 1 ĐVKT = 1 Infographic Portrait).\n"
        infographic_rules += f"   - Nội dung trên Infographic phải bám sát câu hỏi, sơ đồ điền khuyết và bài tập của Phiếu học tập (`{lesson_slug}_phieu_hoc_tap.md`).\n"
        infographic_rules += f"   - Thiết kế dạng đục lỗ (ví dụ: các ô trống nét đứt `........` hoặc bong bóng thoại trống kèm dấu `?`) để học sinh tự hoàn thành và ghi chú trên lớp.\n"
        infographic_rules += "2. **Yêu cầu giao diện:**\n"
        infographic_rules += f"   - Đồng bộ màu sắc Navy/Mint và font chữ {guide_info['font']} giống bộ slide bài giảng.\n"
        infographic_rules += "   - Xuất bản hình ảnh sắc nét dưới định dạng PNG.\n"

    # Xây dựng các quy tắc thiết kế slide cụ thể trích xuất được
    guide_rules_str = ""
    if guide_info["rules"]:
        guide_rules_str += "\n3. **Các quy tắc thiết kế bắt buộc bổ sung trích xuất trực tiếp từ file hướng dẫn slide:**\n"
        for r in guide_info["rules"]:
            guide_rules_str += f"   - {r}\n"

    # --- 1. SLIDE DECK PROMPT ---
    prompt_slide_content = f"""# NOTEBOOKLM PROMPT TẠO SLIDE BÀI GIẢNG - {lesson_title}
> **HƯỚNG DẪN:** Hãy sao chép toàn bộ nội dung dưới đây và dán trực tiếp vào khung chat của Google NotebookLM sau khi đã tải các tệp tài liệu nguồn (`{lesson_slug}_dac_ta_gems.md`, `{lesson_slug}_ke_hoach_bai_day.md`, `{lesson_slug}_phieu_hoc_tap.md`, `{lesson_slug}_huong_dan_slide.md`) làm sources.

---

## NỘI DUNG PROMPT NẠP CHO NOTEBOOKLM (TẠO SLIDE BÀI GIẢNG)

Bạn là một trợ lý thiết kế bài giảng chuyên nghiệp theo hệ thống tiêu chuẩn {guide_info['truong_phai']}. Hãy dựa trên các tài liệu nguồn đã được tải lên để thực hiện nhiệm vụ sau:

### NHIỆM VỤ: XÂY DỰNG CẤU TRÚC CHI TIẾT CỦA BỘ SLIDE BÀI GIẢNG (SLIDE DECK)
1. **Yêu cầu nội dung & Đặt tên Slide dễ hiểu:**
   - Tạo cấu trúc slide chi tiết khớp hoàn toàn 1-1 với tệp `{lesson_slug}_huong_dan_slide.md`.
   - Giữ nguyên các phần phân cấp tiêu đề số hiệu dạng X.Y (ví dụ: Slide 1.0, Slide 1.1, Slide 2.1...).
   - Tách biệt hoàn toàn giữa **Slide Nhiệm vụ (không chứa đáp án)** và **Slide Đáp án (xuất hiện ngay tiếp sau)**.
   - Slide Trang Bìa (Slide Mở đầu) ghi rõ giáo viên thực hiện: **{guide_info['gv']}**.
   - **Tên Slide và nhãn nhiệm vụ phải thuần Việt 100%:**
     - Thay thế hoàn toàn "Assertion Reasoning" -> "Nhận định & Lý do"
     - Thay thế hoàn toàn "Matching Matrix" -> "Ghép nối đa biến"
     - Thay thế hoàn toàn "Bug Buster" -> "Tìm và sửa lỗi vật lý"
     - Thay thế hoàn toàn "Algorithmic Ordering" -> "Sắp xếp tiến trình"
     - Thay thế hoàn toàn "Visual Cloze Test" -> "Điền khuyết trực quan"
   - Highlight đậm và làm nổi bật các từ khóa định nghĩa, công thức toán lý bằng nhãn chú thích rõ ràng.
   - **Yêu cầu bắt buộc:** Toàn bộ tiêu đề, nội dung slide, câu hỏi và đáp án phải hiển thị 100% bằng tiếng Việt chính xác theo tệp nguồn. Tuyệt đối không tự ý dịch sang tiếng Anh.

2. **Yêu cầu Thiết kế và Giao diện (Theme & Design Sync):**
   - **Tông màu chủ đạo:** Sử dụng màu Navy mã HSL `#1E3A5F` làm màu chính cho tiêu đề, đường kẻ phân cách và khung viền.
   - **Tông màu bổ trợ:** Sử dụng màu Mint `#E8F5E9` làm màu nền cho các hộp ghi chú (Note boxes), bảng tóm tắt công thức hoặc ô ghi nhớ quan trọng.
   - **Phông chữ:** Thống nhất sử dụng phông chữ **{guide_info['font']}** cho cả tiêu đề và nội dung văn bản.
   - **Bố cục:** Đảm bảo tỷ lệ khoảng trống (white space) tối thiểu từ 35-40% trên mỗi slide, không nhồi nhét chữ (tối đa 6-8 dòng chữ mỗi slide), nền sáng chữ tối. Chừa khoảng trống hợp lý ở phần bên phải để tích hợp hình ảnh minh họa.
{guide_rules_str}"""

    # --- 2. INFOGRAPHIC PROMPT ---
    prompt_info_content = f"""# NOTEBOOKLM PROMPT TẠO INFOGRAPHIC HỌC TẬP - {lesson_title}
> **HƯỚNG DẪN:** Hãy sao chép toàn bộ nội dung dưới đây và dán trực tiếp vào khung chat của Google NotebookLM sau khi đã tải các tệp tài liệu nguồn (`{lesson_slug}_dac_ta_gems.md`, `{lesson_slug}_ke_hoach_bai_day.md`, `{lesson_slug}_phieu_hoc_tap.md`) làm sources.

---

## NỘI DUNG PROMPT NẠP CHO NOTEBOOKLM (TẠO INFOGRAPHIC ĐỤC LỖ HƯỚNG DỌC)

Bạn là một trợ lý thiết kế đồ họa giáo dục chuyên nghiệp theo hệ thống tiêu chuẩn GEMS v8.0. Hãy dựa trên các tài liệu nguồn đã được tải lên để thực hiện nhiệm vụ sau:

### NHIỆM VỤ: THIẾT KẾ CÁC INFOGRAPHIC ĐỤC LỖ HƯỚNG DỌC (STUDENT WORKSHEET VISUALS)
{infographic_rules}
"""

    # --- 3. GENERAL PROMPT (SHARED) ---
    prompt_content = f"""# NOTEBOOKLM PROMPT TRUNG TÂM (CHUNG) - {lesson_title}
{prompt_slide_content}

---

{prompt_info_content}
"""

    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt_content.strip() + "\n")
    with open(prompt_path_slide, "w", encoding="utf-8") as f:
        f.write(prompt_slide_content.strip() + "\n")
    with open(prompt_path_info, "w", encoding="utf-8") as f:
        f.write(prompt_info_content.strip() + "\n")
        
    console.print(f"  [green]✓ Đã sinh Slide prompt tại: {prompt_path_slide}[/green]")
    console.print(f"  [green]✓ Đã sinh Infographic prompt tại: {prompt_path_info}[/green]")
    
    return prompt_path_slide, prompt_path_info, prompt_path


def run_command_live(cmd):
    """Run shell command and return stdout/stderr."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)


def execute_notebooklm_pipeline(output_dir, lesson_slug, lesson_title, notebook_id=None):
    """
    Run the nlm CLI tool to generate slide decks and infographics.
    """
    # 1. Generate prompt files
    prompt_path_slide, prompt_path_info, prompt_path = generate_notebooklm_prompt(output_dir, lesson_slug, lesson_title)
    
    if not notebook_id:
        console.print("[yellow]ℹ Không có --notebook-id được cung cấp. Bỏ qua bước tự động gọi nlm CLI.[/yellow]")
        console.print("[yellow]  Giáo viên có thể sao chép các file prompt ở trên để chạy thủ công trên giao diện web.[/yellow]")
        return False
        
    console.print(f"\n[bold]Đang tự động chạy NotebookLM CLI (nlm) cho Notebook ID: {notebook_id}...[/bold]")
    
    # 2. Check if logged in
    code, stdout, stderr = run_command_live("nlm login --check")
    if code != 0:
        console.print("[red]✗ Chưa đăng nhập nlm CLI. Vui lòng chạy lệnh 'nlm login' trước tiên.[/red]")
        return False
        
    # 3. Create slides
    console.print("  [cyan]1. Đang gửi yêu cầu Google NotebookLM tạo Slide Deck...[/cyan]")
    slide_cmd = f'nlm create slides {notebook_id} --focus "@{prompt_path_slide}" --language vi --confirm'
    code, stdout, stderr = run_command_live(slide_cmd)
    
    slide_artifact_id = None
    if code == 0:
        match = re.search(r'Artifact ID:\s*([a-f0-9\-]+)', stdout)
        if match:
            slide_artifact_id = match.group(1)
            console.print(f"     [green]✓ Yêu cầu tạo Slide thành công. Artifact ID: {slide_artifact_id}[/green]")
        else:
            console.print(f"     [yellow]⚠ Không trích xuất được Artifact ID từ đầu ra CLI. Đầu ra: {stdout.strip()}[/yellow]")
    else:
        console.print(f"     [red]✗ Lỗi khi tạo Slide: {stderr or stdout}[/red]")
        
    # 4. Create infographic
    console.print("  [cyan]2. Đang gửi yêu cầu Google NotebookLM tạo Infographic...[/cyan]")
    info_cmd = f'nlm create infographic {notebook_id} --focus "@{prompt_path_info}" --language vi --confirm'
    code, stdout, stderr = run_command_live(info_cmd)
    
    info_artifact_id = None
    if code == 0:
        match = re.search(r'Artifact ID:\s*([a-f0-9\-]+)', stdout)
        if match:
            info_artifact_id = match.group(1)
            console.print(f"     [green]✓ Yêu cầu tạo Infographic thành công. Artifact ID: {info_artifact_id}[/green]")
        else:
            console.print(f"     [yellow]⚠ Không trích xuất được Artifact ID từ đầu ra CLI. Đầu ra: {stdout.strip()}[/yellow]")
    else:
        console.print(f"     [red]✗ Lỗi khi tạo Infographic: {stderr or stdout}[/red]")
        
    # 5. Smart Polling & Auto-Download every 5 minutes (300 seconds)
    if slide_artifact_id or info_artifact_id:
        console.print("\n[bold cyan]⏳ Khởi động cơ chế Smart Polling kiểm tra trạng thái mỗi 5 phút (Slide / Infographic)...[/bold cyan]")
        wait_interval = 300  # 5 minutes
        max_wait_time = 3600  # 1 hour maximum timeout
        elapsed_time = 0
        
        slide_downloaded = False
        info_downloaded = False
        
        while elapsed_time < max_wait_time:
            # Check if all completed or failed
            if (not slide_artifact_id or slide_downloaded) and (not info_artifact_id or info_downloaded):
                break
                
            console.print(f"[dim]Chờ 5 phút tiếp theo để NotebookLM Cloud xử lý... (Đã chờ: {elapsed_time // 60} phút)[/dim]")
            time.sleep(wait_interval)
            elapsed_time += wait_interval
            
            # Query status
            chk_code, chk_stdout, chk_stderr = run_command_live(f"nlm list artifacts {notebook_id} --json")
            if chk_code != 0:
                console.print("[yellow]⚠ Lỗi khi lấy danh sách artifacts từ CLI. Sẽ thử lại sau.[/yellow]")
                continue
                
            try:
                artifacts = json.loads(chk_stdout)
            except Exception:
                console.print("[yellow]⚠ Lỗi phân tích JSON kết quả artifacts. Sẽ thử lại sau.[/yellow]")
                continue
                
            artifacts_map = {art["id"]: art for art in artifacts}
            
            # Check Slides
            if slide_artifact_id and not slide_downloaded:
                slide_art = artifacts_map.get(slide_artifact_id)
                if slide_art:
                    status = slide_art.get("status", "").lower()
                    console.print(f"   [status] Slide Deck status: {status.upper()}")
                    if status == "completed":
                        console.print("     [green]✓ Slide Deck hoàn thành! Đang tự động tải về...[/green]")
                        pptx_dest = os.path.join(output_dir, "ready", f"{lesson_slug}_slide_deck.pptx")
                        run_command_live(f"nlm download slide-deck {notebook_id} --id {slide_artifact_id} --format pptx -o \"{pptx_dest}\"")
                        
                        pdf_dest = os.path.join(output_dir, "ready", f"{lesson_slug}_slide_deck.pdf")
                        run_command_live(f"nlm download slide-deck {notebook_id} --id {slide_artifact_id} --format pdf -o \"{pdf_dest}\"")
                        slide_downloaded = True
                    elif status in ["failed", "error", "cancelled"]:
                        console.print(f"     [red]✗ Slide Deck thất bại với trạng thái: {status}[/red]")
                        slide_downloaded = True
                else:
                    console.print(f"     [yellow]⚠ Không tìm thấy Slide artifact ID {slide_artifact_id}.[/yellow]")
                    
            # Check Infographic
            if info_artifact_id and not info_downloaded:
                info_art = artifacts_map.get(info_artifact_id)
                if info_art:
                    status = info_art.get("status", "").lower()
                    console.print(f"   [status] Infographic status: {status.upper()}")
                    if status == "completed":
                        console.print("     [green]✓ Infographic hoàn thành! Đang tự động tải về...[/green]")
                        png_dest = os.path.join(output_dir, "ready", f"{lesson_slug}_infographic.png")
                        run_command_live(f"nlm download infographic {notebook_id} --id {info_artifact_id} -o \"{png_dest}\"")
                        info_downloaded = True
                    elif status in ["failed", "error", "cancelled"]:
                        console.print(f"     [red]✗ Infographic thất bại với trạng thái: {status}[/red]")
                        info_downloaded = True
                else:
                    console.print(f"     [yellow]⚠ Không tìm thấy Infographic artifact ID {info_artifact_id}.[/yellow]")
                    
        if elapsed_time >= max_wait_time:
            console.print("[red]❌ Hết thời gian chờ (1 giờ). Quy trình tải xuống tự động bị gián đoạn.[/red]")
            return False
            
    return True
