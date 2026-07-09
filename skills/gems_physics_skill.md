---
name: gems_physics_skill
description: |
  Bộ Tiêu chuẩn Sư phạm GEMS Vật lý (Single Source of Truth về NỘI DUNG) định nghĩa
  7 nguyên tắc sư phạm cốt lõi, 12 loại hình nhiệm vụ học tập, và 15 tiêu chí QA.
  Quy chuẩn ĐỊNH DẠNG KỸ THUẬT (lề, font, màu, cấu trúc Markdown) nằm ở
  `.agents/agents.md` — tài liệu này KHÔNG lặp lại số liệu định dạng để tránh
  2 nguồn lệch nhau theo thời gian (bài học đã xảy ra với bản trước 7/2026).
  Kích hoạt khi AI thiết kế, biên soạn hoặc kiểm định NỘI DUNG tài liệu Vật lý GEMS.
version: 9.5.0
---
# TIÊU CHUẨN SƯ PHẠM GEMS VẬT LÝ (MÃ: GEMS_VAT_LY)

## 1. VAI TRÒ & PHONG CÁCH

* **Vai trò:** Chuyển hóa kiến thức khoa học trừu tượng thành bộ học liệu đồng bộ bám sát SGK Kết nối tri thức theo chương trình GDPT 2018.
* **Phong cách thiết kế:** Infographic hiện đại, tinh gọn, tối ưu hóa không gian in ấn, tối đa hóa trải nghiệm thị giác.
* **Quy tắc in ấn:** Chừa tối thiểu 35-40% không gian trống cho học sinh viết và vẽ.

---

## 2. 7 NGUYÊN TẮC SƯ PHẠM CỐT LÕI

1. **Chính xác tuyệt đối:** Bám sát SGK gốc Kết nối tri thức, chi tiết, không làm chung chung, không tự ý thêm chú thích ngoài luồng.
2. **Thuần Việt sư phạm:** Không dùng tiếng Anh hoặc chú thích tiếng Anh trong tài liệu. Tên riêng khoa học (Newton, Joule, Pascal...) phải kèm chú thích tiếng Việt ở lần đầu xuất hiện.
3. **Tiến trình tuyến tính mạch lạc:** Lộ trình từ dễ đến khó, từ khám phá đến chốt lý thuyết và vận dụng.
4. **Bản chất khoa học & Trực quan thực tế:** Mọi nhiệm vụ, hình ảnh minh họa phải gắn liền với bản chất hiện tượng thực tế và chuẩn xác về mặt vật lý.
5. **Tiêu chuẩn hình ảnh thực tế:** Chỉ dùng ảnh chụp thực tế hoặc tư liệu khoa học chất lượng cao. Không dùng hoạt hình, ảnh đồ họa 3D ảo, hoặc ảnh sai vật lý.
6. **Tinh giản tối đa (Thanh lọc):** Loại bỏ các chú thích rườm rà, lời dẫn giải kỹ thuật dài dòng. Chỉ giữ lại hệ thống nhãn và số thứ tự logic (Nhiệm vụ 1, 2, 3...).
7. **Đa dạng hóa nhiệm vụ học tập (Task Chain):** Thiết kế các nhiệm vụ dưới dạng chuỗi liên kết logic, liền mạch, luân phiên đa dạng từ 12 loại hình nhiệm vụ bên dưới.

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

## 4. YÊU CẦU NỘI DUNG THEO LOẠI TÀI LIỆU

Đây là yêu cầu **nội dung sư phạm** — quy chuẩn định dạng kỹ thuật (lề, font, màu,
cú pháp Markdown nhận diện được) nằm ở [`.agents/agents.md`](../.agents/agents.md).

