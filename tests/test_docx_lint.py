from pathlib import Path

from gems.config.loader import load_identity
from gems.docx_export.khbd_exporter import export_khbd
from gems.docx_export.pht_exporter import export_pht
from gems.qa.docx_lint import lint_khbd_docx, lint_docx_margins

KHBD_FIXTURE = Path(__file__).parent / "fixtures" / "khbd_bai3.md"
PHT_FIXTURE = Path(__file__).parent / "fixtures" / "pht_bai3.md"


def test_lint_passes_on_freshly_exported_khbd(tmp_path):
    out_path = tmp_path / "khbd.docx"
    export_khbd(str(KHBD_FIXTURE), str(out_path), load_identity())
    report = lint_khbd_docx(out_path)
    assert report.passed, report.issues


def test_lint_detects_wrong_margin(tmp_path):
    from docx import Document
    from gems.docx_export import styles

    out_path = tmp_path / "bad_margins.docx"
    doc = Document()
    styles.setup_margins(doc, "pht")  # cố tình sai lề cho 1 file tự nhận là "khbd"
    doc.save(out_path)
    report = lint_docx_margins(out_path, "khbd")
    assert not report.passed
    assert any("Lề trang" in issue for issue in report.issues)


def test_lint_pht_margins_pass(tmp_path):
    out_path = tmp_path / "pht.docx"
    export_pht(str(PHT_FIXTURE), str(out_path), "Bài 3")
    report = lint_docx_margins(out_path, "pht")
    assert report.passed, report.issues
