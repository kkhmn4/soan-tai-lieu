"""Vẽ minh họa khoa học cho Bài 28 - Động lượng, bản mở rộng (v2):

1. Thêm ảnh MỚI: sơ đồ thí nghiệm 3 viên bi A, B, C trên máng trượt (Hình
   28.1 SGK) — minh họa cho nhiệm vụ thí nghiệm khám phá mới ở mục 2.1.
2. Vẽ lại TOÀN BỘ 4 ảnh minh họa ở 2 tông màu riêng biệt để dùng cho 2 bộ
   Slide khác nhau (yêu cầu người dùng: "ảnh phải giống nhau" về nội dung/bố
   cục giữa 2 slide, chỉ khác tông màu):
   - `ready/hinh_anh/xam/*.png` — tông TRẮNG/ĐEN/XÁM thuần túy, dùng cho
     Slide Phiếu học tập học sinh (nền trắng, tối giản).
   - `ready/hinh_anh/mau/*.png` — tông màu thương hiệu Anthropic (Orange/
     Blue/Green), dùng cho Slide Giáo viên (đẹp, thu hút).
   Bản gốc 3 ảnh cũ (`ready/hinh_anh/*.png`, tông xanh dương #1F4E79 + đỏ,
   dùng trong KHBD/PHT bản Word) được GIỮ NGUYÊN không đổi — chỉ thêm ảnh thí
   nghiệm bi A/B/C bản tương tự (cùng tông) để KHBD/PHT dùng.

Chạy: python "output/bai28_dong_luong/scripts/generate_illustrations_v2.py"
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

BASE_DIR = Path(__file__).resolve().parent.parent / "ready" / "hinh_anh"
DOCX_DIR = BASE_DIR  # ảnh dùng trong KHBD/PHT bản Word (giữ nguyên tông cũ)
GRAY_DIR = BASE_DIR / "xam"
COLOR_DIR = BASE_DIR / "mau"
for d in (DOCX_DIR, GRAY_DIR, COLOR_DIR):
    d.mkdir(parents=True, exist_ok=True)

FONT_FAMILY = "Times New Roman"


@dataclass
class Palette:
    line: str        # màu đường viền/mũi tên chính
    accent: str       # màu nhấn thứ 2 (đối lập)
    fill: str         # nền hộp/khối nhạt
    text: str         # màu chữ
    border: str       # màu viền phụ/trục
    highlight: str    # màu tô nhấn từ khóa


DOCX_PALETTE = Palette(line="#1F4E79", accent="#C0392B", fill="#EAF2F8",
                       text="#000000", border="#BFBFBF", highlight="#FFD600")
GRAY_PALETTE = Palette(line="#2B2B2B", accent="#595959", fill="#E8E8E8",
                       text="#000000", border="#A6A6A6", highlight="#D9D9D9")
COLOR_PALETTE = Palette(line="#6A9BCC", accent="#D97757", fill="#E8E6DC",
                        text="#141413", border="#B0AEA5", highlight="#D97757")


@contextmanager
def textbook_style(palette: Palette):
    with plt.rc_context({
        "font.family": FONT_FAMILY, "font.size": 12, "text.color": palette.text,
        "axes.edgecolor": palette.border, "axes.labelcolor": palette.text,
        "xtick.color": palette.text, "ytick.color": palette.text,
        "figure.facecolor": "white", "savefig.facecolor": "white",
    }):
        yield


def new_diagram_figure(figsize=(9, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10 * figsize[1] / figsize[0])
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def new_graph_figure(figsize=(8, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def draw_labeled_box(ax, xy, width, height, text, palette: Palette, *, fontsize=11, bold=False):
    x, y = xy
    box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.05,rounding_size=0.08",
                          linewidth=1.2, edgecolor=palette.line, facecolor=palette.fill)
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fontsize,
            color=palette.text, fontweight="bold" if bold else "normal", wrap=True)


def draw_arrow(ax, start, end, palette: Palette, *, color=None, label=None, label_offset=(0, 0.25), fontsize=10):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16, linewidth=1.6,
                             color=color or palette.line)
    ax.add_patch(arrow)
    if label:
        mx = (start[0] + end[0]) / 2 + label_offset[0]
        my = (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize, color=color or palette.line)


def save_figure(fig, path: Path, *, dpi=220):
    fig.tight_layout()
    fig.savefig(str(path), dpi=dpi, facecolor="white", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# 1. VECTƠ ĐỘNG LƯỢNG
# ============================================================
def draw_momentum_vector(palette: Palette, out_path: Path) -> None:
    with textbook_style(palette):
        fig, ax = new_diagram_figure(figsize=(9, 4.5))
        ax.set_title("VECTƠ ĐỘNG LƯỢNG CỦA MỘT VẬT CHUYỂN ĐỘNG", fontsize=13, fontweight="bold",
                      color=palette.line, pad=14)
        ax.plot([0.6, 8.6], [2.0, 2.0], color=palette.border, linewidth=1.0, linestyle="--", zorder=1)
        draw_labeled_box(ax, (2.6, 1.5), 1.4, 1.0, "m", palette, fontsize=14, bold=True)
        draw_arrow(ax, (4.0, 2.35), (6.4, 2.35), palette, color=palette.line)
        ax.text(5.2, 2.75, r"$\vec{v}$", fontsize=15, color=palette.line, ha="center")
        draw_arrow(ax, (4.0, 1.15), (7.4, 1.15), palette, color=palette.accent)
        ax.text(5.7, 0.75, r"$\vec{p} = m\vec{v}$", fontsize=15, color=palette.accent, ha="center")
        ax.annotate("", xy=(4.0, 1.4), xytext=(4.0, 2.1),
                    arrowprops=dict(arrowstyle="-", color=palette.border, linewidth=0.8, linestyle=":"))
        ax.text(1.0, 3.3, "Vectơ động lượng $\\vec{p}$ luôn cùng phương,\ncùng chiều với vectơ vận tốc "
                          "$\\vec{v}$ của vật.", fontsize=10.5, color=palette.text, ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=palette.fill, edgecolor=palette.border))
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 4)
        save_figure(fig, out_path)


# ============================================================
# 2. ĐỒ THỊ LỰC - THỜI GIAN
# ============================================================
def draw_force_time_graph(palette: Palette, out_path: Path) -> None:
    with textbook_style(palette):
        fig, ax = new_graph_figure(figsize=(7.5, 5))
        ax.spines["bottom"].set_color(palette.border)
        ax.spines["left"].set_color(palette.border)
        ax.grid(True, linewidth=0.5, color=palette.border, alpha=0.5)
        ax.set_axisbelow(True)

        t0, t1, F0 = 1.0, 3.0, 4.0
        ax.plot([0, t0], [0, 0], color=palette.line, linewidth=2.2)
        ax.plot([t0, t0], [0, F0], color=palette.line, linewidth=2.2)
        ax.plot([t0, t1], [F0, F0], color=palette.line, linewidth=2.2)
        ax.plot([t1, t1], [F0, 0], color=palette.line, linewidth=2.2)
        ax.plot([t1, 4.2], [0, 0], color=palette.line, linewidth=2.2)

        xs = np.linspace(t0, t1, 5)
        ax.fill_between(xs, 0, F0, color=palette.highlight, alpha=0.6, zorder=0)
        ax.text((t0 + t1) / 2, F0 / 2, "Diện tích = $F.\\Delta t$\n(độ lớn xung lượng)",
                ha="center", va="center", fontsize=10.5, color=palette.text)

        ax.annotate("", xy=(t0, -0.35), xytext=(t1, -0.35),
                    arrowprops=dict(arrowstyle="<->", color=palette.text, linewidth=1.0))
        ax.text((t0 + t1) / 2, -0.7, "$\\Delta t$", fontsize=12, ha="center", color=palette.text)

        ax.set_xlim(0, 4.2)
        ax.set_ylim(-1.0, F0 + 1.2)
        ax.set_xticks([t0, t1])
        ax.set_xticklabels(["$t_1$", "$t_2$"])
        ax.set_yticks([F0])
        ax.set_yticklabels(["$F$"])
        ax.set_xlabel("Thời gian $t$", fontsize=11)
        ax.set_ylabel("Độ lớn lực $F$", fontsize=11)
        ax.set_title("ĐỒ THỊ LỰC - THỜI GIAN CỦA MỘT LỰC KHÔNG ĐỔI", fontsize=12, fontweight="bold",
                     color=palette.line, pad=12)
        save_figure(fig, out_path)


# ============================================================
# 3. SƠ ĐỒ BÓNG VA CHẠM TƯỜNG
# ============================================================
def draw_ball_wall_bounce(palette: Palette, out_path: Path) -> None:
    with textbook_style(palette):
        fig, ax = new_diagram_figure(figsize=(9, 5))
        ax.set_title("ĐỘNG LƯỢNG CỦA QUẢ BÓNG TRƯỚC VÀ SAU KHI VA CHẠM TƯỜNG", fontsize=12.5,
                     fontweight="bold", color=palette.line, pad=14)
        wall_x = 7.6
        ax.plot([wall_x, wall_x], [0.5, 4.5], color=palette.text, linewidth=5, solid_capstyle="butt")
        for hy in np.linspace(0.7, 4.3, 6):
            ax.plot([wall_x, wall_x + 0.35], [hy, hy + 0.3], color=palette.text, linewidth=1.0)
        ax.text(wall_x + 0.5, 2.5, "Tường", fontsize=10, color=palette.text, rotation=90, va="center")

        ax.add_patch(Circle((2.2, 3.1), 0.32, facecolor=palette.fill, edgecolor=palette.line, linewidth=1.4))
        draw_arrow(ax, (2.6, 3.1), (5.4, 3.1), palette, color=palette.line)
        ax.text(4.0, 3.55, r"$\vec{p_1}$ (trước va chạm)", fontsize=11, color=palette.line, ha="center")

        ax.add_patch(Circle((2.2, 1.5), 0.32, facecolor=palette.fill, edgecolor=palette.accent, linewidth=1.4))
        draw_arrow(ax, (5.4, 1.5), (2.6, 1.5), palette, color=palette.accent)
        ax.text(4.0, 1.05, r"$\vec{p_2}$ (sau va chạm)", fontsize=11, color=palette.accent, ha="center")

        ax.text(0.3, 4.3, "Tốc độ trước và sau va chạm có thể\nbằng nhau về độ lớn, nhưng $\\vec{p_2}$\n"
                          "ngược chiều $\\vec{p_1}$ nên $\\Delta \\vec{p} = \\vec{p_2}-\\vec{p_1} \\neq 0$.",
                fontsize=10, color=palette.text, ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=palette.fill, edgecolor=palette.border))
        ax.set_xlim(0, 9.5)
        ax.set_ylim(0, 5)
        save_figure(fig, out_path)


# ============================================================
# 4. SƠ ĐỒ THÍ NGHIỆM BA VIÊN BI A, B, C (MỚI — Hình 28.1 SGK)
# ============================================================
def draw_ramp_experiment(palette: Palette, out_path: Path) -> None:
    with textbook_style(palette):
        fig, ax = new_diagram_figure(figsize=(9, 6))
        ax.set_title("SƠ ĐỒ THÍ NGHIỆM TRUYỀN CHUYỂN ĐỘNG (BA VIÊN BI A, B, C)", fontsize=12.5,
                     fontweight="bold", color=palette.line, pad=14)

        # Máng trượt nghiêng (tam giác)
        ramp_top = (1.5, 5.2)
        ramp_foot = (6.5, 1.2)
        ramp_base_right = (6.5, 5.2)
        ax.plot([ramp_top[0], ramp_foot[0]], [ramp_top[1], ramp_foot[1]], color=palette.line, linewidth=2.2)
        ax.plot([ramp_top[0], ramp_base_right[0]], [ramp_top[1], ramp_base_right[1]], color=palette.border,
                linewidth=1.0, linestyle="--")
        ax.plot([ramp_foot[0], ramp_base_right[0]], [ramp_foot[1], ramp_base_right[1]], color=palette.border,
                linewidth=1.0, linestyle="--")
        # Mặt bàn ngang
        ax.plot([ramp_foot[0], 9.2], [ramp_foot[1], ramp_foot[1]], color=palette.line, linewidth=2.2)

        # Bi A/B ở đỉnh dốc (v0 = 0)
        ax.add_patch(Circle((ramp_top[0] + 0.35, ramp_top[1] - 0.15), 0.28, facecolor=palette.fill,
                             edgecolor=palette.line, linewidth=1.4))
        ax.text(ramp_top[0] + 0.35, ramp_top[1] + 0.45, "Bi A (hoặc B)", fontsize=10, color=palette.text,
                ha="center")
        ax.text(ramp_top[0] + 1.5, ramp_top[1] - 0.15, "$v_0=0$", fontsize=10, color=palette.text, va="center")

        # Mũi tên v dọc theo máng trượt
        mid_x = (ramp_top[0] + ramp_foot[0]) / 2
        mid_y = (ramp_top[1] + ramp_foot[1]) / 2
        draw_arrow(ax, (ramp_top[0] + 1.0, ramp_top[1] - 0.9), (mid_x + 0.5, mid_y - 0.5), palette,
                   color=palette.accent, label="$v$", label_offset=(0.55, 0.15), fontsize=12)

        # Bi C ở chân dốc trên mặt bàn
        ax.add_patch(Circle((ramp_foot[0] + 0.9, ramp_foot[1] + 0.28), 0.28, facecolor=palette.fill,
                             edgecolor=palette.line, linewidth=1.4))
        ax.text(ramp_foot[0] + 0.9, ramp_foot[1] + 0.85, "Bi C", fontsize=10, color=palette.text, ha="center")

        # Ghi chú độ dốc thay đổi (thí nghiệm 2)
        ax.text(2.0, 2.0, "Thay đổi độ dốc\n(Thí nghiệm 2)", fontsize=9.5, color=palette.text, ha="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=palette.fill, edgecolor=palette.border))

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6.2)
        save_figure(fig, out_path)


DRAWERS = [
    ("vecto_dong_luong.png", draw_momentum_vector),
    ("do_thi_luc_thoi_gian.png", draw_force_time_graph),
    ("so_do_bong_va_cham_tuong.png", draw_ball_wall_bounce),
    ("so_do_thi_nghiem_bi_abc.png", draw_ramp_experiment),
]

if __name__ == "__main__":
    # Bản Word (KHBD/PHT) — chỉ vẽ MỚI ảnh thí nghiệm (3 ảnh còn lại đã có sẵn, giữ nguyên).
    draw_ramp_experiment(DOCX_PALETTE, DOCX_DIR / "so_do_thi_nghiem_bi_abc.png")

    # 2 bộ ảnh đầy đủ cho 2 slide deck (nội dung/bố cục giống hệt nhau, chỉ khác tông màu)
    for name, fn in DRAWERS:
        fn(GRAY_PALETTE, GRAY_DIR / name)
        fn(COLOR_PALETTE, COLOR_DIR / name)

    print("OK - da ve xong anh minh hoa (docx + xam + mau)")
