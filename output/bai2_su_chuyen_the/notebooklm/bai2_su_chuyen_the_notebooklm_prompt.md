# NOTEBOOKLM PROMPT TRUNG TÂM - Bài 2 - Sự chuyển thể
> **HƯỚNG DẪN:** Hãy sao chép toàn bộ nội dung dưới đây và dán trực tiếp vào khung chat của Google NotebookLM sau khi đã tải các file tài liệu nguồn (`bai2_su_chuyen_the_dac_ta_gems.md`, `bai2_su_chuyen_the_ke_hoach_bai_day.md`, `bai2_su_chuyen_the_phieu_hoc_tap.md`, `bai2_su_chuyen_the_huong_dan_slide.md`) làm sources.

---

## NỘI DUNG PROMPT NỘP CHO NOTEBOOKLM

Bạn là một trợ lý thiết kế bài giảng chuyên nghiệp theo hệ thống tiêu chuẩn GEMS v8.0. Hãy dựa trên các tài liệu nguồn đã được tải lên để thực hiện hai nhiệm vụ sau:

### NHIỆM VỤ 1: XÂY DỰNG CẤU TRÚC CHI TIẾT CỦA BỘ SLIDE BÀI GIẢNG (SLIDE DECK)
1. **Yêu cầu nội dung & Đặt tên Slide dễ hiểu:**
   - Tạo cấu trúc slide chi tiết khớp hoàn toàn 1-1 với tệp `bai2_su_chuyen_the_huong_dan_slide.md`.
   - Giữ nguyên các phần phân cấp tiêu đề số hiệu dạng X.Y (ví dụ: Slide 1.0, Slide 1.1, Slide 2.1...).
   - Tách biệt hoàn toàn giữa **Slide Nhiệm vụ (không chứa đáp án)** và **Slide Đáp án (xuất hiện ngay tiếp sau)**.
   - **Tên Slide và nhãn nhiệm vụ phải thuần Việt 100%:**
     - Thay thế hoàn toàn "Assertion Reasoning" -> "Nhận định & Lý do"
     - Thay thế hoàn toàn "Matching Matrix" -> "Ghép nối đa biến"
     - Thay thế hoàn toàn "Bug Buster" -> "Tìm và sửa lỗi vật lý"
     - Thay thế hoàn toàn "Algorithmic Ordering" -> "Sắp xếp tiến trình"
     - Thay thế hoàn toàn "Visual Cloze Test" -> "Điền khuyết trực quan"
   - Highlight đậm và làm nổi bật các từ khóa định nghĩa, công thức toán lý bằng nhãn chú thích rõ ràng.
   - **Yêu cầu bắt buộc:** Toàn bộ tiêu đề, nội dung slide, câu hỏi và đáp án phải hiển thị 100% bằng tiếng Việt chính xác theo tệp nguồn. Tuyệt đối không tự ý dịch sang tiếng Anh.

2. **Yêu cầu Thiết kế và Giao diện (Theme & Design Sync):**
   - **Tông màu chủ đạo:** Sử dụng màu Navy mã HSL `#1E3A5F` làm màu chính cho tiêu đề, đường kẻ phân cách và khung viền.
   - **Tông màu bổ trợ:** Sử dụng màu Mint `#E8F5E9` làm màu nền cho các hộp ghi chú (Note boxes), bảng tóm tắt công thức hoặc ô ghi nhớ quan trọng.
   - **Phông chữ:** Thống nhất sử dụng phông chữ **Times New Roman** cho cả tiêu đề và nội dung văn bản.
   - **Bố cục:** Tối đa 6-8 dòng chữ/slide, nền sáng, chừa khoảng trống cho hình ảnh.

### NHIỆM VỤ 2: THIẾT KẾ CÁC INFOGRAPHIC ĐỤC LỖ HƯỚNG DỌC (STUDENT WORKSHEET VISUALS)
1. **Nguyên tắc thiết kế:**
   - Mỗi Đơn vị Kiến thức (ĐVKT) trong Phiếu học tập tương ứng với 1 Infographic độc lập hướng dọc (Quy tắc: 1 ĐVKT = 1 Infographic Portrait).
   - Nội dung trên Infographic phải bám sát câu hỏi, sơ đồ điền khuyết và bài tập của Phiếu học tập (`bai2_su_chuyen_the_phieu_hoc_tap.md`).
   - Thiết kế dạng đục lỗ (ví dụ: các ô trống nét đứt `........` hoặc bong bóng thoại trống kèm dấu `?`) để học sinh tự hoàn thành và ghi chú trên lớp.
2. **Yêu cầu giao diện:**
   - Đồng bộ màu sắc Navy/Mint và font chữ Times New Roman giống bộ slide bài giảng.
   - Xuất bản hình ảnh sắc nét dưới định dạng PNG.
