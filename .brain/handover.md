# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 HANDOVER DOCUMENT – GEMS Physics Pipeline
# Lưu lúc: 2026-06-30T22:15:00+07:00
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📍 Đang làm gì

**Dự án:** GEMS Physics – Hệ thống tự động biên soạn và xuất bản học liệu Vật lý 12  
**Bước tiếp theo:** 
1. Đợi hoàn tất quá trình tải Slide (PPTX/PDF) và Infographic (PNG) cho Bài 2 (Sự chuyển thế) từ Google NotebookLM Cloud (quy trình Smart Polling đang chạy ngầm).
2. Chạy pipeline sinh học liệu và NotebookLM cho Bài 5 (Nhiệt độ. Thang nhiệt độ. Nhiệt kế) để hoàn thành toàn bộ chương Nhiệt học.

---

## ✅ Đã hoàn thành

- [x] **Tái cấu trúc thư mục toàn dự án:** Loại bỏ thư mục trung gian `hermes`, đưa toàn bộ các thư mục bài học (`bai2` đến `bai7`) ra trực tiếp thư mục `output/` để tối giản hóa đường dẫn.
- [x] **Dọn dẹp thư mục gốc cực sạch:** Di chuyển tất cả tài liệu rời rạc vào `docs/reference/` và `docs/diagrams/`, chuyển các script thử nghiệm/nháp cũ vào `scratch/`, và di chuyển các file YCCĐ thô vào `tai-lieu-goc/`.
- [x] **Thiết lập và đẩy dự án lên GitHub:** Tạo repository mới và đẩy toàn bộ mã nguồn sạch của dự án lên GitHub cá nhân của bạn tại [https://github.com/kkhmn4/soan-tai-lieu.git](https://github.com/kkhmn4/soan-tai-lieu.git) thành công.
- [x] **Dọn dẹp tệp nháp lập trình viên:** Xóa bỏ hơn 100 tệp tin nháp, tệp chẩn đoán và tệp sao lưu thừa trong `scratch/`, chỉ giữ lại 2 tập lệnh tự động hóa cốt lõi. Xóa bỏ thư mục `TEST/` trống và thư mục `brain/` thừa ở thư mục gốc.
- [x] **Tạo lại Bài 2 (Sự chuyển thế):** Biên dịch thành công 3/3 tệp Word (.docx) chuẩn quy định GEMS v8.0, kích hoạt quy trình upload và tự động sinh Slide + Infographic trên Google NotebookLM Cloud với cơ chế Smart Polling 5 phút.

---

## ⏳ Còn lại

1. **Kiểm tra và hoàn tất tải về Bài 2:**
   * Script `generate_notebook_materials.py` đang chạy và kiểm tra trạng thái Slide trên Cloud.
   * Sau khi hoàn tất, slide và infographic sẽ nằm gọn gàng tại `output/bai2_su_chuyen_the/ready/`.
2. **Triển khai sinh học liệu cho Bài 5 (Nhiệt độ. Thang nhiệt độ. Nhiệt kế):**
   * Các tệp tin markdown nguồn của bài 5 đã có sẵn trong `output/bai5_nhiet_do_nhiet_ke/md/`.
   * Cần chạy biên dịch DOCX và sau đó chạy `python scratch/generate_notebook_materials.py --lesson "Bài 5"`.

---

## 🔧 Quyết định quan trọng

| Quyết định | Lý do |
|---|---|
| Loại bỏ thư mục `hermes/` | Cải tiến cấu trúc thư mục theo yêu cầu trực tiếp của người dùng để tài nguyên học liệu nằm gọn gàng hơn ngay dưới `output/`. |
| Script PowerShell định dạng ASCII | Khắc phục lỗi định dạng chuỗi (`FormatError`) do lỗi font chữ tiếng Việt/emoji của PowerShell trên Windows khi chạy lệnh đồng bộ GitHub. |

---

## 📁 Files quan trọng

| File | Vai trò |
|---|---|
| `readme.md` | Tài liệu hướng dẫn chính toàn dự án (đã viết lại hoàn chỉnh theo GEMS v8.0) |
| `docs/diagrams/gems_agent_pipeline.mmd` | Sơ đồ luồng hoạt động chi tiết của GEMS Agent |
| `scratch/generate_notebook_materials.py` | Kịch bản điều phối trung tâm tự động hóa NotebookLM |
| `scratch/create_and_push.ps1` | Tập lệnh hỗ trợ đăng nhập và đồng bộ GitHub (bằng ASCII) |
| `.brain/brain.json` & `session.json` | Bộ nhớ tĩnh và nhật ký hoạt động động của Agent |

---

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📍 Gõ /recap trong session mới để khôi phục context
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
