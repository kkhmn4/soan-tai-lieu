"""Soạn Bài tập về nhà cho Bài 28 - Động lượng (V2), tái sử dụng trực tiếp
`gems.docx_export.homework_exporter` + schema `gems.models.homework` (kiến
trúc gems v9.0+) — KHÔNG sửa code trong `gems/`, KHÔNG đăng ký vào
`gems/config/curriculum.yaml` (one-off, theo dac_ta_v2.md mục 2).

Nội dung bám sát SGK Vật lí 10 (Kết nối tri thức) trang 110-112: định nghĩa
động lượng p = m.v, ý nghĩa vật lí, xung lượng của lực F.Δt, liên hệ
F.Δt = Δp, dạng tổng quát định luật II Newton F = Δp/Δt. 18 câu trắc nghiệm
(Phần I) + 4 câu Đúng/Sai (Phần II) + 6 câu trả lời ngắn (Phần III), đúng
chuẩn GEMS B.4.4 (`skills/gems_physics_skill.md` mục 4.4, `.agents/agents.md`
mục 6).

Chạy: python "output/bai28_dong_luong_v2/scripts/build_homework.py"
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
    key="bai28_v2",
    name="Bài 28 - Động lượng",
    slug="bai28_dong_luong_v2",
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
            question_text="Khi một lực $F$ (không đổi) tác dụng lên một vật trong khoảng thời gian ngắn "
                          "$\\Delta t$, xung lượng của lực đó được xác định bằng biểu thức",
            option_a="$F.\\Delta t$", option_b="$F/\\Delta t$",
            option_c="$\\Delta t/F$", option_d="$F.\\Delta t^2$",
            correct_option="A",
            explanation="Theo định nghĩa SGK, xung lượng của lực F trong khoảng thời gian Δt là tích F.Δt.",
        ),
        Part1Question(
            question_text="Đơn vị của xung lượng của lực trong hệ SI là",
            option_a="N.s", option_b="N/s", option_c="N.m", option_d="kg.m/s²",
            correct_option="A",
            explanation="Từ định nghĩa xung lượng = F.Δt, đơn vị là N.s.",
        ),
        Part1Question(
            question_text="Biểu thức nào sau đây là dạng tổng quát của định luật II Newton viết theo độ "
                          "biến thiên động lượng?",
            option_a="$F = ma$", option_b="$F = \\dfrac{\\Delta p}{\\Delta t}$",
            option_c="$F = m\\Delta v$", option_d="$F = \\Delta p.\\Delta t$",
            correct_option="B",
            explanation="Từ F.Δt = Δp suy ra F = Δp/Δt — dạng tổng quát của định luật II Newton (công thức 28.4 SGK).",
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
            question_text="Khi bắt bóng, nếu thủ môn co tay lại và lùi người theo hướng bóng bay thay vì "
                          "giữ tay cứng, tay thủ môn sẽ đỡ đau hơn. Giải thích nào đúng về mặt vật lí?",
            option_a="Vì động lượng của quả bóng đã giảm trước khi chạm tay.",
            option_b="Vì hành động đó làm giảm độ biến thiên động lượng của quả bóng.",
            option_c="Vì hành động đó làm tăng thời gian tương tác Δt, trong khi độ biến thiên động lượng "
                     "gần như không đổi, nên theo F = Δp/Δt, lực trung bình tác dụng lên tay giảm.",
            option_d="Vì hành động đó làm giảm xung lượng của lực mà tay tác dụng lên bóng.",
            correct_option="C",
            explanation="Δp của bóng gần như không đổi; theo F = Δp/Δt, Δt tăng thì F giảm — đúng bản chất "
                        "vật lí câu hỏi 2 mục II.2 SGK trang 112.",
        ),
        Part1Question(
            question_text="Đồ thị biểu diễn độ lớn của một lực không đổi theo thời gian tác dụng có dạng "
                          "một hình chữ nhật (trục tung là F, trục hoành là t, trong khoảng Δt). Diện tích "
                          "hình chữ nhật đó biểu diễn đại lượng nào?",
            option_a="Công của lực.", option_b="Độ lớn xung lượng của lực.",
            option_c="Độ lớn vận tốc của vật.", option_d="Động năng của vật.",
            correct_option="B",
            explanation="Diện tích hình chữ nhật = F × Δt, đúng bằng độ lớn xung lượng của lực.",
        ),
        Part1Question(
            question_text="Một quả bóng bay theo phương ngang đến đập vào tường rồi bật ngược trở lại với "
                          "cùng tốc độ ban đầu. Nhận định nào sau đây đúng?",
            option_a="Động lượng của bóng không đổi vì tốc độ không đổi.",
            option_b="Động lượng của bóng bằng 0 sau va chạm.",
            option_c="Động lượng của bóng đổi chiều nhưng không đổi độ lớn, nên vẫn có độ biến thiên động "
                     "lượng khác 0.",
            option_d="Động lượng của bóng tăng gấp đôi.",
            correct_option="C",
            explanation="Động lượng là vectơ; tốc độ không đổi nhưng hướng đổi ngược lại nên vectơ động "
                        "lượng đổi chiều, dẫn tới Δp ≠ 0 dù độ lớn động lượng trước/sau bằng nhau.",
        ),
        Part1Question(
            question_text="Khi đóng cọc bằng búa máy, để cọc lún sâu hơn sau mỗi nhát búa, người ta thường "
                          "làm búa đạt tốc độ lớn hơn khi chạm cọc, thay vì kéo dài thời gian va chạm. Giải "
                          "thích nào hợp lí nhất?",
            option_a="Búa tốc độ lớn hơn có động lượng lớn hơn, dẫn tới độ biến thiên động lượng truyền cho "
                     "cọc lớn hơn, nên xung lượng của lực búa tác dụng lên cọc lớn hơn.",
            option_b="Thời gian va chạm giữa búa và cọc không ảnh hưởng đến lực tác dụng lên cọc.",
            option_c="Tốc độ của búa không liên quan đến động lượng.",
            option_d="Xung lượng của lực chỉ phụ thuộc thời gian va chạm, không phụ thuộc tốc độ búa.",
            correct_option="A",
            explanation="Búa tốc độ lớn hơn có động lượng lớn hơn; khi va chạm dừng đột ngột, độ biến thiên "
                        "động lượng lớn hơn nên xung lượng lực (F.Δt = Δp) tác dụng lên cọc cũng lớn hơn.",
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
            question_text="Một quả bóng khối lượng 300 g bay đến đập vuông góc vào tường với tốc độ 10 m/s "
                          "rồi bật ngược trở lại theo phương cũ với tốc độ 8 m/s. Độ lớn độ biến thiên động "
                          "lượng của quả bóng là",
            option_a="5,4 kg.m/s", option_b="0,6 kg.m/s", option_c="3,0 kg.m/s", option_d="1,8 kg.m/s",
            correct_option="A",
            explanation="Do đổi chiều nên Δp = m(v1+v2) = 0,3×(10+8) = 5,4 kg.m/s.",
        ),
        Part1Question(
            question_text="Một ô tô khối lượng 1,5 tấn đang chuyển động với tốc độ 54 km/h thì hãm phanh, "
                          "chuyển động chậm dần rồi dừng hẳn sau 5 s. Độ lớn lực hãm trung bình tác dụng "
                          "lên xe là",
            option_a="4500 N", option_b="8100 N", option_c="450 N", option_d="22500 N",
            correct_option="A",
            explanation="54 km/h = 15 m/s; Δp = 1500×15 = 22500 kg.m/s; F = Δp/Δt = 22500/5 = 4500 N.",
        ),
        Part1Question(
            question_text="Một cầu thủ sút một quả bóng khối lượng 450 g đang nằm yên; thời gian chân cầu "
                          "thủ tiếp xúc với bóng là 0,05 s, ngay sau cú sút bóng bay đi với tốc độ 20 m/s. "
                          "Độ lớn lực trung bình mà chân cầu thủ tác dụng lên bóng là",
            option_a="180 N", option_b="9 N", option_c="45 N", option_d="900 N",
            correct_option="A",
            explanation="Δp = mv = 0,45×20 = 9 kg.m/s; F = Δp/Δt = 9/0,05 = 180 N.",
        ),
        Part1Question(
            question_text="Một vật khối lượng 2 kg đang chuyển động thẳng với tốc độ 3 m/s thì chịu tác "
                          "dụng của một lực không đổi cùng hướng chuyển động trong 2 s, làm tốc độ vật tăng "
                          "lên 9 m/s. Độ lớn lực tác dụng lên vật là",
            option_a="6 N", option_b="3 N", option_c="12 N", option_d="18 N",
            correct_option="A",
            explanation="Δv = 9-3 = 6 m/s; Δp = 2×6 = 12 kg.m/s; F = Δp/Δt = 12/2 = 6 N.",
        ),
        Part1Question(
            question_text="Một viên đạn khối lượng 8 g bay ra khỏi nòng súng với tốc độ 400 m/s. Độ lớn "
                          "động lượng của viên đạn là",
            option_a="3,2 kg.m/s", option_b="32 kg.m/s", option_c="0,32 kg.m/s", option_d="320 kg.m/s",
            correct_option="A",
            explanation="Đổi 8 g = 0,008 kg; p = mv = 0,008×400 = 3,2 kg.m/s.",
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
                          "độ 20 m/s, sau va chạm bật trở lại theo phương cũ với tốc độ 20 m/s (coi va chạm "
                          "là đàn hồi, bỏ qua các lực khác trong lúc va chạm).",
            statement_a="Tốc độ bóng trước và sau va chạm bằng nhau nên động lượng của bóng không đổi.",
            statement_b="Độ biến thiên động lượng của bóng có độ lớn bằng 2,4 kg.m/s.",
            statement_c="Vectơ động lượng của bóng sau va chạm ngược hướng với vectơ động lượng trước va chạm.",
            statement_d="Nếu thời gian va chạm giữa bóng và mặt vợt càng ngắn thì lực mặt vợt tác dụng lên "
                       "bóng càng nhỏ.",
            correct_a=False, correct_b=True, correct_c=True, correct_d=False,
            explanation="Động lượng là vectơ; tốc độ không đổi nhưng hướng đổi ngược nên động lượng vẫn "
                        "thay đổi (a Sai). Δp = m(v1+v2) = 0,06×(20+20) = 2,4 kg.m/s (b Đúng). Bóng bật "
                        "ngược theo phương cũ nên vectơ động lượng sau ngược hướng vectơ động lượng trước "
                        "(c Đúng). Theo F = Δp/Δt, với Δp không đổi, Δt càng ngắn thì F càng LỚN, không "
                        "phải càng nhỏ (d Sai).",
        ),
        Part2Question(
            question_text="Một vật khối lượng 600 g đang đứng yên thì chịu tác dụng của một lực không đổi "
                          "theo phương ngang trong khoảng thời gian 0,3 s, sau đó vật đạt tốc độ 5 m/s.",
            statement_a="Độ biến thiên động lượng của vật có độ lớn bằng 3 kg.m/s.",
            statement_b="Độ lớn lực trung bình tác dụng lên vật bằng 10 N.",
            statement_c="Nếu thời gian tác dụng lực tăng gấp đôi (0,6 s) mà vật vẫn đạt tốc độ 5 m/s như "
                       "trên thì độ lớn lực trung bình cần thiết giảm đi một nửa.",
            statement_d="Xung lượng của lực tác dụng lên vật trong 0,3 s có độ lớn bằng 10 N.s.",
            correct_a=True, correct_b=True, correct_c=True, correct_d=False,
            explanation="Δp = mΔv = 0,6×5 = 3 kg.m/s (a Đúng). F = Δp/Δt = 3/0,3 = 10 N (b Đúng). Δp cố "
                        "định = 3 kg.m/s, Δt tăng gấp đôi thì F = 3/0,6 = 5 N, giảm một nửa so với 10 N "
                        "(c Đúng). Xung lượng của lực trong 0,3 s CHÍNH LÀ độ biến thiên động lượng = 3 "
                        "N.s, không phải 10 N.s — 10 N là giá trị của lực F, không phải xung lượng F.Δt "
                        "(d Sai, bẫy nhầm giữa giá trị F và giá trị F.Δt).",
        ),
        Part2Question(
            question_text="Trong môn quyền anh (boxing), khi bị đấm trúng mặt, võ sĩ thường có phản xạ ngả "
                          "đầu ra sau theo hướng cú đấm thay vì giữ đầu cố định.",
            statement_a="Việc ngả đầu ra sau giúp kéo dài thời gian tương tác Δt giữa nắm đấm và mặt.",
            statement_b="Độ biến thiên động lượng mà nắm đấm truyền cho phần đầu không đổi thì khi Δt tăng, "
                       "lực tác dụng trung bình F sẽ giảm.",
            statement_c="Việc ngả đầu ra sau làm giảm động lượng ban đầu của cú đấm nên sẽ đỡ đau hơn.",
            statement_d="Nguyên tắc trên tương tự nguyên lí hoạt động của túi khí trên ô tô: kéo dài thời "
                       "gian va chạm để giảm lực tác dụng lên người ngồi trong xe.",
            correct_a=True, correct_b=True, correct_c=False, correct_d=True,
            explanation="Ngả đầu ra sau kéo dài Δt (a Đúng), theo F = Δp/Δt thì F giảm khi Δt tăng và Δp "
                        "không đổi (b Đúng). Bản chất KHÔNG phải giảm động lượng của cú đấm mà là kéo dài "
                        "thời gian tương tác để giảm lực trung bình (c Sai). Túi khí ô tô hoạt động theo "
                        "đúng nguyên lí kéo dài Δt để giảm F (d Đúng).",
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
            question_text="Tính độ lớn xung lượng của lực mà quả bóng gôn nhận được. Làm tròn kết quả đến "
                          "chữ số hàng phần mười (đơn vị N.s).",
            correct_answer="3,2", unit="N.s",
            explanation="Xung lượng của lực = độ biến thiên động lượng: F.Δt = Δp = mv - 0 = 0,046×70 = 3,22 ≈ 3,2 N.s.",
            shared_context="Một quả bóng gôn khối lượng 46 g đang nằm yên, sau một cú đánh quả bóng bay lên "
                          "với tốc độ 70 m/s. Thời gian tác dụng lực là $0,5.10^{-3}$ s.",
        ),
        Part3Question(
            question_text="Tính độ lớn trung bình của lực tác dụng vào quả bóng. Làm tròn kết quả đến chữ "
                          "số hàng đơn vị (đơn vị N).",
            correct_answer="6440", unit="N",
            explanation="F = Δp/Δt = 3,22/(0,5.10⁻³) = 6440 N.",
            shared_context="Một quả bóng gôn khối lượng 46 g đang nằm yên, sau một cú đánh quả bóng bay lên "
                          "với tốc độ 70 m/s. Thời gian tác dụng lực là $0,5.10^{-3}$ s.",
        ),
        Part3Question(
            question_text="Tính độ lớn động lượng ban đầu của xe. Làm tròn kết quả đến chữ số hàng trăm "
                          "(đơn vị kg.m/s).",
            correct_answer="15000", unit="kg.m/s",
            explanation="Đổi 54 km/h = 15 m/s; p = mv = 1000×15 = 15000 kg.m/s.",
            shared_context="Một ô tô khối lượng 1 tấn đang chuyển động thẳng với tốc độ 54 km/h thì người "
                          "lái xe đạp phanh, lực hãm trung bình tác dụng lên xe có độ lớn 3000 N (coi lực "
                          "hãm không đổi).",
        ),
        Part3Question(
            question_text="Tính thời gian tối thiểu để xe dừng hẳn kể từ lúc đạp phanh. Làm tròn kết quả "
                          "đến chữ số hàng phần mười (đơn vị s).",
            correct_answer="5,0", unit="s",
            explanation="Δt = Δp/F = 15000/3000 = 5,0 s.",
            shared_context="Một ô tô khối lượng 1 tấn đang chuyển động thẳng với tốc độ 54 km/h thì người "
                          "lái xe đạp phanh, lực hãm trung bình tác dụng lên xe có độ lớn 3000 N (coi lực "
                          "hãm không đổi).",
        ),
    ],
    shared_constants=None,
)

assert homework.question_counts == (18, 4, 6), homework.question_counts
homework_md_path = stages.write_homework_markdown(homework, LESSON, MD_DIR)

identity = load_identity()
homework_docx = READY_DIR / f"{LESSON.slug}_bai_tap_ve_nha.docx"
export_homework(str(homework_md_path), str(homework_docx), identity, LESSON.name)

print("OK - da xuat bai tap ve nha V2 vao", homework_docx)
