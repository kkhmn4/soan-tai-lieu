# Phase 04: Frontend UI & Components

Status: ⬜ Pending
Dependencies: [Phase 01: Setup Environment &amp; Project](file:///c:/Users/Admin/.antigravity-ide/t%E1%BA%A1o%20t%C3%A0i%20nguy%C3%AAn%20h%E1%BB%8Dc%20t%E1%BA%ADp/plans/260604-2043-gems-notebooklm-website/phase-01-setup.md)

## Objective

Thiết kế giao diện người dùng (UI) đẹp mắt, hiện đại, mang phong cách giáo dục cao cấp của GEMS, tối ưu hóa trải nghiệm tìm kiếm học liệu của thầy cô.

## Requirements

### Functional

- Trang chủ: Banner thu hút, giới thiệu kênh YouTube/TikTok, form đăng ký email đẹp mắt.
- Trang Kho học liệu: Bố cục lưới (Grid) hiển thị các thẻ học liệu (ResourceCard) gồm ảnh chụp, tên môn, bộ sách, lượt tải.
- Thanh tìm kiếm và bộ lọc hoạt động mượt mà bằng Client-side state hoặc URL params.
- Trang Chi tiết học liệu: Hiển thị hình ảnh rõ nét, video YouTube nhúng trực tiếp, và nút tải xuống.

### Non-Functional

- Giao diện đáp ứng (Responsive), hiển thị hoàn hảo trên cả điện thoại (Mobile) và máy tính (Desktop).
- Tốc độ tải trang nhanh, hình ảnh được tối ưu hóa bằng component `next/image`.
- Màu sắc phối hợp trang nhã (Tailwind slate/indigo/emerald), không sử dụng màu cơ bản chói mắt.

---

## Detailed UI 















































































  * *Nút hành động chính:* `TẢI XUỐNG HỌC LIỆU MIỄN PHÍ` (Nút lớn, hiệu ứng hover mượt mà).
  * *Ghi chú bản quyền:* *"Vui lòng không tự ý thương mại hóa sản phẩm. Hãy chia sẻ trực tiếp link website này đến đồng nghiệp."*

---

## Implementation Steps

1. [ ] Xây dựng layout chung (Navbar điều hướng, Footer thông tin liên hệ).
2. [ ] Thiết kế trang chủ `/` với khu vực "Hộp quà tặng" (Form đăng ký email nhận 100 Prompts).
3. [ ] Thiết kế trang kho tài nguyên `/resources` hiển thị danh sách thẻ học liệu kèm bộ lọc.
4. [ ] Thiết kế trang chi tiết học liệu `/resources/[id]` hiển thị mô tả đầy đủ, ảnh chụp thực tế và nút tải.
5. [ ] Tạo trang quản trị đơn giản `/admin` có form điền thông tin để upload học liệu mới.

## Files to Create/Modify

- `components/Navbar.tsx` - Thanh menu trên đầu trang
- `components/ResourceCard.tsx` - Thẻ hiển thị học liệu
- `app/page.tsx` - Trang chủ chính
- `app/resources/page.tsx` - Trang kho học liệu
- `app/resources/[id]/page.tsx` - Trang chi tiết
- `app/admin/page.tsx` - Trang upload học liệu cho Admin

## Test Criteria

- [ ] Mở thử trên mobile giả lập của Chrome DevTools xem bố cục có bị tràn/lỗi hiển thị không.
- [ ] Gõ thử vào thanh tìm kiếm xem kết quả lọc có phản hồi trực quan không.

---

Next Phase: [phase-05-integration.md](file:///c:/Users/Admin/.antigravity-ide/t%E1%BA%A1o%20t%C3%A0i%20nguy%C3%AAn%20h%E1%BB%8Dc%20t%E1%BA%ADp/plans/260604-2043-gems-notebooklm-website/phase-05-integration.md)
