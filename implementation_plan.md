"# Kế hoạch nâng cấp học liệu GEMS Vật lý 12 (Bài 4, 5, 6, 7) đồng bộ Việt hóa & Bổ sung nhiệm vụ

Kế hoạch này chi tiết hóa phương án kỹ thuật nâng cấp quy trình tạo slide và infographic bằng NotebookLM, bổ sung slide hướng dẫn thực hiện nhiệm vụ, tích hợp nhiệm vụ học sinh trên infographic, đảm bảo đồng bộ 100% tiếng Việt và khớp nội dung với Phiếu học tập (PHT) cũng như Kế hoạch bài dạy cho cả 4 bài học (Bài 4, 5, 6, 7) chương Vật lý Nhiệt.

## User Review Required

> [!IMPORTANT]
> **1. Đồng bộ Việt hóa 100% và Loại bỏ ngoại ngữ:**
> * Cập nhật prompt focus của Slide và Infographic trong script `generate_notebook_materials.py` để chỉ thị AI sinh nội dung 100% bằng tiếng Việt.
> * Cấm tuyệt đối việc sử dụng tiếng Anh hoặc ngôn ngữ khác trên giao diện, đề mục, nhãn hay mô tả (ngoại trừ ký hiệu vật lý chuẩn như $Q, m, c, \Delta T, L, \lambda$).
> * Các file md nguồn (`_phieu_hoc_tap.md`, `_huong_dan_slide.md`, `_ke_hoach_bai_day.md`) sẽ được rà soát và viết bằng tiếng Việt chuẩn.

> [!IMPORTANT]
> **2. Bổ sung Slide Hướng dẫn thực hiện Nhiệm vụ sau mỗi ĐVKT:**
> * Trong mỗi tệp `_huong_dan_slide.md` của các bài, sau phần lý thuyết/nội dung của từng Đơn vị Kiến thức (ĐVKT), sẽ bổ sung thêm 1 slide có tiêu đề: **"Slide X.Y: Hướng dẫn thực hiện nhiệm vụ ĐVKT X"**.
> * Slide này sẽ ghi rõ các yêu cầu, câu hỏi hoặc bài tập mà học sinh phải làm trên Phiếu học tập/Infographic.
> * Cập nhật focus prompt của Slide trong script để AI NotebookLM bắt buộc phải tạo slide này, bám sát hướng dẫn 1-1.

> [!IMPORTANT]
> **3. Bổ sung Nhiệm vụ học sinh trên Infographic:**
> * Infographic của từng ĐVKT sẽ không chỉ có lý thuyết tóm t
<truncated 4845 bytes>