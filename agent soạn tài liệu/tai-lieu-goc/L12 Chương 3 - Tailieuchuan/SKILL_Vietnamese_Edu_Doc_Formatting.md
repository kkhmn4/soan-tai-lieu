# SKILL: Vietnamese Educational Document Formatting

## Overview

This skill provides comprehensive formatting rules for creating professional Vietnamese educational documents in Microsoft Word (.docx) format. It covers four primary document types used in Vietnamese schools according to the CTGDPT 2018 curriculum:

1. **Phiếu học tập** (Study worksheets)
2. **Kế hoạch bài dạy** (Lesson plans - per CV 5512/BGDĐT-GDTrH)
3. **Giáo án chi tiết** (Detailed lesson plans)
4. **Đề thi TN THPT** (High school graduation exams - 2025-2026 structure)

All rules are optimized for print, photocopying, and readability in classroom environments.

## Quick Setup

### Required Software
- Microsoft Word 2016+ / WPS Office / LibreOffice Writer
- Vietnamese keyboard (UniKey or similar) with Unicode encoding
- Fonts: Times New Roman (primary), Arial (backup)

### File Naming Convention
```
[Loại_tài_liệu]_[Môn]_[Khối]_[Bài]_[Năm_học].docx
Ví dụ: PhieuHT_VatLi_12_Bai1_DaoDongDieuHoa_2025-2026.docx
       KHBD_VatLi_12_Bai1_2025-2026.docx
       GiaoAn_VatLi_12_Bai1_2025-2026.docx
       DeThi_TNTHPT_VatLi_2025-2026_MaDe01.docx
```

## Task Router

| User Intent | Document Type | Apply Rules From |
|-------------|---------------|------------------|
| Phiếu học tập, worksheet, bài tập nhóm | Phiếu HT | § 5.1 + § 7 |
| Kế hoạch bài dạy, KHBD, giáo án ngắn | KHBD | § 5.2 + § 7 |
| Giáo án chi tiết, giáo án word | Giáo án | § 5.3 + § 7 |
| Đề thi, đề kiểm tra, đề TN THPT | Đề thi | § 5.4 + § 7 |
| Báo cáo, kế hoạch chung | General | § 3 + § 4 + § 7 |

---

## 1. Page Setup (Bắt buộc)

### Paper & Margins

| Document Type | Paper | Orientation | Top | Bottom | Left | Right |
|---------------|-------|-------------|-----|--------|------|-------|
| Phiếu học tập | A4 | Portrait | 2 cm | 2 cm | 2 cm | 2 cm |
| Kế hoạch bài dạy | A4 | Portrait | 2 cm | 2 cm | 3 cm | 2 cm |
| Giáo án chi tiết | A4 | Portrait | 2 cm | 2 cm | 3 cm | 2 cm |
| Đề thi TN THPT | A4 | Portrait | 1,5 cm | 1,5 cm | 2 cm | 2 cm |
| Đề thi chính thức | A3 | Landscape | 1,5 cm | 1,5 cm | 2 cm | 1,5 cm |

### Ghi chú:
- **Lề trái 3 cm** cho KHBD/Giáo án để có chỗ bấm ghim
- Đề thi không dùng seal line (đóng dấu dọc) → lề trái 2 cm
- Đề thi có seal line → lề trái 3,5 cm

---

## 2. Typography (Font System)

### Primary Font Table

| Element | Font | Size | Style | Color |
|---------|------|------|-------|-------|
| School name (header) | Times New Roman | 14pt | Bold | #000000 |
| Document title (main) | Times New Roman | 16pt | Bold | #1F4E79 |
| Section heading (I, II, III) | Times New Roman | 14pt | Bold | #1F4E79 |
| Subsection (1, 2, 3) | Times New Roman | 13pt | Bold | #000000 |
| Sub-subsection (a, b, c) | Times New Roman | 13pt | Normal, italic | #000000 |
| Body text | Times New Roman | 13pt | Normal | #000000 |
| Bullet content | Times New Roman | 13pt | Normal | #000000 |
| Table header | Times New Roman | 12pt | Bold | #000000 |
| Table content | Times New Roman | 12pt | Normal | #000000 |
| Notes / Captions | Times New Roman | 11pt | Italic | #666666 |
| Page number | Times New Roman | 9pt | Normal | #666666 |
| Seal line | Times New Roman | 8pt | Normal | #999999 |
| Answer dots | Times New Roman | 13pt | Normal | #999999 |

