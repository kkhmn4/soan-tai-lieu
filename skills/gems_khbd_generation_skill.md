---
name: gems-khbd-generation
description: Hướng dẫn Agent AI tự động biên soạn Kế hoạch bài dạy (Giáo án) chi tiết theo Công văn 5512 môn Vật lý đạt chuẩn GEMS v8.0.
---

# SKILL: GEMS KHBD (LESSON PLAN) GENERATION STANDARDS

Tài liệu này định nghĩa bộ tiêu chuẩn sư phạm và quy chuẩn định dạng bắt buộc dành cho các Agent AI khi tự động biên soạn **Kế hoạch bài dạy (KHBD / Giáo án)** môn Vật lý trung học phổ thông.

---

## 1. TIÊU CHUẨN SƯ PHẠM (CÔNG VĂN 5512)

Kế hoạch bài dạy phải tuân thủ nghiêm ngặt cấu trúc 4 phần lớn theo quy định của **Công văn 5512/BGDĐT-GDTrH**:

### I. Yêu cầu cần đạt
- **Năng lực đặc thù (Vật lí):** Phân rã cụ thể thành 3 thành phần năng lực:
  - *Nhận thức vật lí:* Phát biểu định nghĩa, viết công thức, nêu đặc điểm...
  - *Tìm hiểu thế giới tự nhiên:* Nêu phương án thực nghiệm, phân tích số liệu...
  - *Vận dụng kiến thức, kĩ năng:* Giải thích hiện tượng thực tế, giải bài tập...
- **Năng lực chung:** Tự học, Giao tiếp & Hợp tác.
- **Phẩm chất:** Chăm chỉ, Trung thực.

### II. Thiết bị dạy học và học liệu
- Phân tách rõ ràng giữa:
  - *Giáo viên:* Máy chiếu, dụng cụ thí nghiệm (số lượng cụ thể), phiếu học tập.
  - *Học sinh:* SGK, vở ghi, thiết bị di động để chạy mô phỏng (nếu có).

### III. Tiến trình dạy học
Triển khai mạch học tuyến tính qua 4 Hoạt động chính:
1. **Hoạt động 1: Khởi động (Xác định nhiệm vụ học tập)** - 10-15 phút.
2. **Hoạt động 2: Hình thành kiến thức mới (Giải quyết nhiệm vụ)** - 35-40 phút.
3. **Hoạt động 3: Luyện tập** - 25-30 phút.
4. **Hoạt động 4: Vận dụng** - 10 phút.

> [!IMPORTANT]
> **Yêu cầu bắt buộc đối với mỗi Hoạt động:**
> Mỗi hoạt động phải có đầy đủ 4 nội dung:
> - **Mục tiêu:** HS đạt được năng lực cụ thể nào sau hoạt động.
> - **Nội dung:** Nhiệm vụ học tập cụ thể giao cho HS (đọc SGK, làm thí nghiệm, thảo luận).
> - **Sản phẩm:** Kết quả bằng văn bản, câu trả lời hoặc phiếu học tập đã điền của HS.
> - **Tổ chức thực hiện:** Phải mô tả chi tiết quy trình 4 bước tương tác (Giao - Nhận - Báo cáo - Chốt):
>   - **Bước 1: Chuyển giao nhiệm vụ** (Giáo viên giao nhiệm vụ).
>   - **Bước 2: Thực hiện nhiệm vụ** (Học sinh làm việc cá nhân/nhóm).
>   - **Bước 3: Báo cáo, thảo luận** (Học sinh trình bày, phản biện).
>   - **Bước 4: Kết luận, nhận định** (Giáo viên chuẩn hóa kiến thức).

### IV. Phần Điều chỉnh sau bài dạy & Chữ ký
- **Mục điều chỉnh:** Bắt buộc có các mục: `Ưu điểm:`, `Hạn chế:`, `Hướng điều chỉnh:` và tự động chèn **2 dòng chấm nét đứt** phía sau mỗi mục để viết tay.
- **Bảng chữ ký xác nhận (Signature Block):** Bảng 2 cột không viền ở cuối bài dạy:
  - *Cột trái:* XÁC NHẬN CỦA TỔ CHUYÊN MÔN / (Ký và ghi rõ họ tên).
  - *Cột phải:* GIÁO VIÊN SOẠN / (Ký và ghi rõ họ tên).

