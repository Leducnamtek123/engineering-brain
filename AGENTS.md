# AGENTS.md

Lối vào cho mọi coding agent. Giữ file này ngắn: chi tiết nằm trong `knowledge/` và `skills/`, chỉ đọc khi task cần.

## Khi nhận task
- Tìm skill phù hợp trong `skills/`. Có thì làm theo; quy tắc nó trỏ tới nằm trong `knowledge/`.
- Chỉ áp dụng quy tắc có `status: reviewed` hoặc `verified`. Quy tắc `draft` chỉ để tham khảo, nếu dùng phải nói rõ.

## Khi xong task (bước compound)
Nếu task có lỗi đáng nhớ, một lần sửa sai, hoặc một cách làm hiệu quả: tạo một file trong `lessons/` theo `lessons/_TEMPLATE.md`. Không tự sửa file trong `knowledge/` để biến bài học thành quy tắc; việc đó cần người duyệt.

## Không được
- Không tự đổi `status` của quy tắc sang `verified`.
- Không tự xác nhận kết quả của chính mình: dùng test, eval hoặc người review.
- Không ghi secret, token, dữ liệu khách hàng vào repo này.
