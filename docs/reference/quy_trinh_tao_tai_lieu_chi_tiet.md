---
tags: [GEMS, training, workflow, SOP, team]
---

# 📋 QUY TRÌNH TẠO TÀI LIỆU DẠY HỌC CHI TIẾT
> Phiên bản: 2.0 | Dành cho giáo viên hướng dẫn
> Hệ thống: package `gems/` kiến trúc v9.0 (viết lại toàn bộ 7/2026) | Chương trình: GDPT 2018 - Vật lý 12 KNTT
>
> Tài liệu này mô tả đúng quy trình mà code trong `gems/` đang chạy — không phải một bản mô tả lý
> tưởng tách rời thực tế. Số liệu định dạng (lề/font/màu) KHÔNG lặp lại ở đây, xem
> [`.agents/agents.md`](../../.agents/agents.md). Chuẩn NỘI DUNG (nguyên tắc sư phạm, 12 loại
> nhiệm vụ, chuẩn cấu trúc đề thi tốt nghiệp, 15 tiêu chí QA) KHÔNG lặp lại ở đây, xem
> [`skills/gems_physics_skill.md`](../../skills/gems_physics_skill.md) — tài liệu này chỉ nói
> **thứ tự vận hành, lệnh CLI và vai trò từng giai đoạn**, để tránh 3 nguồn lệch nhau theo thời
> gian (bài học từng xảy ra: bản v1.0 tham chiếu `engine/`, Hermes Telegram bot, LaTeX/TikZ và bảng
> màu Navy/Mint — tất cả đã bị thay thế hoàn toàn bởi package `gems/` từ 7/2026, xem `changelog.md`).

---

