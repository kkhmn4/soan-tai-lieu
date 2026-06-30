# KỊCH BẢN DẠY HỌC — BÀI 1: CẤU TRÚC CỦA CHẤT
## Vật Lý 12 — Kết nối tri thức (GDPT 2018)

> **Công cụ:** Google Flow + Toolflow (Batch Gen + @ref binding)  
> **Thời lượng:** 2 tiết  
> **Giáo viên:** Kha Khung Hiệp  

---

## 📌 MỤC TIÊU BÀI HỌC (YCCĐ)

1. Trình bày được mô hình cấu trúc của chất (rắn, lỏng, khí) dựa trên thuyết động học phân tử.
2. Giải thích được sự khác biệt giữa các thể (rắn, lỏng, khí) về khoảng cách và tương tác phân tử.
3. Vận dụng giải thích các hiện tượng thực tế: bay hơi, khuếch tán, áp suất khí.
4. Xác định các yếu tố ảnh hưởng đến quá trình chuyển thể và nêu ứng dụng.

---

## 🎨 @REF BANK (UPLOAD TRƯỚC)

| @refKey | Nội dung | Mô tả |
|---------|----------|-------|
| `@teacher_hiệp` | Avatar giáo viên | Chân dung giáo viên Kha Khung Hiệp (bán thân, phong cách giảng dạy) |
| `@atom_core` | Hạt nhân nguyên tử | Cấu trúc proton/neutron (3D, tối giản) |
| `@molecule_h2o` | Phân tử nước (H₂O) | 2H + 1O, liên kết cộng hóa trị |
| `@lattice_nacl` | Mạng tinh thể NaCl | Cấu trúc ion khối vuông, màu xanh/trắng |
| `@gas_particles` | Hạt khí chuyển động | Các chấm tròn sáng chuyển động Brown |
| `@liquid_water` | Nước thể lỏng | Phân tử nước sắp xếp gần, trật tự ngắn |
| `@solid_ice` | Nước đá thể rắn | Tinh thể băng 6 cạnh, mạng lưới liên kết H |
| `@diffusion_demo` | Khuếch tán mực trong nước | Giọt mực tim lan tỏa trong cốc nước |
| `@pressure_demo` | Áp suất khí | Pittong - phân tử khí va chạm thành bình |
| `@bg_classroom` | Phòng học | Background lớp học vật lý |
| `@bg_lab` | Phòng thí nghiệm | Background lab thực hành |

---

## 📋 CÁC CẢNH (PROMPTS) CHO BATCH GEN

### 🟦 ĐVKT 1: MÔ HÌNH CẤU TRÚC CHẤT

| # | Tiêu đề | Prompt cho Batch Gen |
|---|---------|---------------------|
| 1 | **Slide mở đầu** | `@bg_classroom` Phòng học vật lý hiện đại, bảng xanh, bàn thí nghiệm. Giáo viên `@teacher_hiệp` đứng cạnh mô hình phân tử 3D. Ánh sáng tự nhiên, phong cách sư phạm, 16:9. |
| 2 | **Ba thể của chất** | Sơ đồ 3 khối: rắn (tinh thể muối `@lattice_nacl`) → lỏng (`@liquid_water`) → khí (`@gas_particles`). Mũi tên chuyển thể màu cam. Background trắng sạch, phong cách infographic, 16:9. |
| 3 | **Khoảng cách phân tử** | So sánh trực quan: 3 ô vuông cạnh nhau. Trái: Rắn - `@lattice_nacl` chặt khít. Giữa: Lỏng - `@liquid_water` gần nhau. Phải: Khí - `@gas_particles` xa nhau. Chú thích số liệu, 16:9. |
| 4 | **Chuyển động Brown** | Kính hiển vi + hạt phấn hoa trong nước. Chấm sáng nhỏ chuyển động zigzag. `@bg_lab` Background lab tối. Phong cách macro shot, 16:9. |
| 5 | **Mô phỏng khí trong bình** | `@pressure_demo` Bình kính chứa `@gas_particles` chuyển động hỗn loạn. Mũi tên lực va chạm màu đỏ. Pittong màu xám. Phong cách đồ họa kỹ thuật, 16:9. |

### 🟩 ĐVKT 2: SO SÁNH RẮN — LỎNG — KHÍ

