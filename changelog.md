# Changelog

All notable changes to this project will be documented in this file.

## [2026-07-08] — Migrate code `gems/notebooklm/` sang chuẩn "2 bộ Slide" (thực thi skill v9.5.0)

### Added
- `gems/models/worksheet.py::PracticeItem`: thêm trường bắt buộc `instructions` (Hình thức/Thời
  gian/Tài liệu) — trước đây mục "2. Luyện tập" là loại nhiệm vụ DUY NHẤT thiếu trường này, khiến
  Slide không thể gắn nhãn 3 ý theo đúng yêu cầu skill 4.2 ("MỌI nhiệm vụ, không ngoại lệ"). Cập nhật
  tương ứng `gems/prompts/worksheet.py` (system prompt Gemini) và `gems/offline/fixtures.py`.
- `gems/generation/stages.py`: `write_worksheet_markdown` giờ in thêm dòng "Hướng dẫn thực hiện" cho
  từng bài toán mục 2 (trước đây chỉ có ở mục 1 và 3). Thêm hàm mới `write_worksheet_json` — ghi
  `{slug}_worksheet_data.json` (cùng cách làm với `write_lesson_matrix_json` đã có), là nguồn dữ liệu
  CHÍNH cho `gems/notebooklm/prompt_builder.py` đọc — thay vì regex-parse lại Markdown đã render
  (cách cũ từng có bug thật không bị phát hiện do thiếu test coverage: `_NHIEM_VU_RE` không khớp bất
  kỳ nhiệm vụ nào suốt nhiều đợt). Gọi hàm này ở cả 3 đường `generate`/`offline`/`compose`
  (`gems/pipeline/orchestrator.py`).
- `gems/notebooklm/prompt_builder.py`: viết lại hoàn toàn — sinh **2 bộ Slide tách biệt** (Slide
  Giáo viên + Slide Phiếu học tập) thay "1 Slide + N+2 Infographic". Danh sách slide dựng động từ
  `LessonWorksheet` (đọc qua `load_worksheet_data`) dạng "SLIDE N: ..." đánh số tường minh — kỹ thuật
  đã kiểm chứng thực tế qua 7 vòng thử ở đợt soạn Bài 28 (Vật Lý 10, one-off), giảm mạnh rủi ro AI tự
  gộp/bỏ sót slide. Áp dụng đầy đủ chuẩn skill 4.2: tách Nhiệm vụ/Đáp án luôn luôn (mọi mục, không
  ngoại lệ), master slide dùng chung, cỡ chữ cố định theo vai trò (32/28pt Giáo viên, 24/20pt Phiếu
  học tập), số trang mọi slide kể cả bìa, mục lục + slide phân đoạn (Giáo viên), cấm tiếng Anh/dấu
  ngoặc vuông placeholder, chống lộ đáp án qua chú thích ảnh. `generate_notebooklm_prompt()` đổi chữ
  ký trả về `(teacher_prompt_path, student_prompt_path, teacher_slide_count, student_slide_count)`.
- `gems/notebooklm/pipeline.py`: `create_artifacts`/`poll_and_download` viết lại cho 2 slide deck
  thay 1 slide + N infographic. Thêm cơ chế chống cắt ngang (silent truncation) đúc kết từ Bài 28: sau
  khi tải về, tự đếm số slide THẬT bằng `python-pptx` và so với số kỳ vọng — nếu lệch, ghi trạng thái
  `slide_count_mismatch:X/Y` vào `RunReport` (không tin số "Trang X/Y" tự ghi trên slide).
- Thêm `python-pptx>=1.0.0` vào `requirements.txt`/`pyproject.toml` (dùng để đếm slide).
- `gems/cli.py`: cập nhật help text lệnh `notebooklm`.
- `tests/test_notebooklm_pipeline.py`: viết lại toàn bộ theo API mới; thêm test phát hiện lệch số
  slide. `tests/test_prompt_builder.py` (mới): test `load_worksheet_data`, tách Nhiệm vụ/Đáp án bên
  Giáo viên, không có slide đáp án nào bên Phiếu học tập, số SLIDE khớp giữa outline và số đếm được.
  109 test — xanh 100%.
- `.agents/agents.md` (mục 10) và `docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md` (Giai đoạn 5):
  gỡ ghi chú "CHƯA MIGRATE" đã thêm ở đợt trước, cập nhật mô tả đúng theo code mới.

