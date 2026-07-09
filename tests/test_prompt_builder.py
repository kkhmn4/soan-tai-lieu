from gems.config.loader import load_curriculum, load_identity
from gems.generation import stages
from gems.notebooklm.prompt_builder import (
    _build_slide_items,
    generate_notebooklm_prompt,
    load_worksheet_data,
    parse_slide_guide_for_prompt,
)
from gems.offline import fixtures


def _build_worksheet():
    lesson = load_curriculum().get("bai4")
    architect = fixtures.build_architect(lesson)
    return fixtures.build_worksheet(architect)


def test_load_worksheet_data_roundtrips_via_json(tmp_path):
    worksheet = _build_worksheet()
    stages.write_worksheet_json(worksheet, tmp_path)

    loaded = load_worksheet_data(tmp_path)
    assert loaded is not None
    assert loaded.lesson_name == worksheet.lesson_name
    assert len(loaded.knowledge_formation) == len(worksheet.knowledge_formation)
    assert len(loaded.practice_items) == len(worksheet.practice_items)


def test_load_worksheet_data_returns_none_when_missing(tmp_path):
    assert load_worksheet_data(tmp_path) is None


def test_practice_items_require_instructions_field():
    worksheet = _build_worksheet()
    assert worksheet.practice_items, "fixture cần có ít nhất 1 bài toán Luyện tập"
    for item in worksheet.practice_items:
        assert item.instructions  # bắt buộc khớp yêu cầu skill 4.2 (mọi nhiệm vụ, kể cả Luyện tập)


def test_teacher_slide_items_separate_task_and_answer():
    worksheet = _build_worksheet()
    guide = parse_slide_guide_for_prompt(None, load_identity())
    items = _build_slide_items(worksheet, guide, teacher=True)

    task_slides = [s for s in items if s.startswith("Nhiệm vụ")]
    answer_slides = [s for s in items if s.startswith("Đáp án")]
    assert len(task_slides) == len(answer_slides) > 0
    # mọi slide "Nhiệm vụ" của giáo viên không được in đề bài
    for s in task_slides:
        assert "KHÔNG in đề bài" in s


def test_student_slide_items_never_mention_answers():
    worksheet = _build_worksheet()
    guide = parse_slide_guide_for_prompt(None, load_identity())
    items = _build_slide_items(worksheet, guide, teacher=False)

    assert not any(s.startswith("Đáp án") for s in items)
    assert any("KHÔNG hiện đáp án" in s or "KHÔNG điền sẵn" in s for s in items)


def test_generate_notebooklm_prompt_expected_counts_match_rendered_slide_markers(tmp_path):
    identity = load_identity()
    output_dir = tmp_path / "bai4_nhiet_dung_rieng"
    md_dir = output_dir / "md"
    md_dir.mkdir(parents=True)
    stages.write_worksheet_json(_build_worksheet(), md_dir)

    teacher_path, student_path, teacher_count, student_count = generate_notebooklm_prompt(
        output_dir, "bai4_nhiet_dung_rieng", "Bài 4 - Nhiệt dung riêng", identity
    )
    teacher_text = teacher_path.read_text(encoding="utf-8")
    student_text = student_path.read_text(encoding="utf-8")

    assert "SLIDE 1:" in teacher_text
    assert f"SLIDE {teacher_count}:" in teacher_text
    assert f"SLIDE {student_count}:" in student_text
