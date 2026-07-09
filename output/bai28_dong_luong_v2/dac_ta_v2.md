# ĐẶC TẢ V2 — BÀI 28: ĐỘNG LƯỢNG (Vật Lý 10, one-off)

> Bản dựng lại từ đầu của `output/bai28_dong_luong/` (V1), lưu riêng vào `output/bai28_dong_luong_v2/`,
> không ghi đè V1. Dùng lại thư viện `gems.docx_export`/`gems.notebooklm`, KHÔNG đụng `gems/` hay
> `curriculum.yaml` (one-off, đúng ràng buộc đã chốt ở Phần C tài liệu `yeu_cau_du_an_chi_tiet.md`).

## 0.1 Cập nhật quan trọng (sau vòng phản hồi 1 — GHI ĐÈ các mục liên quan bên dưới)
- **Bài 28 dạy trong 2 TIẾT**, không gộp 1 tiết như bản nháp đầu: **Tiết 1 = "I. Động lượng"**,
  **Tiết 2 = "II. Xung lượng của lực"**. Mỗi tiết là 1 giáo án CV5512 đầy đủ (Khởi động → Hình thành
  kiến thức mới → Luyện tập → Vận dụng).
- **Tiết dạy minh họa (được đánh giá theo bảng tiêu chí) là TIẾT 1** — đầu tư chất lượng cao nhất cho
  tiết này; Tiết 2 vẫn soạn đầy đủ nhưng không phải trọng tâm chấm.
- **Khởi động Tiết 1 đổi sang trò chơi AR "Bảo vệ hành tinh xanh"**: học sinh dùng tay điều khiển tên
  lửa bắn thiên thạch để đổi hướng, tránh va chạm Trái Đất. Sau trò chơi, rút ra vấn đề "tên lửa khối
  lượng lớn + vận tốc lớn làm thiên thạch lệch hướng nhiều hơn" → dẫn vào khái niệm động lượng, sau đó
  khám phá qua thí nghiệm thực tế (3 viên bi).
- **Đa dạng hoá lại loại hình nhiệm vụ, ưu tiên loại hình gây hào hứng** (đáp ứng tiêu chí đánh giá phần
  giảng dạy: "học sinh hào hứng tham gia, tương tác tích cực") — tránh dùng liên tiếp loại hình khô khan
  (đúng/sai) nhiều lần liền nhau trong cùng 1 tiết. Xem bảng nhiệm vụ mới ở mục 3.

## 0. Vì sao làm lại (V2 khác V1 ở đâu)
- Người dùng cung cấp lại nguyên văn **Mục tiêu** (I. Kiến thức + I. Phát triển năng lực) — dùng làm
  nguồn CHUẨN duy nhất cho mục tiêu bài học ở KHBD (khác V1 vốn tự soạn mục tiêu).
- Áp dụng rõ ràng bảng **TIÊU CHÍ ĐÁNH GIÁ** (Trường Đinh Thiện Lý) làm khung tự-kiểm trước khi hoàn
  thiện — V1 không đối chiếu tường minh với bảng này. 3 tiêu chí chấm giáo án cần đạt mức 4 (Giỏi):
  1. **Mục tiêu bài học**: cụ thể/rõ ràng/khả thi + có mở rộng/liên hệ thực tiễn **phù hợp** (không
     gượng ép).
  2. **Phương pháp giảng dạy**: mọi hoạt động bám sát mục tiêu, **liên kết chặt chẽ** với nhau (hoạt
     động sau kế thừa hoạt động trước), phát triển **tư duy bậc cao** + **năng lực học tập hợp tác**.
  3. **Biện pháp kiểm tra – đánh giá**: có phương thức đánh giá **phù hợp, hiệu quả, khả thi** sau MỖI
     hoạt động (không chỉ đánh giá cuối bài).
- Kế thừa nguyên vẹn các bài học kỹ thuật đã rút ra ở V1 (xem `docs/reference/yeu_cau_du_an_chi_tiet.md`
  Phần C.6): tránh prompt NotebookLM quá dài/nhiều slide một lượt (rủi ro cắt ngang), đánh số "SLIDE
  N:" tường minh, không dùng dấu ngoặc vuông làm placeholder, luôn tự đếm số slide thật bằng
  `python-pptx` sau khi tải.

## 1. Mục tiêu bài học (nguồn: người dùng cung cấp, giữ nguyên văn)

**1. Kiến thức**
- Phát biểu được định nghĩa của động lượng và nêu được ý nghĩa vật lí của đại lượng đó.
- Phát biểu và viết được công thức liên hệ giữa lực tác dụng lên vật và tốc độ biến thiên của động
  lượng (thường được gọi là dạng thứ 2 của định luật II Newton).

