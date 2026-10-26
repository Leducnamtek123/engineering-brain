# Backlog

## Bây giờ
- ~~Chạy baseline và có skill cho 2 ca~~ (xong 2026-10-26: skill cắt hết báo sai, chưa tăng tỷ lệ bắt lỗi).
- ~~Xử lý bài học Prisma `undefined`~~ (xong: A2, ca 003, v0.1.2).
- Chạy lại ca 001 và 002 với v0.1.2 (chưa kiểm chứng sau lần sửa câu chữ A2).
- ~~Ca khó: service, update/delete, orgId lồng; chạy sonnet + haiku~~ (xong vòng 3: 24/24 trúng ở mọi cấu hình, nên vẫn chưa đo được tỷ lệ bắt lỗi; skill cắt báo sai của haiku 3 → 0).
- ~~Ca dạng repo nhiều file~~ (xong vòng 4: 8/8 trúng ở mọi cấu hình. Qua 42 lượt chưa có baseline nào bỏ sót IDOR).
- **Quyết định cần người chốt:** với lỗi phân quyền kiểu IDOR, model đã tự làm tốt, nên skill này chỉ còn giá trị ở độ chính xác và khuôn báo cáo. Hai hướng:
  1. Giữ skill gọn như hiện tại để dùng cho model nhỏ và CI, rồi chuyển sang skill khác.
  2. Chuyển sang mảng mà model hay sai vì **quy ước riêng của dự án** (ví dụ cách đặt tên quyền, policy layer nội bộ, quy ước multi-tenant của Square). Ở đó skill có cơ hội tăng tỷ lệ bắt lỗi.
- Nếu muốn đo tiếp tỷ lệ bắt lỗi: lấy diff thật từ lịch sử bug của dự án (lỗi đã từng lọt qua review), không tự viết ca.
- Thêm 8–18 ca nữa từ dự án thật (đã xoá dữ liệu nhạy cảm), có cả ca negative.
- Nhờ người có chuyên môn bảo mật duyệt `A1` để lên `reviewed`.

## Sau
- Luật tiếp theo cho phân quyền: tin `userId` / `role` từ body, mass assignment, endpoint admin thiếu kiểm vai trò.
- Skill thứ hai, chọn theo lỗi lặp lại nhiều nhất trong `lessons/`.
- Thêm index tìm kiếm (basic-memory) khi grep không còn đủ.
