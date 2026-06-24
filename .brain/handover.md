# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 HANDOVER DOCUMENT – GEMS Hermes Pipeline
# Lưu lúc: 2026-06-23T13:30:54+07:00
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📍 Đang làm gì

**Dự án:** GEMS Hermes – Tự động hoá sinh học liệu Vật lý Chương Nhiệt (Bài 4–7)  
**Bước hiện tại:** Upload tài liệu lên NotebookLM → Tạo Slide + Infographic → Download

---

## ✅ Đã hoàn thành

- [x] Sinh toàn bộ nội dung Markdown cho **Bài 4** (Nhiệt dung riêng): đặc tả, PHT, đáp án, KHBD, báo cáo NLM
- [x] Sinh toàn bộ nội dung Markdown cho **Bài 5** (Nhiệt độ nhiệt kế)
- [x] Sinh toàn bộ nội dung Markdown cho **Bài 6** (Nhiệt nóng chảy riêng)
- [x] Sinh toàn bộ nội dung Markdown cho **Bài 7** (Nhiệt hóa hơi riêng)
- [x] Tải ảnh minh họa cho Bài 4-7 vào `assets/images/`
- [x] Rollback engine Python (main.py + 5 generator files) về trạng thái gốc trước 01:00 sáng – xóa offline mode
- [x] Cập nhật session.json + brain.json

---

## ⏳ Còn lại

1. **Upload PHT + đáp án bài 4 lên NotebookLM** qua MCP tool
2. **Nhập prompt tạo slide** (xem prompt trong `output/hermes/bai4_nhiet_dung_rieng/notebooklm/`)
3. **Nhập prompt tạo infographic**
4. **Đợi xong → download PPTX + PNG**
5. **Kiểm tra chất lượng** (slide có đúng phông, tên GV, ngôn ngữ không?)
6. Lặp lại bước 1-5 cho Bài 5, 6, 7

---

## 🔧 Quyết định quan trọng

| Quyết định | Lý do |
|---|---|
| Dùng Anti Gravity MCP (không API key ngoài) | User yêu cầu: "chỉ dùng Anti Gravity platform" |
| Engine Python PHẢI có GEMINI_API_KEY | Không offline mode trong engine chính; dry_run.py là script riêng |
| Cấu trúc Hermes: `output/hermes/[bai]/[md\|notebooklm\|assets]` | Tách biệt rõ ràng từng loại file |
| Tên file: `Bai X [ten]_[loai]_[phan]` | Nhất quán cho toàn hệ thống |

---

## ⚠️ Lưu ý cho session sau

- **Không có git** → Nếu cần rollback, phải làm thủ công từ transcript. Nên chạy `git init` sớm!
- **NotebookLM session:** Nếu bị timeout → `nlm login --clear`
- **File cần upload lên NLM cho bài 4:**
  - `output/hermes/bai4_nhiet_dung_rieng/md/bai4_nhiet_dung_rieng_phieu_hoc_tap.md`
  - `output/hermes/bai4_nhiet_dung_rieng/md/bai4_nhiet_dung_rieng_dap_an.md`
- **Prompt NLM:** xem file `output/hermes/bai4_nhiet_dung_rieng/notebooklm/bai4_nhiet_dung_rieng_notebooklm_prompt.md`

---

## 📁 Files quan trọng

| File | Vai trò |
|---|---|
| `.brain/brain.json` | Kiến thức dự án (kiến trúc, quy tắc, gotcha) |
| `.brain/session.json` | Tiến độ session hiện tại |
| `engine/main.py` | Entry point pipeline GEMS (282 dòng, đã rollback) |
| `skills/hermes-gems-automation.md` | Skill hướng dẫn quy trình Hermes |
| `output/hermes/bai4_nhiet_dung_rieng/` | Toàn bộ nội dung bài 4 đã sẵn sàng |

---

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📍 Gõ /recap trong session mới để khôi phục context
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