### 4.1 Phiếu học tập (PHT)
* **Bám THẲNG tiến trình dạy thật trong KHBD** — 1 trình tự phẳng duy nhất, KHÔNG dùng khung riêng
  của GEMS lặp lại 4 phần/ĐVKT (bản trước v9.4.0). Đúng 3 mục lớn, đánh số `1/2/3`:
  - **1. HÌNH THÀNH KIẾN THỨC MỚI** — mỗi ĐVKT 1 mục con (`### 📍 ĐVKT {i}: ...`), gồm nhiệm vụ
    khám phá + lý thuyết trọng tâm đục lỗ điền khuyết (ký hiệu `(1)`, `(2)`...). **Độ dài đường chấm
    của mỗi chỗ trống phải ước lượng theo độ dài đáp án cần điền, không dùng 1 độ dài cố định cho mọi
    chỗ** — ký hiệu/số liệu ngắn (vd. `$L$`, đơn vị) dùng đường chấm ngắn (~4-7 ký tự `.`), cụm từ
    dài hơn (vd. "nhiệt độ", "ngưng tụ") dùng đường chấm dài hơn tương ứng (~10-12 ký tự `.`). Áp
    dụng cho cả `summary_cloze` (PHT bản Word) lẫn văn bản đục lỗ trên Infographic (đọc lại đúng nội
    dung PHT, không tự bịa độ dài khác — xem `gems/notebooklm/prompt_builder.py::_BLANK_LENGTH_RULE`).
  - **2. LUYỆN TẬP** — mỗi ĐVKT 1 bài toán/tình huống, gộp chung 1 mục (không lặp theo từng ĐVKT).
  - **3. VẬN DỤNG** — nhiệm vụ vận dụng nâng cao (nếu có, ví dụ Engineering Debugger) + đoạn đọc
    mở rộng mỗi ĐVKT (trích nguồn uy tín khi giới thiệu ứng dụng thực tế).
  - **KHÔNG có mục cho hoạt động Khởi động** — hoạt động này chỉ diễn ra trên lớp, không cần PHT giấy.
* Đồng bộ tiêu đề: tên ĐVKT và tên nhiệm vụ phải khớp 1-1 với Slide bài giảng và KHBD.
* Mỗi nhiệm vụ (kể cả nhiệm vụ vận dụng ở mục 3) bắt buộc có dòng **Hướng dẫn thực hiện** nêu đủ 3
  ý: (1) hình thức tổ chức (cá nhân/cặp đôi/nhóm N học sinh), (2) thời gian cụ thể (phút), (3) tài
  liệu/công cụ phải dùng (đọc SGK trang mấy, quan sát thí nghiệm/video nào, hay tự suy luận) —
  không bỏ trống.
* Mục 2 (Luyện tập) phải **diễn đạt bằng đúng 1 trong 3 dạng câu hỏi của đề thi tốt nghiệp THPT**
  (trắc nghiệm 4 phương án A/B/C/D, hoặc Đúng/Sai 4 ý a-d, hoặc trả lời ngắn dạng số có nêu rõ quy
  tắc làm tròn) — xem chuẩn chi tiết ở mục 4.4. Mục đích: học sinh làm quen "cảm giác đề thi thật"
  ngay trong giờ học, không phải đợi đến Bài tập về nhà mới gặp lần đầu.
* Khoảng trống viết bài dùng placeholder `[DOT_LINE_90]` — engine tự thay bằng dòng chấm 90 ký tự.

### 4.2 Slide bài giảng — 2 BỘ tách biệt (qua NotebookLM, xem `gems/notebooklm/`)

**Quyết định chuẩn hóa (áp dụng cho MỌI bài học, không riêng bài nào):** thay vì 1 bộ Slide + N+2
Infographic rời (mục 4.5 cũ — nay đã loại bỏ, xem cuối mục này), quy trình sinh **2 bộ Slide tách
biệt hoàn toàn qua NotebookLM**, đúc kết từ đợt thiết kế lại Bài 28 - Động lượng:

1. **Slide Giáo viên** — trình chiếu dẫn dắt cả lớp, màu sắc/đồ họa đẹp, có đầy đủ đáp án.
2. **Slide Phiếu học tập** — bản chiếu số hóa của PHT giấy, dùng bởi học sinh, KHÔNG có đáp án nào.

