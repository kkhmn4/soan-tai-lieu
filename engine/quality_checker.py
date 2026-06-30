class QualityChecker:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("[INFO] Không tìm thấy GEMINI_API_KEY trong file .env. QualityChecker sẽ chạy ở chế độ Offline (Local Static Check).")
            self.client = None
            self.model_name = None
        else:
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = "gemini-2.5-flash"
class CriterionCheck(BaseModel):
    name: str = Field(description="Tên tiêu chí kiểm định")
    passed: bool = Field(description="Đạt (True) hoặc Không đạt (False)")
    comment: str = Field(description="Nhận xét chi tiết hoặc hướng dẫn sửa đổi nếu không đạt")

class LLMTextCheckReport(BaseModel):
    lesson_name: str
    criteria: list[CriterionCheck] = Field(description="Danh sách kết quả kiểm định cho 6 tiêu chí")
    overall_passed: bool = Field(description="Đánh giá chung: Đạt toàn bộ (True) hay cần chỉnh sửa (False)")
    summary: str = Field(description="Tóm tắt kết quả kiểm định")

# --- CÁC SCHEMA PYDANTIC CHO GIẢI BÀI TOÁN LÝ ĐỘC LẬP ---
class SolvedPart1Question(BaseModel):
    index: int = Field(description="Số thứ tự câu hỏi (1-indexed)")
    solved_option: str = Field(description="Đáp án giải độc lập (A, B, C, hoặc D)")
    explanation: str = Field(description="Lời giải chi tiết từng bước")

