# NÂNG CẤP: Hệ Thống AI Tạo Tài Liệu GEMS Vật Lý 12

> ⚠️ **Đã lỗi thời:** đề xuất dưới đây tham chiếu kiến trúc `engine/` + LaTeX/TikZ đã bị thay thế
> hoàn toàn bởi package `gems/` (kiến trúc v9.0, 7/2026 — xem `changelog.md` mục [2026-07-06]).
> Phần lớn hạng mục P0/P1 đã được giải quyết theo cách khác trong `gems/` (validation số câu ở
> `gems/generation/stages.py`, xuất DOCX thay vì LaTeX ở `gems/docx_export/`). Giữ lại làm tư liệu
> lịch sử; quy trình vận hành hiện tại xem
> [`docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md`](quy_trinh_tao_tai_lieu_chi_tiet.md).
>
> **Ngày:** 2026-06-24  
> **Nội dung kiểm tra:** Bài 4 — Nhiệt Dung Riêng  
> **Thư mục:** `output/hermes/bai4_nhiet_dung_rieng/` (đường dẫn cũ, nay là `output/bai4_nhiet_dung_rieng/`)

## I. VẤN ĐỀ CẤU TRÚC — Cross-File Validation

### 1.1 Module validation engine (P0)

**Hiện trạng:** Không có cơ chế kiểm tra tính nhất quán giữa các file đầu ra. Code tả GEMS (`dac_ta_gems.md`) khai báo 6 nhiệm vụ nhưng Phiếu học tập (`phieu_hoc_tap.md`) chỉ có 5 nhiệm vụ, số thứ tự lệch nhau.

**Yêu cầu nâng cấp:**
```
validate_cross_schema(dac_ta, phieu, huong_dan_slide) → match_tasks()
```
- Đọc YAML frontmatter của `dac_ta_gems.md` → trích xuất [ĐVKT, Nhiệm vụ, Loại]
- Quét `phieu_hoc_tap.md` và `huong_dan_slide.md` để kiểm tra:
  - Mỗi Nhiệm vụ trong code tả PHẢI xuất hiện đúng 1 lần
  - Số thứ tự nhiệm vụ PHẢI khớp xuyên suốt
  - Nếu thiếu/lệch → **BLOCK** output, không cho xuất `ready/`

### 1.2 Single source of truth cho task mapping (P1)

**Hiện trạng:** Danh sách 12 loại nhiệm vụ GEMS được hardcode rải rác. AI dễ sinh sai tên hoặc sai số thứ tự.

**Yêu cầu:**
- 1 file JSON central: `engine/gems_task_registry.json`
- Prompt injection: Inject registry vào system prompt của agent sinh tài liệu
- Validation check: So khớp mọi `Nhiệm vụ X` trong output với registry trước khi ghi file

---

## II. VẤN ĐỀ KỸ THUẬT — Template & Build

### 2.1 LaTeX template chuẩn (P0)

**Hiện trạng:** Mỗi `.tex` tự viết preamble riêng, gây conflict `inputenc` + `fontspec` → không compile được.

**Yêu cầu:**
```
soạn tài liệu/
├── engine/
│   ├── templates/
│   │   ├── preamble-xelatex.tex    # Dùng fontspec + XeLaTeX
│   │   ├── preamble-pdflatex.tex   # Dùng inputenc + font mặc định
│   │   ├── homework-template.tex    # \input{preamble-xelatex}
│   │   └── answer-key-template.tex  # \input{preamble-xelatex}
│   └── latex_compiler.py           # Tự động chọn XeLaTeX, báo lỗi compile
```
- Agent chỉ viết `\input{engine/templates/preamble-...tex}` → không tự viết preamble
- Post-generation script: `xelatex --interaction=nonstopmode file.tex` → nếu exit code ≠ 0, **ghi log lỗi và không đưa vào `ready/`**

### 2.2 Placeholder detection (P1)

**Hiện trạng:** Bài tập về nhà có hàng loạt placeholder chưa được fill:
- "Các câu hỏi trắc nghiệm từ Câu 3 đến Câu 18..."
- Chỉ 1/6 câu trả lời ngắn có nội dung

**Yêu cầu:**
- Scan file output sau khi sinh:
  - Pattern `\(.*\)` chứa từ khóa: `placeholder`, `TODO`, `...`, `(Các câu hỏi`, `* (Các`
  - Pattern `\(.*Các câu hỏi.*\)`
  - Nếu match → **BLOCK**, không cho vào `ready/`
- Hoặc: Agent phải đảm bảo count exact:
  - Trắc nghiệm: đúng N câu (lấy từ `dac_ta_gems.md`)
  - Trả lời ngắn: đúng M câu

---

## III. VẤN ĐỀ NỘI DUNG — Pedagogical Accuracy

### 3.1 Fact-check số liệu vật lý (P1)

**Hiện trạng:** Slide so sánh nước/dầu ăn không có số liệu `c_dầu`. Thiếu bảng tra cứu NHIỆT DUNG RIÊNG của các chất thông dụng.