Cả 2 bộ dùng chung 1 nội dung/nhiệm vụ/đánh số, chỉ khác vai trò hiển thị và bảng màu — xem "Master
slide" bên dưới.

**A. Cấu trúc & phân vai nội dung (áp dụng cho MỌI nhiệm vụ, không có ngoại lệ — kể cả Luyện tập,
Vận dụng, không chỉ Hình thành kiến thức mới):**
* Slide Giáo viên: mỗi nhiệm vụ tách thành đúng 2 slide liên tiếp — 1 slide **"Nhiệm vụ"** (CHỈ tên
  nhiệm vụ + 3 ý "Hình thức: ...; Thời gian: ...; Tài liệu: ..." lấy **nguyên văn** từ bước Chuyển
  giao trong KHBD, KHÔNG in đề bài/câu hỏi) và 1 slide **"Đáp án"** (CHỈ đáp án/kết luận + ảnh minh
  họa, KHÔNG lặp lại hướng dẫn). TUYỆT ĐỐI không gộp 2 loại này vào chung 1 slide, dù đặt cạnh nhau
  hay trên-dưới.
* Slide Phiếu học tập: mỗi nhiệm vụ là 1 slide DUY NHẤT gồm tên nhiệm vụ + 3 ý Hình thức/Thời
  gian/Tài liệu + TOÀN BỘ câu hỏi/đề bài nguyên văn từ PHT + khoảng trống kẻ ngang (độ dài tỉ lệ câu
  trả lời kỳ vọng) để học sinh viết trực tiếp. **TUYỆT ĐỐI KHÔNG có slide đáp án nào trong toàn bộ
  deck này**, kể cả ở mục "Kiến thức trọng tâm" (chỉ dạng điền khuyết, không có bản đáp án đầy đủ đi
  kèm) hay slide kết bài (chỉ khung sơ đồ tư duy trống).
* Bám đúng 1 trục số X.Y duy nhất — X lấy trực tiếp từ số mục PHT (`1`/`2.1`/`2.2`/`3.1`/`3.2`/...),
  KHÔNG dùng thuật ngữ viết tắt "ĐVKT" ở bất kỳ đâu trên slide (xem mục 4.1).
* Slide Giáo viên bắt buộc có thêm: 1 slide **Mục lục** ngay sau slide bìa, liệt kê đủ các mục lớn;
  và **1 slide "phân đoạn" riêng biệt** trước mỗi phần lớn mới (chỉ tiêu đề in hoa của phần đó + 1
  ảnh minh họa tiêu biểu, KHÔNG có nội dung nào khác) — giúp nhận biết ngay khi chuyển phần.
* Slide kết bài: sơ đồ tư duy tổng hợp — Giáo viên điền đầy đủ, Phiếu học tập chỉ có khung trống.

**B. Thiết kế & Master slide (dùng chung khuôn mẫu, chỉ khác bảng màu):**
* 2 bộ được dựng như 2 bản phối màu khác nhau của CÙNG 1 khuôn mẫu (master): cùng hệ thống phân cấp
  tiêu đề, cùng bố cục cho từng LOẠI slide (Nhiệm vụ/Đáp án/Kiến thức trọng tâm/Đọc thêm/Mục
  lục/Phân đoạn — mỗi loại đúng 1 kiểu khung/màu/vị trí cố định, không đổi kiểu giữa chừng deck),
  cùng vị trí số trang, cùng kiểu khung ảnh minh họa.
* **Slide Giáo viên:** màu sắc tươi mới, hài hòa, giàu năng lượng, đồ họa thu hút (bảng màu Anthropic
  — xem chi tiết bên dưới). Cỡ chữ CỐ ĐỊNH (không phải khoảng/range): tiêu đề **32pt**, nội
  dung/thân bài **28pt** — không tự thu nhỏ chữ để nhồi nội dung dài, thà viết súc tích hơn.
