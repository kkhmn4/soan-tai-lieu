# NOTEBOOKLM PROMPT — Bài 6: NHIỆT NÓNG CHẢY RIÊNG

# GEMS v8.0 — NotebookLM Integration

# Dùng để: Copy vào NotebookLM (notebooklm.google.com) để tạo trợ lý AI soạn bài

## 📋 NỘI DUNG NHẬP VÀO NOTEBOOKLM (Sources)

### Source 1: YCCĐ & Kiến thức cốt lõi (copy toàn bộ phần này)

```
CHỦ ĐỀ 6: NHIỆT NÓNG CHẢY RIÊNG — Vật lý 12 (Kết nối tri thức)

YÊU CẦU CẦN ĐẠT (YCCĐ):
- YCCĐ-1: Nêu được khái niệm nhiệt nóng chảy riêng, kí hiệu λ, đơn vị J/kg
- YCCĐ-2: Viết được công thức Q = λm và vận dụng giải bài tập
- YCCĐ-3: Mô tả được phương án thí nghiệm xác định λ nước đá
- YCCĐ-4: Giải thích được hiện tượng thực tế: tan băng, đúc kim loại, muối trên đường

KIẾN THỨC CỐT LÕI:
ĐVKT 1: Định nghĩa λ = Q/m. Đơn vị: J/kg. Bảng λ: Nước đá 334, Nhôm 398, Đồng 205, Sắt 247, Thép 272, Chì 23, Thiếc 59 (kJ/kg)
ĐVKT 2: Công thức Q = λm. Đặc điểm quá trình nc: nhiệt độ không đổi. Đồ thị T(t): đoạn ngang tại T_nc
ĐVKT 3: Thí nghiệm xác định λ nước đá: Nhiệt lượng kế + điện trở + oát kế + nhiệt kế. Thứ tự: b→e→d→a→c
ĐVKT 4: Cân bằng nhiệt có nhiệt nóng chảy. Q_thu = Q_tỏa. Trường hợp không đủ nhiệt tan hết → t = 0°C, còn đá

QUAN NIỆM SAI LẦM:
1. λ phụ thuộc khối lượng → Sai: λ là hằng số chất
2. Đá tan thì nhiệt độ tăng → Sai: T không đổi trong quá trình nc
3. λ và c là một → Sai: λ [J/kg] khác c [J/(kg·K)]
4. Đơn vị λ là J/(kg·K) → Sai: đơn vị J/kg (không có K/độ)
```

### Source 2: Phiếu học tập (PHT) — 6 Nhiệm vụ (copy toàn bộ)

```
PHIẾU HỌC TẬP — Bài 6: NHIỆT NÓNG CHẢY RIÊNG

NHIỆM VỤ 1 (Visual Cloze Test): Điền khuyết định nghĩa λ
- "Nhiệt nóng chảy riêng của một chất là nhiệt lượng cần làm cho ___ chất đó nóng chảy hoàn toàn ở ___."
- "Kí hiệu: λ. Đơn vị: ___"
- "Công thức: Q = ___. Q là ___, m là ___"

NHIỆM VỤ 2 (Matching Matrix): Ghép đa biến
- 1. Nhiệt nóng chảy riêng → d. J/kg
- 2. Nhiệt dung riêng → a. J/(kg·K)
- 3. Công thức tính λ → e. λ = Q/m
- 4. Nhiệt độ nc nước đá → c. 0°C
- 5. Nhiệt lượng Q → b. Q = λm

NHIỆM VỤ 3 (Algorithmic Ordering): Sắp xếp thao tác TN
Thứ tự đúng: b → e → d → a → c
a. Bật nguồn điện
b. Cho nước đá + nước lạnh vào bình nhiệt lượng kế
c. Khuấy liên tục, đọc số đo 2 phút/lần
d. Nối oát kế với nhiệt lượng kế và nguồn điện
e. Cắm nhiệt kế vào bình

NHIỆM VỤ 4 (Contextual MCQ): Bài toán thực tế
Cho: m_đá = 0,5 kg ở 0°C, λ = 334 kJ/kg
Q = ? → Q = λm = 334 × 0,5 = 167 kJ → Đáp án A

NHIỆM VỤ 5 (Engineering Debugger): Tìm 3 lỗi thiết kế TN
Kế hoạch sai: "Bình nhựa thường, đun bếp ga, λ = Q·m"
Lỗi 1: Bình nhựa thường → mất nhiệt → Sửa: Nhiệt lượng kế cách nhiệt
Lỗi 2: Đun bếp ga → không đo P → Sửa: Điện trở + oát kế (Q = Pt)
Lỗi 3: λ = Q·m sai đơn vị → Sửa: λ = Q/m (J/kg)

NHIỆM VỤ 6 (Vận dụng cao): Tổng hợp
Đá 200g (0°C) + Nước 400g (20°C) + Cốc nhôm 100g (20°C)
λ = 334, c_nước = 4,2, c_nhôm = 0,9 kJ/(kg·K)
a. Q_tan = 66,8 kJ
b. Q_max tỏa = 35,4 kJ < 66,8 kJ → Không đủ nhiệt
→ t = 0°C, tan 106g đá, còn 94g đá rắn
```

### Source 3: Kế hoạch bài dạy (5E + EDP)

