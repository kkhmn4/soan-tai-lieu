# Project Rules: GEMS Word Document Formatting & Design Standards

This document establishes the comprehensive and mandatory project-scoped rules for formatting and designing Word (.docx) documents in this workspace. All subsequent agents and sessions MUST automatically follow these guidelines.

## 1. Typography & Page Layout
- **Font Family:** Strictly use **Times New Roman** for all text elements.
- **Font Sizes (CV5512 — Công văn 5512):**
  - **Heading 1 (Main Title):** 16 pt, Bold, Navy color (`#1E3A5F`), Center-aligned, ALL CAPS.
  - **Heading 2 (Main Sections I, II, III, IV):** 14 pt, Bold, Navy color (`#1E3A5F`), Left-aligned.
  - **Heading 3 (Sub-sections):** 13 pt, Bold, Gray color (`#595959`), Left-aligned.
  - **Heading 4 (Task Phases):** 13 pt, Bold, Navy color (`#1E3A5F`), Left-aligned.
  - **Info Block / Table text / Footers:** 11 pt (or 10 pt for dynamic fields).
- **Page Margins (A4 Setup):**
  - **Left Margin:** **3.0 cm** (strictly reserved for binding/stapling).
  - **Right Margin:** **1.5 cm**.
  - **Top & Bottom Margins:** **2.0 cm**.
- **Paragraph Spacing:**
  - Line spacing must be set to **1.15 lines**.
  - Paragraph space after must be set to **4 pt**.
  - Paragraph space before must be set to **0 pt** (except for headings).
- **Paragraph Alignment:**
  - **Body text / Content paragraphs:** Justify (`WD_ALIGN_PARAGRAPH.JUSTIFY`) — CV5512 requirement.
  - **Headings (H1):** Center-aligned.
  - **Headings (H2, H3, H4):** Left-aligned.

## 2. Color Palette (Design Tokens)
- **Primary Navy:** RGB `(30, 58, 95)` / Hex `#1E3A5F` (used for major headers, titles, table headers).
- **Secondary Mint:** RGB `(232, 245, 233)` / Hex `#E8F5E9` (used for table row alternating shading).
- **Body Dark:** RGB `(33, 33, 33)` / Hex `#212121` (used for body text instead of harsh pure black).
- **Neutral Gray:** RGB `(89, 89, 89)` / Hex `#595959` (used for H3 headers).
- **Neutral Light Gray:** RGB `(191, 191, 191)` / Hex `#BFBFBF` (used for borders, dotted answer lines, separators).

## 3. Document Headers & Metadata
- **Lesson Plan (KHBD) Administrative Header (CV5512):**
  - Single-column header (left-aligned) — **do NOT include Quốc hiệu/Tiêu ngữ** in KHBD:
    * SỞ GIÁO DỤC VÀ ĐÀO TẠO (12 pt, Regular).
    * TRƯỜNG THPT: ... (12 pt, Bold).
    * Thin separator rule below.
  - Main title "KẾ HOẠCH BÀI DẠY" in bold Navy H1 (16 pt, centered) below the header.
  - Metadata block: Môn học, Giáo viên, Ngày soạn, Thời lượng in a borderless 2-column table.
  - Skip repeating metadata from the Markdown source, starting content directly from **I. YÊU CẦU CẦN ĐẠT**.
- **Student Worksheet (PHT) Header:**
  - Worksheet title centered in bold Navy H1.
  - Student information block (Họ và tên, Lớp, Ngày) below the title, styled using a table with fixed column widths (`widths = [Cm(8.5), Cm(3.2), Cm(4.8)]`) and a shortened dotted line to ensure it fits on a **single line** without wrapping.
  - Subtitle line with Time, Score, and Teacher's Comments separated by tabs, followed by a light gray separator rule.

## 4. Chân trang và Đánh số trang (Footer)
- The footer of all documents must center-align dynamic page numbers in the format: `Trang X / Y`.
- This MUST be implemented using MS Word dynamic XML field codes (`PAGE` and `NUMPAGES` wrapped in `w:fldSimple` objects) so that Word automatically updates the page numbers upon document load or print.

