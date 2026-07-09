"""Kiểm tra chất lượng Markdown bằng regex thuần (không gọi AI).

3 kiểm tra này vốn nằm bên trong `gems_agent.py::tool_self_correction_loop`
(bản cũ) — tách ra thành pure function độc lập để test trực tiếp, không
phải giả lập cả 1 vòng lặp gọi Gemini mới kiểm tra được logic phát hiện lỗi.
"""
from __future__ import annotations

_RAW_LATEX_SYMBOLS = ["\\Delta", "\\omega", "\\varphi", "\\pi", "\\cos", "\\sin"]
_CV5512_REQUIRED_KEYWORDS = ["Chuyển giao nhiệm vụ:", "Thực hiện nhiệm vụ:", "Báo cáo, thảo luận:", "Kết luận:"]
_KHBD_REQUIRED_SECTIONS = ["c) Sản phẩm:", "Kĩ thuật dạy học tích cực:", "Năng lực số"]


def check_raw_bullets(content: str) -> str | None:
    if "•" in content:
        return ("Phát hiện ký tự bullet thô '•' (U+2022). GEMS quy định không sử dụng bullet thô "
                "làm ký tự văn bản, phải thay thế bằng dấu gạch ngang '-' hoặc dấu cộng '+'.")
    return None


def check_raw_latex(content: str) -> str | None:
    if "\\" in content and any(sym in content for sym in _RAW_LATEX_SYMBOLS):
        return "Phát hiện các từ khóa LaTeX chưa được dịch sang Unicode (ví dụ: \\Delta, \\omega...). Hãy dịch sang ký tự Unicode tương ứng (Δ, ω...)."
    return None


def check_cv5512_keywords(content: str) -> str | None:
    missing = [kw for kw in _CV5512_REQUIRED_KEYWORDS if kw.lower() not in content.lower()]
    if missing:
        return f"Giáo án CV5512 thiếu các từ khóa hoạt động bắt buộc: {', '.join(missing)}."
    return None


def check_khbd_integrated_sections(content: str) -> str | None:
    missing = [item for item in _KHBD_REQUIRED_SECTIONS if item.lower() not in content.lower()]
    if missing:
        return f"KHBD thiếu cấu phần mẫu/tích hợp bắt buộc: {', '.join(missing)}."
    return None


def lint_markdown(content: str, *, is_lesson_plan: bool = False) -> list[str]:
    checks = [check_raw_bullets(content), check_raw_latex(content)]
    if is_lesson_plan:
        checks.append(check_cv5512_keywords(content))
        checks.append(check_khbd_integrated_sections(content))
    return [issue for issue in checks if issue]
