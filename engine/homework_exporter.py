"""
homework_exporter.py — GEMS Bài Tập Về Nhà → DOCX
===================================================
Exports structured GEMS homework (18 MCQ + 4 T/F + 6 tự luận)
to .docx with the GEMS v8.0 Design System.

USAGE:
    from homework_exporter import export_homework
    export_homework(md_path="path/to/bai_tap_ve_nha.md",
                    output_path="path/to/output.docx")
"""

import re
import os
from gems_styles import (
    Document, setup_a4_page, set_default_style,
    GEMSColors, GEMSFonts,
    add_heading, add_body, add_separator, add_dot_line,
    add_student_info_block, make_navy_table, add_image,
    save_doc, set_cell_shading, set_cell_margins, set_cell_border,
    Cm, Pt, Inches, RGBColor, WD_ALIGN_PARAGRAPH,
    clean_latex, preprocess_markdown_lines, add_page_number_footer,
    smart_typography
)


# ============================================================
#  PARSING HELPERS
# ============================================================

def _add_question(doc, number, text, indent=True):
    """Add a numbered question."""
    text = smart_typography(clean_latex(text))  # Rule 6: LaTeX cleanup + Smart Typography on full text
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    if indent:
        p.paragraph_format.left_indent = Cm(0.5)

    run = p.add_run(f"Câu {number}. ")
    run.bold = True
    run.font.name = GEMSFonts.BODY
    run.font.size = GEMSFonts.SIZE_BODY
    run.font.color.rgb = GEMSColors.DARK

    # Process **bold** and $latex$ in text
    parts = re.split(r'(\*\*.*?\*\*|\$.*?\$)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2])
            r.bold = True
        elif part.startswith('$') and part.endswith('$'):
            formula = clean_latex(part[1:-1])
            r = p.add_run(formula)
            r.italic = True
        else:
            r = p.add_run(part)
        r.font.name = GEMSFonts.BODY
        r.font.size = GEMSFonts.SIZE_BODY
        r.font.color.rgb = GEMSColors.DARK
    return p


def _add_option(doc, label, text):
    """Add a multiple-choice option (A. ... , B. ... , etc.)."""
    text = smart_typography(clean_latex(text))  # Rule 6: LaTeX cleanup + Smart Typography on full text
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.2)
    p.paragraph_format.space_after = Pt(2)
    
    # Render label
    r_lbl = p.add_run(f"{label}. ")
    r_lbl.font.name = GEMSFonts.BODY
    r_lbl.font.size = GEMSFonts.SIZE_SMALL
    r_lbl.font.color.rgb = GEMSColors.DARK
    
    # Process **bold** and $latex$ in text
    parts = re.split(r'(\*\*.*?\*\*|\$.*?\$)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2])
            r.bold = True
        elif part.startswith('$') and part.endswith('$'):
            formula = clean_latex(part[1:-1])
            r = p.add_run(formula)
            r.italic = True
        else:
            r = p.add_run(part)
        r.font.name = GEMSFonts.BODY
        r.font.size = GEMSFonts.SIZE_SMALL
        r.font.color.rgb = GEMSColors.DARK
    return p


def _add_mcq_block(doc, question_number, question_text, options):
    """Question block: stem + 4 options."""
    _add_question(doc, question_number, question_text)
    option_labels = ['A', 'B', 'C', 'D']
    for i, opt in enumerate(options):
        if i < len(option_labels):
            _add_option(doc, option_labels[i], opt)


def _add_tf_block(doc, question_number, stem, statements):
    """True/False question: stem + 4 statements a, b, c, d."""
    _add_question(doc, question_number, stem)  # clean_latex applied inside
    for stmt_label in ['a', 'b', 'c', 'd']:
        if stmt_label in statements:
            stmt_text = smart_typography(clean_latex(statements[stmt_label]))  # Rule 6: LaTeX cleanup + Smart Typography
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.space_after = Pt(2)
            
            # Label
            r_lbl = p.add_run(f"{stmt_label}) ")
            r_lbl.font.name = GEMSFonts.BODY
            r_lbl.font.size = GEMSFonts.SIZE_SMALL
            r_lbl.font.color.rgb = GEMSColors.DARK
            
            # Process **bold** and $latex$ in statement text
            parts = re.split(r'(\*\*.*?\*\*|\$.*?\$)', stmt_text)
            for part in parts:
                if not part:
                    continue
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                elif part.startswith('$') and part.endswith('$'):
                    formula = clean_latex(part[1:-1])
                    r = p.add_run(formula)
                    r.italic = True
                else:
                    r = p.add_run(part)
                r.font.name = GEMSFonts.BODY
                r.font.size = GEMSFonts.SIZE_SMALL
                r.font.color.rgb = GEMSColors.DARK
                
            # "Đúng / Sai" inline
            r2 = p.add_run("  [  Đúng  ·  Sai  ]")
            r2.font.name = GEMSFonts.BODY
            r2.font.size = GEMSFonts.SIZE_TINY
            r2.font.color.rgb = GEMSColors.LIGHT_GRAY


def _add_short_answer_block(doc, question_number, text, answer_space=True):
    """Short-answer question with space for working."""
    _add_question(doc, question_number, text)
    # Rule 9: Three lines of dot answer space to align with PHT
    if answer_space:
        for _ in range(3):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run("." * 85)
            r.font.size = GEMSFonts.SIZE_SMALL
            r.font.color.rgb = GEMSColors.LIGHT_GRAY
            r.font.name = GEMSFonts.BODY


# ============================================================
#  MAIN EXPORTER
# ============================================================

def export_homework(md_path, output_path):
    """
    Convert GEMS Bài Tập Về Nhà (Markdown) → DOCX.

    Auto-detects homework structure:
      - Part I: 18 MCQ (often marked with "Phần I" or "I.")
      - Part II: 4 True/False (often "Phần II" or "II.")
      - Part III: 6 Short answer (often "Phần III" or "III.")

    If the structure labels are absent, falls back to parsing
    all questions in order.

    Parameters
    ----------
    md_path : str
        Path to the .md file containing the homework.
    output_path : str
        Desired .docx output path.
    """
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Homework source not found: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    # Rule 6: merge split formula/connector lines before parsing
    lines = preprocess_markdown_lines(raw_lines)

    # Extract lesson title
    title = "BÀI TẬP VỀ NHÀ VẬT LÝ 12"
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip().upper()
            break

    doc = Document()
    setup_a4_page(doc)
    set_default_style(doc)

    # -- Title + Student info block --
    # add_student_info_block already calls add_heading(level=1) internally
    # Rule: do NOT call add_heading separately to avoid duplicate title
    add_student_info_block(doc, title)

    # -- Instructions --
    add_body(doc,
             "Hướng dẫn: Học sinh làm bài ra giấy hoặc điền trực tiếp vào phiếu. "
             "Thời gian dự kiến: 45 phút.",
             size=GEMSFonts.SIZE_INFO)
    add_separator(doc)

    # ================================================================
    #  PARSING — three parts
    # ================================================================

    current_part = None  # 'I', 'II', 'III' or None
    part_titles = {
        'I': 'PHẦN I — TRẮC NGHIỆM NHIỀU LỰA CHỌN (18 câu)',
        'II': 'PHẦN II — TRẮC NGHIỆM ĐÚNG / SAI (4 câu)',
        'III': 'PHẦN III — TỰ LUẬN (6 câu)',
    }

    # State machine for MCQ parsing
    in_mcq = False
    in_tf = False
    in_short = False
    current_qnum = 0
    mcq_count = 0
    tf_count = 0
    short_count = 0

    # Buffer for an MCQ question
    buffered_stem = None
    buffered_options = []

    def flush_mcq():
        """Emit the buffered MCQ if present."""
        nonlocal buffered_stem, buffered_options, mcq_count
        if buffered_stem is not None:
            mcq_count += 1
            _add_mcq_block(doc, mcq_count, buffered_stem, buffered_options)
        buffered_stem = None
        buffered_options = []

    # Buffer for TF question
    tf_stem = None
    tf_statements = {}

    def flush_tf():
        nonlocal tf_stem, tf_statements, tf_count
        if tf_stem is not None:
            tf_count += 1
            _add_tf_block(doc, tf_count, tf_stem, tf_statements)
        tf_stem = None
        tf_statements = {}

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        # Dừng vòng lặp câu hỏi khi bắt đầu phần đáp án
        if re.match(r'^#+\s*[Đđ]áp\s*[áa]n', stripped, re.IGNORECASE) or (stripped.startswith('#') and 'ĐÁP ÁN' in stripped.upper()):
            break

        # ---- Part headings ----
        part_match = re.match(r'#{1,3}\s*[Pp]hần\s+(I{1,3}|[IV]+)\b', stripped)
        if not part_match:
            part_match = re.match(r'#+\s*(I{1,3})[\.\)]\s', stripped)
        if not part_match:
            part_match = re.match(r'\*\*?Phần (I{1,3})\*\*?', stripped)

        if part_match:
            roman = part_match.group(1)
            roman_map = {'I': 'I', 'II': 'II', 'III': 'III'}
            if roman in roman_map:
                flush_mcq()
                flush_tf()
                current_part = roman_map[roman]
                add_heading(doc, part_titles.get(current_part, f'Phần {current_part}'), level=2)
            i += 1
            continue

        # Detect part with simple pattern like "Phần I" "Phần II" "Phần III"
        if stripped in ('Phần I', 'Phần II', 'Phần III',
                        'PHẦN I', 'PHẦN II', 'PHẦN III',
                        'I.', 'II.', 'III.',
                        'I)', 'II)', 'III)'):
            flush_mcq()
            flush_tf()
            part_key = {'I': 'I', 'II': 'II', 'III': 'III',
                        'I.': 'I', 'II.': 'II', 'III.': 'III',
                        'I)': 'I', 'II)': 'II', 'III)': 'III'}.get(stripped.split('.')[0]
                                                                 if '.' in stripped else
                                                                 stripped.split(')')[0]
                                                                 if ')' in stripped else
                                                                 stripped.split()[-1])
            # Normalize
            if stripped in ('I.', 'I)') or stripped == 'Phần I' or stripped == 'PHẦN I':
                current_part = 'I'
            elif stripped in ('II.', 'II)') or stripped == 'Phần II' or stripped == 'PHẦN II':
                current_part = 'II'
            elif stripped in ('III.', 'III)') or stripped == 'Phần III' or stripped == 'PHẦN III':
                current_part = 'III'

            title_text = part_titles.get(current_part, f'Phần {current_part}')
            add_heading(doc, title_text, level=2)
            i += 1
            continue

        # ---- Empty lines ----
        if not stripped:
            i += 1
            continue

        # ---- Separator ----
        if re.match(r'^-{3,}$', stripped) or stripped == '___':
            i += 1
            continue

        # Process blockquote (dấu >)
        is_blockquote = False
        if stripped.startswith('> '):
            stripped = stripped[2:]
            is_blockquote = True
        elif stripped.startswith('>'):
            stripped = stripped[1:]
            is_blockquote = True

        # Process image run
        if stripped.startswith('![') and stripped.endswith(')'):
            m = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
            if m:
                caption = m.group(1)
                img_path = m.group(2)
                resolved = os.path.join(os.path.dirname(md_path), img_path)
                if not os.path.exists(resolved):
                    resolved = img_path
                if not os.path.exists(resolved):
                    lesson_root = os.path.dirname(os.path.dirname(md_path))
                    resolved = os.path.join(lesson_root, img_path)
                if not os.path.exists(resolved):
                    lesson_root = os.path.dirname(os.path.dirname(md_path))
                    resolved = os.path.join(lesson_root, "ready", "hinh_anh", os.path.basename(img_path))
                add_image(doc, resolved, caption)
                i += 1
                continue

        # ---- Detect MCQ question pattern: "Câu N." or "N." followed by 4 options ----
        mcq_qmatch = re.match(r'(?:Câu\s+)?(\d+)[\.\)]\s+(.*)', stripped)

        # ---- Detect True/False question ----
        tf_qmatch = re.match(r'(?:Câu\s+)?(\d+)[\.\)]\s+(.*)', stripped) if not mcq_qmatch else None

        # ---- If we're in Part I (MCQ) ----
        if current_part == 'I' or (current_part is None and mcq_count < 18):
            if mcq_qmatch:
                # Check if next few lines are options A-D
                opts_found = []
                j = i + 1
                while j < min(i + 5, len(lines)):
                    optm = re.match(r'([A-Da-d])[\.\)]\s+(.*)', lines[j].strip())
                    if optm:
                        opts_found.append(optm.group(2).strip())
                    else:
                        break
                    j += 1

                if len(opts_found) >= 3:
                    # It's an MCQ
                    flush_mcq()
                    buffered_stem = mcq_qmatch.group(2).strip()
                    buffered_options = opts_found[:4]
                    i = j
                    continue

            # Not an MCQ line — emit as body text (instructions etc.)
            if current_part == 'I':
                add_body(doc, stripped, size=GEMSFonts.SIZE_SMALL)

        # ---- If we're in Part II (True/False) ----
        if current_part == 'II' or (current_part is None and 18 <= mcq_count < 22):
            if tf_qmatch:
                flush_tf()
                tf_stem = tf_qmatch.group(2).strip()
                # Parse substatements
                j = i + 1
                while j < len(lines):
                    sub = lines[j].strip()
                    subm = re.match(r'([a-d])[\)\.]\s+(.*)', sub)
                    if subm:
                        tf_statements[subm.group(1)] = subm.group(2).strip()
                    else:
                        break
                    j += 1
                if tf_statements:
                    i = j
                    continue

        # ---- If we're in Part III (Short answer) ----
        if current_part == 'III' or (current_part is None and short_count < 6):
            if mcq_qmatch:
                short_count += 1
                _add_short_answer_block(doc, short_count, mcq_qmatch.group(2).strip())
                i += 1
                continue

        # ---- Regular text (headings, notes, instructions) ----
        if stripped.startswith('#'):
            level = min(len(line) - len(line.lstrip('#')), 3)
            add_heading(doc, smart_typography(clean_latex(stripped.lstrip('#').strip())), level=level)
        elif stripped.startswith('- ') or stripped.startswith('* '):
            # Rule 13: no raw Unicode bullets — use dash prefix with indent
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.5)
            p.paragraph_format.first_line_indent = Cm(-0.3)
            p.paragraph_format.space_after = Pt(4)
            r_bullet = p.add_run("- ")
            r_bullet.font.name = GEMSFonts.BODY
            r_bullet.font.size = GEMSFonts.SIZE_BODY
            r_bullet.font.color.rgb = GEMSColors.DARK
            r_text = p.add_run(smart_typography(clean_latex(stripped[2:])))
            r_text.font.name = GEMSFonts.BODY
            r_text.font.size = GEMSFonts.SIZE_BODY
            r_text.font.color.rgb = GEMSColors.DARK
            if is_blockquote:
                r_text.italic = True
        else:
            p_body = add_body(doc, smart_typography(clean_latex(stripped)), size=GEMSFonts.SIZE_SMALL)
            if is_blockquote:
                p_body.paragraph_format.left_indent = Cm(1.0)
                for run in p_body.runs:
                    run.italic = True

        i += 1

    # Flush any remaining buffered question
    flush_mcq()
    flush_tf()

    # ---- Answer key section (separate page) ----
    add_separator(doc)
    add_heading(doc, "ĐÁP ÁN CHO GIÁO VIÊN", level=1)

    # Try to find answer key block (## Đáp án or --- ĐÁP ÁN ---)
    answer_mode = False
    answer_text = []
    for line in lines:
        sl = line.strip()
        if re.match(r'^#+\s*[Đđ]áp\s*[áa]n', sl, re.IGNORECASE) or (sl.startswith('#') and 'ĐÁP ÁN' in sl.upper()):
            answer_mode = True
            continue
        if answer_mode:
            answer_text.append(line)

    if answer_text:
        answer_lines = [l.strip() for l in answer_text if l.strip()]
        
        table_headers = None
        table_rows = []
        
        def flush_table_buffer():
            nonlocal table_headers, table_rows
            if table_headers and table_rows:
                cleaned_headers = [smart_typography(clean_latex(h)) for h in table_headers]
                cleaned_rows = []
                for r in table_rows:
                    cleaned_rows.append([smart_typography(clean_latex(cell)) for cell in r])
                make_navy_table(doc, cleaned_headers, cleaned_rows)
            table_headers = None
            table_rows = []

        for l in answer_lines:
            if l.startswith('|'):
                cells = [c.strip() for c in l.split('|')[1:-1]]
                if cells and all(ch in ':- ' for ch in ''.join(cells).replace(' ', '')):
                    continue
                if table_headers is None:
                    table_headers = cells
                else:
                    table_rows.append(cells)
            else:
                flush_table_buffer()
                
                # Render non-table elements
                if l.startswith('#'):
                    level = min(len(l) - len(l.lstrip('#')), 3)
                    add_heading(doc, smart_typography(clean_latex(l.lstrip('#').strip())), level=level)
                elif l.startswith('- ') or l.startswith('* '):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    p.paragraph_format.left_indent = Cm(0.5)
                    p.paragraph_format.first_line_indent = Cm(-0.3)
                    p.paragraph_format.space_after = Pt(4)
                    r_bullet = p.add_run("- ")
                    r_bullet.font.name = GEMSFonts.BODY
                    r_bullet.font.size = GEMSFonts.SIZE_BODY
                    r_bullet.font.color.rgb = GEMSColors.DARK
                    
                    r_text = p.add_run(smart_typography(clean_latex(l[2:])))
                    r_text.font.name = GEMSFonts.BODY
                    r_text.font.size = GEMSFonts.SIZE_BODY
                    r_text.font.color.rgb = GEMSColors.DARK
                elif l.startswith('+ '):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    p.paragraph_format.left_indent = Cm(1.0)
                    p.paragraph_format.first_line_indent = Cm(-0.3)
                    p.paragraph_format.space_after = Pt(4)
                    r_bullet = p.add_run("+ ")
                    r_bullet.font.name = GEMSFonts.BODY
                    r_bullet.font.size = GEMSFonts.SIZE_BODY
                    r_bullet.font.color.rgb = GEMSColors.DARK
                    
                    r_text = p.add_run(smart_typography(clean_latex(l[2:])))
                    r_text.font.name = GEMSFonts.BODY
                    r_text.font.size = GEMSFonts.SIZE_BODY
                    r_text.font.color.rgb = GEMSColors.DARK
                else:
                    add_body(doc, smart_typography(clean_latex(l)), size=GEMSFonts.SIZE_SMALL)
                    
        flush_table_buffer()
    else:
        add_body(doc, "(Đáp án chi tiết vui lòng xem file đáp án riêng.)",
                 italic=True, size=GEMSFonts.SIZE_INFO)

    add_page_number_footer(doc)  # Rule 4: Trang X / Y dynamic footer
    return save_doc(doc, output_path)


# ============================================================
#  CLI
# ============================================================
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python homework_exporter.py <input.md> <output.docx>")
        sys.exit(1)
    result = export_homework(sys.argv[1], sys.argv[2])
    print(f"[OK] Homework saved -> {result}")