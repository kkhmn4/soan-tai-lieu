"""Sửa hậu kỳ (post-process) file Bài tập về nhà đã xuất cho Bài 28 - Động
lượng, KHÔNG sửa code dùng chung trong `gems/docx_export/` (dùng chung cho
toàn bộ pipeline Vật Lý 12, không đụng tới cho tác vụ một lần này):

`homework_exporter._render_student_body` không nhận diện cú pháp phân cách
Markdown "---" (không giống `parse_markdown_blocks` dùng ở PHT/KHBD) nên dòng
"---" mà `stages.write_homework_markdown` luôn chèn trước heading đáp án bị
in lộ ra thành văn bản thô "---" ngay trước dòng "----- HẾT -----" — đây là
lỗi có sẵn trong code dùng chung (xảy ra với MỌI bài, không riêng bài này),
sửa hậu kỳ bằng cách xoá đoạn văn thừa đó thay vì sửa exporter dùng chung.

(PHT không cần sửa hậu kỳ nữa — từ khi PHT chuyển sang dựng riêng bằng
python-docx ở `build_pht.py`, không còn qua `pht_exporter.py` với chuỗi
hardcode "Vật lí 12".)

Chạy: python "output/bai28_dong_luong/scripts/fix_docx_postprocess.py"
"""
from __future__ import annotations

from pathlib import Path

from docx import Document

READY_DIR = Path(__file__).resolve().parent.parent / "ready"
HW_PATH = READY_DIR / "bai28_dong_luong_bai_tap_ve_nha.docx"


def fix_homework_stray_separator() -> int:
    doc = Document(str(HW_PATH))
    removed = 0
    for p in list(doc.paragraphs):
        if p.text.strip() == "---":
            elem = p._element
            elem.getparent().remove(elem)
            removed += 1
    doc.save(str(HW_PATH))
    return removed


if __name__ == "__main__":
    n = fix_homework_stray_separator()
    print(f"Bai tap ve nha: da xoa {n} doan thua.")