## 5. Bảng biểu (Alternating Tables)
- **Table Formatting:**
  - **Header Row:** Shaded in Primary Navy (`#1E3A5F`), with text in bold White, center-aligned.
  - **Alternating Rows:** Alternating data rows must be shaded in Secondary Mint (`#E8F5E9`) for odd rows, and White for even rows.
  - **Borders:** Thin light gray borders (`#BFBFBF`) around all cells.
  - **Margins:** Top/bottom cell margins set to 6 pt, left/right margins set to 8 pt for readability.
- **Administrative Lesson Plan Tables:**
  - Teaching activities must use a 2-column format: `Hoạt động của Giáo viên` (Left) and `Hoạt động của Học sinh` (Right).
  - Bold Navy/Dark labels (e.g., `**Chuyển giao nhiệm vụ:**`, `**Kết luận:**` on the left; `**Thực hiện nhiệm vụ:**`, `**Báo cáo, thảo luận:**`, `**Sản phẩm:**` on the right) must lead the blocks, with action items indented using bullet dashes `-`.

## 6. Paragraph Merging & Formatting
- **Standard Paragraph Folding:** Consecutive lines of text that are not separated by blank lines must be merged into a single paragraph during parsing, unless the next line starts a structural element (heading, list, table, separator).
- **Forced Merge:** Merging must occur even with blank lines if the next non-empty line starts with a lowercase letter, connective symbol (`)`, `,`, `.`, `;`, `:`), or is a short math formula (e.g. `U = E_đ + E_t` or `Q > 0`).
- **HTML Sanitization:** Strip all `<br>`, `<br/>`, and `</br>` tags before writing text runs.
- **LaTeX translation:** Run the `clean_latex` filter over the entire paragraph string to translate raw math expressions (like `\Delta`, `\omega`, `\varphi`, `\pi`) into Unicode equivalents (`Δ`, `ω`, `φ`, `π`) in italic.

## 7. Auto Image Embedding
- Scan paragraph text for raw local image paths (e.g., matching the pattern `ready/hinh_anh/...`).
- Automatically embed the target image centered below that paragraph, clean the raw path from the text, and replace it with a single space to avoid word-joining typos.

## 8. Heading Level 4 (####)
- Render lines starting with `#### ` as bold paragraphs in Navy color (13 pt), removing the raw thashes.

## 9. White Space Preservation
- Worksheet structures must preserve **35-40% empty white space** for student writing and drawing.
- Auto-generate grey dotted answer lines (3 lines) when keywords like `vẽ`, `biểu diễn`, `mô tả`, `vai trò`, `giải thích` are detected, or for questions without punctuation endings.

## 10. Smart Typography (Professional Quotes)
- Convert all straight quotes `"` and `'` to proper Unicode smart/curly quotes before inserting text into Word.
- Use `'` (`\u2019`) for apostrophes, `"` / `"` (`\u201c` / `\u201d`) for quotation marks.
- Implementation: call `smart_typography(text)` from `gems_styles.py` on body text before writing runs.

## 11. Explicit Table Widths (DXA — Never Percentage)
- **CRITICAL:** Always set explicit table width using DXA units. **Never** use `autofit=True` or percentage widths (incompatible with PDF/LibreOffice rendering).
- The `set_table_width(table, width_cm)` utility in `gems_styles.py` handles this conversion (cm → DXA).
- A4 content width with GEMS margins: `21 - 3 - 1.5 = 16.5 cm` = the standard table width.
- Both the table-level width AND each cell's `cell.width` must be set explicitly (dual widths rule).

## 12. Image Alt Text
- Every embedded image must include alt text for accessibility and professional XML compliance.
- Set both `name` and `descr` attributes on the `<wp:docPr>` XML element of the inline drawing.
- Use the image caption (or filename as fallback) as the alt text value.