* **Slide Phiếu học tập:** nền TRẮNG tuyệt đối mọi slide, ảnh minh họa CHỈ tông trắng/đen/xám (không
  màu). Cỡ chữ CỐ ĐỊNH: tiêu đề **24pt**, nội dung **20pt**.
* **Ảnh minh họa giữa 2 bộ phải giống hệt nhau về bố cục/chi tiết/nhãn chữ, chỉ khác màu sắc** (màu
  vs. grayscale) — soạn 1 bộ mô tả ảnh chi tiết dùng chung cho cả 2 prompt để đảm bảo đồng bộ, không
  để 2 AI vẽ độc lập ra 2 kết quả khác nhau.
* **Theme màu/font thương hiệu Anthropic** (khác Primary `#1F4E79`/Times New Roman của PHT/KHBD/Bài
  tập — có chủ đích, không cần khớp màu nhau): Dark `#141413`/Light `#FAF9F5` nền/chữ chính, nhấn
  luân phiên Orange `#D97757`/Blue `#6A9BCC`/Green `#788C5D`, font tiêu đề **Poppins** + thân bài
  **Lora**. Chi tiết đầy đủ xem mục 4.6 và `gems/notebooklm/prompt_builder.py::_ANTHROPIC_THEME_RULE`.
* Mỗi slide (không trừ slide nào, kể cả Đáp án/Kiến thức trọng tâm/Mục lục) phải có ≥1 ảnh minh họa
  khoa học chính xác liên quan trực tiếp nội dung slide đó — ưu tiên tuyệt đối ảnh minh họa kiến
  thức, không dùng ảnh trang trí chung chung.
* Số trang **"Trang X/Y"** ở góc dưới bên phải, cỡ chữ cố định 16pt, mọi slide của CẢ 2 bộ, kể cả
  slide bìa — không bị logo/watermark của công cụ che khuất.

**C. Nội dung & ngôn ngữ:**
* Slide Nhiệm vụ phải hiển thị nguyên văn dòng "Hướng dẫn thực hiện" (hình thức/thời gian/tài liệu)
  lấy từ KHBD nguồn (**KHBD là nguồn tham chiếu duy nhất**, sinh ra ĐẦU TIÊN — xem mục 4.3) — không
  tự diễn đạt lại khác.
* Cấm tuyệt đối chữ tiếng Anh ở bất kỳ đâu, kể cả nhãn/tên khung hộp nội dung (ví dụ: dùng "ĐÁP ÁN"/
  "NHIỆM VỤ", không dùng "Answer Frame"/"Task Box").
* Slide Phiếu học tập: chú thích trên ảnh minh họa ở các slide điền khuyết KHÔNG được viết ra câu
  kết luận/công thức hoàn chỉnh trùng với đáp án của chỗ trống trên cùng slide đó (chỉ vẽ hình + nhãn
  đại lượng cơ bản).
* Nhiệm vụ đa dạng đúng 12 loại hình học tập (mục 3), tránh lặp loại hình gây nhàm chán.
* Không dùng dấu ngoặc vuông `[...]` hay bất kỳ ký hiệu placeholder nào trong nội dung hiển thị thật
  trên slide (ngoại lệ: `[ ? ]` dùng làm ô trống điền khuyết THẬT SỰ là nội dung cố ý, không phải
  placeholder cho AI tự thay — xem thêm bài học vận hành NotebookLM ở
  `docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md`).

**D. Infographic học sinh — ĐÃ LOẠI BỎ khỏi quy trình chuẩn (mục 4.5 cũ):** thay thế hoàn toàn bằng
bộ "Slide Phiếu học tập" ở trên, vì N+2 ảnh AI độc lập dễ thiếu đồng bộ về tên bài/tên học sinh/hình
ảnh giữa các ảnh với nhau, trong khi slide đảm bảo đồng bộ tuyệt đối và cho phép viết trực tiếp lên
slide khi dùng bảng tương tác.

