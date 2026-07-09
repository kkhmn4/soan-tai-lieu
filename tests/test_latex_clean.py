from gems.docx_export.latex_clean import clean_latex, smart_typography


def test_greek_letters():
    # Chỉ "\Delta" được thay bằng "Δ" — khoảng trắng gốc giữa \Delta và t giữ nguyên.
    assert clean_latex(r"\Delta t = 5") == "Δ t = 5"
    assert clean_latex(r"\omega, \varphi, \pi") == "ω, φ, π"
    assert clean_latex(r"\alpha \beta \gamma \lambda \mu \theta \rho \tau") == "α β γ λ μ θ ρ τ"


def test_math_operators():
    assert clean_latex(r"a \approx b, c \neq d, e \le f, g \ge h") == "a ≈ b, c ≠ d, e ≤ f, g ≥ h"
    assert clean_latex(r"a \times b, a \cdot b, a \pm b") == "a × b, a · b, a ± b"


def test_degree_and_arrow():
    assert clean_latex(r"25^{\circ}C") == "25°C"
    assert clean_latex(r"25^\circ C") == "25° C"
    assert clean_latex(r"A \to B") == "A → B"
    assert clean_latex(r"\infty") == "∞"


def test_superscript_braced_and_bare():
    assert clean_latex(r"10^{-3}") == "10⁻³"
    assert clean_latex(r"10^6") == "10⁶"
    assert clean_latex(r"x^n") == "xⁿ"


def test_text_macro_unit_shortcuts_and_generic_strip():
    assert clean_latex(r"5\text{ kg}") == "5 kg"
    assert clean_latex(r"3\text{ J/kg.K}") == "3 J/kg.K"
    assert clean_latex(r"\text{ khối lượng}") == " khối lượng"


def test_multiplication_cleanup():
    assert clean_latex("5 * 3") == "5 × 3"
    assert clean_latex(r"m * c") == "m·c"
    assert clean_latex(r"m * \Delta t") == "m·Δ t"


def test_tab_roundtrip_workaround():
    # Ký tự tab thật (do lỗi encode cp1252 khi gõ \text{...}) phải quay lại thành "\t"
    assert clean_latex("Q\t= mc") == r"Q\t= mc"


def test_dollar_sign_and_empty():
    assert clean_latex("$Q = mc\\Delta t$") == "Q = mcΔ t"
    assert clean_latex("") == ""
    assert clean_latex(None) == ""


def test_smart_typography_quotes():
    assert smart_typography('Nói "xin chào" nhé') == "Nói “xin chào” nhé"
    assert smart_typography("don't") == "don’t"
    assert smart_typography("") == ""
