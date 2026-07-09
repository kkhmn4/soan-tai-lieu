"""Sinh prompt cho NotebookLM — 2 bộ Slide tách biệt (Giáo viên + Phiếu học
tập), thay cơ chế "1 Slide + N+2 Infographic" trước đây (xem
`skills/gems_physics_skill.md` mục 4.2, v9.5.0).

Nguồn dữ liệu: đọc THẲNG `{slug}_worksheet_data.json` (ghi bởi
`gems.generation.stages.write_worksheet_json`) qua Pydantic, KHÔNG regex-parse
lại `{slug}_phieu_hoc_tap.md` đã render như bản cũ — cách cũ từng có bug thật
không bị phát hiện do thiếu test coverage (`_NHIEM_VU_RE` không khớp bất kỳ
nhiệm vụ nào suốt nhiều đợt). Đọc JSON có cấu trúc loại bỏ hoàn toàn rủi ro đó.

Danh sách slide dựng theo dạng "SLIDE N: ..." đánh số tường minh (không phải
mô tả outline rời rạc) — kỹ thuật đã kiểm chứng thực tế qua 7 vòng thử ở đợt
soạn Bài 28 (Vật Lý 10, one-off): giảm mạnh rủi ro AI tự gộp 2 nội dung vào 1
slide hoặc bỏ sót slide so với yêu cầu.
"""
from __future__ import annotations

import glob
import re
from dataclasses import dataclass, field
from pathlib import Path

from gems.config.loader import Identity
from gems.models.worksheet import LessonWorksheet

_GV_RE = re.compile(r"\*?Giáo viên thực hiện:\*?\s*([^\n\r]+)")
_TRUONG_PHAI_RE = re.compile(r"\*?Trường phái thiết kế:\*?\s*([^\n\r]+)")
_FONT_RE = re.compile(r"\*?Phông chữ chủ đạo:\*?\s*([^\n\r]+)")
_RULES_BLOCK_RE = re.compile(r"##\s*QUY TẮC THIẾT KẾ BẮT BUỘC(.*?)(?:##|---)", re.DOTALL)

_TASK_TYPE_VI = {
    "Assertion Reasoning": "Nhận định & Lý do",
    "Matching Matrix": "Ghép nối đa biến",
    "Bug Buster": "Tìm và sửa lỗi vật lý",
    "Algorithmic Ordering": "Sắp xếp tiến trình",
    "Visual Cloze Test": "Điền khuyết trực quan",
}


@dataclass
class SlideGuideInfo:
    gv: str
    truong_phai: str
    font: str
    rules: list[str] = field(default_factory=list)


def parse_slide_guide_for_prompt(guide_path: Path | None, identity: Identity) -> SlideGuideInfo:
    info = SlideGuideInfo(gv=identity.teacher_name, truong_phai=identity.brand_label, font=identity.default_font)
    if not guide_path or not Path(guide_path).exists():
        return info
    content = Path(guide_path).read_text(encoding="utf-8")

    if m := _GV_RE.search(content):
        info.gv = m.group(1).strip().replace("*", "")
    if m := _TRUONG_PHAI_RE.search(content):
        info.truong_phai = m.group(1).strip().replace("*", "")
    if m := _FONT_RE.search(content):
        info.font = m.group(1).strip().replace("*", "")

    if m := _RULES_BLOCK_RE.search(content):
        for line in m.group(1).strip().split("\n"):
            line = line.strip()
            if line.startswith(("-", "*")) or (line[:1].isdigit() and ". " in line[:5]):
                cleaned = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
                if cleaned:
                    info.rules.append(cleaned)
    return info


def load_worksheet_data(md_dir: Path) -> LessonWorksheet | None:
    """Đọc `worksheet_data.json` (ghi bởi `stages.write_worksheet_json`) — nguồn
    dữ liệu CHÍNH để dựng danh sách slide, thay cho regex-parse Markdown."""
    data_path = md_dir / "worksheet_data.json"
    if not data_path.exists():
        return None
    return LessonWorksheet.model_validate_json(data_path.read_text(encoding="utf-8"))


