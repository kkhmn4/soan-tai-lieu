import os
import sys
import json
import shutil
import re
from datetime import datetime

# Set stdout encoding to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def clean_no_accent_vietnamese(text: str) -> str:
    """Loại bỏ dấu tiếng Việt để đưa về dạng không dấu chuẩn."""
    unicode_map = {
        'a': 'áàảãạăắằẳẵặâấầẩẫậ',
        'A': 'ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ',
        'd': 'đ',
        'D': 'Đ',
        'e': 'éèẻẽẹêếềểễệ',
        'E': 'ÉÈẺẼẸÊẾỀỂỄỆ',
        'i': 'íìỉĩị',
        'I': 'ÍÌỈĨỊ',
        'o': 'óòỏõọôốồổỗộơớờởỡợ',
        'O': 'ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ',
        'u': 'úùủũụưứừửữự',
        'U': 'ÚÙỦŨỤƯỨỪỬỮỰ',
        'y': 'ýỳỷỹỵ',
        'Y': 'ÝỲỶỸỴ'
    }
    res = text
    for k, v in unicode_map.items():
        for char in v:
            res = res.replace(char, k)
    return res

def get_lesson_prefix(dir_name: str) -> str:
    """Tạo tiền tố tên bài chuẩn từ tên thư mục (ví dụ: bai4_nhiet_dung_rieng -> Bai 4 nhiet dung rieng)."""
    base_name = os.path.basename(dir_name)
    match = re.search(r'bai(\d+)', base_name.lower())
    if match:
        num = match.group(1)
        body = base_name.lower().replace(f"bai{num}", "").strip("_")
        body_no_accent = clean_no_accent_vietnamese(body).replace("_", " ").strip()
        return f"Bai {num} {body_no_accent}"
    else:
        body_no_accent = clean_no_accent_vietnamese(base_name).replace("_", " ").strip()
        return body_no_accent.capitalize()

def main():
    if len(sys.argv) < 2:
        print("Usage: python restructure_output.py <lesson_path>")
        sys.exit(1)
        
    lesson_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(lesson_path):
        print(f"Error: Path does not exist: {lesson_path}")
        sys.exit(1)
        
    slug = os.path.basename(lesson_path)
    lesson_prefix = get_lesson_prefix(lesson_path)
    
    print(f"Restructuring GEMS output for lesson: {lesson_prefix} (Slug: {slug})")
    
    # Ensure standard directories exist
    ready_dir = os.path.join(lesson_path, "ready")
    md_dir = os.path.join(lesson_path, "md")
    os.makedirs(ready_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)
    
    files_metadata = []
    
    # 1. First, search for all files recursively inside the lesson folder
    all_files = []
    for root, dirs, files in os.walk(lesson_path):
        for f in files:
            all_files.append((os.path.join(root, f), f))
            
    # 2. Process and move files based on GEMS naming rules
    for file_path, filename in all_files:
        dest_subfolder = "ready"
        new_name = None
        doc_type = "other"
        
        lower_name = filename.lower()
        
        # Word docs
        if lower_name.endswith(".docx"):
            if "phieu_hoc_tap" in lower_name:
                new_name = f"{slug}_phieu_hoc_tap.docx"
                doc_type = "PHT"
            elif "ke_hoach_bai_day" in lower_name:
                new_name = f"{slug}_ke_hoach_bai_day.docx"
                doc_type = "KHBD"
            elif "bai_tap_ve_nha" in lower_name or "homework" in lower_name:
                new_name = f"{slug}_bai_tap_ve_nha.docx"
                doc_type = "HW"
                
        # Slides
        elif lower_name.endswith(".pptx") and "slide" in lower_name:
            new_name = f"{slug}_slide_deck.pptx"
            doc_type = "Slides"
        elif lower_name.endswith(".pdf") and "slide" in lower_name:
            new_name = f"{slug}_slide_deck.pdf"
            doc_type = "Slides_PDF"
            
        # Infographics
        elif lower_name.endswith(".png") and "infographic" in lower_name:
            if lower_name.endswith("_infographic.png") or lower_name == "infographic.png":
                new_name = f"{slug}_infographic.png"
                doc_type = "Infographic"
            else:
                # Sub infographics, keep descriptive name
                desc = lower_name.replace("infographic_", "").replace(".png", "")
                new_name = f"{slug}_infographic_{desc}.png"
                doc_type = "Sub_Infographic"
                
        # LaTeX / TeX files
        elif lower_name.endswith(".tex"):
            if "dap_an" in lower_name:
                new_name = f"{slug}_dap_an.tex"
                doc_type = "Answer_Key"
            elif "bai_tap_ve_nha" in lower_name or "homework" in lower_name:
                new_name = f"{slug}_bai_tap_ve_nha.tex"
                doc_type = "HW_TeX"
                
        # Markdown source files (move to md/ if not already there)
        elif lower_name.endswith(".md"):
            dest_subfolder = "md"
            if "phieu_hoc_tap" in lower_name:
                new_name = f"{slug}_phieu_hoc_tap.md"
                doc_type = "PHT_MD"
            elif "ke_hoach_bai_day" in lower_name:
                new_name = f"{slug}_ke_hoach_bai_day.md"
                doc_type = "KHBD_MD"
            elif "huong_dan_slide" in lower_name:
                new_name = f"{slug}_huong_dan_slide.md"
                doc_type = "Slide_Guide_MD"
            elif "dac_ta_gems" in lower_name:
                new_name = f"{slug}_dac_ta_gems.md"
                doc_type = "Spec_MD"
            elif "bai_tap_ve_nha" in lower_name or "homework" in lower_name:
                new_name = f"{slug}_bai_tap_ve_nha.md"
                doc_type = "HW_MD"
                
        # Images (move to ready/hinh_anh/ for docx embed compatibility)
        elif lower_name.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")) and "infographic" not in lower_name:
            dest_subfolder = os.path.join("ready", "hinh_anh")
            new_name = filename
            doc_type = "Image"
            
        if new_name:
            dest_dir = os.path.join(lesson_path, dest_subfolder)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, new_name)
            
            if os.path.abspath(file_path) != os.path.abspath(dest_path):
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                shutil.move(file_path, dest_path)
                print(f"  Moved: {filename} -> {dest_subfolder}/{new_name}")
                
            files_metadata.append({
                "original_name": filename,
                "name": new_name,
                "type": doc_type,
                "format": new_name.split('.')[-1],
                "path": f"{dest_subfolder}/{new_name}".replace(os.sep, "/")
            })
            
    # 3. Clean up empty temporary directories
    subdirs_to_clean = ["worksheets", "homework", "docs", "generated", "images"]
    for subdir in subdirs_to_clean:
        subdir_p = os.path.join(lesson_path, subdir)
        if os.path.exists(subdir_p):
            try:
                for root, dirs, files in os.walk(subdir_p, topdown=False):
                    for d in dirs:
                        os.rmdir(os.path.join(root, d))
                os.rmdir(subdir_p)
                print(f"  Cleaned temporary folder: {subdir}")
            except Exception:
                pass
                
    # 4. Write/Update metadata.json
    metadata = {
        "lesson_name": lesson_prefix,
        "slug": slug,
        "updated_at": datetime.now().isoformat(),
        "files": files_metadata
    }
    
    with open(os.path.join(lesson_path, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print("✓ Successfully wrote metadata.json")

if __name__ == "__main__":
    main()