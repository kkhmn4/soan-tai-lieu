"""Vẽ 3 minh họa khoa học cho Bài 7 - Nhiệt hóa hơi riêng bằng matplotlib
(vector, chính xác vật lý, không hoạt hình) — xem quyết định công cụ ở
`docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md` và quy tắc chọn vector
vs ảnh AI ở `skills/gems_physics_skill.md` mục 4.6.

Chạy 1 lần: `python output/bai7_nhiet_hoa_hoi_rieng/scripts/generate_illustrations.py`
Ghi PNG vào `output/bai7_nhiet_hoa_hoi_rieng/ready/hinh_anh/` — đúng thư mục
fallback mà `gems.docx_export.markdown_ir.resolve_image_path` tự tìm.
"""
from __future__ import annotations

from pathlib import Path

from gems.illustrations import style

OUT_DIR = Path(__file__).resolve().parent.parent / "ready" / "hinh_anh"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_apparatus_diagram() -> None:
    with style.textbook_style():
        fig, ax = style.new_diagram_figure(figsize=(10, 8))
        ax.set_title("SƠ ĐỒ BỘ THÍ NGHIỆM ĐO NHIỆT HÓA HƠI RIÊNG CỦA NƯỚC",
                      fontsize=13, fontweight="bold", color=style.PRIMARY, pad=14)

        # --- Cân điện tử (đế) ---
        style.draw_labeled_box(ax, (1.5, 0.6), 5.0, 0.9, "", fill="white", edge=style.PRIMARY)
        ax.text(6.9, 1.05, "m = ..... g", fontsize=10, color=style.DARK, va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=style.GREY_FILL, edgecolor=style.BORDER))

        # --- Nhiệt lượng kế xốp (2 lớp vỏ để gợi cách nhiệt) ---
        cal_x, cal_y, cal_w, cal_h = 2.2, 1.5, 3.8, 4.6
        style.draw_labeled_box(ax, (cal_x, cal_y), cal_w, cal_h, "", fill="white", edge=style.PRIMARY)
        inset = 0.22
        style.draw_labeled_box(ax, (cal_x + inset, cal_y + inset), cal_w - 2 * inset, cal_h - 2 * inset - 0.6,
                                 "", fill="white", edge=style.BORDER)

        # --- Mực nước ---
        water_y0, water_y1 = cal_y + inset, cal_y + inset + 2.6
        ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
            (cal_x + inset, water_y0), cal_w - 2 * inset, water_y1 - water_y0,
            facecolor="#EAF2F8", edgecolor="none"))
        ax.plot([cal_x + inset, cal_x + cal_w - inset], [water_y1, water_y1],
                color=style.BORDER, linewidth=1.0, linestyle="--")

        # --- Dây đun điện trở (ngoằn ngoèo, ngập trong nước) ---
        import numpy as np
        xs = np.linspace(cal_x + 0.9, cal_x + cal_w - 1.3, 11)
        ys = water_y0 + 0.35 + 0.18 * (np.arange(len(xs)) % 2)
        ax.plot(xs, ys, color="#C0392B", linewidth=2.0, solid_capstyle="round")
        # Dây dẫn ra ngoài nhiệt lượng kế qua thành bên phải, nối tới oát kế
        wire_exit = (cal_x + cal_w - inset, water_y0 + 0.35)
        ax.plot([xs[-1], wire_exit[0]], [ys[-1], wire_exit[1]], color="#C0392B", linewidth=1.6)

        # --- Nhiệt kế điện tử (que dò từ trên cắm xuống nước) ---
        probe_x = cal_x + cal_w / 2 + 0.6
        ax.plot([probe_x, probe_x], [water_y0 + 0.5, cal_y + cal_h + 0.5], color=style.PRIMARY, linewidth=2.0)
        ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
            (probe_x, water_y0 + 0.5), 0.10, facecolor=style.PRIMARY, edgecolor="none"))
        style.draw_labeled_box(ax, (probe_x - 0.9, cal_y + cal_h + 0.5), 1.8, 0.55, "100,0 °C",
                                 fill=style.GREY_FILL, edge=style.PRIMARY, fontsize=9)

        # --- Hơi nước thoát ra (mũi tên đứt lên trên) ---
        style.draw_arrow_label(ax, (cal_x + cal_w / 2 - 0.8, cal_y + cal_h - 0.1),
                                 (cal_x + cal_w / 2 - 0.8, cal_y + cal_h + 1.3),
                                 label="hơi nước\nthoát ra", color=style.BORDER, style="-|>")

        # --- Oát kế điện tử + Biến thế nguồn (bên phải) ---
        style.draw_labeled_box(ax, (7.0, 3.6), 2.4, 1.0, "OÁT KẾ\nĐIỆN TỬ\n(đo P, t)", fill=style.GREY_FILL,
                                 edge=style.PRIMARY, fontsize=9)
        style.draw_labeled_box(ax, (7.0, 5.0), 2.4, 1.0, "BIẾN THẾ\nNGUỒN", fill=style.GREY_FILL,
                                 edge=style.PRIMARY, fontsize=9)
        ax.plot([xs[-1] + 0.5, 7.0], [ys[-1] + 1.5, 4.1], color="#C0392B", linewidth=1.4)
        style.draw_arrow_label(ax, (8.2, 4.6), (8.2, 5.0), color=style.PRIMARY)

        # --- Nhãn leader-line ---
        labels = [
            ((cal_x + cal_w / 2, cal_y + cal_h + 0.05), (cal_x - 1.7, cal_y + cal_h + 1.0), "Nhiệt lượng kế xốp\n(vỏ cách nhiệt)"),
            ((xs[6], ys[6]), (cal_x - 1.9, water_y0 + 0.4), "Dây đun điện trở"),
            ((4.0, 1.05), (1.0, 0.2), "Cân điện tử"),
        ]
        for (tx, ty), (lx, ly), text in labels:
            ax.plot([tx, lx], [ty, ly], color=style.BORDER, linewidth=0.8)
            ax.text(lx, ly, text, fontsize=9, color=style.DARK, ha="center", va="center",
                     bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=style.BORDER))

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        style.save_figure(fig, str(OUT_DIR / "so_do_thi_nghiem_do_L.png"))


