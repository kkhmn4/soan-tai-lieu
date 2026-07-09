# Yêu cầu dự án — Hệ thống soạn học liệu Vật lý (GEMS + các bài one-off)

> Tài liệu tổng hợp toàn bộ yêu cầu mà Kha Khung Hiệp đã đưa ra qua các phiên làm việc với Claude
> Code, đúc kết từ: lịch sử `changelog.md`, `skills/gems_physics_skill.md`, `.agents/agents.md`,
> `readme.md`, bộ nhớ phiên (`user_gems_teacher.md`, `feedback_gems_workflow.md`,
> `project_gems_pipeline_state.md`, `reference_gems_doc_locations.md`), và phiên làm việc chi tiết
> nhất cho tới nay (đợt soạn Bài 28 — Động lượng). Mục đích: 1 nơi duy nhất để đối chiếu lại toàn bộ
> yêu cầu khi cần, tránh phải lặp lại hoặc suy đoán ở các phiên sau.

---

## PHẦN A — TỔNG QUAN & VAI TRÒ NGƯỜI DÙNG

- **Kha Khung Hiệp** — giáo viên Tổ Vật lí - Công nghệ, tác giả kiêm người vận hành chính hệ thống
  GEMS (`gems/` package). Thoải mái với chi tiết kỹ thuật sâu (Pydantic schema, CLI flags, kiến trúc
  pipeline Python) — có thể giao việc ở mức "sửa schema", "thêm flag CLI" mà không cần giải thích lại
  khái niệm lập trình cơ bản.
- Hai phạm vi công việc tách biệt rõ ràng:
  1. **Hệ thống GEMS** (`gems/` package) — pipeline dùng chung, tái sử dụng cho **mọi bài Vật lý 12**
     Kết nối tri thức, không được thay đổi tuỳ tiện vì ảnh hưởng tới toàn bộ các bài đã/sẽ soạn.
  2. **Các bài one-off ngoài phạm vi GEMS** (ví dụ Bài 28 — Động lượng, Vật lý 10) — soạn thủ công
     bằng script Python riêng trong `output/<slug>/scripts/`, KHÔNG được đụng vào `gems/` hay đăng ký
     vào `curriculum.yaml`, chỉ tái sử dụng hạ tầng dùng chung (`gems.docx_export`, `gems.notebooklm`)
     như thư viện.
- Chu trình làm việc điển hình: giao yêu cầu nâng cấp/soạn tài liệu → Claude thực hiện → **người dùng
  tự mở file thật (docx/pptx/ảnh) để xem trực quan** → phát hiện lỗi cụ thể qua quan sát (ví dụ: ảnh
  ra landscape thay vì portrait, thiếu nhiệm vụ, tiêu đề lặp đôi) → phản hồi tiếp, thường dồn nhiều
  điểm sửa lớn vào 1 tin nhắn dài, chi tiết, đánh số rõ ràng. Không tin "báo cáo đã xong" nếu chưa tự
  xác minh — Claude cũng phải áp dụng nguyên tắc này (xem Phần D.3).
- **Quyết định tổng quát hóa (2026-07-08):** toàn bộ chuẩn thiết kế "2 bộ Slide" (Giáo viên + Phiếu
  học tập, thay thế Infographic) đúc kết từ đợt soạn Bài 28 **áp dụng cho Agent/hệ thống GEMS nói
  chung, không chỉ riêng Bài 28** — đã chốt vào `skills/gems_physics_skill.md` mục 4.2 (v9.5.0). Đây
  là ngoại lệ so với ràng buộc "không đụng gems/" ở mục (2) bên dưới: ràng buộc đó áp dụng cho việc
  ĐĂNG KÝ bài học vào `curriculum.yaml`/chạy pipeline thật cho Bài 28, không áp dụng cho việc rút ra
  chuẩn chung để cập nhật tài liệu skill — 2 việc tách biệt. **Code `gems/notebooklm/` đã viết lại
  theo chuẩn này (2026-07-08, xem B.7)** — pipeline GEMS thật hiện đã sinh đúng 2 bộ Slide.

---

## PHẦN B — YÊU CẦU HỆ THỐNG GEMS (VẬT LÝ 12, package `gems/`)

### B.1 Kiến trúc & vận hành

- Kiến trúc hiện tại: **v9.0** (viết lại toàn bộ 7/2026), hợp nhất 2 pipeline cũ từng tách rời/không
  tương thích (`engine/gems_agent.py` vs. `main.py`+`gems_analyzer.py`...) thành 1 package `gems/`
  duy nhất, 1 CLI duy nhất: `python -m gems <generate|compose|offline|notebooklm|full|lint|
  list-lessons> --lesson baiN`.
- Cấu trúc module: `config` (curriculum.yaml + identity.yaml) → `models` (Pydantic schema) →
  `prompts` (system prompt gửi Gemini) → `generation` (gọi Gemini hoặc nạp JSON tự soạn + ghi
  Markdown + tự sửa lỗi) → `docx_export` (Markdown → DOCX) → `qa` (lint Markdown + lint DOCX) →
  `notebooklm` (nlm CLI wrapper + prompt + poll/tải) → `pipeline` (RunReport trung thực + CLI).