| # | Tiêu đề | Prompt cho Batch Gen |
|---|---------|---------------------|
| 6 | **Cấu trúc tinh thể** | `@lattice_nacl` Mạng tinh thể NaCl 3D. Ion Na⁺ xanh dương, Cl⁻ xanh lá. Các đường nối trật tự. Nền tối, hightlight cạnh ô mạng. 16:9. |
| 7 | **Nước thể lỏng** | `@liquid_water` Phân tử `@molecule_h2o` ở gần nhau nhưng trật tự ngắn. Liên kết H đứt - tạo. Màu trong suốt xanh nhạt. 16:9. |
| 8 | **Tinh thể băng** | `@solid_ice` Mạng tinh thể băng 6 cạnh. Liên kết H giữa các `@molecule_h2o`. Màu xanh băng trong suốt, ánh sáng mặt trời. 16:9. |
| 9 | **Bảng so sánh 3 thể** | Bảng 3 cột: Rắn/Lỏng/Khí. Hàng: Khoảng cách, Tương tác, Chuyển động, Thể tích, Hình dạng. Icons cho mỗi ô. Infographic, 16:9. |

### 🟨 ĐVKT 3: ỨNG DỤNG THỰC TẾ

| # | Tiêu đề | Prompt cho Batch Gen |
|---|---------|---------------------|
| 10 | **Khuếch tán trong chất lỏng** | `@diffusion_demo` Cốc thủy tinh trong suốt. Giọt mực tím bắt đầu lan tỏa. Các `@molecule_h2o` và phân tử mực hòa trộn. 16:9. |
| 11 | **Bay hơi mặt thoáng** | Ao nước nhỏ, các `@molecule_h2o` ở mặt thoáng bay lên. Mũi tên thể hiện chuyển động thoát khỏi bề mặt. Ánh nắng, 16:9. |
| 12 | **Kết tinh trong tự nhiên** | `@lattice_nacl` Hình thành tinh thể muối từ dung dịch bốc hơi. Cận cảnh tinh thể phát triển từng lớp. Macro style, 16:9. |
| 13 | **Ảnh hưởng nhiệt độ lên áp suất** | `@pressure_demo` Bình kín bị đun nóng. `@gas_particles` chuyển động nhanh hơn, va chạm mạnh hơn. Nhiệt kế chỉ nhiệt độ tăng. 16:9. |

### 🟪 SLIDE KẾT BÀI + CỦNG CỐ

| # | Tiêu đề | Prompt cho Batch Gen |
|---|---------|---------------------|
| 14 | **Sơ đồ tư duy tổng kết** | Mindmap trung tâm: "Cấu trúc chất". Nhánh: Rắn - Lỏng - Khí - Chuyển thể - Ứng dụng. Màu sắc phân cấp. Nền trắng, 16:9. |
| 15 | **Bài tập củng cố (Slide QA)** | `@bg_classroom` Giáo viên `@teacher_hiệp` chỉ bảng với câu hỏi: "Tại sao chất khí dễ nén hơn chất lỏng?". Phong cách lớp học, 16:9. |

---

## 🚀 CÁCH CHẠY TRONG TOOLFLOW

### Bước 1: Upload Ref Bank
```
📚 Ref Bank → Upload 12 ảnh tương ứng với @refKeys ở trên
  (có thể dùng AI vẽ trước hoặc ảnh minh họa sưu tầm)
```

### Bước 2: Mở Batch Gen
```
🎨 Batch Gen → Paste prompts từ 15 cảnh ở trên
```

### Bước 3: Bind @refKeys
```
🔗 Bind all refs → Tự động thêm @refKeys vào prompts
```

### Bước 4: Gen Batch
```
Chọn burst ×2 (8 ảnh/cảnh → chọn ảnh đẹp nhất)
→ 🎬 Gen batch
```

### Bước 5: Sequence workflow (tùy chỉnh)
```
Sau khi có ảnh → dùng Edit action + refs:
  - Cảnh 1 ÷ 2: setting chung (bối cảnh)
  - Cảnh 3 ÷ 9: infographic (style phẳng)
  - Cảnh 10 ÷ 15: ảnh thực tế (photorealistic)
```

---

## 📐 THÔNG SỐ GEN KHUYẾN NGHỊ

| Tham số | Giá trị |
|---------|---------|
| **Aspect ratio** | 16:9 (ngang) — phù hợp slide trình chiếu |
| **Resolution** | 4K (3840×2160) — nếu dùng cho video |
| **Burst count** | ×2 hoặc ×3 — để có nhiều variant chọn |
| **Model** | Omni Flash (nếu video) / Web (nếu ảnh) |
| **Workers** | 1 (đảm bảo ref chain tuần tự) |
| **Cooldown** | 30-60 giây giữa các lần gen |

---

## 📂 FILE OUTPUT

```
Khi chạy xong, các ảnh/video nằm ở:
  ~/.hermes/google-flow/toolflow/output/<project>/BATCH_01.png ...
  ~/.hermes/google-flow/toolflow/output/<project>/BATCH_02.png ...

Ghép vào slide bài giảng hoặc video:
  - PowerPoint: Chèn ảnh → chỉnh sửa → xuất slide
  - Video: Dùng FFmpeg hoặc CapCut ghép ảnh + TTS
```