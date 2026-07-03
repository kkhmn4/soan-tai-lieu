# GEMS Skills — Hướng dẫn Tài liệu Tri thức & Điều phối

Thư mục này chứa các tệp tin tri thức (GEMS standard) và điều phối tương tác (AWF skills) của dự án. 

---

## 📚 Bản đồ Kỹ năng (Skills Map)

```
                       ┌──────────────────────┐
                       │  gems_physics_skill  │ (Single Source of Truth)
                       │  - Định nghĩa chuẩn  │
                       │  - Quy chuẩn in ấn   │
                       └──────────┬───────────┘
                                  │
                                  ▼ (Tham chiếu luật)
                       ┌──────────────────────┐
                       │ awf-gems_workflow_sk.│ (Điều phối 6 bước tương tác)
                       │  - Cách viết Markdown│
                       │  - Hướng dẫn chạy    │
                       └──────────┬───────────┘
                                  │
                                  ▼ (Vận hành tự động)
                       ┌──────────────────────┐
                       │  hermes-gems-automa. │ (Pipeline tự động hóa 1 click)
                       │  - Cấu trúc Hermes   │









* **Mô tả:** Là nguồn tri thức cốt lõi (Single Source of Truth) của hệ thống.
* **Nhiệm vụ:**
  * Định nghĩa 7 nguyên tắc sư phạm cốt lõi trong biên soạn tài liệu Vật lý.
  * Hướng dẫn cụ thể về 12 loại hình nhiệm vụ học tập GEMS mới.
  * Định hình quy chuẩn in ấn bắt buộc: dòng chấm điền khuyết dài đúng 90 ký tự (`..........................................................................................`), phông chữ, định dạng LaTeX công thức vật lý, biên dịch sơ đồ TikZ.
  * Cung cấp 15 tiêu chí QA Self-Check giúp đánh giá tính chính xác của tài liệu.

### 2. **[awf-gems_workflow_skill.md](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/skills/awf-gems_workflow_skill.md) — AWF GEMS Workflow**
* **Mô tả:** Điều phối tiến trình tương tác 6 bước giữa người dùng và trợ lý AI.
* **Nhiệm vụ:**
  * Hướng dẫn cách sinh và kiểm định cấu trúc các tệp tin đặc tả (SPEC), phiếu học tập, giáo án và slide thô.
  * Hướng dẫn cách gọi các script hậu kỳ ở cuối mỗi bước.

### 3. **[hermes-gems-automation.md](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/skills/hermes-gems-automation.md) — GEMS Hermes Pipeline**
* **Mô tả:** Kỹ năng tự động hóa quy trình sản xuất học liệu.
* **Nhiệm vụ:**
  * Định nghĩa cấu trúc phân loại đầu ra Hermes chuẩn: `md/`, `ready/`, `assets/`, `notebooklm/`.
  * Hướng dẫn quy trình nạp tài liệu và tạo slide/infographic dạng dọc theo từng đơn vị kiến thức trên Google NotebookLM thông qua CLI.

### 4. **[gems_khbd_generation_skill.md](file:///c:/Users/Admin/.antigravity-ide/soạn%20tài%20liệu/skills/gems_khbd_generation_skill.md) — GEMS KHBD Generation Standards**
* **Mô tả:** Hướng dẫn Agent AI tự động biên soạn Kế hoạch bài dạy (Giáo án) chi tiết theo Công văn 5512 môn Vật lý.
* **Nhiệm vụ:**
  * Định nghĩa chi tiết cấu trúc 4 hoạt động sư phạm của Công văn 5512.
  * Quy định định dạng Microsoft Word (.docx) chuyên sâu (lề trang động, giãn dòng 1.3 lines, spacing 6pt, thụt đầu dòng 1cm, bảng hoạt động 2 cột).
  * Tự động bôi đậm các từ khóa hành động sư phạm cốt lõi.
