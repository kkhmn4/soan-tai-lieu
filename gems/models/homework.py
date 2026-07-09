"""Schema Giai đoạn 3: Bài tập về nhà.

Số lượng câu đúng 18/4/6 KHÔNG được ép bằng Pydantic validator (sẽ làm
mất nguyên request Gemini nếu model trả thiếu 1 câu, không có đường sửa) —
thay vào đó `generation/stages.py` kiểm tra số lượng sau khi sinh và tự
retry có giới hạn, sai thì ghi cảnh báo vào RunReport chứ không âm thầm bỏ qua.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class Part1Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trắc nghiệm một lựa chọn.")
    option_a: str = Field(description="Phương án A")
    option_b: str = Field(description="Phương án B")
    option_c: str = Field(description="Phương án C")
    option_d: str = Field(description="Phương án D")
    correct_option: str = Field(description="Đáp án đúng (A, B, C, hoặc D)")
    explanation: str = Field(description="Giải thích lý do chọn đáp án")
    shared_context: str | None = Field(
        default=None,
        description=(
            "Dữ kiện/đoạn văn dùng chung cho câu này và (các) câu liền sau có cùng "
            "giá trị shared_context — khớp mẫu 'Nội dung câu X và Y: ...' trong đề "
            "thi tốt nghiệp THPT thật. Để trống nếu câu không thuộc nhóm dùng chung dữ kiện."
        ),
    )


class Part2Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trắc nghiệm Đúng/Sai.")
    statement_a: str = Field(description="Mệnh đề a")
    statement_b: str = Field(description="Mệnh đề b")
    statement_c: str = Field(description="Mệnh đề c")
    statement_d: str = Field(description="Mệnh đề d")
    correct_a: bool = Field(description="Đúng hay Sai")
    correct_b: bool = Field(description="Đúng hay Sai")
    correct_c: bool = Field(description="Đúng hay Sai")
    correct_d: bool = Field(description="Đúng hay Sai")
    explanation: str = Field(description="Giải thích chi tiết cho từng mệnh đề")


class Part3Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trả lời ngắn.")
    correct_answer: str = Field(description="Kết quả số")
    unit: str = Field(description="Đơn vị vật lý")
    explanation: str = Field(description="Lời giải chi tiết")
    shared_context: str | None = Field(
        default=None, description="Dữ kiện dùng chung cho câu này và (các) câu liền sau, xem Part1Question.shared_context.",
    )


class HomeworkContent(BaseModel):
    lesson_name: str
    part1_questions: list[Part1Question] = Field(description="Đúng 18 câu trắc nghiệm nhiều lựa chọn.")
    part2_questions: list[Part2Question] = Field(description="Đúng 4 câu Đúng/Sai.")
    part3_questions: list[Part3Question] = Field(description="Đúng 6 câu trả lời ngắn.")
    shared_constants: str | None = Field(
        default=None,
        description=(
            "Khối hằng số vật lí dùng chung, in ngay dưới phần thông tin thí sinh — "
            "khớp dòng '+ Cho biết: ...' trong đề thi tốt nghiệp THPT thật. "
            "Để trống nếu đề không cần hằng số dùng chung."
        ),
    )

    @property
    def question_counts(self) -> tuple[int, int, int]:
        return len(self.part1_questions), len(self.part2_questions), len(self.part3_questions)
