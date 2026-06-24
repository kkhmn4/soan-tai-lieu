---
name: gems_physics_skill
description: |
  Bộ Tiêu chuẩn GEMS Vật lý v7.0 (Single Source of Truth) định nghĩa các nguyên tắc sư phạm, 12 loại hình nhiệm vụ, quy chuẩn thiết kế (LaTeX, TikZ, dòng chấm 90 ký tự, slide, homework) và 15 tiêu chí QA.
  Kích hoạt khi AI thiết kế, biên soạn hoặc kiểm định tài liệu Vật lý GEMS.
version: 7.0.0
---

# TIÊU CHUẨN GEMS VẬT LÝ V7.0 (MÃ: GEMS_VAT_LY_V7)

## 1. VAI TRÒ & PHONG CÁCH
* **Vai trò:** Chuyển hóa kiến thức khoa học trừu tượng thành bộ học liệu đồng bộ bám sát SGK Kết nối tri thức theo chương trình GDPT 2018.
* **Phong cách thiết kế:** Infographic hiện đại, tinh gọn, tối ưu hóa không gian in ấn, tối đa hóa trải nghiệm thị giác.
* **Quy tắc in ấn:** Chừa tối thiểu 35-40% không gian trống cho học sinh viết và vẽ.

---

## 2. 7 NGUYÊN TẮC SƯ PHẠM CỐT LÕI
1. **Chính xác tuyệt đối:** Bám sát SGK gốc Kết nối tri thức, chi tiết, không làm chung chung, không tự ý thêm chú thích ngoài luồng.
2. **Thuần Việt sư phạm:** Không dùng tiếng Anh hoặc chú thích tiếng Anh trong tài liệu (trừ phần ẩn Image Prompt cho AI vẽ hình). Tên riêng khoa học (Newton, Joule, Pascal...) phải kèm chú thích tiếng Việt ở lần đầu xuất hiện.
3. **Tiến trình tuyến tính mạch lạc:** Lộ trình từ dễ đến khó, từ khám phá đến chốt lý thuyết và vận dụng.
4. **Bản chất khoa học & Trực quan thực tế:** Mọi nhiệm vụ, hình ảnh minh họa phải gắn liền với bản chất hiện tượng thực tế và chuẩn xác về mặt vật lý.
5. **Tiêu chuẩn hình ảnh thực tế:** Chỉ dùng ảnh chụp thực tế hoặc tư liệu khoa học chất lượng cao. Không dùng hoạt hình, ảnh đồ họa 3D ảo, hoặc ảnh sai vật lý. Phông nền đơn giản, rõ ràng.
6. **Tinh giản tối đa (Thanh lọc):** Loại bỏ các chú thích rườm rà, lời dẫn giải kỹ thuật dài dòng. Chỉ giữ lại hệ thống nhãn (Phần 1, Phần 2...) và số thứ tự logic (Nhiệm vụ 1, 2, 3...).
7. **Đa dạng hóa nhiệm vụ học tập (Task Chain):** Thiết kế các nhiệm vụ dưới dạng chuỗi liên kết logic, liền mạch, luân phiên đa dạng từ 12 loại hình nhiệm vụ mới.

---

## 3. HỆ THỐNG 12 LOẠI HÌNH NHIỆM VỤ HỌC TẬP
1. **Ghép nối đa biến (Matching Matrix):** Kết nối các đại lượng, đơn vị, hiện tượng hoặc đồ thị tương thích.
2. **Sắp xếp tiến trình (Algorithmic Ordering):** Thiết lập trật tự logic của các bước thí nghiệm hoặc giai đoạn hiện tượng.
3. **Tìm và sửa lỗi Vật lý (Bug Buster):** Phát hiện và đính chính các điểm sai bản chất trong phát biểu, hình vẽ hoặc bài giải.
4. **Đúng/Sai có biện giải (Assertion Reasoning):** Đánh giá tính đúng/sai của mệnh đề và đưa ra lập luận vật lý cốt lõi.
5. **Trắc nghiệm bối cảnh (Contextual MCQ):** Câu hỏi trắc nghiệm gắn với tình huống thực tế hoặc ứng dụng kỹ thuật.
6. **Điền khuyết trực quan (Visual Cloze Test):** Quan sát hình ảnh hoặc sơ đồ để điền từ khóa hoặc số liệu vào chỗ trống.
7. **Giải mã Meme Vật lý (Meme Analyzer):** Phân tích tính hài hước dựa trên các định luật vật lý từ hình ảnh chế khoa học.
8. **Gỡ lỗi thiết kế kỹ thuật (Engineering Debugger):** Tìm ra điểm bất hợp lý trong sơ đồ nguyên lý của thiết bị thực tế.
9. **Bóc phốt TikTok/Shorts (Fact Check Influencer):** Kiểm chứng tính đúng đắn khoa học của video thử nghiệm lan truyền.
10. **Bản đồ lựa chọn sinh tử (Decision Tree):** Đưa ra quyết định xử lý tình huống dựa trên phân tích quy luật vật lý.
11. **Khai thác Infographic (Infographic Decryption):** Đọc hiểu, trích xuất thông tin và số liệu từ biểu đồ trực quan hóa.
12. **Xây dựng mô hình (Model Builder):** Xây dựng mô hình vật lý từ dữ kiện cho trước và dự đoán kết quả.

