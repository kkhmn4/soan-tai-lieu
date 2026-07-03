---
name: awf-gems
description: |
  Điều phối và thực hiện quy trình thiết kế học liệu Vật lý GEMS v7.1 (Tối ưu Token & Tốc độ).
  Kích hoạt khi người dùng gõ /gems hoặc yêu cầu "soạn tài liệu", "tạo học liệu".
version: 7.1.0
---

# WORKFLOW: /gems - QUY TRÌNH BIÊN SOẠN HỌC LIỆU VẬT LÝ GEMS V7.1

## QUY TẮC TỐI ƯU HÓA HỆ THỐNG (BẮT BUỘC 100%)
*   **Tiết kiệm Token (Context & Output):**
    *   **Không sinh các ký tự lặp:** Tuyệt đối không để AI sinh dòng chấm dấu chấm thô `....`. Thay vào đó, bắt buộc sử dụng thẻ placeholder `[DOT_LINE_90]`. Script hậu kỳ `_generate_docx.py` sẽ tự động tìm và thay thế thẻ này thành dòng chấm 90 ký tự trong file Word.
    *   **Trích xuất tối giản (Selective Include):** Chỉ nạp thông tin cần thiết nhất (tên bài, tên ĐVKT) cho các bước sinh tiếp theo. Không nhồi nhét toàn bộ văn bản thô của bước trước vào prompt.
*   **Tách biệt Generative (LLM) và Deterministic (Code):**
    *   AI không trực tiếp lập trình/sinh mã TikZ dài hàng trăm dòng trong quy trình sinh văn bản học thuật chính. Thay vào đó, AI chỉ tạo nhãn yêu cầu hình vẽ dạng `[TIKZ_REQ: Mô tả sơ đồ cần vẽ]`. Việc sinh mã TikZ thực tế sẽ được chạy trong một prompt đơn lẻ hoặc do giáo viên tự thiết lập.
*   **Tối ưu hóa Điểm dừng (Pause Gates):**
    *   Gộp toàn bộ các bước dừng rời rạc lại thành 2 giai đoạn chính nhằm tránh việc AI phải nạp đi nạp lại lịch sử hội thoại (gây lãng phí Token đầu vào khổng lồ).

---

## TIẾN TRÌNH THỰC THI 3 BƯỚC

### BƯỚC 1: Phân tích sư phạm & Ma trận nội dung (Dừng duyệt 1)
*   **Nhiệm vụ:**
    1. Đọc và phân tích YCCĐ Vật lý theo chương trình GDPT 2018.
    2. Xác định các lỗi sai thường gặp (Misconceptions) của học sinh.
    3. Thiết lập bảng ma trận bài học gồm các Đơn vị Kiến thức (ĐVKT) và chuỗi nhiệm vụ luân phiên (12 loại hình nhiệm vụ mới).
    4. Lên danh sách mô tả hình ảnh cần thiết và đặt nhãn `[TIKZ_REQ: Mô tả hình vẽ]` cho các sơ đồ kỹ thuật.
*   **Sản phẩm:** Tệp đặc tả `output/[ten_bai]/md/GEMS_SPEC.md` và `output/[ten_bai]/md/lesson_matrix.json`.
*   **Hành động:** Xuất bản nội dung và **DỪNG LẠI ĐỢI DUYỆT.**
    *(Khi người dùng phê duyệt "OK" hoặc "Tiếp tục", hệ thống sẽ chạy tự động liền mạch toàn bộ các bước tiếp theo).*

### BƯỚC 2: Sinh Học Liệu Hàng Loạt (Chạy tự động)
*Hành động: Tự động tạo và ghi tất cả các tài liệu dưới đây vào thư mục của bài học mà không dừng lại.*

*   **2.1. Sinh Phiếu học tập (Worksheet - Student Version):**
    *   Triển khai chi tiết các nhiệm vụ học sinh theo ma trận.
    *   **Đồng bộ tiêu đề:** Tiêu đề của từng ĐVKT và từng nhiệm vụ phải đồng bộ hoàn toàn (khớp 1-1) với tiêu đề Slide.
    *   **Phần Mở rộng:** Bắt buộc có phần Mở rộng kiến thức (sau Vận dụng) về ứng dụng thực tế trong máy móc, thiết bị, hiện tượng tự nhiên,... tham khảo nguồn uy tín (sách, bài báo).
    *   Dùng các khoảng trống đục lỗ lý thuyết `(1), (2)` và thẻ `[DOT_LINE_90]` cho vùng viết bài.
    *   Ghi vào: `output/[ten_bai]/md/gems_worksheet_[ten_bai].md`.