_IMAGERY_RULES = """   - **Ảnh minh họa phải chính xác khoa học, KHÔNG được hoạt hình:** cấm tuyệt đối phong cách
     hoạt hình/cartoon, 3D ảo, phóng đại phi thực tế hoặc "vẽ chơi". Ưu tiên tuyệt đối:
     (a) dùng lại nguyên trạng các ảnh sơ đồ đã có sẵn trong PHT nguồn (đường dẫn `ready/hinh_anh/...`)
     thay vì tự vẽ lại; nếu phải vẽ mới, chỉ vẽ dạng sơ đồ kỹ thuật đường nét (line-art) có nhãn/mũi
     tên như hình vẽ trong sách giáo khoa Vật Lý — tỉ lệ hợp lý, đúng bản chất vật lý, không thêm
     chi tiết trang trí không liên quan.
   - Mọi chữ/nhãn/chú thích xuất hiện trên ảnh minh họa phải bằng tiếng Việt.
   - **Ảnh minh họa giữa Slide Giáo viên và Slide Phiếu học tập phải giống hệt nhau về bố cục/chi
     tiết/nhãn chữ, chỉ khác màu sắc** (màu vs. trắng-đen-xám) — không để 2 lần sinh ảnh độc lập ra
     2 kết quả khác nhau cho cùng 1 nội dung."""

_BOX_STYLE_RULE = """   - **Khung/hộp (hộp ghi nhớ, hộp gợi ý, khung nhiệm vụ):** viền mảnh, bo góc nhẹ, không đổ bóng
     nặng, không dùng gradient sặc sỡ — phong cách nghiêm túc như sách giáo khoa/tài liệu khoa học,
     không phải slide quảng cáo hay poster sự kiện. Mỗi LOẠI slide (Nhiệm vụ/Đáp án/Kiến thức trọng
     tâm/Đọc mở rộng/Mục lục/Phân đoạn) dùng đúng 1 kiểu khung/màu/vị trí cố định xuyên suốt cả deck
     — không đổi kiểu giữa chừng."""

_ANTHROPIC_THEME_RULE = """   - **Tông màu chủ đạo (thương hiệu Anthropic, CHỈ áp dụng cho Slide Giáo viên):** Dark `#141413`
     cho tiêu đề/chữ chính, Light `#FAF9F5` cho nền — KHÁC với Primary `#1F4E79` chỉ dùng trong
     PHT/KHBD/Bài tập về nhà bản Word (có chủ đích, không phải nhầm lẫn).
   - **Tông màu nhấn:** luân phiên Orange `#D97757` (nhấn chính), Blue `#6A9BCC`, Green `#788C5D`
     cho khung/hình dạng/icon không phải khối chữ lớn — tạo điểm nhấn tinh tế, không sặc sỡ.
   - **Phông chữ (thương hiệu Anthropic):** tiêu đề dùng **Poppins** (dự phòng Arial), thân bài dùng
     **Lora** (dự phòng Georgia) — không dùng Times New Roman (đó là font riêng của bản Word)."""

_MASTER_SLIDE_RULE = """### MASTER SLIDE — KHUÔN MẪU NỀN TẢNG DÙNG CHUNG CHO CẢ 2 BỘ SLIDE (BẮT BUỘC)
Slide Giáo viên và Slide Phiếu học tập PHẢI được dựng như 2 bản phối màu khác nhau của CÙNG 1 bộ khuôn
mẫu (master slide): cùng 1 hệ thống phân cấp tiêu đề (vị trí, kiểu chữ, thứ tự to nhỏ), cùng 1 kiểu bố
cục cho từng loại slide (Nhiệm vụ, Đáp án, Kiến thức trọng tâm, Đọc mở rộng, Mục lục, Phân đoạn), cùng
1 vị trí số trang, cùng 1 kiểu khung ảnh minh họa — CHỈ khác nhau ở bảng màu (Slide Giáo viên: màu sắc
tươi sáng; Slide Phiếu học tập: nền trắng, ảnh trắng/đen/xám) và ở việc có/không hiển thị đáp án."""

