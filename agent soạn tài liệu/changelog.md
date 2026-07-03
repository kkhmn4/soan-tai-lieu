# Changelog

All notable changes to this project will be documented in this file.

## [2026-06-30]
### Added
- **Tách biệt Prompt NotebookLM**:
  - Hỗ trợ parser tự động trích xuất ĐVKT và từ khóa gợi ý điền khuyết của Phiếu học tập.
  - Hỗ trợ parser tự động bóc tách các đặc tính thiết kế (giáo viên, phông chữ, trường phái, quy tắc bổ sung) từ Hướng dẫn slide.
  - Tự động sinh ra 2 tệp prompt Slide bài giảng (`_slide_prompt.md`) và Infographic đục lỗ (`_info_prompt.md`) riêng biệt cho mỗi bài học để tăng cường độ chính xác khi tạo học liệu trên NotebookLM.
- **Biên dịch Word DOCX Nâng cao**:
  - Thiết lập lề trang động theo loại tài liệu (pht, khbd, dethi).
  - Tự động giãn dòng 1.3 lines, spacing 6pt before/after, thụt dòng đầu 1cm cho văn bản thường.
  - Bảng biểu tự động chống ngắt đôi dòng (`cantSplit`) và lặp lại header (`tblHeader`).
  - Đề thi tự động chống ngắt trang mồ côi và xếp phương án lựa chọn ABCD vào bảng không viền (1, 2, 4 cột) linh hoạt theo độ dài phương án.

### Fixed
- Sửa lỗi gộp dòng (paragraph folding) đối với câu hỏi trắc nghiệm in đậm và phương án trắc nghiệm.
- Sửa lỗi Regex trượt khớp các câu hỏi trắc nghiệm in đậm.
- Chuẩn hóa khoảng trắng viết chính tả tiếng Việt và khoảng trắng giữa số - đơn vị vật lý.

## [2026-06-28]
### Added
- **Bài 7: Nhiệt hóa hơi riêng**:
  - [x] Phân tích sư phạm & Đặc tả GEMS v8.0.
  - [x] Phiếu học tập Markdown & Word `.docx` tích hợp các hoạt động đục lỗ lý thuyết và phần Mở rộng.
  - [x] Slide bài giảng PowerPoint `.pptx` chuẩn GEMS v8.0 (phân cấp X.Y, tách slide câu hỏi & đáp án).
  - [x] Bộ 2 Infographics hướng dọc (portrait) GEMS v8.0 (Khái niệm & Thực hành).
  - [x] Giáo án giảng dạy chi tiết 2 tiết học.
  - [x] Bài tập về nhà và Đáp án chi tiết dạng LaTeX `.tex`.

### Fixed
- Khôi phục và tái thiết lập tệp mã nguồn cốt lõi `engine/main.py` bị hỏng từ nhật ký lịch sử hội thoại IDE.
- Làm sạch không gian làm việc bằng cách loại bỏ các tập tin chẩn đoán tạm thời.

## [2026-06-25]
### Added
- **Bài 6: Nhiệt nóng chảy riêng**:
  - [x] Phiếu học tập Markdown & Word `.docx` tích hợp các hoạt động đục lỗ lý thuyết và phần Mở rộng.
  - [x] Slide bài giảng PowerPoint `.pptx` chuẩn GEMS v7.2 (phân cấp X.Y, tách slide câu hỏi & đáp án).
  - [x] Bộ 2 Infographics hướng dọc (portrait) GEMS v7.3 (Khái niệm & Thực hành).
  - [x] Giáo án giảng dạy chi tiết 2 tiết học.
  - [x] Bài tập về nhà và Đáp án chi tiết dạng LaTeX `.tex`.
  - [x] Script tự động hóa pipeline NotebookLM: `scratch/rebuild_bai6_complete.py`.

### Changed
- **Bài 4: Nhiệt dung riêng**:
  - Cập nhật quy chuẩn GEMS v7.3: bổ sung phần Mở rộng kiến thức thực tế (Két nước làm mát và vật liệu PCM trữ nhiệt) vào Phiếu học tập, Slide và Giáo án.
  - Biên dịch lại Phiếu học tập Word `.docx` tương thích 100%.

### Fixed
- Khắc phục lỗi thiếu trình biên dịch LaTeX bằng cách lưu mã nguồn `.tex` nguyên bản vào thư mục `ready/` của Bài 6.
- Khắc phục lỗi mã hóa ký tự Unicode trên Windows CLI bằng cách cấu hình UTF-8 mặc định trong các script pipeline.