**2. Phát triển năng lực**
- *Năng lực chung:*
  - Tự học: chủ động tích cực thực hiện công việc bản thân, đóng góp ý tưởng, đặt câu hỏi, trả lời yêu cầu.
  - Giao tiếp và hợp tác: khiêm tốn tiếp thu góp ý, nhiệt tình chia sẻ/hỗ trợ thành viên nhóm.
- *Năng lực vật lí:*
  - Nêu được ý nghĩa vật lí và định nghĩa động lượng.
  - Phát biểu được mối liên hệ giữa lực tác dụng lên vật và tốc độ biến thiên của động lượng.
  - Viết được công thức liên hệ giữa lực tác dụng lên vật và tốc độ biến thiên của động lượng.

Thời lượng: **1 tiết (45 phút)**, gộp cả 2 yêu cầu cần đạt (định nghĩa động lượng + dạng 2 định luật II
Newton), bám sát SGK trang 110-112 (thí nghiệm Hình 28.1 ba viên bi, ví dụ xe tải/xe con, sút phạt bóng
đá, vợt bóng tennis Hình 28.2).

## 2. Bộ 5 tài liệu (giữ nguyên cấu trúc đã chốt ở V1)

| # | Tài liệu | Công cụ dựng | Nguồn định dạng |
|---|---|---|---|
| 1 | KHBD (.docx) | Script Python riêng, bảng 5 cột Hoạt động/Mục tiêu/Chi tiết hoạt động/Nội dung kiến thức/Ghi chú, landscape | `tai-lieu-goc/KẾ HOẠCH GIẢNG DẠY.docx` (mẫu thật, đã đọc: bảng thông tin 8 dòng + bảng hoạt động 5 cột) |
| 2 | PHT (.docx) | Script custom (không dùng `pht_exporter.py` của GEMS) | Cấu trúc 4 mục: Khởi động/Hình thành kiến thức mới (2.1, 2.2)/Luyện tập (3.1, 3.2)/Vận dụng-Mở rộng (4.1, 4.2) |
| 3 | Bài tập về nhà (.docx) | Tái dùng `gems.docx_export.homework_exporter` | Chuẩn GEMS B.4.4 |
| 4 | Slide Giáo viên (.pptx) | NotebookLM (`nlm create slides`) | 2 slide/nhiệm vụ (Nhiệm vụ + Đáp án), màu tươi, chữ 32/28pt |
| 5 | Slide Phiếu học tập (.pptx) | NotebookLM (`nlm create slides`) | 1 slide/nhiệm vụ, trắng-đen-xám, KHÔNG đáp án, chữ 24/20pt |

## 3. Tiến trình 2 tiết (KHBD) — đối chiếu chuỗi nhiệm vụ ↔ loại hình ↔ đánh giá (bản cập nhật)

### TIẾT 1 — I. ĐỘNG LƯỢNG (★ TIẾT DẠY MINH HỌA, trọng tâm chất lượng)

| Hoạt động | Thời gian | Nội dung | Loại hình nhiệm vụ | Đánh giá cuối hoạt động |
|---|---|---|---|---|
| 1. Khởi động | 10' | Trò chơi AR "Bảo vệ hành tinh xanh": HS dùng tay điều khiển tên lửa bắn thiên thạch đổi hướng, tránh va chạm Trái Đất. Sau khi chơi, rút ra: tên lửa khối lượng lớn + vận tốc lớn làm thiên thạch lệch hướng nhiều hơn → đặt vấn đề "đại lượng nào đặc trưng cho khả năng làm lệch hướng/truyền tương tác này?" | Trò chơi mô phỏng tương tác (game-based, ngoài 12 loại chuẩn nhưng phù hợp Khởi động) + 1 câu dự đoán nhanh (Trắc nghiệm bối cảnh) | GV quan sát mức hào hứng + câu trả lời dự đoán, không chấm điểm, dùng để dẫn dắt |
| 2. Hình thành kiến thức mới — Động lượng | 20' | HS tự tay làm thí nghiệm Hình 28.1 (3 viên bi A/B/C) → rút ra p = m.v, ý nghĩa vật lí; đối chiếu ngược lại với trò chơi mở đầu (tên lửa ↔ viên bi) | NV1: Model Builder (tự làm TN, rút ra công thức) + NV2: Giải mã Meme Vật lý (Meme Analyzer — phân tích 1 hình chế "xe tăng vs xe đạp" để khắc sâu vai trò của CẢ m và v) | Phiếu quan sát TN theo nhóm + sản phẩm phân tích meme (chấm nhanh, không cần đúng tuyệt đối) |
| 3. Luyện tập | 10' | 1 câu hỏi bám 1 trong 3 dạng đề thi tốt nghiệp THPT, có yếu tố "bóc phốt" 1 phát biểu sai lan truyền trên mạng | Bóc phốt TikTok/Shorts (Fact Check Influencer) kết hợp tính toán p = m.v | Chấm nhanh tại lớp, công bố đáp án ngay |
| 4. Vận dụng, củng cố, dặn dò | 5' | Quay lại đúng bối cảnh trò chơi mở đầu: chọn phương án tên lửa (khối lượng/vận tốc) tối ưu để bảo vệ Trái Đất — khép vòng Khởi động↔Vận dụng | Bản đồ lựa chọn sinh tử (Decision Tree) | Câu hỏi vận dụng miệng + biểu quyết nhanh, không chấm điểm. Dặn dò chuẩn bị Tiết 2 |

