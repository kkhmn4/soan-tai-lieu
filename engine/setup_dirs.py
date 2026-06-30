import os

def create_project_directories():
    """Tự động tạo các thư mục đầu ra và lưu trữ của dự án GEMS."""
    directories = [
        "worksheets",
        "homework",
        "assets/images",
        "docs",
        "logs"
    ]
    
    print("[DIR] Dang tao cau truc thu muc cho du an GEMS...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  + Da tao thu muc: {directory}/")
        else:
            print(f"  o Thu muc da ton tai: {directory}/")
            
    print("[SUCCESS] Hoan thanh khoi tao thu muc!")

if __name__ == "__main__":
    create_project_directories()
