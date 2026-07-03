---
name: gems_document_generator_skill
description: |
  Kỹ năng quản lý và điều phối toàn bộ hệ thống GEMS Vật lý v7.0, tích hợp chế độ chạy tự động Auto-pilot từ Bước 1 đến Bước 6.
  Kích hoạt khi người dùng yêu cầu "tạo tài liệu", "soạn tài liệu", "tạo học liệu", "chạy gems", "tự động".
version: 7.0.0
---

# Goal
Tự động hóa hoàn toàn việc thiết kế, biên soạn và định dạng trọn bộ học liệu môn Vật lí chất lượng cao bám sát Chương trình GDPT 2018 Kết nối tri thức và quy định của GEMS_VAT_LY_V7_PRINT_WORKSHEET_FRAMEWORK để xuất file Word (.docx) và Markdown tích hợp hình vẽ TikZ, hỗ trợ chế độ tự động chạy từ Bước 1 đến Bước 6 (Auto-pilot).

# Instructions

## 1. KHỞI CHẠY & KIỂM TRA ĐẦU VÀO
- Xác nhận thông tin đầu vào từ người dùng (tên bài học, chương, tài liệu đi kèm).
- Xác định chế độ chạy:
  - Nếu người dùng nhập trực tiếp tên bài học hoặc thêm cờ `--auto` / yêu cầu "chạy tự động" → Kích hoạt **Chế độ Tự động (Auto-pilot)**. Chạy liên tục từ Bước 1 đến Bước 6 không dừng.
  - Nếu người dùng chạy lệnh `/gems` thông thường → Kích hoạt **Chế độ Từng bước (Interactive)**. Dừng lại hỏi ý kiến phê duyệt ở cuối mỗi bước.

##









- Lưu trữ kết quả phân tích vào `docs/GEMS_SPEC.md`.
- *Chế độ Từng bước: Dừng lại đợi duyệt.*

### Bước 3: Xuất bản Phiếu học tập chi tiết (Worksheet)
- Gọi `gems_content_generator_skill` sinh nội dung Phiếu học tập chi tiết ghi vào `docs/gems_worksheet_[ten_bai].md`.
- Đảm bảo chừa dòng chấm `....` dài 90 ký tự, 3-5 dòng, đục lỗ lý thuyết Trọng tâm.
- *Chế độ Từng bước: Dừng lại đợi duyệt.*

### Bước 4: Xuất bản Slide bài giảng đồng bộ (Lecture Slides)
- Gọi `gems_content_generator_skill` sinh nội dung Slide bài giảng ghi vào `docs/gems_slides_guide_[ten_bai].md`.
- Đồng bộ 1-1 với PHT, cấu trúc 7 slide cho mỗi ĐVKT, giáo viên tên "Kha Khung Hiệp", font "UVN bai sau", highlight vàng.
- *Chế độ Từng bước: Dừng lại đợi duyệt.*

### Bước 5: Xuất bản Phiếu luyện tập tại nhà (Homework)
- Gọi `gems_content_generator_skill` sinh hệ thống bài tập về nhà và đáp án chi tiết dưới dạng Markdown, có nhúng hình vẽ TikZ cho các câu hỏi đồ thị hoặc hình vẽ cần thiết.
- Lưu trữ vào thư mục chung `output/generated_docs/gems_homework_[ten_bai].md` và các file đáp án tương ứng (không tạo tệp .tex độc lập cho toàn bộ tài liệu).
- *Chế độ Từng bước: Dừng lại đợi duyệt.*

### Bước 6: Kiểm định chất lượng tổng hợp (QA Check)
- Chạy đối chiếu toàn bộ tệp học liệu với bộ 15 tiêu chí kiểm định chất lượng (AI Self-Check).
- Chạy script biên dịch Word `.docx` (ví dụ: `export_docx.py`) nếu có sẵn trên hệ thống.
- Xuất bản Báo cáo Kiểm định QA và hiển thị danh sách các file học liệu đã được tạo thành công trong thư mục chung `output/generated_docs/`.

# Constraints
- 🚫 KHÔNG sử dụng các từ ngữ mơ hồ như "xử lý", "tối ưu", "phù hợp", "đầy đủ", "chính xác", "kiểm tra", "chuẩn", "nhiều", "lớn".
- 🚫 KHÔNG dùng định dạng HTML phức tạp làm lỗi trình biên dịch Word.
- ✅ LUÔN dùng đúng 90 ký tự chấm liên tiếp cho dòng kẻ viết bài trên PHT: `..........................................................................................`
- ✅ Bắt buộc sử dụng hình vẽ TikZ nhúng trong khối mã Markdown của Homework đối với các câu hỏi đồ thị hoặc mô tả hiện tượng cần hình minh họa.
- ✅ Toàn bộ biểu thức toán học trong tài liệu được viết dạng `$công_thức$`. Đặc biệt, ký hiệu động năng là `$W_đ$`, thế năng là `$W_t$`.
