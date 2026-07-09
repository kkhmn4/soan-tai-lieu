/**
 * Dựng 2 bộ Slide cho Bài 28 - Động lượng từ CHUNG một mảng OUTLINE dữ liệu,
 * đảm bảo nội dung/ảnh minh họa đồng bộ tuyệt đối giữa 2 bộ (thay vì để
 * NotebookLM tự vẽ độc lập 2 lần, từng gây lệch màu/layout ở lần trước).
 *
 * - Slide GIÁO VIÊN (mau/*.png, theme Anthropic màu sắc): slide Nhiệm vụ CHỈ
 *   có Hướng dẫn thực hiện, KHÔNG có câu hỏi. Slide Đáp án CHỈ có đáp án +
 *   ảnh minh họa, KHÔNG có hướng dẫn.
 * - Slide PHIẾU HỌC TẬP học sinh (xam/*.png, nền trắng): slide Nhiệm vụ có
 *   ĐẦY ĐỦ hướng dẫn + câu hỏi (giống hệt PHT giấy). Slide Đáp án giống hệt
 *   slide Đáp án bên Giáo viên (cùng nội dung, cùng ảnh) — chỉ khác tông màu.
 *
 * Chạy: node "output/bai28_dong_luong/scripts/build_slides.js"
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const IMG_MAU = path.join(ROOT, "ready", "hinh_anh", "mau");
const IMG_XAM = path.join(ROOT, "ready", "hinh_anh", "xam");
const OUT_DIR = path.join(ROOT, "ready");

// ============================================================
// THEME
// ============================================================
const TEACHER = {
  key: "teacher",
  bgDark: "141413", bgLight: "FAF9F5", textOnDark: "FAF9F5", textOnLight: "141413",
  orange: "D97757", blue: "6A9BCC", green: "788C5D", grayLine: "B0AEA5", grayBox: "E8E6DC",
  headFont: "Arial Black", bodyFont: "Georgia",
  imgDir: IMG_MAU,
};
const STUDENT = {
  key: "student",
  bgDark: "FFFFFF", bgLight: "FFFFFF", textOnDark: "1A1A1A", textOnLight: "1A1A1A",
  orange: "595959", blue: "404040", green: "737373", grayLine: "BFBFBF", grayBox: "F2F2F2",
  headFont: "Times New Roman", bodyFont: "Times New Roman",
  imgDir: IMG_XAM,
};

const W = 10, H = 5.625; // LAYOUT_16x9

// ============================================================
// OUTLINE (dữ liệu dùng chung tuyệt đối cho cả 2 deck)
// ============================================================
const OUTLINE = [
  { type: "section", number: "1", title: "KHỞI ĐỘNG" },
  {
    type: "pair",
    taskLabel: "a) Tình huống 1  ·  b) Tình huống 2",
    instructions: "Hoạt động cá nhân, 3 phút, quan sát hình ảnh GV trình chiếu và đọc phần mở bài SGK trang 110.",
    question: [
      "a) Xe tải và xe con đang chạy cạnh nhau với CÙNG một tốc độ. Khi đèn tín hiệu chuyển đỏ, xe nào cần một lực hãm (phanh) lớn hơn để dừng lại trong cùng một khoảng thời gian? Vì sao?",
      "b) Trong pha sút phạt 11 m, thủ môn khó bắt bóng hơn khi bóng bay tới với tốc độ lớn hay tốc độ nhỏ? Vì sao?",
    ],
    answerLabel: "c) Dự đoán",
    answer: [
      "Xe tải (khối lượng lớn) cần lực hãm lớn hơn xe con dù cùng tốc độ.",
      "Bóng bay với tốc độ càng lớn thì thủ môn càng khó bắt.",
      "→ Cả khối lượng lẫn tốc độ đều ảnh hưởng đến \"khả năng gây khó khăn khi làm vật dừng lại/đổi hướng\".",
      "Chúng ta sẽ tìm hiểu đại lượng đặc trưng cho điều này qua bài học hôm nay: ĐỘNG LƯỢNG.",
    ],
  },

  { type: "section", number: "2", title: "HÌNH THÀNH KIẾN THỨC MỚI" },
  { type: "subsection", number: "2.1", title: "Động lượng" },
  {
    type: "pair",
    taskLabel: "Nhiệm vụ — Thí nghiệm ba viên bi A, B, C",
    instructions: "Hoạt động nhóm 4–5 học sinh, 7 phút, dùng bộ dụng cụ thí nghiệm (máng trượt + 3 viên bi A, B, C — bi B nặng hơn bi A), đọc mục I SGK trang 110–111.",
    question: [
      "Thí nghiệm 1: Lần lượt thả bi A rồi bi B từ CÙNG một độ cao (cùng tốc độ khi tới chân dốc). Đo quãng đường bi C dịch chuyển sau mỗi lần va chạm.",
      "Thí nghiệm 2: Chỉ thả bi A, nhưng tăng độ dốc của máng trượt. Đo quãng đường bi C dịch chuyển sau mỗi lần va chạm.",
      "Thảo luận: (a) Viên bi nào làm bi C lăn xa hơn trong TN1? (b) Ứng với độ dốc nào bi C lăn xa hơn trong TN2? (c) Kết luận: khả năng truyền chuyển động phụ thuộc yếu tố nào?",
    ],
    answerLabel: "Kết luận thí nghiệm",
    answer: [
      "TN1: bi B (nặng hơn) làm bi C lăn xa hơn dù cùng tốc độ — khối lượng càng lớn, khả năng truyền chuyển động càng mạnh.",
      "TN2: độ dốc càng cao, bi A đến chân dốc với tốc độ càng lớn, làm bi C lăn càng xa — tốc độ càng lớn, khả năng truyền chuyển động càng mạnh.",
      "→ Khả năng truyền chuyển động (động lượng) phụ thuộc CẢ khối lượng lẫn tốc độ của vật.",
    ],
    image: "so_do_thi_nghiem_bi_abc.png",
  },
  {
    type: "theory",
    label: "2.1.b  Kiến thức trọng tâm",
    blanks: [
      "Định nghĩa: động lượng của vật khối lượng m chuyển động với vận tốc v là p = (1) …………",
      "Đặc điểm: động lượng là đại lượng (2) …………, luôn (3) ………… với vectơ vận tốc của vật.",
      "Đơn vị: (4) …………",
      "Ý nghĩa vật lí: đặc trưng cho (5) ………… giữa các vật khi va chạm.",
    ],
    filled: [
      "Định nghĩa: p = m.v (dạng vectơ)",
      "Đặc điểm: động lượng là đại lượng vectơ, luôn cùng phương, cùng chiều với vectơ vận tốc.",
      "Đơn vị: kg.m/s",
      "Ý nghĩa vật lí: đặc trưng cho khả năng truyền tương tác (truyền chuyển động) giữa các vật khi va chạm.",
    ],
    image: "vecto_dong_luong.png",
  },

  { type: "subsection", number: "2.2", title: "Xung lượng của lực" },
  {
    type: "pair",
    taskLabel: "Nhiệm vụ 1 — Đọc đồ thị lực – thời gian",
    instructions: "Hoạt động nhóm 4 học sinh, 7 phút, quan sát đồ thị lực – thời gian và đọc mục II.1 SGK trang 111.",
    question: [
      "a) Diện tích phần tô màu trên đồ thị được tính bằng biểu thức nào theo F và Δt = t₂ – t₁?",
      "b) Đại lượng đó được gọi là gì trong Vật lí? Nêu đơn vị.",
      "c) Liên hệ thực tế: tại sao thủ môn co tay và lùi người khi bắt bóng giúp đỡ đau tay hơn?",
    ],
    answerLabel: "Đáp án — Nhiệm vụ 1",
    answer: [
      "a) Diện tích = F.Δt",
      "b) Đó là xung lượng của lực. Đơn vị: N.s",
      "c) Hành động đó làm TĂNG Δt, trong khi độ biến thiên động lượng gần như không đổi → lực trung bình tác dụng lên tay GIẢM.",
    ],
    image: "do_thi_luc_thoi_gian.png",
  },
  {
    type: "pair",
    taskLabel: "Nhiệm vụ 2 — Suy luận công thức liên hệ",
    instructions: "Hoạt động cá nhân 3 phút, sau đó thảo luận chung cả lớp 2 phút, dựa vào định luật II Newton F = m.a đã học ở Bài 15.",
    question: [
      "a) Viết biểu thức gia tốc a của vật theo v₁, v₂, Δt.",
      "b) Thay vào định luật II Newton F = m.a, biến đổi để đưa F.Δt về dạng chứa m.v₂ và m.v₁.",
      "c) Nhận xét: m.v₂ và m.v₁ là động lượng ở hai thời điểm nào? Phát biểu mối liên hệ F.Δt và Δp = p₂ – p₁.",
      "d) Viết lại định luật II Newton dưới dạng tổng quát theo Δp và Δt.",
    ],
    answerLabel: "Đáp án — Nhiệm vụ 2",
    answer: [
      "a) a = (v₂ – v₁)/Δt",
      "b) F.Δt = m.v₂ – m.v₁",
      "c) m.v₂ = p₂ (động lượng lúc sau), m.v₁ = p₁ (động lượng lúc đầu) → F.Δt = Δp = p₂ – p₁",
      "d) F = Δp/Δt (dạng tổng quát của định luật II Newton)",
    ],
  },
  {
    type: "theory",
    label: "2.2.b  Kiến thức trọng tâm",
    blanks: [
      "Xung lượng của lực: F (không đổi) tác dụng trong Δt ngắn → tích (1) ………… gọi là xung lượng. Đơn vị: (2) …………",
      "Liên hệ với độ biến thiên động lượng: F.Δt = (3) …………",
      "Dạng tổng quát của định luật II Newton: (4) …………",
    ],
    filled: [
      "Xung lượng của lực: F.Δt, đơn vị N.s",
      "Liên hệ: F.Δt = Δp = p₂ – p₁",
      "Dạng tổng quát định luật II Newton: F = Δp/Δt",
    ],
    image: "do_thi_luc_thoi_gian.png",
  },

  { type: "section", number: "3", title: "LUYỆN TẬP" },
  {
    type: "pair",
    taskLabel: "3.1  Động lượng",
    instructions: "Hoạt động cá nhân, 5 phút, tài liệu: PHT mục 3.1.",
    question: [
      "Một xe máy khối lượng 120 kg (kể cả người lái) đang chuyển động với tốc độ 54 km/h. Độ lớn động lượng của xe máy là",
      "A. 1800 kg.m/s     B. 6480 kg.m/s     C. 900 kg.m/s     D. 15 kg.m/s",
    ],
    answerLabel: "Đáp án 3.1",
    answer: ["Chọn A. Đổi 54 km/h = 15 m/s; p = m.v = 120 × 15 = 1800 kg.m/s."],
  },
  {
    type: "pair",
    taskLabel: "3.2  Xung lượng của lực",
    instructions: "Hoạt động cá nhân, 5 phút, tài liệu: PHT mục 3.2.",
    question: [
      "Một quả bóng bàn khối lượng 2,7 g bay tới đập vuông góc vào mặt vợt với tốc độ 15 m/s rồi bật ngược trở lại với tốc độ 12 m/s. Thời gian va chạm là 2.10⁻³ s. Tính độ lớn lực trung bình mà vợt tác dụng lên bóng.",
    ],
    answerLabel: "Đáp án 3.2",
    answer: [
      "Δp = m(v₁+v₂) = 0,0027 × (15+12) = 0,0729 kg.m/s",
      "F = Δp/Δt = 0,0729 / 0,002 ≈ 36 N",
    ],
  },

  { type: "section", number: "4", title: "VẬN DỤNG - MỞ RỘNG" },
  {
    type: "reading",
    label: "4.1  Động lượng — Mở rộng",
    text: "Động lượng là nền tảng của nguyên lí phóng tên lửa: tên lửa đẩy khí nóng phụt ra phía sau với tốc độ rất lớn để tự thân nó thu được động lượng theo chiều ngược lại (bay lên phía trước). Đây là ý tưởng mở đầu cho Định luật bảo toàn động lượng — Bài 29.",
  },
  {
    type: "pair",
    taskLabel: "4.2.a  Nhiệm vụ vận dụng — Mũ bảo hiểm lót thép",
    instructions: "Hoạt động nhóm đôi, 7 phút, dựa vào công thức F = Δp/Δt vừa học ở mục 2.2.",
    question: [
      "Một kĩ sư đề xuất thiết kế mũ bảo hiểm gắn thêm lớp lót bằng THÉP CỨNG sát da đầu (thay cho lớp xốp EPS êm), với lí do \"thép cứng chịu lực tốt hơn xốp nên bảo vệ đầu tốt hơn\".",
      "a) Dựa vào F = Δp/Δt, chỉ ra điểm bất hợp lí trong lí do trên.",
      "b) Đề xuất cách khắc phục đúng nguyên lí vật lí.",
    ],
    answerLabel: "Đáp án 4.2.a",
    answer: [
      "a) Lớp thép cứng làm Δt (thời gian va chạm) rất nhỏ → với cùng Δp, lực F tác dụng lên đầu lại RẤT LỚN — ngược với mục đích bảo vệ.",
      "b) Lớp xốp EPS êm giúp KÉO DÀI Δt lúc va chạm, làm giảm lực F tác dụng lên đầu — đúng nguyên lí F = Δp/Δt.",
    ],
  },
  {
    type: "reading",
    label: "4.2.b  Xung lượng của lực — Mở rộng",
    text: "Nguyên lí \"kéo dài Δt để giảm lực F khi Δp không đổi\" được ứng dụng trong an toàn giao thông: túi khí ô tô bung ra và xẹp từ từ trong 30–50 mili giây khi va chạm, kéo dài thời gian tương tác giữa người và vô-lăng, nhờ đó giảm mạnh lực tác dụng lên cơ thể. Dây an toàn co giãn nhẹ cũng hoạt động theo cùng nguyên lí này.",
  },

  {
    type: "mindmap",
    bullets: [
      "Động lượng: p = m.v (vectơ, cùng hướng v, đơn vị kg.m/s)",
      "Xung lượng của lực: F.Δt (đơn vị N.s)",
      "Liên hệ: F.Δt = Δp = p₂ – p₁",
      "Dạng tổng quát định luật II Newton: F = Δp/Δt",
    ],
  },
];

// ============================================================
// HÀM DỰNG SLIDE
// ============================================================
function addBackground(slide, theme, dark) {
  slide.background = { color: dark ? theme.bgDark : theme.bgLight };
}

function addFooter(slide, theme, text) {
  slide.addText(text, {
    x: 0.4, y: H - 0.35, w: W - 0.8, h: 0.3, fontSize: 10, color: theme.grayLine,
    fontFace: theme.bodyFont, align: "left",
  });
}

function addCover(pres, theme, deck) {
  const slide = pres.addSlide();
  addBackground(slide, theme, true);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 2.55, w: W, h: 0.06, fill: { color: theme.orange } });
  slide.addText("BÀI 28 – ĐỘNG LƯỢNG", {
    x: 0.6, y: 1.7, w: W - 1.2, h: 1.0, fontSize: 40, bold: true, color: theme.textOnDark,
    fontFace: theme.headFont, align: "left",
  });
  if (deck === "teacher") {
    slide.addText("Slide bài giảng  ·  Vật lí 10 – Kết nối tri thức với cuộc sống", {
      x: 0.6, y: 2.75, w: W - 1.2, h: 0.5, fontSize: 16, color: theme.grayLine, fontFace: theme.bodyFont,
    });
    slide.addText("Giáo viên thực hiện: Kha Khung Hiệp", {
      x: 0.6, y: 3.3, w: W - 1.2, h: 0.4, fontSize: 14, italic: true, color: theme.orange, fontFace: theme.bodyFont,
    });
  } else {
    slide.addText("PHIẾU HỌC TẬP  ·  Vật lí 10 – Kết nối tri thức với cuộc sống", {
      x: 0.6, y: 2.75, w: W - 1.2, h: 0.5, fontSize: 16, color: "595959", fontFace: theme.bodyFont,
    });
    slide.addText("Họ và tên học sinh: ..........................................        Lớp: ................", {
      x: 0.6, y: 3.35, w: W - 1.2, h: 0.4, fontSize: 14, color: "1A1A1A", fontFace: theme.bodyFont,
    });
  }
}

function addSection(pres, theme, item) {
  const slide = pres.addSlide();
  addBackground(slide, theme, true);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: H, fill: { color: theme.orange } });
  slide.addText(item.number, {
    x: 0.7, y: 1.7, w: 2.0, h: 1.5, fontSize: 72, bold: true, color: theme.orange, fontFace: theme.headFont,
  });
  slide.addText(item.title, {
    x: 0.7, y: 3.1, w: W - 1.4, h: 1.0, fontSize: 30, bold: true, color: theme.textOnDark, fontFace: theme.headFont,
  });
}

function addSubsection(pres, theme, item) {
  const slide = pres.addSlide();
  addBackground(slide, theme, false);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.3, w: 1.6, h: 1.0, fill: { color: theme.blue } });
  slide.addText(item.number, {
    x: 0.6, y: 2.3, w: 1.6, h: 1.0, fontSize: 28, bold: true, color: theme.bgDark === "141413" ? "141413" : "FFFFFF",
    fontFace: theme.headFont, align: "center", valign: "middle",
  });
  slide.addText(item.title, {
    x: 2.4, y: 2.3, w: W - 3.0, h: 1.0, fontSize: 30, bold: true, color: theme.textOnLight, fontFace: theme.headFont,
    valign: "middle",
  });
}

function addBulletText(slide, lines, opts) {
  const items = lines.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < lines.length - 1 } }));
  slide.addText(items, opts);
}

function addTaskSlide(pres, theme, deck, item) {
  const slide = pres.addSlide();
  addBackground(slide, theme, false);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.85, fill: { color: theme.blue } });
  slide.addText(item.taskLabel, {
    x: 0.5, y: 0, w: W - 1.0, h: 0.85, fontSize: 20, bold: true,
    color: theme.key === "teacher" ? "141413" : "FFFFFF", fontFace: theme.headFont, valign: "middle",
  });
  slide.addText([
    { text: "Hướng dẫn thực hiện: ", options: { bold: true, breakLine: false } },
    { text: item.instructions, options: { italic: true } },
  ], {
    x: 0.5, y: 1.05, w: W - 1.0, h: 0.8, fontSize: 13, color: theme.textOnLight, fontFace: theme.bodyFont,
  });
  if (deck === "student") {
    addBulletText(slide, item.question, {
      x: 0.5, y: 1.85, w: W - 1.0, h: H - 2.2, fontSize: 13, color: theme.textOnLight, fontFace: theme.bodyFont,
      valign: "top", paraSpaceAfter: 8,
    });
  } else {
    slide.addShape(pres.shapes.OVAL, {
      x: W - 2.3, y: 2.2, w: 1.6, h: 1.6, fill: { color: theme.grayBox }, line: { color: theme.orange, width: 2 },
    });
    slide.addText("!", {
      x: W - 2.3, y: 2.2, w: 1.6, h: 1.6, fontSize: 48, bold: true, color: theme.orange, align: "center",
      valign: "middle", fontFace: theme.headFont,
    });
    slide.addText("Học sinh tự đọc câu hỏi trong Phiếu học tập", {
      x: 0.5, y: 3.9, w: W - 3.0, h: 0.6, fontSize: 12, italic: true, color: theme.grayLine, fontFace: theme.bodyFont,
    });
  }
  addFooter(slide, theme, deck === "teacher" ? "Slide Giáo viên" : "Slide Phiếu học tập");
}

function addAnswerSlide(pres, theme, deck, item, labelOverride) {
  const slide = pres.addSlide();
  addBackground(slide, theme, false);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.85, fill: { color: theme.green } });
  slide.addText(labelOverride || item.answerLabel, {
    x: 0.5, y: 0, w: W - 1.0, h: 0.85, fontSize: 20, bold: true,
    color: theme.key === "teacher" ? "141413" : "FFFFFF", fontFace: theme.headFont, valign: "middle",
  });
  const hasImage = !!item.image;
  const textW = hasImage ? 5.6 : W - 1.0;
  addBulletText(slide, item.answer, {
    x: 0.5, y: 1.1, w: textW, h: H - 1.5, fontSize: 13, color: theme.textOnLight, fontFace: theme.bodyFont,
    valign: "top", paraSpaceAfter: 8,
  });
  if (hasImage) {
    slide.addImage({ path: path.join(theme.imgDir, item.image), x: 6.3, y: 1.1, w: 3.2, h: 3.2, sizing: { type: "contain", w: 3.2, h: 3.2 } });
  }
  addFooter(slide, theme, deck === "teacher" ? "Slide Giáo viên" : "Slide Phiếu học tập");
}

function addTheorySlides(pres, theme, deck, item) {
  // Slide 1: điền khuyết (giống nhau cả 2 deck, chỉ khác tông màu)
  let slide = pres.addSlide();
  addBackground(slide, theme, false);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.85, fill: { color: theme.blue } });
  slide.addText(item.label, {
    x: 0.5, y: 0, w: W - 1.0, h: 0.85, fontSize: 20, bold: true,
    color: theme.key === "teacher" ? "141413" : "FFFFFF", fontFace: theme.headFont, valign: "middle",
  });
  addBulletText(slide, item.blanks, {
    x: 0.5, y: 1.1, w: item.image ? 5.6 : W - 1.0, h: H - 1.5, fontSize: 13, color: theme.textOnLight,
    fontFace: theme.bodyFont, valign: "top", paraSpaceAfter: 10,
  });
  if (item.image) {
    slide.addImage({ path: path.join(theme.imgDir, item.image), x: 6.3, y: 1.1, w: 3.2, h: 3.2, sizing: { type: "contain", w: 3.2, h: 3.2 } });
  }
  addFooter(slide, theme, deck === "teacher" ? "Slide Giáo viên" : "Slide Phiếu học tập");

  // Slide 2: đáp án đầy đủ
  addAnswerSlide(pres, theme, deck, { answer: item.filled, image: item.image }, item.label + " — Đáp án");
}

function addReadingSlide(pres, theme, deck, item) {
  const slide = pres.addSlide();
  addBackground(slide, theme, false);
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.85, fill: { color: theme.orange } });
  slide.addText(item.label, {
    x: 0.5, y: 0, w: W - 1.0, h: 0.85, fontSize: 20, bold: true,
    color: theme.key === "teacher" ? "141413" : "FFFFFF", fontFace: theme.headFont, valign: "middle",
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.3, w: W - 1.0, h: 3.0, fill: { color: theme.grayBox }, line: { color: theme.grayLine, width: 1 },
  });
  slide.addText(item.text, {
    x: 0.8, y: 1.5, w: W - 1.6, h: 2.6, fontSize: 14, italic: true, color: theme.textOnLight,
    fontFace: theme.bodyFont, valign: "top",
  });
  addFooter(slide, theme, deck === "teacher" ? "Slide Giáo viên" : "Slide Phiếu học tập");
}

function addMindmapSlide(pres, theme, item) {
  const slide = pres.addSlide();
  addBackground(slide, theme, true);
  slide.addText("TỔNG KẾT BÀI HỌC", {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.7, fontSize: 26, bold: true, color: theme.orange, fontFace: theme.headFont,
  });
  const colors = [theme.orange, theme.blue, theme.green, theme.grayLine];
  item.bullets.forEach((t, i) => {
    const y = 1.5 + i * 0.9;
    slide.addShape(pres.shapes.OVAL, { x: 0.6, y: y, w: 0.35, h: 0.35, fill: { color: colors[i % colors.length] } });
    slide.addText(t, {
      x: 1.2, y: y - 0.1, w: W - 1.8, h: 0.6, fontSize: 15, color: theme.textOnDark, fontFace: theme.bodyFont,
      valign: "middle",
    });
  });
}

// ============================================================
// BUILD
// ============================================================
function buildDeck(deckKey) {
  const theme = deckKey === "teacher" ? TEACHER : STUDENT;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Kha Khung Hiep";
  pres.title = deckKey === "teacher" ? "Bai 28 - Dong luong (Slide Giao vien)" : "Bai 28 - Dong luong (Slide Phieu hoc tap)";

  addCover(pres, theme, deckKey);
  for (const item of OUTLINE) {
    if (item.type === "section") addSection(pres, theme, item);
    else if (item.type === "subsection") addSubsection(pres, theme, item);
    else if (item.type === "pair") {
      addTaskSlide(pres, theme, deckKey, item);
      addAnswerSlide(pres, theme, deckKey, item);
    } else if (item.type === "theory") addTheorySlides(pres, theme, deckKey, item);
    else if (item.type === "reading") addReadingSlide(pres, theme, deckKey, item);
    else if (item.type === "mindmap") addMindmapSlide(pres, theme, item);
  }
  return pres;
}

async function main() {
  const teacherPres = buildDeck("teacher");
  const studentPres = buildDeck("student");
  await teacherPres.writeFile({ fileName: path.join(OUT_DIR, "bai28_dong_luong_slide_giao_vien.pptx") });
  await studentPres.writeFile({ fileName: path.join(OUT_DIR, "bai28_dong_luong_slide_phieu_hoc_tap.pptx") });
  console.log("OK - da xuat 2 bo slide");
}

main();