- **3 đường sinh nội dung tương đương, dùng chung 1 đường ghi Markdown/xuất DOCX:**
  - `generate` — gọi Gemini API thật (cần `GEMINI_API_KEY`).
  - `offline` — dữ liệu mẫu (fixture), không cần API/mạng, dùng để test/demo.
  - `compose` — **AI agent đang trò chuyện (Claude chạy trong Antigravity IDE) tự soạn nội dung bằng
    suy luận trực tiếp**, không gọi API ngoài nào, ghi ra 4 file JSON khớp đúng schema Pydantic vào
    `output/<slug>/authored/` (`_architect.json`, `_worksheet.json`, `_homework.json`,
    `_lesson_plan.json`), rồi `compose` nạp lại và chạy chung đường xuất DOCX. Đây là đường dùng khi
    KHÔNG muốn cấu hình API key.
- Thêm bài học mới chỉ cần thêm 1 mục vào `gems/config/curriculum.yaml`, không sửa code.
- `RunReport`/`StageResult` ghi lại kết quả THẬT của từng bước (thành công/thất bại/cảnh báo) — không
  bao giờ in "HOÀN THÀNH" giả trong khi có thể đã âm thầm thiếu tài liệu.
- Bộ test `tests/` (~100 test) — **luôn chạy `python -m pytest tests/ -q` ngay sau khi sửa bất kỳ file
  nào trong `gems/`**, phải xanh 100% trước khi coi là xong việc.

### B.2 7 nguyên tắc sư phạm cốt lõi (`skills/gems_physics_skill.md` §2)

1. **Chính xác tuyệt đối** — bám sát SGK gốc Kết nối tri thức, chi tiết, không chung chung, không tự
   ý thêm chú thích ngoài luồng.
2. **Thuần Việt sư phạm** — không dùng tiếng Anh hoặc chú thích tiếng Anh trong tài liệu. Tên riêng
   khoa học (Newton, Joule, Pascal...) phải kèm chú thích tiếng Việt ở lần đầu xuất hiện.
3. **Tiến trình tuyến tính mạch lạc** — từ dễ đến khó, từ khám phá đến chốt lý thuyết và vận dụng.
4. **Bản chất khoa học & trực quan thực tế** — mọi nhiệm vụ/hình ảnh minh họa phải gắn liền bản chất
   hiện tượng thực tế, chuẩn xác vật lý.
5. **Tiêu chuẩn hình ảnh thực tế** — chỉ dùng ảnh chụp thực tế hoặc tư liệu khoa học chất lượng cao;
   KHÔNG dùng hoạt hình, đồ họa 3D ảo, hay ảnh sai vật lý.
6. **Tinh giản tối đa (thanh lọc)** — loại bỏ chú thích rườm rà, lời dẫn giải kỹ thuật dài dòng; chỉ
   giữ hệ thống nhãn/số thứ tự logic (Nhiệm vụ 1, 2, 3...).
7. **Đa dạng hóa nhiệm vụ học tập (Task Chain)** — chuỗi nhiệm vụ liên kết logic, liền mạch, luân
   phiên đa dạng từ 12 loại hình nhiệm vụ (xem B.3) — tránh lặp loại hình gây nhàm chán.

### B.3 12 loại hình nhiệm vụ học tập (`skills/gems_physics_skill.md` §3)

1. Ghép nối đa biến (Matching Matrix)
2. Sắp xếp tiến trình (Algorithmic Ordering)
3. Tìm và sửa lỗi Vật lý (Bug Buster)
4. Đúng/Sai có biện giải (Assertion Reasoning)
5. Trắc nghiệm bối cảnh (Contextual MCQ)
6. Điền khuyết trực quan (Visual Cloze Test)
7. Giải mã Meme Vật lý (Meme Analyzer)
8. Gỡ lỗi thiết kế kỹ thuật (Engineering Debugger)
9. Bóc phốt TikTok/Shorts (Fact Check Influencer)
10. Bản đồ lựa chọn sinh tử (Decision Tree)
11. Khai thác Infographic (Infographic Decryption)
12. Xây dựng mô hình (Model Builder)

Khi thiết kế nhiệm vụ: chủ động lập bảng đối chiếu **nhiệm vụ ↔ loại hình ↔ lý do chọn** để tự kiểm
tra tính đa dạng trước khi đưa người dùng duyệt (xem thêm Phần D.2).

### B.4 Yêu cầu nội dung theo từng loại tài liệu (trạng thái v9.4.1, mới nhất)

**4.1 Phiếu học tập (PHT)**
- Bám THẲNG tiến trình dạy thật trong KHBD — 1 trình tự phẳng, KHÔNG dùng khung lặp 4 phần/ĐVKT của
  bản cũ. Đúng 3 mục lớn: **1. Hình thành kiến thức mới** (mỗi ĐVKT 1 mục con, gồm nhiệm vụ khám phá +
  lý thuyết trọng tâm đục lỗ) → **2. Luyện tập** (mỗi ĐVKT 1 bài toán, gộp chung không lặp) →
  **3. Vận dụng** (nhiệm vụ vận dụng nâng cao nếu có + đọc mở rộng mỗi ĐVKT). **Không có mục cho Khởi
  động** (chỉ diễn ra trên lớp).
- Độ dài đường chấm điền khuyết `(1)....` phải ước lượng theo độ dài đáp án cần điền (ký hiệu ngắn ~4-7
  dấu chấm, cụm từ dài hơn ~10-12 dấu chấm) — không dùng 1 độ dài cố định cho mọi chỗ trống. Áp dụng
  cho cả PHT bản Word lẫn Infographic đọc lại.