### Font Alternatives (when Times New Roman unavailable)
- Body: Tinos, Liberation Serif, DejaVu Serif
- Modern style headers: Arial / Calibri (12pt for body, 14-16pt for headings)

---

## 3. Paragraph Standards

### Spacing Rules

| Setting | Value |
|---------|-------|
| Line spacing | 1.3 lines (hoặc Fixed 22pt) |
| Space before paragraph | 6pt |
| Space after paragraph | 6pt |
| First line indent (body) | 1 cm (≈ 567 twips) |
| First line indent (heading) | 0 cm |
| First line indent (bullet/list) | 0 cm (use left indent instead) |
| Left indent (sub-bullet) | 0.5 cm mỗi cấp |

### Alignment

| Content Type | Alignment |
|--------------|-----------|
| Body paragraph | Justify (căn đều 2 bên) |
| Title | Center |
| Section heading | Left |
| Table header | Center |
| Table content (text) | Left |
| Table content (number) | Right |
| Page number | Center |
| Signature | Right |

### Bullet & Numbering Convention

```
I.  MỤC TIÊU CHUNG              ← 14pt bold, ALL CAPS
    1. Về kiến thức              ← 13pt bold
       a) Năng lực chung         ← 13pt normal italic
          - Nội dung cụ thể 1    ← 13pt normal
          - Nội dung cụ thể 2
       b) Năng lực chuyên biệt
    2. Về kỹ năng
II. NỘI DUNG BÀI HỌC
```

**Cấm kỵ (FORBIDDEN):**
- ❌ Dùng bullet tự động của Word cho số câu hỏi đề thi
- ❌ Trộn lẫn "- " và "•" trong cùng tài liệu
- ❌ Dùng nhiều hơn 4 cấp heading

---

## 4. Heading Hierarchy

### Mandatory Word Heading Styles

Sử dụng **Heading 1, 2, 3** có sẵn trong Word (để có thể tạo Mục lục tự động):

| Level | Style | Format |
|-------|-------|--------|
| Cấp 1 (I, II, III) | Heading 1 | 14pt Bold, color #1F4E79, before: 12pt, after: 6pt |
| Cấp 2 (1, 2, 3) | Heading 2 | 13pt Bold, color #000000, before: 8pt, after: 4pt |
| Cấp 3 (a, b, c) | Heading 3 | 13pt Normal Italic, before: 6pt, after: 3pt |
| Cấp 4 (-, +) | Normal | 13pt Normal with left indent |

### Khi nào dùng Mục lục (TOC)?
- ✅ Tài liệu dài > 5 trang
- ✅ Có ≥ 3 chương mục lớn
- ❌ Phiếu HT, đề thi ngắn, KHBD 1 bài → không cần TOC

---

## 5. Document-Specific Templates

### 5.1 PHIẾU HỌC TẬP (Study Worksheet)

