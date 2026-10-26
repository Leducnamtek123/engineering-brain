# Backlog

## Bây giờ
- ~~Chạy baseline và có skill cho 2 ca~~ (xong 2026-10-26: skill cắt hết báo sai, chưa tăng tỷ lệ bắt lỗi).
- ~~Xử lý bài học Prisma `undefined`~~ (xong: A2, ca 003, v0.1.2).
- Chạy lại ca 001 và 002 với v0.1.2 (chưa kiểm chứng sau lần sửa câu chữ A2).
- Cần ca mà baseline **bỏ sót**, để đo skill có tăng tỷ lệ bắt lỗi không. Gợi ý: kiểm tra quyền nằm ở service, update hay delete theo id, id lồng nhau (`/orgs/:orgId/invoices/:id`), hoặc chạy bằng model nhỏ hơn (haiku).
- Thêm 8–18 ca nữa từ dự án thật (đã xoá dữ liệu nhạy cảm), có cả ca negative.
- Nhờ người có chuyên môn bảo mật duyệt `A1` để lên `reviewed`.

## Sau
- Luật tiếp theo cho phân quyền: tin `userId` / `role` từ body, mass assignment, endpoint admin thiếu kiểm vai trò.
- Skill thứ hai, chọn theo lỗi lặp lại nhiều nhất trong `lessons/`.
- Thêm index tìm kiếm (basic-memory) khi grep không còn đủ.
