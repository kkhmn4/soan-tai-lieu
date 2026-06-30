---
tags: [GEMS, NotebookLM, Google]
---

# GEMS - NotebookLM Integration

Hướng dẫn tích hợp Google **NotebookLM** vào pipeline [[GEMS v8.0 - Tổng quan]] để tạo nhanh slide và infographic.

Công cụ bổ trợ cho [[GEMS - Workflow 6 bước]], giúp đẩy nhanh Bước 4 (Slide) và Bước 5 (Homework).

---

## 🔧 CLI Pipeline

Quy trình chạy từ terminal (git-bash/MSYS):

```bash
# Bước 1: Đăng nhập
nlm login

# Bước 2: Tạo notebook mới
nlm create "Vật lý 12 - [Chủ đề]" --description "GEMS Physics notebook"

# Bước 3: Thêm nguồn (source PDF, image, web pages)
nlm source add path/to/[Tài liệu nguồn].pdf

# Bước 4: Tạo slide deck (tiếng Việt)
nlm slides create --language vi

# Bước 5: Tạo infographic
nlm infographic create --language vi

# Bước 6: Download sản phẩm
nlm download
```

---

## ⚠️ Gotchas — Những lỗi thường gặp

### Gotcha 1: `nlm download slide-deck` chỉ ra PDF, không phải PPTX
> `nlm download` xuất slide dạng **PDF**, **không** phải PowerPoint (.pptx)
- **Giải pháp**: Dùng backend khác để import PDF → PPTX (ví dụ Google Slides automation)
- **Mẹo**: Định dạng trước trong NotebookLM, xuất PDF rồi dùng công cụ chuyển đổi

### Gotcha 2: Session timeout
> NotebookLM CLI có session timeout ~30 phút không hoạt động
- **Hiện tượng**: Chạy lệnh sau 30 phút → báo lỗi auth
- **Giải pháp**:
  ```bash
  nlm login --clear   # Xóa cache session cũ
  nlm login           # Đăng nhập lại
  ```

### Gotcha 3: `nlm --profile` đặt SAU subcommand
> Sai cú pháp hay gặp:
```bash
nlm --profile account2 login      # ❌ Sai
nlm login --profile account2      # ✅ Đúng
```
- **Cú pháp chuẩn**: `nlm <subcommand> --profile <tên>`
- Profile phải đặt **sau subcommand**, không trước

### Gotcha 4: UnicodeEncodeError khi chạy trên Windows
> Windows console mặc định không hỗ trợ UTF-8 đầy đủ cho tiếng Việt
- **Hiện tượng**: Lỗi `UnicodeEncodeError` khi gõ tiếng Việt trong lệnh
- **Giải pháp**:
  ```bash
  # Trước khi chạy bất kỳ lệnh nào:
  export PYTHONUTF8=1     # git-bash
  # hoặc
  set PYTHONUTF8=1        # cmd.exe
  ```

---

## 🔄 Account Rotation

Lý do: Google NotebookLM có giới hạn sử dụng miễn phí, cần xoay vòng tài khoản.

| Tài khoản | Username | Ghi chú |
|-----------|----------|---------|
| **default** | `khakhunghiep` | Tài khoản chính |
| **account2** | `hoatrang756` | Dự phòng 1 |
| **account3** | `aichampionhk1` | Dự phòng 2 |

### Cách đổi tài khoản
```bash
# Đăng xuất tài khoản hiện tại
nlm logout --profile default

# Đăng nhập tài khoản khác
nlm login --profile account2
```

### Lịch xoay vòng khuyến nghị
- Dùng **default** cho 70% sản phẩm
- **account2** cho 20% (khi default bị rate-limit)
- **account3** cho 10% (khi cả 2 đều bị hạn chế)

---

## 🧠 Mẹo sử dụng hiệu quả

1. **Chuẩn bị nguồn kỹ** trước khi add vào NotebookLM: PDF sạch, có cấu trúc rõ ràng
2. **Luôn xem trước** slide trong NotebookLM trước khi download
3. **Luôn chạy [[GEMS - 15 QA Criteria]]** sau khi lấy file từ NotebookLM
4. **Humanize** lại ngôn ngữ ([[GEMS - Humanization Rules]]) sau khi xuất — NotebookLM thường sinh văn "AI-ism"
5. **Không dùng NotebookLM cho Bước 3 (PHT)** — PHT cần QA chặt từ đầu

---

*Tham khảo: [[GEMS - Workflow 6 bước]] | [[GEMS - Slide Design Rules]] | [[GEMS - Humanization Rules]]*