### TIẾT 2 — II. XUNG LƯỢNG CỦA LỰC

| Hoạt động | Thời gian | Nội dung | Loại hình nhiệm vụ | Đánh giá cuối hoạt động |
|---|---|---|---|---|
| 1. Khởi động | 5' | Video/hình ảnh thủ môn bắt bóng sút phạt 11m + túi khí ô tô bung ra, dự đoán nhanh, ôn lại p = m.v | Trắc nghiệm bối cảnh (dự đoán nhanh) | GV quan sát, không chấm điểm |
| 2. Hình thành kiến thức mới — Xung lượng của lực | 20' | Từ định luật II Newton suy ra F.Δt = Δp (dạng 2 định luật II Newton) | NV1: Sắp xếp tiến trình (Algorithmic Ordering — suy luận a=Δv/Δt → F.Δt=Δp) + NV2: Bug Buster (tìm lỗi trong 1 lời giải mẫu sai) | Bài tập nhỏ chấm chéo giữa các nhóm |
| 3. Luyện tập | 12' | Câu hỏi Đúng/Sai có biện giải, gộp cả 2 tiết (p=m.v và F=Δp/Δt), đúng 1 trong 3 dạng đề thi tốt nghiệp THPT | Đúng/Sai có biện giải (Assertion Reasoning) | Chấm nhanh tại lớp, công bố đáp án ngay |
| 4. Vận dụng, củng cố, dặn dò | 8' | Đề xuất kĩ thuật sai (mũ bảo hiểm lót thép) cần HS gỡ lỗi + đọc thông tin túi khí/dây an toàn | Gỡ lỗi thiết kế kỹ thuật (Engineering Debugger) + Khai thác Infographic | Câu hỏi vận dụng + sản phẩm gỡ lỗi. Dặn dò hoàn thành Bài tập về nhà |

*Ghi chú đối chiếu tiêu chí đánh giá:* mỗi tiết đều có đủ 4 bước CV5512 với đánh giá riêng sau mỗi hoạt
động (không dồn cuối bài). Loại hình nhiệm vụ đa dạng, KHÔNG lặp trong cùng 1 tiết, ưu tiên các loại
hình có yếu tố trò chơi/mạng xã hội/tình huống gần gũi (AR, Meme, TikTok, Decision Tree) ở Tiết 1 (tiết
minh họa) để tối đa hoá tiêu chí "học sinh hào hứng tham gia, tương tác tích cực". Vận dụng Tiết 1 khép
vòng trực tiếp với Khởi động (cùng bối cảnh trò chơi) — thể hiện rõ "liên kết chặt chẽ giữa các hoạt
động". Tiết 2 giữ các loại hình thiên về suy luận/kỹ thuật (phù hợp nội dung xung lượng-lực nặng tính
toán hơn), có Engineering Debugger/Infographic ở Vận dụng để không toàn suy luận khô khan.

## 4. Rủi ro & bước cần xác nhận trước khi chạy

1. **Bước tốn kém nhất (NotebookLM)**: sinh 2 bộ Slide — cần xác nhận riêng trước khi gọi, vì rate
   limit theo giờ (V1 từng bị `RESOURCE_EXHAUSTED`, phải chờ 25-30 phút). Đề xuất: hoàn thiện + duyệt
   xong KHBD/PHT/Bài tập về nhà (bản .docx) trước, rồi mới sinh Slide sau cùng.
2. Ảnh minh hoạ khoa học (nếu cần) dùng vector matplotlib tự vẽ theo chuẩn GEMS (không hoạt hình/3D ảo).
3. Toàn bộ nội dung sẽ tự đối chiếu ngược với 3 tiêu chí ở mục 0 trước khi xuất bản.

---

**Xin xác nhận trước khi soạn tài liệu thật:**
- Tiến trình 5 hoạt động ở mục 3 có ổn không, hay cần điều chỉnh thời lượng/nội dung?
- Có nên dùng lại nguyên PHT 4-mục (Khởi động/Hình thành KT mới/Luyện tập/Vận dụng-Mở rộng) như V1,
  hay đổi sang chuẩn PHT phẳng 3-mục mới nhất của GEMS (đã áp dụng cho Bài 7, bỏ mục Khởi động)?
- Xác nhận: soạn xong KHBD + PHT + Bài tập về nhà (.docx) trước, sau đó mới xin phép gọi NotebookLM
  sinh Slide (đúng quy trình D.2 đã thống nhất)?
