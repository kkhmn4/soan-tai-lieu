"""Vòng lặp tự kiểm duyệt + tự sửa lỗi Markdown bằng Gemini.

Chỉ quét những lỗi xác định được bằng regex thuần (`gems.qa.markdown_lint`)
rồi nhờ Gemini sửa lại toàn bộ file — KHÔNG phải hệ thống 4 lớp AI-vision/
giải lại toán-lý/kiểm PPTX như `quality_checker.py` (bản cũ) từng mô tả
trong tài liệu (module đó thực ra hỏng cú pháp, chưa từng chạy được).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from gems.generation.gemini_client import GeminiClient
from gems.prompts import self_correction as prompts
from gems.qa.markdown_lint import lint_markdown

MAX_ATTEMPTS = 3


@dataclass
class CorrectionResult:
    file_name: str
    issues_found: list[str] = field(default_factory=list)
    fixed: bool = False
    attempts: int = 0
    error: str | None = None


def correct_markdown_file(client: GeminiClient, identity, md_file: Path, *, is_lesson_plan: bool = False,
                           max_attempts: int = MAX_ATTEMPTS) -> CorrectionResult:
    result = CorrectionResult(file_name=md_file.name)
    for attempt in range(1, max_attempts + 1):
        result.attempts = attempt
        content = md_file.read_text(encoding="utf-8")
        issues = lint_markdown(content, is_lesson_plan=is_lesson_plan)
        if not issues:
            result.fixed = True
            return result

        result.issues_found = issues
        if not client.is_online:
            result.error = "Không có GEMINI_API_KEY — cần người dùng tự sửa thủ công."
            return result

        try:
            fixed_content = client.generate_text(
                model=identity.gemini_model_content,
                system_instruction=prompts.SYSTEM_INSTRUCTION,
                prompt=prompts.build_prompt(content, issues),
                temperature=0.1,
            )
            md_file.write_text(fixed_content, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001 — ghi lại lỗi thật, không nuốt im lặng
            result.error = str(exc)
            return result

    result.error = f"Vẫn còn lỗi sau {max_attempts} lần thử: {result.issues_found}"
    return result