_PAGE_NUMBER_RULE = """   - **Số trang (BẮT BUỘC 100%, KHÔNG ĐƯỢC BỎ SÓT DÙ CHỈ 1 SLIDE — kể cả slide bìa):** mọi slide
     đều PHẢI có số trang ở GÓC DƯỚI BÊN PHẢI, định dạng "Trang X/Y", cỡ chữ CỐ ĐỊNH 16pt, màu tương
     phản rõ với nền, vị trí giống hệt nhau trên mọi slide. Nếu công cụ tự thêm logo/watermark ở góc
     dưới bên phải, đặt số trang lệch sang bên trái ngay cạnh logo đó để không chồng chữ lên nhau.
     Luôn chừa vùng trống ở góc dưới bên phải, không đặt khung nội dung nào lấn sát mép đó."""

_NO_ENGLISH_RULE = """   - **CẤM TUYỆT ĐỐI mọi chữ tiếng Anh ở BẤT KỲ ĐÂU** — kể cả nhãn/chú thích/mũi tên bên TRONG hình
     vẽ minh họa, dòng chữ phụ/tagline trang trí, VÀ tên nhãn của các khung/hộp nội dung (ví dụ đúng:
     "ĐÁP ÁN", "NHIỆM VỤ", "KIẾN THỨC TRỌNG TÂM" — TUYỆT ĐỐI không dùng nhãn kiểu "Answer Frame",
     "Task Box"). Trước khi xuất mỗi slide/ảnh, tự kiểm tra lại toàn bộ chữ có phải tiếng Việt 100%."""

_NO_PLACEHOLDER_RULE = """   - **Không dùng dấu ngoặc vuông `[...]` hay bất kỳ ký hiệu placeholder nào trong nội dung hiển thị
     thật trên slide** — các đoạn trong dấu ngoặc kép ở outline bên dưới là NỘI DUNG THẬT cần chép
     nguyên văn lên slide, không phải placeholder cần thay thế; không được tự thêm dấu ngoặc vuông
     bao quanh khi hiển thị."""

_NO_MERGE_RULE = """   - **TUYỆT ĐỐI KHÔNG gộp khung "Nhiệm vụ" và khung "Đáp án" vào chung 1 slide** (dù đặt cạnh nhau
     hay trên-dưới) — MỌI cặp Nhiệm vụ/Đáp án, không có ngoại lệ nào (kể cả Luyện tập/Vận dụng), PHẢI
     là 2 SLIDE HOÀN TOÀN TÁCH BIỆT nối tiếp nhau."""

_ANSWER_LEAK_RULE = """   - **Không lộ đáp án qua chú thích ảnh minh họa:** ở các slide "Kiến thức trọng tâm (điền khuyết)",
     ảnh minh họa đi kèm KHÔNG được có dòng chữ chú thích/kết luận hoàn chỉnh trùng với đáp án của chỗ
     trống trên cùng slide đó — ảnh chỉ vẽ hình + nhãn đại lượng cơ bản, không viết câu kết luận."""

_VERBATIM_RULE = """   - **Chép NGUYÊN VĂN, không diễn đạt lại, không rút gọn, không làm rớt số liệu:** với mọi đoạn
     văn/câu hỏi/hướng dẫn được trích dẫn trong dấu ngoặc kép ở outline bên dưới — copy chính xác
     từng chữ, từng con số. Sau khi soạn xong mỗi slide, đối chiếu lại với đoạn trích dẫn gốc."""


def _numbering_rule(count_hint: str) -> str:
    return f"""   - **Danh sách "SLIDE N:" bên dưới là DUY NHẤT và ĐẦY ĐỦ** — mỗi dòng "SLIDE N:" tương ứng ĐÚNG 1
     slide, không được gộp 2 dòng thành 1 slide hay tách 1 dòng thành 2 slide. Tổng cộng có đúng
     {count_hint} slide. Trước khi hoàn thành, đếm lại số slide đã tạo để xác nhận khớp."""


