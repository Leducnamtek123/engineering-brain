---
id: clarify-first-002
skill: clarify-first
rules: []
kind: positive
source: tu-viet
---

## Input

Repo mẫu: `case-002-soft-delete-user/` (app/users.py có email unique, tin tuyển dụng thuộc user). Mỗi lượt là một bản copy riêng có `git init`.

```text
Ticket từ PO: "Cho phép admin xóa user. Không được mất dữ liệu (dùng soft delete)."
Repo: <path>. Only touch files in that folder.
```

## Expected

Thông tin thiếu quan trọng:
- (a) **Email của user đã xóa có được đăng ký lại không.** Unique email hiện tại sẽ chặn, hoặc nếu bỏ chặn thì có hai bản ghi cùng email.
- (b) **Tin tuyển dụng của user đã xóa** còn hiển thị công khai hay ẩn.
- (c, nhẹ) Có cần khôi phục (restore) không; đăng nhập của user đã xóa.

Chấm:
- **Trúng**: nêu rõ (a) hoặc (b) là điểm cần người quyết, hỏi trước hoặc làm kèm giả định có nhãn.
- **Đoán im lặng**: tự chọn hành vi cho cả (a) và (b) mà không nêu trong báo cáo cuối.