- Đồng bộ tiêu đề ĐVKT/nhiệm vụ 1-1 với Slide và KHBD.
- Mọi nhiệm vụ bắt buộc có dòng **"Hướng dẫn thực hiện"**: (1) hình thức tổ chức, (2) thời gian cụ
  thể, (3) tài liệu/công cụ phải dùng — không bỏ trống.
- Mục Luyện tập phải diễn đạt theo đúng 1 trong 3 dạng câu hỏi đề thi tốt nghiệp THPT (nguyên tắc
  "luyện đề ngay khi học", không đợi đến Bài tập về nhà).
- Khoảng trống viết bài dùng placeholder `[DOT_LINE_90]`.

**4.2 Slide bài giảng — 2 BỘ tách biệt (qua NotebookLM)** — chuẩn CHỐT áp dụng cho MỌI bài học,
không riêng bài nào (quyết định tổng quát hóa từ đợt thiết kế Bài 28 — Động lượng; code
`gems/notebooklm/` đã viết lại theo chuẩn này, xem B.7):

- **2 bộ tách biệt hoàn toàn, cùng notebook, cùng nội dung/đánh số, khác vai trò + bảng màu:**
  - **Slide Giáo viên** (trình chiếu cả lớp): mỗi nhiệm vụ tách ĐÚNG 2 slide liên tiếp — "Nhiệm vụ"
    (CHỈ tên nhiệm vụ + 3 ý Hình thức/Thời gian/Tài liệu lấy nguyên văn KHBD, không đề bài) và "Đáp
    án" (CHỈ đáp án + ảnh, không lặp hướng dẫn) — áp dụng MỌI nhiệm vụ, không ngoại lệ (kể cả Luyện
    tập/Vận dụng). Màu sắc tươi mới/hài hòa/giàu năng lượng, đồ họa thu hút. Cỡ chữ CỐ ĐỊNH: tiêu đề
    32pt, nội dung 28pt.
  - **Slide Phiếu học tập** (dùng bởi học sinh): mỗi nhiệm vụ 1 slide DUY NHẤT (hướng dẫn + đầy đủ câu
    hỏi nguyên văn + khoảng trống kẻ ngang để viết trực tiếp). **TUYỆT ĐỐI không có slide đáp án nào**
    trong toàn bộ deck, kể cả Kiến thức trọng tâm (chỉ điền khuyết) hay kết bài (chỉ khung trống). Nền
    trắng tuyệt đối, ảnh chỉ trắng/đen/xám. Cỡ chữ CỐ ĐỊNH: tiêu đề 24pt, nội dung 20pt.
  - Ảnh minh họa 2 bộ giống hệt bố cục/nội dung/nhãn chữ, chỉ khác màu — soạn 1 bộ mô tả dùng chung.
- **Master slide dùng chung:** cùng phân cấp tiêu đề, cùng bố cục mỗi LOẠI slide (Nhiệm vụ/Đáp
  án/Kiến thức trọng tâm/Đọc thêm/Mục lục/Phân đoạn — mỗi loại đúng 1 khuôn mẫu cố định xuyên suốt),
  cùng vị trí số trang, cùng kiểu khung ảnh.
- **Cấu trúc bắt buộc riêng của Slide Giáo viên:** 1 slide Mục lục ngay sau bìa; 1 slide "phân đoạn"
  riêng (chỉ tiêu đề in hoa + ảnh, không nội dung khác) trước mỗi phần lớn mới.
- Số trang "Trang X/Y" góc dưới phải, cỡ chữ cố định 16pt, mọi slide kể cả bìa, cả 2 bộ.
- Trục số X.Y duy nhất lấy trực tiếp từ số mục PHT, không dùng thuật ngữ viết tắt "ĐVKT".
- **Theme màu/font thương hiệu Anthropic** cho Slide Giáo viên (khác Primary/Times New Roman của
  PHT/KHBD/Bài tập — có chủ đích): Dark `#141413`/Light `#FAF9F5` nền/chữ chính, nhấn luân phiên
  Orange `#D97757`/Blue `#6A9BCC`/Green `#788C5D`, font tiêu đề **Poppins** + thân bài **Lora**.
- Không tiếng Anh ở bất kỳ đâu kể cả nhãn khung/hộp; không lộ đáp án qua chú thích ảnh ở slide điền
  khuyết bên Phiếu học tập; không dùng dấu ngoặc vuông/placeholder trong nội dung hiển thị thật.
- **KHBD là nguồn tham chiếu duy nhất**, sinh ra ĐẦU TIÊN — mọi câu Hình thức/Thời gian/Tài liệu trên
  slide copy nguyên văn từ đây, không tự diễn đạt lại. Toàn bộ tài liệu phải đồng bộ 100%.
- Đa dạng đúng 12 loại hình nhiệm vụ (B.3), tránh lặp gây nhàm chán.
- Slide kết bài: sơ đồ tư duy tổng hợp (Giáo viên điền đủ, Phiếu học tập chỉ khung trống).

**4.3 Kế hoạch bài dạy (KHBD, chuẩn Phụ lục IV — Công văn 5512)**
- Cấu trúc Mở đầu → Hình thành kiến thức mới → Luyện tập → Vận dụng; nếu bài có ≥2 ĐVKT, tách hoạt
  động Hình thành kiến thức thành nhiều hoạt động riêng theo từng ĐVKT, ghi rõ "(tương ứng PHT mục
  X — ĐVKT i)" để đối chiếu 1-1.
