# ĐÁP ÁN PHIẾU HỌC TẬP — Bài 6: NHIỆT NÓNG CHẢY RIÊNG

---

## I. NHIỆM VỤ KHÁM PHÁ

### Nhiệm vụ 1: Điền khuyết định nghĩa

1. **1 kg** — **nhiệt độ nóng chảy**
2. **J/kg**
3. **λm** — **nhiệt lượng cần truyền** — **khối lượng của vật**

---

### Nhiệm vụ 2: Ghép nối đa biến

| Cột A | Đáp án | Cột B |
|:---:|:---:|:---|
| 1. Nhiệt nóng chảy riêng | **d** | d. J/kg |
| 2. Nhiệt dung riêng | **a** | a. J/(kg·K) |
| 3. Công thức tính λ | **e** | e. λ = Q/m |
| 4. Nhiệt độ nóng chảy của nước đá | **c** | c. 0°C |
| 5. Nhiệt lượng Q | **b** | b. Q = λm |

---

### Nhiệm vụ 3: Sắp xếp thao tác thí nghiệm

**Thứ tự đúng: b → e → d → a → c**

| Thứ tự | Thao tác | Giải thích |
|--------|----------|------------|
| 1 | **b** | Cho nước đá + nước lạnh vào nhiệt lượng kế |
| 2 | **e** | Cắm nhiệt kế vào bình |
| 3 | **d** | Nối oát kế, nguồn điện |
| 4 | **a** | Bật nguồn đun |
| 5 | **c** | Khuấy & đo dữ liệu mỗi 2 phút |

---

## II. NHIỆM VỤ TRỌNG TÂM

### Nhiệm vụ 4: Phân tích hiện tượng

**Đáp án: A. 167 kJ**

**Lời giải:**
- Khối lượng nước đá: m = 0,5 kg
- Nhiệt nóng chảy riêng: λ = 334 kJ/kg
- Nhiệt lượng nóng chảy: Q = λ × m = 334 × 0,5 = **167 kJ**

---

## III. NHIỆM VỤ VẬN DỤNG

### Nhiệm vụ 5: Engineering Debugger

| Lỗi | Sửa |
|-----|-----|
| 1. **Bình nhựa thường** — không cách nhiệt, mất nhiệt lớn | **Dùng bình nhiệt lượng kế** (có vỏ xốp, nắp kín, có dây điện trở đun) |
| 2. **Đun bếp ga** — nhiệt lượng không đo được, không đồng đều | **Dùng điện trở đun + oát kế** đo công suất P và thời gian t → Q = Pt |
| 3. **Công thức sai: λ = Q·m** — đơn vị sai (J·kg thay vì J/kg) | **λ = Q/m** (J/kg) |

---

## IV. MỞ RỘNG

### Nhiệm vụ 6: Bài tập Tổng hợp

**Cho:**
- m_đá = 0,2 kg, t_đá = 0°C
- m_nước = 0,4 kg, t_nước = 20°C
- m_nhôm = 0,1 kg, t_nhôm = 20°C
- λ = 334 kJ/kg = 334 000 J/kg
- c_nước = 4 200 J/(kg·K)
- c_nhôm = 900 J/(kg·K)

---

**a. Nhiệt lượng để đá tan hoàn toàn:**

Q₁ = λ × m_đá = 334 000 × 0,2 = **66 800 J = 66,8 kJ**

---

**b. Nhiệt độ cân bằng t (°C):**

*Phương trình cân bằng nhiệt:*

Nhiệt thu (đá tan + nước đá nóng lên):
- Q_đá_tan = λ·m_đá = 66 800 J
- Q_đá_nóng = c_nước·m_đá·(t - 0) = 4 200 × 0,2 × t = 840 t

Nhiệt tỏa (nước + cốc nhôm nguội):
- Q_nước_nguội = c_nước·m_nước·(20 - t) = 4 200 × 0,4 × (20 - t) = 1 680(20 - t)
- Q_nhôm_nguội = c_nhôm·m_nhôm·(20 - t) = 900 × 0,1 × (20 - t) = 90(20 - t)

Cân bằng:
66 800 + 840 t = 1 680(20 - t) + 90(20 - t)  
66 800 + 840 t = 1 770(20 - t)  
66 800 + 840 t = 35 400 - 1 770 t  
840 t + 1 770 t = 35 400 - 66 800  
2 610 t = -31 400

→ **t ≈ -12°C** ❌ **Vô lý!** (nhiệt độ không thể âm khi có đá 0°C)

**Giải thích:** Nhiệt lượng của nước + nhôm (ở 20°C) **không đủ** để tan hết 200 g đá ở 0°C.

**Tính nhiệt lượng tối đa nước+nhôm có thể tỏa (về 0°C):**
Q_max = (c_nước·m_nước + c_nhôm·m_nhôm) × (20 - 0)  
= (1 680 + 90) × 20 = 35 400 J

Mà cần 66 800 J để tan hết đá → **Chỉ tan một phần đá**.

**Khối lượng đá tan được:**
m_tan = Q_max / λ = 35 400 / 334 000 ≈ **0,106 kg = 106 g**

**Kết luận:** Cục đá 200 g chỉ tan 106 g, còn lại 94 g đá. Nhiệt độ cân bằng **t = 0°C**.

---

## V. KẾT QUẢ HỌC TẬP

| Mục tiêu | Đạt / Chưa đạt |
|----------|:--------------:|
| Nêu được λ, đơn vị, công thức | ✅ |
| Vận dụng λ giải bài tập | ✅ |
| Mô tả thí nghiệm xác định λ | ✅ |
| Giải thích hiện tượng thực tế | ✅ |

---

*Đáp án: Kha Khung Hiệp — Đòn Bẩy AI*