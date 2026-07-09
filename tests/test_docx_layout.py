import pytest

from gems.docx_export.layout import LAYOUTS, get_layout


def test_pht_layout():
    layout = get_layout("pht")
    assert (layout.top_margin_cm, layout.bottom_margin_cm, layout.left_margin_cm, layout.right_margin_cm) == (2.0, 2.0, 2.0, 2.0)
    assert layout.content_width_cm == pytest.approx(17.0)


def test_khbd_layout():
    layout = get_layout("khbd")
    assert (layout.top_margin_cm, layout.bottom_margin_cm, layout.left_margin_cm, layout.right_margin_cm) == (2.0, 2.0, 3.0, 2.0)
    assert layout.content_width_cm == pytest.approx(16.0)


def test_homework_layout():
    layout = get_layout("homework")
    assert (layout.top_margin_cm, layout.bottom_margin_cm, layout.left_margin_cm, layout.right_margin_cm) == (1.5, 1.5, 2.0, 2.0)
    assert layout.content_width_cm == pytest.approx(17.0)


def test_unknown_doc_type_raises():
    with pytest.raises(ValueError):
        get_layout("unknown")


def test_all_layouts_registered():
    assert set(LAYOUTS.keys()) == {"pht", "khbd", "homework"}