#### Cấu trúc chuẩn:
```
[Tên trường, lớp - nhỏ, 11pt italic]
           PHIẾU HỌC TẬP  (16pt bold, center)
    (Mẫu tham khảo – CTGDPT 2018)  (10pt italic, gray)

┌─────────────────────────────────────────┐
│ Họ và tên: ____  Lớp: ___  Nhóm: ___   │  ← Bảng thông tin
│ Môn học: Vật Lí   Bài: Dao động ĐH     │
│ Tiết: ___  Ngày: __/__/202_            │
└─────────────────────────────────────────┘

I. MỤC TIÊU NHIỆM VỤ
   - Mô tả được dao động điều hoà...
   - Viết được phương trình dao động...

II. NỘI DUNG NHIỆM VỤ
   Nhiệm vụ 1: Quan sát thí nghiệm
   [Bảng ghi số liệu đo được]
   
   Nhiệm vụ 2: Viết phương trình dao động
   Câu hỏi 1: .........
   Trả lời: ...............................
   ...............................
   
   Nhiệm vụ 3: Thảo luận nhóm
   a) .........  b) .........

III. TỰ ĐÁNH GIÁ
┌──────────────────────────┬──────┬────────┐
│ Tiêu chí                 │ Đạt  │ Chưa Đ  │
├──────────────────────────┼──────┼────────┤
│ 1. Mô tả được hiện tượng │  ☐   │   ☐    │
│ 2. Xác định đại lượng    │  ☐   │   ☐    │
└──────────────────────────┴──────┴────────┘

                    Ngày __/__/202_
                    Chữ ký HS: ______
```

#### Quy tắc riêng:
- Kích thước tối đa: **2 trang A4**
- Có 3 nhiệm vụ tối thiểu: quan sát, thực hành, vận dụng
- Phần trả lời: gạch chấm `...........`, line spacing 1.5
- Có bảng tự đánh giá cuối phiếu

---

### 5.2 KẾ HOẠCH BÀI DẠY (Lesson Plan - CV 5512)

#### Cấu trúc chuẩn (theo Công văn 5512/BGDĐT-GDTrH):

```
SỞ GD&ĐT ....................
TRƯỜNG THPT ..................
Tổ: Vật Lí - Công nghệ

         KẾ HOẠCH BÀI DẠY
     (Mẫu theo CV 5512/BGDĐT-GDTrH)

┌──────────────┬──────────┬──────────┬────────┐
│ Tên môn học  │ Vật Lí   │ Lớp      │ 12     │
│ Tên bài học  │ Bài 1... │ Số tiết  │ 02     │
│ Ngày soạn    │ ...      │ Ngày dạy │ ...    │
│ Tên SGK      │ KNTT     │ NXB      │ GDVN   │
└──────────────┴──────────┴──────────┴────────┘

I. MỤC TIÊU
   1. Về kiến thức
   2. Về năng lực
      a) Năng lực chung
      b) Năng lực vật lí
   3. Về phẩm chất

II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
   1. Đối với giáo viên
   2. Đối với học sinh

III. TIẾN TRÌNH DẠY HỌC
   Hoạt động 1: KHỞI ĐỘNG (10')
   - Mục tiêu: ...
   - Phương pháp: ...
   - Nội dung: ...
   - Sản phẩm: ...
   
   Hoạt động 2: HÌNH THÀNH KIẾN THỨC (40')
   ...
   
   Hoạt động 3: LUYỆN TẬP - VẬN DỤNG (25')
   ...
   
   Hoạt động 4: TÌM TÒI - MỞ RỘNG (10')
   ...
   
   Hoạt động 5: CỦNG CỐ - DẶN DÒ (5')

IV. RÚT KINH NGHIỆM
   - Nội dung: .........
   - Phương pháp: .........

┌─────────────┬─────────────────┐
│ Tổ trưởng   │ Hiệu trưởng     │
│ (Kí, họ tên)│ (Kí, đóng dấu)  │
│             │                 │
│ ........... │ ............... │
└─────────────┴─────────────────┘
         Ngày __/__/202_
         Giáo viên soạn
         (Kí, họ tên)
         ...............
```

#### Quy tắc riêng:
- Tổng thời gian các hoạt động = số tiết × 45 phút
- Mỗi hoạt động phải có đủ 4 yếu tố: **Mục tiêu - Phương pháp - Nội dung - Sản phẩm**
- Có chữ kí 3 bên: Tổ trưởng, Hiệu trưởng, GV soạn

