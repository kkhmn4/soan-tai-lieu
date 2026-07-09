# ĐẶC TẢ NÂNG CẤP BỘ TÀI LIỆU — BÀI 28: ĐỘNG LƯỢNG

> File này mô tả CHÍNH XÁC những gì sẽ được tạo ra ở vòng nâng cấp tiếp theo,
> theo 4 yêu cầu điều chỉnh. Đọc và xác nhận (hoặc yêu cầu sửa) trước khi các
> bước tạo hàng loạt (vẽ ảnh, dựng script, chạy NotebookLM) được thực hiện.

---

## 1. Tóm tắt 4 thay đổi

1. **Bỏ 4 ảnh Infographic rời rạc** (từng lệch màu/layout giữa các ảnh do
   NotebookLM vẽ độc lập từng ảnh) → thay bằng **1 bộ Slide "Phiếu học tập"**
   dựng thống nhất trong cùng 1 lần sinh, đủ tên bài / tên học sinh / toàn bộ
   nhiệm vụ — đồng bộ tuyệt đối về font, màu, layout giữa các slide.
2. **Tách 2 bộ slide dùng cho 2 mục đích khác nhau**, dùng chung 1 bộ ảnh
   minh họa (chỉ khác tông màu):
   - **Slide GIÁO VIÊN** (trình chiếu cả lớp): slide Nhiệm vụ chỉ ghi
     **Hướng dẫn thực hiện** (hình thức/thời gian/tài liệu) — KHÔNG in lại
     câu hỏi (học sinh tự đọc câu hỏi trên PHT giấy của mình). Slide Đáp án
     chỉ có đáp án + ảnh minh họa — KHÔNG in lại hướng dẫn. Nền có màu sắc,
     đồ họa bắt mắt (theme Anthropic).
   - **Slide PHIẾU HỌC TẬP học sinh** (bản chiếu/số hóa của PHT giấy): slide
     Nhiệm vụ có ĐẦY ĐỦ hướng dẫn + câu hỏi (giống hệt PHT giấy). Slide Đáp
     án cũng chỉ có đáp án + ảnh (không hướng dẫn). Nền TRẮNG, ảnh minh họa
     chỉ dùng tông TRẮNG/ĐEN/XÁM (không màu).
3. **Đa dạng hoá loại hình nhiệm vụ** — rà soát lại 5 nhiệm vụ NV1–NV5, chọn
   từ đúng 12 loại hình trong `skills/gems_physics_skill.md`, không lặp loại
   hình, bám sát kiến thức + mục tiêu cần đạt, tránh nhiệm vụ đơn điệu.
4. **Dừng lại ở bước đặc tả này** — sau khi bạn xác nhận, mới chạy hàng loạt:
   vẽ lại ảnh minh họa (2 tông màu), dựng script, chạy NotebookLM sinh 2 bộ
   slide, xoá 4 ảnh infographic cũ.

---

## 2. Ma trận nhiệm vụ học tập (đa dạng hoá 12 loại hình GEMS)

| Mã | Vị trí trong PHT | Tên nhiệm vụ | Loại hình (trong 12 loại GEMS) | Kiến thức/mục tiêu nhắm tới | Vì sao chọn loại hình này |
|---|---|---|---|---|---|
| NV1 | 1. Khởi động | Xe nào khó dừng hơn? Bóng nào khó bắt hơn? | **Trắc nghiệm bối cảnh** (Contextual MCQ) — dạng lựa chọn nhị phân mở bài | Huy động trực giác, dẫn nhập khái niệm động lượng | Tình huống thực tế 2 lựa chọn, phù hợp khởi động nhẹ nhàng, không cần lý thuyết trước |
| NV2 | 2.1 Động lượng | Đúng hay sai về động lượng? | **Đúng/Sai có biện giải** (Assertion Reasoning) | Định nghĩa, đơn vị, tính vectơ, yếu tố quyết định độ lớn | Buộc học sinh biện giải đúng/sai từng ý — bắt lỗi quan niệm sai (M1, M2) hiệu quả hơn MCQ thường |
| NV3 | 2.2 Xung lượng (Nhiệm vụ 1) | Đọc đồ thị lực – thời gian | **Khai thác Infographic** (Infographic Decryption) | Xung lượng = diện tích đồ thị F-t | Rèn kỹ năng đọc/trích xuất thông tin từ biểu đồ trực quan — khác hẳn dạng hỏi-đáp thuần chữ |
| NV4 | 2.2 Xung lượng (Nhiệm vụ 2) | Suy luận công thức liên hệ | **Xây dựng mô hình** (Model Builder) | F.Δt = Δp; dạng tổng quát định luật II Newton | Học sinh tự suy luận từng bước từ định luật đã học để "xây" ra công thức mới — tư duy bậc cao, không học vẹt |
| NV5 | 4.2 Vận dụng | Bắt lỗi thiết kế: Mũ bảo hiểm lót thép | **Gỡ lỗi thiết kế kỹ thuật** (Engineering Debugger) | Vận dụng F=Δp/Δt để phân tích an toàn kỹ thuật | Tình huống kỹ thuật có "lỗi cài sẵn" cần học sinh phát hiện — vận dụng sáng tạo, không lặp lại tính toán đơn thuần |

