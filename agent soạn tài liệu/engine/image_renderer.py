import os
import sys
import subprocess
import shutil
from google import genai
from PIL import Image
import io

# Ensure stdout encoding is UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class ImageRenderer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("[INFO] Không tìm thấy GEMINI_API_KEY trong file .env. ImageRenderer sẽ chạy ở chế độ Offline.")
            self.client = None
            self.imagen_model = None
        else:
            self.client = genai.Client(api_key=self.api_key)
            self.imagen_model = "imagen-3.0-generate-002"

    def generate_scientific_illustration(self, prompt: str, output_path: str) -> bool:
        """
        Tạo ảnh minh họa khoa học thực tế bằng mô hình Imagen 3.0 Pro.
        Tự động tăng cường prompt để đạt tính chính xác khoa học cao nhất.
        """
        if not self.client:
            print(f"[OFFLINE] Bỏ qua sinh ảnh thực tế cho: {prompt}")
            return False

        # Tăng cường prompt để đảm bảo tính chân thực khoa học, loại bỏ yếu tố ảo hóa
        enhanced_prompt = (
            f"A realistic, scientifically accurate photo of {prompt}. "
            "Clean professional laboratory setting, realistic physics, clear details, "
            "high resolution, professional photography, studio lighting. "
            "No cartoon elements, no fantasy or sci-fi elements, no text, "
            "no AI hallucinations, no unrealistic colors."
        )
        
        print(f"[IMAGEN] Đang yêu cầu sinh ảnh: '{prompt}'...")
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            result = self.client.models.generate_images(
                model=self.imagen_model,
                prompt=enhanced_prompt,
                config=dict(
                    number_of_images=1,
                    output_mime_type='image/png',
                    aspect_ratio='4:3'
                )
            )
            
            if result and result.generated_images:
                img_bytes = result.generated_images[0].image.image_bytes
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  [SUCCESS] Đã lưu ảnh minh họa thực tế vào: {output_path}")
                return True
            else:
                print("  [ERROR] Không có ảnh nào được trả về từ API.")
                return False
        except Exception as e:
            print(f"  [ERROR] Lỗi sinh ảnh minh họa thực tế: {e}")
            return False

    def render_tikz_diagram(self, tikz_code: str, output_path: str) -> bool:
        """
        Biên dịch sơ đồ TikZ thành ảnh PNG thông qua xelatex và pdftoppm.
        Nếu không có trình dịch cục bộ, sẽ tự động lưu file .tex thô để người dùng biên dịch sau.
        """
        base_name = os.path.splitext(output_path)[0]
        tex_path = base_name + ".tex"
        pdf_path = base_name + ".pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Tạo file LaTeX hoàn chỉnh sử dụng lớp standalone
        latex_template = f"""\\documentclass[tikz,border=2pt]{{standalone}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{pgfplots}}
\\usetikzlibrary{{shapes,arrows,positioning,calc,patterns,decorations.pathmorphing,decorations.markings}}
\\pgfplotsset{{compat=1.18}}
\\begin{{document}}
{tikz_code}
\\end{{document}}
"""
        
        # Ghi file .tex thô
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_template)
        print(f"  [TIKZ] Đã lưu mã nguồn TikZ (.tex) vào: {tex_path}")
        
        # Kiểm tra trình biên dịch xelatex
        xelatex_found = shutil.which("xelatex")
        pdftoppm_found = shutil.which("pdftoppm")
        
        if not xelatex_found:
            print(f"  [WARNING] Không tìm thấy xelatex. Giữ lại file .tex thô. Quy trình vẽ hình hoàn tất ở chế độ Offline.")
            return False
            
        print("  [TIKZ] Đang biên dịch TikZ cục bộ bằng xelatex...")
        try:
            # Biên dịch sang PDF
            temp_dir = os.path.dirname(output_path) or "."
            cmd_pdf = ["xelatex", "-interaction=nonstopmode", f"-output-directory={temp_dir}", tex_path]
            r_pdf = subprocess.run(cmd_pdf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if r_pdf.returncode != 0 or not os.path.exists(pdf_path):
                print(f"  [ERROR] Lỗi biên dịch xelatex. Mã lỗi: {r_pdf.returncode}")
                return False
                
            if not pdftoppm_found:
                print("  [WARNING] Đã biên dịch PDF thành công nhưng thiếu pdftoppm để chuyển sang PNG.")
                return True
                
            # Chuyển đổi PDF sang PNG
            cmd_png = ["pdftoppm", "-png", "-r", "300", "-singlefile", pdf_path, base_name]
            r_png = subprocess.run(cmd_png, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if r_png.returncode == 0 and os.path.exists(output_path):
                print(f"  [SUCCESS] Đã tạo thành công ảnh sơ đồ TikZ: {output_path}")
                # Dọn dẹp tệp trung gian
                for ext in [".aux", ".log", ".pdf"]:
                    tmp_f = base_name + ext
                    if os.path.exists(tmp_f):
                        os.remove(tmp_f)
                return True
            else:
                print(f"  [ERROR] Lỗi chuyển đổi pdftoppm. Mã lỗi: {r_png.returncode}")
                return False
        except Exception as e:
            print(f"  [ERROR] Lỗi không xác định trong quá trình biên dịch TikZ: {e}")
            return False