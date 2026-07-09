from gems.qa.markdown_lint import lint_markdown


def test_clean_content_has_no_issues():
    assert lint_markdown("Nội dung sạch, không lỗi gì cả.") == []


def test_detects_raw_bullet():
    issues = lint_markdown("• Mục thứ nhất\n• Mục thứ hai")
    assert len(issues) == 1
    assert "bullet thô" in issues[0]


def test_detects_raw_latex_symbols():
    issues = lint_markdown(r"Công thức \Delta U = A + Q chưa dịch")
    assert any("LaTeX" in i for i in issues)


def test_lesson_plan_missing_cv5512_keywords():
    issues = lint_markdown("Giáo án không có đủ từ khóa hoạt động.", is_lesson_plan=True)
    assert any("CV5512" in i or "từ khóa" in i for i in issues)


def test_lesson_plan_with_all_keywords_passes():
    content = (
        "c) Sản phẩm: Phiếu học tập\n"
        "Kĩ thuật dạy học tích cực: Chia sẻ nhóm đôi\n"
        "Năng lực số: 1.2\n"
        "Chuyển giao nhiệm vụ: ...\n"
        "Thực hiện nhiệm vụ: ...\n"
        "Báo cáo, thảo luận: ...\n"
        "Kết luận: ...\n"
    )
    assert lint_markdown(content, is_lesson_plan=True) == []


def test_lesson_plan_requires_product_technique_and_digital_competency():
    content = (
        "Chuyển giao nhiệm vụ: ...\nThực hiện nhiệm vụ: ...\n"
        "Báo cáo, thảo luận: ...\nKết luận: ...\n"
    )
    issues = lint_markdown(content, is_lesson_plan=True)
    assert any("Sản phẩm" in issue and "Kĩ thuật" in issue and "Năng lực số" in issue for issue in issues)


def test_non_lesson_plan_skips_cv5512_check():
    assert lint_markdown("Không có từ khóa gì cả", is_lesson_plan=False) == []