```
KẾ HOẠCH BÀI DẠY — 90 phút (2 tiết)

ENGAGE (5'): Khởi động - Câu hỏi "Tại sao đá tan mà nước vẫn 0°C?" + Video băng tan Bắc Cực
→ KWL: Know / Want / Learn

EXPLORE (20'): Khám phá - Station Learning 3 trạm
Trạm 1: NV1 điền khuyết định nghĩa
Trạm 2: NV2 ghép nối đơn vị/công thức
Trạm 3: NV3 sắp xếp thao tác thí nghiệm
→ Research: Tự tìm hiểu λ, công thức, quy trình

EXPLAIN (25'): Giải thích - Hệ thống hóa trên slide
+ Think-Pair-Share: Thảo luận NV4 (Q = λm)
+ Sửa sai lầm: λ ≠ c, đơn vị J/kg
+ Sơ đồ tư duy trên bảng

ELABORATE (25'): Mở rộng
+ Engineering Debugger (NV5): Tìm/sửa lỗi TN
+ Bài tập tổng hợp (NV6): Cân bằng nhiệt có λ
→ Test & Evaluate

EVALUATE (10'): Đánh giá
+ Quiz nhanh 5 câu (Kahoot/giấy)
+ Tự đánh giá 4 mục tiêu MT1-MT4
+ Giao Homework (18 MCQ + 4 Đ/S + 6 TL)

PHƯƠNG PHÁP: KWL, Think-Pair-Share, Station Learning, Engineering Debugger
```

### Source 4: Bài tập về nhà (18 MCQ + 4 Đ/S + 6 TL)

```
HOMEWORK — Bài 6: NHIỆT NÓNG CHẢY RIÊNG

PHẦN I: 18 TRẮC NGHIỆM (4 phương án)
A. Nhận biết (6): Định nghĩa λ, đơn vị, công thức, T_nc nước đá, yếu tố ảnh hưởng λ, chất có λ max
B. Thông hiểu (6): Đồ thị T(t), dụng cụ không cần (Vôn kế), hiện tượng đá tan, oát kế đo P, muối đường, đúc thép
C. Vận dụng (6): Tính m từ Q, tính Q cho 2kg nhôm, cân bằng nhiệt đá-nước, đun chảy đồng, tìm λ thiếc, hiệu suất lò nấu thép

PHẦN II: 4 ĐÚNG/SAI (mỗi câu 4 ý a,b,c,d)
C1: Quá trình nóng chảy (Đ, S, Đ, S)
C2: Thí nghiệm λ (Đ, S, Đ, Đ)
C3: Đá 50g + nước 100g@40°C (Đ, Đ, Đ, Đ)
C4: Ứng dụng thực tế (S, Đ, Đ, S)

PHẦN III: 6 TỰ LUẬN NGẮN
1. Q tan 0,8kg đá = 267,2 kJ
2. Q đun chảy 500g nhôm từ 20°C = 487 kJ
3. Đá 200g + nước 300g@30°C + cốc nhôm 100g → t = 0°C (còn đá)
4. Tìm λ chì từ cân bằng nhiệt (dữ liệu minh họa)
5. Than đá cho lò nấu 5 tấn thép hiệu suất 50%
6. Bất phương trình điều kiện tan hết đá: M·c·T > m·λ
```

---

## 🎯 PROMPT CHO NOTEBOOKLM (Copy vào chat NotebookLM sau khi add sources)

> **Prompt 1 — Tóm tắt bài học cho học sinh:**
> "Hãy tóm tắt bài 'Nhiệt nóng chảy riêng' thành 5 gạch đầu dòng quan trọng nhất, dùng ngôn ngữ đơn giản dành cho học sinh lớp 12. Nhấn mạnh: định nghĩa λ, công thức Q = λm, đơn vị J/kg, thí nghiệm chính, và 1 ứng dụng thực tế."
>
> **Prompt 2 — Tạo câu hỏi ôn tập:**
> "Tạo 10 câu hỏi trắc nghiệm ôn tập (4 phương án) bao phủ 4 YCCĐ, mức độ từ Nhận biết đến Vận dụng cao. Mỗi câu có đáp án và giải thích 1-2 câu."
>
> **Prompt 3 — Phân tích sai lầm học sinh:**
> "Dựa trên 4 quan niệm sai liệt kê, hãy viết 4 tình huống ngắn (mỗi 3-4 dòng) mà học sinh thường mắc lỗi, kèm cách giải thích sửa sai dành cho GV."
>
> **Prompt 4 — Kịch bản video 5 phút:**
> "Viết kịch bản video 5 phút dạy 'Nhiệt nóng chảy riêng' theo cấu trúc: Mở đầu (hook 30s) → Khái niệm (90s) → Thí nghiệm (90s) → Bài tập mẫu (60s) → Tổng hợp/Ứng dụng (60s). Mỗi đoạn có gợi ý hình ảnh minh họa."
>
> **Prompt 5 — Bảng so sánh λ vs c:**
> "Tạo bảng so sánh chi tiết giữa 'Nhiệt nóng chảy riêng (λ)' và 'Nhiệt dung riêng (c)' theo các cột: Định nghĩa, Công thức, Đơn vị, Ý nghĩa vật lý, Vai trò trong cân bằng nhiệt, Ví dụ giá trị nước. Format markdown table."

---

## 📁 LƯU FILE NÀY VÀO:

`output/hermes/bai6_nhiet_nong_chay_rieng/notebooklm/bai6_notebooklm_prompts.md`

---

## 🔧 HƯỚNG DẪN SỬ DỤNG

1. Mở **notebooklm.google.com** → Tạo notebook mới: "VL12 - Bài 6: Nhiệt nóng chảy riêng"
2. **Add Sources** (4 nguồn trên): Copy từng block "Source 1-4" → Paste vào NotebookLM
3. **Chat với NotebookLM**: Copy từng **Prompt 1-5** vào chat để sinh nội dung hỗ trợ
4. **Lưu kết quả**: NotebookLM sẽ trả lời dựa trên sources bạn cung cấp → Copy kết quả vào giáo án/slide

---

*File này là một phần của pipeline GEMS v8.0 — Tích hợp NotebookLM*
*Tác giả: Kha Khung Hiệp — Đòn Bẩy AI*
