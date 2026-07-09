"""Schema Giai đoạn 1: Phân tích sư phạm + Ma trận bài học GEMS.

Trước đây được khai gần như y hệt ở CẢ HAI nơi (gems_agent.py và
gems_analyzer.py — module thứ 2 đã "chết", không còn import) — giờ chỉ
khai đúng 1 lần ở đây.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class MisconceptionItem(BaseModel):
    misconception: str = Field(description="Mô tả quan niệm sai lầm phổ biến của học sinh")
    correct_concept: str = Field(description="Bản chất vật lý đúng đắn")
    explanation: str = Field(description="Giải thích sư phạm trực quan để sửa sai")


class PedagogicalAnalysis(BaseModel):
    key_concepts: list[str] = Field(description="Các kiến thức cốt lõi của bài học")
    misconceptions: list[MisconceptionItem] = Field(description="Danh sách các bẫy sai lầm")
    teaching_methods: list[str] = Field(description="Phương pháp giảng dạy đề xuất")


class TaskItem(BaseModel):
    task_id: str = Field(description="Mã nhiệm vụ (ví dụ: NV1, NV2...)")
    task_type: str = Field(description="Loại nhiệm vụ GEMS (ví dụ: Matching Matrix, Bug Buster...)")
    task_name: str = Field(description="Tên nhiệm vụ ngắn gọn")
    description: str = Field(description="Mô tả chi tiết yêu cầu nhiệm vụ")
    context_real: str = Field(description="Bối cảnh thực tế đời sống liên quan")


class KnowledgeUnit(BaseModel):
    unit_id: str = Field(description="Mã đơn vị kiến thức (ví dụ: ĐVKT 1...)")
    unit_name: str = Field(description="Tên đơn vị kiến thức")
    concepts: list[str] = Field(description="Khái niệm chính cấu thành")
    tasks: list[TaskItem] = Field(description="Chuỗi nhiệm vụ học tập")


class LessonMatrix(BaseModel):
    lesson_name: str = Field(description="Tên bài học tổng quát")
    units: list[KnowledgeUnit] = Field(description="Danh sách các đơn vị kiến thức nhỏ")


class GEMSArchitect(BaseModel):
    analysis: PedagogicalAnalysis = Field(description="Phân tích sư phạm từ YCCĐ")
    matrix: LessonMatrix = Field(description="Ma trận bài học và chuỗi nhiệm vụ")
