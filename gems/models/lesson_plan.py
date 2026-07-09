"""Schema Giai đoạn 4: Kế hoạch bài dạy (KHBD, chuẩn Công văn 5512)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class DigitalCompetencyTarget(BaseModel):
    code: str = Field(description="Mã năng lực thành phần, ví dụ 1.2 hoặc 3.1")
    competency: str = Field(description="Tên năng lực thành phần theo Khung NLS")
    learning_outcome: str = Field(description="Biểu hiện cần đạt ở mức Nâng cao 1 cho lớp 10-12")
    evidence: str = Field(description="Minh chứng/sản phẩm số quan sát và đánh giá được")


class ObjectivesSection(BaseModel):
    physics_competency: list[str] = Field(description="Năng lực đặc thù Vật lý")
    general_competency: list[str] = Field(description="Năng lực chung")
    digital_competency: list[DigitalCompetencyTarget] = Field(
        default_factory=list,
        description="Mục tiêu năng lực số lớp 10-12 theo Công văn 3456, có mã và minh chứng",
    )
    qualities: list[str] = Field(description="Phẩm chất")


class MaterialsSection(BaseModel):
    teacher_materials: list[str] = Field(description="Thiết bị của GV")
    student_materials: list[str] = Field(description="Học liệu của HS")


class ActivitySteps(BaseModel):
    step1_transfer: str = Field(description="Bước 1: Chuyển giao nhiệm vụ học tập")
    step2_execution: str = Field(description="Bước 2: Thực hiện nhiệm vụ")
    step3_report: str = Field(description="Bước 3: Báo cáo, thảo luận")
    step4_conclusion: str = Field(description="Bước 4: Kết luận, nhận định")


class ActivityPlan(BaseModel):
    activity_id: str = Field(description="Ví dụ: HD1, HD2...")
    activity_name: str = Field(description="Tên hoạt động")
    objectives: str = Field(description="Mục tiêu của hoạt động")
    content: str = Field(description="Nội dung hoạt động")
    product: str = Field(description="Sản phẩm học tập")
    active_learning_techniques: list[str] = Field(
        default_factory=list,
        description="1-2 kĩ thuật dạy học tích cực thực sự được triển khai trong hoạt động",
    )
    digital_competency_codes: list[str] = Field(
        default_factory=list,
        description="Mã NLS được hoạt động này phát triển; để trống nếu không có tích hợp số xác thực",
    )
    steps: ActivitySteps = Field(description="Quy trình tổ chức thực hiện 4 bước")


class AdjustmentSection(BaseModel):
    advantages: str = Field(description="Ưu điểm bài dạy")
    limitations: str = Field(description="Hạn chế")
    solutions: str = Field(description="Hướng điều chỉnh")


class LessonPlanContent(BaseModel):
    lesson_name: str
    duration: str = Field(description="Thời lượng (ví dụ: 2 tiết)")
    objectives: ObjectivesSection
    materials: MaterialsSection
    activities: list[ActivityPlan]
    adjustments: AdjustmentSection
