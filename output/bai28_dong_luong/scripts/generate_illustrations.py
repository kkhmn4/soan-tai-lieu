"""Vẽ minh họa khoa học cho Bài 28 - Động lượng (Vật Lý 10 KNTT) bằng
matplotlib (vector, chính xác vật lý, không hoạt hình) — theo đúng quy tắc
chọn công cụ vẽ ở `skills/gems_physics_skill.md` mục 4.6, tái sử dụng bộ
style dùng chung `gems/illustrations/style.py` (không sửa code dùng chung).

Đây là script một lần (one-off) cho bài Động lượng — không đăng ký vào
curriculum.yaml, chỉ dùng nội bộ cho thư mục output/bai28_dong_luong/.

Chạy: python "output/bai28_dong_luong/scripts/generate_illustrations.py"
Ghi PNG vào output/bai28_dong_luong/ready/hinh_anh/.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from gems.illustrations import style

OUT_DIR = Path(__file__).resolve().parent.parent / "ready" / "hinh_anh"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_momentum_vector_diagram() -> None:
    """Sơ đồ vectơ động lượng p = m.v cùng hướng với vận tốc v."""
    with style.textbook_style():
        fig, ax = style.new_diagram_figure(figsize=(9, 4.5))
        ax.set_title("VECTƠ ĐỘNG LƯỢNG CỦA MỘT VẬT CHUYỂN ĐỘNG",
                      fontsize=13, fontweight="bold", color=style.PRIMARY, pad=14)

        # Đường quỹ đạo chuyển động thẳng (nét đứt)
        ax.plot([0.6, 8.6], [2.0, 2.0], color=style.BORDER, linewidth=1.0, linestyle="--", zorder=1)

        # Vật (khối hộp) đặt giữa quỹ đạo
        style.draw_labeled_box(ax, (2.6, 1.5), 1.4, 1.0, "m", fill="#EAF2F8",
                                edge=style.PRIMARY, fontsize=14, bold=True)

        # Vectơ vận tốc v (từ tâm vật, hướng ngang)
        style.draw_arrow_label(ax, (4.0, 2.35), (6.4, 2.35), label=None, color=style.PRIMARY)
        ax.text(5.2, 2.75, r"$\vec{v}$", fontsize=15, color=style.PRIMARY, ha="center")

        # Vectơ động lượng p (song song, cùng hướng, vẽ thấp hơn để phân biệt)
        style.draw_arrow_label(ax, (4.0, 1.15), (7.4, 1.15), label=None, color="#C0392B")
        ax.text(5.7, 0.75, r"$\vec{p} = m\vec{v}$", fontsize=15, color="#C0392B", ha="center")

        # Chú thích cùng phương cùng chiều
        ax.annotate("", xy=(4.0, 1.4), xytext=(4.0, 2.1),
                     arrowprops=dict(arrowstyle="-", color=style.BORDER, linewidth=0.8, linestyle=":"))
        ax.text(1.0, 3.3,
                "Vectơ động lượng $\\vec{p}$ luôn cùng phương,\ncùng chiều với vectơ vận tốc $\\vec{v}$ của vật.",
                fontsize=10.5, color=style.DARK, ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=style.GREY_FILL, edgecolor=style.BORDER))

        ax.set_xlim(0, 9)
        ax.set_ylim(0, 4)
        style.save_figure(fig, str(OUT_DIR / "vecto_dong_luong.png"))


def draw_force_time_impulse_graph() -> None:
    """Đồ thị lực - thời gian (F không đổi trong Δt): diện tích hình chữ nhật
    = độ lớn xung lượng của lực F.Δt."""
    with style.textbook_style():
        fig, ax = style.new_graph_figure(figsize=(7.5, 5))

        t0, t1 = 1.0, 3.0
        F0 = 4.0
        ax.plot([0, t0], [0, 0], color=style.PRIMARY, linewidth=2.2)
        ax.plot([t0, t0], [0, F0], color=style.PRIMARY, linewidth=2.2)
        ax.plot([t0, t1], [F0, F0], color=style.PRIMARY, linewidth=2.2)
        ax.plot([t1, t1], [F0, 0], color=style.PRIMARY, linewidth=2.2)
        ax.plot([t1, 4.2], [0, 0], color=style.PRIMARY, linewidth=2.2)

        xs = np.linspace(t0, t1, 5)
        ax.fill_between(xs, 0, F0, color=style.HIGHLIGHT, alpha=0.55, zorder=0)
        ax.text((t0 + t1) / 2, F0 / 2, "Diện tích = $F.\\Delta t$\n(độ lớn xung lượng)",
                 ha="center", va="center", fontsize=10.5, color=style.DARK)

        ax.annotate("", xy=(t0, -0.35), xytext=(t1, -0.35),
                     arrowprops=dict(arrowstyle="<->", color=style.DARK, linewidth=1.0))
        ax.text((t0 + t1) / 2, -0.7, "$\\Delta t$", fontsize=12, ha="center", color=style.DARK)

        ax.set_xlim(0, 4.2)
        ax.set_ylim(-1.0, F0 + 1.2)
        ax.set_xticks([t0, t1])
        ax.set_xticklabels(["$t_1$", "$t_2$"])
        ax.set_yticks([F0])
        ax.set_yticklabels(["$F$"])
        ax.set_xlabel("Thời gian $t$", fontsize=11)
        ax.set_ylabel("Độ lớn lực $F$", fontsize=11)
        ax.set_title("ĐỒ THỊ LỰC - THỜI GIAN CỦA MỘT LỰC KHÔNG ĐỔI",
                      fontsize=12, fontweight="bold", color=style.PRIMARY, pad=12)
        style.save_figure(fig, str(OUT_DIR / "do_thi_luc_thoi_gian.png"))


def draw_ball_wall_bounce_diagram() -> None:
    """Sơ đồ va chạm bóng - tường: vectơ động lượng trước/sau đổi chiều."""
    with style.textbook_style():
        fig, ax = style.new_diagram_figure(figsize=(9, 5))
        ax.set_title("ĐỘNG LƯỢNG CỦA QUẢ BÓNG TRƯỚC VÀ SAU KHI VA CHẠM TƯỜNG",
                      fontsize=12.5, fontweight="bold", color=style.PRIMARY, pad=14)

        # Bức tường (bên phải)
        wall_x = 7.6
        ax.plot([wall_x, wall_x], [0.5, 4.5], color=style.DARK, linewidth=5, solid_capstyle="butt")
        for hy in np.linspace(0.7, 4.3, 6):
            ax.plot([wall_x, wall_x + 0.35], [hy, hy + 0.3], color=style.DARK, linewidth=1.0)
        ax.text(wall_x + 0.5, 2.5, "Tường", fontsize=10, color=style.DARK, rotation=90, va="center")

        # Bóng trước va chạm (bên trái, đi tới)
        ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
            (2.2, 3.1), 0.32, facecolor="#EAF2F8", edgecolor=style.PRIMARY, linewidth=1.4))
        style.draw_arrow_label(ax, (2.6, 3.1), (5.4, 3.1), label=None, color=style.PRIMARY)
        ax.text(4.0, 3.55, r"$\vec{p_1}$ (trước va chạm)", fontsize=11, color=style.PRIMARY, ha="center")

        # Bóng sau va chạm (bật ngược lại)
        ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
            (2.2, 1.5), 0.32, facecolor="#FDEBD0", edgecolor="#C0392B", linewidth=1.4))
        style.draw_arrow_label(ax, (5.4, 1.5), (2.6, 1.5), label=None, color="#C0392B")
        ax.text(4.0, 1.05, r"$\vec{p_2}$ (sau va chạm)", fontsize=11, color="#C0392B", ha="center")

        ax.text(0.3, 4.3,
                "Tốc độ trước và sau va chạm có thể\nbằng nhau về độ lớn, nhưng $\\vec{p_2}$\n"
                "ngược chiều $\\vec{p_1}$ nên $\\Delta \\vec{p} = \\vec{p_2}-\\vec{p_1} \\neq 0$.",
                fontsize=10, color=style.DARK, ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=style.GREY_FILL, edgecolor=style.BORDER))

        ax.set_xlim(0, 9.5)
        ax.set_ylim(0, 5)
        style.save_figure(fig, str(OUT_DIR / "so_do_bong_va_cham_tuong.png"))


if __name__ == "__main__":
    draw_momentum_vector_diagram()
    draw_force_time_impulse_graph()
    draw_ball_wall_bounce_diagram()
    print("Da ghi 3 anh minh hoa vao:", OUT_DIR)
