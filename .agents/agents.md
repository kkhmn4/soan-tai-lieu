# Quy tắc dự án: Định dạng & Kiến trúc GEMS (package `gems/`)

Tài liệu này mô tả đúng những gì package `gems/` (kiến trúc v9.0, xây lại toàn bộ
7/2026) đang làm — không phải một bản đặc tả lý tưởng tách rời code. Mọi con số
lề/màu/font dưới đây được lấy trực tiếp từ `gems/docx_export/layout.py` và
`gems/docx_export/palette.py`; khi sửa code, sửa tài liệu này trong cùng lần sửa.

## 1. Kiến trúc tổng quan

Một pipeline duy nhất (`gems/pipeline/orchestrator.py::GEMSPipeline`), không còn
2 đường song song như bản trước 7/2026:

```
gems/config       -> curriculum.yaml (danh mục bài học) + identity.yaml (tên GV/brand/model)
gems/models       -> Pydantic schema (khai đúng 1 lần/schema)
gems/prompts      -> prompt hệ thống gửi Gemini
gems/generation   -> gọi Gemini (gemini_client.py) HOẶC nạp JSON do AI agent tự soạn (from_json.py) + ghi Markdown (stages.py) + tự sửa lỗi (self_correction.py)
gems/docx_export  -> Markdown -> DOCX (layout/palette/styles/run_formatter/markdown_ir/renderer + 3 exporter)
gems/qa           -> lint Markdown (regex) và lint DOCX đã biên dịch (cấu trúc)
gems/notebooklm   -> nlm CLI wrapper + tạo prompt + poll/tải 2 bộ Slide (Giáo viên + Phiếu học tập)
gems/pipeline     -> RunReport (báo cáo trung thực từng bước) + orchestrator + cli.py
```

CLI: `python -m gems <generate|compose|offline|notebooklm|full|lint|list-lessons> --lesson bai4`
(hoặc `--prompt "soạn bài 4 nhiệt dung riêng"`).

`generate` gọi Gemini API thật (cần `GEMINI_API_KEY`). `compose` KHÔNG gọi API
nào — dùng khi chính AI agent đang chạy trong Antigravity IDE tự soạn nội
dung bằng suy luận trực tiếp, ghi ra 4 file JSON khớp schema
`gems/models/*.py` vào `output/<slug>/authored/` (`{slug}_architect.json`,
`_worksheet.json`, `_homework.json`, `_lesson_plan.json`), rồi `compose` nạp
lại và chạy chung 1 đường ghi Markdown + xuất DOCX như `generate`/`offline`
(`gems/generation/from_json.py`).

## 2. Lề trang & độ rộng bảng (nguồn thật: `gems/docx_export/layout.py`)

| Loại tài liệu | Trên | Dưới | Trái | Phải | Độ rộng bảng (suy ra) |
|---|---|---|---|---|---|
| Phiếu học tập (`pht`) | 2.0cm | 2.0cm | 2.0cm | 2.0cm | 17.0cm |
| Giáo án CV5512 (`khbd`) | 2.0cm | 2.0cm | 3.0cm | 2.0cm | 16.0cm |
| Bài tập về nhà (`homework`) | 1.5cm | 1.5cm | 2.0cm | 2.0cm | 17.0cm |

Không có giá trị "16.5cm cố định" hay "lề phải luôn 1.5cm" — đó là số liệu của
bản trước 7/2026 đã lệch khỏi code từ lâu. Mọi bảng PHẢI qua
`gems.docx_export.styles.set_table_width_dxa()` hoặc `make_table()` — không tự
viết `w:tblW` ở nơi khác.

## 3. Màu & Font (nguồn thật: `gems/docx_export/palette.py`)

- Font: **Times New Roman** toàn bộ tài liệu.
- Cỡ chữ: Title 16pt · H1 14pt (đậm, `#1F4E79`) · H2/H3 13pt (H3 nghiêng, đen) ·
  Header bảng 12pt · Ô bảng/chú thích 11pt · Thân bài 13pt · Chữ nhỏ (footer/dot-line) 9pt.
- Màu: Primary `#1F4E79` (tiêu đề/H1) · Dark `#000000` (thân bài) ·
  Header bảng nền `#D9D9D9` chữ đen đậm · Viền/dot-line `#BFBFBF`.
  **Không có** màu Navy `#1E3A5F` hay xen kẽ dòng Mint `#E8F5E9` — đó là bảng
  màu của thế hệ exporter cũ (`gems_styles.py`, đã xoá), không phải bảng màu
  đang chạy.

