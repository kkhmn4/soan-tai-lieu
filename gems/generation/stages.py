"""6 bước sinh nội dung GEMS: gọi Gemini + ghi file Markdown nguồn.

Tách rõ 2 việc trước đây bị trộn lẫn trong 1 hàm khổng lồ của gems_agent.py
cũ: (1) gọi Gemini trả về đối tượng Pydantic, (2) ghi đối tượng đó ra
Markdown. Tách riêng giúp test được từng phần — offline fixtures có thể
cấp thẳng đối tượng Pydantic mẫu để test bước (2) mà không cần gọi API thật.
"""
from __future__ import annotations

import json
from pathlib import Path

from gems.config.loader import Identity, LessonSpec
from gems.generation.gemini_client import GeminiClient
from gems.models.architect import GEMSArchitect
from gems.models.homework import HomeworkContent
from gems.models.lesson_plan import LessonPlanContent
from gems.models.worksheet import LessonWorksheet
from gems.prompts import architect as architect_prompts
from gems.prompts import homework as homework_prompts
from gems.prompts import lesson_plan as lesson_plan_prompts
from gems.prompts import worksheet as worksheet_prompts

MODEL_ARCHITECT_DEFAULT = "gemini-2.5-pro"
MODEL_CONTENT_DEFAULT = "gemini-2.5-flash"


# ============================================================
#  GỌI GEMINI — TRẢ VỀ ĐỐI TƯỢNG PYDANTIC
# ============================================================
def analyze_yccd(client: GeminiClient, identity: Identity, lesson: LessonSpec, yccd_text: str) -> GEMSArchitect:
    system_instruction = architect_prompts.SYSTEM_INSTRUCTION.format(num_units=lesson.num_knowledge_units)
    prompt = architect_prompts.build_prompt(lesson.name, yccd_text)
    return client.generate_structured(
        model=identity.gemini_model_architect, schema=GEMSArchitect,
        system_instruction=system_instruction, prompt=prompt, temperature=0.2,
    )


def generate_worksheet_content(client: GeminiClient, identity: Identity, architect: GEMSArchitect) -> LessonWorksheet:
    matrix_json = json.dumps(architect.matrix.model_dump(), ensure_ascii=False)
    return client.generate_structured(
        model=identity.gemini_model_content, schema=LessonWorksheet,
        system_instruction=worksheet_prompts.SYSTEM_INSTRUCTION,
        prompt=worksheet_prompts.build_prompt(matrix_json), temperature=0.3,
    )


def generate_homework_content(client: GeminiClient, identity: Identity, architect: GEMSArchitect,
                               *, max_retries: int = 2) -> tuple[HomeworkContent, list[str]]:
    """Sinh bài tập, kiểm tra đúng 18/4/6 câu. Không ép bằng Pydantic
    validator (sẽ làm hỏng cả response nếu model lệch 1 câu, không có
    đường sửa) — kiểm tra sau khi sinh, retry có giới hạn, còn sai thì trả
    về kèm cảnh báo thay vì âm thầm chấp nhận."""
    matrix_json = json.dumps(architect.matrix.model_dump(), ensure_ascii=False)
    analysis_json = json.dumps(architect.analysis.model_dump(), ensure_ascii=False)
    prompt = homework_prompts.build_prompt(matrix_json, analysis_json)

    expected = (18, 4, 6)
    warnings: list[str] = []
    content: HomeworkContent | None = None
    for attempt in range(max_retries + 1):
        content = client.generate_structured(
            model=identity.gemini_model_content, schema=HomeworkContent,
            system_instruction=homework_prompts.SYSTEM_INSTRUCTION, prompt=prompt, temperature=0.3,
        )
        if content.question_counts == expected:
            return content, warnings
        if attempt < max_retries:
            prompt += (
                f"\n\nLƯU Ý: lần trước bạn trả về {content.question_counts} câu cho "
                f"(Phần I, Phần II, Phần III) — PHẢI trả đúng {expected}. Hãy sinh lại đầy đủ."
            )

    warnings.append(
        f"Số câu sinh ra {content.question_counts} không khớp yêu cầu {expected} sau {max_retries + 1} lần thử."
    )
    return content, warnings


