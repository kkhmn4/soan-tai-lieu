SYSTEM_INSTRUCTION = (
    "Bạn là một trợ lý chỉnh sửa học liệu có nhiệm vụ sửa đổi và tối ưu hóa tệp Markdown nguồn theo báo cáo lỗi.\n"
    "Hãy giữ nguyên cấu trúc và nội dung gốc, chỉ tập trung khắc phục triệt để các lỗi được liệt kê.\n"
    "Ngôn ngữ đầu ra phải là tiếng Việt chuẩn mực."
)


def build_prompt(content: str, issues: list[str]) -> str:
    prompt = f"Dưới đây là tệp Markdown học liệu Vật lý:\n\n```markdown\n{content}\n```\n\nHãy sửa đổi tệp này để khắc phục các lỗi chất lượng sau:\n"
    for idx, issue in enumerate(issues, 1):
        prompt += f"{idx}. {issue}\n"
    prompt += "\nTrả về tệp Markdown hoàn chỉnh sau khi đã được sửa sạch lỗi."
    return prompt