---

## 4. QUY CHUẨN THIẾT KẾ & ĐỊNH DẠNG HỌC LIỆU
 
### 4.1 Phiếu học tập (Worksheet)
* **Khu vực quản lý thông tin:** Họ và tên học sinh, Lớp, Ngày... tháng... năm...
* **Đồng bộ tiêu đề:** Tiêu đề của từng Đơn vị Kiến thức (ĐVKT) và tiêu đề của từng nhiệm vụ trong Phiếu học tập phải đồng bộ hoàn toàn (khớp 1-1) với tiêu đề hiển thị trên Slide bài giảng.
* **Cấu trúc tuyến tính 4 phần cho mỗi ĐVKT:** Khám phá -> Trọng tâm -> Vận dụng -> Mở rộng.
* **Phần Mở rộng Kiến thức:** Nằm ngay sau phần Vận dụng. Tập trung giới thiệu ứng dụng thực tế trong máy móc, thiết bị kỹ thuật, công nghệ hoặc giải thích các hiện tượng tự nhiên liên quan đến bài học. Nội dung mở rộng bắt buộc phải tham khảo và trích dẫn rõ ràng từ các nguồn tài liệu uy tín (như sách chuyên khảo, bài báo khoa học hoặc tạp chí khoa học uy tín).
* **Khoảng trống viết bài:** Bắt buộc sử dụng thẻ placeholder `[DOT_LINE_90]` (chừa từ 3-5 dòng) đại diện cho dòng dấu chấm ghi câu trả lời. Script hậu kỳ sẽ tự động thay thế bằng dòng chấm thật dài 90 ký tự.
* **Lý thuyết Trọng tâm:** Đục lỗ điền khuyết bằng ký hiệu `(1)`, `(2)`...
 
### 4.2 Slide bài giảng đồng bộ
* **Slide mở đầu:** Tên bài học + Giáo viên giảng dạy mặc định: `Kha Khung Hiệp`.
* **Cấu trúc 7 slide cho mỗi ĐVKT:**
  1. *Tên đề mục* (kèm hình ảnh thực tế - khớp 1-1 với tiêu đề ĐVKT trong PHT)
  2. *Nhiệm vụ Khám phá* (mỗi nhiệm vụ 1 slide riêng - khớp tiêu đề nhiệm vụ với PHT)
  3. *Đáp án Khám phá* (giải mã hiện tượng và công bố đáp án)
  4. *Kiến thức Trọng tâm* (lý thuyết chốt, highlight từ khóa quan trọng bằng màu vàng `<span style="background-color: yellow">từ khóa</span>`)
  5. *Thử thách Vận dụng* (tình huống đời sống mới)
  6. *Đáp án Vận dụng* (lời giải chi tiết + tư duy giải nhanh)
  7. *Mở rộng Kiến thức* (Giới thiệu ứng dụng thực tế trong máy móc, thiết bị, hiện tượng tự nhiên,... tham khảo nguồn uy tín từ sách, bài báo khoa học - khớp 1-1 với phần Mở rộng trong PHT và KHBD)
* **Slide kết bài:** Sơ đồ tư duy (Mindmap) tổng hợp bài học.
* **Thiết kế:** Font chữ `"UVN bai sau"`. Cỡ chữ: tiêu đề 28-32pt, nội dung 24-28pt. Tối đa 6-8 dòng mỗi slide.

### 4.3 Kế hoạch bài dạy (KHBD / Giáo án)
* **Đồng bộ tiến trình dạy học:** Tiến trình dạy học trong KHBD phải phản ánh chính xác các ĐVKT và các nhiệm vụ tương ứng trong Phiếu học tập và Slide.
* **Cấu trúc hoạt động dạy học:** Mỗi ĐVKT trong bài dạy phải đi qua đầy đủ tiến trình Khám phá, Trọng tâm, Vận dụng và Mở rộng kiến thức.
* **Hoạt động Mở rộng kiến thức:** KHBD bắt buộc phải có hoạt động hướng dẫn học sinh tìm hiểu phần Mở rộng kiến thức (sau hoạt động Vận dụng), giới thiệu các ứng dụng thực tế trong thiết bị, máy móc, hiện tượng tự nhiên,... dựa trên nguồn tài liệu khoa học uy tín, sách chuyên khảo hoặc bài báo.


