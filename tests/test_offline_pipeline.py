from docx import Document

from gems.config.loader import load_curriculum, load_identity
from gems.docx_export.homework_exporter import export_homework
from gems.docx_export.khbd_exporter import export_khbd
from gems.docx_export.pht_exporter import export_pht
from gems.generation import stages
from gems.offline import fixtures


def test_offline_fixture_to_docx_end_to_end(tmp_path):
    """Không gọi Gemini, không cần mạng: fixture -> markdown -> docx cho cả
    3 loại tài liệu, mô phỏng đúng luồng thật của pipeline."""
    curriculum = load_curriculum()
    identity = load_identity()
    lesson = curriculum.get("bai4")
    md_dir = tmp_path / "md"
    ready_dir = tmp_path / "ready"
    md_dir.mkdir()
    ready_dir.mkdir()

    architect = fixtures.build_architect(lesson)
    worksheet = fixtures.build_worksheet(architect)
    homework = fixtures.build_homework(architect)
    plan = fixtures.build_lesson_plan(architect)

    stages.write_architect_markdown(architect, lesson, md_dir)
    stages.write_lesson_matrix_json(architect, md_dir)
    pht_md = stages.write_worksheet_markdown(worksheet, lesson, md_dir)
    hw_md = stages.write_homework_markdown(homework, lesson, md_dir)
    khbd_md = stages.write_lesson_plan_markdown(plan, lesson, md_dir, identity)

    pht_docx = ready_dir / f"{lesson.slug}_phieu_hoc_tap.docx"
    hw_docx = ready_dir / f"{lesson.slug}_bai_tap_ve_nha.docx"
    khbd_docx = ready_dir / f"{lesson.slug}_ke_hoach_bai_day.docx"

    export_pht(str(pht_md), str(pht_docx), lesson.name)
    export_homework(str(hw_md), str(hw_docx), identity, lesson.name)
    export_khbd(str(khbd_md), str(khbd_docx), identity)

    assert pht_docx.exists() and hw_docx.exists() and khbd_docx.exists()

    hw_doc = Document(str(hw_docx))
    hw_text = "\n".join(p.text for p in hw_doc.paragraphs)
    assert "Câu 1." in hw_text
    assert "Câu 18." in hw_text


def test_homework_question_counts_match_schema_expectation():
    curriculum = load_curriculum()
    lesson = curriculum.get("bai4")
    architect = fixtures.build_architect(lesson)
    homework = fixtures.build_homework(architect)
    assert homework.question_counts == (18, 4, 6)
