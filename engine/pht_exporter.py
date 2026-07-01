"""
pht_exporter.py — GEMS Phiếu Học Tập → DOCX
=============================================
Exports a structured GEMS worksheet (PHT) from a Markdown spec
directly to .docx with the GEMS v8.0 Design System.

USAGE:
    from pht_exporter import export_pht
    export_pht(md_path="path/to/phieu_hoc_tap.md",
               output_path="path/to/output.docx",
               lesson_label="Bài 4 — Nhiệt dung riêng")
"""

import re
import os
from gems_styles import (
    Document, setup_page_margins, set_default_style,
    GEMSColors, GEMSFonts,
    add_heading, add_body, add_dot_line, add_separator,
    add_student_info_block, make_navy_table, add_image,
    save_doc, set_cell_shading, set_cell_margins, set_cell_border,
    preprocess_markdown_lines, add_page_number_footer,
    Cm, Pt, Inches, RGBColor, WD_ALIGN_PARAGRAPH,
    clean_latex, smart_typography
)


def _process_single_line(p, text, force_italic=False):
    """
    Parse **bold** and $latex$ fragments inside one line,
    adding runs with appropriate formatting.
    """
    parts = re.split(r'(\*\*.*?\*\*|\$.*?\$)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.bold = True
            run.italic = force_italic
        elif part.startswith('$') and part.endswith('$'):
            # Render formula as italic (substitute for LaTeX)
            formula = clean_latex(part[1:-1])
            run = p.add_run(formula)
            run.italic = True
        else:
            run = p.add_run(part)
            run.italic = force_italic
        run.font.name = GEMSFonts.BODY
        run.font.size = GEMSFonts.SIZE_BODY
        run.font.color.rgb = GEMSColors.DARK


# add_image is imported from gems_styles


def _process_dvkt_section(doc, md_lines, start_idx, md_path):
    """
    Parse one ĐVKT section (## heading) including its tasks.
    Returns the index of the next unprocessed line.
    """
    i = start_idx
    while i < len(md_lines):
        line = md_lines[i].rstrip()

        # --- ĐVKT heading (##) ---
        if line.startswith('## '):
            add_heading(doc, smart_typography(clean_latex(line[3:].strip())), level=2)
            i += 1
            continue

        # --- Sub-heading (###) — task name ---
        if line.startswith('### '):
            # make it a slightly indented bold paragraph
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(smart_typography(clean_latex(line[4:].strip())))
            run.bold = True
            run.font.name = GEMSFonts.BODY
            run.font.size = GEMSFonts.SIZE_H3
            run.font.color.rgb = GEMSColors.GRAY
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

        # --- Table ---
        if line.strip().startswith('|'):
            rows_data = []
            headers = None
            while i < len(md_lines) and md_lines[i].strip().startswith('|'):
                row = [c.strip() for c in md_lines[i].split('|')[1:-1]]
                # Skip alignment row
                if row and all(ch in ':- ' for ch in ''.join(row).replace(' ', '')):
                    i += 1
                    continue
                if headers is None:
                    headers = row
                else:
                    rows_data.append(row)
                i += 1
            if headers:
                # Clean LaTeX in headers and rows before making table
                headers = [smart_typography(clean_latex(h)) for h in headers]
                cleaned_rows = []
                for r in rows_data:
                    cleaned_rows.append([smart_typography(clean_latex(cell)) for cell in r])
                make_navy_table(doc, headers, cleaned_rows)
            continue

        # --- Separator ---
        if line.strip().startswith('---') and len(line.strip()) < 5:
            add_separator(doc)
            i += 1
            continue

        # --- Empty line ---
        if not line.strip():
            i += 1
            continue

        # --- Regular line (text, bullet, instruction) ---
        text_content = smart_typography(clean_latex(line.strip()))

        is_blockquote = False
        if text_content.startswith('> '):
            text_content = text_content[2:]
            is_blockquote = True
        elif text_content.startswith('>'):
            text_content = text_content[1:]
            is_blockquote = True

        # Auto-detect and embed raw image paths (e.g. ready/hinh_anh/do_thi_quy_uoc_dau.png)
        img_match = re.search(r'([\(\s]*)(ready[^\(\s]+\.(?:png|jpg|jpeg))([\s\)]*)', text_content)
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
                text_content = text_content.replace(entire_match, " ")
                text_content = re.sub(r'\s+', ' ', text_content).strip()

        if text_content:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(4)
            if is_blockquote:
                p.paragraph_format.left_indent = Cm(1.0)

            # Rule 9: standalone [DOT_LINE_90] on its own line → use add_dot_line()
            if text_content == '[DOT_LINE_90]':
                # Replace the empty paragraph with a proper dot line
                p._element.getparent().remove(p._element)
                add_dot_line(doc)
                i += 1
                continue

            if text_content.startswith('- ') or text_content.startswith('* '):
                p.paragraph_format.left_indent = Cm(0.5)
                p.paragraph_format.first_line_indent = Cm(-0.3)
                # bullet symbol
                run = p.add_run("- ")
                run.font.name = GEMSFonts.BODY
                run.font.size = GEMSFonts.SIZE_BODY
                run.font.color.rgb = GEMSColors.DARK
                text_to_process = text_content[2:]
            elif text_content.startswith('+ '):
                p.paragraph_format.left_indent = Cm(1.0)
                p.paragraph_format.first_line_indent = Cm(-0.3)
                # bullet symbol
                run = p.add_run("+ ")
                run.font.name = GEMSFonts.BODY
                run.font.size = GEMSFonts.SIZE_BODY
                run.font.color.rgb = GEMSColors.DARK
                text_to_process = text_content[2:]
            else:
                text_to_process = text_content

            # Handle [DOT_LINE_90] inline
            if '[DOT_LINE_90]' in text_to_process:
                parts2 = text_to_process.split('[DOT_LINE_90]')
                for idx2, seg in enumerate(parts2):
                    if seg:
                        _process_single_line(p, seg, force_italic=is_blockquote)
                    if idx2 < len(parts2) - 1:
                        r = p.add_run("." * 90)
                        r.font.color.rgb = GEMSColors.LIGHT_GRAY
                        r.font.size = GEMSFonts.SIZE_SMALL
                        r.font.name = GEMSFonts.BODY
            else:
                _process_single_line(p, text_to_process, force_italic=is_blockquote)

            # If it asks for drawing / answer space, add dot lines
            lowline = text_content.lower()
            if any(kw in lowline for kw in ['vẽ', 'biểu diễn', 'mô tả', 'vai trò', 'giải thích']):
                for _ in range(3):
                    add_dot_line(doc)

            # Numbered lists
            match_num = re.match(r'^(\d+)[\.\)]\s+', text_content)
            if not match_num:
                _check_one = text_content.strip()
                if len(_check_one) > 50 and not re.search(r'[?.:;!]$', _check_one):
                    add_dot_line(doc)

        # Embed the image below the paragraph
        if embedded_img_path:
            add_image(doc, embedded_img_path, "")

        i += 1

    return i


def export_pht(md_path, output_path, lesson_label=None):
    """
    Convert GEMS Phiếu Học Tập (Markdown) → DOCX.

    Parameters
    ----------
    md_path : str
        Path to the .md file containing the worksheet.
    output_path : str
        Desired .docx output path.
    lesson_label : str, optional
        Override lesson title. If omitted, inferred from first # heading.
    """
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"PHT source not found: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    md_lines = preprocess_markdown_lines(raw_lines)

    # Extract lesson name from first # heading if not given
    if not lesson_label:
        for line in md_lines:
            if line.startswith('# '):
                lesson_label = line[2:].strip()
                break
        lesson_label = lesson_label or "Phiếu Học Tập Vật Lý 12"

    doc = Document()
    setup_page_margins(doc, doc_type="pht")
    set_default_style(doc)

    # --- Student info block ---
    add_student_info_block(doc, lesson_label)

    # --- Subtitle ---
    add_body(doc,
             "Thời gian: ........ phút          "
              "Điểm: ......../10          "
              "Nhận xét của giáo viên: ........................................",
             size=GEMSFonts.SIZE_INFO)

    add_separator(doc)

    # --- Process sections ---
    # skip the first line if it's the # heading (already used)
    # and find remaining ## sections
    i = 0
    # skip any preamble after the heading, up to first ##
    started = False
    while i < len(md_lines):
        line = md_lines[i].rstrip()
        if line.startswith('# ') and not started:
            # main title — already used
            started = True
            i += 1
            continue
        if line.startswith('## '):
            _process_dvkt_section(doc, md_lines, i, md_path)
            # find next ## or end
            next_i = i + 1
            while next_i < len(md_lines):
                nl = md_lines[next_i].rstrip()
                if nl.startswith('## '):
                    break
                next_i += 1
            i = next_i
        else:
            i += 1

    # --- Footer info ---
    add_separator(doc)
    add_body(doc, "— Chúc em học tốt! —", size=GEMSFonts.SIZE_INFO)

    return save_doc(doc, output_path)


# ============================================================
#  CLI
# ============================================================
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python pht_exporter.py <input.md> <output.docx> [lesson_label]")
        sys.exit(1)
    label = sys.argv[3] if len(sys.argv) > 3 else None
    result = export_pht(sys.argv[1], sys.argv[2], label)
    print(f"[OK] PHT saved -> {result}")