### 4.3 Kế hoạch bài dạy (KHBD)
* Bám cấu trúc hoạt động trong Phụ lục IV: Mở đầu → Hình thành kiến thức mới → Luyện tập → Vận dụng.
  Nếu bài có từ 2 ĐVKT trở lên, **tách hoạt động Hình thành kiến thức thành nhiều hoạt động riêng
  theo từng ĐVKT** (không gộp chung) để cấu trúc KHBD bám sát cấu trúc tuần tự theo ĐVKT của PHT;
  trong nội dung mỗi hoạt động ghi rõ "(tương ứng PHT mục 1 — ĐVKT {i})"/"(tương ứng PHT mục 2)"/
  "(tương ứng PHT mục 3)" để đối chiếu 1-1 với đúng mục PHT (xem cấu trúc phẳng 3 mục ở 4.1). Riêng
  Khởi động không cần đối chiếu — mục này không có PHT tương ứng.
* Mỗi hoạt động phải hiện đủ `a) Mục tiêu`, `b) Nội dung`, `c) Sản phẩm`, `d) Tổ chức thực hiện`; phần d gồm 4 bước CV5512 (Chuyển giao → Thực hiện → Báo cáo → Kết luận).
* Bước 1 (Chuyển giao nhiệm vụ) của MỌI hoạt động phải nêu đủ 3 ý như PHT: (1) hình thức tổ chức
  (cá nhân/cặp đôi/nhóm N học sinh), (2) thời gian cụ thể (phút), (3) tài liệu/công cụ học sinh
  phải dùng (SGK trang mấy, quan sát thí nghiệm/video nào, hay Phiếu học tập nhiệm vụ nào).
* Hoạt động Luyện tập bắt buộc có ít nhất 1 câu hỏi soạn theo đúng 1 trong 3 dạng của đề thi tốt
  nghiệp THPT (mục 4.4) — cùng nguyên tắc "luyện đề ngay khi học" với phần Vận dụng của PHT, không
  để học sinh lần đầu gặp cấu trúc đề thi thật là lúc làm Bài tập về nhà.
* Chọn 1-2 kĩ thuật dạy học tích cực phù hợp cho mỗi hoạt động từ tài liệu `tai-lieu-goc/mẫu/17_KY_THUAT_DAY_HOC_TICH_CUC.md`. Cơ chế của kĩ thuật phải xuất hiện trong tiến trình, không chỉ ghi tên.
* Tích hợp năng lực số theo `tai-lieu-goc/mẫu/Cong-van-3456-Khung-Nang-luc-so.md`: lớp 10-12 dùng mức **Nâng cao 1**, mỗi mục tiêu có mã năng lực thành phần, biểu hiện và minh chứng/sản phẩm số đánh giá được.
* Không tích hợp công nghệ gượng ép. Chỉ gắn mã NLS khi hoạt động có công cụ hoặc thao tác số và sản phẩm tạo ra minh chứng tương ứng; chú ý an toàn, bản quyền và trích nguồn khi liên quan.
* Không tích hợp khung 5E/IDB hay mô hình nước ngoài khác.

### 4.4 Bài tập về nhà
* Cấu trúc: Phần I (18 câu MCQ) → Phần II (4 câu Đúng/Sai, mỗi câu 4 ý) → Phần III (6 câu trả lời ngắn).
  Chuẩn dưới đây được đối chiếu trực tiếp với đề thi chính thức Bộ GD&ĐT (mã đề 0227 năm 2025,
  mã đề 0214 năm 2026 — lưu tại `tai-lieu-goc/mẫu/`): không chỉ đúng **số lượng** câu mà còn đúng
  **phong cách ra đề** của từng phần, để bài tập tự luyện có "cảm giác đề thi thật" ngay từ đầu.