def generate_lesson_plan_content(client: GeminiClient, identity: Identity, architect: GEMSArchitect) -> LessonPlanContent:
    matrix_json = json.dumps(architect.matrix.model_dump(), ensure_ascii=False)
    return client.generate_structured(
        model=identity.gemini_model_content, schema=LessonPlanContent,
        system_instruction=lesson_plan_prompts.SYSTEM_INSTRUCTION,
        prompt=lesson_plan_prompts.build_prompt(matrix_json), temperature=0.3,
    )


# ============================================================
#  GHI MARKDOWN NGUỒN
# ============================================================
def write_architect_markdown(architect: GEMSArchitect, lesson: LessonSpec, md_dir: Path) -> Path:
    spec_path = md_dir / f"{lesson.slug}_dac_ta_gems.md"
    lines = [f"# ĐẶC TẢ GEMS: {lesson.name.upper()}", "", "## I. KIẾN THỨC CỐT LÕI"]
    lines += [f"- {c}" for c in architect.analysis.key_concepts]
    lines += ["", "## II. BẪY SAI LẦM PHỔ BIẾN (MISCONCEPTIONS)"]
    for idx, item in enumerate(architect.analysis.misconceptions, 1):
        lines += [
            f"### Lỗi {idx}: {item.misconception}",
            f"- *Bản chất vật lý đúng:* {item.correct_concept}",
            f"- *Giải thích sư phạm:* {item.explanation}",
            "",
        ]
    lines += ["## III. PHƯƠNG PHÁP GIẢNG DẠY"]
    lines += [f"- {m}" for m in architect.analysis.teaching_methods]
    lines += ["", "## IV. MA TRẬN NHIỆM VỤ HỌC TẬP"]
    for unit in architect.matrix.units:
        lines += [
            f"### [{unit.unit_id}] {unit.unit_name}",
            f"- Khái niệm chính: {', '.join(unit.concepts)}",
            "- Chuỗi nhiệm vụ:",
        ]
        for t in unit.tasks:
            lines.append(f"  - **{t.task_id} ({t.task_type})**: {t.task_name} - {t.description} (Bối cảnh: {t.context_real})")
        lines.append("")
    spec_path.write_text("\n".join(lines), encoding="utf-8")
    return spec_path