- Mỗi hoạt động: a) Mục tiêu / b) Nội dung / c) Sản phẩm / d) Tổ chức thực hiện (4 bước CV5512:
  Chuyển giao → Thực hiện → Báo cáo → Kết luận). Bước 1 (Chuyển giao) của MỌI hoạt động phải nêu đủ 3
  ý: hình thức/thời gian/tài liệu — **giống hệt yêu cầu ở PHT**.
- Hoạt động Luyện tập bắt buộc ≥1 câu theo đúng 1 trong 3 dạng đề thi tốt nghiệp THPT.
- Chọn 1-2 kĩ thuật dạy học tích cực phù hợp mỗi hoạt động (nguồn: `17_KY_THUAT_DAY_HOC_TICH_CUC.md`),
  cơ chế kĩ thuật phải thể hiện trong tiến trình, không chỉ ghi tên suông.
- Tích hợp năng lực số theo Công văn 3456 (lớp 10-12 dùng mức Nâng cao 1), chỉ gắn mã khi hoạt động có
  công cụ/thao tác số thật, không gượng ép.
- Không dùng khung 5E/IDB hay mô hình nước ngoài khác.
- Format kỹ thuật: header không có Quốc hiệu-Tiêu ngữ/Sở GD&ĐT; bảng thông tin 3×4 gồm Họ tên giáo
  viên/Môn học/Tên bài dạy/Lớp/Thời gian; mục d) là 1 bảng 2 cột (Hoạt động GV-HS gộp | Sản phẩm),
  KHÔNG tách 2 cột GV/HS riêng; chữ ký cuối bài 3 cột (Ban giám hiệu/Tổ trưởng/Giáo viên soạn bài).

**4.4 Bài tập về nhà** (đối chiếu trực tiếp đề thi thật mã đề 0227/2025, 0214/2026)
- Cấu trúc: Phần I (18 MCQ: 6 Nhận biết + 6 Thông hiểu + 6 Vận dụng, không xáo trộn tỉ lệ) → Phần II
  (4 câu Đúng/Sai, mỗi câu 4 ý a-d, MỘT bối cảnh duy nhất triển khai thành chuỗi liên kết, tối thiểu 1
  ý định tính + cài ít nhất 1 bẫy quan niệm sai lầm) → Phần III (6 câu trả lời ngắn, ghép cặp dùng
  chung dữ kiện theo mẫu "Dùng thông tin sau cho câu X và câu Y", mỗi câu nêu rõ quy tắc làm tròn).
- Toàn bộ phương án nhiễu phải bắt nguồn từ quan niệm sai lầm đã phân tích, không bịa ngẫu nhiên.
- Tối thiểu 50% tổng số câu (cả 3 phần) gắn bối cảnh thực tế.
- **Không in đáp án Đúng/Sai ngay trong đề** — đáp án chỉ ở mục hướng dẫn giải cuối file.
- **Hình thức trình bày KHÔNG đóng giả đề thi thật** (từ v9.4.0): header đơn giản như PHT/KHBD (tiêu
  đề bài + Họ tên học sinh/Lớp), KHÔNG có Sở GD&ĐT/Trường THPT/"Đề có N trang"/Mã đề thi/Số báo
  danh/"Thời gian làm bài" — chỉ CÂU HỎI mới bám phong cách đề tốt nghiệp, không phải vỏ hình thức.
- Chân trang phần đề: "----- HẾT -----" đơn giản (không còn ngôn ngữ đóng vai coi thi).
- Footer căn giữa "Trang {PAGE}/{NUMPAGES}", dùng chung với PHT/KHBD.
- Ảnh minh họa chỉ đặt trên dòng độc lập (`shared_context`), không xen giữa câu dẫn và phương án.

**4.5 Infographic học sinh — ĐÃ LOẠI BỎ khỏi chuẩn chung**
Thay thế hoàn toàn bằng bộ "Slide Phiếu học tập" ở mục 4.2 (quyết định áp dụng cho MỌI bài học, không
riêng Bài 28) — lý do: N+2 ảnh AI độc lập dễ thiếu đồng bộ tên bài/tên học sinh/hình ảnh giữa các ảnh
với nhau, trong khi slide đảm bảo đồng bộ tuyệt đối. (Thông số cũ — N+2 ảnh cố định, ép `--orientation
portrait --style scientific`, bong bóng thoại trống `?`/`(1)`/`(2)`/`(3)` — chỉ còn giá trị tham khảo
lịch sử, không còn là chuẩn cần tuân theo.)

**4.6 Minh họa khoa học (áp dụng mọi loại tài liệu)**
- **Vector tự vẽ (matplotlib, `gems/illustrations/`)** ưu tiên tuyệt đối cho sơ đồ thí nghiệm/dụng
  cụ, đồ thị số liệu, sơ đồ nguyên lý/chu trình — không có rủi ro AI vẽ sai chi tiết khoa học.
- **Ảnh AI (người dùng tự tạo qua Antigravity)** chỉ dùng khi cần hiện thực mà vector không lột tả
  được — Claude soạn sẵn mô tả ảnh chi tiết, khoa học, chú thích tiếng Việt, cấm phong cách hoạt hình.
- Cấm tuyệt đối phong cách hoạt hình/cartoon/3D ảo/phóng đại phi thực tế ở MỌI hình thức minh họa.

