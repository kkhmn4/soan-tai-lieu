# NOTEBOOKLM PROMPT TẠO SLIDE BÀI GIẢNG - Bài 7 - Nhiệt hóa hơi riêng
> **HƯỚNG DẪN:** Hãy sao chép toàn bộ nội dung dưới đây và dán trực tiếp vào khung chat của Google NotebookLM sau khi đã tải các tệp tài liệu nguồn (`bai7_nhiet_hoa_hoi_rieng_dac_ta_gems.md`, `bai7_nhiet_hoa_hoi_rieng_ke_hoach_bai_day.md`, `bai7_nhiet_hoa_hoi_rieng_phieu_hoc_tap.md`, `bai7_nhiet_hoa_hoi_rieng_huong_dan_slide.md`) làm sources.

---

## NỘI DUNG PROMPT NẠP CHO NOTEBOOKLM (TẠO SLIDE BÀI GIẢNG)

Bạn là một trợ lý thiết kế bài giảng chuyên nghiệp theo hệ thống tiêu chuẩn GEMS v9.0. Hãy dựa trên các tài liệu nguồn đã được tải lên để thực hiện nhiệm vụ sau:

### NHIỆM VỤ: XÂY DỰNG CẤU TRÚC CHI TIẾT CỦA BỘ SLIDE BÀI GIẢNG (SLIDE DECK)
1. **Yêu cầu nội dung & Đặt tên Slide dễ hiểu:**
   - Tạo cấu trúc slide chi tiết khớp hoàn toàn 1-1 với bảng outline trong tệp `bai7_nhiet_hoa_hoi_rieng_huong_dan_slide.md`.
   - **Số mục phải khớp chính xác với PHT nguồn:** dùng đúng số Đơn vị kiến thức (mục 1, 2...) và
     số tiểu mục X.Y đã có trong `bai7_nhiet_hoa_hoi_rieng_phieu_hoc_tap.md` và bảng outline trong
     `bai7_nhiet_hoa_hoi_rieng_huong_dan_slide.md` — tuyệt đối không tự đặt số khác hay đảo thứ tự.
   - Tách biệt hoàn toàn giữa **Slide Nhiệm vụ (không chứa đáp án)** và **Slide Đáp án (xuất hiện ngay tiếp sau)**.
   - Slide Trang Bìa (Slide Mở đầu) ghi rõ giáo viên thực hiện: **Kha Khung Hiệp**.
   - Nhiệm vụ nào có dòng "*Hướng dẫn thực hiện: ...*" trong PHT nguồn (hình thức cá nhân/nhóm,
     thời gian, tài liệu dùng) thì PHẢI hiển thị đúng nguyên văn dòng đó lên slide/infographic
     tương ứng, đặt ở vị trí dễ thấy (ví dụ góc trên khung nhiệm vụ) — không được bỏ qua hoặc tự
     diễn đạt lại khác.
   - **Tên Slide và nhãn nhiệm vụ phải thuần Việt 100%:**
     - Thay thế hoàn toàn "Assertion Reasoning" -> "Nhận định & Lý do"
     - Thay thế hoàn toàn "Matching Matrix" -> "Ghép nối đa biến"
     - Thay thế hoàn toàn "Bug Buster" -> "Tìm và sửa lỗi vật lý"
     - Thay thế hoàn toàn "Algorithmic Ordering" -> "Sắp xếp tiến trình"
     - Thay thế hoàn toàn "Visual Cloze Test" -> "Điền khuyết trực quan"
   - Highlight đậm và làm nổi bật các từ khóa định nghĩa, công thức toán lý bằng nhãn chú thích rõ ràng.
   - **Yêu cầu bắt buộc:** Toàn bộ tiêu đề, nội dung slide, câu hỏi và đáp án phải hiển thị 100% bằng tiếng Việt chính xác theo tệp nguồn. Tuyệt đối không tự ý dịch sang tiếng Anh.

