SYSTEM_INSTRUCTION = (
    "Bạn là Chuyên gia thiết kế phiếu học tập Vật lý THPT. "
    "Hãy sinh nội dung PHT chi tiết, thuần Việt, chất lượng khoa học cao."
)


def build_prompt(matrix_json: str) -> str:
    return (
        f"Dựa vào ma trận bài học: {matrix_json}\n"
        "Hãy sinh nội dung chi tiết Phiếu học tập (PHT) cho học sinh. PHT bám THẲNG tiến trình dạy "
        "thật trong Kế hoạch bài dạy (Hình thành kiến thức → Luyện tập → Vận dụng) — KHÔNG dùng "
        "khung lặp lại 4 phần/ĐVKT như trước. KHÔNG có mục nào cho hoạt động Khởi động.\n"
        "Yêu cầu:\n"
        "- `knowledge_formation` (mục 1. HÌNH THÀNH KIẾN THỨC MỚI): mỗi ĐVKT 1 phần tử, gồm các "
        "nhiệm vụ khám phá chi tiết và phần lý thuyết trọng tâm đục lỗ điền khuyết (ký hiệu (1), "
        "(2), (3)... kèm hộp đáp án gợi ý).\n"
        "- Mỗi nhiệm vụ (trong knowledge_formation, practice_items, VÀ application_tasks nếu có) "
        "PHẢI có trường instructions nêu đủ 3 ý: (1) hình thức tổ chức (cá nhân/cặp đôi/nhóm N học "
        "sinh), (2) thời gian cụ thể (phút), (3) tài liệu/công cụ phải dùng (đọc SGK trang mấy, "
        "quan sát thí nghiệm/video nào, hay tự suy luận). Không bỏ trống — áp dụng cho MỌI nhiệm "
        "vụ, không có ngoại lệ nào (kể cả bài toán ở practice_items).\n"
        "- `practice_items` (mục 2. LUYỆN TẬP): mỗi ĐVKT 1 bài toán/tình huống đời sống có tính "
        "toán hoặc suy luận vật lý, PHẢI diễn đạt bằng đúng 1 trong 3 dạng câu hỏi của đề thi tốt "
        "nghiệp THPT: trắc nghiệm 4 phương án A/B/C/D, hoặc Đúng/Sai 4 ý a-d, hoặc trả lời ngắn "
        "dạng số có nêu rõ quy tắc làm tròn — để học sinh làm quen cấu trúc đề thật ngay khi học, "
        "không đợi đến bài tập về nhà.\n"
        "- `application_readings` (mục 3. VẬN DỤNG): mỗi ĐVKT 1 đoạn đọc hiểu ngắn kết nối "
        "STEM/công nghệ/hướng nghiệp, trích nguồn uy tín.\n"
        "- `application_tasks` (cũng thuộc mục 3. VẬN DỤNG): chỉ thêm khi bài học thực sự có nhiệm "
        "vụ vận dụng nâng cao dạng phản biện/thiết kế (ví dụ Engineering Debugger) — để rỗng nếu "
        "không có, không gượng ép."
    )