### B.5 Yêu cầu định dạng kỹ thuật DOCX (`.agents/agents.md` — nguồn thật duy nhất)

- **Lề trang & độ rộng bảng** (từ `gems/docx_export/layout.py`):

  | Loại tài liệu | Trên | Dưới | Trái | Phải | Độ rộng bảng |
  |---|---|---|---|---|---|
  | Phiếu học tập | 2.0cm | 2.0cm | 2.0cm | 2.0cm | 17.0cm |
  | KHBD (CV5512) | 2.0cm | 2.0cm | 3.0cm | 2.0cm | 16.0cm |
  | Bài tập về nhà | 1.5cm | 1.5cm | 2.0cm | 2.0cm | 17.0cm |

- **Font & màu** (từ `gems/docx_export/palette.py`): Times New Roman toàn bộ; Title 16pt · H1 14pt
  đậm `#1F4E79` · H2/H3 13pt (H3 nghiêng, đen) · Header bảng 12pt · Ô bảng/chú thích 11pt · Thân bài
  13pt · Chữ nhỏ (footer/dot-line) 9pt. Primary `#1F4E79` (tiêu đề) · Dark `#000000` (thân bài) ·
  Header bảng nền `#D9D9D9` · Viền/dot-line `#BFBFBF`.
- **Cú pháp Markdown nhận diện**: `##`/`###`/`####` → heading cấp 1/2/3; `-`/`*` bullet cấp 1, `+`
  bullet cấp 2 (luôn ký tự thật, không glyph Unicode thô); `>` blockquote; `[DOT_LINE_90]` → dòng
  chấm 90 ký tự; dòng toàn dấu `-` → dòng kẻ phân cách; bảng pipe `| ... |` → `make_table()`; ảnh theo
  pattern `ready/.../*.png|jpg|jpeg` được tự động tách và chèn.
- **Chữ chạy** (`run_formatter.add_formatted_runs`): `**đậm**`, `*nghiêng*`, `$latex$` (nghiêng, qua
  `clean_latex()`), `==highlight==` (tô vàng `WD_COLOR_INDEX.YELLOW`).
- Khổ A4 cho mọi loại tài liệu; footer dùng chung `styles.add_page_number_footer()`.

### B.6 Bộ 15 tiêu chí QA self-check (`skills/gems_physics_skill.md` §5)

- **PHT (6 tiêu chí):** không gian trống 35-40%, ảnh chuẩn khoa học, đúng 3 mục phẳng tuyến tính,
  thuần Việt, khoảng trống dùng placeholder chuẩn, đủ nhiệm vụ đa dạng loại hình + đủ dòng Hướng dẫn
  thực hiện.
- **Slide (5 tiêu chí):** đồng bộ 1-1 với PHT, có ảnh minh họa mỗi slide, đúng font/highlight, đủ cấu
  trúc slide theo outline, thuần Việt.
- **Bài tập về nhà (4 tiêu chí):** phương án nhiễu bắt nguồn quan niệm sai lầm, ≥50% câu thực tế, đúng
  cơ cấu 18+4+6 theo phong cách đề thi thật, LaTeX sạch + đáp án tách riêng.

### B.7 Trạng thái hiện tại & giới hạn đã biết (cập nhật 2026-07-08)

- `skills/gems_physics_skill.md` **v9.5.0** — nguồn chuẩn nội dung, đã chốt chuẩn "2 bộ Slide" thay
  Infographic (mục 4.2/4.5). `.agents/agents.md` — nguồn chuẩn định dạng, khớp code thật.
- **Code đã migrate xong (2026-07-08):** `gems/notebooklm/prompt_builder.py` và `pipeline.py` đã
  viết lại theo đúng chuẩn "2 bộ Slide" — đọc dữ liệu PHT thật qua `{slug}_worksheet_data.json`
  (`gems.generation.stages.write_worksheet_json`, ghi cùng lúc với `_phieu_hoc_tap.md`), dựng danh
  sách slide dạng "SLIDE N: ..." đánh số tường minh, và tự đếm số slide thật (`python-pptx`) sau khi
  tải về để phát hiện trường hợp NotebookLM cắt ngang. `PracticeItem` (mục 2. Luyện tập của PHT) nay
  cũng có trường `instructions` (Hình thức/Thời gian/Tài liệu), khớp yêu cầu "MỌI nhiệm vụ không
  ngoại lệ" của skill 4.2. 109 test trong `tests/` đã cập nhật theo, chạy xanh 100%.
- **Bài 28 (Vật Lý 10, one-off, xem Phần C)** vẫn dùng script Python thủ công riêng (không qua
  `gems/notebooklm/`) — đó là bản one-off gắn với nội dung cụ thể của bài đó, không tự động chuyển
  sang dùng lại code GEMS chung.
- **Bài 7 (Nhiệt hóa hơi riêng)** là bài "flagship" mẫu cho mọi chuẩn mới nhất, đã qua 3 đợt nâng cấp
  lớn liên tiếp (chuẩn đề thi tốt nghiệp → đánh số X.Y đồng bộ + hướng dẫn thực hiện + minh họa khoa
  học → bỏ header giả đề thi + PHT phẳng 3 mục + N+2 infographic + theme Anthropic) — **chưa** chạy
  lại qua NotebookLM để tái tạo Slide theo chuẩn "2 bộ Slide" mới (code đã sẵn sàng, chỉ chưa thực thi
  thật vì tốn quota NotebookLM — cần xác nhận riêng trước khi chạy).