2. **Yêu cầu Thiết kế và Giao diện (Theme & Design Sync):**
   - **Tông màu chủ đạo (thương hiệu Anthropic):** Dark `#141413` cho tiêu đề/chữ chính, Light
     `#FAF9F5` cho nền — đây là bảng màu Slide/Infographic, KHÁC với Primary `#1F4E79` chỉ dùng
     trong PHT/KHBD/Bài tập về nhà bản Word (có chủ đích, không phải nhầm lẫn).
   - **Tông màu nhấn:** luân phiên Orange `#D97757` (nhấn chính), Blue `#6A9BCC`, Green `#788C5D`
     cho khung/hình dạng/icon không phải khối chữ lớn — tạo điểm nhấn tinh tế, không sặc sỡ.
   - **Tông màu nền phụ:** Light Gray `#E8E6DC` cho hộp ghi chú/hộp gợi ý; Mid Gray `#B0AEA5` cho
     chi tiết phụ/đường viền mờ. Chỉ dùng màu vàng `#FFD600` để highlight từ khóa định nghĩa/công
     thức ngay trong dòng chữ, không dùng làm nền lớn.
   - **Phông chữ (thương hiệu Anthropic):** tiêu đề dùng **Poppins** (dự phòng Arial nếu máy không
     có sẵn font), thân bài dùng **Lora** (dự phòng Georgia) — không dùng Times New Roman (đó là
     font riêng của bản Word).
   - Tiêu đề đậm cỡ lớn dễ đọc từ xa, thân bài rõ ràng, phân cấp thông tin rành mạch.
   - **Khung/hộp (hộp ghi nhớ, hộp gợi ý, khung nhiệm vụ):** viền mảnh, bo góc nhẹ, không đổ bóng
     nặng, không dùng gradient sặc sỡ — phong cách nghiêm túc như sách giáo khoa/tài liệu khoa học,
     không phải slide quảng cáo hay poster sự kiện.
   - **Ảnh minh họa phải chính xác khoa học, KHÔNG được hoạt hình:** cấm tuyệt đối phong cách
     hoạt hình/cartoon, 3D ảo, phóng đại phi thực tế hoặc "vẽ chơi". Ưu tiên tuyệt đối:
     (a) dùng lại nguyên trạng các ảnh sơ đồ đã có sẵn trong PHT nguồn (đường dẫn `ready/hinh_anh/...`)
     thay vì tự vẽ lại; nếu phải vẽ mới, chỉ vẽ dạng sơ đồ kỹ thuật đường nét (line-art) có nhãn/mũi
     tên như hình vẽ trong sách giáo khoa Vật Lý — tỉ lệ hợp lý, đúng bản chất vật lý, không thêm
     chi tiết trang trí không liên quan.
   - Mọi chữ/nhãn/chú thích xuất hiện trên ảnh minh họa phải bằng tiếng Việt.
   - **Bố cục:** Đảm bảo tỷ lệ khoảng trống (white space) tối thiểu từ 35-40% trên mỗi slide, không nhồi nhét chữ (tối đa 6-8 dòng chữ mỗi slide), nền sáng chữ tối. Chừa khoảng trống hợp lý ở phần bên phải để tích hợp hình ảnh minh họa.

3. **Các quy tắc thiết kế bắt buộc bổ sung trích xuất trực tiếp từ file hướng dẫn slide:**
   - Phân cấp tiêu đề slide có mã số X.Y đúng theo bảng outline bên dưới — không tự đặt số khác.
   - Tách biệt hoàn toàn slide Nhiệm vụ và slide Đáp án — không gộp chung 1 slide.
   - Ngôn ngữ thuần Việt 100%.
   - Màu chủ đạo Primary `#1F4E79` cho tiêu đề/khung/đường kẻ; màu xám nhạt `#D9D9D9` cho nền hộp ghi chú/hộp gợi ý; dùng màu vàng `#FFD600` chỉ để highlight từ khóa định nghĩa/công thức.
   - Font Times New Roman thống nhất; tiêu đề đậm cỡ lớn, thân bài rõ ràng dễ đọc từ xa.
   - Khung/hộp (hộp ghi nhớ, hộp gợi ý, khung nhiệm vụ) dùng viền mảnh, bo góc nhẹ, không đổ bóng nặng — phong cách nghiêm túc như sách giáo khoa, không phải slide quảng cáo.
   - Tối đa 6-8 dòng chữ mỗi slide, nền sáng, chừa khoảng trống 35-40% cho hình minh họa.
   - Ảnh minh họa bắt buộc chính xác khoa học — cấm hoạt hình/3D ảo/phóng đại phi thực tế; ưu tiên sơ đồ dạng đường nét (line-art) có nhãn/mũi tên như hình vẽ SGK Vật Lý, hoặc dùng trực tiếp các ảnh sơ đồ đã có sẵn trong Phiếu học tập nguồn (đường dẫn `ready/hinh_anh/...`) thay vì tự vẽ lại. Mọi chú thích trên ảnh phải bằng tiếng Việt.
   - Slide Nhiệm vụ phải hiển thị kèm dòng "Hướng dẫn thực hiện" (hình thức/thời gian/tài liệu) lấy đúng nguyên văn từ Phiếu học tập nguồn — không tự bịa nội dung khác.
