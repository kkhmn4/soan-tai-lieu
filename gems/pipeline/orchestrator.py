"""Bộ điều phối GEMS duy nhất — thay thế 2 pipeline song song không tương
thích của bản cũ (`gems_agent.py` đang chạy thật vs. `main.py` +
`gems_analyzer.py` + `worksheet_generator.py` + `homework_generator.py` đã
chết, không còn ai import). Từ giờ chỉ có 1 đường đi cho mỗi giai đoạn.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from gems.config.loader import Curriculum, Identity, LessonSpec, load_curriculum, load_identity, match_lesson_from_prompt
from gems.docx_export.homework_exporter import export_homework
from gems.docx_export.khbd_exporter import export_khbd
from gems.docx_export.pht_exporter import export_pht
from gems.generation import from_json, stages
from gems.generation.gemini_client import GeminiClient
from gems.generation.self_correction import correct_markdown_file
from gems.offline import fixtures
from gems.pipeline.report import RunReport

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class LessonNotFoundError(ValueError):
    pass


class GEMSPipeline:
    def __init__(self, root_dir: Path | None = None, curriculum: Curriculum | None = None,
                 identity: Identity | None = None):
        self.root_dir = root_dir or REPO_ROOT
        self.curriculum = curriculum or load_curriculum()
        self.identity = identity or load_identity()

    # ------------------------------------------------------------------
    #  Tiện ích chung
    # ------------------------------------------------------------------
    def resolve_lesson(self, prompt_or_key: str) -> LessonSpec:
        lesson = self.curriculum.lessons.get(prompt_or_key)
        if lesson:
            return lesson
        lesson = match_lesson_from_prompt(prompt_or_key, self.curriculum)
        if lesson is None:
            raise LessonNotFoundError(
                f"Không nhận diện được bài học nào từ: '{prompt_or_key}'. "
                f"Các bài hiện có: {', '.join(sorted(self.curriculum.lessons))}. "
                "Vui lòng nói rõ số bài (ví dụ 'bài 4') hoặc tên bài."
            )
        return lesson

    def get_lesson_dirs(self, lesson: LessonSpec) -> tuple[Path, Path, Path]:
        """API công khai: (output_dir, md_dir, ready_dir) cho 1 bài học, tạo sẵn nếu chưa có."""
        return self._lesson_dirs(lesson)

    def _lesson_dirs(self, lesson: LessonSpec) -> tuple[Path, Path, Path]:
        output_dir = self.root_dir / "output" / lesson.slug
        md_dir = output_dir / "md"
        ready_dir = output_dir / "ready"
        md_dir.mkdir(parents=True, exist_ok=True)
        ready_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "notebooklm").mkdir(parents=True, exist_ok=True)
        return output_dir, md_dir, ready_dir

    def _load_yccd_text(self, lesson: LessonSpec) -> str:
        yccd_path = self.root_dir / "tai-lieu-goc" / lesson.yccd_file
        if yccd_path.exists():
            return yccd_path.read_text(encoding="utf-8")
        return lesson.yccd_fallback

    # ------------------------------------------------------------------
    #  Biên dịch DOCX (dùng chung cho generate/offline)
    # ------------------------------------------------------------------
    def _compile_docx(self, lesson: LessonSpec, md_dir: Path, ready_dir: Path, report: RunReport) -> None:
        dispatch = [
            ("phieu_hoc_tap", lambda src, dest: export_pht(str(src), str(dest), lesson.name)),
            ("ke_hoach_bai_day", lambda src, dest: export_khbd(str(src), str(dest), self.identity)),
            ("bai_tap_ve_nha", lambda src, dest: export_homework(str(src), str(dest), self.identity, lesson.name)),
        ]
        for md_file in sorted(md_dir.glob("*.md")):
            for marker, exporter in dispatch:
                if marker in md_file.name:
                    dest = ready_dir / (md_file.stem + ".docx")
                    try:
                        exporter(md_file, dest)
                        report.add(f"bien_dich_docx:{marker}", ok=True, artifact_path=dest)
                    except Exception as exc:  # noqa: BLE001 — ghi lại lỗi thật cho từng file, không dừng cả pipeline
                        report.add(f"bien_dich_docx:{marker}", ok=False, error=str(exc))
                    break

    def _self_correct(self, client: GeminiClient, lesson: LessonSpec, md_dir: Path, report: RunReport) -> None:
        for md_file in sorted(md_dir.glob("*.md")):
            if "dac_ta" in md_file.name or "matrix" in md_file.name:
                continue
            is_lesson_plan = "ke_hoach_bai_day" in md_file.name
            result = correct_markdown_file(client, self.identity, md_file, is_lesson_plan=is_lesson_plan)
            if result.issues_found and not result.error:
                report.add(f"tu_sua_loi:{md_file.name}", ok=True,
                            detail=f"đã sửa sau {result.attempts} lần thử", warnings=result.issues_found)
                self._compile_docx(lesson, md_dir, md_dir.parent / "ready", report)
            elif result.error:
                report.add(f"tu_sua_loi:{md_file.name}", ok=False, error=result.error,
                            warnings=result.issues_found)

    def _write_metadata(self, lesson: LessonSpec, output_dir: Path, ready_dir: Path, report: RunReport) -> None:
        files = []
        for f in sorted(ready_dir.iterdir()) if ready_dir.exists() else []:
            if f.is_file():
                files.append({"name": f.name, "size_bytes": f.stat().st_size, "type": f.suffix[1:].upper()})
        metadata = {
            "lesson_name": lesson.name,
            "slug": lesson.slug,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "files": files,
            "stages": [{"stage": s.stage, "ok": s.ok} for s in report.stages],
        }
        (output_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    #  Các lệnh chính
    # ------------------------------------------------------------------
    def generate(self, lesson_key: str) -> RunReport:
        """Sinh học liệu thật bằng Gemini (cần GEMINI_API_KEY)."""
        lesson = self.resolve_lesson(lesson_key)
        output_dir, md_dir, ready_dir = self._lesson_dirs(lesson)
        report = RunReport(lesson_slug=lesson.slug)
        client = GeminiClient()

        if not client.is_online:
            report.add("phan_tich_yccd", ok=False, error="Thiếu GEMINI_API_KEY trong .env — không thể sinh học liệu mới.")
            return report

        try:
            architect = stages.analyze_yccd(client, self.identity, lesson, self._load_yccd_text(lesson))
            spec_path = stages.write_architect_markdown(architect, lesson, md_dir)
            stages.write_lesson_matrix_json(architect, md_dir)
            report.add("phan_tich_yccd", ok=True, artifact_path=spec_path)
        except Exception as exc:  # noqa: BLE001
            report.add("phan_tich_yccd", ok=False, error=str(exc))
            return report  # đây là bước duy nhất chặn toàn bộ pipeline, giống thiết kế gốc

        worksheet = None
        try:
            worksheet = stages.generate_worksheet_content(client, self.identity, architect)
            path = stages.write_worksheet_markdown(worksheet, lesson, md_dir)
            stages.write_worksheet_json(worksheet, md_dir)
            report.add("sinh_phieu_hoc_tap", ok=True, artifact_path=path)
        except Exception as exc:  # noqa: BLE001
            report.add("sinh_phieu_hoc_tap", ok=False, error=str(exc))

        for stage_name, fn in [
            ("sinh_ke_hoach_bai_day", lambda: stages.write_lesson_plan_markdown(
                stages.generate_lesson_plan_content(client, self.identity, architect), lesson, md_dir, self.identity)),
            ("sinh_huong_dan_slide", lambda: stages.write_slide_guide_markdown(
                self.identity, lesson, md_dir, architect, worksheet)),
        ]:
            if worksheet is None and stage_name == "sinh_huong_dan_slide":
                report.add(stage_name, ok=False, error="Bỏ qua: Phiếu học tập chưa sinh được nên không có outline để bám theo.")
                continue
            try:
                path = fn()
                report.add(stage_name, ok=True, artifact_path=path)
            except Exception as exc:  # noqa: BLE001
                report.add(stage_name, ok=False, error=str(exc))

        try:
            homework, warnings = stages.generate_homework_content(client, self.identity, architect)
            path = stages.write_homework_markdown(homework, lesson, md_dir)
            report.add("sinh_bai_tap_ve_nha", ok=True, artifact_path=path, warnings=warnings)
        except Exception as exc:  # noqa: BLE001
            report.add("sinh_bai_tap_ve_nha", ok=False, error=str(exc))

        self._compile_docx(lesson, md_dir, ready_dir, report)
        self._self_correct(client, lesson, md_dir, report)
        self._write_metadata(lesson, output_dir, ready_dir, report)
        return report

    def offline(self, lesson_key: str) -> RunReport:
        """Chạy hết pipeline (trừ NotebookLM) bằng dữ liệu mẫu, không cần
        GEMINI_API_KEY hay mạng — đường kiểm thử/demo nhanh."""
        lesson = self.resolve_lesson(lesson_key)
        output_dir, md_dir, ready_dir = self._lesson_dirs(lesson)
        report = RunReport(lesson_slug=lesson.slug)

        architect = fixtures.build_architect(lesson)
        spec_path = stages.write_architect_markdown(architect, lesson, md_dir)
        stages.write_lesson_matrix_json(architect, md_dir)
        report.add("phan_tich_yccd", ok=True, artifact_path=spec_path, detail="offline fixture")

        worksheet = fixtures.build_worksheet(architect)
        homework = fixtures.build_homework(architect)
        plan = fixtures.build_lesson_plan(architect)

        report.add("sinh_phieu_hoc_tap", ok=True,
                    artifact_path=stages.write_worksheet_markdown(worksheet, lesson, md_dir), detail="offline fixture")
        stages.write_worksheet_json(worksheet, md_dir)
        report.add("sinh_bai_tap_ve_nha", ok=True,
                    artifact_path=stages.write_homework_markdown(homework, lesson, md_dir), detail="offline fixture")
        report.add("sinh_ke_hoach_bai_day", ok=True,
                    artifact_path=stages.write_lesson_plan_markdown(plan, lesson, md_dir, self.identity),
                    detail="offline fixture")
        report.add("sinh_huong_dan_slide", ok=True,
                    artifact_path=stages.write_slide_guide_markdown(self.identity, lesson, md_dir, architect, worksheet),
                    detail="offline fixture")

        self._compile_docx(lesson, md_dir, ready_dir, report)
        self._write_metadata(lesson, output_dir, ready_dir, report)
        return report

    def compose(self, lesson_key: str, content_dir: str | Path | None = None) -> RunReport:
        """Nhận nội dung do chính AI agent đang trò chuyện (vd. Claude chạy
        trong Antigravity IDE) trực tiếp soạn — thay cho việc gọi Gemini API
        bằng GEMINI_API_KEY. Agent tự viết 4 file JSON khớp đúng schema
        Pydantic (`gems/models/*.py`) vào `content_dir` TRƯỚC khi gọi lệnh
        này: `{slug}_architect.json`, `_worksheet.json`, `_homework.json`,
        `_lesson_plan.json`. Mặc định `content_dir` là `output/<slug>/authored/`.
        """
        lesson = self.resolve_lesson(lesson_key)
        output_dir, md_dir, ready_dir = self._lesson_dirs(lesson)
        report = RunReport(lesson_slug=lesson.slug)
        content_dir = Path(content_dir) if content_dir else output_dir / "authored"

        try:
            architect = from_json.load_architect(content_dir / f"{lesson.slug}_architect.json")
            spec_path = stages.write_architect_markdown(architect, lesson, md_dir)
            stages.write_lesson_matrix_json(architect, md_dir)
            report.add("phan_tich_yccd", ok=True, artifact_path=spec_path, detail="do AI agent soạn")
        except Exception as exc:  # noqa: BLE001
            report.add("phan_tich_yccd", ok=False, error=str(exc))
            return report  # không có đặc tả thì không thể tiếp tục các bước sau

        worksheet = None
        try:
            worksheet = from_json.load_worksheet(content_dir / f"{lesson.slug}_worksheet.json")
            path = stages.write_worksheet_markdown(worksheet, lesson, md_dir)
            stages.write_worksheet_json(worksheet, md_dir)
            report.add("sinh_phieu_hoc_tap", ok=True, artifact_path=path, detail="do AI agent soạn")
        except Exception as exc:  # noqa: BLE001
            report.add("sinh_phieu_hoc_tap", ok=False, error=str(exc))

        try:
            homework = from_json.load_homework(content_dir / f"{lesson.slug}_homework.json")
            warnings = []
            if homework.question_counts != (18, 4, 6):
                warnings.append(f"Số câu {homework.question_counts} không khớp chuẩn (18, 4, 6) — vẫn xuất file.")
            path = stages.write_homework_markdown(homework, lesson, md_dir)
            report.add("sinh_bai_tap_ve_nha", ok=True, artifact_path=path, detail="do AI agent soạn", warnings=warnings)
        except Exception as exc:  # noqa: BLE001
            report.add("sinh_bai_tap_ve_nha", ok=False, error=str(exc))

        try:
            plan = from_json.load_lesson_plan(content_dir / f"{lesson.slug}_lesson_plan.json")
            path = stages.write_lesson_plan_markdown(plan, lesson, md_dir, self.identity)
            report.add("sinh_ke_hoach_bai_day", ok=True, artifact_path=path, detail="do AI agent soạn")
        except Exception as exc:  # noqa: BLE001
            report.add("sinh_ke_hoach_bai_day", ok=False, error=str(exc))

        if worksheet is None:
            report.add("sinh_huong_dan_slide", ok=False, error="Bỏ qua: Phiếu học tập chưa nạp được nên không có outline để bám theo.")
        else:
            try:
                path = stages.write_slide_guide_markdown(self.identity, lesson, md_dir, architect, worksheet)
                report.add("sinh_huong_dan_slide", ok=True, artifact_path=path)
            except Exception as exc:  # noqa: BLE001
                report.add("sinh_huong_dan_slide", ok=False, error=str(exc))

        self._compile_docx(lesson, md_dir, ready_dir, report)
        self._write_metadata(lesson, output_dir, ready_dir, report)
        return report

    def lint(self, lesson_key: str) -> RunReport:
        """Chỉ kiểm định chất lượng — không sinh lại học liệu."""
        from gems.qa.docx_lint import lint_docx_margins, lint_khbd_docx

        lesson = self.resolve_lesson(lesson_key)
        _, _, ready_dir = self._lesson_dirs(lesson)
        report = RunReport(lesson_slug=lesson.slug)

        khbd_path = ready_dir / f"{lesson.slug}_ke_hoach_bai_day.docx"
        if khbd_path.exists():
            r = lint_khbd_docx(khbd_path)
            report.add("lint_khbd", ok=r.passed, warnings=r.issues)

        for doc_type, suffix in [("pht", "phieu_hoc_tap"), ("homework", "bai_tap_ve_nha")]:
            path = ready_dir / f"{lesson.slug}_{suffix}.docx"
            if path.exists():
                r = lint_docx_margins(path, doc_type)
                report.add(f"lint_{suffix}", ok=r.passed, warnings=r.issues)

        return report