def _build_slide_items(worksheet: LessonWorksheet, guide: SlideGuideInfo, *, teacher: bool) -> list[str]:
    """Trả về danh sách mô tả nội dung slide (1 phần tử = 1 slide), theo đúng
    thứ tự xuất hiện trên deck. `teacher=True` sinh outline cho Slide Giáo
    viên (tách Nhiệm vụ/Đáp án, có mục lục + phân đoạn); `teacher=False` sinh
    outline cho Slide Phiếu học tập (1 slide/nhiệm vụ, không đáp án nào)."""
    items: list[str] = []

    if teacher:
        items.append(f'Bìa: "{worksheet.lesson_name.upper()}" — Giáo viên thực hiện: {guide.gv}.')
        items.append('Mục lục: liệt kê đúng 3 mục lớn theo thứ tự: "1. Hình thành kiến thức mới", '
                      '"2. Luyện tập", "3. Vận dụng".')
    else:
        items.append(f'Bìa: "{worksheet.lesson_name.upper()}" — 2 dòng để trống "Họ và tên học sinh: '
                      '......" và "Lớp: ......".')

    def _task_type_vi(task_type: str) -> str:
        return _TASK_TYPE_VI.get(task_type, task_type)

    # ---- Mục 1: Hình thành kiến thức mới ----
    if teacher:
        items.append('Phân đoạn — CHỈ tiêu đề in hoa "1. HÌNH THÀNH KIẾN THỨC MỚI" căn giữa + 1 ảnh '
                      'minh họa lớn tiêu biểu cho mục này. TUYỆT ĐỐI không thêm nội dung nào khác.')
    for unit in worksheet.knowledge_formation:
        for t in unit.tasks:
            label = f'Nhiệm vụ "{t.task_name}" ({_task_type_vi(t.task_type)}, mục {unit.unit_id})'
            if teacher:
                items.append(
                    f'Nhiệm vụ — {label}: CHỈ tên nhiệm vụ + đúng 3 ý "Hình thức: ...; Thời gian: '
                    f'...; Tài liệu: ..." lấy NGUYÊN VĂN từ: "{t.instructions}". KHÔNG in đề bài/câu '
                    'hỏi lên slide này.'
                )
                items.append(f'Đáp án — {label}: CHỈ đáp án/kết luận + ảnh minh họa. KHÔNG lặp lại '
                              'hướng dẫn thực hiện.')
            else:
                items.append(
                    f'{label}: tên nhiệm vụ + đúng 3 ý "Hình thức: ...; Thời gian: ...; Tài liệu: ..." '
                    f'lấy NGUYÊN VĂN từ: "{t.instructions}", rồi TOÀN BỘ nội dung câu hỏi/đề bài sau '
                    f'đây, chép NGUYÊN VĂN: "{t.content}" — chừa khoảng trống kẻ ngang bên dưới để '
                    'học sinh viết câu trả lời (độ dài tỉ lệ câu trả lời kỳ vọng). KHÔNG hiện đáp án.'
                )
        if teacher:
            items.append(
                f'Kiến thức trọng tâm (mục {unit.unit_id}, điền khuyết): dùng ĐÚNG NGUYÊN VĂN đoạn văn '
                f'đục lỗ sau, GIỮ NGUYÊN các số thứ tự (1)(2)... CHƯA điền: "{unit.core_theory.summary_cloze}"'
            )
            items.append(
                f'Kiến thức trọng tâm (mục {unit.unit_id}, đáp án đầy đủ): như slide trước nhưng điền '
                f'đủ chỗ trống, dùng các từ khóa theo đúng thứ tự: {", ".join(unit.core_theory.key_words)}.'
            )
        else:
            items.append(
                f'Kiến thức trọng tâm (mục {unit.unit_id}, CHỈ dạng điền khuyết, KHÔNG điền sẵn, KHÔNG '
                f'có slide đáp án đi kèm): dùng ĐÚNG NGUYÊN VĂN đoạn văn đục lỗ sau, giữ nguyên các chỗ '
                f'trống (1)(2)...: "{unit.core_theory.summary_cloze}". Ảnh minh họa đi kèm KHÔNG được '
                'ghi chú thích trùng với đáp án của chỗ trống.'
            )

    # ---- Mục 2: Luyện tập ----
    if teacher:
        items.append('Phân đoạn — CHỈ tiêu đề in hoa "2. LUYỆN TẬP" căn giữa + 1 ảnh minh họa lớn tiêu '
                      'biểu. TUYỆT ĐỐI không thêm nội dung nào khác.')
    for idx, pitem in enumerate(worksheet.practice_items, 1):
        label = f'Bài toán Luyện tập {idx} ({pitem.unit_name})'
        if teacher:
            items.append(
                f'Nhiệm vụ — {label}: CHỈ tên nhiệm vụ + đúng 3 ý "Hình thức: ...; Thời gian: ...; '
                f'Tài liệu: ..." lấy NGUYÊN VĂN từ: "{pitem.instructions}". KHÔNG in đề bài.'
            )
            items.append(f'Đáp án — {label}: CHỈ đáp án/lời giải. KHÔNG lặp lại hướng dẫn.')
        else:
            items.append(
                f'{label}: tên nhiệm vụ + đúng 3 ý "Hình thức: ...; Thời gian: ...; Tài liệu: ..." lấy '
                f'NGUYÊN VĂN từ: "{pitem.instructions}", rồi TOÀN BỘ đề bài sau, chép NGUYÊN VĂN không '
                f'rút gọn số liệu: "{pitem.scenario}" — chừa khoảng trống trình bày lời giải. KHÔNG '
                'hiện đáp án.'
            )

    # ---- Mục 3: Vận dụng ----
    if teacher:
        items.append('Phân đoạn — CHỈ tiêu đề in hoa "3. VẬN DỤNG" căn giữa + 1 ảnh minh họa lớn tiêu '
                      'biểu. TUYỆT ĐỐI không thêm nội dung nào khác.')
    for t in worksheet.application_tasks:
        label = f'Nhiệm vụ Vận dụng "{t.task_name}" ({_task_type_vi(t.task_type)})'
        if teacher:
            items.append(
                f'Nhiệm vụ — {label}: CHỈ tên nhiệm vụ + đúng 3 ý NGUYÊN VĂN từ: "{t.instructions}". '
                'KHÔNG in đề bài.'
            )
            items.append(f'Đáp án — {label}: CHỈ đáp án/kết luận. KHÔNG lặp lại hướng dẫn.')
        else:
            items.append(
                f'{label}: đúng 3 ý NGUYÊN VĂN từ: "{t.instructions}", rồi TOÀN BỘ đề bài, chép NGUYÊN '
                f'VĂN: "{t.content}" — chừa khoảng trống viết câu trả lời. KHÔNG hiện đáp án.'
            )
    for reading in worksheet.application_readings:
        items.append(
            f'Đọc mở rộng — {reading.unit_name} (đọc thêm, KHÔNG phải nhiệm vụ, KHÔNG có khung Nhiệm '
            f'vụ/Đáp án nào): dùng ĐÚNG NGUYÊN VĂN đoạn văn sau, không diễn đạt lại, không rút gọn: '
            f'"{reading.reading_content}"'
        )

    # ---- Kết bài ----
    if teacher:
        items.append('Kết bài — sơ đồ tư duy tổng hợp: khối trung tâm là tên bài học, các nhánh điền '
                      'đầy đủ những từ khóa/công thức cốt lõi đã học.')
    else:
        items.append('Kết bài — sơ đồ tư duy: CHỈ khung sơ đồ với khối trung tâm là tên bài học và các '
                      'nhánh để TRỐNG, KHÔNG điền sẵn bất kỳ nội dung nào.')

    return items