---

### 5.3 GIÁO ÁN CHI TIẾT (Detailed Lesson Plan)

#### Cấu trúc với bảng 2 cột:

```
              GIÁO ÁN CHI TIẾT
      Môn: VẬT LÍ 12 - CTGDPT 2018
        Bài 1: DAO ĐỘNG ĐIỀU HOÀ

[Bảng thông tin: Trường/Lớp/Tuần/Tiết/Ngày]

I. MỤC TIÊU BÀI HỌC
   1. Về kiến thức
   2. Về kĩ năng
   3. Về thái độ
   4. Định hướng phát triển năng lực

II. PHƯƠNG PHÁP - PHƯƠNG TIỆN
III. CHUẨN BỊ

IV. TIẾN TRÌNH BÀI HỌC

HOẠT ĐỘNG 1: KHỞI ĐỘNG (5')
┌───────────────────────────┬───────────────────────────┐
│ Hoạt động của GV          │ Hoạt động của HS          │
├───────────────────────────┼───────────────────────────┤
│ - GV yêu cầu HS nhắc...   │ - HS trả lời câu hỏi...   │
│ - GV chiếu hình ảnh...    │ - HS quan sát, thảo luận  │
│ - Đặt câu hỏi: ...        │ - HS phát hiện: ...       │
└───────────────────────────┴───────────────────────────┘

HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (20')
[Bảng 2 cột tương tự]

HOẠT ĐỘNG 3: LUYỆN TẬP - VẬN DỤNG (25')
HOẠT ĐỘNG 4: CỦNG CỐ - DẶN DÒ (10')

V. RÚT KINH NGHIỆM SAU GIẢNG DẠY
   - Ưu điểm: ...
   - Hạn chế: ...
   - Điều chỉnh: ...

                      Ngày __/__/202_
                      Giáo viên soạn
                      (Kí, họ tên)
```

#### Quy tắc riêng:
- Bảng "Hoạt động GV - Hoạt động HS" phải có header tô xám
- Mỗi ô bảng: padding 0,1 cm, font 11pt
- Có ô "Rút kinh nghiệm" để điền sau khi dạy

---

### 5.4 ĐỀ THI TN THPT VẬT LÍ 2025-2026

#### Cấu trúc đề theo quy định mới:

| Phần | Loại câu | Số câu | Điểm/câu | Tổng điểm |
|------|----------|--------|----------|-----------|
| I | Trắc nghiệm nhiều lựa chọn | 18 | 0,25 | 4,5 |
| II | Trắc nghiệm Đúng/Sai (4 ý/câu) | 4 | 0,25 (mỗi ý 0,1) | 1,0 |
| III | Trắc nghiệm trả lời ngắn | 6 | 0,33 | 2,0 |
| | **TỔNG** | **28** | | **7,5** |

**Lưu ý:** Theo cấu trúc mới của Bộ GD&ĐT 2025, đề thi Vật Lí TN THPT có 28 câu hỏi, thời gian 50 phút, điểm tối đa 10 (sẽ quy đổi).

#### Layout đề thi:

