---
name: gems_spec_generator_skill
description: |
  Kỹ năng chuyên biệt dành cho Chuyên gia Giáo dục môn Vật lý để phân tích sư phạm bài học, tạo ảnh học liệu, và thiết lập file định hướng chung (Spec) ở Bước 1 & Bước 2.
  Kích hoạt khi người dùng bắt đầu quy trình /gems hoặc nhập các lệnh: "phân tích sư phạm", "tạo spec", "lập spec", "bắt đầu bước 1", "bước 2".
version: 7.0.0
---

# Goal
Phân tích sư phạm bài học Vật lý bám sát sách giáo khoa Kết nối tri thức, xây dựng bảng ma trận nội dung Phiếu học tập và khung cấu trúc Bài tập về nhà Bộ GD&ĐT 2025, gọi công cụ tạo ảnh, và thiết lập nội dung định hướng chung tại docs/GEMS_SPEC.md theo định dạng GEMS_VAT_LY_V7_PRINT_WORKSHEET_FRAMEWORK.

# Instructions

## 🌟 BƯỚC 1: PHÂN TÍCH SƯ PHẠM & CHỌN PHONG CÁCH GEM

1. **Bắt buộc đọc tài liệu nguồn:** AI bắt buộc phải đọc sách giáo khoa gốc trong thư mục nguồn (ví dụ: `c:\Users\Admin\.antigravity-ide\soạn tài liệu\tai-lieu-goc\`) để lấy hệ thống đề mục, nội dung khoa học nguyên bản.

2. **Phân tích Yêu cầu cần đạt (YCCĐ):**
   - Trích xuất toàn bộ YCCĐ theo chương trình GDPT 2018 môn Vật lý từ chủ đề bài học.
   - Ví dụ: Bài "Nhiệt hóa hơi riêng":
     - YCCĐ 1: Định nghĩa 


















































     - **Nhánh 2 (Sơ đồ, đồ thị, sơ đồ quy trình, hình vẽ khoa học cần độ chính xác cao):** Sử dụng mã LaTeX TikZ để vẽ hình. Sử dụng script `scripts/compile_tikz.py` để biên dịch mã TikZ này thành ảnh `.png` và lưu vào thư mục `docs/images/` hoặc `resources/images/`. Bản thân mã TikZ này phải khai báo đầy đủ các thư viện và gói bổ trợ cần thiết trong Vật lý, Toán học và Hóa học (như `circuitikz` cho mạch điện, `chemfig` cho cấu trúc hóa học, và các thư viện TikZ nâng cao như `arrows.meta`, `decorations.pathreplacing`, `decorations.pathmorphing`, `decorations.markings`, `intersections`, `backgrounds`, `shadows`, `angles`, `quotes`, `3d`, `perspective`, `folding`, `spy`).
   - Định nghĩa tag ảnh dạng `[TAG_ANH_XX]` kèm đường dẫn tuyệt đối, mô tả chi tiết hình ảnh, và mã nguồn TikZ tương ứng (nếu thuộc Nhánh 2) trong file định hướng `docs/GEMS_SPEC.md`.

5. **Hành động (Chế độ Từng bước):** Ghi toàn bộ nội dung Spec & Ma trận vào `docs/GEMS_SPEC.md`. Dừng lại đợi duyệt.

# Constraints
- 🚫 KHÔNG sử dụng các từ ngữ mơ hồ như "xử lý", "tối ưu", "phù hợp", "đầy đủ", "chính xác", "kiểm tra", "chuẩn", "nhiều", "lớn".
- 🚫 KHÔNG sử dụng bất kỳ từ tiếng Anh hoặc chú thích tiếng Anh nào trong tài liệu chính (100% thuần Việt).
- ✅ Toàn bộ biểu thức toán học được viết dưới dạng LaTeX đặt trong dấu đô la đơn: `$công_thức$`. Ký hiệu động năng là `$W_đ$`, thế năng là `$W_t$`.
