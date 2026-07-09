from gems.docx_export.markdown_ir import parse_markdown_blocks


def test_heading_levels_by_hash_count():
    blocks = parse_markdown_blocks(["## Tiêu đề lớn", "### Tiêu đề vừa", "#### Tiêu đề nhỏ"])
    assert [b.kind for b in blocks] == ["heading", "heading", "heading"]
    assert [b.level for b in blocks] == [1, 2, 3]
    assert blocks[0].text == "Tiêu đề lớn"


def test_single_hash_heading_maps_to_level_1():
    blocks = parse_markdown_blocks(["# Chỉ 1 dấu thăng"])
    assert blocks[0].kind == "heading"
    assert blocks[0].level == 1


def test_bullet_levels():
    blocks = parse_markdown_blocks(["- gạch đầu dòng cấp 1", "* cũng cấp 1", "+ cấp 2"])
    assert [b.level for b in blocks] == [1, 1, 2]
    assert all(b.kind == "bullet" for b in blocks)


def test_blockquote_strips_marker():
    blocks = parse_markdown_blocks(["> đoạn trích dẫn", ">không có khoảng trắng"])
    assert blocks[0].kind == "blockquote"
    assert blocks[0].text == "đoạn trích dẫn"
    assert blocks[1].text == "không có khoảng trắng"


def test_dot_line_token():
    blocks = parse_markdown_blocks(["[DOT_LINE_90]"])
    assert blocks[0].kind == "dotline"


def test_horizontal_rule_becomes_separator():
    blocks = parse_markdown_blocks(["---", "-----"])
    assert [b.kind for b in blocks] == ["separator", "separator"]


def test_blank_lines_are_skipped():
    blocks = parse_markdown_blocks(["", "  ", "Nội dung thật"])
    assert len(blocks) == 1
    assert blocks[0].kind == "body"


def test_pipe_table_parsed_with_separator_row():
    lines = [
        "| Cột 1 | Cột 2 |",
        "| :--- | :--- |",
        "| a | b |",
        "| c | d |",
    ]
    blocks = parse_markdown_blocks(lines)
    assert len(blocks) == 1
    table = blocks[0]
    assert table.kind == "table"
    assert table.table_headers == ["Cột 1", "Cột 2"]
    assert table.table_rows == [["a", "b"], ["c", "d"]]


def test_image_reference_stripped_and_resolved(tmp_path):
    img_dir = tmp_path / "ready" / "hinh_anh"
    img_dir.mkdir(parents=True)
    img_file = img_dir / "minh_hoa.png"
    img_file.write_bytes(b"\x89PNG\r\n")

    lines = ["Xem hình (ready/hinh_anh/minh_hoa.png) để hiểu rõ hơn"]
    blocks = parse_markdown_blocks(lines, image_search_dirs=[tmp_path])
    assert len(blocks) == 1
    assert blocks[0].image_path == img_file
    assert "ready/hinh_anh" not in blocks[0].text
    assert "Xem hình" in blocks[0].text


def test_missing_image_path_returns_none(tmp_path):
    lines = ["ready/hinh_anh/khong_ton_tai.png"]
    blocks = parse_markdown_blocks(lines, image_search_dirs=[tmp_path])
    assert blocks[0].image_path is None