```
BỘ GIÁO DỤC VÀ ĐÀO TẠO
ĐỀ THAM KHẢO THI TN THPT 2025-2026
Môn: VẬT LÍ

┌──────────────┬────────┬──────────────┬───────────────┐
│ Mã đề thi    │ ...... │ Thời gian    │ 50 phút       │
└──────────────┴────────┴──────────────┴───────────────┘

Họ và tên TS: .............  SBD: .............

(Đề thi có 04 trang, 28 câu hỏi theo cấu trúc mới)

PHẦN I. CÂU HỎI TRẮC NGHIỆM NHIỀU LỰA CHỌN (18 câu × 0,25đ)
(Thí sinh chọn một phương án đúng nhất)

Câu 1. Dao động điều hoà là dao động trong đó li độ...
A. một hàm số bậc nhất của thời gian.
B. một hàm số bậc hai của thời gian.
C. một hàm cosin (hoặc sin) của thời gian.   ← dùng BẢNG KHÔNG VIỀN 4 cột
D. một hàm mũ của thời gian.

Câu 2. ........................
A. ...   B. ...   C. ...   D. ...

[... tiếp tục đến Câu 18 ...]

PHẦN II. CÂU HỎI TRẮC NGHIỆM ĐÚNG/SAI (4 câu × 0,25đ)
(Thí sinh trả lời Đúng/Sai cho từng ý a, b, c, d)

Câu 19. Một vật dao động điều hoà có phương trình...
Xét tính đúng/sai của các nhận định sau:
┌──────────────────────────────┬─────────┬────────┐
│ a) Biên độ dao động là 8 cm  │  ☐ Đúng │ ☐ Sai  │
│ b) Tần số dao động là 2 Hz   │  ☐ Đúng │ ☐ Sai  │
│ c) ...                       │  ☐ Đúng │ ☐ Sai  │
│ d) ...                       │  ☐ Đúng │ ☐ Sai  │
└──────────────────────────────┴─────────┴────────┘

[... tiếp tục đến Câu 22 ...]

PHẦN III. CÂU HỎI TRẢ LỜI NGẮN (6 câu × 0,33đ)
(Thí sinh điền kết quả vào phiếu trả lời)

Câu 23. Một vật dao động điều hoà... Tính biên độ A.
Câu trả lời: ............................. cm.

Câu 24. ...........................
Câu trả lời: .............................

[... tiếp tục đến Câu 28 ...]
```

#### Quy tắc riêng cho đề thi:
- **KHÔNG dùng bullet tự động** cho số câu → gõ tay "Câu 1.", "Câu 2."...
- **Đáp án ABCD**: dùng **bảng không viền 4 cột** (không dùng dấu cách để căn)
- Câu hỏi dài: dùng 2 cột, 2 dòng (A-B / C-D)
- Seal line (đóng dấu): dòng chấm xám, 8pt
- Số trang: "Trang X/Y" ở footer
- Mỗi câu phải có thuộc tính **keepNext + keepLines** để không ngắt trang giữa câu
- Phần đáp án: trang riêng, có Page Break trước

#### Phân tích cấu trúc đề 2025 (theo Bộ GD&ĐT):

| Mức độ | Tỷ lệ | Đặc điểm |
|--------|-------|----------|
| Biết | ~45% | Khái niệm, định luật cơ bản (Phần I) |
| Hiểu | ~35% | Phân tích, giải thích (Phần I + II) |
| Vận dụng | ~20-25% | Tình huống thực tiễn (Phần III) |

---

## 6. Tables (Quy tắc bảng biểu)

### Table Style Standards

| Setting | Value |
|---------|-------|
| Border | 0.5pt solid black |
| Header background | #D9D9D9 (light gray) |
| Header text | Bold, center, 12pt |
| Cell padding (top/bottom) | 0.1 cm |
| Cell padding (left/right) | 0.15 cm |
| Allow row break across pages | NO (cantSplit) |
| Repeat header on new page | YES (tableHeader) |

### Width Strategy

| Table Type | Width |
|------------|-------|
| Full-width table | 100% page width |
| Info table (4 cells) | Cột nhãn 30% + Cột giá trị 70% |
| 2-column GV/HS table | 50% / 50% |
| Score table (đề thi) | 80% center |
| Answer table (ABCD) | 4 cột đều, không viền |

### Cell Alignment Rules

| Content | Alignment |
|---------|-----------|
| Header text | Center |
| Text content | Left |
| Numbers | Right |
| Single character (Đ/S, ☐) | Center |
| Currency | Right |
| Date | Center |

---

## 7. Header & Footer

### Header Standards

