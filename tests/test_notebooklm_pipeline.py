from pathlib import Path

from gems.config.loader import load_curriculum, load_identity
from gems.notebooklm import nlm_cli
from gems.notebooklm.pipeline import poll_and_download, run_notebooklm_stage, strip_vietnamese_accents
from gems.notebooklm.prompt_builder import generate_notebooklm_prompt
from gems.offline import fixtures
from gems.pipeline.report import RunReport


def test_strip_vietnamese_accents():
    assert strip_vietnamese_accents("Nhiệt dung riêng") == "Nhiet dung rieng"
    assert strip_vietnamese_accents("Đơn vị") == "Don vi"


def _write_worksheet_data(md_dir: Path) -> None:
    """Dựng `worksheet_data.json` thật từ fixture offline — nguồn dữ liệu
    chính mà `prompt_builder.generate_notebooklm_prompt` đọc (thay vì regex
    trên Markdown như bản cũ)."""
    from gems.config.loader import load_curriculum
    from gems.generation import stages

    lesson = load_curriculum().get("bai4")
    architect = fixtures.build_architect(lesson)
    worksheet = fixtures.build_worksheet(architect)
    stages.write_worksheet_json(worksheet, md_dir)


def test_generate_notebooklm_prompt_creates_teacher_and_student_prompts(tmp_path):
    identity = load_identity()
    output_dir = tmp_path / "bai4_nhiet_dung_rieng"
    md_dir = output_dir / "md"
    md_dir.mkdir(parents=True)
    _write_worksheet_data(md_dir)
    (md_dir / "bai4_nhiet_dung_rieng_huong_dan_slide.md").write_text(
        "*Giáo viên thực hiện:* Cô Lan\n## QUY TẮC THIẾT KẾ BẮT BUỘC\n- Quy tắc test 1\n---\n",
        encoding="utf-8",
    )

    teacher_path, student_path, teacher_count, student_count = generate_notebooklm_prompt(
        output_dir, "bai4_nhiet_dung_rieng", "Bài 4 - Nhiệt dung riêng", identity
    )
    assert teacher_path.exists()
    assert student_path.exists()
    assert teacher_count > 0
    assert student_count > 0

    teacher_text = teacher_path.read_text(encoding="utf-8")
    student_text = student_path.read_text(encoding="utf-8")

    assert "Cô Lan" in teacher_text
    assert "Quy tắc test 1" in teacher_text
    # Slide Giáo viên: mục lục + tách Nhiệm vụ/Đáp án
    assert "Mục lục" in teacher_text
    assert "Đáp án" in teacher_text
    # Slide Phiếu học tập: không được có bất kỳ SLIDE nào gắn nhãn "Đáp án —"
    # (từ "Đáp án" vẫn có thể xuất hiện trong câu quy tắc giải thích lý do cấm,
    # nên kiểm tra đúng dòng "SLIDE N: Đáp án — ..." thay vì cả văn bản).
    assert not any(line.split(": ", 1)[-1].startswith("Đáp án —")
                   for line in student_text.splitlines() if line.startswith("SLIDE "))
    assert "SLIDE 1:" in teacher_text
    assert "SLIDE 1:" in student_text


def test_generate_notebooklm_prompt_missing_worksheet_data_returns_zero_counts(tmp_path):
    identity = load_identity()
    output_dir = tmp_path / "bai4_nhiet_dung_rieng"
    (output_dir / "md").mkdir(parents=True)

    teacher_path, student_path, teacher_count, student_count = generate_notebooklm_prompt(
        output_dir, "bai4_nhiet_dung_rieng", "Bài 4 - Nhiệt dung riêng", identity
    )
    assert teacher_count == 0
    assert student_count == 0
    assert teacher_path.exists()  # vẫn ghi file cảnh báo, không crash


def test_poll_and_download_checks_immediately_before_sleeping(monkeypatch, tmp_path):
    """Bug đã sửa: KHÔNG được sleep trước khi kiểm tra lần đầu."""
    sleep_calls = []

    monkeypatch.setattr(nlm_cli, "list_artifacts", lambda notebook_id, profile=None: [
        {"id": "teacher-1", "status": "completed"},
        {"id": "student-1", "status": "completed"},
    ])
    monkeypatch.setattr(nlm_cli, "download_slide_deck", lambda *a, **kw: True)

    statuses = poll_and_download(
        "nb-1", "bai4", tmp_path, "teacher-1", "student-1",
        teacher_expected_slides=0, student_expected_slides=0,
        sleep_fn=lambda s: sleep_calls.append(s), count_slides_fn=lambda p: None,
    )
    assert statuses["giao_vien"] == "downloaded"
    assert statuses["phieu_hoc_tap"] == "downloaded"
    assert sleep_calls == []  # đã xong ngay từ lần check đầu tiên, không được sleep


