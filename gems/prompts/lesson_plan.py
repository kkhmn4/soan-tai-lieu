SYSTEM_INSTRUCTION = (
    "Bạn là chuyên gia thiết kế Kế hoạch bài dạy Vật lí THPT. Soạn đúng Phụ lục IV "
    "Công văn 5512, vận dụng kĩ thuật dạy học tích cực và tích hợp Khung năng lực số "
    "theo Công văn 3456/BGDĐT-GDPT; nội dung chi tiết, khả thi và thuần Việt 100%."
)

ACTIVE_TECHNIQUES = (
    "Các mảnh ghép; Khăn trải bàn; Động não; Ổ bi; Bể cá; Tia chớp; XYZ; "
    "Lược đồ tư duy; Chia sẻ nhóm đôi; Kipling; KWL/KWLH; Đặt câu hỏi; "
    "Chia nhóm; Đọc tích cực; Viết tích cực; Đóng vai; Trình bày một phút; Chúng em biết 3"
)

DIGITAL_AREAS = (
    "1 Khai thác dữ liệu và thông tin; 2 Giao tiếp và hợp tác; 3 Sáng tạo nội dung số; "
    "4 An toàn; 5 Giải quyết vấn đề; 6 Ứng dụng trí tuệ nhân tạo"
)


def build_prompt(matrix_json: str) -> str:
    return (
        f"Dựa vào ma trận bài học: {matrix_json}\n"
        "Hãy viết Kế hoạch bài dạy (KHBD) chi tiết chuẩn Công văn 5512.\n"
        "Yêu cầu:\n"
        "- Xác định rõ mục tiêu Năng lực đặc thù Vật lý, Năng lực chung, Phẩm chất.\n"
        "- Bổ sung mục tiêu năng lực số theo Công văn 3456. Với lớp 12 dùng mức Nâng cao 1: "
        "học sinh xử lí các nhiệm vụ/vấn đề khác nhau và có thể hướng dẫn người khác. "
        "Mỗi mục tiêu phải có mã năng lực thành phần, tên, biểu hiện cần đạt và minh chứng đánh giá được.\n"
        f"- Sáu miền NLS để lựa chọn: {DIGITAL_AREAS}. Không tích hợp gượng ép; nếu hoạt động không có "
        "công cụ, thao tác và sản phẩm số xác thực thì để digital_competency_codes rỗng.\n"
        "- Thiết lập danh mục Thiết bị giảng dạy cho Giáo viên và Học sinh.\n"
        "- Triển khai tối thiểu 4 loại hoạt động: Mở đầu; Hình thành kiến thức mới; Luyện tập; Vận dụng.\n"
        "- Nếu bài học có từ 2 Đơn vị kiến thức (ĐVKT) trở lên, TÁCH hoạt động Hình thành kiến thức "
        "mới thành nhiều hoạt động riêng theo từng ĐVKT (ví dụ Hoạt động 2 cho ĐVKT 1, Hoạt động 3 "
        "cho ĐVKT 2) thay vì gộp chung — để cấu trúc KHBD bám sát cấu trúc Phiếu học tập (PHT vốn "
        "tổ chức tuần tự theo từng ĐVKT). Trong nội dung mỗi hoạt động, ghi rõ '(tương ứng PHT mục "
        "X.Y)' để đối chiếu 1-1 với đúng tiểu mục PHT (X = số ĐVKT, Y = 1 Khám phá/2 Trọng tâm/"
        "3 Vận dụng/4 Mở rộng).\n"
        "- Bước 1 (Chuyển giao nhiệm vụ) của MỌI hoạt động PHẢI nêu đủ 3 ý như PHT: (1) hình thức "
        "tổ chức (cá nhân/cặp đôi/nhóm N học sinh), (2) thời gian cụ thể (phút), (3) tài liệu/công "
        "cụ học sinh phải dùng (SGK trang mấy, quan sát thí nghiệm/video nào, hay Phiếu học tập "
        "nhiệm vụ nào). Không được viết chung chung thiếu 1 trong 3 ý.\n"
        "- Trong hoạt động Luyện tập, nội dung câu hỏi/bài tập PHẢI soạn theo đúng 1 trong 3 dạng "
        "của đề thi tốt nghiệp THPT (trắc nghiệm 4 phương án A/B/C/D, hoặc Đúng/Sai 4 ý a-d, hoặc "
        "trả lời ngắn dạng số có nêu rõ quy tắc làm tròn) — để học sinh luyện đúng cấu trúc đề "
        "thật ngay khi học, không đợi đến Bài tập về nhà mới gặp lần đầu.\n"
        "- Với mỗi hoạt động, viết đủ a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện.\n"
        f"- Chọn 1-2 kĩ thuật phù hợp cho từng hoạt động từ danh mục: {ACTIVE_TECHNIQUES}. "
        "Phải thể hiện cơ chế của kĩ thuật trong bốn bước, không chỉ ghi tên. Không dùng quá nhiều kĩ thuật.\n"
        "- Khi tích hợp NLS, nêu công cụ/thao tác số, quy tắc an toàn-bản quyền-trích nguồn khi liên quan, "
        "và bảo đảm sản phẩm chứa minh chứng tương ứng với mã NLS.\n"
        "- Quy trình thực hiện gồm đúng 4 bước:\n"
        "  * Chuyển giao nhiệm vụ học tập\n"
        "  * Thực hiện nhiệm vụ\n"
        "  * Báo cáo, thảo luận\n"
        "  * Kết luận, nhận định\n"
        "- Cuối giáo án bổ sung mục điều chỉnh bài dạy: Ưu điểm, Hạn chế, Hướng điều chỉnh."
    )