- **Content**: Tên tài liệu (mẫu), môn, khối
- **Format**: 10pt italic, color #666666, center
- **Bottom border**: 0.5pt solid #CCCCCC
- **Different first page**: YES (không có header ở trang bìa)

### Footer Standards

- **Content**: "Trang X / Y" hoặc "Trang X"
- **Format**: 9pt normal, color #666666, center
- **Top border**: optional 0.5pt solid #CCCCCC

### Section Breaks

Sử dụng **Section Break (Next Page)** giữa:
- Trang bìa và nội dung
- Giữa các phần tài liệu khác nhau (KHBD → Giáo án → Đề thi)
- Giữa đề thi và đáp án

---

## 8. Color Palette (Bảng màu chuẩn)

### Primary Palette

```
Nội dung chính:      #000000  (đen)
Tiêu đề:             #1F4E79  (xanh dương đậm - giáo dục)
Tiêu đề phụ:         #2E74B5  (xanh dương vừa)
Header bảng:         #D9D9D9  (xám nhạt)
Đường viền bảng:     #000000  (đen)
Chú thích:           #666666  (xám trung)
Đường gạch đáp án:   #999999  (xám nhạt)
Seal line:           #999999  (xám nhạt)
Đường viền header:   #CCCCCC  (xám rất nhạt)
```

### Tông màu theo môn (tùy chọn)

| Môn | Màu tiêu đề | Hex |
|-----|-------------|-----|
| Vật Lí | Xanh dương | #1F4E79 |
| Toán | Đỏ đậm | #C00000 |
| Ngữ Văn | Nâu đỏ | #8B4513 |
| Hóa Học | Xanh lá | #548235 |
| Sinh Học | Xanh lục đậm | #385723 |
| Lịch Sử | Cam đất | #BF8F00 |
| Địa Lí | Xanh ngọc | #2E8B8B |

---

## 9. Cover Page (Trang bìa)

### Khi nào cần trang bìa?

- ✅ Tài liệu dài ≥ 5 trang
- ✅ Bộ tài liệu tổng hợp (nhiều mẫu)
- ✅ Báo cáo, kế hoạch dài
- ❌ Phiếu HT, đề thi, KHBD 1 bài → KHÔNG cần

### Layout trang bìa chuẩn:

```
[Tên trường - 14pt bold center]
[Tổ bộ môn - 12pt italic center]

              [Tiêu đề chính]
              16pt-20pt bold
              Màu #1F4E79

        [Phụ đề - 14pt bold]

    [Thông tin áp dụng - 12pt italic gray]

         [Năm học - 14pt bold]



   CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
        Độc lập - Tự do - Hạnh phúc
        ........................, ngày ... tháng ... năm 202...
```

---

## 10. Page Break Rules

### Khi nào ngắt trang?

✅ **ĐÚNG**:
- Giữa trang bìa và nội dung
- Giữa TOC và nội dung
- Giữa đề thi và đáp án
- Giữa các phần lớn của bộ tài liệu

❌ **SAI**:
- Ngắt trang giữa câu hỏi và đáp án
- Ngắt trang giữa dòng tiêu đề và nội dung ngay sau
- Ngắt trang sau mỗi câu hỏi (trừ khi cần)
- Tạo 2 Page Break liên tiếp → trang trắng

### Anti-Orphan/Widow Rules

- Heading phải có `keepNext: true` (giữ với đoạn sau)
- Câu hỏi phải có `keepNext: true + keepLines: true`
- Hình vẽ phải đi kèm với câu hỏi (cùng trang)
- Đoạn cuối cùng không bị cô lập (≥ 3 dòng cuối cùng trên trang mới)

---

## 11. Vietnamese Typography Rules

### Dấu câu & Khoảng trắng

