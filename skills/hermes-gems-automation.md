---
name: hermes-gems
description: |
  Pipeline tự động hóa soạn học liệu Vật lý GEMS v7.1.
  Kích hoạt khi gõ /gems hoặc "soạn bài [tên]", "tạo tài liệu [tên]".
  Sinh toàn bộ: SPEC, Phiếu học tập, Slide guide, Homework, Answers,
  Lesson Plan, QA Report, NotebookLM prompt, ảnh minh họa từ web.
  Lưu vào output/hermes/<bài>/.
version: 7.1.0
requires:
  - gems_physics_skill
  - gems-orchestrator
---

# HERMES GEMS AUTOMATION — SOẠN TÀI LIỆU 1 LỆNH

## Kích hoạt
Gõ: `/gems` hoặc `soạn bài [tên]` hoặc `tạo tài liệu [tên bài]`

## Quy trình tự động 3 bước

### Bước 1: Nhận diện bài học
- Từ input người dùng, match vào LESSON_MAP (7 bài Chương 1 Vật lý 12)
- Tìm file SGK gốc trong `tai-lieu-goc/`
- Xác định YCCĐ từ template có sẵn

### Bước 2: Sinh hàng loạt (tự động, không dừng)
- SPEC: Đặc tả GEMS (analysis + matrix)
- Phiếu học tập (Worksheet): Markdown với placeholder [DOT_LINE_90]
- Hướng dẫn Slide (Slide Guide): 7 slide/ĐVKT, font UVN bai sau, GV Kha Khung Hiệp
- Bài tập về nhà (Homework): 18 MCQ + 4 Đ/S + 6 Trả lời ngắn + Đáp án
- Kế hoạch bài dạy (Lesson Plan)
- NotebookLM prompt cho GV tự tạo slide/infographic (sinh các Infographic dạng dọc theo từng ĐVKT)

### Bước 3: Xử lý hậu kỳ
- Tìm ảnh từ web (web_search → download → lưu assets/)
- Tạo metadata.json
- Tạo QA Report 15 tiêu chí
- Tích hợp và download Slide (.pptx) & các Infographic dọc theo ĐVKT (.png) từ NotebookLM

## Cấu trúc output
```
output/hermes/<slug>/
├── md/
│   ├── <slug>_dac_ta_gems.md
│   ├── <slug>_phieu_hoc_tap.md
│   ├── <slug>_huong_dan_slide.md
│   ├── <slug>_bai_tap_ve_nha.md
│   ├── <slug>_dap_an.md
│   ├── <slug>_ke_hoach_bai_day.md
│   └── <slug>_bao_cao_qa.md
├── assets/
│   ├── image_sources.md (danh sách ảnh cần tải)
│   ├── <lesson_prefix>_infographic_[ten_dvkt_khong_dau]_01.png (các infographic dọc theo ĐVKT)
│   └── *.png / *.jpg (ảnh đã tải từ web)
├── notebooklm/
│   └── <slug>_notebooklm_prompts.md
├── ready/
│   ├── <lesson_prefix>_slide deck_01.pptx
│   └── *.docx (file Word nếu có)
└── metadata.json
```

## Lệnh thường dùng
```bash
# Từ Hermes chat
/gems                               # Chọn bài tương tác
soạn bài Nhiệt dung riêng           # Tự động
soạn bài 7 Nhiệt hóa hơi riêng      # Bài 7
tạo tài liệu Bài 1 - Cấu trúc chất  # Bài 1

# Từ terminal
python engine/gems_orchestrator.py --lesson "Bài 6 - Nhiệt nóng chảy riêng"
python engine/gems_orchestrator.py --list  # Xem danh sách bài

# Tìm ảnh cho bài
cd output/hermes/<slug>/assets/
# Hermes tự động tìm và tải ảnh khi chạy pipeline
```