### Removed
- Không còn dùng: `prompt_builder._build_infographic_prompt`, `_build_section_infographic_prompt`,
  `_build_slide_prompt`, `parse_pht_for_prompt` (regex parser cũ) — thay bằng
  `_build_teacher_slide_prompt`/`_build_student_slide_prompt`/`load_worksheet_data`. `nlm_cli.
  create_infographic`/`download_infographic` vẫn giữ nguyên trong `nlm_cli.py` (không xoá, chỉ không
  còn được gọi từ `pipeline.py`).

### Ngoài phạm vi đợt này
- Chưa chạy lại `python -m gems notebooklm --lesson bai7` để tái tạo Slide cho bài flagship theo
  chuẩn mới (tốn quota NotebookLM thật, cần xác nhận riêng). Bài 1-6 không tự động migrate.

## [2026-07-08] — Skill v9.5.0: Chốt chuẩn "2 bộ Slide" thay Infographic (áp dụng toàn hệ thống, CHƯA migrate code)

### Changed
- `skills/gems_physics_skill.md` (9.4.1 → 9.5.0) mục 4.2/4.5: quyết định tổng quát hóa từ đợt thiết
  kế lại Bài 28 - Động lượng (Vật Lý 10, one-off) — thay cơ chế "1 Slide + N+2 Infographic" bằng
  **2 bộ Slide tách biệt qua NotebookLM** cho MỌI bài học tương lai: Slide Giáo viên (màu sắc, tách
  slide Nhiệm vụ/Đáp án riêng cho mọi nhiệm vụ, mục lục, slide phân đoạn mỗi phần lớn, cỡ chữ cố định
  32/28pt) và Slide Phiếu học tập (nền trắng/ảnh trắng-đen-xám, không slide đáp án nào, cỡ chữ cố định
  24/20pt). Cả 2 bộ dùng chung 1 master slide (khuôn mẫu bố cục mỗi loại slide cố định), số trang mọi
  slide, nhãn "Nhiệm vụ [mã]" + 3 ý Hình thức/Thời gian/Tài liệu lấy nguyên văn KHBD. Mục 4.5 (N+2
  Infographic) giữ số mục nhưng nội dung đã gộp vào 4.2, đánh dấu "đã loại bỏ". Cập nhật QA mục 5.2
  (TC-SLD-01..05) và mục 4.6 theo chuẩn mới.
- `.agents/agents.md` và `docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md`: thêm ghi chú **CHƯA
  MIGRATE** ở phần NotebookLM (Giai đoạn 5) — chuẩn mới đã chốt trong skill nhưng
  `gems/notebooklm/prompt_builder.py`/`pipeline.py` vẫn đang chạy theo cơ chế cũ (Slide + Infographic),
  cần 1 đợt nâng cấp code riêng mới thực thi được. Bài 28 hiện dùng script Python thủ công riêng
  (`output/bai28_dong_luong/scripts/build_notebooklm.py`), không qua `gems/notebooklm/`.
- `docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md`: thêm mục "Bài học vận hành NotebookLM đáng tin
  cậy" (rate limit theo giờ, rủi ro cắt ngang khi prompt quá dài + cách ghép slide bổ sung bằng
  `python-pptx`, tránh dấu ngoặc vuông placeholder, dùng danh sách slide đánh số tường minh).
- `docs/reference/yeu_cau_du_an_chi_tiet.md`: cập nhật theo quyết định tổng quát hóa trên (di chuyển
  toàn bộ yêu cầu chi tiết Slide từ mục "riêng Bài 28" sang mục "chung GEMS").

## [2026-07-07] — Skill v9.4.1: Độ dài khoảng trống điền khuyết khớp số từ đáp án (PHT + Infographic)

### Added
- `gems/notebooklm/prompt_builder.py`: thêm hằng số `_BLANK_LENGTH_RULE` — yêu cầu Infographic vẽ
  đường chấm điền khuyết `(1)........` NGAY TRONG DÒNG CHỮ (không tách ô riêng), độ dài đường chấm
  ước lượng theo số từ/ký tự của đáp án cần điền (ký hiệu ngắn ~4-7 dấu chấm, cụm từ dài hơn ~15-20
  dấu chấm) — trước đây chỉ dùng số thứ tự `(1)`/`(2)`/`?` chung chung, không có quy tắc độ dài. Áp
  dụng cho cả prompt infographic theo ĐVKT (`_build_infographic_prompt`) và theo mục Luyện
  tập/Vận dụng (`_build_section_infographic_prompt`).
