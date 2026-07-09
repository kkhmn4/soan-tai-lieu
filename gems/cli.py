"""CLI GEMS — 1 điểm vào duy nhất thay thế 2 cách chạy tách rời của bản cũ
(`python engine/gems_agent.py --prompt "..."` chỉ làm markdown+docx, và
`python scratch/generate_notebook_materials.py --lesson "Bài N"` chạy
riêng phần NotebookLM — người dùng phải nhớ chạy đủ cả 2 lệnh).

Dùng: python -m gems <generate|notebooklm|full|offline|lint|list-lessons> --lesson bai4
      hoặc: python -m gems generate --prompt "soạn bài 4 nhiệt dung riêng"
"""
from __future__ import annotations

import argparse
import sys

# Console Windows mặc định dùng cp1252, không encode được tiếng Việt — trước
# đây mỗi file tự xử lý việc này theo 3 cách khác nhau (io.TextIOWrapper,
# reconfigure, mở lại sys.stdout thủ công). Xử lý đúng 1 lần, đúng 1 chỗ ở
# đây — mọi lệnh `python -m gems ...` đều đi qua module này.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

from gems.pipeline.orchestrator import GEMSPipeline, LessonNotFoundError  # noqa: E402
from gems.pipeline.report import RunReport  # noqa: E402


def _lesson_arg(args: argparse.Namespace) -> str:
    if args.lesson:
        return args.lesson
    if args.prompt:
        return args.prompt
    raise SystemExit("Cần chỉ định --lesson bai4 hoặc --prompt \"soạn bài 4 ...\".")


def _print_report(report: RunReport) -> int:
    for line in report.summary_lines():
        print(line)
    return 0 if report.ok else 1


def cmd_list_lessons(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    for key, lesson in sorted(pipeline.curriculum.lessons.items()):
        print(f"{key}: {lesson.name} (slug={lesson.slug})")
    return 0


def cmd_generate(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    report = pipeline.generate(_lesson_arg(args))
    return _print_report(report)


def cmd_offline(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    report = pipeline.offline(_lesson_arg(args))
    return _print_report(report)


def cmd_compose(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    report = pipeline.compose(_lesson_arg(args), content_dir=args.content_dir)
    return _print_report(report)


def cmd_lint(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    report = pipeline.lint(_lesson_arg(args))
    return _print_report(report)


def cmd_notebooklm(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    from gems.notebooklm.pipeline import run_notebooklm_stage

    lesson = pipeline.resolve_lesson(_lesson_arg(args))
    output_dir, _, _ = pipeline.get_lesson_dirs(lesson)
    report = RunReport(lesson_slug=lesson.slug)
    run_notebooklm_stage(pipeline.identity, lesson, output_dir, report, notebook_id=args.notebook_id,
                          profile=args.profile)
    return _print_report(report)


def cmd_full(pipeline: GEMSPipeline, args: argparse.Namespace) -> int:
    # Có --content-dir (nội dung do AI agent tự soạn) thì dùng compose, không
    # cần GEMINI_API_KEY; ngược lại gọi Gemini thật qua generate.
    exit_code = cmd_compose(pipeline, args) if args.content_dir else cmd_generate(pipeline, args)
    exit_code = max(exit_code, cmd_notebooklm(pipeline, args))
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gems", description="GEMS — Agent soạn học liệu Vật lý 12")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_lesson_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("--lesson", type=str, help="Mã bài học, ví dụ bai4")
        p.add_argument("--prompt", type=str, help="Yêu cầu tự nhiên ngữ, ví dụ 'soạn bài 4 nhiệt dung riêng'")

    p_generate = sub.add_parser("generate", help="Sinh học liệu bằng Gemini (Markdown + DOCX)")
    add_lesson_args(p_generate)
    p_generate.set_defaults(func=cmd_generate)

    p_offline = sub.add_parser("offline", help="Chạy thử toàn bộ pipeline bằng fixture, không cần API/mạng")
    add_lesson_args(p_offline)
    p_offline.set_defaults(func=cmd_offline)

    p_compose = sub.add_parser(
        "compose",
        help="Dựng Markdown+DOCX từ nội dung do AI agent tự soạn (JSON khớp schema), không cần GEMINI_API_KEY",
    )
    add_lesson_args(p_compose)
    p_compose.add_argument("--content-dir", type=str, default=None,
                            help="Thư mục chứa {slug}_architect.json/_worksheet.json/_homework.json/_lesson_plan.json "
                                 "(mặc định: output/<slug>/authored/)")
    p_compose.set_defaults(func=cmd_compose)

    p_lint = sub.add_parser("lint", help="Kiểm định chất lượng DOCX đã có sẵn trong ready/")
    add_lesson_args(p_lint)
    p_lint.set_defaults(func=cmd_lint)

    p_nlm = sub.add_parser("notebooklm", help="Chạy giai đoạn NotebookLM (2 bộ Slide: Giáo viên + Phiếu học tập)")
    add_lesson_args(p_nlm)
    p_nlm.add_argument("--notebook-id", type=str, default=None)
    p_nlm.add_argument("--profile", type=str, default=None, help="Tên profile nlm CLI (vd. account2)")
    p_nlm.set_defaults(func=cmd_notebooklm)

    p_full = sub.add_parser("full", help="Chạy generate (hoặc compose nếu có --content-dir) + notebooklm liên tiếp")
    add_lesson_args(p_full)
    p_full.add_argument("--content-dir", type=str, default=None,
                         help="Nếu chỉ định: dùng nội dung AI agent tự soạn (compose) thay vì gọi Gemini (generate)")
    p_full.add_argument("--notebook-id", type=str, default=None)
    p_full.add_argument("--profile", type=str, default=None)
    p_full.set_defaults(func=cmd_full)

    p_list = sub.add_parser("list-lessons", help="Liệt kê toàn bộ bài học trong curriculum.yaml")
    p_list.set_defaults(func=cmd_list_lessons)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    pipeline = GEMSPipeline()
    try:
        return args.func(pipeline, args)
    except LessonNotFoundError as exc:
        print(f"Lỗi: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
