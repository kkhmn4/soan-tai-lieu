"""Bộ style dùng chung cho minh họa khoa học vẽ bằng matplotlib.

Không dùng đường AI text-to-image (không có sẵn trong phiên Claude Code) và
không dùng SVG->PNG qua cairosvg (máy thiếu thư viện `cairo` gốc, xem
`docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md`) — vẽ thẳng bằng
matplotlib cho ra ảnh raster chất lượng cao, chính xác vật lý, không phụ
thuộc thêm gói ngoài nào (matplotlib + numpy đã có sẵn trong môi trường).

Bảng màu lấy đúng theo `.agents/agents.md` §3 (nguồn thật `gems/docx_export/
palette.py`) để mọi ảnh minh họa nhất quán màu với bản Word — KHÔNG dùng
bảng Navy/Mint của thế hệ thiết kế cũ đã bị khai tử.
"""
from __future__ import annotations

from contextlib import contextmanager

import matplotlib

matplotlib.use("Agg")  # không cần display — chạy được trên máy chủ/CI

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

PRIMARY = "#1F4E79"      # tiêu đề, khung chính, mũi tên chủ đạo
DARK = "#000000"         # chữ thân
GREY_FILL = "#D9D9D9"    # nền hộp ghi chú/hộp gợi ý
BORDER = "#BFBFBF"       # viền phụ, đường chấm
HIGHLIGHT = "#FFD600"    # chỉ dùng highlight từ khóa, không dùng nền lớn

FONT_FAMILY = "Times New Roman"


@contextmanager
def textbook_style():
    """Context manager áp style chữ/màu chuẩn GEMS cho khối vẽ bên trong."""
    with plt.rc_context({
        "font.family": FONT_FAMILY,
        "font.size": 12,
        "text.color": DARK,
        "axes.edgecolor": BORDER,
        "axes.labelcolor": DARK,
        "xtick.color": DARK,
        "ytick.color": DARK,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }):
        yield


def new_diagram_figure(figsize: tuple[float, float] = (9, 6), *, portrait: bool = False):
    """Figure trống cho sơ đồ kỹ thuật (không trục số) — dùng cho sơ đồ thí
    nghiệm, sơ đồ chu trình. `portrait=True` cho infographic dọc."""
    if portrait:
        figsize = (figsize[1], figsize[0])
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10 * figsize[1] / figsize[0])
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def new_graph_figure(figsize: tuple[float, float] = (8, 5)):
    """Figure cho đồ thị số liệu thật (trục X/Y có ý nghĩa vật lý)."""
    fig, ax = plt.subplots(figsize=figsize)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color(BORDER)
    ax.grid(True, linewidth=0.5, color=BORDER, alpha=0.5)
    ax.set_axisbelow(True)
    return fig, ax


def draw_labeled_box(ax, xy: tuple[float, float], width: float, height: float, text: str, *,
                       fill: str = GREY_FILL, edge: str = PRIMARY, fontsize: int = 11,
                       text_color: str = DARK, bold: bool = False) -> None:
    """Vẽ 1 khung chữ nhật bo góc nhẹ (phong cách SGK, không đổ bóng) kèm nhãn giữa khung."""
    x, y = xy
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.05,rounding_size=0.08",
        linewidth=1.2, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center",
             fontsize=fontsize, color=text_color, fontweight="bold" if bold else "normal",
             wrap=True)


def draw_arrow_label(ax, start: tuple[float, float], end: tuple[float, float], *,
                       label: str | None = None, color: str = PRIMARY,
                       label_offset: tuple[float, float] = (0.0, 0.25), fontsize: int = 10,
                       style: str = "-|>") -> None:
    """Vẽ 1 mũi tên có nhãn tùy chọn — dùng cho chiều dòng nhiệt, chiều dòng môi chất..."""
    arrow = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=16,
                              linewidth=1.6, color=color)
    ax.add_patch(arrow)
    if label:
        mx = (start[0] + end[0]) / 2 + label_offset[0]
        my = (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize, color=color)


def save_figure(fig, path: str, *, dpi: int = 220) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, facecolor="white", bbox_inches="tight")
    plt.close(fig)
