"""Prompt Giai đoạn 3: Bài tập về nhà.

Chuẩn dưới đây đối chiếu trực tiếp với đề thi tốt nghiệp THPT chính thức
(mã đề 0227 năm 2025, mã đề 0214 năm 2026 — ảnh lưu tại `tai-lieu-goc/mẫu/`):
không chỉ đúng SỐ LƯỢNG câu (18/4/6) mà còn đúng PHONG CÁCH RA ĐỀ của từng
phần, để bài tập tự luyện có "cảm giác đề thi thật" ngay từ đầu, khớp
`skills/gems_physics_skill.md` mục 4.4.
"""

SYSTEM_INSTRUCTION = (
    "Bạn là Chuyên gia ra đề thi tốt nghiệp THPT môn Vật lí. Hãy tạo hệ thống bài tập bám sát "
    "chính xác phong cách ra đề thật (không chỉ đúng số lượng câu), gài bẫy quan niệm sai lầm "
    "chuẩn xác, thuần Việt 100%."
)

PART1_LEVEL_GUIDE = (
    "- 6 câu mức NHẬN BIẾT: hỏi thẳng định nghĩa, đơn vị đo, phát biểu định luật/nội dung SGK — "
    "không cần tính toán, không qua bước suy luận trung gian.\n"
    "- 6 câu mức THÔNG HIỂU: diễn giải cơ chế, đọc đồ thị/hình vẽ/mô hình, so sánh hai quá trình, "
    "hoặc suy ra hệ quả trực tiếp của một định luật — không có phép tính số.\n"
    "- 6 câu mức VẬN DỤNG: có ít nhất 1 phép tính (1-2 bước) áp dụng công thức vào số liệu cụ "
    "thể, ưu tiên gắn bối cảnh kĩ thuật/đời sống thay vì số liệu trừu tượng."
)

PART2_GUIDE = (
    "Mỗi câu Phần II PHẢI xoay quanh ĐÚNG MỘT bối cảnh/thí nghiệm/thiết bị cụ thể (có thể kèm mô "
    "tả hình vẽ) — 4 ý a), b), c), d) là một CHUỖI SUY LUẬN liên kết chặt quanh bối cảnh đó, không "
    "phải 4 mệnh đề rời rạc ghép ngẫu nhiên. Trong 4 ý: bắt buộc tối thiểu 1 ý định tính thuần suy "
    "luận vật lý, có thể có 1 ý yêu cầu tính toán ngắn, và bắt buộc cài ít nhất 1 bẫy quan niệm "
    "sai lầm lấy từ phần phân tích sư phạm — diễn đạt tự nhiên như một nhận định hợp lý nhìn "
    "thoáng qua, không lộ liễu là bẫy."
)

PART3_GUIDE = (
    "6 câu Phần III phải chia thành 3 CẶP câu dùng chung một đoạn dữ kiện (đặt cùng giá trị "
    "shared_context cho 2 câu liền nhau, khớp mẫu 'Dùng thông tin sau cho câu X và câu Y: ...' "
    "của đề thật) — bối cảnh phải là tình huống kĩ thuật/khoa học/đời sống thật, không dùng số "
    "liệu trừu tượng vô nghĩa. Mỗi câu là một phép tính nhiều bước độc lập trên cùng dữ kiện, và "
    "PHẢI nêu rõ quy tắc làm tròn ngay trong question_text (ví dụ: '(làm tròn kết quả đến chữ số "
    "hàng phần trăm)') — đề thi thật luôn quy định làm tròn riêng cho từng câu, không để mặc định."
)


def build_prompt(matrix_json: str, analysis_json: str) -> str:
    return (
        f"Dựa vào ma trận bài học: {matrix_json}\n"
        f"và phân tích bẫy quan niệm sai lầm: {analysis_json}\n\n"
        "Hãy sinh hệ thống bài tập về nhà bám sát cấu trúc VÀ phong cách ra đề của đề thi tốt "
        "nghiệp THPT môn Vật lí (đối chiếu đề thật các năm 2025-2026):\n\n"
        "PHẦN I — 18 câu trắc nghiệm 4 phương án (A, B, C, D), chỉ 1 đáp án đúng, chia đúng theo "
        "3 mức độ nhận thức sau:\n"
        f"{PART1_LEVEL_GUIDE}\n"
        "Toàn bộ phương án nhiễu (sai) phải bắt nguồn từ đúng các quan niệm sai lầm đã phân tích "
        "ở trên, không bịa phương án nhiễu ngẫu nhiên vô căn cứ.\n\n"
        "PHẦN II — 4 câu Đúng/Sai (mỗi câu gồm 4 mệnh đề a, b, c, d):\n"
        f"{PART2_GUIDE}\n\n"
        "PHẦN III — 6 câu trả lời ngắn (kết quả số):\n"
        f"{PART3_GUIDE}\n\n"
        "YÊU CẦU CHUNG:\n"
        "- Tối thiểu 50% tổng số câu hỏi trên cả 3 phần phải gắn bối cảnh thực tế/kĩ thuật/khoa "
        "học cụ thể (thiết bị, hiện tượng tự nhiên, ứng dụng công nghệ...), không phải bài toán "
        "số liệu trần trụi vô nghĩa.\n"
        "- Nếu bất kỳ câu nào trong Phần III cần hằng số vật lí dùng chung (π, R, N_A, hằng số "
        "Planck...), hãy gom vào trường shared_constants theo đúng dòng '+ Cho biết: ...' của đề "
        "thật, không lặp lại hằng số riêng lẻ trong từng câu.\n"
        "- Không đưa đáp án Đúng/Sai vào ngay trong question_text/statement của Phần II — đáp án "
        "chỉ nằm ở các trường correct_a/b/c/d và explanation."
    )