def write_lesson_matrix_json(architect: GEMSArchitect, md_dir: Path) -> Path:
    matrix_path = md_dir / "lesson_matrix.json"
    matrix_path.write_text(json.dumps(architect.matrix.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    return matrix_path


def write_worksheet_markdown(worksheet: LessonWorksheet, lesson: LessonSpec, md_dir: Path) -> Path:
    """PHT bám thẳng tiến trình dạy thật trong KHBD (1 trình tự phẳng: Hình
    thành kiến thức mới → Luyện tập → Vận dụng), thay vì khung riêng của
    GEMS lặp lại 4 phần/ĐVKT như bản trước v9.4.0 — không có mục cho hoạt
    động Khởi động (không cần PHT giấy cho phần này)."""
    path = md_dir / f"{lesson.slug}_phieu_hoc_tap.md"
    lines = [
        f"# PHIẾU HỌC TẬP: {worksheet.lesson_name.upper()}",
        "**Họ và tên học sinh:** ....................................................  ",
        "**Lớp:** .................. **Ngày:** ......./......./.......  ",
        "", "---", "",
    ]

    lines.append("## 1. HÌNH THÀNH KIẾN THỨC MỚI")
    lines.append("")
    for u in worksheet.knowledge_formation:
        lines.append(f"### 📍 {u.unit_id.upper()}: {u.unit_name.upper()}")
        lines.append("")
        for t in u.tasks:
            lines.append(f"**Nhiệm vụ: {t.task_name} ({t.task_type})**")
            lines.append(f"*Hướng dẫn thực hiện: {t.instructions}*")
            lines.append(t.content)
            lines.append("")
            lines += ["[DOT_LINE_90]"] * 3
            lines.append("")
        lines.append("**Kiến thức trọng tâm:**")
        lines.append(u.core_theory.summary_cloze)
        lines.append("")
        lines.append(f"*Gợi ý từ khóa:* {', '.join(u.core_theory.key_words)}.")
        lines += ["", "---", ""]

    lines.append("## 2. LUYỆN TẬP")
    lines.append("")
    for item in worksheet.practice_items:
        lines.append(f"**Bài toán — {item.unit_name}:**")
        lines.append(f"*Hướng dẫn thực hiện: {item.instructions}*")
        lines.append(item.scenario)
        lines.append("")
        lines += ["[DOT_LINE_90]"] * 2
        lines.append("")
    lines += ["---", ""]

    lines.append("## 3. VẬN DỤNG")
    lines.append("")
    for t in worksheet.application_tasks:
        lines.append(f"**Nhiệm vụ: {t.task_name} ({t.task_type})**")
        lines.append(f"*Hướng dẫn thực hiện: {t.instructions}*")
        lines.append(t.content)
        lines.append("")
        lines += ["[DOT_LINE_90]"] * 3
        lines.append("")
    for reading in worksheet.application_readings:
        lines.append(f"**Mở rộng — {reading.unit_name}:**")
        lines.append(f"> {reading.reading_content}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_worksheet_json(worksheet: LessonWorksheet, md_dir: Path) -> Path:
    """Ghi cấu trúc PHT thật (`LessonWorksheet`) ra JSON — nguồn dữ liệu chính
    cho `gems/notebooklm/prompt_builder.py` khi dựng prompt Slide, thay vì
    regex-parse lại `{slug}_phieu_hoc_tap.md` đã render (cách cũ từng có bug
    thật không bị phát hiện do thiếu test coverage: `_NHIEM_VU_RE` không khớp
    bất kỳ nhiệm vụ nào suốt nhiều đợt). Cùng cách làm với
    `write_lesson_matrix_json` — 1 file JSON cấu trúc song song với Markdown
    dùng để đọc, Markdown dùng để hiển thị/in ấn."""
    path = md_dir / "worksheet_data.json"
    path.write_text(json.dumps(worksheet.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _emit_shared_context_header(lines: list[str], numbers: list[int], context: str) -> None:
    """Khớp mẫu 'Nội dung câu X và Y: ...' / 'Nội dung câu X đến Y: ...' của đề
    thi tốt nghiệp THPT thật (câu 3&4, câu 5&6 dùng chung 1 đoạn dữ kiện)."""
    if len(numbers) == 2:
        span = f"câu {numbers[0]} và {numbers[1]}"
    else:
        span = f"câu {numbers[0]} đến câu {numbers[-1]}"
    lines.append(f"*Nội dung {span}:* {context}")
    lines.append("")


def _emit_questions_with_shared_context(lines: list[str], questions: list, render_question) -> None:
    """Gộp các câu liên tiếp có cùng `shared_context` thành 1 khối dữ kiện
    chung, chỉ in 1 lần, rồi mới in từng câu hỏi riêng lẻ bên dưới."""
    i = 0
    n = len(questions)
    while i < n:
        ctx = questions[i].shared_context
        if ctx:
            j = i
            while j < n and questions[j].shared_context == ctx:
                j += 1
            _emit_shared_context_header(lines, list(range(i + 1, j + 1)), ctx)
            for k in range(i, j):
                render_question(lines, k + 1, questions[k])
            i = j
        else:
            render_question(lines, i + 1, questions[i])
            i += 1


def write_homework_markdown(homework: HomeworkContent, lesson: LessonSpec, md_dir: Path) -> Path:
    """Ghi đề bài tập về nhà — KHÔNG lộ đáp án Đúng/Sai ngay trong đề như
    bản gốc (`(Đ/S: {'Đ' if q.correct_a else 'S'})` viết thẳng vào câu hỏi
    Phần II). Đáp án chỉ xuất hiện ở mục hướng dẫn giải cuối file.

    Hỗ trợ nhóm câu dùng chung dữ kiện ("Nội dung câu X và Y: ...") khớp cấu
    trúc đề thi tốt nghiệp THPT 2025/2026 thật (xem `Part1Question.shared_context`)."""
    path = md_dir / f"{lesson.slug}_bai_tap_ve_nha.md"
    lines = [f"# BÀI TẬP VỀ NHÀ: {homework.lesson_name.upper()}", ""]
    if homework.shared_constants:
        lines.append(f"*Cho biết:* {homework.shared_constants}")
        lines.append("")

    lines.append(f"## PHẦN I: CÂU HỎI TRẮC NGHIỆM NHIỀU LỰA CHỌN ({len(homework.part1_questions)} câu)")
    lines.append("*Mỗi câu hỏi chỉ chọn một phương án trả lời đúng.*")
    lines.append("")

    def _render_p1(lines_, idx, q):
        lines_ += [f"**Câu {idx}:** {q.question_text}", f"A. {q.option_a}", f"B. {q.option_b}",
                   f"C. {q.option_c}", f"D. {q.option_d}", ""]

    _emit_questions_with_shared_context(lines, homework.part1_questions, _render_p1)

    lines.append(f"## PHẦN II: CÂU HỎI TRẮC NGHIỆM ĐÚNG/SAI ({len(homework.part2_questions)} câu)")
    lines.append("*Trong mỗi câu hỏi, thí sinh chọn Đúng hoặc Sai cho mỗi mệnh đề a), b), c), d).*")
    lines.append("")
    for idx, q in enumerate(homework.part2_questions, 1):
        lines.append(f"**Câu {idx}:** {q.question_text}")
        for label, stmt in zip("abcd", [q.statement_a, q.statement_b, q.statement_c, q.statement_d]):
            lines.append(f"{label}) {stmt}")
        lines.append("")

    lines.append(f"## PHẦN III: CÂU HỎI TRẢ LỜI NGẮN ({len(homework.part3_questions)} câu)")
    lines.append("*Thí sinh điền kết quả số vào ô trống tương ứng. Không làm tròn kết quả các phép tính trung gian.*")
    lines.append("")

    def _render_p3(lines_, idx, q):
        lines_.append(f"**Câu {idx}:** {q.question_text}")
        lines_.append("")

    _emit_questions_with_shared_context(lines, homework.part3_questions, _render_p3)

    lines += ["", "---", "## HƯỚNG DẪN GIẢI CHI TIẾT VÀ ĐÁP ÁN", "", "### PHẦN I:"]
    for idx, q in enumerate(homework.part1_questions, 1):
        lines.append(f"- **Câu {idx} (Chọn {q.correct_option}):** {q.explanation}")
    lines.append("")
    lines.append("### PHẦN II:")
    for idx, q in enumerate(homework.part2_questions, 1):
        marks = ", ".join(f"{label}) {'Đúng' if v else 'Sai'}" for label, v in
                           zip("abcd", [q.correct_a, q.correct_b, q.correct_c, q.correct_d]))
        lines.append(f"- **Câu {idx}:** {marks}. {q.explanation}")
    lines.append("")
    lines.append("### PHẦN III:")
    for idx, q in enumerate(homework.part3_questions, 1):
        lines.append(f"- **Câu {idx} ({q.correct_answer} {q.unit}):** {q.explanation}")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_lesson_plan_markdown(plan: LessonPlanContent, lesson: LessonSpec, md_dir: Path, identity: Identity) -> Path:
    """Khớp đúng Phụ lục IV (kèm Công văn 5512/BGDĐT-GDTrH, 18/12/2020): mỗi
    hoạt động có a) Mục tiêu, b) Nội dung, d) Tổ chức thực hiện — mục d) trình
    bày bằng bảng 2 cột "Hoạt động của giáo viên và học sinh" | "Sản phẩm"
    (khớp bài soạn minh hoạ mẫu), KHÔNG còn tách cột riêng cho GV và cột
    riêng cho HS như bản trước (bản đó tự chia đôi nội dung theo cặp khối,
    không đúng với cách trình bày trong tài liệu mẫu)."""
    path = md_dir / f"{lesson.slug}_ke_hoach_bai_day.md"
    lines = [
        "Trường: ................................................",
        f"Tổ: {identity.department}",
        "", "---", "",
        f"# KẾ HOẠCH BÀI DẠY",
        f"**Họ và tên giáo viên:** {identity.teacher_name}  ",
        f"**Tên bài dạy:** {plan.lesson_name}  ",
        "**Môn học/Hoạt động giáo dục:** Vật lí; **Lớp:** 12  ",
        f"**Thời gian thực hiện:** {plan.duration}  ",
        "", "---", "",
        "## I. YÊU CẦU CẦN ĐẠT",
        "### 1. Năng lực đặc thù (Vật lí)",
    ]
    lines += [f"- {c}" for c in plan.objectives.physics_competency]
    lines += ["", "### 2. Năng lực chung"]
    lines += [f"- {c}" for c in plan.objectives.general_competency]
    lines += ["", "### 3. Năng lực số (Công văn 3456/BGDĐT-GDPT)"]
    if plan.objectives.digital_competency:
        lines += [
            f"- **{c.code} — {c.competency}:** {c.learning_outcome} **Minh chứng:** {c.evidence}"
            for c in plan.objectives.digital_competency
        ]
    else:
        lines += ["- Không tích hợp nếu bài học không có nhiệm vụ và sản phẩm số xác thực."]
    lines += ["", "### 4. Phẩm chất"]
    lines += [f"- {c}" for c in plan.objectives.qualities]
    lines += ["", "---", "## II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU", "### 1. Giáo viên"]
    lines += [f"- {m}" for m in plan.materials.teacher_materials]
    lines += ["", "### 2. Học sinh"]
    lines += [f"- {m}" for m in plan.materials.student_materials]
    lines += ["", "---", "## III. TIẾN TRÌNH DẠY HỌC"]

    for idx, act in enumerate(plan.activities, 1):
        to_chuc = (
            f"**Bước 1: Chuyển giao nhiệm vụ:**<br>{act.steps.step1_transfer.replace(chr(10), '<br>')}<br>"
            f"**Bước 2: Thực hiện nhiệm vụ:**<br>{act.steps.step2_execution.replace(chr(10), '<br>')}<br>"
            f"**Bước 3: Báo cáo, thảo luận:**<br>{act.steps.step3_report.replace(chr(10), '<br>')}<br>"
            f"**Bước 4: Kết luận, nhận định:**<br>{act.steps.step4_conclusion.replace(chr(10), '<br>')}"
        )
        lines += [
            f"### {idx}. Hoạt động {idx}: {act.activity_name}",
            f"a) Mục tiêu: {act.objectives}",
            "",
            f"b) Nội dung: {act.content}",
            "",
            f"c) Sản phẩm: {act.product}",
            "",
            "**Kĩ thuật dạy học tích cực:** " + (", ".join(act.active_learning_techniques) or "Không sử dụng"),
            "",
            "**Năng lực số:** " + (", ".join(act.digital_competency_codes) or "Không tích hợp"),
            "",
            "d) Tổ chức thực hiện:",
            "",
            "| Hoạt động của giáo viên và học sinh | Sản phẩm |",
            "| :--- | :--- |",
            f"| {to_chuc} | {act.product} |",
            "", "---", "",
        ]

    lines += [
        "## IV. ĐIỀU CHỈNH BÀI DẠY",
        f"1. **Ưu điểm:**\n{plan.adjustments.advantages}",
        "",
        f"2. **Hạn chế:**\n{plan.adjustments.limitations}",
        "",
        f"3. **Hướng điều chỉnh:**\n{plan.adjustments.solutions}",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_slide_guide_markdown(identity: Identity, lesson: LessonSpec, md_dir: Path,
                                 architect: GEMSArchitect, worksheet: LessonWorksheet) -> Path:
    """Sinh outline slide THẬT bám đúng cấu trúc phẳng mới của PHT — 3 mục
    lớn (1. Hình thành kiến thức mới, 2. Luyện tập, 3. Vận dụng), số slide
    X.Y lấy X trực tiếp từ số mục PHT (1/2/3), Y là chỉ số tuần tự trong
    mục đó. Trước v9.4.0 slide dùng trục X.0-X.6 riêng theo từng ĐVKT (7
    slide/ĐVKT, tách nhiệm vụ/đáp án/vận dụng/mở rộng) trong khi PHT dùng
    trục X.1-X.4 khác — 2 trục lệch nhau, giáo viên phải tự đối chiếu. Giờ
    PHT không còn "vận dụng"/"mở rộng" lồng trong từng ĐVKT (đã tách thành
    mục 2/3 dùng chung), nên slide cũng bám sát y hệt, chỉ 1 trục số duy
    nhất. Dùng tên GV/brand từ identity.yaml thay vì hardcode."""
    path = md_dir / f"{lesson.slug}_huong_dan_slide.md"
    lines = [
        f"# HƯỚNG DẪN SLIDE BÀI GIẢNG: {lesson.name.upper()}",
        f"*Giáo viên thực hiện:* {identity.teacher_name}  ",
        f"*Trường phái thiết kế:* {identity.brand_label}  ",
        f"*Phông chữ chủ đạo:* {identity.default_font}  ",
        "",
        "---", "## QUY TẮC THIẾT KẾ BẮT BUỘC",
        "1. Phân cấp tiêu đề slide có mã số X.Y đúng theo bảng outline bên dưới — không tự đặt số khác.",
        "2. Tách biệt hoàn toàn slide Nhiệm vụ và slide Đáp án — không gộp chung 1 slide.",
        "3. Ngôn ngữ thuần Việt 100%.",
        f"4. Màu chủ đạo Primary `#1F4E79` cho tiêu đề/khung/đường kẻ; màu xám nhạt `#D9D9D9` cho "
        "nền hộp ghi chú/hộp gợi ý; dùng màu vàng `#FFD600` chỉ để highlight từ khóa định nghĩa/công thức.",
        f"5. Font {identity.default_font} thống nhất; tiêu đề đậm cỡ lớn, thân bài rõ ràng dễ đọc từ xa.",
        "6. Khung/hộp (hộp ghi nhớ, hộp gợi ý, khung nhiệm vụ) dùng viền mảnh, bo góc nhẹ, không đổ "
        "bóng nặng — phong cách nghiêm túc như sách giáo khoa, không phải slide quảng cáo.",
        "7. Tối đa 6-8 dòng chữ mỗi slide, nền sáng, chừa khoảng trống 35-40% cho hình minh họa.",
        "8. Ảnh minh họa bắt buộc chính xác khoa học — cấm hoạt hình/3D ảo/phóng đại phi thực tế; "
        "ưu tiên sơ đồ dạng đường nét (line-art) có nhãn/mũi tên như hình vẽ SGK Vật Lý, hoặc dùng "
        "trực tiếp các ảnh sơ đồ đã có sẵn trong Phiếu học tập nguồn (đường dẫn `ready/hinh_anh/...`) "
        "thay vì tự vẽ lại. Mọi chú thích trên ảnh phải bằng tiếng Việt.",
        "9. Slide Nhiệm vụ phải hiển thị kèm dòng \"Hướng dẫn thực hiện\" (hình thức/thời gian/tài "
        "liệu) lấy đúng nguyên văn từ Phiếu học tập nguồn — không tự bịa nội dung khác.",
        "",
        "---", "## SLIDE MỞ ĐẦU — Trang bìa",
        f"- **Tiêu đề chính:** {lesson.name.upper()}",
        f"- **Giáo viên thực hiện:** {identity.teacher_name}",
        "",
    ]

    lines.append("---\n## 📍 OUTLINE MỤC 1 — HÌNH THÀNH KIẾN THỨC MỚI")
    lines.append("")
    lines.append("| Slide | Nội dung | Nhiệm vụ liên quan |")
    lines.append("| :--- | :--- | :--- |")
    for i, unit in enumerate(architect.matrix.units, 1):
        nv_ref = ", ".join(t.task_id for t in unit.tasks) or "—"
        lines.append(f"| 1.{i}.0 | Đề mục — {unit.unit_name} | — |")
        lines.append(f"| 1.{i}.1 | Nhiệm vụ Khám phá | {nv_ref} |")
        lines.append(f"| 1.{i}.2 | Đáp án Khám phá | {nv_ref} |")
        lines.append(f"| 1.{i}.3 | Kiến thức Trọng tâm | — |")
    lines.append("")

    lines.append("---\n## 📍 OUTLINE MỤC 2 — LUYỆN TẬP")
    lines.append("")
    lines.append("| Slide | Nội dung | Nhiệm vụ liên quan |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| 2.0 | Đề mục Luyện tập | — |")
    for k, item in enumerate(worksheet.practice_items, 1):
        lines.append(f"| 2.{2 * k - 1} | Bài toán — {item.unit_name} | — |")
        lines.append(f"| 2.{2 * k} | Đáp án — {item.unit_name} | — |")
    lines.append("")

    lines.append("---\n## 📍 OUTLINE MỤC 3 — VẬN DỤNG")
    lines.append("")
    lines.append("| Slide | Nội dung | Nhiệm vụ liên quan |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| 3.0 | Đề mục Vận dụng | — |")
    idx = 1
    for t in worksheet.application_tasks:
        lines.append(f"| 3.{idx} | Nhiệm vụ Vận dụng — {t.task_name} | {t.task_id} |")
        idx += 1
        lines.append(f"| 3.{idx} | Đáp án Vận dụng — {t.task_name} | {t.task_id} |")
        idx += 1
    for reading in worksheet.application_readings:
        lines.append(f"| 3.{idx} | Mở rộng — {reading.unit_name} | — |")
        idx += 1
    lines.append("")

    lines.append("---")
    lines.append("## SLIDE KẾT BÀI — Sơ đồ tư duy tổng hợp")
    lines.append("- **Nội dung:** sơ đồ tư duy tổng hợp toàn bộ khái niệm cốt lõi của bài:")
    for concept in architect.analysis.key_concepts:
        lines.append(f"  - {concept}")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
