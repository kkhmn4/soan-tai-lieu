"""Chuyển LaTeX/ký hiệu toán-lý thô sang Unicode sạch cho Word.

Đây là phần có mật độ bug lịch sử cao nhất trong toàn dự án cũ (rất nhiều
commit "fix regex" trong changelog) nên được tách thành pure function,
không phụ thuộc python-docx, để test độc lập dễ dàng.
"""
from __future__ import annotations

import re

# Bảng ký hiệu Hy Lạp / toán tử — áp dụng tuần tự theo thứ tự khai báo.
# Lưu ý: các mục "\Delta t"/"\Delta U" và mọi biến thể \circ có tiền tố
# (^{\circ}, ^\circ, \text{}^{\circ}C...) không bao giờ khớp được vì mục
# \Delta / \circ (đứng trước trong dict) đã tiêu thụ chuỗi con trước đó —
# giữ lại các mục này chỉ để tài liệu hoá ý định, hành vi thật do
# _SUPERSCRIPT_RE + \text{...} strip ở cuối đảm nhiệm.
_SYMBOL_MAP: dict[str, str] = {
    r"\Delta": "Δ", r"\delta": "δ",
    r"\omega": "ω", r"\Omega": "Ω",
    r"\varphi": "φ", r"\phi": "φ",
    r"\pi": "π",
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ",
    r"\lambda": "λ", r"\mu": "μ", r"\theta": "θ",
    r"\rho": "ρ", r"\tau": "τ",
    r"\approx": "≈", r"\neq": "≠", r"\le": "≤", r"\ge": "≥",
    r"\times": "×", r"\cdot": "·", r"\pm": "±",
    r"\circ": "°",
    r"\infty": "∞", r"\to": "→",
    r"\text{ J}": " J", r"\text{ J/kg.K}": " J/kg.K",
    r"\text{ kg}": " kg", r"\text{ g}": " g", r"\text{ m}": " m",
    r"\text{ s}": " s", r"\text{ W}": " W", r"\text{ K}": " K",
    r"\text{ kJ}": " kJ", r"\text{ MJ}": " MJ",
}

_SUPERSCRIPT_MAP = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "-": "⁻", "+": "⁺", "=": "⁼", "(": "⁽", ")": "⁾",
    "n": "ⁿ", "x": "ˣ", "i": "ⁱ",
}

_BRACED_SUPERSCRIPT_RE = re.compile(r"\^\{([^}]+)\}")
_BARE_SUPERSCRIPT_RE = re.compile(r"\^([0-9a-zA-Z\-\+\=]+)")
_TEXT_MACRO_RE = re.compile(r"\\text\{([^}]+)\}")

# "^\circ"/"^{\circ}" phải tiêu thụ luôn dấu "^" — nếu không, vòng lặp
# _SYMBOL_MAP phía dưới chỉ thay "\circ" -> "°" và để sót dấu "^" trần
# (superscript regex không khớp vì "°" không phải alnum), ra kết quả lỗi
# kiểu "25^°C" thay vì "25°C".
_CARET_DEGREE_RE = re.compile(r"\^\{?\\circ\}?")

# alnum/đóng-ngoặc, dấu *, rồi chữ cái Unicode (Latin/Hy Lạp...) hoặc mở ngoặc
# => "·" (nhân chấm). Bản gốc dùng char-class [a-zA-Z\(\Delta] — bên trong
# [...] thì \D bị regex hiểu là "ký tự không phải số" (class shorthand),
# khiến vế phải khớp gần như mọi ký tự không phải số một cách ngoài ý muốn.
# Ở đây sửa đúng theo ý định: chữ cái Unicode thật hoặc dấu mở ngoặc.
_MULT_DIGIT_RE = re.compile(r"(\d)\s*\*\s*(\d)")
_MULT_LETTER_RE = re.compile(r"([a-zA-Z0-9\)])\s*\*\s*((?:[^\W\d_])|\()")


def _repl_superscript(match: re.Match) -> str:
    chars = match.group(1)
    return "".join(_SUPERSCRIPT_MAP.get(c, c) for c in chars)


def clean_latex(text: str) -> str:
    """Dịch macro LaTeX vật lý-toán học thô sang glyph Unicode sạch."""
    if not text:
        return ""

    # Khôi phục ký tự tab thật (bị hỏng do cp1252 khi gõ \text{...}) về lại "\t".
    text = text.replace("\t", "\\t")

    text = _CARET_DEGREE_RE.sub("°", text)

    for key, val in _SYMBOL_MAP.items():
        text = text.replace(key, val)

    text = _BRACED_SUPERSCRIPT_RE.sub(_repl_superscript, text)
    text = _BARE_SUPERSCRIPT_RE.sub(_repl_superscript, text)

    text = _MULT_DIGIT_RE.sub(r"\1 × \2", text)
    text = _MULT_LETTER_RE.sub(r"\1·\2", text)

    text = _TEXT_MACRO_RE.sub(r"\1", text)
    text = text.replace("$", "")
    return text


def smart_typography(text: str) -> str:
    """Chuyển nháy thẳng ' " thành nháy cong kiểu Việt/Anh chuẩn in ấn."""
    if not text:
        return ""
    text = re.sub(r'"([^"]*)"', r"“\1”", text)
    text = re.sub(r"'([^']*)'", r"‘\1’", text)
    text = re.sub(r"(\w)'(\w)", r"\1’\2", text)
    return text
