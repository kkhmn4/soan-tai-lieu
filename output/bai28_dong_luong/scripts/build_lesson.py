"""Soạn đặc tả sư phạm GEMS (phân tích + ma trận nhiệm vụ) và Bài tập về nhà
cho Bài 28 - Động lượng (Vật Lý 10, Kết nối tri thức) bằng cách tái sử dụng
trực tiếp các hàm/schema của package `gems/` (kiến trúc v9.0) — KHÔNG sửa
code dùng chung, KHÔNG đăng ký vào `gems/config/curriculum.yaml` (bài học
này nằm ngoài danh mục Vật Lý 12 mà GEMS đang phục vụ, chỉ dùng 1 lần theo
yêu cầu cụ thể).

Cách làm: dựng `LessonSpec` ngay trong script (không qua YAML), dựng đối
tượng Pydantic `GEMSArchitect`/`HomeworkContent` bằng nội dung sư phạm soạn
tay bám sát SGK Bài 28 (KNTT), rồi gọi đúng các hàm
`gems.generation.stages.write_*_markdown` để ra Markdown chuẩn, và
`gems.docx_export.homework_exporter.export_homework` để ra DOCX theo đúng
chuẩn định dạng đang chạy (`.agents/agents.md`).

KHÔNG dựng `LessonWorksheet`/gọi `pht_exporter` — Phiếu học tập của bài này
dùng cấu trúc riêng theo yêu cầu người dùng (1. Khởi động / 2. Hình thành
kiến thức mới / 3. Luyện tập / 4. Vận dụng - Mở rộng, đánh số X.Y + a/b/c,
dòng kẻ liền), xây dựng ở `build_pht.py`.

KHÔNG dựng `LessonPlanContent`/gọi `khbd_exporter` — Kế hoạch bài dạy của bài
này dùng mẫu riêng do người dùng cung cấp (mẫu Đinh Thiện Lý), xây dựng ở
script khác (`build_khbd.py`), không phải mẫu Công văn 5512 mà
`khbd_exporter.py` xuất ra.

Chạy: python "output/bai28_dong_luong/scripts/build_lesson.py"
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from gems.config.loader import LessonSpec, load_identity  # noqa: E402
from gems.docx_export.homework_exporter import export_homework  # noqa: E402
from gems.generation import stages  # noqa: E402
from gems.models.architect import (  # noqa: E402
    GEMSArchitect, KnowledgeUnit, LessonMatrix, MisconceptionItem,
    PedagogicalAnalysis, TaskItem,
)
from gems.models.homework import (  # noqa: E402
    HomeworkContent, Part1Question, Part2Question, Part3Question,
)

LESSON = LessonSpec(
    key="bai28",
    name="Bài 28 - Động lượng",
    slug="bai28_dong_luong",
    yccd_file="",
    yccd_fallback=(
        "Phát biểu được định nghĩa của động lượng và nêu được ý nghĩa vật lí của đại lượng đó. "
        "Phát biểu và viết được công thức liên hệ giữa lực tác dụng lên vật và tốc độ biến thiên "
        "của động lượng (dạng thứ hai của định luật II Newton)."
    ),
    num_knowledge_units=2,
)

OUTPUT_DIR = REPO_ROOT / "output" / LESSON.slug
MD_DIR = OUTPUT_DIR / "md"
READY_DIR = OUTPUT_DIR / "ready"
MD_DIR.mkdir(parents=True, exist_ok=True)
READY_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# GIAI ĐOẠN 1 — ĐẶC TẢ GEMS (phân tích sư phạm + ma trận nhiệm vụ)
# ============================================================
architect = GEMSArchitect(
    analysis=PedagogicalAnalysis(
        key_concepts=[
            "Động lượng của vật là đại lượng vectơ p = m.v, cùng hướng với vận tốc, đơn vị kg.m/s.",
            "Ý nghĩa vật lí của động lượng: đặc trưng cho khả năng truyền tương tác (truyền chuyển động) "
            "giữa các vật khi va chạm — phụ thuộc cả khối lượng lẫn vận tốc.",
            "Xung lượng của lực: khi lực F không đổi tác dụng lên vật trong thời gian ngắn Δt, "
            "tích F.Δt là xung lượng của lực, đơn vị N.s.",
            "Liên hệ giữa xung lượng của lực và độ biến thiên động lượng: F.Δt = Δp = p2 - p1.",
            "Dạng tổng quát của định luật II Newton theo động lượng: F = Δp/Δt.",
        ],
        misconceptions=[
            MisconceptionItem(
                misconception="Cho rằng động lượng chỉ phụ thuộc vào khối lượng — vật nặng hơn thì "
                              "luôn có động lượng lớn hơn, bất kể vận tốc.",
                correct_concept="Động lượng p = m.v phụ thuộc CẢ khối lượng lẫn vận tốc — vật nhẹ chuyển "
                                "động đủ nhanh vẫn có thể có động lượng lớn hơn vật nặng chuyển động chậm.",
                explanation="Dùng ví dụ đối chiếu số liệu cụ thể (xe tải tốc độ thấp và xe con tốc độ cao) "
                            "để học sinh tự tính và so sánh, thấy rõ vai trò ngang nhau của m và v.",
            ),
            MisconceptionItem(
                misconception="Coi động lượng là đại lượng vô hướng, chỉ quan tâm độ lớn m.v mà bỏ qua "
                              "tính chất vectơ (hướng).",
                correct_concept="Động lượng là đại lượng vectơ, cùng hướng với vận tốc; khi vật đổi chiều "
                                "chuyển động (ví dụ bóng bật tường) thì động lượng đổi chiều dù độ lớn "
                                "vận tốc không đổi, nên vẫn có độ biến thiên động lượng khác 0.",
                explanation="Dùng sơ đồ vectơ trước/sau va chạm (bóng bật tường) để học sinh thấy trực "
                            "quan việc đổi chiều vectơ, tránh nhầm '(tốc độ không đổi) = (động lượng "
                            "không đổi)'.",
            ),
            MisconceptionItem(
                misconception="Nhầm xung lượng của lực (F.Δt, đặc trưng cho khả năng làm biến đổi động "
                              "lượng) với công của lực (F.s, đặc trưng cho biến đổi năng lượng).",
                correct_concept="Xung lượng của lực là F.Δt (lực nhân thời gian tác dụng), là đại lượng "
                                "vectơ, còn công của lực là F.s (lực nhân quãng đường theo hướng lực), là "
                                "đại lượng vô hướng — hai khái niệm khác bản chất dù đều có 'lực nhân với "
                                "đại lượng khác'.",
                explanation="Nhấn mạnh đơn vị khác nhau (N.s so với J) và nhắc lại công thức A = F.s đã "
                            "học ở bài Công-Năng lượng để học sinh tự đối chiếu, tránh học vẹt.",
            ),
            MisconceptionItem(
                misconception="Hiểu 'thời gian tác dụng lực càng ngắn thì lực càng lớn' theo kiểu tuyệt "
                              "đối, không gắn với điều kiện độ biến thiên động lượng Δp không đổi.",
                correct_concept="Từ F = Δp/Δt: với CÙNG một Δp, nếu Δt giảm thì F tăng — đây là mối quan "
                                "hệ tỉ lệ nghịch có điều kiện (Δp cố định), không phải quy luật chung cho "
                                "mọi lực trong mọi tình huống.",
                explanation="Dùng chuỗi ví dụ thủ môn co tay lùi người, túi khí ô tô, đóng cọc bằng búa — "
                            "đều giữ Δp gần như không đổi và chỉ thay đổi Δt — để học sinh tự rút ra điều "
                            "kiện áp dụng đúng của công thức.",
            ),
        ],
        teaching_methods=[
            "Dạy học trực quan qua video/hình ảnh thí nghiệm va chạm (bi lăn trên máng trượt Hình 28.1, "
            "sút phạt bóng đá, vợt bóng bàn/tennis) để hình thành khái niệm động lượng từ hiện tượng thật.",
            "Kỹ thuật dạy học hợp tác nhóm nhỏ (khăn trải bàn, think-pair-share) cho các nhiệm vụ so sánh "
            "và tranh luận (vật nào khó dừng lại hơn, lực nào lớn hơn).",
            "Dạy học nêu vấn đề: xuất phát từ 2 tình huống mở bài SGK (xe tải/xe con phanh gấp, thủ môn "
            "bắt bóng sút phạt) để dẫn dắt tự nhiên đến định nghĩa và công thức.",
            "Luyện tập bám sát phong cách câu hỏi thi tốt nghiệp THPT ngay tại lớp, để học sinh làm quen "
            "cấu trúc đề thi thật thay vì chỉ gặp ở bài tập về nhà.",
        ],
    ),
    matrix=LessonMatrix(
        lesson_name=LESSON.name,
        units=[
            KnowledgeUnit(
                unit_id="2.1",
                unit_name="Động lượng",
                concepts=[
                    "Khả năng truyền chuyển động khi tương tác giữa các vật",
                    "Định nghĩa và công thức động lượng p = m.v",
                    "Tính chất vectơ và đơn vị của động lượng",
                ],
                tasks=[
                    TaskItem(
                        task_id="NV1", task_type="Contextual MCQ",
                        task_name="Xe nào khó dừng lại hơn? Bóng nào khó bắt hơn?",
                        description="Quan sát 2 tình huống mở bài (xe tải/xe con cùng tốc độ khi phanh gấp; "
                                    "cầu thủ sút phạt 11 m) để dự đoán vật nào 'khó dừng lại hơn' và giải "
                                    "thích ban đầu bằng trực giác, làm nền cho khái niệm động lượng.",
                        context_real="Xe tải và xe con cùng chạy trên đường; thủ môn bắt bóng sút phạt 11 m.",
                    ),
                    TaskItem(
                        task_id="NV2", task_type="Thí nghiệm khám phá",
                        task_name="Thí nghiệm ba viên bi A, B, C",
                        description="Học sinh trực tiếp làm 2 thí nghiệm với bộ dụng cụ máng trượt + 3 viên bi "
                                    "(Hình 28.1 SGK): (1) so sánh bi A và bi B (khác khối lượng) cùng thả từ "
                                    "một độ cao; (2) chỉ thả bi A nhưng đổi độ dốc. Quan sát, đo quãng đường "
                                    "bi C dịch chuyển sau va chạm, tự rút ra kết luận về các yếu tố ảnh hưởng "
                                    "đến khả năng truyền chuyển động — dẫn tới định nghĩa động lượng.",
                        context_real="Thí nghiệm thật với máng trượt và 3 viên bi khác khối lượng.",
                    ),
                ],
            ),
            KnowledgeUnit(
                unit_id="2.2",
                unit_name="Xung lượng của lực",
                concepts=[
                    "Định nghĩa xung lượng của lực F.Δt",
                    "Liên hệ xung lượng của lực và độ biến thiên động lượng F.Δt = Δp",
                    "Dạng tổng quát của định luật II Newton F = Δp/Δt",
                ],
                tasks=[
                    TaskItem(
                        task_id="NV3", task_type="Infographic Decryption",
                        task_name="Đọc đồ thị lực - thời gian",
                        description="Khai thác đồ thị F-t (lực không đổi tác dụng trong Δt) để nhận ra diện "
                                    "tích hình chữ nhật chính là độ lớn xung lượng của lực, liên hệ với tình "
                                    "huống thủ môn co tay lùi người khi bắt bóng.",
                        context_real="Đồ thị lực-thời gian khi thủ môn bắt bóng sút phạt.",
                    ),
                    TaskItem(
                        task_id="NV4", task_type="Model Builder",
                        task_name="Suy luận công thức liên hệ",
                        description="Từ định luật II Newton dạng F = m.a đã học, xây dựng từng bước để suy "
                                    "ra công thức liên hệ giữa xung lượng của lực và độ biến thiên động "
                                    "lượng, từ đó viết dạng tổng quát F = Δp/Δt.",
                        context_real="Vận dụng lại kiến thức định luật II Newton đã học ở bài trước.",
                    ),
                ],
            ),
        ],
    ),
)

stages.write_architect_markdown(architect, LESSON, MD_DIR)
stages.write_lesson_matrix_json(architect, MD_DIR)


# ============================================================
# GIAI ĐOẠN 3 — BÀI TẬP VỀ NHÀ
# ============================================================
homework = HomeworkContent(
    lesson_name=LESSON.name,
    part1_questions=[
        # --- NHẬN BIẾT (6 câu) ---
        Part1Question(
            question_text="Động lượng $p$ của một vật khối lượng $m$ đang chuyển động với vận tốc $v$ "
                          "được xác định bởi biểu thức nào sau đây?",
            option_a="$p = mv$", option_b="$p = mv^2$", option_c="$p = 0,5mv^2$",
            option_d="$p = m/v$", correct_option="A",
            explanation="Theo định nghĩa (công thức 28.1 SGK), động lượng của vật được xác định bởi "
                        "công thức p = m.v (dạng vectơ).",
        ),
        Part1Question(
            question_text="Trong hệ SI, đơn vị của động lượng là",
            option_a="kg.m/s", option_b="kg.m/s²", option_c="N.m", option_d="J",
            correct_option="A",
            explanation="Từ p = mv, đơn vị động lượng là kg.(m/s) = kg.m/s.",
        ),
        Part1Question(
            question_text="Động lượng là đại lượng",
            option_a="vô hướng, luôn có giá trị dương.",
            option_b="vectơ, cùng hướng với vectơ vận tốc của vật.",
            option_c="vectơ, ngược hướng với vectơ vận tốc của vật.",
            option_d="vô hướng, có thể âm hoặc dương tùy chiều chuyển động.",
            correct_option="B",
            explanation="SGK nêu rõ: động lượng là một đại lượng vectơ có cùng hướng với vận tốc của vật.",
        ),
        Part1Question(
            question_text="Khi một lực $F$ không đổi tác dụng lên một vật trong khoảng thời gian ngắn "
                          "$\\Delta t$ thì xung lượng của lực đó được xác định bằng biểu thức nào?",
            option_a="$F.\\Delta t$", option_b="$F/\\Delta t$",
            option_c="$F.\\Delta t^2$", option_d="$\\Delta t/F$",
            correct_option="A",
            explanation="Theo định nghĩa, xung lượng của lực F trong khoảng thời gian Δt là tích F.Δt.",
        ),
        Part1Question(
            question_text="Đơn vị của xung lượng của lực trong hệ SI là",
            option_a="N.s", option_b="N/s", option_c="N.m", option_d="kg.m/s²",
            correct_option="A",
            explanation="Từ định nghĩa xung lượng = F.Δt, đơn vị là N.s (về bản chất tương đương kg.m/s).",
        ),
        Part1Question(
            question_text="Biểu thức nào sau đây là dạng tổng quát của định luật II Newton viết theo độ "
                          "biến thiên động lượng?",
            option_a="$F = ma$", option_b="$F = \\Delta p/\\Delta t$",
            option_c="$F = m\\Delta v$", option_d="$F = \\Delta p . \\Delta t$",
            correct_option="B",
            explanation="Từ F.Δt = Δp suy ra F = Δp/Δt — đây là dạng tổng quát của định luật II Newton.",
        ),
        # --- THÔNG HIỂU (6 câu) ---
        Part1Question(
            question_text="Trong thí nghiệm ở Hình 28.1 (SGK), hai viên bi A và B (bi B nặng hơn bi A) "
                          "được thả lăn từ cùng một độ cao trên máng trượt nên đến chân dốc với cùng một "
                          "tốc độ, sau đó va chạm vào viên bi C đang đứng yên. Nhận định nào sau đây đúng?",
            option_a="Bi A làm bi C lăn xa hơn vì bi A nhẹ nên tốc độ truyền đi nhanh hơn.",
            option_b="Bi B làm bi C lăn xa hơn vì bi B có khối lượng lớn hơn nên động lượng lớn hơn dù "
                     "cùng tốc độ.",
            option_c="Hai viên bi làm bi C lăn xa như nhau vì chúng có cùng tốc độ khi va chạm.",
            option_d="Không thể xác định được vì còn phụ thuộc vào chất liệu của viên bi.",
            correct_option="B",
            explanation="Cùng tốc độ nhưng bi B có khối lượng lớn hơn nên động lượng p = mv của bi B lớn "
                        "hơn, do đó khả năng truyền tương tác cho bi C mạnh hơn, làm bi C lăn xa hơn.",
        ),
        Part1Question(
            question_text="Hai vật (1) và (2) có cùng khối lượng, đang chuyển động trên một đường thẳng, "
                          "biết tốc độ của vật (1) lớn hơn tốc độ của vật (2). So sánh động lượng của hai "
                          "vật.",
            option_a="Động lượng vật (1) lớn hơn động lượng vật (2).",
            option_b="Động lượng vật (1) nhỏ hơn động lượng vật (2).",
            option_c="Động lượng hai vật bằng nhau vì cùng khối lượng.",
            option_d="Không thể so sánh được vì động lượng là đại lượng vectơ.",
            correct_option="A",
            explanation="Cùng khối lượng, theo p = mv, vật có tốc độ lớn hơn thì động lượng lớn hơn.",
        ),
        Part1Question(
            question_text="Khi bắt một quả bóng bay tới, nếu thủ môn co tay lại và lùi người theo hướng "
                          "bóng bay thay vì giữ tay cứng đờ, thì tay thủ môn sẽ đỡ đau hơn. Giải thích nào "
                          "sau đây đúng về mặt vật lí?",
            option_a="Vì động lượng của quả bóng đã bị giảm đi trước khi chạm tay.",
            option_b="Vì hành động đó làm giảm độ biến thiên động lượng của quả bóng.",
            option_c="Vì hành động đó làm tăng thời gian tương tác Δt, trong khi độ biến thiên động "
                     "lượng gần như không đổi nên lực trung bình tác dụng lên tay giảm.",
            option_d="Vì hành động đó làm giảm xung lượng của lực mà tay tác dụng lên bóng.",
            correct_option="C",
            explanation="Độ biến thiên động lượng của bóng gần như không đổi; theo F = Δp/Δt, khi Δt "
                        "tăng thì F giảm — đây là bản chất vật lí đúng.",
        ),
        Part1Question(
            question_text="Đồ thị biểu diễn độ lớn của một lực không đổi theo thời gian tác dụng lên vật "
                          "trong khoảng thời gian Δt có dạng một hình chữ nhật (trục tung là F, trục "
                          "hoành là t). Diện tích của hình chữ nhật đó biểu diễn đại lượng nào?",
            option_a="Công của lực.", option_b="Độ lớn xung lượng của lực.",
            option_c="Độ lớn vận tốc của vật.", option_d="Động năng của vật.",
            correct_option="B",
            explanation="Diện tích hình chữ nhật = F × Δt, đúng bằng độ lớn xung lượng của lực.",
        ),
        Part1Question(
            question_text="Một quả bóng bay theo phương ngang đến đập vào tường rồi bật ngược trở lại với "
                          "cùng tốc độ ban đầu. Nhận định nào sau đây đúng?",
            option_a="Động lượng của bóng không đổi vì tốc độ không đổi.",
            option_b="Động lượng của bóng bằng 0 sau va chạm vì bóng đổi chiều chuyển động.",
            option_c="Động lượng của bóng đổi chiều nhưng không đổi độ lớn, nên vẫn có độ biến thiên "
                     "động lượng khác 0.",
            option_d="Động lượng của bóng tăng lên gấp đôi vì có lực tác dụng của tường.",
            correct_option="C",
            explanation="Động lượng là vectơ; tốc độ không đổi nhưng hướng đổi ngược lại nên vectơ động "
                        "lượng cũng đổi chiều, dẫn đến Δp ≠ 0 dù độ lớn động lượng trước/sau bằng nhau.",
        ),
        Part1Question(
            question_text="Khi đóng cọc bằng búa máy, để cọc lún sâu hơn sau mỗi nhát búa, người ta "
                          "thường làm cho búa đạt tốc độ lớn hơn khi chạm cọc, thay vì cố tình kéo dài "
                          "thời gian va chạm giữa búa và cọc. Giải thích nào sau đây hợp lí nhất?",
            option_a="Vì búa có tốc độ lớn hơn thì động lượng của búa lớn hơn, dẫn tới độ biến thiên "
                     "động lượng truyền cho cọc lớn hơn, làm xung lượng của lực búa tác dụng lên cọc "
                     "lớn hơn.",
            option_b="Vì thời gian va chạm giữa búa và cọc không ảnh hưởng đến lực tác dụng lên cọc.",
            option_c="Vì tốc độ của búa không liên quan đến động lượng mà chỉ liên quan đến động năng "
                     "của búa.",
            option_d="Vì xung lượng của lực chỉ phụ thuộc vào thời gian va chạm, không phụ thuộc vào "
                     "tốc độ của búa.",
            correct_option="A",
            explanation="Búa tốc độ lớn hơn có động lượng lớn hơn; khi va chạm dừng lại đột ngột, độ "
                        "biến thiên động lượng lớn hơn nên xung lượng của lực (F.Δt = Δp) tác dụng lên "
                        "cọc cũng lớn hơn.",
        ),
        # --- VẬN DỤNG (6 câu) ---
        Part1Question(
            question_text="Một xe buýt khối lượng 2 tấn đang chuyển động với tốc độ 36 km/h. Độ lớn "
                          "động lượng của xe buýt là",
            option_a="$2.10^4$ kg.m/s", option_b="$7,2.10^4$ kg.m/s",
            option_c="$2.10^3$ kg.m/s", option_d="$3,6.10^4$ kg.m/s",
            correct_option="A",
            explanation="Đổi 36 km/h = 10 m/s; p = mv = 2000×10 = 20000 = 2.10⁴ kg.m/s.",
        ),
        Part1Question(
            question_text="Một quả bóng khối lượng 400 g bay đến đập vuông góc vào tường với tốc độ 8 m/s "
                          "rồi bật ngược trở lại theo phương cũ với tốc độ 6 m/s. Độ lớn độ biến thiên "
                          "động lượng của quả bóng là",
            option_a="5,6 kg.m/s", option_b="0,8 kg.m/s", option_c="3,2 kg.m/s", option_d="2,4 kg.m/s",
            correct_option="A",
            explanation="Do đổi chiều nên Δp = m(v1+v2) = 0,4×(8+6) = 5,6 kg.m/s.",
        ),
        Part1Question(
            question_text="Một ô tô khối lượng 1,2 tấn đang chuyển động với tốc độ 54 km/h thì hãm phanh, "
                          "chuyển động chậm dần rồi dừng hẳn sau 5 s. Độ lớn lực hãm trung bình tác dụng "
                          "lên xe là",
            option_a="3600 N", option_b="6480 N", option_c="300 N", option_d="18000 N",
            correct_option="A",
            explanation="54 km/h = 15 m/s; Δp = 1200×15 = 18000 kg.m/s; F = Δp/Δt = 18000/5 = 3600 N.",
        ),
        Part1Question(
            question_text="Một cầu thủ sút một quả bóng khối lượng 450 g đang nằm yên trên sân; biết "
                          "thời gian chân cầu thủ tiếp xúc với bóng là 0,05 s và ngay sau cú sút bóng bay "
                          "đi với tốc độ 20 m/s. Độ lớn lực trung bình mà chân cầu thủ tác dụng lên bóng "
                          "là",
            option_a="180 N", option_b="9 N", option_c="45 N", option_d="900 N",
            correct_option="A",
            explanation="Δp = mv = 0,45×20 = 9 kg.m/s; F = Δp/Δt = 9/0,05 = 180 N.",
        ),
        Part1Question(
            question_text="Một vật khối lượng 3 kg đang chuyển động thẳng với tốc độ 4 m/s thì chịu tác "
                          "dụng của một lực không đổi cùng hướng chuyển động trong 2 s, làm tốc độ của "
                          "vật tăng lên 10 m/s. Độ lớn lực tác dụng lên vật là",
            option_a="9 N", option_b="3 N", option_c="21 N", option_d="12 N",
            correct_option="A",
            explanation="Δv = 10-4 = 6 m/s; Δp = 3×6 = 18 kg.m/s; F = Δp/Δt = 18/2 = 9 N.",
        ),
        Part1Question(
            question_text="Một viên đạn khối lượng 10 g bay ra khỏi nòng súng với tốc độ 300 m/s. Độ lớn "
                          "động lượng của viên đạn là",
            option_a="3 kg.m/s", option_b="30 kg.m/s", option_c="0,3 kg.m/s", option_d="3000 kg.m/s",
            correct_option="A",
            explanation="Đổi 10 g = 0,01 kg; p = mv = 0,01×300 = 3 kg.m/s.",
        ),
    ],
    part2_questions=[
        Part2Question(
            question_text="Xe tải khối lượng 5 tấn và xe con khối lượng 1 tấn đang chuyển động cùng "
                          "chiều trên một đường thẳng với tốc độ lần lượt là 36 km/h và 72 km/h.",
            statement_a="Động lượng của xe tải có độ lớn bằng $5.10^4$ kg.m/s.",
            statement_b="Động lượng của xe con có độ lớn bằng $2.10^4$ kg.m/s.",
            statement_c="Vì xe con chạy nhanh hơn xe tải nên động lượng của xe con lớn hơn động lượng "
                       "của xe tải.",
            statement_d="Hai vectơ động lượng của xe tải và xe con cùng phương, cùng chiều với nhau.",
            correct_a=True, correct_b=True, correct_c=False, correct_d=True,
            explanation="36 km/h = 10 m/s → p_tải = 5000×10 = 5.10⁴ kg.m/s (a Đúng). 72 km/h = 20 m/s → "
                        "p_con = 1000×20 = 2.10⁴ kg.m/s (b Đúng). So sánh 5.10⁴ > 2.10⁴ nên động lượng xe "
                        "tải LỚN HƠN xe con, không phải nhỏ hơn (c Sai — nhầm lẫn chỉ dựa vào tốc độ mà "
                        "bỏ qua khối lượng). Hai xe chuyển động cùng chiều nên hai vectơ động lượng cùng "
                        "phương, cùng chiều (d Đúng).",
        ),
        Part2Question(
            question_text="Một quả bóng tennis khối lượng 60 g bay tới đập vuông góc vào mặt vợt với tốc "
                          "độ 15 m/s, sau va chạm bật trở lại theo phương cũ với tốc độ 15 m/s (coi va "
                          "chạm là đàn hồi, bỏ qua các lực khác trong lúc va chạm).",
            statement_a="Tốc độ của bóng trước và sau va chạm bằng nhau nên động lượng của bóng không "
                       "thay đổi.",
            statement_b="Độ biến thiên động lượng của bóng có độ lớn bằng 1,8 kg.m/s.",
            statement_c="Vectơ động lượng của bóng sau va chạm ngược hướng với vectơ động lượng của bóng "
                       "trước va chạm.",
            statement_d="Nếu thời gian va chạm giữa bóng và mặt vợt càng ngắn thì lực mặt vợt tác dụng "
                       "lên bóng càng nhỏ.",
            correct_a=False, correct_b=True, correct_c=True, correct_d=False,
            explanation="Động lượng là vectơ; dù tốc độ không đổi nhưng hướng đổi ngược lại nên động "
                        "lượng vẫn thay đổi (a Sai). Δp = m(v1+v2) = 0,06×(15+15) = 1,8 kg.m/s (b Đúng). "
                        "Bóng bật ngược theo phương cũ nên vectơ động lượng sau ngược hướng vectơ động "
                        "lượng trước (c Đúng). Theo F = Δp/Δt, với Δp không đổi, Δt càng ngắn thì F càng "
                        "LỚN, không phải càng nhỏ (d Sai).",
        ),
        Part2Question(
            question_text="Một vật khối lượng 500 g đang đứng yên thì chịu tác dụng của một lực không "
                          "đổi theo phương ngang trong khoảng thời gian 0,2 s, sau đó vật đạt tốc độ 4 "
                          "m/s.",
            statement_a="Độ biến thiên động lượng của vật có độ lớn bằng 2 kg.m/s.",
            statement_b="Độ lớn lực trung bình tác dụng lên vật bằng 10 N.",
            statement_c="Nếu thời gian tác dụng lực tăng lên gấp đôi (0,4 s) mà vật vẫn đạt tốc độ 4 m/s "
                       "như trên thì độ lớn lực trung bình cần thiết giảm đi một nửa.",
            statement_d="Xung lượng của lực tác dụng lên vật trong khoảng thời gian 0,2 s có độ lớn bằng "
                       "10 N.s.",
            correct_a=True, correct_b=True, correct_c=True, correct_d=False,
            explanation="Δp = mΔv = 0,5×4 = 2 kg.m/s (a Đúng). F = Δp/Δt = 2/0,2 = 10 N (b Đúng). Δp cố "
                        "định = 2 kg.m/s, nếu Δt tăng gấp đôi thì F = 2/0,4 = 5 N, giảm một nửa so với 10 "
                        "N (c Đúng). Xung lượng của lực trong 0,2 s CHÍNH LÀ độ biến thiên động lượng = 2 "
                        "N.s, không phải 10 N.s — 10 N là giá trị của lực F, không phải xung lượng F.Δt "
                        "(d Sai, đây là bẫy nhầm giữa giá trị F và giá trị F.Δt).",
        ),
        Part2Question(
            question_text="Trong môn quyền anh (boxing), khi bị đấm trúng mặt, võ sĩ thường có phản xạ "
                          "ngả đầu ra sau theo hướng cú đấm thay vì giữ đầu cố định.",
            statement_a="Việc ngả đầu ra sau giúp kéo dài thời gian tương tác Δt giữa nắm đấm và mặt.",
            statement_b="Độ biến thiên động lượng mà nắm đấm truyền cho phần đầu không đổi thì khi Δt "
                       "tăng, lực tác dụng trung bình F sẽ giảm.",
            statement_c="Việc ngả đầu ra sau làm giảm động lượng ban đầu của cú đấm nên sẽ đỡ đau hơn.",
            statement_d="Nguyên tắc trên tương tự như nguyên lí hoạt động của túi khí trên ô tô: kéo dài "
                       "thời gian va chạm để giảm lực tác dụng lên người ngồi trong xe.",
            correct_a=True, correct_b=True, correct_c=False, correct_d=True,
            explanation="Ngả đầu ra sau kéo dài Δt (a Đúng), theo F=Δp/Δt thì F giảm khi Δt tăng và Δp "
                        "không đổi (b Đúng). Bản chất KHÔNG phải giảm động lượng của cú đấm mà là kéo dài "
                        "thời gian tương tác để giảm lực trung bình (c Sai). Túi khí ô tô cũng hoạt động "
                        "theo đúng nguyên lí kéo dài Δt để giảm F (d Đúng).",
        ),
    ],
    part3_questions=[
        Part3Question(
            question_text="Tính độ lớn động lượng của vật thứ nhất. Làm tròn kết quả đến chữ số hàng đơn "
                          "vị (đơn vị kg.m/s).",
            correct_answer="6", unit="kg.m/s",
            explanation="p₁ = m₁v₁ = 2×3 = 6 kg.m/s.",
            shared_context="Một vật khối lượng $m_1 = 2$ kg chuyển động với tốc độ $v_1 = 3$ m/s và một "
                          "vật khác khối lượng $m_2 = 1$ kg chuyển động với tốc độ $v_2 = 5$ m/s, trên "
                          "cùng một đường thẳng.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng của vật thứ hai. Làm tròn kết quả đến chữ số hàng đơn "
                          "vị (đơn vị kg.m/s).",
            correct_answer="5", unit="kg.m/s",
            explanation="p₂ = m₂v₂ = 1×5 = 5 kg.m/s.",
            shared_context="Một vật khối lượng $m_1 = 2$ kg chuyển động với tốc độ $v_1 = 3$ m/s và một "
                          "vật khác khối lượng $m_2 = 1$ kg chuyển động với tốc độ $v_2 = 5$ m/s, trên "
                          "cùng một đường thẳng.",
        ),
        Part3Question(
            question_text="Tính độ lớn độ biến thiên động lượng của quả bóng. Không làm tròn kết quả các "
                          "phép tính trung gian. Làm tròn kết quả cuối cùng đến chữ số hàng phần mười "
                          "(đơn vị kg.m/s).",
            correct_answer="4,0", unit="kg.m/s",
            explanation="Δp = m(v1+v2) = 0,2×(12+8) = 0,2×20 = 4,0 kg.m/s.",
            shared_context="Một quả bóng khối lượng 200 g bay tới đập vuông góc vào một bức tường với "
                          "tốc độ 12 m/s và bật ngược trở lại theo phương cũ với tốc độ 8 m/s. Thời gian "
                          "va chạm giữa bóng và tường là 0,05 s.",
        ),
        Part3Question(
            question_text="Tính độ lớn lực trung bình mà tường tác dụng lên quả bóng trong thời gian va "
                          "chạm. Làm tròn kết quả đến chữ số hàng đơn vị (đơn vị N).",
            correct_answer="80", unit="N",
            explanation="F = Δp/Δt = 4,0/0,05 = 80 N.",
            shared_context="Một quả bóng khối lượng 200 g bay tới đập vuông góc vào một bức tường với "
                          "tốc độ 12 m/s và bật ngược trở lại theo phương cũ với tốc độ 8 m/s. Thời gian "
                          "va chạm giữa bóng và tường là 0,05 s.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng ban đầu của xe. Làm tròn kết quả đến chữ số hàng trăm "
                          "(đơn vị kg.m/s).",
            correct_answer="20000", unit="kg.m/s",
            explanation="Đổi 72 km/h = 20 m/s; p = mv = 1000×20 = 20000 kg.m/s.",
            shared_context="Một ô tô khối lượng 1 tấn đang chuyển động thẳng với tốc độ 72 km/h thì "
                          "người lái xe đạp phanh, lực hãm trung bình tác dụng lên xe có độ lớn 2500 N "
                          "(coi lực hãm không đổi).",
        ),
        Part3Question(
            question_text="Tính thời gian tối thiểu để xe dừng hẳn kể từ lúc đạp phanh. Làm tròn kết quả "
                          "đến chữ số hàng phần mười (đơn vị s).",
            correct_answer="8,0", unit="s",
            explanation="Δt = Δp/F = 20000/2500 = 8,0 s.",
            shared_context="Một ô tô khối lượng 1 tấn đang chuyển động thẳng với tốc độ 72 km/h thì "
                          "người lái xe đạp phanh, lực hãm trung bình tác dụng lên xe có độ lớn 2500 N "
                          "(coi lực hãm không đổi).",
        ),
    ],
    shared_constants=None,
)

assert homework.question_counts == (18, 4, 6), homework.question_counts
homework_md_path = stages.write_homework_markdown(homework, LESSON, MD_DIR)


# ============================================================
# BIÊN DỊCH DOCX (Bài tập về nhà — PHT/KHBD dựng riêng ở build_pht.py/build_khbd.py)
# ============================================================
identity = load_identity()
homework_docx = READY_DIR / f"{LESSON.slug}_bai_tap_ve_nha.docx"

export_homework(str(homework_md_path), str(homework_docx), identity, LESSON.name)

print("OK - da xuat bai tap ve nha va dac ta gems vao thu muc ready/md")