* **Phần I — đúng 3 mức nhận thức, 6 câu mỗi mức (không xáo trộn tỉ lệ):**
  - *Nhận biết* (6 câu): hỏi thẳng định nghĩa, đơn vị đo, phát biểu định luật/nội dung SGK —
    không cần tính toán hay suy luận qua bước trung gian.
  - *Thông hiểu* (6 câu): diễn giải cơ chế, đọc đồ thị/hình vẽ/mô hình, so sánh hai quá trình,
    hoặc suy ra hệ quả trực tiếp của một định luật — không có phép tính số.
  - *Vận dụng* (6 câu): có ít nhất 1 phép tính (1-2 bước) áp dụng công thức vào số liệu cụ thể,
    ưu tiên bối cảnh kĩ thuật/đời sống thay vì số liệu trừu tượng.
  - Toàn bộ phương án nhiễu (sai) của 18 câu phải bắt nguồn từ đúng các quan niệm sai lầm đã xác
    định ở bước phân tích sư phạm (Bước 1) — không bịa phương án nhiễu ngẫu nhiên, vô căn cứ.
* **Phần II — mỗi câu là một bối cảnh duy nhất, 4 ý là một chuỗi suy luận:** đoạn dẫn mô tả ĐÚNG
  MỘT thí nghiệm/thiết bị/tình huống cụ thể (có thể kèm hình vẽ mô tả); 4 ý a)-d) phải liên kết
  chặt với nhau quanh cùng bối cảnh đó — không phải 4 mệnh đề độc lập ghép ngẫu nhiên. Bắt buộc có
  tối thiểu 1 ý định tính thuần suy luận vật lý, có thể có 1 ý yêu cầu tính toán ngắn, và cài ít
  nhất 1 bẫy quan niệm sai lầm diễn đạt tự nhiên như một nhận định hợp lý nhìn thoáng qua.