## MỤC LỤC
1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Quy trình 6 giai đoạn của GEMSPipeline](#2-quy-trình-6-giai-đoạn-của-gemspipeline)
3. [Nguyên tắc "luyện đề ngay khi học"](#3-nguyên-tắc-luyện-đề-ngay-khi-học)
4. [Cấu trúc đầu ra cho mỗi bài học](#4-cấu-trúc-đầu-ra-cho-mỗi-bài-học)
5. [2 cách vận hành: generate (Gemini API) vs. compose (AI agent tự soạn)](#5-2-cách-vận-hành-generate-gemini-api-vs-compose-ai-agent-tự-soạn)
6. [Kiểm định chất lượng (QA)](#6-kiểm-định-chất-lượng-qa)
7. [Công cụ & tài nguyên](#7-công-cụ--tài-nguyên)
8. [Checklist xuất bản](#8-checklist-xuất-bản)

---

## 1. TỔNG QUAN HỆ THỐNG

### 1.1 Mục tiêu & Vai trò các tài liệu
Tạo **bộ tài liệu dạy học hoàn chỉnh và đồng bộ** cho mỗi bài học Vật lý 12 GDPT 2018, từ 1 ma
trận sư phạm duy nhất. Vai trò từng tài liệu:
*   **Kế hoạch bài dạy (KHBD):** Chuẩn Phụ lục IV — Công văn 5512/BGDĐT-GDTrH, là tài liệu **cốt
    lõi (Source of Truth)** cho toàn bộ tiến trình dạy — học. Bước 1 (Chuyển giao) của KHBD PHẢI nêu
    đúng 3 ý (hình thức/thời gian/tài liệu) khớp với `instructions` của nhiệm vụ tương ứng trong PHT
    (xem skill mục 4.3) — 2 bộ Slide đọc trực tiếp `instructions` này từ PHT (qua
    `worksheet_data.json`), không tự parse lại KHBD.
*   **Phiếu học tập (PHT):** Công cụ tự học cho **Học sinh**, bám sát nhiệm vụ trong KHBD; đồng thời
    là nguồn dữ liệu cấu trúc chính (`worksheet_data.json`) mà 2 bộ Slide đọc trực tiếp.
*   **Slide Giáo viên:** Công cụ trực quan cho **Giáo viên** dẫn dắt cả lớp, sinh qua NotebookLM —
    màu sắc/đồ họa đẹp, có đầy đủ đáp án, tách slide Nhiệm vụ/Đáp án riêng biệt cho mọi nhiệm vụ.
*   **Slide Phiếu học tập:** Bản chiếu số hóa của PHT giấy cho **Học sinh**, sinh qua NotebookLM cùng
    notebook với Slide Giáo viên — nền trắng/ảnh trắng-đen-xám, có khoảng trống viết trực tiếp,
    **không có slide đáp án nào**. Thay thế hoàn toàn cơ chế Infographic cũ (xem Giai đoạn 5).
*   **Bài tập về nhà & Đáp án:** Hệ thống câu hỏi củng cố, bám sát cấu trúc VÀ phong cách đề thi
    tốt nghiệp THPT thật (không chỉ đúng số lượng câu — xem mục 3 và
    [skill mục 4.4](../../skills/gems_physics_skill.md)).

### 1.2 Công nghệ sử dụng
| Công cụ | Dùng cho | Yêu cầu |
|---------|----------|---------|
| **Package `gems/` (Python)** | Toàn bộ pipeline: sinh nội dung, xuất DOCX, QA lint | Python 3.11, `pip install -e .` |
| **Gemini API** | Sinh nội dung có cấu trúc (đường `generate`) | `GEMINI_API_KEY` trong `.env` |
| **AI agent trò chuyện (Claude/Antigravity)** | Tự soạn nội dung trực tiếp, không cần API key (đường `compose`) | Không cần key |
| **python-docx** | Xuất PHT/KHBD/Bài tập về nhà thành `.docx` in được | Có sẵn trong `requirements.txt` |
| **NotebookLM (`nlm` CLI)** | Sinh Slide PPTX + Infographic đục lỗ | Tài khoản Google, `nlm login` trước |
| **pytest** | Kiểm thử `gems/` (~85 test, fixture markdown thật) | `pip install -e ".[dev]"` |

> Đã loại bỏ khỏi kiến trúc hiện tại (không còn dùng, chỉ còn dấu vết trong `.brain/` lịch sử):
> Hermes Telegram bot, Groq STT, Google Flow, Edge TTS, biên dịch LaTeX/TikZ cho bài tập về nhà
> (Bài tập về nhà giờ xuất `.docx` giống PHT/KHBD, qua `gems/docx_export/homework_exporter.py`).

### 1.3 Thư mục dự án (đúng theo `readme.md`)
```
soạn tài liệu/
├── gems/                    # TOÀN BỘ logic thật
│   ├── cli.py / __main__.py    # python -m gems <lệnh> --lesson baiN
│   ├── config/                 # curriculum.yaml + identity.yaml
│   ├── models/                  # Pydantic schema (architect, worksheet, homework, lesson_plan)
│   ├── prompts/                  # Prompt hệ thống gửi Gemini (build_prompt mỗi giai đoạn)
│   ├── generation/                # Gọi Gemini + ghi Markdown + tự sửa lỗi
│   ├── docx_export/                # Markdown -> DOCX (layout/palette/3 exporter)
│   ├── qa/                          # Lint Markdown + lint DOCX
│   ├── notebooklm/                  # nlm CLI wrapper + pipeline Slide/Infographic
│   ├── pipeline/                     # RunReport + GEMSPipeline (orchestrator.py — 1 nguồn duy nhất)
│   └── offline/                       # Fixture mẫu — chạy thử không cần API/mạng
├── tai-lieu-goc/            # YCCĐ, SGK, mẫu KHBD/đề thi tốt nghiệp thật (`tai-lieu-goc/mẫu/`)
├── output/<slug>/           # md/ (nguồn) + ready/ (.docx) + notebooklm/ + authored/ (đường compose)
├── skills/                  # gems_physics_skill.md (chuẩn NỘI DUNG) + docx_skill.md (kỹ thuật)
├── .agents/agents.md        # Chuẩn ĐỊNH DẠNG chính thức — nguồn thật duy nhất
└── tests/                   # pytest cho toàn bộ gems/
```

---

## 2. QUY TRÌNH 6 GIAI ĐOẠN CỦA GEMSPipeline

Đúng theo `gems/pipeline/orchestrator.py::GEMSPipeline.generate()` — mỗi giai đoạn ghi kết quả
thật (thành công/thất bại/cảnh báo) vào `RunReport`, không có banner "HOÀN THÀNH" giả khi thiếu
tài liệu. Lỗi ở Giai đoạn 1 chặn toàn bộ pipeline; lỗi ở các giai đoạn sau chỉ ghi nhận, không
chặn các nhánh độc lập còn lại.

### GIAI ĐOẠN 1 — `phan_tich_yccd`: Phân tích sư phạm + Ma trận (1 lệnh gọi Gemini duy nhất)

**Hàm:** `gems.generation.stages.analyze_yccd` → trả về 1 đối tượng `GEMSArchitect` gồm **cả 2**
phần `analysis` (phân tích sư phạm) và `matrix` (ma trận ĐVKT/nhiệm vụ) — đây KHÔNG phải 2 bước
tuần tự tách rời như bản tài liệu trước, mà là 1 lệnh gọi cấu trúc (`gems/models/architect.py`).

**Input:** YCCĐ từ `tai-lieu-goc/` (file thật hoặc `yccd_fallback` trong `curriculum.yaml`).

**Nội dung `analysis` (`PedagogicalAnalysis`):**
- `key_concepts`: kiến thức cốt lõi của bài học.
- `misconceptions`: danh sách quan niệm sai lầm phổ biến — **đây là nguồn bẫy sai lầm duy nhất**
  được tái sử dụng xuyên suốt Phần I (phương án nhiễu), Phần II (ý sai) của Bài tập về nhà.
- `teaching_methods`: phương pháp giảng dạy đề xuất.

**Nội dung `matrix` (`LessonMatrix`):** 2-3 `KnowledgeUnit` (ĐVKT), mỗi ĐVKT có chuỗi `TaskItem`
(nhiệm vụ) gồm mã, loại (1 trong 12 loại GEMS), tên, mô tả và bối cảnh thực tế.

**Đầu ra:** `[slug]_dac_ta_gems.md` + `lesson_matrix.json` trong `output/<slug>/md/`.

---

### GIAI ĐOẠN 2 — Sinh nội dung 4 nhánh song song, cùng đọc 1 `matrix_json`

Mỗi nhánh độc lập (lỗi 1 nhánh không chặn nhánh khác), đều dùng `identity.gemini_model_content`:

| Giai đoạn | Hàm sinh | Prompt (`gems/prompts/`) | Schema |
|---|---|---|---|
| `sinh_phieu_hoc_tap` | `generate_worksheet_content` | `worksheet.py` | `LessonWorksheet` |
| `sinh_ke_hoach_bai_day` | `generate_lesson_plan_content` | `lesson_plan.py` | `LessonPlanContent` |
| `sinh_huong_dan_slide` | `write_slide_guide_markdown` | (dựng trực tiếp từ `matrix`, không gọi Gemini riêng) | — |
| `sinh_bai_tap_ve_nha` | `generate_homework_content` | `homework.py` | `HomeworkContent` |

**Ràng buộc số lượng Bài tập về nhà:** đúng 18 câu Phần I + 4 câu Phần II + 6 câu Phần III.
KHÔNG ép bằng Pydantic validator (sẽ làm hỏng cả response nếu model lệch 1 câu, không có đường
sửa) — `generate_homework_content` tự kiểm tra `question_counts` sau khi sinh, retry tối đa 2 lần
kèm nhắc lại yêu cầu, còn sai thì vẫn ghi file kèm cảnh báo trong `RunReport` thay vì âm thầm bỏ
qua hoặc chặn toàn bộ pipeline.

**Chuẩn nội dung/phong cách từng nhánh:** xem
[`skills/gems_physics_skill.md` mục 4](../../skills/gems_physics_skill.md) — đặc biệt mục 4.4 có
đặc tả chi tiết cấu trúc nhận thức Phần I (6 Nhận biết + 6 Thông hiểu + 6 Vận dụng), phong cách
"1 bối cảnh — chuỗi 4 ý liên kết" của Phần II, và "ghép cặp dùng chung dữ kiện" của Phần III, đúc
kết từ đối chiếu trực tiếp đề thi tốt nghiệp THPT thật (mã đề 0227/2025, 0214/2026).

**PHT là 1 trình tự phẳng 3 mục** (1. Hình thành kiến thức mới — mỗi ĐVKT 1 mục con, 2. Luyện tập,
3. Vận dụng; không có mục cho Khởi động) bám thẳng tiến trình KHBD, thay cho khung riêng của GEMS
lặp lại 4 phần/ĐVKT ở bản trước v9.4.0 — xem skill mục 4.1. Mỗi nhiệm vụ bắt buộc có dòng "Hướng dẫn
thực hiện" (hình thức/thời gian/tài liệu). `write_slide_guide_markdown` tự sinh bảng outline X.Y
lấy X từ đúng số mục PHT (`1.i.y`/`2.y`/`3.y`) — không cần tự tay đồng bộ.

**Minh họa khoa học** (sơ đồ thí nghiệm, đồ thị, sơ đồ nguyên lý...) vẽ bằng matplotlib qua
`gems/illustrations/style.py` (không dùng SVG→PNG vì máy thiếu thư viện `cairo` gốc), lưu vào
`output/<slug>/ready/hinh_anh/` rồi tham chiếu bằng dòng text chứa tên file — xem quy tắc chọn
vector vs ảnh AI ở [skill mục 4.6](../../skills/gems_physics_skill.md).

**Đầu ra:** `[slug]_phieu_hoc_tap.md`, `[slug]_ke_hoach_bai_day.md`, `[slug]_huong_dan_slide.md`,
`[slug]_bai_tap_ve_nha.md` trong `output/<slug>/md/`.

---

### GIAI ĐOẠN 3 — `bien_dich_docx:*`: Biên dịch Markdown → DOCX

**Hàm:** `GEMSPipeline._compile_docx` — quét mọi file `.md` trong `md_dir`, khớp theo tên file với
1 trong 3 exporter (`export_pht`, `export_khbd`, `export_homework` — `gems/docx_export/`). File
`huong_dan_slide.md` KHÔNG được biên dịch DOCX (chỉ dùng làm nguồn cho prompt NotebookLM ở Giai
đoạn 5). Lỗi biên dịch 1 file được ghi nhận riêng, không chặn các file khác.

**Đầu ra:** `[slug]_phieu_hoc_tap.docx`, `[slug]_ke_hoach_bai_day.docx`,
`[slug]_bai_tap_ve_nha.docx` trong `output/<slug>/ready/`.

---

### GIAI ĐOẠN 4 — `tu_sua_loi:*`: Tự sửa lỗi Markdown (CHỈ áp dụng cho đường `generate`)

**Hàm:** `GEMSPipeline._self_correct` → `gems/generation/self_correction.py::correct_markdown_file`.
Chạy lint quy tắc (`gems/qa/markdown_lint.py`) trên từng file Markdown (trừ `dac_ta_gems`/`matrix`),
nếu phát hiện lỗi thì gọi lại Gemini để tự sửa, rồi biên dịch lại DOCX cho file vừa sửa.

> Lưu ý: giai đoạn này **không chạy** ở đường `offline` (dữ liệu mẫu, không gọi API) và **không
> chạy** ở đường `compose` (nội dung do AI agent trò chuyện tự soạn — agent tự chịu trách nhiệm
> đối chiếu chuẩn trước khi ghi JSON, xem mục 5).

---

### GIAI ĐOẠN 5 — NotebookLM: 2 bộ Slide (Giáo viên + Phiếu học tập) (lệnh riêng `notebooklm`/`full`)

Từ 2026-07-08 (skill v9.5.0): sinh **2 bộ Slide tách biệt** — Slide Giáo viên (màu sắc, tách Nhiệm
vụ/Đáp án cho MỌI nhiệm vụ không ngoại lệ, mục lục, 1 slide phân đoạn mỗi mục lớn, cỡ chữ cố định
32/28pt) và Slide Phiếu học tập (nền trắng/ảnh trắng-đen-xám, KHÔNG có slide đáp án nào, cỡ chữ cố
định 24/20pt) — thay hoàn toàn cơ chế "1 Slide + N+2 Infographic" trước đây.

**Không nằm trong `generate`/`offline`/`compose`** — chạy riêng bằng
`python -m gems notebooklm --lesson bai4` (hoặc `full` để nối tiếp `generate` + `notebooklm`).
1 lệnh duy nhất: sinh 2 prompt (`gems/notebooklm/prompt_builder.py`, đọc THẲNG
`{slug}_worksheet_data.json` — ghi bởi `gems.generation.stages.write_worksheet_json` cùng lúc với
`{slug}_phieu_hoc_tap.md`, KHÔNG regex-parse Markdown như bản cũ) → đăng nhập (`nlm login --check`)
→ tìm/tạo notebook → upload nguồn (dedup) → tạo 2 yêu cầu sinh Slide (`create_slides` gọi 2 lần) →
poll trạng thái (kiểm tra ngay lần đầu, tối đa 1 giờ, chờ 5 phút giữa các lần tiếp theo) → tải về
`output/<slug>/ready/{slug}_slide_giao_vien.pptx` và `{slug}_slide_phieu_hoc_tap.pptx`. Trạng thái
`failed/error/cancelled` được ghi nhận là lỗi thật, không bị coi là "đã xong".

**Chống cắt ngang (silent truncation):** sau khi tải về mỗi file, `pipeline.py` tự đếm số slide
THẬT bằng `python-pptx` và so với số slide kỳ vọng (tính sẵn lúc dựng prompt) — nếu lệch, ghi cảnh
báo `slide_count_mismatch:X/Y` vào `RunReport` thay vì báo "downloaded" như đã xong đầy đủ (không
tin số "Trang X/Y" tự ghi trên slide — xem bài học chi tiết ngay dưới đây).

Danh sách slide được dựng động từ dữ liệu PHT thật, dạng "SLIDE N: ..." đánh số tường minh (không
phải mô tả outline rời rạc) — kỹ thuật đã kiểm chứng qua 7 vòng thử thực tế ở đợt Bài 28, giảm mạnh
rủi ro AI tự gộp/bỏ sót slide. Bản thiết kế (theme Anthropic, box bo góc nhẹ không đổ bóng, cấm ảnh
hoạt hình, master slide dùng chung 2 bộ...) nằm trong các hằng số quy tắc của
`gems/notebooklm/prompt_builder.py` — khối `## QUY TẮC THIẾT KẾ BẮT BUỘC` trong
`[slug]_huong_dan_slide.md` vẫn được trích thêm quy tắc bổ sung qua `parse_slide_guide_for_prompt`.

### Bài học vận hành NotebookLM đáng tin cậy (đúc kết từ đợt Bài 28 — Động lượng, 7 vòng tạo lại)

`nlm create slides`/`create infographic` là AI sinh nội dung thật, không phải template máy móc — độ
tin cậy giảm rõ rệt khi prompt quá dài/quá nhiều ràng buộc cùng lúc. Áp dụng các quy tắc sau cho MỌI
lần gọi NotebookLM, kể cả trong `gems/notebooklm/` dùng chung:

- **Giới hạn tần suất (rate limit) theo giờ:** gọi `create_slides` quá dồn dập (nhiều vòng tạo lại
  liên tiếp trong vài giờ) sẽ bị chặn `RESOURCE_EXHAUSTED` ("Wait a few minutes before retrying").
  Thực tế đã gặp: chờ 5 phút CHƯA đủ để hồi phục — cần chờ dài hơn hẳn (~25-30 phút) trước khi thử
  lại. Không lặp lại việc thử ngay lập tức nhiều lần liên tiếp khi gặp lỗi này.
- **Rủi ro bị cắt ngang (silent truncation) khi yêu cầu quá nhiều slide/quy tắc cùng lúc:** 1 prompt
  đòi ~27 slide phức tạp (nhiều loại slide khác nhau, nhiều ràng buộc thiết kế) có thể khiến
  NotebookLM dừng sinh giữa chừng (ví dụ chỉ ra 21/27 slide) mà KHÔNG báo lỗi gì — luôn đếm lại số
  slide thực tế trong file `.pptx` tải về, không tin số trang tự ghi trên slide ("Trang X/27" vẫn có
  thể xuất hiện dù chỉ có 21 slide thật). Nếu bị cắt ngang: **không cần tạo lại toàn bộ** — viết 1
  prompt bổ sung CHỈ yêu cầu đúng các slide còn thiếu (đánh số tiếp nối, ví dụ "SLIDE 22...SLIDE 27"),
  gọi `create_slides` lần nữa trong CÙNG notebook, tải về file riêng, rồi ghép nối bằng `python-pptx`:
  mỗi slide NotebookLM xuất ra là **1 ảnh full-bleed duy nhất** (không có text layer thật), nên ghép
  chỉ cần copy đúng ảnh (`shape.image.blob`) + vị trí/kích thước sang cuối presentation gốc — xem ví
  dụ đầy đủ tại `output/bai28_dong_luong/scripts/build_notebooklm_phan4.py`.
- **Tránh dùng ký hiệu ngoặc vuông `[...]` (hay bất kỳ ký hiệu placeholder nào) để đánh dấu "chỗ cần
  điền tên/nội dung thật" trong ví dụ minh hoạ của prompt** — AI có thể chép y nguyên cả dấu ngoặc vào
  slide thật thay vì hiểu đó là chỉ dẫn. Nếu cần đưa ví dụ, viết rõ bằng lời: "đây là ví dụ nội dung
  cần viết, KHÔNG in dấu ngoặc/ký hiệu placeholder nào lên slide". (Ngoại lệ: `[ ? ]` dùng làm ô trống
  điền khuyết THẬT SỰ trên Infographic — đó là nội dung cố ý, không phải placeholder cho AI tự thay.)
- **Dùng danh sách slide đánh số tường minh** ("SLIDE 1: ...", "SLIDE 2: ...", mỗi dòng = đúng 1
  slide) thay vì outline dạng gạch đầu dòng rời rạc — giảm mạnh rủi ro AI tự gộp 2 nội dung vào 1
  slide hoặc bỏ sót slide. Ràng buộc "không gộp" (ví dụ Nhiệm vụ + Đáp án luôn phải tách 2 slide
  riêng) cần nêu kèm ví dụ cụ thể về đúng lỗi đã từng xảy ra, không chỉ nói chung chung.
- **Nhắc lại các yêu cầu dễ bị bỏ sót ở CẢ đầu và cuối prompt**, không chỉ 1 chỗ duy nhất (ví dụ: số
  trang trên mọi slide kể cả slide bìa, cấm tiếng Anh kể cả trong nhãn khung/hộp, cấm đáp án lộ qua
  chú thích ảnh minh họa) — 1 lần nhắc ở giữa 1 prompt dài dễ bị "trôi" khi AI sinh đến các slide sau.
- **Lỗi console cp1252 khi script Python in tiếng Việt ở dòng cuối là lỗi biết trước, không phải lỗi
  thật** — luôn kiểm tra file `.pptx` đã tải về có tồn tại trước khi kết luận thất bại từ exit code.
  Có thể phòng tránh hoàn toàn bằng `sys.stdout.reconfigure(encoding="utf-8")` ở đầu script nếu cần
  đọc log in ra giữa chừng một cách tin cậy (ví dụ để chẩn đoán lỗi thật như rate limit).

---

### GIAI ĐOẠN 6 — `lint`: Kiểm định chất lượng DOCX đã biên dịch

**Lệnh riêng:** `python -m gems lint --lesson bai4` — không sinh lại học liệu, chỉ đọc DOCX có sẵn
trong `ready/`. `gems/qa/docx_lint.py::lint_khbd_docx` kiểm tra đủ 3 mục lớn I/II/III của KHBD, có
bảng tổ chức thực hiện, mục Điều chỉnh + chữ ký 3 bên; `lint_docx_margins` đối chiếu lề trang/font
với `gems/docx_export/layout.py` cho PHT và Bài tập về nhà. Đây là kiểm tra **kỹ thuật/cấu trúc**
(máy đọc được); phần **nội dung/phong cách sư phạm** (15 tiêu chí QA) vẫn cần người soát theo
[skill mục 5](../../skills/gems_physics_skill.md#5-bộ-15-tiêu-chí-qa-self-check).

---

## 3. NGUYÊN TẮC "LUYỆN ĐỀ NGAY KHI HỌC"

Phân tích đề thi tốt nghiệp THPT thật (2025-2026) cho thấy học sinh cần làm quen **cấu trúc và
phong cách ra đề** càng sớm càng tốt, không phải lần đầu tiếp xúc là lúc làm Bài tập về nhà cuối
bài. Từ v2.0, quy trình gắn nguyên tắc này xuyên suốt 3 điểm chạm — cùng 1 chuẩn dùng chung (1
trong 3 dạng: trắc nghiệm 4 phương án A-D / Đúng-Sai 4 ý a-d / trả lời ngắn dạng số có nêu rõ quy
tắc làm tròn):

1. **PHT — phần Vận dụng của mỗi ĐVKT** (`gems/prompts/worksheet.py`): tình huống Vận dụng phải
   diễn đạt bằng đúng 1 trong 3 dạng trên — học sinh gặp "hình dạng" câu hỏi đề thi ngay trong giờ
   học, khi kiến thức còn mới.
2. **KHBD — hoạt động Luyện tập** (`gems/prompts/lesson_plan.py`): câu hỏi luyện tập trên lớp cũng
   soạn theo đúng 1 trong 3 dạng trên, để giáo viên có sẵn ngữ liệu luyện đề ngay tại lớp.
3. **Bài tập về nhà** (`gems/prompts/homework.py`): áp dụng đầy đủ, quy mô lớn (18/4/6 câu) với
   toàn bộ chi tiết cấu trúc nhận thức và phong cách ra đề — xem mục 2, Giai đoạn 2.

Không yêu cầu 3 điểm chạm này trùng lặp nội dung — PHT/KHBD chỉ cần 1 câu mẫu mỗi ĐVKT để làm quen
"hình dạng" đề thi; Bài tập về nhà mới là nơi luyện tập quy mô đầy đủ.

---

## 4. CẤU TRÚC ĐẦU RA CHO MỖI BÀI HỌC

```
output/<slug>/
├── md/
│   ├── <slug>_dac_ta_gems.md            # Giai đoạn 1: Phân tích + Ma trận
│   ├── lesson_matrix.json               # Giai đoạn 1: ma trận thuần JSON (input cho Giai đoạn 2)
│   ├── <slug>_phieu_hoc_tap.md
│   ├── <slug>_ke_hoach_bai_day.md
│   ├── <slug>_huong_dan_slide.md
│   └── <slug>_bai_tap_ve_nha.md
├── notebooklm/
│   └── <slug>_notebooklm_prompt.md      # Giai đoạn 5: prompt gửi lên NotebookLM
├── authored/                            # Chỉ có khi dùng đường compose — 4 file JSON do AI agent soạn
│   ├── <slug>_architect.json
│   ├── <slug>_worksheet.json
│   ├── <slug>_homework.json
│   └── <slug>_lesson_plan.json
├── ready/
│   ├── <slug>_phieu_hoc_tap.docx
│   ├── <slug>_ke_hoach_bai_day.docx
│   ├── <slug>_bai_tap_ve_nha.docx
│   ├── <slug>_slide_deck.pptx / .pdf    # Giai đoạn 5
│   └── <slug>_infographic_*.png         # Giai đoạn 5
└── metadata.json                        # Danh sách file + trạng thái từng giai đoạn (RunReport)
```

Danh mục bài học (khoá `key` → `slug`, `yccd_file`, `num_knowledge_units`) khai ở
`gems/config/curriculum.yaml` — thêm bài mới chỉ cần thêm 1 mục YAML, không sửa code.

---

## 5. 2 CÁCH VẬN HÀNH: `generate` (Gemini API) vs. `compose` (AI agent tự soạn)

### 5.1 `generate` — gọi Gemini API thật
```powershell
python -m gems generate --lesson bai4
python -m gems generate --prompt "soạn bài 4 nhiệt dung riêng"
```
Cần `GEMINI_API_KEY` trong `.env`. Chạy đủ 6 giai đoạn ở mục 2 (trừ Giai đoạn 5, phải gọi
`notebooklm` hoặc `full` riêng).

### 5.2 `compose` — AI agent đang trò chuyện tự soạn nội dung (không cần API key)
Dùng khi chính AI agent (Claude chạy trong Antigravity IDE) đang tự soạn nội dung bằng suy luận
trực tiếp thay vì gọi Gemini. Agent tự viết 4 file JSON khớp đúng schema Pydantic
(`gems/models/*.py`) vào `output/<slug>/authored/`, rồi chạy:
```powershell
python -m gems compose --lesson bai4
```
`compose` dùng lại đúng 100% đường ghi Markdown + xuất DOCX như `generate`/`offline` — chỉ khác
nguồn nội dung. **Không chạy Giai đoạn 4 (tự sửa lỗi)** — agent tự đối chiếu chuẩn ở
`skills/gems_physics_skill.md` trước khi ghi JSON, và nên tự chạy `python -m gems lint --lesson
bai4` sau khi biên dịch để kiểm tra kỹ thuật/cấu trúc.

### 5.3 `offline` — chạy thử bằng dữ liệu mẫu, không cần API/mạng
```powershell
python -m gems offline --lesson bai4
```
Dùng để demo/kiểm thử nhanh toàn bộ đường biên dịch DOCX mà không tốn quota Gemini.

---

## 6. KIỂM ĐỊNH CHẤT LƯỢNG (QA)

- **Kỹ thuật/cấu trúc (máy đọc được):** `python -m gems lint --lesson bai4` — xem Giai đoạn 6.
- **Nội dung/phong cách sư phạm (người soát):** 15 tiêu chí QA, thang điểm 150, ngưỡng đạt ≥135 —
  đặc tả đầy đủ ở [`skills/gems_physics_skill.md` mục 5](../../skills/gems_physics_skill.md).

| Mức | Điểm | Hành động |
|:---:|:----:|-----------|
| ✅ **Đạt** | ≥ 135/150 | Xuất bản, giữ nguyên trong `ready/` |
| ⚠️ **Có điều kiện** | 120-134/150 | Sửa các tiêu chí thấp điểm nhất rồi soát lại |
| ❌ **Không đạt** | < 120/150 | Sinh lại (Giai đoạn 2) trước khi xuất bản |

### Cross-file validation (kiểm tra chéo giữa các file, soát thủ công)
- [ ] Số nhiệm vụ trong `dac_ta_gems.md` khớp 1-1 với PHT và Slide guide (tên + thứ tự).
- [ ] Bài tập về nhà đúng 18/4/6 câu — nếu `RunReport` có cảnh báo số câu lệch, phải sửa tay.
- [ ] Không còn placeholder kiểu "(Các câu hỏi...)", "TODO", `[DOT_LINE_90]` chưa được thay thế.

---

## 7. CÔNG CỤ & TÀI NGUYÊN

```powershell
# Cài đặt (1 lần)
pip install -r requirements.txt        # hoặc: pip install -e .

# Xem danh mục bài học hiện có
python -m gems list-lessons

# Đăng nhập NotebookLM trước khi chạy notebooklm/full lần đầu
nlm login

# Kiểm thử toàn bộ gems/
python -m pytest tests/ -q
```

Tên giáo viên, phông chữ chủ đạo, tên model Gemini và năm thi (`exam_year` — dùng cho tiêu đề Bài
tập về nhà) đọc từ `gems/config/identity.yaml`, sửa 1 chỗ áp dụng toàn hệ thống.

---

## 8. CHECKLIST XUẤT BẢN

### Trước khi xuất bản (Pre-flight)
- [ ] Giai đoạn 1 chạy thành công (`phan_tich_yccd` = `ok: true` trong `metadata.json`)
- [ ] Đủ 4 file Markdown nguồn (PHT, KHBD, Slide guide, Bài tập về nhà)
- [ ] PHT: đúng 4 phần/ĐVKT (Khám phá → Trọng tâm → Vận dụng → Mở rộng); Vận dụng bám 1 trong 3
      dạng câu hỏi đề tốt nghiệp (mục 3)
- [ ] KHBD: đủ 4 hoạt động, hoạt động Luyện tập có câu hỏi đúng dạng đề tốt nghiệp (mục 3)
- [ ] Bài tập về nhà: đúng 18/4/6 câu, đúng tỉ lệ nhận thức 6+6+6 ở Phần I, Phần III ghép cặp dùng
      chung dữ kiện (mục 2, Giai đoạn 2)
- [ ] `python -m gems lint --lesson <slug>` không còn cảnh báo nghiêm trọng
- [ ] QA nội dung ≥ 135/150 (mục 6)
- [ ] Slide + Infographic đã tải về `ready/` (nếu đã chạy Giai đoạn 5)

### Sau khi xuất bản (Post-flight)
- [ ] Cập nhật `metadata.json` phản ánh đúng file cuối cùng trong `ready/`
- [ ] Ghi nhận thay đổi đáng chú ý vào `changelog.md` nếu có sửa quy trình/chuẩn nội dung

---

*Cập nhật lần cuối: 2026-07-08 — bổ sung mục "Bài học vận hành NotebookLM đáng tin cậy" (Giai đoạn 5)
đúc kết từ đợt soạn Bài 28 - Động lượng (7 vòng tạo lại Slide qua NotebookLM). Trước đó: 2026-07-07 —
đồng bộ với kiến trúc `gems/` v9.0 và chuẩn cấu trúc đề thi tốt nghiệp THPT (skill v9.2.0). Bản v1.0
(24/06/2026) đã lỗi thời do tham chiếu kiến trúc `engine/` cũ, xem `changelog.md` mục [2026-07-06] để
biết lý do viết lại toàn bộ pipeline.*
