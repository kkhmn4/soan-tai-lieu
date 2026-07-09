"""Soạn Bài tập về nhà cho Bài 28 - Động lượng (V3, CHỈ 1 TIẾT — riêng phần
"I. Động lượng"), tái sử dụng trực tiếp `gems.docx_export.homework_exporter`
+ schema `gems.models.homework` — KHÔNG sửa code trong `gems/`, KHÔNG đăng ký
vào `gems/config/curriculum.yaml` (one-off, theo dac_ta_v3.md mục 3).

Khác V2: TOÀN BỘ 18 câu Phần I + 4 câu Phần II + 6 câu Phần III chỉ xoay
quanh p = m.v (định nghĩa, tính vectơ, đơn vị, ý nghĩa vật lí, so sánh động
lượng) — KHÔNG có câu nào về xung lượng của lực F.Δt hay F = Δp/Δt (không
thuộc phạm vi tiết học V3).

Chạy: python "output/bai28_dong_luong_v3/scripts/build_homework.py"
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from gems.config.loader import LessonSpec, load_identity  # noqa: E402
from gems.docx_export.homework_exporter import export_homework  # noqa: E402
from gems.generation import stages  # noqa: E402
from gems.models.homework import (  # noqa: E402
    HomeworkContent, Part1Question, Part2Question, Part3Question,
)

LESSON = LessonSpec(
    key="bai28_v3",
    name="Bài 28 - Động lượng (riêng phần I. Động lượng)",
    slug="bai28_dong_luong_v3",
    yccd_file="",
    yccd_fallback=(
        "Phát biểu được định nghĩa của động lượng và nêu được ý nghĩa vật lí của đại lượng đó."
    ),
    num_knowledge_units=1,
)

OUTPUT_DIR = REPO_ROOT / "output" / LESSON.slug
MD_DIR = OUTPUT_DIR / "md"
READY_DIR = OUTPUT_DIR / "ready"
MD_DIR.mkdir(parents=True, exist_ok=True)
READY_DIR.mkdir(parents=True, exist_ok=True)

homework = HomeworkContent(
    lesson_name=LESSON.name,
    part1_questions=[
        # --- NHẬN BIẾT (6 câu) ---
        Part1Question(
            question_text="Động lượng $p$ của một vật khối lượng $m$ đang chuyển động với vận tốc $v$ "
                          "được xác định bởi công thức nào sau đây?",
            option_a="$p = mv$", option_b="$p = \\dfrac{1}{2}mv^2$",
            option_c="$p = m + v$", option_d="$p = \\dfrac{m}{v}$",
            correct_option="A",
            explanation="Theo công thức (28.1) SGK, động lượng của vật được xác định bởi p = m.v (dạng vectơ).",
        ),
        Part1Question(
            question_text="Trong hệ SI, đơn vị của động lượng là",
            option_a="kg.m/s", option_b="kg.m²/s", option_c="N.m", option_d="J.s",
            correct_option="A",
            explanation="Từ p = mv, đơn vị động lượng là kg.(m/s) = kg.m/s.",
        ),
        Part1Question(
            question_text="Động lượng của một vật là đại lượng",
            option_a="vô hướng, luôn dương.",
            option_b="vectơ, cùng hướng với vectơ vận tốc của vật.",
            option_c="vectơ, ngược hướng với vectơ vận tốc của vật.",
            option_d="vô hướng, có thể âm hoặc dương.",
            correct_option="B",
            explanation="SGK nêu rõ: động lượng là đại lượng vectơ, có cùng hướng với vectơ vận tốc của vật.",
        ),
        Part1Question(
            question_text="Đại lượng đặc trưng cho khả năng truyền chuyển động của một vật khi nó tương "
                          "tác (va chạm) với vật khác được gọi là",
            option_a="động lượng.", option_b="động năng.", option_c="thế năng.", option_d="công suất.",
            correct_option="A",
            explanation="Theo SGK mục I: đại lượng đặc trưng cho khả năng truyền chuyển động của một vật "
                        "khi tương tác với vật khác gọi là động lượng.",
        ),
        Part1Question(
            question_text="Phát biểu nào sau đây về động lượng là KHÔNG đúng?",
            option_a="Động lượng của một vật đặc trưng cho trạng thái chuyển động của vật đó.",
            option_b="Động lượng là đại lượng vectơ.",
            option_c="Động lượng có đơn vị là kg.m/s.",
            option_d="Động lượng của một vật chỉ phụ thuộc vào vận tốc của vật đó.",
            correct_option="D",
            explanation="Động lượng p = mv phụ thuộc CẢ khối lượng lẫn vận tốc, không chỉ phụ thuộc vận "
                        "tốc — đáp án D sai.",
        ),
        Part1Question(
            question_text="Hai vật có cùng độ lớn động lượng nhưng khối lượng vật (1) lớn hơn khối lượng "
                          "vật (2). So sánh tốc độ của hai vật.",
            option_a="Tốc độ vật (1) nhỏ hơn tốc độ vật (2).",
            option_b="Tốc độ vật (1) lớn hơn tốc độ vật (2).",
            option_c="Tốc độ hai vật bằng nhau.",
            option_d="Không thể so sánh được.",
            correct_option="A",
            explanation="Từ p = mv không đổi, m1 > m2 thì v1 = p/m1 < p/m2 = v2 — vật khối lượng lớn hơn "
                        "phải có tốc độ nhỏ hơn để cùng động lượng.",
        ),
        # --- THÔNG HIỂU (6 câu) ---
        Part1Question(
            question_text="Trong thí nghiệm Hình 28.1 (SGK), hai viên bi A và B (bi B nặng hơn bi A) được "
                          "thả lăn từ CÙNG một độ cao trên máng trượt nên đến chân dốc với cùng tốc độ, "
                          "sau đó lần lượt va chạm vào viên bi C đang đứng yên. Nhận định nào sau đây đúng?",
            option_a="Bi A làm bi C lăn xa hơn vì bi A nhẹ nên truyền chuyển động nhanh hơn.",
            option_b="Bi B làm bi C lăn xa hơn vì cùng tốc độ nhưng bi B có khối lượng lớn hơn nên động "
                     "lượng lớn hơn.",
            option_c="Hai viên bi làm bi C lăn xa như nhau vì có cùng tốc độ khi va chạm.",
            option_d="Không xác định được vì còn phụ thuộc chất liệu viên bi.",
            correct_option="B",
            explanation="Cùng tốc độ nhưng bi B khối lượng lớn hơn nên p = mv của bi B lớn hơn, khả năng "
                        "truyền tương tác cho bi C mạnh hơn, làm bi C lăn xa hơn — đúng kết luận thí nghiệm SGK.",
        ),
        Part1Question(
            question_text="Hai vật (1) và (2) có cùng khối lượng, cùng chuyển động trên một đường thẳng; "
                          "tốc độ vật (1) lớn hơn tốc độ vật (2). So sánh độ lớn động lượng hai vật.",
            option_a="Động lượng vật (1) lớn hơn động lượng vật (2).",
            option_b="Động lượng vật (1) nhỏ hơn động lượng vật (2).",
            option_c="Động lượng hai vật bằng nhau vì cùng khối lượng.",
            option_d="Không thể so sánh vì động lượng là đại lượng vectơ.",
            correct_option="A",
            explanation="Cùng khối lượng, theo p = mv, vật có tốc độ lớn hơn thì động lượng lớn hơn.",
        ),
        Part1Question(
            question_text="Một quả bóng bay theo phương ngang đến đập vào tường rồi bật ngược trở lại với "
                          "cùng tốc độ ban đầu. Nhận định nào sau đây đúng về động lượng của quả bóng?",
            option_a="Động lượng của bóng không đổi vì tốc độ không đổi.",
            option_b="Động lượng của bóng bằng 0 sau va chạm.",
            option_c="Động lượng của bóng đổi chiều nhưng không đổi độ lớn, nên vectơ động lượng trước và "
                     "sau va chạm khác nhau.",
            option_d="Động lượng của bóng tăng gấp đôi.",
            correct_option="C",
            explanation="Động lượng là vectơ; tốc độ không đổi nhưng hướng đổi ngược lại nên vectơ động "
                        "lượng đổi chiều — vectơ động lượng trước và sau va chạm là hai vectơ khác nhau dù "
                        "cùng độ lớn.",
        ),
        Part1Question(
            question_text="Một xe tải và một xe máy đang chuyển động cùng chiều trên đường; xe tải có khối "
                          "lượng lớn hơn nhiều nhưng tốc độ nhỏ hơn xe máy. Biết hai xe có độ lớn động "
                          "lượng bằng nhau. Nhận định nào sau đây đúng?",
            option_a="Xe tải khó dừng lại hơn xe máy vì khối lượng lớn hơn.",
            option_b="Xe máy khó dừng lại hơn xe tải vì tốc độ lớn hơn.",
            option_c="Khả năng truyền tương tác (làm khó dừng lại) của hai xe là NHƯ NHAU vì có cùng động "
                     "lượng, dù khối lượng và tốc độ khác nhau.",
            option_d="Không thể so sánh vì hai xe có khối lượng khác nhau.",
            correct_option="C",
            explanation="Ý nghĩa vật lí của động lượng là đặc trưng cho khả năng truyền tương tác — hai vật "
                        "có động lượng bằng nhau thì khả năng này như nhau, bất kể tổ hợp m và v cụ thể "
                        "khác nhau thế nào.",
        ),
        Part1Question(
            question_text="Trong trò chơi mô phỏng \"bắn thiên thạch đổi hướng\", nếu tăng gấp đôi tốc độ "
                          "của tên lửa nhưng giữ nguyên khối lượng, độ lớn động lượng của tên lửa thay đổi "
                          "như thế nào?",
            option_a="Tăng gấp đôi.", option_b="Tăng gấp bốn.", option_c="Không đổi.", option_d="Giảm một nửa.",
            correct_option="A",
            explanation="p = mv; m không đổi, v tăng gấp đôi thì p tăng gấp đôi (quan hệ tỉ lệ thuận, bậc nhất).",
        ),
        Part1Question(
            question_text="Nếu tăng gấp ba khối lượng của một vật nhưng giữ nguyên tốc độ, độ lớn động "
                          "lượng của vật thay đổi như thế nào?",
            option_a="Tăng gấp ba.", option_b="Tăng gấp chín.", option_c="Không đổi.", option_d="Giảm ba lần.",
            correct_option="A",
            explanation="p = mv; v không đổi, m tăng gấp ba thì p tăng gấp ba.",
        ),
        # --- VẬN DỤNG (6 câu) ---
        Part1Question(
            question_text="Một xe tải khối lượng 3 tấn đang chuyển động với tốc độ 36 km/h. Độ lớn động "
                          "lượng của xe tải là",
            option_a="$3.10^4$ kg.m/s", option_b="$1,08.10^5$ kg.m/s",
            option_c="$3.10^3$ kg.m/s", option_d="$1,08.10^4$ kg.m/s",
            correct_option="A",
            explanation="Đổi 36 km/h = 10 m/s; p = mv = 3000×10 = 30000 = 3.10⁴ kg.m/s.",
        ),
        Part1Question(
            question_text="Một hòn đá khối lượng 500 g chuyển động với tốc độ 10 m/s. Độ lớn động lượng "
                          "của hòn đá là",
            option_a="5 kg.m/s", option_b="50 kg.m/s", option_c="0,5 kg.m/s", option_d="500 kg.m/s",
            correct_option="A",
            explanation="Đổi 500 g = 0,5 kg; p = mv = 0,5×10 = 5 kg.m/s.",
        ),
        Part1Question(
            question_text="Một cầu thủ sút một quả bóng khối lượng 450 g, ngay sau cú sút bóng bay đi với "
                          "tốc độ 20 m/s. Độ lớn động lượng của quả bóng là",
            option_a="9 kg.m/s", option_b="90 kg.m/s", option_c="0,9 kg.m/s", option_d="22,5 kg.m/s",
            correct_option="A",
            explanation="p = mv = 0,45×20 = 9 kg.m/s.",
        ),
        Part1Question(
            question_text="Một viên đạn khối lượng 8 g bay ra khỏi nòng súng với tốc độ 400 m/s. Độ lớn "
                          "động lượng của viên đạn là",
            option_a="3,2 kg.m/s", option_b="32 kg.m/s", option_c="0,32 kg.m/s", option_d="320 kg.m/s",
            correct_option="A",
            explanation="Đổi 8 g = 0,008 kg; p = mv = 0,008×400 = 3,2 kg.m/s.",
        ),
        Part1Question(
            question_text="Một xe máy khối lượng 120 kg (kể cả người lái) đang chuyển động với tốc độ "
                          "54 km/h. Độ lớn động lượng của xe máy là",
            option_a="1800 kg.m/s", option_b="6480 kg.m/s", option_c="900 kg.m/s", option_d="15 kg.m/s",
            correct_option="A",
            explanation="Đổi 54 km/h = 15 m/s; p = mv = 120×15 = 1800 kg.m/s.",
        ),
        Part1Question(
            question_text="Một xe buýt khối lượng 3 tấn đang chuyển động với tốc độ 72 km/h. Độ lớn động "
                          "lượng của xe buýt là",
            option_a="$6.10^4$ kg.m/s", option_b="$2,16.10^5$ kg.m/s",
            option_c="$3.10^3$ kg.m/s", option_d="$2,16.10^4$ kg.m/s",
            correct_option="A",
            explanation="Đổi 72 km/h = 20 m/s; p = mv = 3000×20 = 60000 = 6.10⁴ kg.m/s.",
        ),
    ],
    part2_questions=[
        Part2Question(
            question_text="Xe tải khối lượng 4 tấn và xe con khối lượng 1 tấn đang chuyển động cùng chiều "
                          "trên một đường thẳng với tốc độ lần lượt là 36 km/h và 90 km/h.",
            statement_a="Động lượng của xe tải có độ lớn bằng $4.10^4$ kg.m/s.",
            statement_b="Động lượng của xe con có độ lớn bằng $2,5.10^4$ kg.m/s.",
            statement_c="Vì xe con chạy nhanh hơn nên động lượng của xe con lớn hơn động lượng của xe tải.",
            statement_d="Hai vectơ động lượng của xe tải và xe con cùng phương, cùng chiều với nhau.",
            correct_a=True, correct_b=True, correct_c=False, correct_d=True,
            explanation="36 km/h = 10 m/s → p_tải = 4000×10 = 4.10⁴ kg.m/s (a Đúng). 90 km/h = 25 m/s → "
                        "p_con = 1000×25 = 2,5.10⁴ kg.m/s (b Đúng). So sánh 4.10⁴ > 2,5.10⁴ nên động lượng "
                        "xe tải VẪN LỚN HƠN xe con dù xe con nhanh hơn (c Sai — bẫy chỉ xét tốc độ, bỏ qua "
                        "khối lượng). Hai xe cùng chiều nên hai vectơ động lượng cùng phương, cùng chiều (d Đúng).",
        ),
        Part2Question(
            question_text="Một quả bóng tennis khối lượng 60 g bay tới đập vuông góc vào mặt vợt với tốc "
                          "độ 20 m/s, sau va chạm bật trở lại theo phương cũ với tốc độ 20 m/s.",
            statement_a="Tốc độ bóng trước và sau va chạm bằng nhau nên động lượng của bóng không đổi.",
            statement_b="Độ lớn động lượng của bóng trước va chạm bằng 1,2 kg.m/s.",
            statement_c="Vectơ động lượng của bóng sau va chạm ngược hướng với vectơ động lượng trước va chạm.",
            statement_d="Nếu quả bóng có khối lượng lớn hơn nhưng giữ nguyên tốc độ thì độ lớn động lượng "
                       "của nó sẽ lớn hơn.",
            correct_a=False, correct_b=True, correct_c=True, correct_d=True,
            explanation="Động lượng là vectơ; tốc độ không đổi nhưng hướng đổi ngược nên động lượng vẫn "
                        "thay đổi (a Sai). p = mv = 0,06×20 = 1,2 kg.m/s (b Đúng). Bóng bật ngược theo "
                        "phương cũ nên vectơ động lượng sau ngược hướng vectơ động lượng trước (c Đúng). "
                        "Từ p = mv, m tăng thì p tăng nếu v không đổi (d Đúng).",
        ),
        Part2Question(
            question_text="Trong trò chơi mô phỏng \"bắn thiên thạch đổi hướng\", có 2 phương án chế tạo "
                          "tên lửa có CÙNG độ lớn động lượng: phương án A có khối lượng lớn, tốc độ nhỏ; "
                          "phương án B có khối lượng nhỏ, tốc độ lớn.",
            statement_a="Khả năng làm thiên thạch lệch hướng của phương án A và B là như nhau vì có cùng "
                       "động lượng.",
            statement_b="Nếu tăng gấp đôi khối lượng của tên lửa phương án A (giữ nguyên tốc độ) thì động "
                       "lượng của nó tăng gấp đôi.",
            statement_c="Động lượng của tên lửa phương án B chỉ phụ thuộc vào tốc độ, không phụ thuộc khối "
                       "lượng.",
            statement_d="Cả hai phương án đều có vectơ động lượng cùng hướng với vectơ vận tốc của tên lửa.",
            correct_a=True, correct_b=True, correct_c=False, correct_d=True,
            explanation="Cùng động lượng thì khả năng truyền tương tác như nhau theo đúng ý nghĩa vật lí "
                        "của động lượng (a Đúng). p = mv, m tăng gấp đôi thì p tăng gấp đôi (b Đúng). "
                        "Động lượng LUÔN phụ thuộc cả m và v, không chỉ phụ thuộc v dù phương án B có v "
                        "lớn (c Sai — bẫy chỉ xét 1 yếu tố). Động lượng luôn cùng hướng vectơ vận tốc theo "
                        "định nghĩa (d Đúng).",
        ),
        Part2Question(
            question_text="Hai vận động viên chạy điền kinh có cùng tốc độ khi về đích: vận động viên (1) "
                          "có khối lượng 60 kg, vận động viên (2) có khối lượng 75 kg.",
            statement_a="Động lượng của vận động viên (2) lớn hơn động lượng của vận động viên (1).",
            statement_b="Tỉ số động lượng của vận động viên (2) so với vận động viên (1) bằng 75/60 = 1,25.",
            statement_c="Vì cùng tốc độ nên hai vận động viên có cùng động lượng.",
            statement_d="Vectơ động lượng của mỗi vận động viên luôn cùng hướng với vectơ vận tốc của "
                       "người đó.",
            correct_a=True, correct_b=True, correct_c=False, correct_d=True,
            explanation="Cùng tốc độ, m2 > m1 nên p2 > p1 theo p = mv (a Đúng). Tỉ số p2/p1 = m2v/(m1v) = "
                        "m2/m1 = 75/60 = 1,25 (b Đúng). Động lượng phụ thuộc cả khối lượng nên khác khối "
                        "lượng thì động lượng khác nhau dù cùng tốc độ (c Sai — bẫy chỉ xét tốc độ). Theo "
                        "định nghĩa, động lượng luôn cùng hướng vận tốc (d Đúng).",
        ),
    ],
    part3_questions=[
        Part3Question(
            question_text="Tính độ lớn động lượng của vật thứ nhất. Làm tròn kết quả đến chữ số hàng đơn "
                          "vị (đơn vị kg.m/s).",
            correct_answer="3", unit="kg.m/s",
            explanation="p₁ = m₁v₁ = 1×3 = 3 kg.m/s.",
            shared_context="Hai vật có khối lượng lần lượt là $m_1 = 1$ kg và $m_2 = 2$ kg, chuyển động "
                          "với tốc độ có độ lớn lần lượt là $v_1 = 3$ m/s và $v_2 = 2$ m/s.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng của vật thứ hai. Làm tròn kết quả đến chữ số hàng đơn vị "
                          "(đơn vị kg.m/s).",
            correct_answer="4", unit="kg.m/s",
            explanation="p₂ = m₂v₂ = 2×2 = 4 kg.m/s.",
            shared_context="Hai vật có khối lượng lần lượt là $m_1 = 1$ kg và $m_2 = 2$ kg, chuyển động "
                          "với tốc độ có độ lớn lần lượt là $v_1 = 3$ m/s và $v_2 = 2$ m/s.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng của electron. Làm tròn kết quả đến 2 chữ số có nghĩa "
                          "(đơn vị kg.m/s).",
            correct_answer="1,82.10^-23", unit="kg.m/s",
            explanation="p = mv = 9,1.10⁻³¹ × 2.10⁷ = 1,82.10⁻²³ kg.m/s.",
            shared_context="Một electron chuyển động với tốc độ $2.10^{7}$ m/s. Biết khối lượng electron "
                          "bằng $9,1.10^{-31}$ kg.",
        ),
        Part3Question(
            question_text="Tính tỉ số động lượng của xe tải so với ô tô. Làm tròn kết quả đến 2 chữ số "
                          "thập phân.",
            correct_answer="1,33", unit="",
            explanation="p_tải = 1500×10 = 15000 kg.m/s (36 km/h = 10 m/s); p_ô_tô = 750×15 = 11250 kg.m/s "
                        "(54 km/h = 15 m/s); tỉ số = 15000/11250 ≈ 1,33.",
            shared_context="Một xe tải có khối lượng 1,5 tấn chuyển động với tốc độ 36 km/h và một ô tô có "
                          "khối lượng 750 kg chuyển động ngược chiều với tốc độ 54 km/h.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng của xe tải. Làm tròn kết quả đến chữ số hàng trăm (đơn "
                          "vị kg.m/s).",
            correct_answer="15000", unit="kg.m/s",
            explanation="Đổi 36 km/h = 10 m/s; p = mv = 1500×10 = 15000 kg.m/s.",
            shared_context="Một xe tải có khối lượng 1,5 tấn chuyển động với tốc độ 36 km/h và một ô tô có "
                          "khối lượng 750 kg chuyển động ngược chiều với tốc độ 54 km/h.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng của ô tô. Làm tròn kết quả đến chữ số hàng trăm (đơn vị "
                          "kg.m/s).",
            correct_answer="11250", unit="kg.m/s",
            explanation="Đổi 54 km/h = 15 m/s; p = mv = 750×15 = 11250 kg.m/s.",
            shared_context="Một xe tải có khối lượng 1,5 tấn chuyển động với tốc độ 36 km/h và một ô tô có "
                          "khối lượng 750 kg chuyển động ngược chiều với tốc độ 54 km/h.",
        ),
    ],
    shared_constants=None,
)

assert homework.question_counts == (18, 4, 6), homework.question_counts
homework_md_path = stages.write_homework_markdown(homework, LESSON, MD_DIR)

identity = load_identity()
homework_docx = READY_DIR / f"{LESSON.slug}_bai_tap_ve_nha.docx"
export_homework(str(homework_md_path), str(homework_docx), identity, LESSON.name)

print("OK - da xuat bai tap ve nha V3 (chi Dong luong) vao", homework_docx)
