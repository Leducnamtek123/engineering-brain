# Backlog

## Bây giờ
- ~~Chạy baseline và có skill cho 2 ca~~ (xong 2026-10-26: skill cắt hết báo sai, chưa tăng tỷ lệ bắt lỗi).
- ~~Xử lý bài học Prisma `undefined`~~ (xong: A2, ca 003, v0.1.2).
- Chạy lại ca 001 và 002 với v0.1.2 (chưa kiểm chứng sau lần sửa câu chữ A2).
- ~~Ca khó: service, update/delete, orgId lồng; chạy sonnet + haiku~~ (xong vòng 3: 24/24 trúng ở mọi cấu hình, nên vẫn chưa đo được tỷ lệ bắt lỗi; skill cắt báo sai của haiku 3 → 0).
- Cần ca mà baseline **bỏ sót**: input giống repo thật (5–10 file, có code nhiễu, lỗi ở file khác nơi bắt đầu đọc), hoặc cho agent review cả một thư mục thay vì một đoạn dán. Lấy từ dự án thật nếu được (đã xoá dữ liệu nhạy cảm).
- Thêm 8–18 ca nữa từ dự án thật (đã xoá dữ liệu nhạy cảm), có cả ca negative.
- Nhờ người có chuyên môn bảo mật duyệt `A1` để lên `reviewed`.

## Sau
- Luật tiếp theo cho phân quyền: tin `userId` / `role` từ body, mass assignment, endpoint admin thiếu kiểm vai trò.
- Skill thứ hai, chọn theo lỗi lặp lại nhiều nhất trong `lessons/`.
- Thêm index tìm kiếm (basic-memory) khi grep không còn đủ.