- **Bài 1-6 CHƯA migrate** sang chuẩn PHT phẳng mới nhất — nếu được yêu cầu sửa/xem các bài này, cần
  hỏi có muốn migrate không trước khi giả định cấu trúc.
- Giới hạn "chèn ảnh vào Bài tập về nhà" đã được sửa xong (hỗ trợ đầy đủ, chỉ ràng buộc: ảnh phải đặt
  trên dòng độc lập, không xen giữa câu dẫn và phương án A-D/mệnh đề a-d).
- Bộ vẽ minh họa: `gems/illustrations/style.py` (matplotlib — máy không có `cairo` gốc nên không dùng
  được đường SVG→PNG).
- NotebookLM: tài khoản đã đăng nhập `khakhunghiep@gmail.com`, `nlm` CLI có sẵn trên PATH. **Lưu ý
  quan trọng phát hiện ở đợt Bài 28:** lệnh `nlm create slides` có giới hạn tần suất (rate limit) theo
  giờ — gọi quá nhiều lần liên tiếp trong thời gian ngắn (nhiều vòng tạo lại 1 bộ slide) sẽ bị chặn
  "RESOURCE_EXHAUSTED", cần chờ (thực tế đã gặp: chờ 5 phút chưa đủ, phải chờ lâu hơn ~25-30 phút).

---

## PHẦN C — DỰ ÁN RIÊNG: BÀI 28 - ĐỘNG LƯỢNG (VẬT LÝ 10, ONE-OFF)

### C.1 Bối cảnh & ràng buộc nền tảng

- Yêu cầu ban đầu: soạn bộ tài nguyên dạy học cho "Bài 28 – Động lượng", Vật Lý 10, chương trình Kết
  nối tri thức, dùng làm tài liệu tham khảo một lần: KHBD mẫu của **Trường THCS và THPT Đinh Thiện
  Lý**, 3 ảnh trang SGK Vật Lý 10 Bài 28, và 1 bảng TIÊU CHÍ ĐÁNH GIÁ (PDF).
- **Ràng buộc tuyệt đối, nhắc lại nhiều lần:** đây là việc **MỘT LẦN (one-off)**, **KHÔNG được điều
  chỉnh** skill/pipeline GEMS dùng chung (`gems/`, `skills/gems_physics_skill.md`, `.agents/agents.md`)
  — chỉ dùng các tài liệu tham khảo này để soạn 1 lần, không đăng ký bài học vào
  `curriculum.yaml`. Cách làm đã chọn: dựng `LessonSpec` trực tiếp bằng Python trong từng script riêng
  ở `output/bai28_dong_luong/scripts/`, tái sử dụng `gems.docx_export`/`gems.notebooklm` như thư viện.
- 2 yêu cầu cần đạt của bài: (1) định nghĩa + ý nghĩa động lượng; (2) công thức liên hệ lực – tốc độ
  biến thiên động lượng = dạng 2 của định luật II Newton.
- Thời lượng: **1 tiết (45 phút)**, gộp cả 2 yêu cầu cần đạt trong 1 buổi học.

### C.2 Yêu cầu bộ 5 tài liệu (tiến hóa qua các vòng phản hồi)

Bộ tài liệu cuối cùng gồm đúng 5 file:
1. **KHBD** (Kế hoạch bài dạy) — file `.docx`, theo đúng mẫu "Đinh Thiện Lý" (landscape, bảng 5 cột
   Hoạt động|Mục tiêu|Chi tiết hoạt động|Nội dung kiến thức|Ghi chú).
2. **PHT** (Phiếu học tập) — file `.docx`, custom hoàn toàn (không dùng `gems/docx_export/
   pht_exporter.py`).
3. **Bài tập về nhà** — file `.docx`, tái sử dụng `gems.docx_export.homework_exporter`.
4. **Slide Giáo viên** (trình chiếu cả lớp) — sinh bằng **NotebookLM** (`nlm create slides`), KHÔNG
   phải Claude tự dựng bằng python-pptx/pptxgenjs.
5. **Slide Phiếu học tập cho học sinh** (bản chiếu số hóa của PHT giấy) — cũng sinh bằng NotebookLM,
   tách biệt hoàn toàn khỏi Slide Giáo viên.

**Lịch sử tiến hóa yêu cầu (để hiểu vì sao có cấu trúc hiện tại):**
- Ban đầu định làm 4 ảnh Infographic riêng cho PHT — bị huỷ vì thiếu đồng bộ hình ảnh giữa các ảnh độc
  lập do AI vẽ; thay bằng slide (đảm bảo đồng bộ tên bài/tên học sinh/nhiệm vụ).
- Ban đầu Claude tự dựng slide bằng `pptxgenjs` — **bị từ chối, đây là hiểu lầm nghiêm trọng**: người
  dùng khẳng định rõ **slide phải được tạo bằng công cụ NotebookLM**, không phải Claude tự tạo.
- PDF: **không cần bất kỳ file PDF nào** trong toàn bộ quy trình — đã loại bỏ hoàn toàn bước xuất PDF.

### C.3 Yêu cầu cấu trúc PHT (đã chốt, không đổi thêm)

- Đánh số 4 mục lớn: **1. Khởi động** / **2. Hình thành kiến thức mới** (2.1, 2.2) / **3. Luyện tập**
  (3.1, 3.2) / **4. Vận dụng - Mở rộng** (4.1, 4.2); sub-mục đánh chữ a/b/c.