def draw_temperature_time_graph() -> None:
    import numpy as np
    with style.textbook_style():
        fig, ax = style.new_graph_figure(figsize=(8, 5.2))
        t_heat = np.linspace(0, 8, 50)
        temp_heat = 20 + (100 - 20) / 8 * t_heat
        t_boil = np.linspace(8, 20, 50)
        temp_boil = np.full_like(t_boil, 100.0)

        ax.plot(t_heat, temp_heat, color=style.PRIMARY, linewidth=2.2)
        ax.plot(t_boil, temp_boil, color=style.PRIMARY, linewidth=2.2)
        ax.axhline(100, color=style.BORDER, linewidth=0.8, linestyle="--")
        ax.axvline(8, color=style.BORDER, linewidth=0.8, linestyle="--")
        ax.scatter([8], [100], color=style.PRIMARY, s=35, zorder=5)

        ax.annotate("Giai đoạn đun nóng\n(nhiệt độ tăng dần)", xy=(4, 60), fontsize=10, color=style.DARK,
                     ha="center",
                     bbox=dict(boxstyle="round,pad=0.35", facecolor=style.GREY_FILL, edgecolor=style.BORDER))
        ax.annotate("Giai đoạn hóa hơi\n(nhiệt độ KHÔNG ĐỔI ở 100 °C)", xy=(14, 92), fontsize=10,
                     color=style.DARK, ha="center",
                     bbox=dict(boxstyle="round,pad=0.35", facecolor=style.HIGHLIGHT, edgecolor=style.PRIMARY))
        ax.annotate("Bắt đầu sôi", xy=(8, 100), xytext=(8, 78),
                     fontsize=9, color=style.PRIMARY, ha="center",
                     arrowprops=dict(arrowstyle="-", color=style.PRIMARY, linewidth=0.9))

        ax.set_xlim(0, 20)
        ax.set_ylim(0, 115)
        ax.set_xlabel("Thời gian đun t (phút)", fontsize=11)
        ax.set_ylabel("Nhiệt độ của nước (°C)", fontsize=11)
        ax.set_title("ĐỒ THỊ NHIỆT ĐỘ THEO THỜI GIAN KHI ĐUN SÔI VÀ HÓA HƠI NƯỚC",
                      fontsize=12, fontweight="bold", color=style.PRIMARY, pad=12)
        style.save_figure(fig, str(OUT_DIR / "do_thi_nhiet_do_thoi_gian.png"))