## 4. Cú pháp Markdown được `gems.docx_export.markdown_ir` nhận diện

- `## ` / `### ` / `#### ` → heading cấp 1/2/3 (đếm số `#` thật, không cắt chuỗi
  theo offset cố định). `# ` (1 dấu thăng) cũng được nhận, quy về cấp 1.
- `- `, `* ` → bullet cấp 1; `+ ` → bullet cấp 2. Luôn hiển thị bằng ký tự gạch
  ngang/cộng thật trong text run — **không bao giờ** dùng glyph bullet Unicode thô.
- `> ` hoặc `>` đầu dòng → blockquote (thụt lề 1cm, nghiêng).
- `[DOT_LINE_90]` (đúng chuỗi này, riêng 1 dòng) → 1 dòng chấm 90 ký tự.
- Dòng chỉ gồm 3 dấu `-` trở lên (`---`, `-----`...) → dòng kẻ phân cách
  (`add_separator`), không còn bị in ra thành chữ "---" như trước.
- Bảng Markdown (`| ... |`) → dựng qua `make_table()` dùng chung. Trong KHBD,
  bảng đúng 2 cột VÀ có tiêu đề chứa "Sản phẩm" được coi là bảng tiến trình
  dạy học và dựng qua `khbd_exporter._make_process_table` (tô Primary cho 4
  nhãn Bước 1-4 CV5512, xem mục 5).
- Ảnh: pattern `ready/.../*.png|jpg|jpeg` trong dòng văn bản được tách ra, thử
  lần lượt: đường dẫn như đã ghi → `<gốc bài>/<đường dẫn>` →
  `<gốc bài>/ready/hinh_anh/<tên file>`; nếu tìm thấy, ảnh được chèn giữa
  trang ngay dưới đoạn văn chứa nó.
- **Chưa** hỗ trợ gộp nhiều dòng vật lý thành 1 đoạn văn (paragraph folding) —
  mỗi dòng Markdown = 1 đoạn Word. Bên sinh Markdown (`gems/generation/stages.py`)
  chịu trách nhiệm ghi đúng 1 dòng = 1 ý hoàn chỉnh.

## 5. Kế hoạch bài dạy (KHBD, chuẩn Phụ lục IV — Công văn 5512/BGDĐT-GDTrH)

Định dạng đã đối chiếu trực tiếp với `tai-lieu-goc/mẫu/mẫu KHBD 12.pdf` (bản
scan chính thức "Phụ lục IV — KHUNG KẾ HOẠCH BÀI DẠY") và bài soạn minh hoạ mẫu
trong cùng thư mục.

- Header hành chính: "Trường: ..." / "Tổ: {identity.department}" căn trái,
  **không có** khối Quốc hiệu - Tiêu ngữ, không có Sở GD&ĐT (Phụ lục IV thật
  không có 2 dòng này). Ngay dưới tiêu đề "KẾ HOẠCH BÀI DẠY" là bảng 3×4: **Họ
  và tên giáo viên** (`identity.teacher_name`) / Môn học / **Tên bài dạy** /
  Lớp / **Thời gian thực hiện**. Trường "Họ và tên giáo viên" từng vắng mặt
  hoàn toàn ở bản trước 7/2026 — đây là lỗi đã sửa, không phải tính năng mới
  tuỳ chọn.
- Mỗi hoạt động trình bày đúng cấu trúc a) Mục tiêu / b) Nội dung / d) Tổ chức
  thực hiện. Từ v9.1, sửa đầy đủ theo mẫu thành **a) Mục tiêu / b) Nội dung /
  c) Sản phẩm / d) Tổ chức thực hiện**; mục c) phải hiện thành dòng riêng,
  không chỉ nằm trong cột Sản phẩm. Mục d) là **1 bảng 2 cột duy nhất**: "Hoạt động của giáo viên và
  học sinh" (văn bản liên tục, gộp cả 4 bước với nhãn đậm "Bước 1: Chuyển giao
  nhiệm vụ:" → "Bước 4: Kết luận, nhận định:") | "Sản phẩm" (`act.product`).
  **Không còn** tách 2 cột GV riêng/HS riêng như bản trước — cách cũ tự chẻ đôi
  nội dung theo cặp khối phát hiện bằng regex, sinh ra câu HS giả không khớp
  dữ liệu thật (`_split_cell_into_blocks`/`_make_gv_hs_table`, đã xoá).
