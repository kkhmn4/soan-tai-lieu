# GEMS Physics Material Generation Engine — Hướng dẫn tập tin Python

Thư mục này chứa các tập tin mã nguồn Python thực thi của hệ sinh thái GEMS Physics. Dưới đây là cách sắp xếp các tệp tin theo quy trình làm việc từng bước:

---

## 🛠️ Bản đồ tập tin theo Quy trình làm việc GEMS

```
YCCĐ (SGK)
   │
   ├── [GĐ 1: Điều phối chính]
   │    ├── gems_orchestrator.py (Chạy hàng loạt nhiều bài học)
   │    └── main.py              (Chạy đơn lẻ một bài học)
   │
   ├── [GĐ 2: Phân tích & Sinh nội dung]
   │    ├── gems_analyzer.py     (Phân tích sư phạm & Lập ma trận GEMS)
   │    ├── worksheet_generator.py (Sinh phiếu học tập PHT)
   │    └── homework_generator.py (Sinh bài tập về nhà LaTeX)
   │
   ├── [GĐ 3: Xuất bản & Hậu kỳ]
   │    ├── export_docx.py       (Xuất bản file Word chuẩn hóa)
   │    ├── image_renderer.py    (Tải ảnh minh họa / vẽ sơ đồ)
   │    └── compile_tikz.py      (Biên dịch công thức hình học TikZ sang PNG)
   │
   ├── [GĐ 4: Tích hợp NotebookLM]
   │    └── (Sử dụng run_nlm.ps1 hoặc generate_notebook_materials.py)
   │
   └── [GĐ 5: Chuẩn hóa & Rà soát QA]
        ├── restructure_output.py (Sắp xếp tệp tin vào md/, ready/, 


















* **[image_renderer.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/image_renderer.py):** Quản lý tìm kiếm hình ảnh minh họa từ web và nạp prompt vẽ ảnh bằng các mô hình AI.
* **[compile_tikz.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/compile_tikz.py):** Tự động phát hiện và trích xuất mã TikZ từ bài tập về nhà LaTeX để biên dịch thành file ảnh PNG trực quan.

### 4. Chuẩn hóa & Kiểm định (Quality Assurance & Post-Process)
* **[restructure_output.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/restructure_output.py):** Script chuẩn hóa cấu trúc đầu ra của học liệu, phân loại file vào đúng thư mục con và nhận diện ảnh infographic dọc theo ĐVKT.
* **[quality_checker.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/quality_checker.py):** Tự động kiểm tra chất lượng sư phạm của PHT và bài tập về nhà dựa trên 15 tiêu chí kiểm định.

### 5. Tiện ích bổ trợ (Utilities)
* **[dry_run.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/dry_run.py):** Kịch bản chạy thử nghiệm ngoại tuyến (offline) để trình diễn tính năng mà không tiêu tốn Token/gọi API ngoài.
* **[setup_dirs.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/setup_dirs.py):** Khởi tạo cấu trúc thư mục làm việc mặc định.
* **[read_docx.py](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/engine/read_docx.py):** Tiện ích hỗ trợ đọc dữ liệu thô từ file Word.