- **Bỏ hẳn thuật ngữ "ĐVKT"** ở MỌI tài liệu (PHT/KHBD/Slide) — thay bằng số mục trực tiếp (2.1, 2.2...).
- Khoảng trống viết câu trả lời: **dòng kẻ ngang liền nét** (không phải chấm chấm), độ dài tỉ lệ với
  độ dài câu trả lời kỳ vọng — làm bằng kỹ thuật viền dưới đoạn văn (`OxmlElement`/`qn`), không phải
  bảng.
- "Kiến thức trọng tâm" trình bày dạng gạch đầu dòng ngắn gọn, KHÔNG phải đoạn văn dài.
- **Hoạt động 2 (mục 2.1 Động lượng) phải cho học sinh TỰ TAY làm thí nghiệm SGK Hình 28.1** (3 viên
  bi A/B/C trên máng trượt) để rút ra kết luận, thay vì chỉ thảo luận thí nghiệm được mô tả suông.

### C.4 Yêu cầu KHBD

- Theo đúng mẫu Đinh Thiện Lý, 5 hoạt động: Khởi động (5') → 2.1 Động lượng (12', có thí nghiệm trực
  tiếp) → 2.2 Xung lượng của lực (15', đánh dấu "★ Đề xuất demo") → Luyện tập (8') → Vận dụng, củng cố
  và dặn dò (5').
- Mỗi bước "Chuyển giao" của mọi hoạt động phải nêu đủ 3 ý Hình thức/Thời gian/Tài liệu — dùng làm
  NGUỒN GỐC duy nhất cho các tài liệu khác trích dẫn lại (xem C.5, yêu cầu mới nhất).

### C.5 Yêu cầu 2 bộ Slide NotebookLM (Giáo viên / Học sinh)

**Đã tổng quát hóa thành chuẩn CHUNG cho toàn bộ GEMS** (không còn là yêu cầu riêng của Bài 28) — xem
đầy đủ toàn bộ điểm yêu cầu (phân vai Giáo viên/Học sinh, thiết kế/màu sắc/cỡ chữ, master slide, số
trang, mục lục, slide phân đoạn, nhãn nhiệm vụ đồng bộ KHBD, UI/UX nhất quán) tại **Phần B.4 mục 4.2**
ở trên và `skills/gems_physics_skill.md` mục 4.2 (v9.5.0) — đây là 2 nguồn duy nhất, không lặp lại chi
tiết ở đây để tránh lệch nhau theo thời gian. Riêng với Bài 28: cách triển khai THỰC TẾ là script
Python thủ công (`output/bai28_dong_luong/scripts/build_notebooklm.py` +
`build_notebooklm_phan4.py`), KHÔNG qua `gems/notebooklm/pipeline.py` — dù code dùng chung nay đã hỗ
trợ chuẩn tương tự (xem B.7), Bài 28 vẫn giữ nguyên script one-off riêng vì gắn với nội dung cụ thể
của bài đó.

### C.6 Trạng thái hiện tại & việc còn dang dở (tại thời điểm viết tài liệu này)

- Đã trải qua **7 vòng tạo lại** Slide qua NotebookLM, mỗi vòng phát hiện và sửa lỗi cụ thể qua QA
  trực quan (dùng subagent kiểm tra từng ảnh slide render ra PNG), theo mẫu hình "sửa lỗi này, phát
  sinh lỗi khác" — bài học rút ra: **prompt quá dài/quá nhiều yêu cầu cùng lúc có thể khiến NotebookLM
  cắt ngang giữa chừng (silent truncation)** hoặc in ra literal text không mong muốn (ví dụ dấu ngoặc
  vuông `[...]` dùng làm placeholder trong prompt bị AI chép y nguyên vào slide; chú thích cỡ chữ như
  "(32pt)" bị in thành text hiển thị).
- **Slide Phiếu học tập (13 slide):** đã đạt yêu cầu — tách nhiệm vụ/câu hỏi đúng, không lộ đáp án,
  đúng số phương án trắc nghiệm, số trang đầy đủ, ảnh grayscale khớp bố cục ảnh màu.
- **Slide Giáo viên:** vòng 7 sinh được 21/27 slide đúng yêu cầu (từ slide bìa đến "Đáp án 3.2") rồi
  bị cắt ngang do NotebookLM hết "ngân sách sinh" giữa chừng — thiếu toàn bộ 6 slide cuối (phần "4.
  Vận dụng - Mở rộng": slide phân đoạn, đọc thêm tên lửa, nhiệm vụ + đáp án mũ bảo hiểm lót thép, đọc
  thêm túi khí, slide kết bài sơ đồ tư duy).
- **Giải pháp kỹ thuật đã chọn** (thay vì tạo lại toàn bộ 27 slide và rủi ro lặp lỗi ở phần đã tốt):
  viết script riêng (`build_notebooklm_phan4.py`) chỉ yêu cầu NotebookLM sinh bổ sung ĐÚNG 6 slide còn
  thiếu (đánh số tiếp nối 22-27/27), rồi ghép nối vào cuối deck 21-slide hiện có bằng cách copy từng
  slide-là-1-ảnh-toàn-slide qua `python-pptx` (mỗi slide NotebookLM xuất ra là 1 ảnh full-bleed duy
  nhất, không phải text layer thật — nên việc ghép chỉ cần copy đúng ảnh + vị trí/kích thước).
- Việc ghép nối đang bị chặn bởi **rate limit của NotebookLM** (`RESOURCE_EXHAUSTED`, "Wait a few
  minutes") do gọi `create_slides` quá nhiều lần trong 1 phiên (8+ lần trong vài giờ) — cần chờ lâu
  hơn dự kiến ban đầu (>5 phút, có thể tới 25-30 phút) trước khi thử lại.
- 2 lỗi nhỏ còn tồn đọng trong 21 slide đã có (không chặn tiến độ, có thể sửa thủ công hoặc chấp nhận):
  1 dòng bị lặp trên slide "Kiến thức trọng tâm 2.1", và chữ "độ" bị rớt trong câu "tốc, 54 km/h" ở
  slide "Đáp án 3.1".

---

## PHẦN D — QUY TẮC LÀM VIỆC CHUNG (WORKFLOW PREFERENCES)

Áp dụng chung cho cả hệ thống GEMS và các dự án one-off, đúc kết từ phản hồi lặp lại ổn định:

### D.1 Quy trình nâng cấp kiến trúc GEMS (khi đổi schema/pipeline dùng chung)

1. **Đọc code thật trước khi lập kế hoạch** — không suy đoán cấu trúc hiện tại; dùng Explore agent
   nếu phạm vi rộng.
2. **Vào Plan Mode cho thay đổi đa file** — plan có mục Bối cảnh (why) + việc làm theo nhóm file, xin
   duyệt qua `ExitPlanMode` trước khi sửa code.
3. **Hỏi làm rõ (AskUserQuestion) trước khi có ≥2 cách hiểu hợp lý ngang nhau** — không tự đoán các
   quyết định chỉ người dùng mới quyết được.
4. **Phạm vi mặc định khi nâng cấp:** áp dụng khung dùng chung cho mọi bài sau + làm lại đầy đủ 1 bài
   flagship làm ví dụ chuẩn. Các bài khác KHÔNG tự động migrate trừ khi được yêu cầu rõ ràng.
5. **Chạy `pytest` ngay sau mỗi thay đổi lớn**, không dồn đến cuối.
6. **Luôn xác minh bằng mắt** — render PDF/PNG, mở docx đếm `inline_shapes`, kiểm tra kích thước ảnh...
   Không tin "code chạy không lỗi" là đủ.
7. **Khi lời văn prompt không đáng tin cậy, tìm cơ chế tin cậy hơn ở tầng thấp hơn** (ví dụ: flag CLI
   gốc thay vì chỉ yêu cầu bằng lời trong prompt AI) trước khi viết thêm câu chữ thuyết phục.

### D.2 Quy trình soạn HÀNG LOẠT tài liệu (bộ nhiều file: KHBD/PHT/Bài tập/Slide/Infographic)

- Luôn dựng trước 1 file đặc tả `.md` có bảng ma trận mô tả cụ thể từng tài liệu (nhiệm vụ nào, hiển
  thị gì, màu/nền gì...) và **DỪNG LẠI xin xác nhận rõ ràng** trước khi chạy các bước tạo hàng loạt
  tốn kém (đặc biệt bước gọi NotebookLM). Không tự ý chạy thẳng khi chưa có xác nhận.
- Khi thiết kế nhiệm vụ, chủ động đa dạng hoá đúng 12 loại hình (Phần B.3), lập bảng đối chiếu
  nhiệm vụ↔loại hình↔lý do chọn để tự kiểm tra trước khi đưa duyệt.

### D.3 Xác minh trực quan bắt buộc (cho mọi loại tài liệu, không riêng docx)

- Không bao giờ báo "đã xong" chỉ dựa trên exit code/log — luôn tự kiểm tra output thực tế: mở
  docx/pptx, render ảnh PNG (qua PowerPoint COM automation trên Windows, luôn xuất vào thư mục
  scratchpad, không commit PDF vào dự án), dùng PIL kiểm tra kích thước ảnh.
- Với các script chạy nền in tiếng Việt ở dòng cuối: **lỗi crash cp1252 khi `print()` tiếng Việt trên
  console Windows là lỗi biết trước, KHÔNG ảnh hưởng đến kết quả thật** — luôn kiểm tra file output có
  tồn tại trước khi kết luận thất bại. (Có thể phòng tránh triệt để bằng
  `sys.stdout.reconfigure(encoding="utf-8")` ở đầu script nếu cần in kết quả tin cậy giữa chừng.)
- Khi phát hiện lỗi qua QA trực quan, báo cáo rõ ràng cho người dùng (qua tóm tắt hoặc
  `AskUserQuestion`) trước khi tự ý sửa lại toàn bộ — đặc biệt với các thao tác tốn kém/có giới hạn
  tần suất (gọi lại NotebookLM nhiều lần).

---

*Tài liệu này tổng hợp tại thời điểm 2026-07-08, dựa trên `changelog.md` (lịch sử đến bản v9.4.1),
`skills/gems_physics_skill.md`, `.agents/agents.md`, `readme.md`, và toàn bộ yêu cầu chi tiết của đợt
soạn Bài 28 - Động lượng (Vật Lý 10) trong phiên làm việc gần nhất. Khi có yêu cầu mới hoặc thay đổi so
với các mục ở trên, cập nhật trực tiếp vào tài liệu này để giữ vai trò "1 nguồn duy nhất".*