**Yêu cầu:**
- Embed database vào agent context:
```yaml
reference_data:
  specific_heat_capacity_J_per_kgK:
    water: 4180
    cooking_oil: 1700-2100  # tùy loại
    aluminum: 880
    copper: 380
    iron: 460
    sand: 800
```
- Agent bắt buộc phải tra cứu trước khi đưa số liệu
- Nếu dùng số ảo → automatic substitution

### 3.2 Nhiệm vụ 6: Fact Check → Error Analysis (P1)

**Hiện trạng:** Tên "Fact Check Influencer" không phù hợp môi trường giáo dục. Bản thân task này (kiểm chứng sai số) bị thay thế bằng bài toán tính toán đơn thuần.

**Yêu cầu:**
- Đổi tên thành "Error Analysis — Phân Tích Sai Số Thực Nghiệm"
- Prompt template cho Nhiệm vụ 6:
  - Cho số liệu thô
  - Yêu cầu học sinh: (1) tính c, (2) so sánh với chuẩn, (3) xác định nguồn sai số lớn nhất, (4) đề xuất cải tiến phương án thí nghiệm
- Agent bắt buộc sinh Nhiệm vụ 6 cho mỗi ĐVKT thực hành, không được skip

### 3.3 Hệ thống 15 tiêu chí QA tự động (P1)

**Hiện trạng:** Tôi vừa chấm QA thủ công, mất ~15 phút. Không scale được.

**Yêu cầu:**
```
engine/gems_qa_checker.py
```
- Input: thư mục bài học (VD: `bai4_nhiet_dung_rieng/`)
- Output: scorecard `qa-report.md`
- 15 tiêu chí, mỗi tiêu chí 1-10 điểm
- Điểm pass: ≥ 135/150
- Nếu dưới pass → block `ready/`, ghi rõ lý do

---

## IV. VẤN ĐỀ QUY TRÌNH — Pipeline Automation

### 4.1 Giai đoạn "Reconciliation" (P0)

**Hiện trạng:** Pipeline hiện tại:  
`dac_ta_gems → generate [phieu, slide, btvn, dap_an] → output`  
Không có giai đoạn check chéo.

**Yêu cầu:**
```
dac_ta_gems → GENERATE → RECONCILE → OUTPUT → QA → ready/
                            │
                    compare(manifest, actual)
                     - Mỗi nhiệm vụ trong code tả
                       có đúng file output không?
                     - Mỗi file output có số câu
                       đúng kỳ vọng không?
                     - Nếu sai → re-generate
```

### 4.2 Incremental generation (P2)

**Hiện trạng:** Nếu phát hiện lỗi, phải regenerate toàn bộ bài → tốn token.

**Yêu cầu:**
- Mỗi tài liệu output độc lập (đã đúng)
- Reconciliation chỉ re-generate file lỗi, không động file OK

### 4.3 File landing conveyor (P1)

**Hiện trạng:** `ready/` chứa file OK và file lỗi lẫn lộn.

**Yêu cầu;**
```
output/hermes/bai4_nhiet_dung_rieng/
├── md/          # Source markdown
├── ready/       # Only pass QA
├── staging/     # Output mới sinh, chờ QA
└── failed/      # File fail QA + lý do
```
Chỉ `ready/` được publish.

---

## V. TỔNG HỢP ƯU TIÊN

### Sprint 1 (Ngay lập tức)
| Feature | Module | Effort |
|---------|--------|--------|
| LaTeX template chuẩn | `engine/templates/` | 1 file | 
| Cross-file task validation | `engine/validator.py` | ~30 dòng Python |
| Bổ sung Nhiệm vụ Matching Matrix & Error Analysis | Prompt engineering | Sửa prompt |
| Placeholder detection | `engine/placeholder_check.py` | ~20 dòng Python |

### Sprint 2 (Tuần này)
| Feature | Module | Effort |
|---------|--------|--------|
| Hệ thống file conveyor (staging/ready/failed) | Pipeline restructuring | 1 file |
| Fact-check database embedding | `engine/ref_data.yaml` | 1 file |

### Sprint 3 (Dài hạn)
| Feature | Module | Effort |
|---------|--------|--------|
| GEMS QA Checker (15 tiêu chí tự động) | `engine/gems_qa_checker.py` | ~100 dòng |
| Incremental generation | Pipeline upgrade | ~50 dòng |
| GEMS task registry JSON | `engine/gems_task_registry.json` | 1 file |

---

> **Kết luận:** Hệ thống hiện tại tạo content vật lý **chính xác** (122/150 QA) nhưng thiếu **validation layer** và **template chuẩn hóa**. 3 lỗi P0 trực tiếp ngăn file xuất bản (LaTeX không compile, thiếu nhiệm vụ, placeholder chưa fill). Cần 1 pipeline gate trước `ready/` — không phải tốn thêm token regenerate.