### 4.4 Bài tập về nhà (Homework)
* **Cấu trúc 2025:** Phần I (18 MCQ) -> Phần II (4 câu Đúng/Sai, mỗi câu 4 ý a, b, c, d) -> Phần III (6 câu trả lời ngắn tính ra số cụ thể).
* **Bối cảnh thực tế:** 50% câu hỏi bối cảnh thực tế, cung cấp đầy đủ hằng số vật lý và quy tắc làm tròn rõ ràng.
* **LaTeX:** Tất cả biểu thức toán lý dạng `$công_thức$`. Ký hiệu động năng là `$W_đ$`, thế năng là `$W_t$`.
* **Hình vẽ TikZ:** Sử dụng mã TikZ chính xác về mặt vật lý chèn trực tiếp dưới dạng khối mã Markdown (không tạo file `.tex` độc lập). Chú thích bằng Tiếng Việt.

### 4.4 Quy Chuẩn Slide & Infographic Từ Google NotebookLM (Học Sinh)
* **Prompt tạo Slide:** Thiết kế định hướng sinh slide bám sát cấu trúc GEMS v7.0 (Kha Khung Hiệp, font "UVN bai sau", nền sáng, 7 slide cho mỗi ĐVKT).
* **Mô tả Infographic học sinh (Bắt buộc):**
  - Thiết kế infographic phục vụ cho Phiếu học tập của học sinh phải **không có sẵn đáp án/chữ viết cố định** và phải chứa các **khoảng trống/hộp điền khuyết** để học sinh tự hoàn thành nhiệm vụ học tập.
  - 🚫 KHÔNG nhúng văn bản (Tiếng Việt/Tiếng Anh) trực tiếp lên ảnh của AI vẽ (sử dụng prompt tiếng Anh sinh ảnh trống không văn bản để tránh sai chính tả).
  - ⚠️ Thiết lập các bong bóng thoại trống, bệ đỡ, hoặc ô chứa nhãn đi kèm ký hiệu đục lỗ `?` hoặc `(1)`, `(2)`, `(3)` trực tiếp trên ảnh.
  - Đối với sơ đồ thiết bị thí nghiệm, phải vẽ rõ ràng các đường chỉ dẫn (leader lines) trỏ đến bộ phận thiết bị và kết thúc bằng một vòng tròn/ô vuông trống để học sinh tự điền tên dụng cụ.

---

## 5. BỘ 15 TIÊU CHÍ QA SELF-CHECK

### 5.1 Phiếu học tập (PHT)
* **TC-PHT-01 (Không gian):** Chừa tối thiểu 35-40% không gian trống cho học sinh viết/vẽ.
* **TC-PHT-02 (Hình ảnh):** Chỉ mô tả ảnh chụp thực tế hoặc tư liệu khoa học chuẩn vật lý.
* **TC-PHT-03 (Tuyến tính):** Tiến trình Khám phá -> Trọng tâm -> Vận dụng -> Mở rộng đi một chiều.
* **TC-PHT-04 (Ngôn ngữ):** Thuần Việt 100%, nghiêm túc, không từ lóng, không từ tiếng Anh (trừ Image Prompt ẩn).
* **TC-PHT-05 (Khoảng trống):** Vùng trả lời khống chế bằng thẻ placeholder `[DOT_LINE_90]` (3-5 dòng) và không được sinh dòng chấm thô.
* **TC-PHT-06 (Nhiệm vụ):** Đủ số nhiệm vụ cho các ĐVKT, liên kết chuỗi logic và đa dạng loại hình.

### 5.2 Slide bài giảng (SLD)
* **TC-SLD-01 (Đồng bộ):** Khớp 1-1 hoàn toàn về nội dung và thứ tự giữa Slide và PHT.
* **TC-SLD-02 (Trực quan):** Có ít nhất 1 hình ảnh minh họa thực tế khoa học chất lượng trên mỗi Slide.
* **TC-SLD-03 (Thiết kế):** Font `"UVN bai sau"`, cỡ chữ chuẩn (28-32pt tiêu đề, 24-28pt nội dung), highlight vàng.
* **TC-SLD-04 (Cấu trúc):** Đầy đủ cấu trúc 7 slide cho mỗi ĐVKT, có slide mở đầu (Kha Khung Hiệp) và kết bài (Mindmap).
* **TC-SLD-05 (Ngôn ngữ Slide):** Thuần Việt 100%, tiêu đề bám sát SGK, không giải thích ngoài luồng.

### 5.3 Bài tập về nhà (HW)
* **TC-HW-01 (Chẩn đoán):** Gài bẫy lỗi sai lầm, phần dẫn có bối cảnh chi tiết mở rộng tri thức.
* **TC-HW-02 (Thực tế):** 50% câu hỏi là bài toán thực tế trích nguồn từ tài liệu/tạp chí uy tín quốc tế.
* **TC-HW-03 (Cơ cấu):** Đúng số lượng 18 MCQ + 4 Đúng/Sai + 6 trả lời ngắn; có đủ hằng số, quy tắc làm tròn.
* **TC-HW-04 (Kỹ thuật):** Mã LaTeX chuẩn sạch, hình vẽ TikZ chính xác, file đáp án riêng biệt có giải thuật tư duy.