def test_poll_and_download_marks_failed_status_as_failure_not_success(monkeypatch, tmp_path):
    monkeypatch.setattr(nlm_cli, "list_artifacts", lambda notebook_id, profile=None: [
        {"id": "teacher-1", "status": "failed"},
    ])

    statuses = poll_and_download("nb-1", "bai4", tmp_path, "teacher-1", None, sleep_fn=lambda s: None)
    assert statuses["giao_vien"] == "failed:failed"


def test_poll_and_download_download_failure_is_distinct_status(monkeypatch, tmp_path):
    monkeypatch.setattr(nlm_cli, "list_artifacts", lambda notebook_id, profile=None: [
        {"id": "student-1", "status": "completed"},
    ])
    monkeypatch.setattr(nlm_cli, "download_slide_deck", lambda *a, **kw: False)

    statuses = poll_and_download("nb-1", "bai4", tmp_path, None, "student-1", sleep_fn=lambda s: None)
    assert statuses["phieu_hoc_tap"] == "download_failed"


def test_poll_and_download_timeout_when_never_completes(monkeypatch, tmp_path):
    monkeypatch.setattr(nlm_cli, "list_artifacts", lambda notebook_id, profile=None: [
        {"id": "teacher-1", "status": "processing"},
    ])
    statuses = poll_and_download("nb-1", "bai4", tmp_path, "teacher-1", None, poll_interval=1, max_wait=2,
                                   sleep_fn=lambda s: None)
    assert statuses["giao_vien"] == "timeout"


def test_poll_and_download_detects_slide_count_mismatch(monkeypatch, tmp_path):
    """Bài học từ Bài 28: NotebookLM có thể cắt ngang giữa chừng — số slide
    thật tải về ít hơn số slide kỳ vọng, dù trạng thái báo 'completed'."""
    monkeypatch.setattr(nlm_cli, "list_artifacts", lambda notebook_id, profile=None: [
        {"id": "teacher-1", "status": "completed"},
    ])
    monkeypatch.setattr(nlm_cli, "download_slide_deck", lambda *a, **kw: True)

    statuses = poll_and_download(
        "nb-1", "bai4", tmp_path, "teacher-1", None,
        teacher_expected_slides=27, sleep_fn=lambda s: None, count_slides_fn=lambda p: 21,
    )
    assert statuses["giao_vien"] == "slide_count_mismatch:21/27"


def test_run_notebooklm_stage_reports_failure_when_not_logged_in(monkeypatch, tmp_path):
    identity = load_identity()
    curriculum = load_curriculum()
    lesson = curriculum.get("bai4")
    output_dir = tmp_path / lesson.slug
    md_dir = output_dir / "md"
    md_dir.mkdir(parents=True)
    _write_worksheet_data(md_dir)
    monkeypatch.setattr(nlm_cli, "login_check", lambda profile=None: False)

    report = RunReport(lesson_slug=lesson.slug)
    run_notebooklm_stage(identity, lesson, output_dir, report)

    login_stage = next(s for s in report.stages if s.stage == "nlm_login")
    assert not login_stage.ok
    assert not report.ok


def test_run_notebooklm_stage_stops_early_when_worksheet_data_missing(tmp_path):
    """Không có worksheet_data.json (chưa chạy generate/offline/compose) —
    phải dừng sớm với cảnh báo rõ ràng, không tự sinh prompt sai/thiếu."""
    identity = load_identity()
    curriculum = load_curriculum()
    lesson = curriculum.get("bai4")
    output_dir = tmp_path / lesson.slug
    (output_dir / "md").mkdir(parents=True)

    report = RunReport(lesson_slug=lesson.slug)
    run_notebooklm_stage(identity, lesson, output_dir, report)

    prompt_stage = next(s for s in report.stages if s.stage == "sinh_prompt_notebooklm")
    assert not prompt_stage.ok
    assert not any(s.stage == "nlm_login" for s in report.stages)