## 13. Lists — Never Raw Unicode Bullets
- **Never** insert raw Unicode bullet characters (`•`, `\u2022`) as text characters in paragraphs.
- List items starting with `-` must be rendered as properly indented paragraphs with `paragraph_format.left_indent = Cm(0.5)` and a dash prefix run, **not** raw bullet characters.
- Numbered lists must similarly use paragraph-level formatting, not hard-coded `1.`, `2.` text.

## 14. No Newlines Inside Text Runs
- **Never** use `\n` inside a text run. Each paragraph must be a separate `doc.add_paragraph()` call.
- Page breaks must be added inside a paragraph (e.g., `p.runs[0].add_break(WD_BREAK.PAGE)`), never as standalone elements.

## 15. CV5512 Activity Keyword Auto-Bolding (KHBD only)
- In lesson plan activity tables, the following keywords must appear in **bold Navy** (`#1E3A5F`) automatically:
  - `Chuyển giao nhiệm vụ:`, `Thực hiện nhiệm vụ:`, `Báo cáo, thảo luận:`, `Kết luận:`, `Kết luận, nhận định:`, `Sản phẩm:`, `Hỗ trợ:`, `Mục tiêu:`, `Nội dung:`
- Implementation: `_BOLD_KEYWORDS` list in `khbd_exporter.py` auto-injects `**...**` markers before the split-render.

## 16. CV5512 Signature Block (KHBD only)
- Every KHBD must end with a 2-column signature table:
  - **Left column:** XÁC NHẬN CỦA TỔ CHUYÊN MÔN / (Ký và ghi rõ họ tên)
  - **Right column:** GIÁO VIÊN SOẠN / (Ký và ghi rõ họ tên)
- Preceded by a right-aligned italic date line: `........., ngày ....... tháng ....... năm 20.......`

## 17. CV5512 Adjustment Section (KHBD only)
- After "Ưu điểm:", "Hạn chế:", "Hướng điều chỉnh:" lines in section IV, auto-add **2 extra dot lines** for handwritten notes.
- Detected via `_ADJUST_KEYWORDS` in `khbd_exporter.py`.

## 18. Blockquote Handling (dấu >)
- **Never** print raw `>` or `> ` blockquote markers.
- If a line starts with `> `, remove the prefix and format the entire paragraph as a blockquote (indented by `Cm(1.0)` and all runs set to italic).

## 19. Enhanced LaTeX & Symbol Cleanup (clean_latex)
- Automatically convert any LaTeX superscript pattern `^x` or `^{x}` (e.g. `10^6` or `10^{-3}`) into actual Unicode superscript characters (e.g. `10⁶` or `10⁻³`).
- Convert LaTeX degree symbols (e.g. `^{\circ}C`, `^\circ C`) into Unicode `°C`.
- Remove all raw `$` characters remaining in the final text runs to prevent raw LaTeX delimiters from displaying in Word.

## 20. Homework Answer Table Parsing
- In `homework_exporter.py`, if the teacher answer key section contains a Markdown table (lines starting with `|`), the parser must automatically extract and render it into a GEMS styled table (`make_navy_table`) rather than printing raw Markdown text.

## 18. Blockquote Handling (dấu >)
- **Never** print raw `>` or `> ` blockquote markers.
- If a line starts with `> `, remove the prefix and format the entire paragraph as a blockquote (indented by `Cm(1.0)` and all runs set to italic).

## 19. Enhanced LaTeX & Symbol Cleanup (clean_latex)
- Automatically convert any LaTeX superscript pattern `^x` or `^{x}` (e.g. `10^6` or `10^{-3}`) into actual Unicode superscript characters (e.g. `10⁶` or `10⁻³`).
- Convert LaTeX degree symbols (e.g. `^{\circ}C`, `^\circ C`) into Unicode `°C`.
- Remove all raw `$` characters remaining in the final text runs to prevent raw LaTeX delimiters from displaying in Word.

## 20. Homework Answer Table Parsing
- In `homework_exporter.py`, if the teacher answer key section contains a Markdown table (lines starting with `|`), the parser must automatically extract and render it into a GEMS styled table (`make_navy_table`) rather than printing raw Markdown text.
