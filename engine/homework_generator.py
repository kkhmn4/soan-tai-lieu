class HomeworkGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("[INFO] Không tìm thấy GEMINI_API_KEY trong file .env. HomeworkGenerator sẽ chạy ở chế độ Offline.")
            self.client = None
            self.model_name = None
        else:
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = "gemini-2.5-flash"
# Định nghĩa các Schema Pydantic cho Structured Outputs của Bài tập về nhà
class Part1Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trắc nghiệm một lựa chọn, gắn liền với bối cảnh thực tế và lỗi sai cần bẫy.")
    option_a: str = Field(description="Phương án A")
    option_b: str = Field(description="Phương án B")
    option_c: str = Field(description="Phương án C")
    option_d: str = Field(description="Phương án D")
    tikz_code: str | None = Field(default=None, description="Mã vẽ TikZ cho câu hỏi này nếu cần hình minh họa vật lý (cơ học, quang học, điện học). Không chứa document header/footer.")
    correct_option: str = Field(description="Phương án đúng (A, B, C, hoặc D)")
    explanation: str = Field(description="Giải thích lý do lựa chọn phương án và bẫy sai lầm của học sinh.")

class Part2Question(BaseModel):
    question_text: str = Field(description="Đoạn dẫn câu hỏi trắc nghiệm Đúng/Sai, mô tả một hiện tượng hoặc bài toán vật lý.")
    statement_a: str = Field(description="Mệnh đề a")
    statement_b: str = Field(description="Mệnh đề b")
    statem








    unit: str = Field(description="Đơn vị vật lý của đáp án (ví dụ: J, W, m/s...)")
    tikz_code: str | None = Field(default=None, description="Mã vẽ TikZ cho câu hỏi này nếu cần.")
    explanation: str = Field(description="Các bước giải chi tiết và công thức tính toán để ra kết quả số.")

class HomeworkContent(BaseModel):
    lesson_name: str
    part1_questions: list[Part1Question] = Field(description="Danh sách đúng 18 câu hỏi trắc nghiệm nhiều lựa chọn.")
    part2_questions: list[Part2Question] = Field(description="Danh sách đúng 4 câu hỏi Đúng/Sai.")
    part3_questions: list[Part3Question] = Field(description="Danh sách đúng 6 câu hỏi trả lời ngắn.")

class HomeworkGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("[ERROR] Khong tim thay GEMINI_API_KEY trong file .env!")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    def generate_homework(self, matrix_data: dict, pedagogical_data: dict) -> HomeworkContent:
        """Sinh hệ thống câu hỏi bài tập về nhà từ ma trận và phân tích sư phạm."""
        print(f"[PROCESS] Dang sinh he thong cau hoi bai tap ve nha cho: '{matrix_data.get('lesson_name')}'...")
        
        prompt = (
            f"Dựa vào Ma trận bài học: {json.dumps(matrix_data, ensure_ascii=False)}\n"
        prompt = (
            f"Dựa vào Ma trận bài học: {json.dumps(matrix_data, ensure_ascii=False)}\n"
            f"Và phân tích sư phạm (lỗi sai cần bẫy): {json.dumps(pedagogical_data, ensure_ascii=False)}\n"
            f"Hãy sinh hệ thống bài tập về nhà theo đúng cấu trúc Bộ GD&ĐT 2025:\n"
            f"- Phần I: 18 câu trắc nghiệm nhiều lựa chọn.\n"
            f"- Phần II: 4 câu Đúng/Sai.\n"
            f"- Phần III: 6 câu trả lời ngắn.\n"
            f"Lưu ý: 50% câu hỏi phải có bối cảnh thực tế. Chèn mã vẽ TikZ chất lượng cho các câu hỏi cần hình vẽ."
        )
        
        # Gọi Gemini với Structured Output
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=HomeworkContent,
                system_instruction=(
                    "Bạn là một chuyên gia ra đề thi Vật lý THPT Quốc gia theo chương trình mới tại Việt Nam. "
                    "Hãy tạo ra đề bài tập về nhà thuần Việt 100%, chất lượng khoa học cực kỳ cao, gài bẫy logic "
                    "các quan niệm sai lầm đã liệt kê và sinh mã vẽ TikZ chuẩn, tối ưu."
                ),
              






    def export_latex(self, homework: HomeworkContent, template_path: str, output_path: str):
        """Render mã nguồn LaTeX bài tập về nhà từ template Jinja2."""
        print(f"[PROCESS] Dang xuat file LaTeX tai: {output_path}...")
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        template = Template(template_content)
        rendered_tex = template.render(
            lesson_name=homework.lesson_name,
            part1_questions=homework.part1_questions,
            part2_questions=homework.part2_questions,
            part3_questions=homework.part3_questions
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_tex)
        print(f"✅ Da xuat file LaTeX thanh cong: {output_path}")

    def export_answer_key_latex(self, homework: HomeworkContent, output_path: str):
        """Xuất file đáp án chi tiết và lời giải giải thuật tư duy dưới dạng LaTeX."""
        print(f"[PROCESS] Dang xuat file dap an LaTeX tai: {output_path}...")
        
        tex_content = []
        tex_content.append(r"\documentclass[12pt,a4paper]{article}")
        tex_content.append(r"\usepackage[utf8]{vietnam}")
        tex_content.append(r"\usepackage{amsmath,amssymb}")
        tex_content.append(r"\usepackage{geometry}")
        tex_content.append(r"\usepackage{enumitem}")
        tex_content.append(r"\usepackage{tikz}")
        tex_content.append(r"\usetikzlibrary{circuits.ee.IEC, optics, physics, positioning}")
        tex_content.append(r"\geometry{a4paper, margin=20mm}")
        tex_content.append(r"\begin{document}")
        
        tex_content.append(rf"\begin{{center}} {{\bfseries\large ĐÁP ÁN VÀ LỜI GIẢI CHI TIẾT: {homework.lesson_name.upper()}}} \end{{center}} \vspace{{5mm}}")
        
        for q in homework.part1_questions:
            tex_content.append(rf"\item \textbf{{Đáp án: {q.correct_option}}}")
        for q in homework.part1_questions:
            tex_content.append(rf"\item \textbf{{Đáp án: {q.correct_option}}}")
            tex_content.append(rf"\\ \textbf{{Giải thích:}} {q.explanation}")
        tex_content.append(r"\end{enumerate} \vspace{5mm}")

        # 2. Đáp án phần II
        tex_content.append(r"\noindent\textbf{PHẦN II. Đáp án câu hỏi Đúng/Sai}")
        tex_content.append(r"\begin{enumerate}[label=\textbf{Câu \arabic*.}]")
        for q in homework.part2_questions:
            ans_str = []
            for idx, ans in enumerate(q.correct_answers):
                tag = chr(97 + idx) # a, b, c, d
                ans_val = "Đúng" if ans else "Sai"
                ans_str.append(f"{tag}) {ans_val}")
                
            tex_content.append(rf"\item \textbf{{Đáp án:}} {', '.join(ans_str)}")
            tex_content.append(rf"\\ \textbf{{Lời giải chi tiết:}} {q.explanation}")
        tex_content.append(r"\end{enumerate} \vspace{5mm}")

        # 3. Đáp án phần III
        tex_content.append(r"\noindent\textbf{PHẦN III. Đáp án câu hỏi trả lời ngắn}")
        tex_content.append(r"\begin{enumerate}[label=\textbf{Câu \arabic*.}]")
        for q in homework.part3_questions:
            tex_content.append(rf"\item \textbf{{Đáp số:}} {q.correct_value} {q.unit}")
            tex_content.append(rf"\\ \textbf{{Hướng dẫn giải:}} {q.explanation}")
        tex_content.append(r"\end{enumerate}")

        tex_content.append(r"\end{document}")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(tex_content))
        print(f"✅ Da xuat file dap an LaTeX thanh cong: {output_path}")