| Ký tự | Quy tắc |
|-------|---------|
| Dấu chấm `.` | Cách 1 khoảng trắng sau (không trước) |
| Dấu phẩy `,` | Cách 1 khoảng trắng sau |
| Dấu chấm phẩy `;` | Cách 1 khoảng trắng sau |
| Dấu hai chấm `:` | Cách 1 khoảng trắng sau |
| Dấu hỏi `?` | Cách 1 khoảng trắng sau |
| Dấu ngoặc kép `""` | Không cách trước dấu mở, cách 1 sau dấu đóng |
| Dấu ngoặc đơn `()` | Không cách trước `(`, cách 1 sau `)` |

### Số và đơn vị

- Số và đơn vị: `4 cm`, `0,5 s`, `25°C` (cách 1 khoảng trắng)
- Số thập phân: dùng **dấu phẩy** `,` (theo chuẩn Việt Nam)
- Số lớn: dùng **dấu chấm** `.` để phân cách hàng nghìn (vd: 1.000.000)
- Phần trăm: `25%` (không cách)

### Tên riêng & Chữ hoa

- Tên người, địa danh: chữ hoa đầu mỗi từ
- Tên bài học: **VIẾT HOA TOÀN BỘ** (vd: DAO ĐỘNG ĐIỀU HOÀ)
- Tên định luật: chữ hoa đầu (vd: Định luật Jun - Lơ)
- Kí hiệu vật lí: in nghiêng, không hoa (vd: *v*, *a*, *F*)

---

## 12. Math & Physics Formulas

### Cách viết công thức

| Loại | Cách trình bày |
|------|----------------|
| Phương trình đơn giản | `x = Acos(ωt + φ)` (inline, font TNR) |
| Phương trình dài | Đặt riêng dòng, căn giữa, in nghiêng biến |
| Phân số | `a/b` (đơn giản) hoặc dùng Equation Editor |
| Chỉ số trên/dưới | `A²`, `v₀` (dùng Unicode hoặc Equation) |
| Tích phân, tổng | Dùng Equation Editor |

### Kí hiệu vật lí chuẩn Việt Nam

| Đại lượng | Kí hiệu | Đơn vị |
|-----------|---------|--------|
| Li độ | x | m, cm |
| Biên độ | A | m, cm |
| Tần số góc | ω | rad/s |
| Chu kì | T | s |
| Tần số | f | Hz |
| Pha ban đầu | φ | rad |
| Vận tốc | v | m/s, cm/s |
| Gia tốc | a | m/s² |

---

## 13. Quality Checklist

### Pre-Export Checklist

#### Layout
- [ ] Khổ giấy A4, lề đúng theo loại tài liệu
- [ ] Font Times New Roman cho toàn bộ tài liệu
- [ ] Cỡ chữ đồng nhất theo từng cấp
- [ ] Line spacing 1.3 (hoặc theo scene)

#### Structure
- [ ] Số thứ tự I, II, III... liên tục, không bị thiếu
- [ ] Mỗi heading dùng style Heading 1/2/3 (không fake bằng bold)
- [ ] Bảng có header tô xám, lặp lại khi ngắt trang
- [ ] Page break ở đúng vị trí quy định

