class LessonMatrix(BaseModel):
    lesson_name: str = Field(description="Tên bài học tổng quát")
    units: list[KnowledgeUnit] = Field(description="Danh sách các đơn vị kiến thức nhỏ cấu thành")

class GEMSArchitect(BaseModel):
    analysis: PedagogicalAnalysis = Field(description="Phân tích sư phạm chi tiết từ YCCĐ")
    matrix: LessonMatrix = Field(description="Ma trận bài học và các nhiệm vụ luân phiên GEMS")

class GEMSAnalyzer:
    def __init__(self, api_key: str = None):
        # Ưu tiên API Key truyền trực tiếp, sau đó đến env
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("[ERROR] Khong tim thay GEMINI_API_KEY. Vui long cau hinh trong file .env!")
        
        # Khởi tạo client Gemini GenAI
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-pro"  # GEMS v7.1: Sử dụng model Pro cho tính toán khoa học chính xác

    def generate_architect(self, yccd: str) -> GEMSArchitect:
        """Gộp Bước 1 & Bước 2: Phân tích sư phạm và sinh Ma trận trong 1 lượt gọi API duy nhất (v7.1)."""
        print(f"[PROCESS] [GEMS v7.1] Dang sinh Spec va Ma tran dong thoi cho YCCD: '{yccd[:50]}...'")
        
        system_instruction = (
            "Bạn là Chuyên gia Giáo dục môn Vật lý và Thiết kế học liệu hàng đầu theo chương trình GDPT 2018 tại Việt Nam.\n"
            "Hãy thực hiện phân tích sư phạm chi tiết và lập ma trận bài học đồng bộ trong định dạng JSON có cấu trúc.\n\n"
            f"--- QUY TẮC PHÂN TÍCH SƯ PHẠM ---\n{SYSTEM_PEDAGOGICAL_PROMPT}\n\n"
            f"--- QUY TẮC THIẾT LẬP MA TRẬN ---\n{SYSTEM_MATRIX_PROMPT}"
        )
        
        prompt = f"Hãy thực hiện phân tích sư phạm và xây dựng ma trận cho YCCĐ sau:\n{yccd}"
 
<truncated 1137 bytes>
    tasks: list[TaskItem] = Field(description="Danh sách các nhiệm vụ liên kết mạch lạc và luân phiên loại nhiệm vụ")

class LessonMatrix(BaseModel):

class GEMSArchitect(BaseModel):
    analysis: PedagogicalAnalysis = Field(description="Phân tích sư phạm chi tiết từ YCCĐ")
class GEMSArchitect(BaseModel):
    analysis: PedagogicalAnalysis = Field(description="Phân tích sư phạm chi tiết từ YCCĐ")
    matrix: LessonMatrix = Field(description="Ma trận bài học và các nhiệm vụ luân phiên GEMS")

