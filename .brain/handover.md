# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 HANDOVER DOCUMENT – GEMS Hermes Pipeline
# Lưu lúc: 2026-06-28T09:48:00+07:00
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📍 Đang làm gì

**Dự án:** GEMS Hermes – Tự động hoá sinh học liệu Vật lý Chương Nhiệt (Bài 4–7)  
**Bước tiếp theo:** Chạy pipeline sinh học liệu cho Bài 5 (Nhiệt độ. Thang nhiệt độ. Nhiệt kế) trên NotebookLM.

---

## ✅ Đã hoàn thành

- [x] **Bài 4 (Nhiệt dung riêng)**: Hoàn thành 100% tài liệu Markdown, Word, LaTeX, slide deck và infographics.
- [x] **Bài 6 (Nhiệt nóng chảy riêng)**: Hoàn thành 100% tài liệu Markdown, Word, LaTeX, slide deck và infographics.
- [x] **Bài 7 (Nhiệt hóa hơi riêng)**: Hoàn thành 100% tài liệu Markdown, Word, LaTeX, slide deck và infographics (vừa hoàn tất trong session này).
- [x] **Khôi phục tệp hệ thống bị hỏng**: Phân tích lịch sử hội thoại IDE và khôi phục hoàn chỉnh tệp `engine/main.py` về trạng thái sạch sẽ, khôi phục các tệp theo dõi cục bộ bằng `git restore .`.
- [x] **Dọn dẹp môi trường**: Xóa sạch toàn bộ các tệp tin chẩn đoán tạm thời (`scratch/*.py`, `scratch/*.txt`) để giữ không gian làm việc gọn gàng.

---

## ⏳ Còn lại

1. **Chạy pipeline tạo Slide & Infographic cho Bài 5**:
   * File nguồn Markdown của Bài 5 đã có đầy đủ trong `output/hermes/bai5_nhiet_do_nhiet_ke/md/`.
   * Cần tạo notebook trên NotebookLM, tải các file nguồn lên, nhập prompt tạo slide deck/infographics và download về thư mục `ready/` (có thể dùng script tự động hóa tương tự Bài 6/7).

---

## 🔧 Quyết định quan trọng

| Quyết định | Lý do |
|---|---|
| Phục hồi mã nguồn qua phân tích log IDE | Đảm bảo lấy lại mã nguồn gốc chính xác 100% khi HEAD commit bị ghi đè phiên bản hỏng và không có remote GitHub để kéo về. |
| Giữ lại Bài 6 và Bài 7 ở dạng untracked | Khi khôi phục tệp hệ thống bằng `git restore .`, các thư mục bài học mới chưa theo dõi vẫn được bảo toàn nguyên vẹn trên đĩa. |

---

## ⚠️ Lưu ý cho session sau

- **Mã nguồn sạch**: Mọi tệp tin hệ thống hiện tại trong thư mục `engine/` và `skills/` đã được khôi phục về trạng thái chuẩn, hoạt động tốt.
- **Biên dịch Word**: Tool `scratch/compile_docx.py` hoạt động bình thường, biên dịch trực tiếp từ Markdown sang DOCX bằng font *UVN bai sau*.
- **Cách tiếp tục Bài 5**: Khi bắt đầu session mới, chỉ cần gõ `/recap` để khôi phục ngữ cảnh và triển khai pipeline cho Bài 5.

---

## 📁 Files quan trọng

| File | Vai trò |
|---|---|
| `.brain/brain.json` | Bộ nhớ dự án (kiến trúc, stack công nghệ, quy tắc, tiến độ cập nhật đến Bài 7) |
| `.brain/session.json` | Nhật ký tiến độ phiên làm việc hiện tại |
| `engine/main.py` | Entry point chính của GEMS Engine (đã khôi phục sạch sẽ) |
| `output/hermes/bai7_nhiet_hoa_hoi_rieng/` | Tài liệu đầu ra hoàn chỉnh Bài 7 |

---

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📍 Gõ /recap trong session mới để khôi phục context
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
