from docx import Document
from docx.enum.text import WD_COLOR_INDEX

from gems.docx_export.run_formatter import add_formatted_runs


def _runs_for(text):
    doc = Document()
    p = doc.add_paragraph()
    add_formatted_runs(p, text)
    return p.runs


def test_plain_text():
    runs = _runs_for("Nhiệt lượng toả ra")
    assert len(runs) == 1
    assert runs[0].text == "Nhiệt lượng toả ra"
    assert not runs[0].bold
    assert not runs[0].italic


def test_bold_segment():
    runs = _runs_for("Kết luận: **Q = mcΔt**")
    texts = [r.text for r in runs]
    assert "Q = mcΔt" in texts
    bold_run = next(r for r in runs if r.text == "Q = mcΔt")
    assert bold_run.bold is True


def test_italic_segment():
    runs = _runs_for("Đây là *ghi chú nghiêng* trong câu")
    italic_run = next(r for r in runs if r.text == "ghi chú nghiêng")
    assert italic_run.italic is True


def test_latex_segment_is_forced_italic_and_cleaned():
    runs = _runs_for(r"Công thức $Q = mc\Delta t$ áp dụng")
    formula_run = next(r for r in runs if "mcΔ" in r.text)
    assert formula_run.italic is True
    assert "\\Delta" not in formula_run.text


def test_highlight_segment_renders_yellow():
    runs = _runs_for("Từ khóa ==nhiệt dung riêng== cần nhớ")
    highlighted = next(r for r in runs if r.text == "nhiệt dung riêng")
    assert highlighted.font.highlight_color == WD_COLOR_INDEX.YELLOW


def test_empty_text_adds_no_runs():
    runs = _runs_for("")
    assert runs == []
