"""Nguồn thật duy nhất cho lề trang & độ rộng bảng theo từng loại tài liệu.

Trước đây các con số này (2/2/2/2, 2/2/3/2, 1.5/1.5/2/2 cm; 17.0cm/16.0cm)
bị rải rác dưới dạng literal hardcode ở nhiều nơi khác nhau (mỗi exporter tự
gõ lại), và 2 tài liệu đặc tả (.agents/agents.md, skills/gems_physics_skill.md)
còn ghi những con số CŨ không khớp với code (lề phải 1.5cm, bảng "luôn 16.5cm").
Từ giờ mọi nơi — kể cả tài liệu đặc tả — phải bắt nguồn từ đúng 1 chỗ này.
"""
from __future__ import annotations

from dataclasses import dataclass

PAGE_WIDTH_CM = 21.0
PAGE_HEIGHT_CM = 29.7


@dataclass(frozen=True)
class DocLayout:
    doc_type: str
    top_margin_cm: float
    bottom_margin_cm: float
    left_margin_cm: float
    right_margin_cm: float

    @property
    def content_width_cm(self) -> float:
        return PAGE_WIDTH_CM - self.left_margin_cm - self.right_margin_cm


LAYOUTS: dict[str, DocLayout] = {
    "pht": DocLayout("pht", top_margin_cm=2.0, bottom_margin_cm=2.0, left_margin_cm=2.0, right_margin_cm=2.0),
    "khbd": DocLayout("khbd", top_margin_cm=2.0, bottom_margin_cm=2.0, left_margin_cm=3.0, right_margin_cm=2.0),
    "homework": DocLayout("homework", top_margin_cm=1.5, bottom_margin_cm=1.5, left_margin_cm=2.0, right_margin_cm=2.0),
}


def get_layout(doc_type: str) -> DocLayout:
    try:
        return LAYOUTS[doc_type]
    except KeyError as exc:
        raise ValueError(f"Không có layout cho doc_type={doc_type!r}. Các loại hợp lệ: {list(LAYOUTS)}") from exc
