 

# GEMS Skills — Hướng dẫn Tài liệu Tri thức

Từ kiến trúc v9.0 (7/2026), quy trình vận hành GEMS là **code chạy thật**
(`gems/` + `python -m gems ...`), không còn là chuỗi hướng dẫn thao tác thủ
công nhiều bước (AWF workflow cũ) — nên thư mục này chỉ còn 2 tài liệu tri
thức, mỗi tài liệu là nguồn thật cho đúng 1 việc, không chồng chéo:

## 1. [gems_physics_skill.md](gems_physics_skill.md) — Chuẩn sư phạm (nội dung)

* Vai trò/phong cách, 7 nguyên tắc sư phạm cốt lõi, 12 loại hình nhiệm vụ học tập.
* Yêu cầu nội dung theo từng loại tài liệu (PHT/Slide/KHBD/Bài tập/Infographic).
* 15 tiêu chí QA Self-Check.
* **Không** mô tả số liệu định dạng kỹ thuật (lề, font, màu) — xem mục 2.

## 2. [docx_skill.md](docx_skill.md) — Kỹ thuật xuất file Word

* Phần đầu là skill docx-js/XML tổng quát (dùng khi làm việc với .docx nói chung).
* Phần cuối "Adaptation cho hệ thống GEMS" ánh xạ sang các hàm thật trong
  [`gems/docx_export/styles.py`](../gems/docx_export/styles.py) — tra cứu ở đây
  trước khi tự viết lại logic set lề/bảng/footer.

## Số liệu định dạng chính thức (lề, màu, font, cấu trúc Markdown nhận diện được)

Nằm ở [`.agents/agents.md`](../.agents/agents.md) — tài liệu **duy nhất** cho
việc này, lấy trực tiếp từ `gems/docx_export/layout.py` và `palette.py`.

## Cách vận hành pipeline

Không còn quy trình thủ công nhiều bước — chạy thẳng CLI:

```powershell
python -m gems generate --lesson bai4      # Sinh Markdown + DOCX bằng Gemini API (cần GEMINI_API_KEY)
python -m gems compose --lesson bai4       # Như trên nhưng nội dung do AI agent tự soạn (JSON), không cần API key
python -m gems notebooklm --lesson bai4    # Tạo Slide + Infographic qua NotebookLM
python -m gems full --lesson bai4          # generate/compose + notebooklm liên tiếp
python -m gems offline --lesson bai4       # Chạy thử bằng fixture, không cần API/mạng
python -m gems lint --lesson bai4          # Kiểm định DOCX đã có trong ready/
python -m gems list-lessons                # Xem danh mục bài học (curriculum.yaml)
```

`compose` dùng khi không cấu hình `GEMINI_API_KEY` — chính AI agent đang chạy
trong Antigravity IDE tự soạn nội dung, ghi ra JSON khớp schema
`gems/models/*.py` vào `output/<slug>/authored/`, xem chi tiết ở
[readme.md](../readme.md#không-dùng-gemini_api_key--để-ai-agent-claudeantigravity-tự-soạn-nội-dung).