*   **2.2. Sinh Slide Hướng dẫn giảng dạy (Slide Guide):**
    *   Đồng bộ 1-1 với Worksheet về cấu trúc và tiêu đề ĐVKT/nhiệm vụ. Cấu trúc 7 slide cho mỗi ĐVKT, giáo viên mặc định tên `Kha Khung Hiệp`, font chữ `"UVN bai sau"`.
    *   Slide thứ 7 của mỗi ĐVKT phải là slide **Mở rộng Kiến thức** giới thiệu ứng dụng thực tế (thiết bị, máy móc, tự nhiên) tương ứng và ghi rõ nguồn tham khảo uy tín.
    *   Ghi vào: `output/[ten_bai]/md/gems_slides_guide_[ten_bai].md`.
*   **2.3. Sinh Kế hoạch bài dạy (KHBD / Giáo án):**
    *   Xây dựng hoạt động giảng dạy chi tiết theo các ĐVKT, đồng bộ tiến trình với Worksheet và Slide.
    *   Bắt buộc có hoạt động dạy học hướng dẫn tìm hiểu phần **Mở rộng kiến thức** sau hoạt động Vận dụng cho từng ĐVKT.
    *   Ghi vào: `output/[ten_bai]/md/gems_lesson_plan_[ten_bai].md` (hoặc `GEMS_LESSON_PLAN.md`).
*   **2.4. Sinh Bài tập về nhà (Homework):**
    *   Biên soạn đúng cấu trúc 2025: Phần I (18 MCQ), Phần II (4 Đúng/Sai), Phần III (6 Trả lời ngắn).
    *   Ghi vào: `output/[ten_bai]/md/gems_homework_[ten_bai].md` và tệp đáp án chi tiết.


### BƯỚC 3: Xử lý Hậu kỳ & Kiểm định chất lượng QA (Chạy tự động)
*   **Nhiệm vụ:**
    1. **Tích hợp Tự động Google NotebookLM (CLI `nlm`):** Tự động xác thực tài khoản Google, tạo notebook, upload tài liệu nguồn, ra lệnh sinh Slide (.pptx) và Infographic (.png) rồi tải về máy.
    2. **Chuẩn hóa cấu trúc thư mục GEMS v7.1:** Gọi script `restructure_output.py` tự động di chuyển, đổi tên các tệp sang `md/`, `ready/`, `assets/` và ghi tệp `metadata.json`.
    3. **Chạy QA Self-Check Toàn diện:** 
       - Đối chiếu sản phẩm đầu ra với bộ 15 tiêu chí QA.
       - **Kiểm định Slide PPTX:** Đọc cấu trúc tệp XML trong PPTX để xác nhận phông chữ `"UVN bai sau"`, tên giáo viên `"Kha Khung Hiệp"`, cấu trúc bài giảng 7 slide/ĐVKT và tính thuần Việt 100%.
       - **Kiểm định Infographics:** Dùng Gemini Vision rà soát chéo tệp ảnh xem đã đục lỗ hợp lý (không chứa sẵn đáp án chốt, có ô trống để điền) và chính xác bản chất vật lý.
    4. **Biên dịch Word (.docx):** Gọi script `export_docx.py` biên dịch Markdown sang Word, tự động chuyển biểu thức thành native Office OMML và chuyển `[DOT_LINE_90]` thành dòng chấm thật.
*   **Sản phẩm:** File Word `.docx`, File Slide bài giảng `.pptx`, Infographics `.png`, tệp `metadata.json` và Báo cáo kiểm định QA toàn diện.
*   **Hành động:** Xuất báo cáo tổng kết tài nguyên và **KẾT THÚC WORKFLOW.**

*   **Hành động:** Xuất báo cáo tổng kết tài nguyên và **KẾT THÚC WORKFLOW.**