def draw_ac_cycle_diagram() -> None:
    with style.textbook_style():
        fig, ax = style.new_diagram_figure(figsize=(10, 7.5))
        ax.set_title("SƠ ĐỒ NGUYÊN LÝ CHU TRÌNH MÁY ĐIỀU HÒA / TỦ LẠNH",
                      fontsize=13, fontweight="bold", color=style.PRIMARY, pad=14)

        evap = (1.0, 1.0, 3.0, 1.6)   # dàn lạnh (bay hơi) - trong phòng
        comp = (7.0, 1.0, 2.2, 1.6)   # máy nén
        cond = (7.0, 5.0, 3.0, 1.6)   # dàn nóng (ngưng tụ) - ngoài trời
        valve = (1.0, 5.0, 2.2, 1.6)  # van tiết lưu

        style.draw_labeled_box(ax, evap[:2], evap[2], evap[3], "DÀN LẠNH\n(bay hơi)", fill="#EAF2F8",
                                 edge=style.PRIMARY, bold=True)
        style.draw_labeled_box(ax, comp[:2], comp[2], comp[3], "MÁY NÉN", fill=style.GREY_FILL,
                                 edge=style.PRIMARY, bold=True)
        style.draw_labeled_box(ax, cond[:2], cond[2], cond[3], "DÀN NÓNG\n(ngưng tụ)", fill="#FDEBD0",
                                 edge=style.PRIMARY, bold=True)
        style.draw_labeled_box(ax, valve[:2], valve[2], valve[3], "VAN TIẾT LƯU", fill=style.GREY_FILL,
                                 edge=style.PRIMARY, bold=True)

        # Chu trình môi chất (chiều kim đồng hồ)
        style.draw_arrow_label(ax, (evap[0] + evap[2], evap[1] + evap[3] / 2), (comp[0], comp[1] + comp[3] / 2),
                                 label="hơi, áp suất thấp", label_offset=(0, 0.35))
        style.draw_arrow_label(ax, (comp[0] + comp[2] / 2, comp[1] + comp[3]), (cond[0] + cond[2] / 2, cond[1]),
                                 label="hơi, áp suất cao\nnhiệt độ cao", label_offset=(0.9, 0))
        style.draw_arrow_label(ax, (cond[0], cond[1] + cond[3] / 2), (valve[0] + valve[2], valve[1] + valve[3] / 2),
                                 label="lỏng, áp suất cao", label_offset=(0, 0.35))
        style.draw_arrow_label(ax, (valve[0] + valve[2] / 2, valve[1]), (evap[0] + evap[2] / 2, evap[1] + evap[3]),
                                 label="lỏng, áp suất thấp", label_offset=(-1.0, 0))

        # Thu nhiệt / tỏa nhiệt với môi trường
        style.draw_arrow_label(ax, (evap[0] - 1.4, evap[1] + evap[3] / 2 - 0.5), (evap[0], evap[1] + evap[3] / 2 - 0.5),
                                 label=None, color="#2E86C1")
        ax.text(evap[0] - 1.9, evap[1] + evap[3] / 2 - 0.5, "Không khí\ntrong phòng\n(thu nhiệt)",
                 fontsize=9, color="#2E86C1", ha="center", va="center")

        style.draw_arrow_label(ax, (cond[0] + cond[2], cond[1] + cond[3] / 2 + 0.5),
                                 (cond[0] + cond[2] + 1.4, cond[1] + cond[3] / 2 + 0.5),
                                 label=None, color="#C0392B")
        ax.text(cond[0] + cond[2] + 1.9, cond[1] + cond[3] / 2 + 0.5, "Không khí\nngoài trời\n(tỏa nhiệt)",
                 fontsize=9, color="#C0392B", ha="center", va="center")

        ax.set_xlim(-1.5, 11.5)
        ax.set_ylim(0, 8)
        style.save_figure(fig, str(OUT_DIR / "so_do_chu_trinh_dieu_hoa.png"))


if __name__ == "__main__":
    draw_apparatus_diagram()
    draw_temperature_time_graph()
    draw_ac_cycle_diagram()
    print("Đã ghi 3 ảnh minh họa vào:", OUT_DIR)
