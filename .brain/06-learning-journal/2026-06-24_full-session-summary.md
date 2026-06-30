














































































- Settings là slide-out panel
- Selectors cần cập nhật

---

## 4. NOTEBOOKLM INTEGRATION

### 4.1 NLM CLI Pipeline
```
nlm login → nlm create → nlm source add → nlm slides create --language vi
→ nlm infographic create → nlm poll → nlm download
```

### 4.2 Accounts
| Profile | Email |
|---------|-------|
| default | khakhunghiep@gmail.com |
| account2 | hoatrang756@gmail.com |
| account3 | aichampionhk1@gmail.com |

### 4.3 Gotchas
- `nlm --profile` đặt SAU subcommand (VD: `nlm list notebooks --profile account2`)
- Slide mới chỉ download PDF, không PPTX
- Session timeout → `nlm login --clear`
- UnicodeEncodeError → set `PYTHONUTF8=1`

---

## 5. MCP SERVER — BRAINSTORM

### 5.1 Kiến trúc đề xuất
- **1 MCP Server** — 2 tools:
  1. `generate_lesson_plan` — docx (dùng GEMS Engine Python)
  2. `generate_interactive_lesson` — HTML thuần (tương tác, QR)
- **3 client:** Hermes Agent, Web dongbayai.vn, GEMS LMS

### 5.2 GEMS LMS
- **Path:** `.antigravity-ide/dự án LMS/`
- **Stack:** Next.js + TailwindCSS + Supabase
- **5 modules:** AI Copilot, Word Engine, Media Generator, Slide tương tác, Báo cáo năng lực

---

## 6. GAME QA — VŨ TRỤ HÓA HỌC

### 6.1 Thông tin
- **URL:** https://q1x875c1rak0-d.space-z.ai/
- **Tác giả:** Cô Trang Vũ — KHTN

### 6.2 Kết quả test
- **Maze mode:** 230 điểm, 8/8 chữ CONGRATS ✅