def _render_slide_outline(items: list[str]) -> tuple[str, int]:
    lines = [f"SLIDE {i}: {desc}" for i, desc in enumerate(items, 1)]
    return "\n\n".join(lines), len(items)


def _build_teacher_slide_prompt(lesson_slug: str, lesson_title: str, worksheet: LessonWorksheet,
                                  guide: SlideGuideInfo) -> tuple[str, int]:
    items = _build_slide_items(worksheet, guide, teacher=True)
    outline, count = _render_slide_outline(items)
    rules_str = ""
    if guide.rules:
        rules_str = "\n\n**Quy tắc thiết kế bắt buộc bổ sung trích xuất từ file hướng dẫn slide:**\n"
        rules_str += "".join(f"   - {r}\n" for r in guide.rules)

    prompt = f"""# NOTEBOOKLM PROMPT TẠO SLIDE GIÁO VIÊN - {lesson_title.upper()}
> **HƯỚNG DẪN:** Sao chép toàn bộ nội dung dưới đây và dán vào khung chat NotebookLM sau khi đã tải
> các nguồn: `{lesson_slug}_dac_ta_gems.md`, `{lesson_slug}_ke_hoach_bai_day.md`,
> `{lesson_slug}_phieu_hoc_tap.md`, `{lesson_slug}_huong_dan_slide.md`.

---

## NỘI DUNG PROMPT NẠP CHO NOTEBOOKLM (SLIDE GIÁO VIÊN TRÌNH CHIẾU CẢ LỚP)

Bạn là một trợ lý thiết kế bài giảng chuyên nghiệp theo hệ thống tiêu chuẩn {guide.truong_phai}. Hãy
dựa trên danh sách slide đầy đủ bên dưới (đã khớp với các tài liệu nguồn đã tải lên, đặc biệt là
`{lesson_slug}_phieu_hoc_tap.md` và `{lesson_slug}_ke_hoach_bai_day.md`) để dựng SLIDE GIÁO VIÊN — bộ
slide ĐẦY ĐỦ, chi tiết, dùng để trình chiếu và hướng dẫn cả lớp trong giờ học.

**3 YÊU CẦU KỸ THUẬT BẮT BUỘC PHẢI NHỚ TỪ ĐẦU ĐẾN CUỐI:**
(1) TẤT CẢ {count} slide đều phải có số trang "Trang X/{count}" ở góc dưới bên phải, kể cả slide 1.
(2) Mỗi slide phân đoạn CHỈ được có tiêu đề + ảnh, không thêm nội dung nào khác.
(3) Không dùng dấu ngoặc vuông hay ký hiệu placeholder nào trong nội dung hiển thị.

### QUY TẮC BẮT BUỘC VỀ NỘI DUNG HIỂN THỊ (QUAN TRỌNG NHẤT)
{_NO_MERGE_RULE}
{_numbering_rule(str(count))}
{_NO_ENGLISH_RULE}
{_VERBATIM_RULE}
{_NO_PLACEHOLDER_RULE}

{_MASTER_SLIDE_RULE}

### YÊU CẦU THIẾT KẾ VÀ GIAO DIỆN
   - **Cỡ chữ CỐ ĐỊNH, BẮT BUỘC:** tiêu đề slide LUÔN LUÔN đúng 32pt đậm; nội dung/thân bài LUÔN
     LUÔN đúng 28pt. TUYỆT ĐỐI KHÔNG dùng cỡ chữ khác hay tự thu nhỏ chữ để nhồi nội dung dài — thà
     viết súc tích hơn. Dùng 1 bộ font nhất quán cho toàn bộ deck.
   - **Màu sắc tươi mới, hài hòa, giàu năng lượng**, đồ họa đẹp/thu hút, phù hợp trình chiếu.
{_ANTHROPIC_THEME_RULE}
{_BOX_STYLE_RULE}
{_PAGE_NUMBER_RULE}
   - **MỌI slide, không trừ slide nào** (kể cả Đáp án/Kiến thức trọng tâm/Mục lục), PHẢI có ít nhất 1
     ảnh minh họa trực quan chính xác khoa học liên quan trực tiếp nội dung slide đó — ưu tiên tuyệt
     đối ảnh minh họa kiến thức, không dùng ảnh trang trí chung chung.
{_IMAGERY_RULES}
   - **Bố cục:** khoảng trống tối thiểu 30-35%, không nhồi nhét chữ.
{rules_str}
## DANH SÁCH SLIDE CHÍNH XÁC — ĐÚNG {count} SLIDE, ĐÚNG THỨ TỰ NÀY

{outline}

**TRƯỚC KHI HOÀN THÀNH:** đếm lại tổng số slide — phải đúng bằng {count}.
""".strip() + "\n"
    return prompt, count


