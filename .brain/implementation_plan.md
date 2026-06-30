# Kế hoạch điều chỉnh lỗi hiển thị và đồng bộ định dạng in ấn GEMS v8.1

Tài liệu này chi tiết kế hoạch sửa đổi các lỗi hiển thị thô (thẻ HTML `<br>`, ngắt dòng công thức nham nhở, đường dẫn hình ảnh thô) và tối ưu hóa typography theo chuẩn in ấn giáo dục Việt Nam (đối chiếu với file mẫu [Vật lý 11.docx.pdf](file:///c:/Users/Admin/.antigravity-ide/soạn tài liệu/tai-lieu-goc/Vật lý 11.docx.pdf)).

## Các lỗi hiển thị cần khắc phục

> [!WARNING]
> Các lỗi hiển thị dưới đây làm mất đi tính trang trọng và chuyên nghiệp của tài liệu khi trình nộp Ban Giám hiệu:
> 1. **Thẻ HTML thô:** Thẻ `<br>` xuất hiện trực tiếp trong văn bản Word.
> 2. **Lỗi ngắt dòng công thức:** Các ký hiệu toán học ngắn (`U`, `\Delta U = A + Q`) bị rơi xuống dòng riêng lẻ loi do parser coi mỗi dòng Markdown là một paragraph riêng biệt.
> 3. **Đường dẫn ảnh thô:** Đường dẫn ảnh dạng văn bản (ví dụ: `( ready/hinh_anh/do_thi_quy_uoc_dau.png )`) hiển thị thô thay vì được tự động nhúng ảnh vào Word.
> 4. **Dòng kẻ phân cách dính chữ:** Đường kẻ phân cách `---` dính sát vào tiêu đề hoạt động tiếp theo, không có khoảng giãn cách.
> 5. **Chưa có số trang:** Chưa có số trang động dạng `Trang X / Y` ở chân trang.

---

## Giải pháp đề xuất

### 1. Nâng cấp Exporter Parser (Gộp dòng liên tiếp)
Thay đổi logic đọc và parse Markdown của `khbd_exporter.py` và `pht_exporter.py`. Thay vì duyệt và tạo paragraph cho từng dòng đơn lẻ, chúng ta sẽ gộp các dòng văn bản liên tiếp (không bị phân tách bởi dòng trống) thành một paragraph duy nhất, trừ khi dòng đó là:
*   Tiêu đề (bắt đầu bằng `#`, `##`, `###`).
*   Danh sách (bắt đầu bằng `- `, `+ `, `* ` hoặc số thứ tự `1. `, `2. `).
*   Đường kẻ phân cách (`---`).
*   Bảng biểu (`|`).

### 2. Tiền xử lý văn bản (Text Sanitization)
*   **Loại bỏ thẻ HTML:** Sử dụng regex tự động xóa sạch các thẻ `<br>`, `<br/>`, `</br>` trước khi parse.
*   **Dọn dẹp LaTeX thô:** Chạy hàm `clean_latex` trên toàn bộ dòng văn bản thay vì chỉ chạy trong khối `$...$`, giúp các ký hiệu viết thô không có dấu `$` (như `\Delta U = A + Q`) vẫn hiển thị đẹp dưới dạng ký tự Unicode (như `ΔU = A + Q`).

### 3. Tự động phát hiện và nhúng ảnh
*   Quét dòng văn bản bằng regex để tìm các đường dẫn ảnh cục bộ kết thúc bằng `.png`, `.jpg`, `.jpeg`.
*   Nếu phát hiện đường dẫn ảnh, tự động tải/nhúng hình ảnh đó vào Word với kích thước cân đối (căn giữa) và xóa chuỗi đường dẫn text thô khỏi văn bản.

### 4. Đánh số trang chân trang động
*   Chèn footer động dạng `Trang PAGE / NUMPAGES` ở giữa chân trang cho tất cả các section của tài liệu Word.

---

## Proposed Changes

### [Component] Document Exporters

#### [MODIFY] [gems_styles.py](file:///C:/Users/Admin/.antigravity-ide/so%E1%BA%A1n%20t%C3%A0i%20li%E1%BB%87u/engine/gems_styles.py)
*   Bổ sung hàm `add_page_number_footer(doc)` chèn mã XML động đánh số trang chân trang.
*   Bổ sung regex làm sạch thẻ `<br>` trong `clean_latex`.

#### [MODIFY] [khbd_exporter.py](file:///C:/Users/Admin/.antigravity-ide/so%E1%BA%A1n%20t%C3%A0i%20li%E1%BB%87u/engine/khbd_exporter.py)
*   Cải tiến hàm `_parse_lines_to_doc` để tự động gộp các dòng văn bản liên tiếp thành một paragraph duy nhất.
*   Tích hợp tự động phát hiện đường dẫn ảnh thô để nhúng ảnh và làm sạch text.
*   Gọi `add_page_number_footer` trước khi lưu tài liệu.

#### [MODIFY] [pht_exporter.py](file:///C:/Users/Admin/.antigravity-ide/so%E1%BA%A1n%20t%C3%A0i%20li%E1%BB%87u/engine/pht_exporter.py)
*   Cải tiến logic phân tích đoạn và gộp dòng tương tự giáo án.
*   Gọi `add_page_number_footer` trước khi lưu tài liệu.

---

## Verification Plan

### Automated Tests
Chạy lệnh biên dịch DOCX và kiểm tra cấu trúc Paragraph:
```powershell
$env:PYTHONIOENCODING="utf-8"; python engine/main.py --docx-only -o output/hermes/bai3_noi_nang -l "Bài 3. Nội năng"
python scratch/check_final_docx_paragraphs.py
```
Đảm bảo kết quả in ra không còn các paragraph cụt và ký hiệu bị rơi dòng.

### Manual Verification
*   Chuyển đổi DOCX sang PDF bằng `convert_all_docx_to_pdf.py`.
*   Mở xem trực tiếp các file PDF để xác nhận không còn thẻ `<br>`, số trang hiển thị đúng ở footer và các ảnh đồ thị được nhúng ngay ngắn.
