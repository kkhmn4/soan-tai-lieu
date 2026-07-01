"""
khbd_exporter.py — GEMS Kế Hoạch Bài Dạy → DOCX
=================================================
Exports a structured lesson plan (KHBD) to .docx
with the GEMS v8.0 Design System.
        lines = f.readlines()
USAGE:
    from khbd_exporter import export_khbd
    export_khbd(md_path="path/to/ke_hoach_bai_day.md",
                output_path="path/to/output.docx")
"""

import re
import os
from datetime import date
from gems_styles import (
    Document, setup_page_margins, set_default_style,
    GEMSColors, GEMSFonts,
    add_heading, add_body, add_separator,
    add_student_info_block, make_navy_table,
    save_doc, set_cell_shading, set_cell_margins, set_cell_border,
    set_table_width, add_page_number_footer,
    Cm, Pt, Inches, RGBColor, WD_ALIGN_PARAGRAPH, WD_TABLE_ALIGNMENT,
    OxmlElement, qn, clean_latex
)


def _add_meta_row(doc, label, value):
    """Label–value in a single line with bold label."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{label}: ")
    r1.bold = True
    r1.font.name = GEMSFonts.BODY
    r1.font.size = GEMSFonts.SIZE_BODY
    r1.font.color.rgb = GEMSColors.DARK
    r2 = p.add_run(str(value))
    r2.font.name = GEMSFonts.BODY
    r2.font.size = GEMSFonts.SIZE_BODY
    r2.font.color.rgb = GEMSColors.DARK
    return p


def add_image(doc, img_path, caption):
    if not os.path.exists(img_path):
        print(f"[WARNING] Image path not found: {img_path}")
        return False
    try:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run()
        run.add_picture(img_path, width=Inches(4.5))
        
        # Add caption
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            run_cap = p_cap.add_run(f"Hình: {caption}")
            run_cap.italic = True
            run_cap.font.name = GEMSFonts.BODY
            run_cap.font.size = Pt(10)
            run_cap.font.color.rgb = GEMSColors.GRAY
        return True
    except Exception as e:
        print(f"[ERROR] Failed to insert image {img_path}: {e}")
        return False


def _parse_lines_to_doc(doc, lines, start=0, md_path=""):
    """Parse a block of markdown lines into the doc with GEMS styling."""
    from gems_styles import add_dot_line, smart_typography
    i = start
    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith('# ') and start == 0:
            # main title — handled externally in KHBD
            i += 1
            continue

        if line.startswith('## '):
            add_heading(doc, smart_typography(clean_latex(line[3:].strip())), level=2)
            i += 1
            continue

        if line.startswith('### '):
            add_heading(doc, smart_typography(clean_latex(line[4:].strip())), level=3)
            i += 1
            continue

        if line.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(smart_typography(clean_latex(line[5:].strip())))
            run.bold = True
            run.font.name = GEMSFonts.BODY
            run.font.size = GEMSFonts.SIZE_BODY
            run.font.color.rgb = GEMSColors.NAVY
            i += 1
            continue

        # Image parsing
        if line.strip().startswith('![') and line.strip().endswith(')'):
            m = re.match(r'^!\[(.*?)\]\((.*?)\)$', line.strip())
            if m:
                caption = m.group(1)
                img_path = m.group(2)
                resolved = os.path.join(os.path.dirname(md_path), img_path)
                if not os.path.exists(resolved):
                    resolved = img_path
                if not os.path.exists(resolved):
                    # Try resolving relative to lesson root (parent of md)
                    lesson_root = os.path.dirname(os.path.dirname(md_path))
                    resolved = os.path.join(lesson_root, img_path)
                if not os.path.exists(resolved):
                    # Try resolving directly in ready/hinh_anh/
                    lesson_root = os.path.dirname(os.path.dirname(md_path))
                    resolved = os.path.join(lesson_root, "ready", "hinh_anh", os.path.basename(img_path))
                add_image(doc, resolved, caption)
                i += 1
                continue

        if line.strip().startswith('|'):
            headers = None
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].split('|')[1:-1]]
                if all(ch in ':- ' for ch in ''.join(cells).replace(' ', '')):
                    i += 1
                    continue
                if headers is None:
                    headers = cells
                else:
                    rows.append(cells)
                i += 1
            if headers:
                # Clean LaTeX and typography in headers and rows before making table
                headers = [smart_typography(clean_latex(h)) for h in headers]
                cleaned_rows = []
                for row in rows:
                    cleaned_rows.append([smart_typography(clean_latex(cell)) for cell in row])
                make_navy_table(doc, headers, cleaned_rows)
            continue

        if line.strip() in ('---', '___') or re.match(r'^-{3,}$', line.strip()):
            add_separator(doc)
            i += 1
            continue

        if not line.strip():
            # skip multiple empties
            i += 1
            continue

        # normal paragraph
        text = line.strip()

        # Rule 18: Blockquote handling
        is_blockquote = False
        if text.startswith('> '):
            text = text[2:]
            is_blockquote = True
        elif text.startswith('>'):
            text = text[1:]
            is_blockquote = True

        # Rule 7: Auto-detect and embed raw image paths in paragraph text
        img_match = re.search(r'([\(\s]*)(ready[^\(\s]+\.(?:png|jpg|jpeg))([\s\)]*)', text)
        embedded_img_path = None
        if img_match:
            entire_match = img_match.group(0)
            img_path = img_match.group(2)
            
            resolved = img_path
            if not os.path.exists(resolved):
                lesson_root = os.path.dirname(os.path.dirname(md_path))
                resolved = os.path.join(lesson_root, img_path)
            if not os.path.exists(resolved):
                lesson_root = os.path.dirname(os.path.dirname(md_path))
                resolved = os.path.join(lesson_root, "ready", "hinh_anh", os.path.basename(img_path))
            
            if os.path.exists(resolved):
                embedded_img_path = resolved
                text = text.replace(entire_match, " ")
                text = re.sub(r'\s+', ' ', text).strip()

        text_content = smart_typography(clean_latex(text))

        if text_content:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

            if is_blockquote:
                p.paragraph_format.left_indent = Cm(1.0)

            # list detection (- is level 1, + is level 2)
            bullet = ''
            if text_content.startswith('- ') or text_content.startswith('* '):
                bullet = '- '
                text_content = text_content[2:]
                p.paragraph_format.left_indent = Cm(0.5)
                p.paragraph_format.first_line_indent = Cm(-0.3)
            elif text_content.startswith('+ '):
                bullet = '+ '
                text_content = text_content[2:]
                p.paragraph_format.left_indent = Cm(1.0)
                p.paragraph_format.first_line_indent = Cm(-0.3)

            parts = re.split(r'(\*\*.*?\*\*|\$.*?\$)', text_content)
            first = True
            for part in parts:
                if not part:
                    continue
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                elif part.startswith('$') and part.endswith('$'):
                    formula = clean_latex(part[1:-1])
                    run = p.add_run(formula)
                    run.italic = True
                else:
                    if bullet and first:
                        run = p.add_run(bullet)
                        run.font.name = GEMSFonts.BODY
                        run.font.size = GEMSFonts.SIZE_BODY
                        run.font.color.rgb = GEMSColors.DARK
                        first = False
                    run = p.add_run(part)
                    if is_blockquote:
                        run.italic = True
                run.font.name = GEMSFonts.BODY
                run.font.size = GEMSFonts.SIZE_BODY
                run.font.color.rgb = GEMSColors.DARK

            # Rule 17: Auto-add 2 extra dot lines after adjustment keywords
            _ADJUST_KEYWORDS = ["Ưu điểm:", "Hạn chế:", "Hướng điều chỉnh:"]
            if any(kw in text for kw in _ADJUST_KEYWORDS):
                for _ in range(2):
                    add_dot_line(doc)

        # Embed the image below the paragraph
        if embedded_img_path:
            add_image(doc, embedded_img_path, "")

        i += 1

    return i

    return i


def export_khbd(md_path, output_path):
    """
    Convert GEMS Kế Hoạch Bài Dạy (Markdown) → DOCX.

    Parameters
    ----------
    md_path : str
        Path to the .md file containing the lesson plan.
    output_path : str
        Desired .docx output path.
    """
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"KHBD source not found: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract title
    title = "KẾ HOẠCH BÀI DẠY"
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip().upper()
            break

    doc = Document()
    setup_page_margins(doc, doc_type="khbd")
    set_default_style(doc)

    # -- Administrative Header (Single-column, left-aligned, per Rule 3) --
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_hdr.paragraph_format.space_after = Pt(2)
    
    r_hdr1 = p_hdr.add_run("SỞ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r_hdr1.font.name = GEMSFonts.BODY
    r_hdr1.font.size = Pt(12)
    r_hdr1.font.color.rgb = GEMSColors.DARK
    
    r_hdr2 = p_hdr.add_run("TRƯỜNG THPT: ................................................")
    r_hdr2.font.name = GEMSFonts.BODY
    r_hdr2.font.size = Pt(12)
    r_hdr2.bold = True
    r_hdr2.font.color.rgb = GEMSColors.DARK
    
    # Kẻ đường separator mỏng ở dưới header
    add_separator(doc)

    # -- Main Title (KẾ HOẠCH BÀI DẠY) --
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.size = GEMSFonts.SIZE_H1
    r_title.font.name = GEMSFonts.HEADER
    r_title.font.color.rgb = GEMSColors.NAVY

    # -- Metadata Block (Borderless Table for clean layout) --
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Row 0: Môn học & Giáo viên
    m_cells0 = meta_table.rows[0].cells
    m_cells0[0].paragraphs[0].add_run("Môn học: ").bold = True
    m_cells0[0].paragraphs[0].add_run("Vật lí 12 (Kết nối tri thức)")
    m_cells0[1].paragraphs[0].add_run("Giáo viên soạn: ").bold = True
    m_cells0[1].paragraphs[0].add_run("Kha Khung Hiệp")
    
    # Row 1: Ngày soạn & Thời lượng
    today = date.today().strftime("%d/%m/%Y")
    m_cells1 = meta_table.rows[1].cells
    m_cells1[0].paragraphs[0].add_run("Ngày soạn: ").bold = True
    m_cells1[0].paragraphs[0].add_run(today)
    m_cells1[1].paragraphs[0].add_run("Thời lượng thực hiện: ").bold = True
    m_cells1[1].paragraphs[0].add_run("2 tiết")

    # Set styles and margins for meta table cells
    for row in meta_table.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=30, bottom=30, left=50, right=50)
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for side in ['w:top', 'w:left', 'w:bottom', 'w:right']:
                el = OxmlElement(side)
                el.set(qn('w:val'), 'none')
                tcBorders.append(el)
            tcPr.append(tcBorders)
            
            p = cell.paragraphs[0]
            for r in p.runs:
                r.font.name = GEMSFonts.BODY
                r.font.size = GEMSFonts.SIZE_BODY
                r.font.color.rgb = GEMSColors.DARK

    add_separator(doc)

    # Skip markdown preamble and titles up to "I. YÊU CẦU CẦN ĐẠT"
    start_line = 0
    for idx, line in enumerate(lines):
        if any(term in line for term in ["I. YÊU CẦU CẦN ĐẠT", "I. Yêu cầu cần đạt", "I. YÊU CẦU"]):
            start_line = idx
            break

    _parse_lines_to_doc(doc, lines, start=start_line, md_path=md_path)

    # -- Signature block (CV5512) --
    add_separator(doc)

    # Date line
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_date = p_date.add_run("........., ngày ....... tháng ....... năm 20.......")
    r_date.italic = True
    r_date.font.name = GEMSFonts.BODY
    r_date.font.size = GEMSFonts.SIZE_BODY
    r_date.font.color.rgb = GEMSColors.DARK

    # 2-column signature table: TCM/BGH | GV
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.autofit = False
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_width(sig_table, 16.5)

    def _fill_sig_cell(cell, title_text, sub_text):
        p1 = cell.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p1.add_run(title_text)
        r1.bold = True; r1.font.name = GEMSFonts.BODY
        r1.font.size = GEMSFonts.SIZE_BODY; r1.font.color.rgb = GEMSColors.DARK

        p2 = cell.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run(sub_text)
        r2.italic = True; r2.font.name = GEMSFonts.BODY
        r2.font.size = GEMSFonts.SIZE_SMALL; r2.font.color.rgb = GEMSColors.GRAY

        for _ in range(4):  # blank space for signature
            cell.add_paragraph()

        p_line = cell.add_paragraph()
        p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_line = p_line.add_run(".................................")
        r_line.font.name = GEMSFonts.BODY
        r_line.font.size = GEMSFonts.SIZE_BODY
        r_line.font.color.rgb = GEMSColors.GRAY

        # Make borderless
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for side in ['w:top', 'w:left', 'w:bottom', 'w:right']:
            el = OxmlElement(side)
            el.set(qn('w:val'), 'none')
            tcBorders.append(el)
        tcPr.append(tcBorders)

    _fill_sig_cell(
        sig_table.rows[0].cells[0],
        "XÁC NHẬN CỦA TỔ CHUYÊN MÔN",
        "(Ký và ghi rõ họ tên)"
    )
    _fill_sig_cell(
        sig_table.rows[0].cells[1],
        "GIÁO VIÊN SOẠN",
        "(Ký và ghi rõ họ tên)"
    )

    # Add dynamic page numbering footer (Trang X / Y)
    add_page_number_footer(doc)

    return save_doc(doc, output_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python khbd_exporter.py <input.md> <output.docx>")
        sys.exit(1)
    result = export_khbd(sys.argv[1], sys.argv[2])
    print(f"[OK] KHBD saved -> {result}")