---

## 2. QUY CHUẨN ĐỊNH DẠNG WORD (DOCX) THEO GEMS V8.0

Mọi tệp tin KHBD khi xuất ra định dạng `.docx` phải tuân thủ các quy tắc định dạng nâng cao sau:

### 1. Typography & Căn lề trang (A4 Setup)
- **Font chữ:** Chỉ sử dụng duy nhất font **Times New Roman**.
- **Căn lề (Margins):**
  - Lề trái: **3.0 cm** (dành cho đóng gáy/lưu trữ).
  - Lề phải, trên, dưới: **2.0 cm**.
- **Giãn dòng (Line Spacing):** Đặt cố định giãn dòng **1.3 lines** (Fixed 22pt) cho đoạn thường.
- **Giãn đoạn (Paragraph Spacing):** Khoảng cách trước/sau đoạn là **6pt** (`space_before = Pt(6)`, `space_after = Pt(6)`).
- **Thụt dòng đầu:** Tất cả các đoạn văn thường (Body text) phải thụt dòng đầu **1.0 cm** (`first_line_indent = Cm(1.0)`).
- **Căn lề văn bản:** Căn đều 2 bên (Justified) cho các đoạn nội dung.

### 2. Thiết lập Bảng hoạt động (Teacher - Student Table)
- Trong các hoạt động tổ chức thực hiện, sử dụng bảng **2 cột**:
  - *Cột trái (rộng 8.25 cm):* Hoạt động của Giáo viên.
  - *Cột phải (rộng 8.25 cm):* Hoạt động của Học sinh.
- **Bảo toàn phân trang bảng:**
  - Tiêu đề hàng bảng bắt buộc có thuộc tính lặp lại ở trang mới (`tblHeader`).
  - Dòng dữ liệu trong bảng bắt buộc thiết lập không bị ngắt đôi giữa 2 trang (`cantSplit`).

### 3. Tự động Bôi đậm từ khóa Sư phạm
Bộ chuyển đổi (Exporter) phải tự động nhận diện và in đậm màu Navy (`#1E3A5F`) đối với các nhãn hành động cốt lõi:
- `Chuyển giao nhiệm vụ:`, `Thực hiện nhiệm vụ:`, `Báo cáo, thảo luận:`, `Kết luận:`, `Kết luận, nhận định:`, `Sản phẩm:`, `Mục tiêu:`, `Nội dung:`

### 4. Xử lý LaTeX & Biểu thức Toán lý
- Sử dụng hàm filter `clean_latex` để dịch các ký tự toán học phổ biến (như `\Delta`, `\omega`, `\pi`) sang dạng ký tự Unicode in nghiêng tương ứng (`Δ`, `ω`, `π`).
- Loại bỏ toàn bộ các ký tự `$` bao quanh biểu thức toán trước khi ghi đè vào tệp Word.

---

## 3. CHỈ DẪN CHO AGENT AI (SYSTEM INSTRUCTION)

Khi nhận yêu cầu tạo mới hoặc chỉnh sửa Kế hoạch bài dạy, Agent cần:
1. Đọc kỹ file YCCĐ thô trong `tai-lieu-goc/` để phân tích sư phạm.
2. Dựng khung mục tiêu Năng lực & Phẩm chất bám sát YCCĐ đó.
3. Đề xuất hoạt động Khởi động liên quan đến hiện tượng thực tiễn sống động.
4. Tổ chức các hoạt động khám phá bám sát cấu trúc của Phiếu học tập của bài học.
5. In đậm các từ khóa sư phạm CV5512 trong quá trình sinh nội dung.
6. Sử dụng exporter `khbd_exporter.py` để xuất tệp Word, tuyệt đối không tự viết code xuất không qua engine.
