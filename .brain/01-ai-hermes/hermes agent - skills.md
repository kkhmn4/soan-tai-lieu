---
tags: [Hermes, skills, learning]
---

# 📚 Hermes Agent — Skills

Skills là **bộ nhớ thủ tục** của Hermes — quy trình có thể tái sử dụng cho các tác vụ lặp lại.

## Skills hiện có

### Education
- **[[GEMS v8.0 - Tổng quan]]** — Framework tạo học liệu Vật lý 12 GDPT 2018
- **[[GEMS - NotebookLM Integration]]** — Tích hợp Google NotebookLM

### Autonomous AI Agents
- **hermes-agent** — Cấu hình, mở rộng Hermes
- **claude-code** — Delegate coding cho Claude Code
- **codex** — Delegate coding cho Codex CLI

### Google Automation
- **google-labs-automation** — Google Flow automation

## Cách tạo skill mới
Dùng tool `skill_manage(action='create', name='skill-name', content='...')`

## Cách xem skill
`skill_view(name='skill-name')`

## Lưu ý
- Skills nằm ở `~/.hermes/skills/`
- Mỗi skill có frontmatter YAML + nội dung Markdown
- Có thể có file đính kèm (references, templates, scripts)
- Skills tự động được load khi tên khớp với task

---

#Hermes #skills #learning #reuse
