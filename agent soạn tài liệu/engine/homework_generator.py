# engine/homework_generator.py
"""
HomeworkGenerator — Sinh đề bài tập về nhà bằng Gemini API (Structured Outputs).
"""

import os
import json
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# --- Định nghĩa các Schema Pydantic cho Structured Outputs ---
class Part1Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trắc nghiệm một lựa chọn.")
    option_a: str = Field(description="Phương án A")
    option_b: str = Field(description="Phương án B")
    option_c: str = Field(description="Phương án C")
    option_d: str = Field(description="Phương án D")
    correct_option: str = Field(description="Phương án đúng (A, B, C, hoặc D)")
    explanation: str = Field(description="Giải thích lí do chọn đáp án")

class Part2Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trắc nghiệm Đúng/Sai.")
    statement_a: str = Field(description="Mệnh đề a")
    statement_b: str = Field(description="Mệnh đề b")
    statement_c: str = Field(description="Mệnh đề c")
    statement_d: str = Field(description="Mệnh đề d")
    correct_a: bool = Field(description="Mệnh đề a đúng hay sai")
    correct_b: bool = Field(description="Mệnh đề b đúng hay sai")
    correct_c: bool = Field(description="Mệnh đề c đúng hay sai")
    correct_d: bool = Field(description="Mệnh đề d đúng hay sai")
    explanation: str = Field(description="Giải thích chi tiết cho từng mệnh đề")

class Part3Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trả lời ngắn.")
    correct_answer: str = Field(description="Kết quả số")
    unit: str = Field(description="Đơn vị vật lý")
    explanation: str = Field(description="Lời giải chi tiết")

class HomeworkContent(BaseModel):
    lesson_name: str
    part1_questions: list[Part1Question] = Field(description="Đúng 18 câu trắc nghiệm nhiều lựa chọn.")
    part2_questions: list[Part2Question] = Field(description="Đúng 4 câu Đúng/Sai.")
    part3_questions: list[Part3Question] = Field(description="Đúng 6 câu trả lời ngắn.")

class HomeworkGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("[GEMS] Không tìm thấy GEMINI_API_KEY trong file .env!")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    def generate_homework(self, matrix_data: dict, pedagogical_data: dict = None) -> HomeworkContent:
        """Sinh hệ thống câu hỏi bài tập về nhà từ ma trận và phân tích sư phạm."""
        print(f"[PROCESS] Đang sinh đề bài tập về nhà cho: '{matrix_data.get('lesson_name')}'...")
        
        prompt = (
            f"Dựa vào Ma trận bài học: {json.dumps(matrix_data, ensure_ascii=False)}\n"
            f"Và phân tích sư phạm (lỗi sai cần bẫy): {json.dumps(pedagogical_data, ensure_ascii=False) if pedagogical_data else ''}\n"
            f"Hãy sinh hệ thống bài tập về nhà theo đúng cấu trúc Bộ GD&ĐT 2025:\n"
            f"- Phần I: 18 câu trắc nghiệm nhiều lựa chọn.\n"
            f"- Phần II: 4 câu Đúng/Sai.\n"
            f"- Phần III: 6 câu trả lời ngắn.\n"
            f"Lưu ý: 50% câu hỏi phải có bối cảnh thực tế."
        )
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=HomeworkContent,
                system_instruction=(
                    "Bạn là một chuyên gia ra đề thi Vật lý THPT Quốc gia theo chương trình mới tại Việt Nam. "
                    "Hãy tạo ra đề bài tập về nhà thuần Việt 100%, chất lượng khoa học cực kỳ cao, gài bẫy logic "
                    "các quan niệm sai lầm."
                ),
                temperature=0.3,
            )
        )
        
        data = json.loads(response.text)
        return HomeworkContent(**data)

    def generate(self, matrix, output_dir: str):
        """Phương thức tương thích ngược với main.py cũ để sinh file markdown."""
        matrix_data = matrix.model_dump() if hasattr(matrix, "model_dump") else matrix
        homework = self.generate_homework(matrix_data)
        
        slug = output_dir.split("/")[-1] if "/" in output_dir else output_dir.split("\\")[-1]
        hw_path = os.path.join(output_dir, "md", f"{slug}_bai_tap_ve_nha.md")
        
        with open(hw_path, "w", encoding="utf-8") as f:
            f.write(f"# BÀI TẬP VỀ NHÀ: {homework.lesson_name.upper()}\n\n")
            f.write("## PHẦN I: CÂU HỎI TRẮC NGHIỆM NHIỀU LỰA CHỌN (18 câu)\n")
            f.write("*Mỗi câu hỏi chỉ chọn một phương án trả lời đúng.*\n\n")
            for idx, q in enumerate(homework.part1_questions, 1):
                f.write(f"**Câu {idx}:** {q.question_text}\n")
                f.write(f"A. {q.option_a}\n")
                f.write(f"B. {q.option_b}\n")
                f.write(f"C. {q.option_c}\n")
                f.write(f"D. {q.option_d}\n\n")
            
            f.write("\n## PHẦN II: CÂU HỎI TRẮC NGHIỆM ĐÚNG/SAI (4 câu)\n")
            f.write("*Trong mỗi câu hỏi, thí sinh chọn Đúng hoặc Sai cho mỗi mệnh đề a), b), c), d).*\n\n")
            for idx, q in enumerate(homework.part2_questions, 1):
                f.write(f"**Câu {idx}:** {q.question_text}\n")
                f.write(f"a) {q.statement_a} (Đ/S: {'Đ' if q.correct_a else 'S'})\n")
                f.write(f"b) {q.statement_b} (Đ/S: {'Đ' if q.correct_b else 'S'})\n")
                f.write(f"c) {q.statement_c} (Đ/S: {'Đ' if q.correct_c else 'S'})\n")
                f.write(f"d) {q.statement_d} (Đ/S: {'Đ' if q.correct_d else 'S'})\n\n")
            
            f.write("\n## PHẦN III: CÂU HỎI TRẢ LỜI NGẮN (6 câu)\n")
            f.write("*Thí sinh điền kết quả số vào ô trống tương ứng.*\n\n")
            for idx, q in enumerate(homework.part3_questions, 1):
                f.write(f"**Câu {idx}:** {q.question_text}\n")
                f.write(f"Đáp án: {q.correct_answer} {q.unit}\n\n")
                
            f.write("\n---\n## HƯỚNG DẪN GIẢI CHI TIẾT VÀ ĐÁP ÁN\n\n")
            f.write("### PHẦN I:\n")
            for idx, q in enumerate(homework.part1_questions, 1):
                f.write(f"- **Câu {idx} (Chọn {q.correct_option}):** {q.explanation}\n")
            f.write("\n### PHẦN II:\n")
            for idx, q in enumerate(homework.part2_questions, 1):
                f.write(f"- **Câu {idx}:** {q.explanation}\n")
            f.write("\n### PHẦN III:\n")
            for idx, q in enumerate(homework.part3_questions, 1):
                f.write(f"- **Câu {idx} ({q.correct_answer} {q.unit}):** {q.explanation}\n")
        print(f"  + Đã lưu file Bài tập về nhà MD: {hw_path}")