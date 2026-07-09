"""Bảng màu & font dùng chung cho mọi loại tài liệu Word GEMS."""
from docx.shared import Pt, RGBColor


class VietColors:
    PRIMARY = RGBColor(0x1F, 0x4E, 0x79)        # #1F4E79 — tiêu đề/heading cấp 1
    DARK = RGBColor(0x00, 0x00, 0x00)           # #000000 — nội dung thân bài
    GRAY = RGBColor(0x66, 0x66, 0x66)           # #666666
    LIGHT_GRAY = RGBColor(0xD9, 0xD9, 0xD9)     # #D9D9D9 — nền header bảng
    BORDER_GRAY = RGBColor(0xBF, 0xBF, 0xBF)    # #BFBFBF — viền/chấm dòng

    PRIMARY_HEX = "1F4E79"
    LIGHT_GRAY_HEX = "D9D9D9"
    WHITE_HEX = "FFFFFF"
    BORDER_GRAY_HEX = "BFBFBF"


class VietFonts:
    BODY = "Times New Roman"
    HEADER = "Times New Roman"

    SIZE_TITLE = Pt(16)
    SIZE_H1 = Pt(14)
    SIZE_H2 = Pt(13)
    SIZE_H3 = Pt(13)
    SIZE_BODY = Pt(13)
    SIZE_TABLE = Pt(12)
    SIZE_INFO = Pt(11)
    SIZE_TINY = Pt(9)
