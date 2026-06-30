---
tags: [GEMS, training, workflow, SOP, team]
---

# 📋 QUY TRÌNH TẠO TÀI LIỆU DẠY HỌC CHI TIẾT
> Phiên bản: 1.0 | Dành cho giáo viên hướng dẫn
> Hệ thống: GEMS v8.0 | Chương trình: GDPT 2018 - Vật lý 12 KNTT

---

## MỤC LỤC
1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Quy trình 6 bước chi tiết](#2-quy-trình-6-bước-chi-tiết)
3. [Cấu trúc đầu ra cho mỗi bài học](#3-cấu-trúc-đầu-ra-cho-mỗi-bài-học)
4. [Mẫu Prompt cho từng bước](#4-mẫu-prompt-cho-từng-bước)
5. [Tiêu chí kiểm định chất lượng (15 QA)](#5-tiêu-chí-kiểm-định-chất-lượng-15-qa)
6. [Công cụ & Tài nguyên](#6-công-cụ--tài-nguyên)
7. [Checklist xuất bản](#7-checklist-xuất-bản)

---

## 1. TỔNG QUAN HỆ THỐNG

### 1.1 Mục tiêu & Vai trò các tài liệu
Tạo **bộ tài liệu dạy học hoàn chỉnh và đồng bộ** cho mỗi bài học Vật lý 12 GDPT 2018. Mối quan hệ và định vị vai trò của các tài liệu được quy định nghiêm ngặt như sau:
*   **Kế hoạch bài dạy (Giáo án / Lesson Plan):** Là tài liệu **chuẩn cốt lõi (Source of Truth)** làm gốc cho toàn bộ hệ thống. Tất cả các phần trong Phiếu học tập và Slide bài giảng bắt buộc phải bám sát theo các hoạt động và tiến trình trong Kế hoạch bài dạy.
*   **Slide bài giảng (Slide Deck):** Thiết kế bám sát từng bước trong Kế hoạch bài dạy, đóng vai trò là công cụ trực quan để **Giáo viên** sử dụng dẫn dắt, điều khiển và hướng dẫn học sinh học tập trên lớp.
*   **Phiếu học tập (Student Worksheet):** Thiết kế bám sát nội dung nhiệm vụ trong Kế hoạch bài dạy, đóng vai trò là công cụ tự học để **Học sinh** sử dụng tự tìm hiểu, thảo luận và thực hiện nhiệm vụ học tập nhằm đạt mục tiêu.
*   **Infographic:** Phiên bản trực quan hóa của Phiếu học tập (đục lỗ trống) phục vụ cho học sinh thực hành điền khuyết trên lớp.
*   **Bài tập về nhà & Đáp án chi tiết (Homework & Answer Key):** Hệ thống câu hỏi củng cố biên dịch qua LaTeX.

### 1.2 Công nghệ sử dụng
| Công cụ | Dùng cho | Yêu cầu |
|---------|----------|---------|
| **Hermes Agent** | Chạy pipeline tạo nội dung | Đã cài sẵn |
| **GEMS Engine (Python)** | Tự động hóa các bước | `GEMINI_API_KEY` |
| **Groq API** | STT voice note + Chat | `GROQ_API_KEY` |
| **Google Flow** | Tạo ảnh/video minh họa | 8 Google Pro accounts |
| **Edge TTS** | Voiceover cho video | Free, không cần key |
| **NotebookLM (nlm CLI)** | Tạo Slide PPTX + Infographic | Google account |
| **python-docx** | Xuất file .docx | Python 3.11 |
| **xelatex** | Biên dịch LaTeX → PDF | MiKTeX / TeX Live |

### 1.3 Thư mục dự án
```
C:\Users\Admin\.antigravity-ide\soạn tài liệu\
├── engine/                    # Python scripts
│   ├── main.py               # Orchestrator chính
│   ├── gems_analyzer.py      # Phân tích sư phạm
│   ├── worksheet_generator.py# Sinh PHT
│   ├── homework_generator.py # Sinh bài tập
│   ├── image_renderer.py     # Vẽ ảnh
│   ├── quality_checker.py    # QA
│   └── export_docx.py        # Markdown→docx
├── tai-lieu-goc/              # SGK, YCCĐ, chương trình
├── output/hermes/             # Đầu ra
│   └── [baiX_slug]/          
│       ├── md/               # File markdown nguồn
│       ├── notebooklm/       # Dữ liệu NotebookLM
│       ├── assets/           # Ảnh minh họa
│       └── ready/            # File sẵn sàng (docx, tex, pdf)
└── .brain/                   # Obsidian vault kiến thức
```

---

## 2. QUY TRÌNH 6 BƯỚC CHI TIẾT

### ⚠️ QUY TẮC VÀNG: DỪNG sau mỗi bước — chờ phê duyệt

---

### BƯỚC 1: PHÂN TÍCH SƯ PHẠM

**Mục tiêu:** Trích xuất YCCĐ, xác định kiến thức cốt lõi, quan niệm sai lầm.

**Input:** 
- SGK Vật lý 12 KNTT (file DOCX từ `tai-lieu-goc/`)
- Khung chương trình GDPT 2018 môn Vật lý
- Công văn hướng dẫn của Bộ GD&ĐT

**Các bước thực hiện:**

1a. Đọc YCCĐ từ tài liệu nguồn (mỗi bài có 2-4 YCCĐ)
1b. Xác định Đơn vị Kiến thức (ĐVKT) — mỗi bài 2-3 ĐVKT
1c. Xác định:
   - Kiến thức cốt lõi (core knowledge)
   - Quan niệm sai lầm phổ biến của học sinh
   - Hiện tượng thực tế có thể liên hệ
1d. Đề xuất kỹ thuật dạy học tích cực: KWL, Think-Pair-Share, Station Learning

**Đầu ra:** `[slug]_dac_ta_gems.md`

**Ví dụ đã làm:** Bài 4 — Nhiệt dung riêng
- 4 YCCĐ: định nghĩa, hệ thức, thực hành, vận dụng
- 2 ĐVKT: Khái niệm nhiệt dung riêng, Thực hành đo nhiệt dung riêng
- Sai lầm: nhầm nhiệt dung riêng với nhiệt dung, quên đơn vị

---

### BƯỚC 2: MA TRẬN NỘI DUNG

**Mục tiêu:** Xây dựng ma trận chi tiết ĐVKT → Nhiệm vụ → Bài tập.

**Cấu trúc ma trận:**
```
| ĐVKT | Nội dung cốt lõi | Hiện tượng thực tế | Nhiệm vụ PHT | Homework |
|------|-------------------|--------------------|--------------|----------|
```

**Homework format (Bộ GD&ĐT 2025 - BẮT BUỘC):**
- **Phần I:** 18 câu trắc nghiệm (6 Nhận biết + 6 Thông hiểu + 6 Vận dụng)
- **Phần II:** 4 câu Đúng/Sai (mỗi câu 4 ý a,b,c,d)
- **Phần III:** 6 câu trả lời ngắn (tính toán ra kết quả)

**Đầu ra:** File ma trận (tích hợp trong `dac_ta_gems.md`)

---

### BƯỚC 3: PHIẾU HỌC TẬP (PHT)

**Mục tiêu:** Tạo PHT chất lượng cao, in được, đúng chuẩn GEMS.

**Cấu trúc mỗi ĐVKT (4 phần bắt buộc):**

| Phần | Nội dung | Loại nhiệm vụ gợi ý |
|------|----------|--------------------|
| 1. **Khám phá** | Tình huống có vấn đề, kích thích tò mò | Assertion Reasoning, Contextual MCQ, Meme Analyzer |
| 2. **Trọng tâm** | Định nghĩa, công thức, kiến thức cốt lõi | Visual Cloze Test, Bug Buster |
| 3. **Vận dụng** | Bài tập áp dụng, tình huống mới | Matching Matrix, Engineering Debugger |
| 4. **Mở rộng** | Ứng dụng thực tế, STEM, có trích nguồn | Infographic Decryption, Model Builder |

**12 loại nhiệm vụ (chọn 1-2/ĐVKT):**
1. ✅ Matching Matrix — Ghép nối đa biến
2. ✅ Algorithmic Ordering — Sắp xếp tiến trình
3. ✅ Bug Buster — Tìm và sửa lỗi vật lý
4. ✅ Assertion Reasoning — Đúng/Sai có biện giải
5. ✅ Contextual MCQ — Trắc nghiệm bối cảnh
6. ✅ Visual Cloze Test — Điền khuyết trực quan
7. ✅ Meme Analyzer — Giải mã Meme vật lý
8. ✅ Engineering Debugger — Gỡ lỗi thiết kế
9. ✅ Fact Check Influencer — Bóc phốt TikTok/Shorts
10. ✅ Decision Tree — Bản đồ lựa chọn sinh tử
11. ✅ Infographic Decryption — Khai thác Infographic
12. ✅ Model Builder — Xây dựng mô hình

**Design System (áp dụng cho docx):**
- Font: Times New Roman (body 11pt, header 14-18pt)
- Màu: Navy #1E3A5F (header), Dark #212121 (body)
- Dòng kẻ chấm: `[DOT_LINE_90]` (90 ký tự)
- White space: 35-40% trang
- Căn lề: 2cm các cạnh
- Header PHT: Tên bài + Họ tên + Lớp + Ngày

**Đầu ra:** 
- `[slug]_phieu_hoc_tap.md` (bản markdown thuần)
- `[slug]_phieu_hoc_tap.docx` (bản Word in được — **ƯU TIÊN**)

---

### BƯỚC 4: HƯỚNG DẪN SLIDE & TÍCH HỢP NOTEBOOKLM
**Mục tiêu:** Tạo tệp tin `[slug]_huong_dan_slide.md` đồng bộ 1:1 với Phiếu học tập và chuẩn bị Prompt tự động hóa tích hợp trên Google NotebookLM để tạo slide PPTX và ảnh Infographic.

**Cấu trúc mỗi ĐVKT (7 slide bắt buộc):**

| Slide | Nội dung | Ghi chú |
|:-----:|----------|---------|
| **X.0** | Đề mục ĐVKT | Mã phân cấp X.Y |
| **X.1** | Nhiệm vụ Khám phá | Slide RIÊNG, không gộp đáp án |
| **X.2** | Đáp án Khám phá | Slide TIẾP THEO |
| **X.3** | Kiến thức Trọng tâm | Highlight vàng #FFD600 từ khóa |
| **X.4** | Thử thách Vận dụng | Tình huống mới, khác PHT |
| **X.5** | Đáp án Vận dụng | Lời giải chi tiết |
| **X.6** | Mở rộng Kiến thức | Ứng dụng STEM, trích nguồn |

**Slide bổ sung:**
- **Slide mở đầu:** Tên bài + "Giáo viên: Kha Khung Hiệp"
- **Slide kết bài:** Mindmap tổng hợp toàn bài

**Quy trình tự động hóa tích hợp NotebookLM:**
1. **Sinh File Prompt trung tâm:** Hệ thống tự động tạo tệp `output/hermes/[slug_bai]/notebooklm/[slug]_notebooklm_prompt.md` chứa cấu trúc bài học, nội dung slide guide và các chỉ dẫn thiết kế infographic đục lỗ.
2. **Nạp nguồn vào NotebookLM:** Tải tệp tài liệu đặc tả GEMS và giáo án đã duyệt lên Google NotebookLM làm tài liệu nguồn (sources).
3. **Thực thi sinh Slide & Infographic:** **Bắt buộc sao chép toàn bộ nội dung của tệp `[slug]_notebooklm_prompt.md` và nhập trực tiếp lên Google NotebookLM**. Prompt này hướng dẫn chi tiết cách tạo nội dung slide và infographic đồng bộ 1-1 với cấu trúc nhiệm vụ của `phieu_hoc_tap.docx` và `ke_hoach_bai_day.docx`.
4. **Đồng bộ Theme và Thiết kế (Theme & Design Sync):** Các tệp Slide PPTX và Infographic tải xuống phải tuân thủ đồng bộ bảng màu và phong cách thiết kế GEMS v8.0:
   - Sử dụng gam màu Navy `#1E3A5F` làm màu chủ đạo cho tiêu đề, khung viền chính.
   - Sử dụng gam màu Mint `#E8F5E9` cho các nền vùng phụ trợ, hộp ghi nhớ.
   - Đồng nhất sử dụng font chữ Times New Roman xuyên suốt.
5. **Xuất bản & Tải về:** Xuất slide thành tệp PowerPoint (`[slug]_slide_deck.pptx` hoặc `.pdf`) và tải các hình ảnh infographic đục lỗ về, lưu trực tiếp vào thư mục `output/hermes/[slug_bai]/ready/` của bài học.

**Quy tắc thiết kế slide (7 rules):**
1. Phân cấp tiêu đề X.Y (1.0, 1.1, 2.0, 2.1...)
2. Tách nhiệm vụ & đáp án — TUYỆT ĐỐI KHÔNG gộp chung
3. Đồng bộ tiêu đề PHT-Slide (khớp 1-1)
4. Mở rộng kiến thức sau Vận dụng (có trích nguồn uy tín)
5. 100% tiếng Việt
6. Highlight vàng #FFD600 cho từ khóa, định nghĩa, công thức
7. Tối đa 6-8 dòng chữ/slide, nền sáng

**Đầu ra:** 
*   `[slug]_huong_dan_slide.md`
*   `notebooklm/[slug]_notebooklm_prompt.md`
*   Slide và Infographic tải về lưu trong thư mục `ready/` của bài học.

---

### BƯỚC 5: BÀI TẬP VỀ NHÀ (LaTeX/TikZ)

**Mục tiêu:** Tạo homework + đáp án dạng LaTeX biên dịch được.

**Cấu trúc:**

**Phần I — Trắc nghiệm (18 câu):**
- 6 câu Nhận biết: định nghĩa, đơn vị, công thức
- 6 câu Thông hiểu: quy trình thí nghiệm, hiện tượng
- 6 câu Vận dụng: tính toán đơn giản

**Phần II — Đúng/Sai (4 câu × 4 ý):**
- Mỗi câu phải có ít nhất 1 ý sai
- Yêu cầu giải thích cho ý sai

**Phần III — Trả lời ngắn (6 câu):**
- Tính toán ra kết quả cụ thể
- Cung cấp hằng số vật lý nếu cần

**Yêu cầu chất lượng:**
- 50% câu hỏi có bối cảnh thực tế từ nguồn quốc tế
- Có citation cụ thể
- Bao gồm bẫy sai lầm từ Bước 1
- TikZ chính xác vật lý

**Kỹ thuật LaTeX:**
- Dùng XeLaTeX (fontspec), KHÔNG dùng inputenc
- Packages: `pgfplots`, `tikz`, `amsmath`, `amssymb`, `vietnam`
- Nhãn 100% tiếng Việt
- File riêng: `[slug]_bai_tap_ve_nha.tex` + `[slug]_dap_an.tex`

---

### BƯỚC 6: KIỂM ĐỊNH CHẤT LƯỢNG (QA)

**Mục tiêu:** Đánh giá 15 tiêu chí, đạt ≥ 135/150 mới xuất bản.

**15 tiêu chí QA:**

**PHT (60 điểm):**
| Mã | Tiêu chí | Điểm |
|:--:|----------|:----:|
| TC-PHT-01 | 35-40% white space, bố cục gọn | 10 |
| TC-PHT-02 | Ảnh khoa học thực tế (không cartoon) | 10 |
| TC-PHT-03 | Tiến trình 4 bước (KP→TT→VD→MR) | 10 |
| TC-PHT-04 | 100% tiếng Việt | 10 |
| TC-PHT-05 | Dòng kẻ chấm đủ độ dài | 10 |
| TC-PHT-06 | Đủ nhiệm vụ, đa dạng loại, logic | 10 |

**Slide (50 điểm):**
| Mã | Tiêu chí | Điểm |
|:--:|----------|:----:|
| TC-SLD-01 | Đồng bộ 1:1 với PHT | 10 |
| TC-SLD-02 | Ảnh thực tế trên mọi slide | 10 |
| TC-SLD-03 | Font UVN bai sau, highlight vàng | 10 |
| TC-SLD-04 | Đủ 7 slide/ĐVKT + mở đầu + kết bài | 10 |
| TC-SLD-05 | 100% tiếng Việt | 10 |

**Homework (40 điểm):**
| Mã | Tiêu chí | Điểm |
|:--:|----------|:----:|
| TC-HW-01 | Bẫy sai lầm, bối cảnh chi tiết | 10 |
| TC-HW-02 | 50% câu hỏi thực tế từ nguồn QT | 10 |
| TC-HW-03 | Đúng số lượng (18 MCQ + 4 T/F + 6 SA) | 10 |
| TC-HW-04 | LaTeX sạch, TikZ chính xác | 10 |

**Thang điểm:**
| Mức | Điểm | Hành động |
|:---:|:----:|-----------|
| ✅ **Đạt** | ≥ 135 | Chuyển sang `ready/` |
| ⚠️ **Có điều kiện** | 120-134 | Sửa P1 rồi chuyển |
| ❌ **Không đạt** | < 120 | Block, về `failed/` |

---

## 3. CẤU TRÚC ĐẦU RA CHO MỖI BÀI HỌC

```
output/hermes/[slug_bai]/
├── md/
│   ├── [slug]_dac_ta_gems.md           # Bước 1+2: Phân tích + Ma trận
│   ├── [slug]_phieu_hoc_tap.md          # Bước 3: PHT bản thô
│   ├── [slug]_dap_an.md                 # Đáp án PHT
│   ├── [slug]_ke_hoach_bai_day.md       # Kế hoạch bài giảng
│   ├── [slug]_huong_dan_slide.md        # Bước 4: Slide guide
│   ├── [slug]_bai_tap_ve_nha.md         # Bước 5: Homework bản thô
├── notebooklm/
│   └── [slug]_notebooklm_prompt.md      # Prompt cho NotebookLM
├── assets/images/                       # Ảnh minh họa
└── ready/
    ├── [slug]_phieu_hoc_tap.docx        # PHT Word (in được)
    ├── [slug]_slide_deck.pptx/.pdf      # Slide PowerPoint/PDF
    ├── [slug]_infographic_*.png         # Infographic
    ├── [slug]_bai_tap_ve_nha.tex        # Homework LaTeX
    └── [slug]_dap_an.tex               # Đáp án LaTeX
```

**Cách đặt tên slug:**

| Bài | Slug |
|:---:|------|
| Bài 4 — Nhiệt dung riêng | `bai4_nhiet_dung_rieng` |
| Bài 5 — Nhiệt độ nhiệt kế | `bai5_nhiet_do_nhiet_ke` |
| Bài 6 — Nhiệt nóng chảy riêng | `bai6_nhiet_nong_chay_rieng` |
| Bài 7 — Nhiệt hóa hơi riêng | `bai7_nhiet_hoa_hoi_rieng` |

---

## 4. MẪU PROMPT CHO TỪNG BƯỚC

### Bước 1+2: Phân tích & Ma trận
```
Bạn là chuyên gia sư phạm Vật lý GDPT 2018. Hãy phân tích bài học sau:

[PASTE YCCĐ + nội dung SGK]

Yêu cầu:
1. Xác định YCCĐ (2-4 mục tiêu)
2. Chia ĐVKT (2-3 đơn vị)
3. Mỗi ĐVKT: xác định nội dung cốt lõi, hiện tượng thực tế, sai lầm phổ biến
4. Đề xuất loại nhiệm vụ cho PHT (chọn từ 12 loại)
5. Lên cấu trúc homework: 18 MCQ + 4 T/F + 6 short answer

Đầu ra: File markdown có cấu trúc [slug]_dac_ta_gems.md
```

### Bước 3: Phiếu học tập
```
Dựa vào ma trận sau, hãy tạo Phiếu học tập:

[PASTE MA TRẬN]

Yêu cầu:
- Mỗi ĐVKT: 4 phần (Khám phá, Trọng tâm, Vận dụng, Mở rộng)
- Chọn 1 loại nhiệm vụ phù hợp cho mỗi phần
- 100% tiếng Việt, giọng giáo viên tự nhiên
- Dòng kẻ chấm [DOT_LINE_90] cho chỗ điền
- Header: Họ tên + Lớp + Ngày

Đầu ra: [slug]_phieu_hoc_tap.md
```

### Bước 4: Slide guide
```
Dựa vào PHT sau, tạo hướng dẫn slide:

[PASTE PHT]

Yêu cầu:
- Mỗi ĐVKT: 7 slide (đề mục, nhiệm vụ, đáp án, trọng tâm, vận dụng, đáp án VD, mở rộng)
- Mở đầu: tên bài + "Giáo viên: Kha Khung Hiệp"
- Kết bài: mindmap
- 7 rules thiết kế (phân cấp X.Y, tách NV/ĐA, đồng bộ PHT, 100% TV, highlight vàng...)

Đầu ra: [slug]_huong_dan_slide.md
```

### Bước 5: Homework LaTeX
```
Dựa vào ma trận, tạo bài tập về nhà LaTeX:

[PASTE MA TRẬN]

Yêu cầu:
- Phần I: 18 MCQ (6 NB + 6 TH + 6 VD)
- Phần II: 4 câu Đ/S (mỗi câu 4 ý)
- Phần III: 6 câu trả lời ngắn
- 50% bối cảnh thực tế
- Dùng XeLaTeX (fontspec), KHÔNG inputenc
- TikZ chính xác, nhãn tiếng Việt
- File riêng: homework.tex + answers.tex
```

---

## 5. TIÊU CHÍ KIỂM ĐỊNH CHẤT LƯỢNG

### Cross-file Validation (KIỂM TRA CHÉO GIỮA CÁC FILE)

- [ ] **Số lượng NV đồng nhất**: "Nhiệm vụ X" trong `dac_ta_gems` = PHT = Slide
- [ ] **Thứ tự NV giống nhau**: Trình tự đánh số nhất quán
- [ ] **Tên NV khớp nhau**: Matching Matrix = Matching Matrix (không lệch)
- [ ] **ĐVKT giống nhau**: Cùng số lượng, cùng tên
- [ ] **Homework đủ số lượng**: 18 MCQ + 4 T/F + 6 SA

### Placeholder Detection

- [ ] Không còn `(.*Các câu hỏi.*)` trong homework
- [ ] Không còn `(.*TODO.*)` trong bất kỳ file nào
- [ ] `[DOT_LINE_90]` đã được thay thế đúng

---

## 6. CÔNG CỤ & TÀI NGUYÊN

### Hermes Agent
```bash
# Load skill GEMS
/skill gems-physics-v8

# Xem hướng dẫn
/skill ai-media-suite

# Tạo ảnh minh họa
/skill image-gen-flow
```

### Google Flow — Tạo ảnh/video
```bash
cd ~/.hermes/google-flow/toolflow && npm start
# Mở http://localhost:3737
```

### Edge TTS — Voiceover
```python
# Tạo file audio giọng Việt
edge-tts --text "Nội dung" --voice vi-VN-HoaiMyNeural --write-media output.mp3
```

### Groq STT — Voice note
```bash
# Voice → text bằng Groq Whisper
# (tích hợp sẵn trong Hermes Telegram)
```

---

## 7. CHECKLIST XUẤT BẢN

### Trước khi xuất bản (Pre-flight)
- [ ] Đọc YCCĐ từ SGK gốc
- [ ] Chia ĐVKT hợp lý
- [ ] PHT: đúng 4 phần/ĐVKT
- [ ] Slide: đúng 7 slide/ĐVKT
- [ ] Homework: đúng format 2025
- [ ] QA Score ≥ 135/150
- [ ] Đồng bộ tiêu đề cross-file
- [ ] 100% tiếng Việt
- [ ] LaTeX compile được
- [ ] .docx in được, font đẹp

### Sau khi xuất bản (Post-flight)
- [ ] Upload lên website dongbayai.vn
- [ ] Copy vào Obsidian vault (.brain/)
- [ ] Ghi nhận vào learning journal
- [ ] Announce trên Telegram group

---

*Tài liệu này được cập nhật từ phiên bản GEMS v8.0 — dựa trên dữ liệu thực tế từ quá trình soạn Bài 4 (Nhiệt dung riêng) và Bài 5 (Nhiệt độ nhiệt kế).*
*Cập nhật lần cuối: 24/06/2026*

### Sau khi xuất bản (Post-flight)
- [ ] Upload lên website dongbayai.vn
- [ ] Copy vào Obsidian vault (.brain/)
- [ ] Ghi nhận vào learning journal
- [ ] Announce trên Telegram group

---

*Tài liệu này được cập nhật từ phiên bản GEMS v8.0 — dựa trên dữ liệu thực tế từ quá trình soạn Bài 4 (Nhiệt dung riêng) và Bài 5 (Nhiệt độ nhiệt kế).*
*Cập nhật lần cuối: 24/06/2026*