* **Phần III — ghép cặp dùng chung dữ kiện:** 6 câu chia thành 3 cặp, mỗi cặp dùng chung một đoạn
  bối cảnh kĩ thuật/khoa học/đời sống thật (không dùng số liệu trừu tượng vô nghĩa) theo đúng mẫu
  "Dùng thông tin sau cho câu X và câu Y: ..." của đề thi thật. Mỗi câu là một phép tính nhiều
  bước độc lập trên cùng dữ kiện, và PHẢI nêu rõ quy tắc làm tròn ngay trong đề bài (ví dụ: "làm
  tròn kết quả đến chữ số hàng phần trăm/phần mười/hàng đơn vị") — đề thi thật luôn quy định làm
  tròn riêng cho từng câu, không để mặc định.
* Tối thiểu 50% tổng số câu hỏi trên **cả 3 phần** gắn bối cảnh thực tế, cung cấp đầy đủ hằng số
  vật lý dùng chung (mục "+ Cho biết: ...") và quy tắc làm tròn; khi Phần III cần tính nhiều bước,
  cân nhắc thêm dòng "Không làm tròn kết quả các phép tính trung gian" như đề thi thật.
* LaTeX viết dạng `$công_thức$` (vd. `$W_đ$`, `$W_t$`) — engine tự dịch sang Unicode khi xuất Word.
* **Không in đáp án Đúng/Sai ngay trong đề** — đáp án chỉ được phép xuất hiện ở mục hướng dẫn giải cuối file.
* **Hình thức trình bày KHÔNG đóng giả đề thi thật** (khác bản trước v9.4.0): header đơn giản như
  PHT/KHBD (tiêu đề bài + Họ tên học sinh/Lớp), không còn Sở GD&ĐT/Trường THPT/"Đề có N trang"/Mã đề
  thi/Số báo danh/"Thời gian làm bài" — chỉ CÂU HỎI mới bám phong cách đề tốt nghiệp, không phải vỏ
  hình thức. Hướng dẫn từng phần viết liền sau nhãn PHẦN như cũ.
* Phần II trình bày các ý `a)`–`d)` dạng đoạn văn, không dùng bảng/checkbox Đúng–Sai. Phần III không thêm hộp “Đáp số của học sinh”.
* Footer căn giữa `Trang x/y` (dùng chung `styles.add_page_number_footer()` với PHT/KHBD, không còn
  mã đề); phần đáp án bắt đầu ở trang mới, trước đó có dòng phân cách "----- HẾT -----" đơn giản
  (không còn 2 dòng thông báo kiểu đóng vai coi thi).

### 4.5 (đã loại bỏ — nội dung gộp vào 4.2.D)
Mục này trước đây mô tả "N+2 Infographic". Đã được thay thế hoàn toàn bằng bộ "Slide Phiếu học tập"
— xem mục 4.2 (phần D) để biết lý do và mục 4.2 (phần A-C) để biết chuẩn thay thế đầy đủ. Giữ lại số
mục này (không xoá hẳn) để các tham chiếu cũ trỏ đúng chỗ giải thích, tránh gây khó hiểu khi đọc lại
lịch sử `changelog.md`.

### 4.6 Minh họa khoa học (PHT, KHBD, Bài tập về nhà, 2 bộ Slide)
* **Nguyên tắc chọn công cụ vẽ — theo bản chất nội dung cần minh họa, không tùy tiện:**
  - **Vector tự vẽ (matplotlib, xem `gems/illustrations/`)** cho: sơ đồ thí nghiệm/dụng cụ, đồ thị
    số liệu (nhiệt độ-thời gian, áp suất-thể tích...), sơ đồ nguyên lý/chu trình kỹ thuật — bất cứ
    thứ gì cần chính xác nhãn, mũi tên, tỉ lệ, số liệu. Ưu tiên tuyệt đối vì không có rủi ro AI vẽ
    sai chi tiết khoa học.
  - **Ảnh AI (do người dùng tự tạo trên nền tảng Antigravity, không có sẵn trong phiên agent)** chỉ
    dùng khi cần minh họa trực quan hiện thực mà vector không lột tả được (ví dụ: hiện tượng đời
    sống thật, kết cấu vật liệu, sản phẩm chưa có sẵn ảnh chụp) — Claude Code soạn sẵn mô tả ảnh
    chi tiết, khoa học, chú thích tiếng Việt, cấm phong cách hoạt hình, để người dùng tự tạo rồi
    cung cấp file chèn vào đúng vị trí `ready/hinh_anh/`.
  - Nếu đã có ảnh chụp thực tế/tư liệu khoa học đáng tin cậy (nguyên tắc 5, mục 2) thì luôn ưu tiên
    dùng ảnh thật thay vì vẽ lại.
* **Cấm tuyệt đối** phong cách hoạt hình/cartoon, 3D ảo, phóng đại phi thực tế ở MỌI hình thức minh
  họa (vector lẫn ảnh AI) — khớp nguyên tắc 5. Mọi chú thích/nhãn trên ảnh phải bằng tiếng Việt.
* Ảnh minh họa nhúng vào PHT/KHBD/Bài tập về nhà theo đúng cú pháp `.agents/agents.md` §4 (dòng
  text chứa `ready/hinh_anh/<tên file>.png`) — không cần sửa exporter, engine tự tách và chèn ảnh.
* Ảnh minh họa dùng trong 2 bộ Slide (mục 4.2) phải giống hệt nhau về bố cục giữa bản màu (Giáo
  viên) và bản trắng/đen/xám (Phiếu học tập) — soạn 1 bộ mô tả dùng chung cho cả 2 prompt.

---

## 5. BỘ 15 TIÊU CHÍ QA SELF-CHECK

### 5.1 Phiếu học tập (PHT)
* **TC-PHT-01 (Không gian):** Chừa tối thiểu 35-40% không gian trống cho học sinh viết/vẽ.
* **TC-PHT-02 (Hình ảnh):** Chỉ mô tả ảnh chụp thực tế hoặc tư liệu khoa học chuẩn vật lý.
* **TC-PHT-03 (Tuyến tính):** Đúng 3 mục phẳng "1. Hình thành kiến thức mới → 2. Luyện tập →
  3. Vận dụng" đi một chiều, không có mục cho Khởi động, không quay lại khung 4 phần/ĐVKT cũ.
* **TC-PHT-04 (Ngôn ngữ):** Thuần Việt 100%, nghiêm túc, không từ lóng, không từ tiếng Anh.
* **TC-PHT-05 (Khoảng trống):** Vùng trả lời khống chế bằng placeholder `[DOT_LINE_90]`, không sinh dòng chấm thô thủ công.
* **TC-PHT-06 (Nhiệm vụ):** Đủ số nhiệm vụ cho các ĐVKT, liên kết chuỗi logic và đa dạng loại hình;
  mục Luyện tập bám đúng 1 trong 3 dạng câu hỏi đề tốt nghiệp (mục 4.4); mọi nhiệm vụ có đủ dòng
  Hướng dẫn thực hiện 3 ý.

### 5.2 Slide bài giảng — 2 bộ (SLD)
* **TC-SLD-01 (Đồng bộ):** Khớp 1-1 hoàn toàn về nội dung/thứ tự/đánh số giữa CẢ 2 bộ Slide, PHT và
  KHBD; nhãn "Hình thức/Thời gian/Tài liệu" lấy nguyên văn từ KHBD, không tự diễn đạt lại.
* **TC-SLD-02 (Trực quan):** Có ít nhất 1 hình ảnh minh họa khoa học chất lượng trên MỌI slide (kể cả
  Đáp án/Kiến thức trọng tâm/Mục lục); ảnh giống hệt bố cục giữa 2 bộ, chỉ khác màu.
* **TC-SLD-03 (Thiết kế):** Cỡ chữ CỐ ĐỊNH đúng chuẩn từng bộ (Giáo viên 32/28pt, Phiếu học tập
  24/20pt — không tự thu nhỏ); master slide nhất quán mỗi loại slide xuyên suốt deck; số trang "Trang
  X/Y" mọi slide kể cả bìa; highlight `==từ khoá==` hiển thị màu vàng.
* **TC-SLD-04 (Cấu trúc & phân vai):** Slide Giáo viên có Mục lục + slide phân đoạn mỗi phần lớn +
  MỌI nhiệm vụ tách đúng 2 slide Nhiệm vụ/Đáp án riêng biệt (không gộp); Slide Phiếu học tập mỗi
  nhiệm vụ 1 slide (hướng dẫn+câu hỏi+khoảng trống) và **tuyệt đối không có slide đáp án nào**, kể cả
  qua chú thích ảnh minh họa; đủ slide mở đầu và kết bài (Mindmap, bên Phiếu học tập chỉ khung trống).
* **TC-SLD-05 (Ngôn ngữ):** Thuần Việt 100% kể cả nhãn khung/hộp, tiêu đề bám sát SGK, không giải
  thích ngoài luồng, không ký hiệu placeholder `[...]` xuất hiện trong nội dung hiển thị thật.

### 5.3 Bài tập về nhà (HW)
* **TC-HW-01 (Chẩn đoán):** Phương án nhiễu Phần I và tối thiểu 1 ý mỗi câu Phần II bắt nguồn từ
  quan niệm sai lầm đã phân tích; mỗi câu Phần II là một bối cảnh duy nhất triển khai thành chuỗi
  4 ý liên kết (không phải 4 mệnh đề rời rạc).
* **TC-HW-02 (Thực tế):** Tối thiểu 50% câu hỏi toàn bài (cả 3 phần) là bài toán thực tế/kĩ thuật,
  trích nguồn uy tín khi có thể.
* **TC-HW-03 (Cơ cấu & phong cách đề thi):** Đúng 18 MCQ (6 Nhận biết + 6 Thông hiểu + 6 Vận dụng)
  + 4 Đúng/Sai (mỗi câu 4 ý) + 6 trả lời ngắn (chia 3 cặp dùng chung dữ kiện, mỗi câu nêu rõ quy
  tắc làm tròn); có đủ hằng số vật lý dùng chung khi cần.
* **TC-HW-04 (Kỹ thuật):** LaTeX chuẩn sạch, đáp án tách riêng khỏi đề, không lộ đáp án trong phần câu hỏi.