- `skills/gems_physics_skill.md` (9.4.0 → 9.4.1) mục 4.1: ghi rõ quy tắc trên áp dụng cho cả
  `summary_cloze` (nội dung gốc PHT bản Word, là nguồn Infographic đọc lại) lẫn Infographic.
- Bài 7: sửa lại 2 đoạn `summary_cloze` (ĐVKT 1 + ĐVKT 2) từ toàn bộ chỗ trống dùng đồng loạt 8 dấu
  chấm sang độ dài biến thiên theo đáp án thật (vd. `(1)....` cho kí hiệu `$L$` ngắn, `(4)............`
  cho cụm "nhiệt độ" dài hơn) — xác nhận qua `python -m gems compose --lesson bai7` + đọc lại đoạn
  văn trong PHT đã biên dịch.

## [2026-07-07] — Hoàn thiện "chèn ảnh minh họa vào Bài tập về nhà" (đóng giới hạn đã biết từ đợt v9.4.0)

### Added
- `gems/docx_export/homework_exporter.py::_render_student_body`: thêm hỗ trợ nhúng ảnh thật (trước
  đây đường dẫn `ready/hinh_anh/*.png` hiện ra thành text thô) — nhận thêm tham số `image_dirs`,
  dùng chung `_extract_image`/`embed_image` với pipeline Markdown chung. Chỉ nhận diện ảnh trên dòng
  độc lập (`shared_context` hoặc dòng nội dung ngoài phần dẫn câu I/II) — xem ràng buộc an toàn ghi
  rõ trong docstring và `.agents/agents.md` §6, vì 2 vòng lặp dựng bảng phương án A-D/mệnh đề a-d
  dừng ngay khi gặp dòng không khớp định dạng.
- `export_homework`: bổ sung `image_search_dirs` còn thiếu khi gọi `parse_markdown_blocks` cho phần
  đáp án — ảnh trong phần "ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI CHI TIẾT" trước đây cũng không được nhận diện.
- Bài 7: thêm ảnh `so_do_thi_nghiem_do_L.png` vào `shared_context` của cặp câu Phần III về thí
  nghiệm xác định nhiệt hóa hơi riêng của cồn — xác minh `inline_shapes: 1` trong file đã biên dịch,
  không còn đường dẫn text thô rò rỉ ra tài liệu.
- `.agents/agents.md`: sửa mục 8 (còn ghi sai "bài tập về nhà dùng footer đề thi căn phải kèm mã đề"
  — lỗi tham chiếu chéo lỗi thời, mâu thuẫn với mục 6 đã cập nhật ở đợt trước); bổ sung đoạn mô tả cơ
  chế + ràng buộc nhúng ảnh trong Bài tập về nhà vào mục 6.
- Dọn file thừa: `output/bai7_nhiet_hoa_hoi_rieng/ready/bai7_nhiet_hoa_hoi_rieng_slide.pptx` (bản nháp
  1 slide, đã bị thay thế bởi `..._slide_deck.pptx` sinh từ NotebookLM) và `.inspect.ndjson` đi kèm.

## [2026-07-07] — Skill v9.4.0: Bỏ header giả đề thi ở Bài tập về nhà, PHT bám thẳng tiến trình KHBD, 4 Infographic theo hoạt động dạy học, theme Anthropic + portrait/scientific qua flag gốc `nlm`

### Added
- `gems/docx_export/homework_exporter.py`: bỏ hẳn header/footer đóng giả đề thi tốt nghiệp thật
  (Sở GD&ĐT/Trường THPT/"Đề có N trang"/Mã đề thi/Số báo danh/"Thời gian làm bài"/2 dòng thông báo
  đóng vai coi thi) — thay bằng header đơn giản như PHT/KHBD (`styles.add_title` + Họ tên học
  sinh/Lớp) và footer dùng chung `styles.add_page_number_footer()`. Xoá `_derive_exam_code`/
  `exam_year` (không còn dùng ở đâu). Cấu trúc CÂU HỎI (18 MCQ + 4 Đ/S + 6 TLN, phong cách bám đề
  tốt nghiệp) giữ nguyên — chỉ bỏ phần đóng giả HÌNH THỨC đề thi.