- Mỗi hoạt động ghi 1-2 **kĩ thuật dạy học tích cực** được chọn theo mục tiêu,
  quy mô lớp và thời lượng; bốn bước phải mô tả đúng cơ chế thực hiện của kĩ
  thuật. Danh mục nguồn: `tai-lieu-goc/mẫu/17_KY_THUAT_DAY_HOC_TICH_CUC.md`.
- KHBD có mục **Năng lực số (Công văn 3456/BGDĐT-GDPT)**. Với lớp 12 dùng
  mức Nâng cao 1; ghi mã năng lực thành phần, biểu hiện cần đạt và minh chứng.
  Mỗi hoạt động chỉ gắn mã khi có nhiệm vụ số thật. Nguồn:
  `tai-lieu-goc/mẫu/Cong-van-3456-Khung-Nang-luc-so.md`.
- Đúng 4 nhãn bước trên, khi ở dạng `**...**`, được tô màu Primary
  (`khbd_exporter._CV5512_KEYWORDS`, đã rút từ 13 cụm rời rạc kiểu diễn đạt
  khác nhau xuống đúng 4 nhãn chuẩn Phụ lục IV).
- Mục IV "Điều chỉnh bài dạy sau tiết giảng" luôn được dựng lại bằng tiêu đề
  chuẩn hoá + 1 dòng chấm dự phòng cho mỗi mục (Ưu điểm/Hạn chế/Hướng điều
  chỉnh), bất kể heading gốc trong Markdown viết gì.
- Chữ ký cuối bài: bảng **3 cột** — Ban giám hiệu / Tổ trưởng / Giáo viên soạn
  bài (không phải 2 cột).

## 6. Bài tập về nhà (bám PHONG CÁCH CÂU HỎI đề thi tốt nghiệp THPT, KHÔNG đóng giả hình thức đề thi)

Cấu trúc CÂU HỎI (Phần I/II/III, tỉ lệ nhận thức, shared_context...) đối chiếu
trực tiếp với các ảnh đề thi thật trong `tai-lieu-goc/mẫu/` (2 ảnh 2025, 2 ảnh
2026) — xem chi tiết ở `skills/gems_physics_skill.md` mục 4.4. Nhưng từ
v9.4.0, HÌNH THỨC trình bày (header/footer) KHÔNG còn mô phỏng đề thi thật
(từng có Sở GD&ĐT/Trường THPT/Mã đề thi/Số báo danh) — đây là bài tập về nhà
bình thường, dùng header đơn giản như PHT/KHBD (tiêu đề bài + Họ tên học
sinh/Lớp), không cần đóng giả hình thức đề thi.

- Cấu trúc: Phần I (mặc định 18 câu trắc nghiệm ABCD) → Phần II (4 câu Đúng/Sai,
  mỗi câu 4 ý a-d) → Phần III (6 câu trả lời ngắn). Số lượng không bị ép cứng
  bằng validator — `gems/generation/stages.py::generate_homework_content` kiểm
  tra sau khi Gemini trả lời, tự yêu cầu sinh lại (tối đa 2 lần) nếu sai số,
  còn sai thì vẫn xuất tài liệu kèm cảnh báo trong `RunReport` thay vì âm thầm bỏ qua.
- **Không được** in đáp án Đúng/Sai ngay trong đề Phần II (bug đã sửa — bản
  trước 7/2026 từng in thẳng `(Đ/S: Đ)` cạnh mệnh đề trong đề học sinh). Đáp án
  chỉ xuất hiện ở mục "ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI CHI TIẾT" cuối file.
- Phần II in bốn nhận định `a)`–`d)` thành các đoạn văn liên tiếp như ảnh mẫu;
  **không** dựng bảng, không có cột/ô `Đúng`–`Sai`. Phần III không in hộp hay
  dòng "Đáp số của học sinh".
- Bảng trắc nghiệm ABCD tự chọn bố cục 4/2/1 cột theo độ dài phương án dài
  nhất (< 18 ký tự / < 38 ký tự / còn lại), không có hàng tiêu đề hoặc đường viền.
- **Nhóm câu dùng chung dữ kiện**: `Part1Question.shared_context` /
  `Part3Question.shared_context` — các câu liên tiếp có cùng giá trị này được
  gộp thành 1 khối "*Nội dung câu X và Y: ...*" in đúng 1 lần trước nhóm câu,
  khớp mẫu thật ("Sử dụng thông tin sau cho Câu 3 và Câu 4..."). Xử lý ở
  `stages._emit_questions_with_shared_context`; để trống (`None`) nếu câu
  không thuộc nhóm nào.
