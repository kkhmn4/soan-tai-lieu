"""Schema Giai đoạn 2: Phiếu học tập (PHT).

Trước đây PHT tổ chức theo khung riêng của GEMS: mỗi ĐVKT tự lặp lại đủ 4
phần Khám phá → Trọng tâm → Vận dụng → Mở rộng (`UnitWorksheetContent`). Từ
skill v9.4.0, PHT bám THẲNG tiến trình dạy thật trong KHBD — 1 trình tự
phẳng "1. Hình thành kiến thức mới" (mỗi ĐVKT là 1 mục con) → "2. Luyện
tập" → "3. Vận dụng" — để giáo viên/học sinh dùng PHT song song KHBD mà
không phải tự "dịch" giữa 2 cách tổ chức khác nhau. Không có mục cho hoạt
động Khởi động (không cần PHT giấy cho phần này)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class TaskContent(BaseModel):
    task_id: str = Field(description="Mã nhiệm vụ (ví dụ: NV1...)")
    task_type: str = Field(description="Loại nhiệm vụ GEMS")
    task_name: str = Field(description="Tên nhiệm vụ")
    content: str = Field(description="Nội dung chi tiết câu hỏi hoặc bối cảnh và câu hỏi chi tiết. Phải cụ thể và hướng dẫn chi tiết học sinh làm gì.")
    instructions: str = Field(description=(
        "Hướng dẫn thực hiện nhiệm vụ, bắt buộc nêu đủ 3 ý: (1) hình thức tổ chức "
        "(cá nhân/cặp đôi/nhóm N học sinh), (2) thời gian cụ thể (phút), (3) tài liệu/công cụ "
        "phải dùng (đọc SGK trang mấy, quan sát thí nghiệm/video nào, hay tự suy luận). "
        "Không được bỏ trống hoặc chỉ nêu 1-2 ý."
    ))


class CoreTheorySection(BaseModel):
    summary_cloze: str = Field(description="Đoạn văn tóm tắt lý thuyết đục lỗ điền khuyết sử dụng các số thứ tự (1), (2)...")
    key_words: list[str] = Field(description="Danh sách đáp án tương ứng")


class KnowledgeFormationUnit(BaseModel):
    """1 mục con của "1. HÌNH THÀNH KIẾN THỨC MỚI" — đúng 1 ĐVKT, gồm nhiệm
    vụ khám phá + lý thuyết trọng tâm (không còn Vận dụng/Mở rộng lồng ở
    đây — 2 phần đó nay là mục lớn riêng, dùng chung cho mọi ĐVKT)."""
    unit_id: str = Field(description="Mã đơn vị kiến thức")
    unit_name: str = Field(description="Tên đơn vị kiến thức")
    tasks: list[TaskContent] = Field(description="Các nhiệm vụ khám phá")
    core_theory: CoreTheorySection


class PracticeItem(BaseModel):
    """1 bài toán/tình huống của mục "2. LUYỆN TẬP", gắn với 1 ĐVKT cụ thể
    nhưng hiển thị trong 1 mục lớn dùng chung — khớp cách KHBD gộp bài
    luyện tập của nhiều ĐVKT vào 1 hoạt động Luyện tập duy nhất."""
    unit_id: str = Field(description="Mã đơn vị kiến thức mà bài toán này thuộc về")
    unit_name: str = Field(description="Tên đơn vị kiến thức")
    scenario: str = Field(description="Bài toán/tình huống thực tế có tính toán hoặc suy luận vật lý")
    instructions: str = Field(description=(
        "Hướng dẫn thực hiện nhiệm vụ, bắt buộc nêu đủ 3 ý: (1) hình thức tổ chức "
        "(cá nhân/cặp đôi/nhóm N học sinh), (2) thời gian cụ thể (phút), (3) tài liệu/công cụ "
        "phải dùng. Không được bỏ trống hoặc chỉ nêu 1-2 ý — khớp yêu cầu skill mục 4.2: MỌI nhiệm "
        "vụ, kể cả Luyện tập, phải có nhãn Hình thức/Thời gian/Tài liệu để dùng trên Slide."
    ))


class ApplicationReading(BaseModel):
    """1 đoạn đọc mở rộng của mục "3. VẬN DỤNG", gắn với 1 ĐVKT."""
    unit_id: str = Field(description="Mã đơn vị kiến thức mà đoạn đọc này thuộc về")
    unit_name: str = Field(description="Tên đơn vị kiến thức")
    reading_content: str = Field(description="Nội dung đọc hiểu mở rộng, kết nối STEM hoặc hướng nghiệp")


class LessonWorksheet(BaseModel):
    lesson_name: str
    knowledge_formation: list[KnowledgeFormationUnit] = Field(description='Mục "1. HÌNH THÀNH KIẾN THỨC MỚI" — mỗi ĐVKT 1 phần tử')
    practice_items: list[PracticeItem] = Field(description='Mục "2. LUYỆN TẬP" — mỗi ĐVKT 1 bài toán')
    application_tasks: list[TaskContent] = Field(
        default_factory=list,
        description='Mục "3. VẬN DỤNG" — nhiệm vụ vận dụng nâng cao (ví dụ Engineering Debugger); để rỗng nếu bài không có.',
    )
    application_readings: list[ApplicationReading] = Field(description='Mục "3. VẬN DỤNG" — đoạn đọc mở rộng mỗi ĐVKT')