def _build_student_slide_prompt(lesson_slug: str, lesson_title: str, worksheet: LessonWorksheet,
                                  guide: SlideGuideInfo) -> tuple[str, int]:
    items = _build_slide_items(worksheet, guide, teacher=False)
    outline, count = _render_slide_outline(items)

    prompt = f"""# NOTEBOOKLM PROMPT TẠO SLIDE PHIẾU HỌC TẬP HỌC SINH - {lesson_title.upper()}
> **HƯỚNG DẪN:** Sao chép toàn bộ nội dung dưới đây và dán vào khung chat NotebookLM sau khi đã tải
> các nguồn: `{lesson_slug}_dac_ta_gems.md`, `{lesson_slug}_ke_hoach_bai_day.md`,
> `{lesson_slug}_phieu_hoc_tap.md`, `{lesson_slug}_huong_dan_slide.md`.

---

## NỘI DUNG PROMPT NẠP CHO NOTEBOOKLM (SLIDE PHIẾU HỌC TẬP — BẢN CHIẾU SỐ HÓA CỦA PHT GIẤY)

Bạn là một trợ lý thiết kế học liệu chuyên nghiệp theo hệ thống tiêu chuẩn {guide.truong_phai}. Hãy
dựa trên danh sách slide đầy đủ bên dưới (khớp với `{lesson_slug}_phieu_hoc_tap.md` đã tải lên làm
source) để dựng SLIDE PHIẾU HỌC TẬP — bản chiếu số hóa của chính PHT giấy, dùng để học sinh vừa xem
slide vừa viết câu trả lời TRỰC TIẾP lên slide (nếu dùng bảng tương tác) hoặc đối chiếu với PHT giấy.

**2 YÊU CẦU KỸ THUẬT BẮT BUỘC PHẢI NHỚ TỪ ĐẦU ĐẾN CUỐI:**
(1) TẤT CẢ {count} slide đều phải có số trang "Trang X/{count}" ở góc dưới bên phải, kể cả slide bìa.
(2) Không dùng dấu ngoặc vuông hay ký hiệu placeholder nào trong nội dung hiển thị.

### QUY TẮC BẮT BUỘC VỀ NỘI DUNG HIỂN THỊ (QUAN TRỌNG NHẤT)
1. **TUYỆT ĐỐI KHÔNG tạo bất kỳ slide "Đáp án" nào trong toàn bộ bộ slide này** — bộ slide này CHỈ
   gồm slide câu hỏi/nhiệm vụ, không có slide nào hiện đáp án, kết luận, hay lời giải.
2. **Mỗi slide Nhiệm vụ hiển thị ĐẦY ĐỦ: tên nhiệm vụ + 3 ý Hình thức/Thời gian/Tài liệu + TOÀN BỘ
   câu hỏi/đề bài NGUYÊN VĂN** — và PHẢI có khoảng trống (dòng kẻ ngang mảnh, màu xám nhạt) ngay dưới
   mỗi câu hỏi để học sinh viết câu trả lời trực tiếp, độ dài tỉ lệ câu trả lời kỳ vọng.
{_ANSWER_LEAK_RULE}
{_numbering_rule(str(count))}
{_NO_ENGLISH_RULE}
{_VERBATIM_RULE}
{_NO_PLACEHOLDER_RULE}

{_MASTER_SLIDE_RULE}

### YÊU CẦU THIẾT KẾ VÀ GIAO DIỆN — CÙNG MASTER VỚI SLIDE GIÁO VIÊN, KHÁC BẢNG MÀU
   - **Nền TRẮNG tuyệt đối trên MỌI slide** (kể cả slide bìa) — không dùng nền tối, không màu sặc sỡ.
   - **Ảnh minh họa CHỈ dùng tông TRẮNG/ĐEN/XÁM** — cấm mọi màu sắc khác trong hình vẽ minh họa.
   - **Cỡ chữ CỐ ĐỊNH:** tiêu đề slide LUÔN LUÔN đúng 24pt đậm; nội dung LUÔN LUÔN đúng 20pt. TUYỆT
     ĐỐI KHÔNG dùng cỡ chữ khác. Chữ màu đen hoặc xám đậm.
   - Khung/hộp viền mỏng màu xám, không tô nền màu, không đổ bóng — phong cách tối giản như trang
     giấy in. Vị trí khung giữ ĐÚNG bố cục master dùng chung với Slide Giáo viên.
{_BOX_STYLE_RULE}
{_PAGE_NUMBER_RULE}
   - **MỌI slide, không trừ slide nào, PHẢI có ít nhất 1 ảnh minh họa khoa học chính xác** liên quan
     trực tiếp nội dung slide đó, đồng bộ bố cục với ảnh bên Slide Giáo viên (chỉ khác màu).
{_IMAGERY_RULES}

## DANH SÁCH SLIDE CHÍNH XÁC — ĐÚNG {count} SLIDE, ĐÚNG THỨ TỰ NÀY

{outline}

**TRƯỚC KHI HOÀN THÀNH:** đếm lại tổng số slide — phải đúng bằng {count}.
""".strip() + "\n"
    return prompt, count