- **Khối hằng số dùng chung**: `HomeworkContent.shared_constants` (tuỳ chọn) →
  in thành dòng "+ Cho biết: ..." ngay dưới thông tin thí sinh, trước Phần I.
- **Ảnh minh họa**: phần thân câu hỏi được dựng bằng parser riêng
  (`homework_exporter._render_student_body`), không qua
  `gems.docx_export.markdown_ir`/`renderer` dùng chung, nhưng vẫn nhận diện
  cùng 1 pattern ảnh `ready/.../*.png|jpg|jpeg` (dùng `_extract_image`) và chèn
  qua `embed_image()`. **Chỉ đặt ảnh trên 1 dòng độc lập** (ví dụ trong
  `shared_context` của `Part1Question`/`Part3Question`) — **không** đặt ảnh xen
  giữa câu dẫn Phần I và các phương án A-D, hoặc giữa câu dẫn Phần II và các
  mệnh đề a-d, vì 2 vòng lặp dựng phương án/mệnh đề dừng ngay khi gặp dòng
  không khớp định dạng (kể cả đường dẫn ảnh), làm hỏng bảng/danh sách đó.
  Phần đáp án cuối file vẫn dùng chung `parse_markdown_blocks`/`render_blocks`
  nên nhận ảnh bình thường ở bất kỳ vị trí nào.
- **Header đơn giản (không đóng giả đề thi)**: `styles.add_title()` in tiêu đề bài (lấy từ
  heading `#` đầu file Markdown) + 2 dòng "Họ và tên học sinh: ..." / "Lớp: ... Ngày: ..."
  — cùng style với PHT/KHBD. Không còn Sở GD&ĐT/Trường THPT/"(Đề có N trang)"/Mã đề
  thi/Số báo danh/dòng "Thời gian làm bài". Khối "+ Cho biết: ..." / "+ Không làm
  tròn kết quả các phép tính trung gian." (nếu có hằng số dùng chung) vẫn giữ
  nguyên ngay dưới header — đây là nội dung hữu ích, không phải phần đóng vai đề thi.
- **Chân trang phần đề**: sau câu cuối Phần III, trước khi ngắt trang sang đáp
  án, in "----- HẾT -----" (không còn 2 dòng "Thí sinh không được sử dụng tài
  liệu/Giám thị không giải thích gì thêm" — ngôn ngữ đóng vai coi thi, không
  hợp bài tập về nhà) — vẫn tách biệt rõ ràng phần "đề" và phần "đáp án" phía sau.
- Footer từng trang dùng chung `styles.add_page_number_footer()`: căn giữa
  "Trang {PAGE}/{NUMPAGES}" — giống hệt PHT/KHBD, không còn kèm mã đề.

## 7. Định dạng chữ chạy (`gems.docx_export.run_formatter.add_formatted_runs`)

Nhận diện đồng thời trong MỌI nơi ghi văn bản (thân bài, tiêu đề, VÀ ô bảng —
không còn bản sao yếu hơn thiếu tính năng bên trong hàm dựng bảng như trước):
- `**đậm**`, `*nghiêng*`
- `$công thức latex$` → luôn nghiêng, chạy qua `clean_latex()`
- `==highlight==` → tô vàng (`WD_COLOR_INDEX.YELLOW`) — trước đây `==` chỉ bị
  xoá không tô màu gì, giờ hiển thị đúng như prompt NotebookLM đã yêu cầu.

`clean_latex()` (`gems/docx_export/latex_clean.py`) dịch Hy Lạp
(Δ,δ,ω,Ω,φ,π,α,β,γ,λ,μ,θ,ρ,τ), toán tử (≈,≠,≤,≥,×,·,±), `\circ`→°, `\to`→→,
`\infty`→∞, luỹ thừa `^{...}`/`^X` → ký tự Unicode luỹ thừa, `\text{...}` → bỏ
lệnh giữ nội dung, dấu `*` giữa số/chữ → `×`/`·`. Không tự thêm bullet Unicode,
không chèn `\n` thô trong 1 run (trừ vài khối tiêu đề/chữ ký cố định, nơi
python-docx tự tách `\n` thành `<w:br/>` — không phải lỗi hiển thị).

