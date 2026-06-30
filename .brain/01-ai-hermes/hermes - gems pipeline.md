---
tags: [Hermes, GEMS, automation, pipeline]
---

# 🔄 Hermes ⟷ GEMS — Liên kết xuyên domain

> Cầu nối giữa [[01-AI-Hermes|Hermes Agent]] và [[02-GEMS-Physics|GEMS Framework]]

## Hermes dùng để tự động hóa GEMS

Hermes chạy toàn bộ pipeline GEMS thông qua:

| Công cụ Hermes | Dùng trong GEMS |
|----------------|----------------|
| `delegate_task` | Chạy song song multiple GEMS generators |
| `cronjob` | Tự động chạy pipeline GEMS theo lịch |
| Skills (`gems-physics-v8`) | Framework GEMS v8.0 dưới dạng skill |
| `terminal` | Chạy Python engine GEMS |
| Skill `gems-notebooklm` | Tích hợp NotebookLM với GEMS |

## Luồng Hermes chạy GEMS

```
Hermes session
    │
    ├── skill_view('gems-physics-v8') → Load framework
    ├── terminal('python main.py ...') → Chạy engine
    ├── delegate_task → Subagent sinh nội dung song song
    └── cronjob → Lên lịch chạy tự động
```

## GEMS Skills trong Hermes
- [[Hermes Agent - Skills]] — education/gems-physics-v8, gems-notebooklm
- [[GEMS v8.0 - Tổng quan]] — Framework đầy đủ

## STT & Ghi chép
- [[Hermes Agent - STT Nâng cấp]] — Ghi voice notes cho Learning Journal
- [[2026-06-22]] ngày tạo GEMS v8.0
- [[2026-06-24]] ngày tích hợp GEMS + Web + Google Flow

---

#Hermes #GEMS #automation #pipeline