#### Content
- [ ] Không có placeholder `[xxx]` còn sót
- [ ] Không có chú thích Markdown (##, **, -) trong Word
- [ ] Dấu câu Việt Nam chuẩn (theo § 11)
- [ ] Số liệu, công thức đúng đơn vị

#### Print Test
- [ ] In thử trang 1 để kiểm tra layout
- [ ] Kiểm tra header/footer không đè lên nội dung
- [ ] Đảm bảo không có trang trắng
- [ ] Số trang liên tục, đúng thứ tự

---

## 14. Common Mistakes to Avoid

### ❌ Sai phổ biến và cách sửa

| Lỗi | Hậu quả | Cách sửa |
|-----|---------|----------|
| Dùng dấu cách để căn đáp án ABCD | Lệch khi in | Dùng bảng không viền 4 cột |
| Dùng bullet tự động cho "Câu 1." | Word tự thêm icon | Gõ tay số câu + dấu chấm |
| Ngắt trang giữa câu hỏi và đáp án | HS khó theo dõi | `keepNext + keepLines` |
| Dùng font Calibri trộn với TNR | Không đồng nhất | Set default font = Times New Roman |
| Heading không dùng Style | Không tạo được TOC | Áp dụng Heading 1/2/3 |
| Line spacing 1.0 | Khó đọc | Đặt 1.3 hoặc 1.5 |
| Quên header/footer | Thiếu thông tin | Thêm header + page number |
| Đề thi không có seal line | Không đúng quy định | Thêm seal line dọc (nếu cần) |
| Bảng không có padding | Text dính viền | Cell margin: 0.1 cm top/bottom, 0.15 cm L/R |
| Đáp án không tách riêng | HS nhìn được | Page Break giữa đề và đáp án |

---

## 15. Output Requirements

### Bắt buộc:
- File phải là `.docx` (không phải .doc, .odt, .rtf)
- Tên file rõ ràng, theo format đã quy định (§ Quick Setup)
- Lưu vào thư mục có cấu trúc: `[Năm học]/[Môn]/[Loại tài liệu]/[Tên file].docx`

### Tùy chọn:
- Xuất thêm PDF để in ấn ổn định hơn (File → Export → PDF)
- Nén ZIP nếu có nhiều file đính kèm (hình ảnh, phiếu in)

---

## 16. Workflow (Quy trình soạn thảo chuẩn)

```
1. Xác định loại tài liệu → Router (§ Task Router)
2. Tạo file mới từ template Word (.dotx) hoặc file mẫu
3. Setup page: khổ giấy, lề, orientation (§ 1)
4. Setup styles: Heading 1/2/3, font, size, color (§ 2, 4)
5. Viết nội dung theo cấu trúc tài liệu (§ 5.1-5.4)
6. Thêm header/footer + page number (§ 7)
7. Thêm trang bìa (nếu cần - § 9)
8. Kiểm tra bảng, công thức, dấu câu (§ 6, 11, 12)
9. Chạy checklist chất lượng (§ 13)
10. In thử 1 trang để kiểm tra
11. Xuất file cuối cùng + PDF (nếu cần)
```

---

## 17. References

### Văn bản pháp lý tham chiếu:
- **Thông tư 22/2021/TT-BGDĐT** - Đánh giá học sinh THCS và THPT
- **Công văn 5512/BGDĐT-GDTrH** - Xây dựng kế hoạch giáo dục
- **Chương trình GDPT 2018** - Bộ GD&ĐT
- **Cấu trúc đề thi TN THPT 2025** - Bộ GD&ĐT (28 câu, 50 phút)

### Tài liệu chuyên môn:
- SGK Vật Lí 12 - Kết nối tri thức (NXB Giáo dục Việt Nam)
- SGK Vật Lí 12 - Cánh diều (NXB Đại học Sư phạm)
- SGK Vật Lí 12 - Chân trời sáng tạo (NXB Giáo dục Việt Nam)

---

## 18. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-06-30 | Initial release - 4 document types, CV 5512, CTGDPT 2018, exam structure 2025-2026 |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│        VIETNAMESE EDU DOC - QUICK REF           │
├─────────────────────────────────────────────────┤
│ Font:    Times New Roman                        │
│ Body:    13pt, Justify, 1.3 lines               │
│ H1:      14pt bold, #1F4E79                     │
│ H2:      13pt bold, #000000                     │
│ Margin:  Top 2, Bot 2, Left 3, Right 2 (cm)     │
│ Table:   0.5pt border, header #D9D9D9 bold      │
│ Bullet:  I → 1 → a) → -                         │
│ Number:  Câu 1. Câu 2. (NO auto bullet)         │
│ ABCD:    Borderless 4-col table                 │
│ Page:    "Trang X / Y" footer, 9pt gray         │
│ Break:   keepNext + keepLines for questions     │
└─────────────────────────────────────────────────┘
```

---

**END OF SKILL DOCUMENT**