## 8. Trang & Footer

- Khổ A4 (21×29.7cm) cho mọi loại tài liệu.
- Footer PHT/KHBD/Bài tập về nhà dùng chung `styles.add_page_number_footer()`,
  căn giữa: "Trang {PAGE}/{NUMPAGES}". Từ v9.4.0, bài tập về nhà không còn
  footer đề thi căn phải kèm mã đề (xem mục 6). Các số trang là field code
  Word thật.

## 9. Kiểm định chất lượng (`gems/qa/`)

- `markdown_lint.py`: quét regex thuần trên Markdown (bullet thô, LaTeX chưa
  dịch, thiếu từ khoá CV5512 bắt buộc trong giáo án) — dùng trong vòng tự sửa
  lỗi (`gems/generation/self_correction.py`).
- `docx_lint.py`: kiểm tra file `.docx` đã biên dịch (lề trang đối chiếu
  `layout.py`, font đồng nhất Times New Roman, đủ 3 mục lớn I/II/III của KHBD,
  có bảng GV/HS, có mục Điều chỉnh + chữ ký 3 bên) — chạy qua `python -m gems lint`.

## 10. NotebookLM (`gems/notebooklm/`)

Từ 2026-07-08 (skill v9.5.0): sinh **2 bộ Slide tách biệt** — Slide Giáo viên (màu sắc, tách Nhiệm
vụ/Đáp án cho mọi nhiệm vụ, mục lục, slide phân đoạn mỗi mục lớn, cỡ chữ cố định 32/28pt) và Slide
Phiếu học tập (nền trắng/ảnh trắng-đen-xám, không slide đáp án nào, cỡ chữ cố định 24/20pt) — thay
hoàn toàn cơ chế "1 Slide + N+2 Infographic" trước đây. Xem toàn bộ chuẩn ở
`skills/gems_physics_skill.md` mục 4.2.

- `gems/notebooklm/prompt_builder.py`: đọc `{slug}_worksheet_data.json` (ghi bởi
  `gems.generation.stages.write_worksheet_json`, cùng cách làm với `lesson_matrix.json`) qua
  Pydantic — KHÔNG regex-parse lại `{slug}_phieu_hoc_tap.md` như bản cũ (cách cũ từng có bug thật
  không bị phát hiện do thiếu test coverage). Dựng danh sách slide dạng "SLIDE N: ..." đánh số tường
  minh (kỹ thuật giảm rủi ro AI tự gộp/bỏ sót slide, đúc kết từ đợt Bài 28). `generate_notebooklm_
  prompt()` trả về `(teacher_prompt_path, student_prompt_path, teacher_slide_count,
  student_slide_count)`.
- `gems/notebooklm/pipeline.py`: `create_artifacts()` gọi `create_slides()` đúng 2 lần; tải về
  `{slug}_slide_giao_vien.pptx` / `{slug}_slide_phieu_hoc_tap.pptx`. Sau khi tải, **tự đếm số slide
  thật bằng `python-pptx`** và so với số slide kỳ vọng — nếu lệch (dấu hiệu NotebookLM cắt ngang
  giữa chừng), ghi cảnh báo `slide_count_mismatch:X/Y` vào `RunReport` thay vì báo "downloaded" như
  đã xong đầy đủ (không tin số "Trang X/Y" tự ghi trên slide).
- 1 lệnh duy nhất `python -m gems notebooklm --lesson bai4` chạy hết: tạo 2 prompt → đăng nhập →
  tìm/tạo notebook → upload nguồn (dedup) → tạo 2 yêu cầu sinh Slide → poll trạng thái → tải về
  `ready/`.
- Poll kiểm tra trạng thái NGAY LẦN ĐẦU, chỉ chờ 5 phút giữa các lần tiếp theo
  (không còn chờ 5 phút trước khi kiểm tra lần đầu). Tối đa 1 giờ.
- Trạng thái `failed/error/cancelled` được ghi nhận là lỗi thật trong
  `RunReport`, không còn bị coi như "đã xong".
- Hỗ trợ `--profile <tên>` xoay tài khoản né rate-limit — truyền thẳng vào mọi
  lệnh `nlm` qua `gems/notebooklm/nlm_cli.py`. Kỹ thuật vận hành đáng tin cậy khác (rate limit theo
  giờ, cách phục hồi khi bị cắt ngang bằng sinh bổ sung + ghép `python-pptx`) xem
  `docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md` mục Giai đoạn 5.
