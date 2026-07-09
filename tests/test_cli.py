import subprocess
import sys

import gems.cli as cli
from gems.offline import fixtures
from gems.pipeline.orchestrator import GEMSPipeline


def test_list_lessons_subprocess_does_not_crash_on_windows_console_encoding():
    """Phát hiện khi kiểm thử thật trên Windows: in tiếng Việt ra console mặc
    định cp1252 (không phải capsys của pytest, vốn luôn Unicode) làm crash
    UnicodeEncodeError. Chạy qua subprocess thật để tái hiện đúng môi trường
    console, xác nhận bản vá `sys.stdout.reconfigure(encoding="utf-8")` ở
    đầu gems/cli.py có hiệu lực."""
    result = subprocess.run(
        [sys.executable, "-m", "gems", "list-lessons"],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "Nhiệt dung riêng" in result.stdout


def test_list_lessons_exit_code(capsys):
    exit_code = cli.main(["list-lessons"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "bai4" in out


def test_offline_command_via_cli(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "GEMSPipeline", lambda: GEMSPipeline(root_dir=tmp_path))
    exit_code = cli.main(["offline", "--lesson", "bai4"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "HOÀN THÀNH" in out
    assert (tmp_path / "output" / "bai4_nhiet_dung_rieng" / "ready" /
            "bai4_nhiet_dung_rieng_phieu_hoc_tap.docx").exists()


def test_lint_command_after_offline_via_cli(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "GEMSPipeline", lambda: GEMSPipeline(root_dir=tmp_path))
    cli.main(["offline", "--lesson", "bai3"])
    exit_code = cli.main(["lint", "--lesson", "bai3"])
    assert exit_code == 0


def test_unrecognized_prompt_returns_exit_1(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "GEMSPipeline", lambda: GEMSPipeline(root_dir=tmp_path))
    exit_code = cli.main(["offline", "--prompt", "xin chào bạn"])
    assert exit_code == 1
    out = capsys.readouterr().out
    assert "Lỗi" in out


def test_compose_command_via_cli(tmp_path, monkeypatch, capsys):
    """Luồng không cần GEMINI_API_KEY: nội dung do AI agent soạn (ở đây giả
    lập bằng fixtures) ghi ra JSON, rồi `python -m gems compose` dựng DOCX."""
    monkeypatch.setattr(cli, "GEMSPipeline", lambda: GEMSPipeline(root_dir=tmp_path))
    pipeline = GEMSPipeline(root_dir=tmp_path)
    lesson = pipeline.curriculum.get("bai6")

    architect = fixtures.build_architect(lesson)
    content_dir = tmp_path / "output" / lesson.slug / "authored"
    content_dir.mkdir(parents=True)
    (content_dir / f"{lesson.slug}_architect.json").write_text(architect.model_dump_json(), encoding="utf-8")
    (content_dir / f"{lesson.slug}_worksheet.json").write_text(
        fixtures.build_worksheet(architect).model_dump_json(), encoding="utf-8")
    (content_dir / f"{lesson.slug}_homework.json").write_text(
        fixtures.build_homework(architect).model_dump_json(), encoding="utf-8")
    (content_dir / f"{lesson.slug}_lesson_plan.json").write_text(
        fixtures.build_lesson_plan(architect).model_dump_json(), encoding="utf-8")

    exit_code = cli.main(["compose", "--lesson", "bai6"])
    assert exit_code == 0, capsys.readouterr().out
    ready_dir = tmp_path / "output" / lesson.slug / "ready"
    assert (ready_dir / f"{lesson.slug}_ke_hoach_bai_day.docx").exists()