class GEMSAnalyzer:
    def __init__(self, api_key: str = None):
        # Ưu tiên API Key truyền trực tiếp, sau đó đến env
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("[GEMS] Không tìm thấy GEMINI_API_KEY trong file .env! Vui lòng cấu hình API key trước khi chạy.")
        # Khởi tạo client Gemini GenAI
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-pro"  # GEMS v7.1: Sử dụng model Pro cho tính toán khoa học chính xác

    def generate_architect(self, yccd: str) -> GEMSArchitect:
        """Gộp Bước 1 & Bước 2: Phân tích sư phạm và sinh Ma trận trong 1 lượt gọi API duy nhất (v7.1)."""
        print(f"[PROCESS] [GEMS v7.1] Dang sinh Spec va Ma tran dong thoi cho YCCD: '{yccd[:50]}...'")
        
        system_instruction = (
            "Bạn là Chuyên gia Giáo dục môn Vật lý và Thiết kế học liệu hàng đầu theo chương trình GDPT 2018 tại Việt Nam.\n"
            "Hãy thực hiện phân tích sư phạm chi tiết và lập ma trận bài học đồng bộ trong định dạng JSON có cấu trúc.\n\n"
            f"--- QUY TẮC PHÂN TÍCH SƯ PHẠM ---\n{SYSTEM_PEDAGOGICAL_PROMPT}\n\n"
            f"--- QUY TẮC THIẾT LẬP MA TRẬN ---\n{SYSTEM_MATRIX_PROMPT}"
        )
        
        prompt = f"Hãy thực hiện phân tích sư phạm và xây dựng ma trận cho YCCĐ sau:\n{yccd}"
        
        response = self.client.models.generate_content(
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GEMSArchitect,
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        
        data = json.loads(response.text)
        return GEMSArchitect(**data)

    def pedagogical_analysis(self, yccd: str) -> PedagogicalAnalysis:
        """Thực hiện Bước 1: Phân tích sư phạm từ YCCĐ."""
        # Gọi qua generate_architect để tương thích
        arch = self.generate_architect(yccd)
        return arch.analysis

    def generate_matrix(self, yccd: str, analysis: PedagogicalAnalysis) -> LessonMatrix:
        """Thực hiện Bước 2: Thiết lập ma trận bài học và nhiệm vụ từ phân tích sư phạm."""
        # Gọi qua generate_architect để tương thích
        arch = self.generate_architect(yccd)
        return arch.matrix

    def save_to_docs(self, analysis: PedagogicalAnalysis, matrix: LessonMatrix, output_dir: str = "docs"):
        """Lưu trữ kết quả phân tích sư phạm và ma trận bài học ra file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 1. Lưu ma trận JSON
        matrix_path = os.path.join(output_dir, "lesson_matrix.json")
        with open(matrix_path, "w", encoding="utf-8") as f:
            json.dump(matrix.model_dump(), f, ensure_ascii=False, indent=2)
        print(f"  + Da luu file ma tran: {matrix_path}")
        
        # 2. Lưu tài liệu phân tích sư phạm dạng Markdown
        analysis_path = os.path.join(output_dir, "pedagogical_analysis.md")
        with open(analysis_path, "w", encoding="utf-8") as f:
        analysis_path = os.path.join(output_dir, "pedagogical_analysis.md")
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write(f"# PHÂN TÍCH SƯ PHẠM VÀ MA TRẬN BÀI HỌC: {matrix.lesson_name}\n\n")
            f.write("## 1. Kiến thức cốt lõi\n")
            for concept in analysis.key_concepts:
                f.write(f"- {concept}\n")
            f.write("\n")
            
            f.write("## 2. Các lỗi sai thường gặp (Misconceptions)\n")
            for idx, item in enumerate(analysis.misconceptions, 1):
                f.write(f"### Lỗi {idx}: {item.misconception}\n")
                f.write(f"- **Bản chất vật lý đúng:** {item.correct_concept}\n")
                f.write(f"- **Giải thích sư phạm:** {item.explanation}\n\n")
                
            f.write("## 3. Phương pháp dạy học đề xuất\n")
            for method in analysis.teaching_methods:
                f.write(f"- {method}\n")
            f.write("\n")
            
            f.write("## 4. Ma trận phân chia nhiệm vụ học tập\n")
            for unit in matrix.units:
                f.write(f"### [{unit.unit_id}] {unit.unit_name}\n")
                f.write(f"- **Khái niệm chính:** {', '.join(unit.concepts)}\n")
                f.write("- **Chuỗi nhiệm vụ:**\n")
                for task in unit.tasks:
                    f.write(f"  - **{task.task_id} ({task.task_type}) - {task.task_name}**\n")
                    f.write(f"    - *Mô tả:* {task.description}\n")
                    f.write(f"    - *Bối cảnh:* {task.context_real}\n")
                f.write("\n")
                
        print(f"  + Da luu file Markdown: {analysis_path}")

                f.write(f"- **Khái niệm chính:** {', '.join(unit.concepts)}\n")
                f.write("- **Chuỗi nhiệm vụ:**\n")
                for task in unit.tasks:
                    f.write(f"  - **{task.task_id} ({task.task_type}) - {task.task_name}**\n")
                    f.write(f"    - *Mô tả:* {task.description}\n")
                    f.write(f"    - *Bối cảnh:* {task.context_real}\n")
                f.write("\n")
                