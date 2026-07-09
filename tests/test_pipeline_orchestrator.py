import pytest

from gems.offline import fixtures
from gems.pipeline.orchestrator import GEMSPipeline, LessonNotFoundError


def test_offline_pipeline_produces_ready_docx_and_metadata(tmp_path):
    pipeline = GEMSPipeline(root_dir=tmp_path)
    report = pipeline.offline("bai4")

    assert report.ok, report.summary_lines()
    ready_dir = tmp_path / "output" / "bai4_nhiet_dung_rieng" / "ready"
    assert (ready_dir / "bai4_nhiet_dung_rieng_phieu_hoc_tap.docx").exists()
    assert (ready_dir / "bai4_nhiet_dung_rieng_ke_hoach_bai_day.docx").exists()
    assert (ready_dir / "bai4_nhiet_dung_rieng_bai_tap_ve_nha.docx").exists()

    metadata_path = tmp_path / "output" / "bai4_nhiet_dung_rieng" / "metadata.json"
    assert metadata_path.exists()


def test_resolve_lesson_by_natural_language_prompt(tmp_path):
    pipeline = GEMSPipeline(root_dir=tmp_path)
    lesson = pipeline.resolve_lesson("soạn bài 6 nhiệt nóng chảy riêng")
    assert lesson.key == "bai6"


def test_resolve_lesson_raises_when_no_match(tmp_path):
    pipeline = GEMSPipeline(root_dir=tmp_path)
    with pytest.raises(LessonNotFoundError):
        pipeline.resolve_lesson("xin chào bạn khỏe không")


def test_generate_without_api_key_reports_failure(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    pipeline = GEMSPipeline(root_dir=tmp_path)
    report = pipeline.generate("bai4")
    assert not report.ok
    assert any("GEMINI_API_KEY" in (s.error or "") for s in report.stages)


def test_lint_after_offline_run_passes(tmp_path):
    pipeline = GEMSPipeline(root_dir=tmp_path)
    pipeline.offline("bai3")
    report = pipeline.lint("bai3")
    assert report.ok, report.summary_lines()


def test_compose_from_ai_authored_json_produces_docx(tmp_path):
    """Mô phỏng đúng luồng người dùng muốn: KHÔNG gọi Gemini API, mà nội dung
    (ở đây giả lập bằng fixtures, thực tế do AI agent tự soạn) được ghi sẵn
    thành JSON khớp schema Pydantic rồi đưa qua compose()."""
    pipeline = GEMSPipeline(root_dir=tmp_path)
    lesson = pipeline.curriculum.get("bai5")

    architect = fixtures.build_architect(lesson)
    worksheet = fixtures.build_worksheet(architect)
    homework = fixtures.build_homework(architect)
    plan = fixtures.build_lesson_plan(architect)

    content_dir = tmp_path / "authored_by_agent"
    content_dir.mkdir()
    (content_dir / f"{lesson.slug}_architect.json").write_text(architect.model_dump_json(), encoding="utf-8")
    (content_dir / f"{lesson.slug}_worksheet.json").write_text(worksheet.model_dump_json(), encoding="utf-8")
    (content_dir / f"{lesson.slug}_homework.json").write_text(homework.model_dump_json(), encoding="utf-8")
    (content_dir / f"{lesson.slug}_lesson_plan.json").write_text(plan.model_dump_json(), encoding="utf-8")

    report = pipeline.compose("bai5", content_dir=content_dir)
    assert report.ok, report.summary_lines()

    ready_dir = tmp_path / "output" / lesson.slug / "ready"
    assert (ready_dir / f"{lesson.slug}_phieu_hoc_tap.docx").exists()
    assert (ready_dir / f"{lesson.slug}_ke_hoach_bai_day.docx").exists()
    assert (ready_dir / f"{lesson.slug}_bai_tap_ve_nha.docx").exists()


def test_compose_uses_default_content_dir_under_output(tmp_path):
    pipeline = GEMSPipeline(root_dir=tmp_path)
    lesson = pipeline.curriculum.get("bai2")
    architect = fixtures.build_architect(lesson)

    default_dir = tmp_path / "output" / lesson.slug / "authored"
    default_dir.mkdir(parents=True)
    (default_dir / f"{lesson.slug}_architect.json").write_text(architect.model_dump_json(), encoding="utf-8")

    report = pipeline.compose("bai2")  # không truyền content_dir
    architect_stage = next(s for s in report.stages if s.stage == "phan_tich_yccd")
    assert architect_stage.ok
    # Các bước sau thiếu file JSON tương ứng nên thất bại có kiểm soát, không crash
    assert not report.ok


def test_compose_missing_content_reports_failure_not_crash(tmp_path):
    pipeline = GEMSPipeline(root_dir=tmp_path)
    report = pipeline.compose("bai1", content_dir=tmp_path / "khong_ton_tai")
    assert not report.ok
    assert any("architect" in (s.error or "").lower() or "Không tìm thấy" in (s.error or "")
               for s in report.stages)
