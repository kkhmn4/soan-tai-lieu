from gems.config.loader import load_curriculum, load_identity, match_lesson_from_prompt


def test_load_curriculum_has_seven_lessons():
    curriculum = load_curriculum()
    assert curriculum.version == 1
    assert set(curriculum.lessons.keys()) == {f"bai{i}" for i in range(1, 8)}
    for lesson in curriculum.lessons.values():
        assert lesson.slug
        assert lesson.yccd_fallback.strip()


def test_load_identity():
    identity = load_identity()
    assert identity.teacher_name == "Kha Khung Hiệp"
    assert identity.default_font == "Times New Roman"


def test_match_lesson_by_number():
    curriculum = load_curriculum()
    lesson = match_lesson_from_prompt("Soạn bài 4 nhiệt dung riêng", curriculum)
    assert lesson is not None
    assert lesson.key == "bai4"
    assert lesson.slug == "bai4_nhiet_dung_rieng"


def test_match_lesson_by_slug_keyword():
    curriculum = load_curriculum()
    lesson = match_lesson_from_prompt("tạo lại học liệu nhiet_dung_rieng", curriculum)
    assert lesson is not None
    assert lesson.key == "bai4"


def test_match_lesson_by_name_keyword():
    curriculum = load_curriculum()
    lesson = match_lesson_from_prompt("Tôi cần phiếu học tập về sự chuyển thể", curriculum)
    assert lesson is not None
    assert lesson.key == "bai2"


def test_match_lesson_returns_none_when_no_match():
    curriculum = load_curriculum()
    lesson = match_lesson_from_prompt("xin chào bạn khỏe không", curriculum)
    assert lesson is None