class SolvedPart2Question(BaseModel):
    index: int = Field(description="Số thứ tự câu hỏi (1-indexed)")
    solved_answers: list[bool] = Field(descriptio
    explanation: str = Field(description="Lời giải chi tiết từng bước cho từng ý a, b, c, d")

class SolvedPart3Question(BaseModel):
    index: int = Field(description="Số thứ tự câu hỏi (1-indexed)")
    solved_value: float = Field(description="Kết quả số giải độc lập (sau khi làm tròn)")
    explanation: str = Field(description="Lời giải chi tiết từng bước và công thức tính toán")

class SolvedHomework(BaseModel):
    part1_solved: list[SolvedPart1Question] = Field(description="Danh sách đáp án giải độc lập phần I")
    part2_solved: list[SolvedPart2Question] = Field(description="Danh sách đáp án giải độc lập phần II")
    part3_solved: list[SolvedPart3Question] = Field(description="Danh sách đáp án giải độc lập phần III")

# --- SCHEMA PYDANTIC CHO KIỂM DUYỆT HÌNH ẢNH (AI VISION) ---
class ImageVerificationResult(BaseModel):
    filename: str = Field(description="Tên tệp ảnh (ví dụ: photo_dvkt1_nv1.png)")
    passed: bool = Field(description="Đạt độ chính xác khoa học/vật lý (True) hay không (False)")
    comment: str = Field(description="Nhận xét chi tiết về ảnh, chỉ ra các điểm phi vật lý hoặc sai lệch nếu có")

# --- SCHEMA PYDANTIC CHO KIỂM DUYỆT SLIDE (GEMS SLIDES) ---
class SlideVerificationResult(BaseModel):
    passed: bool = Field(description="Đạt chuẩn thiết kế slide GEMS v7.1 hay không")
    slide_count: int = Field(description="Số lượng slide đếm được")
    detected_teacher: str = Field(description="Tên giáo viên phát hiện trên slide mở đầu")
    detected_fonts: list[str] = Field(description="Danh sách các phông chữ phát hiện được")
    comment: str = Field(description="Nhận xét chi tiết về cấu trúc slide, tính thuần Việt, và tính chính xác vật lý")

# --- SCHEMA BÁO CÁO CUỐI CÙNG ---
class QualityReport(BaseModel):
    lesson_name: str
    criteria: list[CriterionCheck]
    overall_passed: bool
    summary: str
    math_physics_errors: dict | None = None
    image_verification_results: list[ImageVerificationResult] | None = None
    slide_verification_result: SlideVerificationResult | None = None


class QualityChecker:
    def __init__(self, api_key: str = None):
        # Ưu tiên API Key truyền trực tiếp, sau đó đến env, nếu không có sẽ tự động dùng credentials mặc định của Antigravity
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    def check_quality(self, worksheet_md_content: str, homework_tex_content: str, 
                      homework_data: dict = None, worksheet_data: dict = None, 
                      images_dir: str = None, pptx_path: str = None) -> QualityReport:
        """Sử dụng Gemini API để tự động kiểm định chất lượng sản phẩm đầu ra theo 6 tiêu chí GEMS + Toán lý chéo + Vision + Slides."""
        print("[PROCESS] Dang chay tu dong kiem dinh chat luong (AI Self-Check)...")
        
        prompt = (
            f"Hãy kiểm tra chất lượng của hai tài liệu học tập sau đây:\n\n"
            f"--- PHIẾU HỌC TẬP HỌC SINH (Markdown) ---\n{worksheet_md_content}\n\n"
            f"--- BÀI TẬP VỀ NHÀ (LaTeX) ---\n{homework_tex_content}\n\n"
            f"Đối chiếu nghiêm ngặt với 6 tiêu chí chất lượng sau:\n"
            f"1. Tối ưu không gian in ấn: Chừa đủ khoảng trống (chấm chấm) để viết bài (khoảng 35-40% diện tích).\n"
            f"2. Tính chân thực hình ảnh (Scientific Realism): Các hình vẽ hoặc sơ đồ mô tả có hợp lý khoa học và thực tế không.\n"
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LLMTextCheckReport,
                system_instruction=(
                    "Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý. "
                    "Hãy kiểm tra cực kỳ khắt khe, chỉ ra mọi điểm chưa đạt để cải thiện chất lượng phiếu."
                ),
                response_schema=LLMTextCheckReport,
                system_instruction=(
                    "Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý. "
                    "Hãy kiểm tra cực kỳ khắt khe, chỉ ra mọi điểm chưa đạt để cải thiện chất lượng phiếu."
                ),
                temperature=0.1,
            )
        )
        
        text_report_data = json.loads(response.text)
        
        # 1. Chạy Math & Physics Checker giải bài độc lập
        math_physics_errors = {"part1_errors": [], "part2_errors": [], "part3_errors": []}
        if homework_data:
            math_physics_errors = self.verify_math_physics(homework_data)
            
        # 2. Chạy AI Vision Validator kiểm duyệt hình ảnh
        image_results = []
        if images_dir and (homework_data or worksheet_data):
            image_results = self.verify_images(images_dir, homework_data or {}, worksheet_data or {})
            
        # 3. Chạy Slide Validator
        slide_result = None
        if pptx_path:
            slide_result = self.verify_slides(pptx_path)
            
        # Đánh giá xem có lỗi sai số liệu hay ảnh phi vật lý không
        has_math_errors = (
            len(math_physics_errors.get("part1_errors", [])) > 0 or
            len(math_physics_errors.get("part2_
        # Trả về đối tượng QualityReport đầy đủ
        return QualityReport(
            lesson_name=text_report_data.get("lesson_name"),
            criteria=[CriterionCheck(**c) for c in text_report_data.get("criteria", [])],
            overall_passed=overall_passed,
            summary=summary,
            math_physics_errors=math_physics_errors,
            image_verification_results=image_results
        )

    def verify_math_physics(self, homework_data: dict) -> dict:
        """Gọi Gemini giải độc lập toàn bộ bài tập và đối chiếu đáp án."""
        print("[PROCESS] Dang chay kiem dinh cheo toan ly doc lap (Math & Physics Checker)...")
        if not homework_data:
            return {"part1_errors": [], "part2_errors": [], "part3_errors": []}
            
        prompt = (
            "Dưới đây là một đề bài tập về nhà môn Vật lý (gồm 3 phần: Trắc nghiệm nhiều lựa chọn, Đúng/Sai, Trả lời ngắn).\n"
            "Hãy đóng vai trò là một Giáo sư Vật lý và giải độc lập toàn bộ các câu hỏi này. "
            "Hãy tính toán thật chính xác và cẩn thận từng câu hỏi để đảm bảo tính đúng đắn khoa học.\n\n"































            f"--- PHIẾU HỌC TẬP HỌC SINH (Markdown) ---\n{worksheet_md_content}\n\n"
            f"--- BÀI TẬP VỀ NHÀ (LaTeX) ---\n{homework_tex_content}\n\n"
            f"Đối chiếu nghiêm ngặt với 6 tiêu chí chất lượng sau:\n"
            f"1. Tối ưu không gian in ấn: Chừa đủ khoảng trống (chấm chấm) để viết bài (khoảng 35-40% diện tích).\n"
            f"2. Tính chân thực hình ảnh (Scientific Realism): Các hình vẽ hoặc sơ đồ mô tả có hợp lý khoa học và thực tế không.\n"
            f"3. Tính tuyến tính nội dung: Phiếu học tập đi theo tiến trình 4 phần chặt chẽ (Khám phá -> Trọng tâm -> Vận dụng -> Mở rộng).\n"
            f"4. Tính chuẩn mực ngôn ngữ: Sử dụng 100% tiếng Việt sư phạm nghiêm túc, không chứa từ lóng hay tiếng Anh.\n"
            f"5. Tính thực dụng của khoảng trống: Số lượng dòng chừa trống thích hợp (3-5 dòng cho phần trả lời).\n"
            f"6. Tính chẩn đoán lỗi & Chi tiết bối cảnh: Bài tập về nhà có gài bẫy kiểm tra lỗi sai thường gặp của học sinh và có 50% bối cảnh thực tế không."
        )
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LLMTextCheckReport,
                system_instruction=(
                    "Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý. "
                    "Hãy kiểm tra cực kỳ khắt khe, chỉ ra mọi điểm chưa đạt để cải thiện chất lượng phiếu."
                ),
                temperature=0.1,
            )
        )
        
        text_report_data = json.loads(response.text)
        
        # 1. Chạy Math & Physics Checker giải bài độc lập
        math_physics_errors = {"part1_errors": [], "part2_errors": [], "part3_errors": []}
        if homework_data:
            math_physics_errors = self.verify_math_physics(homework_data)
            
        # 2. Chạy AI Vision Validator kiểm duyệt hình ảnh
        image_results = []
        if images_dir and (homework_data or worksheet_data):
            image_results = self.verify_images(images_dir, homework_data or {}, worksheet_data or {})
            
        # 3. Chạy Slide Validator
        slide_result = None
        if pptx_path:
            slide_result = self.verify_slides(pptx_path)
            
        # Đánh giá xem có lỗi sai số liệu hay ảnh phi vật lý không
        has_math_errors = (
            len(math_physics_errors.get("part1_errors", [])) > 0 or
            len(math_physics_errors.get("part2_errors", [])) > 0 or
            len(math_physics_errors.get("part3_errors", [])) > 0
        )
        has_image_errors = any(not img.passed for img in image_results)
        has_slide_error
            sol_p3 = solved_data.part3_solved
            for idx, (orig, solved) in enumerate(zip(orig_p3, sol_p3), 1):
                try:
                    orig_val = float(orig.get("correct_value", 0))
                    sol_val = float(solved.solved_value)
                except ValueError:
                    orig_val = 0.0
                    sol_val = 0.0
                    
                # Chấp nhận sai lệch cực nhỏ do làm tròn
                if abs(orig_val - sol_val) > 0.05:
                    part3_errors.append({
                        "index": idx,
                        "question": orig.get("question_text"),
                        "original_ans": f"{orig_val} {orig.get('unit', '')}",
                        "solved_ans": f"{sol_val} {orig.get('unit', '')}",
                        "original_explanation": orig.get("explanation"),
                        "solved_explanation": solved.explanation
        # Trả về đối tượng QualityReport đầy đủ
        return QualityReport(
            lesson_name=text_report_data.get("lesson_name"),
            criteria=[CriterionCheck(**c) for c in text_report_data.get("criteria", [])],
            overall_passed=overall_passed,
            summary=summary,
            math_physics_errors=math_physics_errors,
            image_verification_results=image_results,
            slide_verification_result=slide_result
        )

    def verify_math_physics(self, homework_data: dict) -> dict:
        """Gọi Gemini giải độc lập toàn bộ bài tập và đối chiếu đáp án."""
        print("[PROCESS] Dang chay kiem dinh cheo toan ly doc lap (Math & Physics Checker)...")
        if not homework_data:
            return {"part1_errors": [], "part2_errors": [], "part3_errors": []}
            
        prompt = (
            "Dưới đây là một đề bài tập về nhà môn Vật lý (gồm 3 phần: Trắc nghiệm nhiều lựa chọn, Đúng/Sai, Trả lời ngắn).\n"
            "Hãy đóng vai trò là một Giáo sư Vật lý và giải độc lập toàn bộ các câu hỏi này. "
            "Hãy tính toán thật chính xác và cẩn thận từng câu hỏi để đảm bảo tính đúng đắn khoa học.\n\n"
            f"--- ĐỀ BÀI TẬP VỀ NHÀ ---\n{json.dumps(homework_data, ensure_ascii=False)}\n"
        )
        
                continue
                
            image_path = os.path.join(images_dir, filename)
            context_text = ""
            
            # Phân loại và lấy bối cảnh yêu cầu hình vẽ
            if filename.startswith("photo_"):
                parts = filename.replace("photo_", "").replace(".png", "").split("_")
                if len(pa
                    except Exception:
                        pass
                        
            if not context_text:
                continue
                
            print(f"  -> Dang kiem duyet hinh anh: {filename}...")
            try:
                img = Image.open(image_path)
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[
                        img,
                        f"Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý.\n"
                        f"Hãy đối chiếu hình vẽ đính kèm với nội dung bài học/bài tập dưới đây:\n\n"
                        f"--- YÊU CẦU ĐỀ BÀI ---\n{context_text}\n\n"
                        "Hãy đánh giá xem hình vẽ này có đạt độ chính xác khoa học và bản chất vật lý không. "
                        "Chú ý: Trục tọa độ, chiều dòng điện, các vạch chia số, góc truyền ánh sáng, hướng lực tác dụng..."
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ImageVerificationResult,
                        system_instruction=(
                            "Bạn là một chuyên gia thẩm định hình ảnh khoa học môn Vật lý. "
                            "Hãy phân tích hình vẽ đính kèm cực kỳ khắt khe so với yêu cầu đề bài. "
                            "Nếu phát hiện lỗi sai vật lý, hãy đánh dấu passed = False và mô tả chi tiết lỗi."
                        ),
                        temperature=0.1,
                    )
                )
                
                res_data = json.loads(response.text)
                # Đảm bảo trường filename được gán đúng
                res_data["filename"] = filename
                results.append(ImageVerificationResult(**res_data))
            except Exception as e:
                sol_ans = solved.solved_answers
                if orig_ans != sol_ans:
                    part2_errors.append({
                        "index": idx,
                        "question": orig.get("question_text"),
                        "original_ans": orig_ans,
                        "solved_ans": sol_ans,
                        "original_explanation": orig.get("explanation"),
                        "solved_explanation": solved.explanation
                    })
                    
            # 3. Phần III: Trả lời ngắn (6 câu)
            orig_p3 = homework_data.get("part3_questions", [])
            sol_p3 = solved_data.part3_solved
            for idx, (orig, solved) in enumerate(zip(orig_p3, sol_p3), 1):
                try:
                    orig_val = float(orig.get("correct_value", 0))
                    sol_val = float(solved.solved_value)
                except ValueError:
                    orig_val = 0.0
                    sol_val = 0.0
                    
                # Chấp nhận sai lệch cực nhỏ do làm tròn
                if abs(orig_val - sol_val) > 0.05:
                    part3_errors.append({
                        "index": idx,
                        "question": orig.get("question_text"),
                        "original_ans": f"{orig_val} {orig.get('unit', '')}",
                        "solved_ans": f"{sol_val} {orig.get('unit', '')}",
                        "original_explanation": orig.get("explanation"),
                        "solved_explanation": solved.explanation
                    })
                    
            return {
                "part1_errors": part1_errors,
                "part2_errors": part2_errors,
                "part3_errors": part3_errors
            }
        except Exception as e:
            print(f"[ERROR] Loi khi giai cheo toan ly: {e}")
                
        return results

    def save_report(self, report: QualityReport, output_path: str = "docs/quality_report.md"):
        """Lưu báo cáo kiểm định chất lượng nâng cấp thành file Markdown."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG NÂNG CAO: {report.lesson_name.upper()}\n\n")
            f.write(f"**Kết luận chung:** {'✅ ĐẠT TIÊU CHUẨN GEMS' if report.overall_passed else '⚠️ CẦN CHỈNH SỬA'}\n\n")
            f.write(f"**Tóm tắt kết quả:** {report.summary}\n\n")
            
            f.write("## I. CHI TIẾT 6 TIÊU CHÍ GEMS VỐN CÓ\n")
            for idx, criterion in enumerate(report.criteria, 1):
                status = "✅ Đạt" if criterion.passed else "❌ Chưa đạt"
                f.write(f"### {idx}. {criterion.name}: {status}\n")
                f.write(f"- *Nhận xét:* {criterion.comment}\n\n")
                
            f.write("---\n\n")
            f.write("## II. KIỂM ĐỊNH CHÉO TOÁN LÝ ĐA TẦNG (Math & Physics Solver)\n")
            math_errors = report.math_physics_errors
            has_math_errors = (
                len(math_errors.get("part1_errors", [])) > 0 or
                len(math_errors.get("part2_errors", [])) > 0 or
                len(math_errors.get("part3_errors", [])) > 0
            )
            
            if not has_math_errors:
                f.write("✅ **ĐẠT TIÊU CHUẨN:** Giải chéo thành công. Không phát hiện sai sót số liệu khoa học ở toàn bộ 28 câu bài tập về nhà.\n\n")
            else:
                f.write("❌ **CÓ LỖI SAI SỐ LIỆU:** Phát hiện sự sai lệch đáp án giữa bản sinh ra và bản giải độc lập của AI:\n\n")
                
                # 1. Lỗi phần I
                if math_errors.get("part1_errors"):
                    f.write("### 📍 Phần I (Trắc nghiệm nhiều lựa chọn):\n")
                    for err in math_errors.get("part1_errors"):
                        f.write(f"- **Câu {err['index']}:** {err['question']}\n")
                        f.write(f"  - Đáp án đề bài: `{err['original_ans']}`\n")
                        f.write(f"  - Đáp án giải độc lập: `{err['solved_ans']}`\n")
                        f.write(f"  - Lời giải độc lập: *{err['solved_explanation']}*\n\n")
                        
                # 2. Lỗi phần II
                if math_errors.get("part2_errors"):
                    f.write("### 📍 Phần II (Đúng/Sai):\n")
                    for err in math_errors.get("part2_errors"):
                        f.write(f"- **Câu {err['index']}:** {err['question']}\n")
                        f.write(f"  - Đáp án đề bài: `{err['original_ans']}`\n")
                        f.write(f"  - Đáp án giải độc lập: `{err['solved_ans']}`\n")
                        f.write(f"  - Lời giải độc lập: *{err['solved_explanation']}*\n\n")
                        
                # 3. Lỗi phần III
                if math_errors.get("part3_errors"):
                    f.write("### 📍 Phần III (Trả lời ngắn):\n")
                    for err in math_errors.get("part3_errors"):
                        f.write(f"- **Câu {err['index']}:** {err['question']}\n")
                        f.write(f"  - Đáp số đề bài: `{err['original_ans']}`\n")
                        f.write(f"  - Đáp số giải độc lập: `{err['solved_ans']}`\n")
                        f.write(f"  - Lời giải độc lập: *{err['solved_explanation']}*\n\n")
            
            f.write("---\n\n")
            f.write("## III. KIỂM DUYỆT HÌNH ẢNH & INFOGRAPHIC TỰ ĐỘNG (AI Vision Validator)\n")
            img_results = report.image_verification_results
            if not img_results:
                f.write("❔ Kh



                    f.write(f"### 🖼️ Tệp ảnh: `{img.filename}` - {status}\n")
                    f.write(f"- *Nhận xét kiểm định:* {img.comment}\n\n")
            
            f.write("---\n\n")
            f.write("## IV. KIỂM ĐỊNH THIẾT KẾ SLIDE PPTX (GEMS Slide Validator)\n")
            slide_res = report.slide_verification_result
            if not slide_res:
                f.write("❔ Không tìm thấy file slide PPTX để kiểm duyệt.\n\n")
            else:
                status = "✅ Đạt chuẩn thiết kế Slide" if slide_res.passed else "❌ CẢNH BÁO LỖI"
                f.write(f"### 📊 Slide Deck - {status}\n")
                f.write(f"- **Số lượng slide:** {slide_res.slide_count}\n")
                f.write(f"- **Giáo viên phát hiện:** `{slide_res.detected_teacher}`\n")
                f.write(f"- **Phông chữ phát hiện:** `{', '.join(slide_res.detected_fonts)}`\n")
                f.write(f"- *Nhận xét kiểm định:* {slide_res.comment}\n\n")
                    
        print(f"[SUCCESS] Bao cao kiem dinh nang cao da duoc luu tai: {output_path.encode('ascii', errors='replace').decode('ascii')}")

    def verify_slides(self, pptx_path: str) -> SlideVerificationResult:
        """Đọc và kiểm định chi tiết file slide PPTX (Kha Khung Hiệp, font UVN bai sau, 7 slide/ĐVKT, thuần Việt, chuẩn lý)."""
        print(f"[PROCESS] Dang kiem dinh file slide PPTX: {pptx_path}...")
        if not os.path.exists(pptx_path):
            return SlideVerificationResult(
                passed=False,
                slide_count=0,
                detected_teacher="Không tìm thấy file",
                comment=f"Lỗi: Không tìm thấy file slide deck tại {pptx_path}"
            )
            
        import zipfile
        import re
        import xml.etree.ElementTree as ET
        
        slides_text = []
        fonts = set()
        
        try:
            with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
                slide_files = sorted(
                    [name for name in zip_ref.namelist() if name.startswith('ppt/slides/slide') and name.endswith('.xml')],
                    key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1))
                )
                
                for slide_file in slide_files:
                    slide_xml = zip_ref.read(slide_file)
                    root = ET.fromstring(slide_xml)
                    
                    text_runs = []
                    for elem


























                if math_errors.get("part1_errors"):
                    f.write("### 📍 Phần I (Trắc nghiệm nhiều lựa chọn):\n")
                    for err in math_errors.get("part1_errors"):
                        f.write(f"- **Câu {err['index']}:** {err['question']}\n")
            f"4. Ngôn ngữ: Phải thuần Việt 100% ở các slide nội dung bài giảng chính, không chứa chữ tiếng Anh.\n"
            f"5. Tính chính xác khoa học: Nội dung vật lý, công thức, số liệu phải chuẩn xác tuyệt đối."
        )
        
        if not self.client:
            raise EnvironmentError("[GEMS] Không tìm thấy GEMINI_API_KEY. Không thể kiểm định slide.")

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SlideVerificationResult,
                    system_instruction=(
                        "Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý. "
                        "Hãy kiểm tra file slide cực kỳ khắt khe, chỉ ra mọi lỗi sai thiết kế, cấu trúc hoặc vật lý."
                    ),
                    temperature=0.1,
                )
            )
            res_result = json.loads(response.text)
            res_result["slide_count"] = slide_count
            res_result["detected_fonts"] = detected_fonts_list
            return SlideVerificationResult(**res_result)
        except Exception as e:
            return SlideVerificationResult(
                passed=False,
                slide_count=slide_count,
                detected_teacher="Lỗi phân tích AI",
                detected_fonts=detected_fonts_list,
                comment=f"Lỗi khi gọi Gemini kiểm định slide: {str(e)}"
            )

























            )
            
        import zipfile
        import re
        import xml.etree.ElementTree as ET
        
        slides_text = []
        fonts = set()
        
        try:
            with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
                slide_files = sorted(
                    [name for name in zip_ref.namelist() if name.startswith('ppt/slides/slide') and name.endswith('.xml')],
                    key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1))
                )
                
                for slide_file in slide_files:
                    slide_xml = zip_ref.read(slide_file)
                    root = ET.fromstring(slide_xml)
                    
                    text_runs = []
                    for elem in root.iter():
                        # Lấy text
                        if elem.tag.endswith('}t') and elem.text:
                            text_runs.append(elem.text)
                        # Lấy font
                        if elem.tag.endswith('}rPr') or elem.tag.endswith('}defRPr'):
                            typeface = elem.attrib.get('typeface')
                            if typeface:
                                fonts.add(typeface)
                                
                    slides_text.append(" ".join(text_runs))
        except Exception as e:
            return SlideVerificationResult(
                passed=False,
                slide_count=0,
                detected_teacher="Lỗi đọc file",
                detected_fonts=[],
                comment=f"Lỗi khi đọc phân tích XML cấu trúc PPTX: {str(e)}"
            )
            
        slide_count = len(slides_text)
        all_text_content = "\n".join([f"Slide {i+1}: {text}" for i, text in enumerate(slides_text)])
        detected_fonts_list = list(fonts)
        
        prompt = (
            f"Hãy kiểm duyệt nội dung của bài giảng slide dạng PPTX sau:\n\n"
            f"--- NỘI DUNG CÁC SLIDE ĐÃ TRÍCH XUẤT ---\n{all_text_content}\n\n"
            f"Danh sách font chữ phát hiện trong file: {', '.join(detected_fonts_list)}\n\n"
            f"Đối chiếu nghiêm ngặt với các tiêu chuẩn slide GEMS v7.1:\n"
            f"1. Tên giáo viên giảng dạy mặc định phải là 'Kha Khung Hiệp' ở slide 1.\n"
            f"2. Font chữ chủ đạo được yêu cầu thiết kế là 'UVN bai sau'.\n"
            f"3. Cấu trúc bài giảng: Slide mở đầu + 7 slide cho mỗi Đơn vị Kiến thức (ĐVKT) (định dạng: Đề mục -> Khám phá -> Đáp án -> Trọng tâm -> Vận dụng -> Lời giải -> Mở rộng).\n"
            f"4. Ngôn ngữ: Phải thuần Việt 100% ở các slide nội dung bài giảng chính, không chứa chữ tiếng Anh.\n"
            f"5. Tính chính xác khoa học: Nội dung vật lý, công thức, số liệu phải chuẩn xác tuyệt đối."
        )
        
        if not self.client:
            print("[INFO] Chạy kiểm định slide offline...")
            # Kiểm 
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SlideVerificationResult,
                    system_instruction=(
                        "Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý. "
                        "Hãy kiểm tra file slide cực kỳ khắt khe, chỉ ra mọi lỗi sai thiết kế, cấu trúc hoặc vật lý."
                    ),
                    temperature=0.1,
                )
            )
            res_result = json.loads(response.text)
                
            return SlideVerificationResult(
                passed=passed,
                slide_count=slide_count,
                detected_teacher="Kha Khung Hiệp" if has_teacher else "Không xác định",
                detected_fonts=detected_fonts_list,
                comment=comment + " (Kiểm duyệt Slide tĩnh cục bộ thành công)"
            )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SlideVerificationResult,
                    system_instruction=(
                        "Bạn là Trưởng ban Kiểm định Chất lượng Học liệu môn Vật lý. "
                        "Hãy kiểm tra file slide cực kỳ khắt khe, chỉ ra mọi lỗi sai thiết kế, cấu trúc hoặc vật lý."
                    ),
                    temperature=0.1,
                )
            )
            res_result = json.loads(response.text)
            res_result["slide_count"] = slide_count
            res_result["detected_fonts"] = detected_fonts_list
            return SlideVerificationResult(**res_result)
        except Exception as e:
            return SlideVerificationResult(
                passed=False,
                slide_count=slide_count,
                detected_teacher="Lỗi phân tích AI",
                detected_fonts=detected_fonts_list,
                comment=f"Lỗi khi gọi Gemini kiểm định slide: {str(e)}"
            )