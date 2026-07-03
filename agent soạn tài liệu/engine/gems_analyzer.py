# engine/gems_analyzer.py
"""
GEMSAnalyzer — Phân tích sư phạm và lập ma trận bài học tự động (GEMS v7.1).
"""

import os
import json
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from templates.prompts import SYSTEM_PEDAGOGICAL_PROMPT, SYSTEM_MATRIX_PROMPT

# --- Định nghĩa các Schema Pydantic cho Structured Outputs ---
class MisconceptionItem(BaseModel):
    misconception: str = Field(description="Mô tả quan niệm sai lầm phổ biến của học sinh")
    correct_concept: str = Field(description="Bản chất vật lý đúng đắn")
    explanation: str = Field(description="Giải thích sư phạm để sửa sai")

class PedagogicalAnalysis(BaseModel):
    key_concepts: list[str] = Field(description="Các kiến thức cốt lõi của bài học")
    misconceptions: list[MisconceptionItem] = Field(description="Danh sách các bẫy sai lầm")
    teaching_methods: list[str] = Field(description="Phương pháp dạy học đề xuất")

class TaskItem(BaseModel):
    task_id: str = Field(description="Mã nhiệm vụ (ví dụ: NV1, NV2...)")
    task_type: str = Field(description="Loại nhiệm vụ (ví dụ: Matching Matrix, Bug Buster...)")
    task_name: str = Field(description="Tên nhiệm vụ")
    description: str = Field(description="Mô tả chi tiết yêu cầu nhiệm vụ")
    context_real: str = Field(description="Bối cảnh thực tế đời sống liên quan")

class KnowledgeUnit(BaseModel):
    unit_id: str = Field(description="Mã đơn vị kiến thức")
    unit_name: str = Field(description="Tên đơn vị kiến thức")
    concepts: list[str] = Field(description="Khái niệm chính")
    tasks: list[TaskItem] = Field(description="Chuỗi nhiệm vụ học tập")

class LessonMatrix(BaseModel):
    lesson_name: str = Field(description="Tên bài học tổng quát")
    units: list[KnowledgeUnit] = Field(description="Danh sách các đơn vị kiến thức")

class GEMSArchitect(BaseModel):
    analysis: PedagogicalAnalysis = Field(description="Phân tích sư phạm chi tiết từ YCCĐ")
    matrix: LessonMatrix = Field(description="Ma trận bài học và các nhiệm vụ")

class GEMSAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("[GEMS] Không tìm thấy GEMINI_API_KEY trong file .env! Vui lòng cấu hình API key trước khi chạy.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-pro"  # Sử dụng model Pro cho tính toán khoa học chính xác

    def generate_architect(self, yccd: str) -> GEMSArchitect:
        """Gộp Bước 1 & Bước 2: Phân tích sư phạm và sinh Ma trận trong 1 lượt gọi API duy nhất."""
        print(f"[PROCESS] [GEMS v7.1] Đang sinh Spec và Ma trận đồng thời cho YCCĐ: '{yccd[:50]}...'")
        
        system_instruction = (
            "Bạn là Chuyên gia Giáo dục môn Vật lý và Thiết kế học liệu hàng đầu theo chương trình GDPT 2018 tại Việt Nam.\n"
            "Hãy thực hiện phân tích sư phạm chi tiết và lập ma trận bài học đồng bộ trong định dạng JSON có cấu trúc.\n\n"
            f"--- QUY TẮC PHÂN TÍCH SƯ PHẠM ---\n{SYSTEM_PEDAGOGICAL_PROMPT}\n\n"
            f"--- QUY TẮC THIẾT LẬP MA TRẬN ---\n{SYSTEM_MATRIX_PROMPT}"
        )
        
        prompt = f"Hãy thực hiện phân tích sư phạm và xây dựng ma trận cho YCCĐ sau:\n{yccd}"
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GEMSArchitect,
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        
        data = json.loads(response.text)
        return GEMSArchitect(**data)

    def analyze(self, yccd: str) -> LessonMatrix:
        """Phương thức tương thích ngược với main.py cũ để lấy ma trận bài học."""
        architect = self.generate_architect(yccd)
        return architect.matrix

    def save_to_docs(self, analysis: PedagogicalAnalysis, matrix: LessonMatrix, output_dir: str = "docs"):
        """Lưu trữ kết quả phân tích sư phạm và ma trận bài học ra file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 1. Lưu ma trận JSON
        matrix_path = os.path.join(output_dir, "lesson_matrix.json")
        with open(matrix_path, "w", encoding="utf-8") as f:
            json.dump(matrix.model_dump(), f, ensure_ascii=False, indent=2)
        print(f"  + Đã lưu file ma trận: {matrix_path}")
        
        # 2. Lưu tài liệu phân tích sư phạm dạng Markdown
        analysis_path = os.path.join(output_dir, "pedagogical_analysis.md")
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write(f"# PHÂN TÍCH SƯ PHẠM VÀ MA TRẬN BÀI HỌC: {matrix.lesson_name}\n\n")
            f.write("## 1. Kiến thức cốt lõi\n")
            for concept in analysis.key_concepts:
                f.write(f"- {concept}\n")
            f.write("\n")
            
            f.write("## 2. Các lỗi sai thường gặp (Misconceptions)\n")
            for idx, item in enumerate(analysis.misconceptions, 1):
                f.write(f"### Lỗi {idx}: {item.misconception}\n")
                f.write(f"- **Bản chất vật lý đúng:** {item.correct_concept}\n")
                f.write(f"- **Giải thích sư phạm:** {item.explanation}\n\n")
                
            f.write("## 3. Phương pháp dạy học đề xuất\n")
            for method in analysis.teaching_methods:
                f.write(f"- {method}\n")
            f.write("\n")
            
            f.write("## 4. Ma trận phân chia nhiệm vụ học tập\n")
            for unit in matrix.units:
                f.write(f"### [{unit.unit_id}] {unit.unit_name}\n")
                f.write(f"- **Khái niệm chính:** {', '.join(unit.concepts)}\n")
                f.write("- **Chuỗi nhiệm vụ:**\n")
                for task in unit.tasks:
                    f.write(f"  - **{task.task_id} ({task.task_type}) - {task.task_name}**\n")
                    f.write(f"    - *Mô tả:* {task.description}\n")
                    f.write(f"    - *Bối cảnh:* {task.context_real}\n")
                f.write("\n")
                
        print(f"  + Đã lưu file Markdown: {analysis_path}")