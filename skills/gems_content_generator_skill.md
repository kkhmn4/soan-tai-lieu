---
name: gems_content_generator_skill
description: |
  Kỹ năng chuyên biệt dành cho Chuyên gia Giáo dục môn Vật lý để sinh Phiếu học tập in ấn, Slide bài giảng đồng bộ và Bài tập về nhà dạng Markdown tích hợp TikZ ở các Bước từ 3 đến 5.
  Kích hoạt khi người dùng nhập các lệnh: "sinh tài liệu", "tạo worksheet", "tạo slide", "tạo homework", "bước 3", "bước 4", "bước 5".
version: 7.0.0
---

# Goal
Sinh đồng bộ toàn bộ tài liệu dạy học môn Vật lý (Phiếu học tập, Slide bài giảng đồng bộ v7, Bài tập về nhà Markdown, Giáo án 5512) bám sát Spec & Ma trận đã duyệt, tự động chạy script biên dịch sang Word .docx tiết kiệm không gian in ấn và soát xét XML sạch lỗi.

# Instructions

## 🌟 BƯỚC 3: XUẤT BẢN PHIẾU HỌC TẬP CHI TIẾT (GRAPHIC WORKSHEET)
- **Nhiệm vụ:**
  - Ghi vào thư mục chung `output/generated_docs/gems_worksheet_[ten_bai].md`.
  - Thiết kế khu vực thông tin chung ở đầu trang nhất (Tên bài học đầy đủ, Họ và tên học sinh, Lớp, Ngày... tháng... năm...).
  - Từng đơn vị kiến thức nhỏ triển khai qua 4 phần tuyến tính:
    - `[Phần 1] NHIỆM VỤ KHÁM PHÁ`: Đưa ra hiện tượng thực tế, giao chuỗi nhiệm vụ khám phá liên kết logic (Nhiệm vụ 1, Nhiệm vụ 2...) từ 12 loại hình nhiệm vụ mới.
    - `[Phần 2] KIẾN THỨC TRỌNG TÂM`: Lý thuyết cốt lõi dưới dạng đục lỗ điền khuyết (1), (2)... và công thức dạng infographic thu nhỏ.
    - `[Phần 3] THỬ THÁCH VẬN DỤNG`: Tình huống thực tế đời sống mới kèm hình ảnh dán bằng đường dẫn tuyệt đối, chừa sẵn 3-5 dòng kẻ chấm.
    - `[Phần 4] MỞ RỘNG KIẾN THỨC`: Đọc hiểu kết nối 




















  - **Slide kết bài:** Sơ đồ tư duy (Mindmap) tổng hợp toàn bộ bài học.
  - **Quy chuẩn thiết kế Slide:**
    - Font chữ `"UVN bai sau"` đồng bộ toàn bộ slide.
    - Cỡ chữ tiêu đề 28-32pt, cỡ chữ nội dung 24-28pt. Nền sáng (trắng hoặc nhạt).
    - Tối đa 6-8 dòng văn bản mỗi slide, bố cục sạch, nhiều khoảng trắng.
    - Chỉ sử dụng ảnh chụp thực tế hoặc ảnh tư liệu khoa học chất lượng cao, không dùng tranh vẽ hoạt hình/3D bồng bềnh/ảnh ảo.

---

## 🌟 BƯỚC 5: XUẤT BẢN PHIẾU LUYỆN TẬP TẠI NHÀ (HOMEWORK)
- **Nhiệm vụ:**
  - **Bản Markdown:** Ghi vào thư mục chung `output/generated_docs/gems_homework_[ten_bai].md` và tệp đáp án chi tiết `output/generated_docs/gems_homework_answers_[ten_bai].md`.
    - Thiết kế đúng cấu trúc 2025: Phần I (18 MCQ) - Phần II (4 Đúng/Sai, mỗi câu 4 ý a, b, c, d) - Phần III (6 Trả lời ngắn tính ra số cụ thể).
    - 50% câu hỏi bối cảnh thực tế quốc tế có hằng số, quy tắc làm tròn rõ ràng.
    - Viết biểu thức toán lý dạng LaTeX đặt trong dấu đô la đơn: `$công_thức$`. Động năng là `$W_đ$`, thế năng là `$W_t$`.
  - **Vẽ hình TikZ (Chỉ dùng khi cần tạo đồ thị hoặc hình vẽ cần thiết):**
    - Với các câu hỏi hoặc bài giải yêu cầu hiển thị đồ thị, sơ đồ thí nghiệm hoặc hình vẽ cấu trúc vật lý cần thiết, thiết kế hình bằng mã TikZ và nhúng trực tiếp dưới dạng khối mã (code block) trong tệp Markdown tương ứng.
    - Không tạo hoặc xuất ra tệp `.tex` độc lập cho toàn bộ tài liệu Homework.

# Constraints
- 🚫 KHÔNG sử dụng các từ ngữ mơ hồ như "xử lý", "tối ưu", "phù hợp", "đầy đủ", "chính xác", "kiểm tra", "chuẩn", "nhiều", "lớn".
- 🚫 KHÔNG sử dụng bất kỳ từ tiếng Anh hoặc chú thích tiếng Anh nào trong tài liệu chính (100% thuần Việt).
- ✅ Slide giáo viên bắt buộc tên "Kha Khung Hiệp", font "UVN bai sau", và cấu trúc 7 bước cho mỗi ĐVKT.
- ✅ Chỉ sử dụng mã vẽ hình TikZ nhúng trong khối mã Markdown khi cần biểu diễn đồ thị hoặc sơ đồ vật lý cần thiết. (Không soạn thảo toàn bộ đề bài/đáp án dưới dạng file .tex độc lập).