- `gems/models/worksheet.py`: viết lại schema PHT từ khung lồng theo từng ĐVKT
  (`UnitWorksheetContent` với 4 phần Khám phá/Trọng tâm/Vận dụng/Mở rộng lặp lại mỗi đơn vị) sang
  1 trình tự phẳng bám thẳng tiến trình KHBD: `knowledge_formation` (mục "1. Hình thành kiến thức
  mới", mỗi ĐVKT 1 phần tử) → `practice_items` (mục "2. Luyện tập", gộp chung không lặp theo ĐVKT)
  → `application_tasks` + `application_readings` (mục "3. Vận dụng"). Không có mục cho Khởi động.
  Cập nhật theo: `gems/offline/fixtures.py`, `gems/prompts/worksheet.py`,
  `gems/generation/stages.py::write_worksheet_markdown`.
- `gems/generation/stages.py::write_slide_guide_markdown`: outline slide đổi từ trục X.0-X.6 riêng
  theo ĐVKT sang 1 trục X.Y duy nhất lấy X trực tiếp từ số mục PHT (1/2/3) — khớp cấu trúc phẳng
  mới; nhận thêm tham số `worksheet` (đã cập nhật 3 điểm gọi trong `gems/pipeline/orchestrator.py`,
  restructure để `sinh_huong_dan_slide` dùng lại đúng object `worksheet` vừa sinh ở
  `sinh_phieu_hoc_tap` thay vì gọi lại `generate_worksheet_content` một lần nữa).
- `gems/notebooklm/nlm_cli.py::create_infographic`: thêm `--orientation portrait --style scientific`
  — phát hiện quan trọng: `nlm create infographic --help` có flag gốc cho hướng ảnh và phong cách,
  đáng tin cậy hơn nhiều so với chỉ yêu cầu bằng lời văn trong prompt (đã xác nhận: lời văn không đủ,
  ảnh vẫn ra landscape/hoạt hình ở đợt trước dù prompt đã yêu cầu portrait).
- `gems/notebooklm/prompt_builder.py`: thêm `_build_section_infographic_prompt` dùng chung cho 2
  infographic mới (mục Luyện tập, mục Vận dụng — không tự trích xuất chi tiết bằng regex như ĐVKT,
  chỉ trỏ NotebookLM đọc đúng mục tương ứng trong PHT nguồn). `generate_notebooklm_prompt` giờ luôn
  sinh N+2 infographic (N = số ĐVKT) với label ổn định (`dvkt1`, `dvkt2`, `luyen_tap`, `van_dung`)
  thay vì cơ chế 1/ĐVKT cũ. Thay bảng màu/font Primary+Times New Roman bằng bảng màu/font thương
  hiệu Anthropic chính thức (Dark `#141413`/Light `#FAF9F5`, nhấn Orange `#D97757`/Blue `#6A9BCC`/
  Green `#788C5D`, Poppins/Lora) cho CẢ Slide lẫn Infographic — chỉ áp dụng ở đây, không đụng
  `gems/docx_export/palette.py` (PHT/KHBD/Bài tập về nhà bản Word giữ nguyên Primary `#1F4E79`).
- `gems/notebooklm/pipeline.py`: `create_artifacts`/`poll_and_download` đổi từ khoá `int` (số thứ
  tự 1..N) sang khoá `str` (label ổn định) cho `info_artifacts`, để tên file tải về đúng ngữ nghĩa
  (`_infographic_luyen_tap.png` thay vì `_infographic_dvkt3.png` — số 3/4 từng dễ bị hiểu nhầm là
  "ĐVKT 3/4" dù bài chỉ có 2 ĐVKT thật).
- `skills/gems_physics_skill.md` (9.3.0 → 9.4.0) và `.agents/agents.md` §6 cập nhật đầy đủ theo các
  thay đổi trên (mục 4.1/4.2/4.3/4.4/4.5 và bộ 15 tiêu chí QA).
- Bài 7 (Nhiệt hóa hơi riêng) làm lại đầy đủ theo chuẩn mới: PHT còn 3 mục lớn (không còn "Khám
  phá/Trọng tâm/Vận dụng/Mở rộng" lặp theo ĐVKT), Bài tập về nhà bỏ hẳn header giả đề thi, Slide 20
  slide theme Anthropic, 4 Infographic portrait đúng label ngữ nghĩa. Nhân tiện khôi phục nhiệm vụ
  NV5 (Engineering Debugger) — bị rớt mất khi soạn lại worksheet.json ở đợt nâng cấp trước, nay đặt
  đúng vào mục "3. Vận dụng" (đúng vị trí ngữ nghĩa, khớp KHBD).

## [2026-07-07] — Skill v9.3.0: Theme Slide/Infographic, đánh số X.Y đồng bộ PHT-Slide, hướng dẫn thực hiện nhiệm vụ, minh họa khoa học

### Added
- `gems/models/worksheet.py::TaskContent`: trường bắt buộc mới `instructions` (hướng dẫn thực hiện —
  hình thức cá nhân/cặp/nhóm, thời gian, tài liệu dùng); cập nhật `gems/offline/fixtures.py` và
  prompt `gems/prompts/worksheet.py` tương ứng.
- `gems/prompts/lesson_plan.py`: yêu cầu Bước 1 mọi hoạt động nêu đủ 3 ý như PHT; khuyến khích tách
  hoạt động Hình thành kiến thức theo từng ĐVKT khi bài có ≥2 đơn vị, kèm cross-reference "tương
  ứng PHT mục X.Y".
- `gems/generation/stages.py::write_worksheet_markdown`: đổi tiêu đề con mỗi ĐVKT từ `1. Khám phá`
  (lặp lại y hệt mọi đơn vị) sang đánh số phân cấp thật `{i}.1 Khám phá / {i}.2 Trọng tâm / {i}.3
  Vận dụng / {i}.4 Mở rộng`; render dòng "Hướng dẫn thực hiện" dưới mỗi nhiệm vụ khám phá.
- `gems/generation/stages.py::write_slide_guide_markdown`: viết lại hoàn toàn — trước đây là 1
  template tĩnh gần như rỗng (không lặp qua ĐVKT/nhiệm vụ nào); giờ nhận thêm `GEMSArchitect` và
  sinh bảng outline thật `X.0-X.6` mỗi ĐVKT đối chiếu ngược đúng mục PHT `X.Y` + mã nhiệm vụ; khối
  quy tắc thiết kế được viết phong phú hẳn (màu/font/box/ảnh khoa học) — 3 lệnh gọi trong
  `gems/pipeline/orchestrator.py` (`generate`/`offline`/`compose`) cập nhật theo.
- `gems/notebooklm/prompt_builder.py`: viết lại `_build_slide_prompt`/`_build_infographic_prompt`
  với hệ thống thiết kế đầy đủ (màu Primary `#1F4E79`, box bo góc nhẹ không đổ bóng, cấm ảnh hoạt
  hình/3D ảo — ưu tiên sơ đồ line-art khoa học), ràng buộc số mục phải khớp PHT, và bắt buộc hiển
  thị dòng "Hướng dẫn thực hiện". Sửa luôn `_NHIEM_VU_RE` (trước đây không khớp bất kỳ nhiệm vụ
  thật nào do đòi số ngay sau "Nhiệm vụ" thay vì dấu hai chấm — không có test coverage nên chưa ai
  phát hiện).
- `gems/illustrations/` (module mới): `style.py` cung cấp bảng màu/font dùng chung và hàm vẽ
  (`draw_labeled_box`, `draw_arrow_label`, `new_diagram_figure`, `new_graph_figure`) bằng matplotlib
  cho minh họa khoa học vector chính xác — không dùng SVG→PNG (máy thiếu thư viện `cairo` gốc) và
  không có tool text-to-image trong phiên agent. Thêm `matplotlib>=3.8.0` vào
  `requirements.txt`/`pyproject.toml`.
- `skills/gems_physics_skill.md` (9.2.0 → 9.3.0): mục 4.1/4.2/4.3 cập nhật theo các chuẩn trên; mục
  4.6 mới "Minh họa khoa học" — quy tắc chọn vector (matplotlib) vs ảnh AI nền tảng ngoài (người
  dùng tự tạo qua Antigravity khi vector không lột tả được), cấm hoạt hình/phi thực tế ở mọi hình
  thức minh họa.
- Bài 7 (Nhiệt hóa hơi riêng) làm mẫu đầy đủ theo chuẩn mới: 3 ảnh minh họa khoa học (sơ đồ thí
  nghiệm, đồ thị nhiệt độ-thời gian, chu trình điều hòa) nhúng vào PHT (3 ảnh) và KHBD (2 ảnh);
  KHBD tách hoạt động Hình thành kiến thức thành 2 hoạt động theo ĐVKT (HĐ2/HĐ3); Slide (16 slide,
  đúng cấu trúc `X.0-X.6`) và Infographic (2 ảnh, đúng số `X.Y`, hiển thị "Hướng dẫn thực hiện",
  ảnh minh họa dạng kỹ thuật/đường nét — không còn phong cách hoạt hình như bản trước) sinh lại qua
  NotebookLM.

### Known limitation
- `gems/docx_export/homework_exporter.py::_render_student_body` là parser riêng cho định dạng đề
  thi (không dùng `gems.docx_export.markdown_ir`/`renderer` dùng chung), nên **chưa hỗ trợ nhúng
  ảnh** trong phần câu hỏi của Bài tập về nhà — một đường dẫn ảnh chèn vào sẽ hiện ra thành text thô
  thay vì ảnh. Phần đáp án (`answer_lines`) có gọi `parse_markdown_blocks` nhưng thiếu tham số
  `image_search_dirs` nên cũng không resolve được ảnh. Chưa sửa trong đợt này (ngoài phạm vi kế
  hoạch đã duyệt).
  **→ Đã sửa** ở đợt "Hoàn thiện chèn ảnh minh họa vào Bài tập về nhà" (xem mục đầu file).

## [2026-07-07] — Skill v9.2.0: Chuẩn cấu trúc đề thi tốt nghiệp THPT + "luyện đề ngay khi học"

### Added
- `skills/gems_physics_skill.md` (9.1.0 → 9.2.0): đặc tả chi tiết mục 4.4 (Bài tập về nhà) đúc kết
  từ đối chiếu trực tiếp đề thi tốt nghiệp THPT chính thức (mã đề 0227/2025, 0214/2026) — tỉ lệ
  nhận thức 6 Nhận biết + 6 Thông hiểu + 6 Vận dụng ở Phần I, phong cách "1 bối cảnh — chuỗi 4 ý
  liên kết" ở Phần II, "ghép cặp dùng chung dữ kiện + yêu cầu làm tròn theo từng câu" ở Phần III.
  Cập nhật tương ứng 4 tiêu chí QA Bài tập về nhà (mục 5.3) mà không đổi tổng 15 tiêu chí/150 điểm.
- Nguyên tắc "luyện đề ngay khi học": PHT (Vận dụng) và KHBD (hoạt động Luyện tập) nay đều yêu cầu
  ít nhất 1 câu hỏi soạn theo đúng 1 trong 3 dạng của đề thi tốt nghiệp, thay vì chỉ xuất hiện lần
  đầu ở Bài tập về nhà cuối bài.
- Nâng cấp `gems/prompts/homework.py` (trước đây chỉ ~10 dòng, sơ sài hơn hẳn 3 prompt còn lại) để
  thực thi đúng chuẩn trên trong nội dung Gemini sinh ra, không chỉ nằm trên giấy; nâng cấp tương
  ứng `gems/prompts/worksheet.py` (Vận dụng) và `gems/prompts/lesson_plan.py` (Luyện tập).
- Viết lại toàn bộ `docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md` (v1.0 → v2.0): đồng bộ với
  kiến trúc `gems/` v9.0 thật (6 giai đoạn đúng theo `gems/pipeline/orchestrator.py`, lệnh CLI thật,
  đường `compose` không cần API key) — bản v1.0 vẫn tham chiếu `engine/`, Hermes Telegram bot,
  LaTeX/TikZ và bảng màu Navy/Mint đã bị xoá từ 7/2026.

## [2026-07-06] — Kiến trúc v9.0: Viết lại toàn bộ pipeline

### Added
- Lệnh `python -m gems compose` (+ `gems/generation/from_json.py`): dựng
  Markdown + DOCX từ nội dung do chính AI agent đang trò chuyện (Claude chạy
  trong Antigravity IDE) tự soạn bằng suy luận trực tiếp, ghi ra 4 file JSON
  khớp schema Pydantic — không cần `GEMINI_API_KEY`, không gọi API ngoài nào.
  Dùng chung 100% đường ghi Markdown/xuất DOCX với `generate`/`offline`.
- Package `gems/` mới hoàn toàn thay thế 2 pipeline cũ song song không tương
  thích (`engine/gems_agent.py` đang chạy thật vs. `main.py`+`gems_analyzer.py`
  +`worksheet_generator.py`+`homework_generator.py` đã chết, không còn ai import).
- 1 CLI duy nhất `python -m gems <generate|offline|notebooklm|full|lint|list-lessons>`
  thay vì phải nhớ chạy 2 lệnh rời (agent chính + `scratch/generate_notebook_materials.py`).
- `gems/config/curriculum.yaml` + `identity.yaml`: danh mục bài học và tên
  GV/brand/model đọc từ 1 nguồn duy nhất, thay `LESSON_MAP` từng khai trùng ở
  2 file và `default_yccds` hardcode.
- `RunReport`/`StageResult` (`gems/pipeline/report.py`): mỗi bước ghi lại kết
  quả thật (thành công/thất bại/cảnh báo) — không còn in banner "HOÀN THÀNH"
  trong khi có thể đã âm thầm thiếu tài liệu.
- `gems/docx_export/markdown_ir.py` + `renderer.py`: parser Markdown dùng
  chung cho cả 3 loại tài liệu, thay 3 bản copy-paste đã lệch nhau (PHT không
  hỗ trợ bảng pipe-table, KHBD có; heading bị cắt theo offset cố định).
- `==highlight==` giờ tô vàng thật (`WD_COLOR_INDEX.YELLOW`) thay vì chỉ bị xoá.
- `python -m gems offline` — đường kiểm thử/demo không cần API key/mạng đầu
  tiên thực sự chạy được (bản `dry_run.py` cũ đã hỏng cú pháp từ lâu).
- `gems/qa/docx_lint.py`: linter cấu trúc DOCX đối chiếu trực tiếp với
  `layout.py` thay vì hardcode lại số liệu lề/font.
- Bộ test `tests/` (~85 test) cho toàn bộ `gems/`, dùng markdown thật lấy từ
  `output/` làm fixture cho phần parse/export.

### Fixed
- Hợp nhất giai đoạn NotebookLM làm 1 (`gems/notebooklm/pipeline.py`) — trước
  đây agent chính chỉ ghi file prompt rồi dừng, phải chạy thêm 1 script rời
  mới thực sự gọi `nlm create slides/infographic`.
- Sửa bug polling luôn `sleep 5 phút` TRƯỚC khi kiểm tra lần đầu (dù artifact
  có thể đã xong trong vài giây) — giờ kiểm tra ngay, chỉ chờ nếu chưa xong.
- Trạng thái NotebookLM `failed/error/cancelled` trước đây bị coi như "đã
  xong" (chỉ dừng polling, không báo lỗi) — giờ ghi nhận là lỗi thật.
- Thêm timeout cho mọi lệnh gọi `nlm` CLI — phát hiện trực tiếp khi kiểm thử
  rằng lệnh có thể treo vô thời hạn nếu chưa đăng nhập, kéo theo treo cả pipeline.
- Bài tập về nhà Phần II không còn in lộ đáp án Đúng/Sai ngay trong đề học
  sinh (`(Đ/S: Đ)` từng bị ghi thẳng vào câu hỏi) — đáp án chỉ còn ở mục
  hướng dẫn giải cuối file.
- Sửa bug `set_table_width_dxa` tạo 2 phần tử `w:tblW` xung đột (append thêm
  mà không xoá phần tử mặc định của python-docx).
- Sửa bug ký tự `^` còn sót lại trước dấu độ trong `clean_latex` (`25^°C`
  thay vì `25°C`) khi LaTeX gốc viết `^\circ` dạng không có ngoặc nhọn.
- Gộp dữ liệu `output/` từ 3 bản sao đã lệch nhau (bài 2 và bài 5 từng chỉ
  có đủ tài liệu ở 1 trong 3 bản) thành 1 cây thư mục duy nhất, đủ 7 bài.
- Xoá cây thư mục dự án bị nhân đôi hoàn toàn (~280MB tài liệu nguồn trùng
  lặp byte-for-byte) và toàn bộ code chết đã xác nhận hỏng cú pháp
  (`quality_checker.py`, `compile_tikz.py`, `dry_run.py` cũ).
- `requirements.txt` bổ sung `pydantic`, `Pillow`, `requests`, `PyYAML` (đã
  được import nhưng chưa khai) và bỏ `jinja2` (chưa từng được dùng).

### Removed
- `engine/`, `scratch/` (bản cũ ở root và trong wrapper `agent soạn tài
  liệu/`), toàn bộ exporter thế hệ trước (`gems_styles.py`, `pht_exporter.py`,
  `khbd_exporter.py`, `homework_exporter.py`), `gems_orchestrator.py`,
  `image_renderer.py`/`compile_tikz.py` (TikZ/Imagen — không dùng trong
  pipeline thật), các script một-lần trong `scratch/`.
- 5 file skill mô tả quy trình thao tác thủ công nhiều bước (AWF workflow) đã
  được thay bằng code chạy thật trong `gems/` + `.agents/agents.md`.

## [2026-06-30]
### Added
- **Tách biệt Prompt NotebookLM**:
  - Hỗ trợ parser tự động trích xuất ĐVKT và từ khóa gợi ý điền khuyết của Phiếu học tập.
  - Hỗ trợ parser tự động bóc tách các đặc tính thiết kế (giáo viên, phông chữ, trường phái, quy tắc bổ sung) từ Hướng dẫn slide.
  - Tự động sinh ra 2 tệp prompt Slide bài giảng (`_slide_prompt.md`) và Infographic đục lỗ (`_info_prompt.md`) riêng biệt cho mỗi bài học để tăng cường độ chính xác khi tạo học liệu trên NotebookLM.
- **Biên dịch Word DOCX Nâng cao**:
  - Thiết lập lề trang động theo loại tài liệu (pht, khbd, dethi).
  - Tự động giãn dòng 1.3 lines, spacing 6pt before/after, thụt dòng đầu 1cm cho văn bản thường.
  - Bảng biểu tự động chống ngắt đôi dòng (`cantSplit`) và lặp lại header (`tblHeader`).
  - Đề thi tự động chống ngắt trang mồ côi và xếp phương án lựa chọn ABCD vào bảng không viền (1, 2, 4 cột) linh hoạt theo độ dài phương án.

### Fixed
- Sửa lỗi gộp dòng (paragraph folding) đối với câu hỏi trắc nghiệm in đậm và phương án trắc nghiệm.
- Sửa lỗi Regex trượt khớp các câu hỏi trắc nghiệm in đậm.
- Chuẩn hóa khoảng trắng viết chính tả tiếng Việt và khoảng trắng giữa số - đơn vị vật lý.

## [2026-06-28]
### Added
- **Bài 7: Nhiệt hóa hơi riêng**:
  - [x] Phân tích sư phạm & Đặc tả GEMS v8.0.
  - [x] Phiếu học tập Markdown & Word `.docx` tích hợp các hoạt động đục lỗ lý thuyết và phần Mở rộng.
  - [x] Slide bài giảng PowerPoint `.pptx` chuẩn GEMS v8.0 (phân cấp X.Y, tách slide câu hỏi & đáp án).
  - [x] Bộ 2 Infographics hướng dọc (portrait) GEMS v8.0 (Khái niệm & Thực hành).
  - [x] Giáo án giảng dạy chi tiết 2 tiết học.
  - [x] Bài tập về nhà và Đáp án chi tiết dạng LaTeX `.tex`.

### Fixed
- Khôi phục và tái thiết lập tệp mã nguồn cốt lõi `engine/main.py` bị hỏng từ nhật ký lịch sử hội thoại IDE.
- Làm sạch không gian làm việc bằng cách loại bỏ các tập tin chẩn đoán tạm thời.

## [2026-06-25]
### Added
- **Bài 6: Nhiệt nóng chảy riêng**:
  - [x] Phiếu học tập Markdown & Word `.docx` tích hợp các hoạt động đục lỗ lý thuyết và phần Mở rộng.
  - [x] Slide bài giảng PowerPoint `.pptx` chuẩn GEMS v7.2 (phân cấp X.Y, tách slide câu hỏi & đáp án).
  - [x] Bộ 2 Infographics hướng dọc (portrait) GEMS v7.3 (Khái niệm & Thực hành).
  - [x] Giáo án giảng dạy chi tiết 2 tiết học.
  - [x] Bài tập về nhà và Đáp án chi tiết dạng LaTeX `.tex`.
  - [x] Script tự động hóa pipeline NotebookLM: `scratch/rebuild_bai6_complete.py`.

### Changed
- **Bài 4: Nhiệt dung riêng**:
  - Cập nhật quy chuẩn GEMS v7.3: bổ sung phần Mở rộng kiến thức thực tế (Két nước làm mát và vật liệu PCM trữ nhiệt) vào Phiếu học tập, Slide và Giáo án.
  - Biên dịch lại Phiếu học tập Word `.docx` tương thích 100%.

### Fixed
- Khắc phục lỗi thiếu trình biên dịch LaTeX bằng cách lưu mã nguồn `.tex` nguyên bản vào thư mục `ready/` của Bài 6.
- Khắc phục lỗi mã hóa ký tự Unicode trên Windows CLI bằng cách cấu hình UTF-8 mặc định trong các script pipeline.