def generate_notebooklm_prompt(output_dir: Path, lesson_slug: str, lesson_title: str,
                                identity: Identity) -> tuple[Path, Path, int, int]:
    """Sinh 2 file prompt (Slide Giáo viên + Slide Phiếu học tập) từ dữ liệu
    PHT thật (`worksheet_data.json`). Trả về
    (teacher_prompt_path, student_prompt_path, teacher_slide_count,
    student_slide_count) — 2 số đếm dùng để đối chiếu với số slide THẬT tải
    về sau này (`gems/notebooklm/pipeline.py`), phát hiện trường hợp
    NotebookLM cắt ngang giữa chừng (bài học từ đợt Bài 28: KHÔNG được tin số
    "Trang X/Y" tự ghi trên slide, phải tự đếm lại số slide thật)."""
    notebooklm_dir = output_dir / "notebooklm"
    notebooklm_dir.mkdir(parents=True, exist_ok=True)

    md_dir = output_dir / "md"
    guide_files = sorted(glob.glob(str(md_dir / "*_huong_dan_slide.md")))
    guide_path = Path(guide_files[0]) if guide_files else None
    guide_info = parse_slide_guide_for_prompt(guide_path, identity)

    worksheet = load_worksheet_data(md_dir)
    if worksheet is None:
        # Không có dữ liệu PHT có cấu trúc — không thể dựng outline slide đáng
        # tin cậy (xem docstring module). Trả về prompt rỗng có cảnh báo rõ,
        # thay vì sinh 1 prompt outline sai/thiếu mà không ai biết.
        empty = (
            f"# LỖI: KHÔNG TÌM THẤY {lesson_slug}_worksheet_data.json\n\n"
            "Cần chạy giai đoạn sinh Phiếu học tập (`generate`/`offline`/`compose`) trước khi chạy "
            "`notebooklm` — file `worksheet_data.json` được ghi cùng lúc với "
            f"`{lesson_slug}_phieu_hoc_tap.md`.\n"
        )
        teacher_path = notebooklm_dir / f"{lesson_slug}_notebooklm_slide_giao_vien_prompt.md"
        student_path = notebooklm_dir / f"{lesson_slug}_notebooklm_slide_phieu_hoc_tap_prompt.md"
        teacher_path.write_text(empty, encoding="utf-8")
        student_path.write_text(empty, encoding="utf-8")
        return teacher_path, student_path, 0, 0

    teacher_prompt, teacher_count = _build_teacher_slide_prompt(lesson_slug, lesson_title, worksheet, guide_info)
    student_prompt, student_count = _build_student_slide_prompt(lesson_slug, lesson_title, worksheet, guide_info)

    teacher_path = notebooklm_dir / f"{lesson_slug}_notebooklm_slide_giao_vien_prompt.md"
    student_path = notebooklm_dir / f"{lesson_slug}_notebooklm_slide_phieu_hoc_tap_prompt.md"
    teacher_path.write_text(teacher_prompt, encoding="utf-8")
    student_path.write_text(student_prompt, encoding="utf-8")

    return teacher_path, student_path, teacher_count, student_count
