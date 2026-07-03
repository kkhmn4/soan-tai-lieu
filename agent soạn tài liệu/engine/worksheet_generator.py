# engine/worksheet_generator.py
"""
WorksheetGenerator — Sinh nội dung Phiếu học tập chi tiết bằng Gemini API.
"""

import os
import json
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from templates.prompts import SYSTEM_WORKSHEET_GENERATION_PROMPT

# --- Định nghĩa các Schema Pydantic cho Structured Outputs ---
class TaskContent(BaseModel):
    task_id: str = Field(description="Mã nhiệm vụ (ví dụ: NV1...)")
    task_type: str = Field(description="Loại nhiệm vụ")
    task_name: str = Field(description="Tên nhiệm vụ")
    content: str = Field(description="Nội dung câu hỏi hoặc bối cảnh nhiệm vụ cụ thể.")

class DiscoverySection(BaseModel):
    tasks: list[TaskContent] = Field(description="Danh sách các nhiệm vụ khám phá")

class CoreTheorySection(BaseModel):
    summary_cloze: str = Field(description="Đoạn văn tóm tắt lý thuyết đục lỗ điền khuyết sử dụng các số thứ tự (1), (2)...")
    key_words: list[str] = Field(description="Danh sách đáp án từ khóa tương ứng")

class ApplicationSection(BaseModel):
    scenario: str = Field(description="Tình huống thực tế đời sống mới và thử thách tính toán/lập luận vật lý")

class ExtensionSection(BaseModel):
    reading_content: str = Field(description="Nội dung đọc hiểu mở rộng, kết nối STEM hoặc hướng nghiệp")

class UnitWorksheetContent(BaseModel):
    unit_id: str = Field(description="Mã đơn vị kiến thức")
    unit_name: str = Field(description="Tên đơn vị kiến thức")
    discovery: DiscoverySection
    core_theory: CoreTheorySection
    application: ApplicationSection
    extension: ExtensionSection

class LessonWorksheet(BaseModel):
    lesson_name: str
    units: list[UnitWorksheetContent]

class WorksheetGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("[GEMS] Không tìm thấy GEMINI_API_KEY trong file .env!")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"  # Sử dụng Flash để sinh nhanh nội dung chi tiết

    def generate_content(self, matrix_data: dict) -> LessonWorksheet:
        """Gọi Gemini API để sinh nội dung chi tiết cho phiếu học tập dựa trên ma trận bài học."""
        print(f"[PROCESS] Đang sinh nội dung chi tiết cho phiếu học tập: '{matrix_data.get('lesson_name')}'...")
        
        matrix_json = json.dumps(matrix_data, ensure_ascii=False)
        prompt = f"Hãy sinh nội dung phiếu học tập chi tiết cho ma trận bài học sau:\n{matrix_json}"
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LessonWorksheet,
                system_instruction=SYSTEM_WORKSHEET_GENERATION_PROMPT,
                temperature=0.3,
            )
        )
        
        data = json.loads(response.text)
        return LessonWorksheet(**data)

    def generate(self, matrix, output_dir: str):
        """Phương thức tương thích ngược với main.py cũ để sinh file markdown."""
        matrix_data = matrix.model_dump() if hasattr(matrix, "model_dump") else matrix
        worksheet = self.generate_content(matrix_data)
        
        slug = output_dir.split("/")[-1] if "/" in output_dir else output_dir.split("\\")[-1]
        pht_path = os.path.join(output_dir, "md", f"{slug}_phieu_hoc_tap.md")
        
        with open(pht_path, "w", encoding="utf-8") as f:
            f.write(f"# PHIẾU HỌC TẬP: {worksheet.lesson_name.upper()}\n")
            f.write("**Họ và tên học sinh:** ....................................................  \n")
            f.write("**Lớp:** .................. **Ngày:** ......./......./.......  \n\n---\n\n")
            for u in worksheet.units:
                f.write(f"## 📍 {u.unit_id.upper()}: {u.unit_name.upper()}\n\n")
                f.write("### 1. Khám phá\n")
                for t in u.discovery.tasks:
                    f.write(f"**Nhiệm vụ: {t.task_name} ({t.task_type})**\n")
                    f.write(f"{t.content}\n\n")
                    f.write("[DOT_LINE_90]\n[DOT_LINE_90]\n[DOT_LINE_90]\n\n")
                
                f.write("### 2. Trọng tâm\n")
                f.write(f"{u.core_theory.summary_cloze}\n\n")
                f.write(f"*Gợi ý từ khóa:* {', '.join(u.core_theory.key_words)}.\n\n")
                
                f.write("### 3. Vận dụng\n")
                f.write(f"**Tình huống thực tế:** {u.application.scenario}\n\n")
                f.write("[DOT_LINE_90]\n[DOT_LINE_90]\n\n")
                
                f.write("### 4. Mở rộng (STEM Connection)\n")
                f.write(f"> {u.extension.reading_content}\n\n---\n\n")
        print(f"  + Đã lưu file Phiếu học tập MD: {pht_path}")