**Nhận xét đa dạng:** 5 nhiệm vụ dùng 5 loại hình khác nhau trong số 12 loại
(không lặp lại loại nào), trải đều từ khởi động → khám phá lý thuyết →
suy luận công thức → vận dụng kỹ thuật. Nếu bạn muốn thay loại hình nào
(ví dụ đổi NV1 sang **Sắp xếp tiến trình**/Algorithmic Ordering hoặc **Điền
khuyết trực quan**/Visual Cloze Test), cho biết cụ thể ở bước duyệt.

*(Mục 3.1/3.2 Luyện tập và mục 4.1/4.2.b Mở rộng KHÔNG tính vào bảng này —
theo đúng chuẩn skill, mục Luyện tập bám phong cách câu hỏi đề thi tốt
nghiệp THPT [trắc nghiệm/Đúng-Sai/trả lời ngắn], không thuộc 12 loại hình
nhiệm vụ khám phá; mục Mở rộng là đoạn đọc thêm, không phải nhiệm vụ.)*

---

## 3. Ma trận cấu trúc từng tài liệu

| Tài liệu | Trạng thái | Nhiệm vụ hiển thị | Đáp án hiển thị | Nền / màu sắc | Ảnh minh họa |
|---|---|---|---|---|---|
| **KHBD** (`..._ke_hoach_bai_day.docx`) | Đã có, giữ nguyên cấu trúc, chỉ cập nhật câu chữ "Chuẩn bị của giáo viên" để nhắc đến 2 bộ slide mới | — (tài liệu giáo viên, không phải slide) | — | Trắng, Times New Roman, mẫu Đinh Thiện Lý | 3 ảnh bản MÀU (đồng bộ với slide GV) |
| **PHT giấy** (`..._phieu_hoc_tap.docx`) | Đã có, giữ nguyên | Hướng dẫn + câu hỏi đầy đủ | Không có đáp án (học sinh tự làm) | Trắng, Times New Roman | 3 ảnh bản TRẮNG/ĐEN/XÁM (đã đúng chuẩn từ trước — vẽ matplotlib 2 màu) |
| **Bài tập về nhà** (`..._bai_tap_ve_nha.docx`) | Đã có, giữ nguyên | Câu hỏi đầy đủ | Đáp án tách trang cuối file | Trắng | Không cần ảnh mới |
| **Slide GIÁO VIÊN** (mới — thay thế phần "slide bài giảng" trước đó) | **Sẽ tạo** | CHỈ Hướng dẫn thực hiện (hình thức/thời gian/tài liệu) — KHÔNG in câu hỏi | CHỈ đáp án + ảnh minh họa — KHÔNG in lại hướng dẫn | Có màu, đồ họa đẹp/thu hút (theme Anthropic: Dark/Light + Orange/Blue/Green, Poppins/Lora) | 3 ảnh bản MÀU (cùng nội dung/layout với bản PHT, chỉ khác tông màu) |
| **Slide PHIẾU HỌC TẬP học sinh** (mới — thay thế 4 ảnh Infographic) | **Sẽ tạo** | Hướng dẫn + câu hỏi đầy đủ (y hệt PHT giấy) — đủ tên bài, tên học sinh, tất cả nhiệm vụ 1→2.1→2.2→3.1→3.2→4.1→4.2 | CHỈ đáp án + ảnh minh họa — KHÔNG in lại hướng dẫn | **Nền TRẮNG**, chữ đen, tối giản như trang giấy | 3 ảnh bản TRẮNG/ĐEN/XÁM — **giống hệt nội dung/layout ảnh dùng ở Slide Giáo viên**, chỉ khác là không màu |

**Ảnh minh họa dùng chung (cần vẽ lại 2 phiên bản màu từ 3 ảnh matplotlib đã có):**

| Ảnh | Dùng ở mục | Phiên bản màu (Slide GV) | Phiên bản trắng/đen/xám (PHT giấy + Slide PHT) |
|---|---|---|---|
| Vectơ động lượng (p = m.v) | 2.1 | Cam/Xanh dương Anthropic | Đã có sẵn (matplotlib, trắng/xám/đen) |
| Đồ thị lực – thời gian | 2.2 | Cam/Vàng nhấn Anthropic | Đã có sẵn |
| Sơ đồ bóng va chạm tường | 2.1 (minh hoạ vectơ đổi chiều) | Xanh dương/Đỏ Anthropic | Đã có sẵn |

---

## 4. Việc sẽ làm SAU KHI bạn xác nhận file này

1. Vẽ thêm phiên bản MÀU (theme Anthropic) cho 3 ảnh minh họa — giữ nguyên bố cục/nội dung như bản trắng/đen/xám hiện có, chỉ đổi bảng màu.
2. Viết prompt + dựng outline cho 2 bộ slide (Giáo viên / Phiếu học tập học sinh) theo đúng bảng mục 3.
3. Chạy NotebookLM sinh 2 bộ slide (`.pptx`), xoá 4 file `infographic_muc_*.png` cũ.
4. Xác minh trực quan cả 2 bộ slide (nhất quán ảnh, đúng phân vai nhiệm vụ/đáp án, đúng màu nền).

**Xin xác nhận:** bảng đa dạng hoá nhiệm vụ (mục 2) và ma trận tài liệu (mục
3) đã đúng ý bạn chưa, hay cần chỉnh gì trước khi tôi làm hàng loạt các bước
ở mục 4?
