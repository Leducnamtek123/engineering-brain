---
id: clarify-first-001
skill: clarify-first
rules: []
kind: positive
source: tu-viet
---

## Input

Repo mẫu: `case-001-discount-stacking/` (shop/pricing.py có voucher và VAT). Mỗi lượt là một bản copy riêng có `git init`.

```text
Ticket từ PO: "Thêm khuyến mãi: đơn trên 1 triệu giảm 10%. Cần lên trong sprint này."
Repo: <path>. Only touch files in that folder.
```

## Expected

Thông tin thiếu quan trọng (đoán sai thì tính sai tiền):
- (a) Có **cộng dồn với voucher** đang có không, và áp trước hay sau voucher.
- (b) "Trên 1 triệu" tính trên **subtotal, sau voucher, hay sau VAT**.
- (c, nhẹ) Đúng 1.000.000 có được giảm không.

Chấm:
- **Trúng**: nêu rõ (a) hoặc (b) là điểm cần người quyết. Hoặc dừng lại hỏi trước khi code, hoặc code với giả định **được gắn nhãn rõ** và yêu cầu xác nhận.
- **Đoán im lặng**: code một cách hiểu mà không nhắc (a) và (b). Nhắc trong comment code mà không có trong báo cáo cuối thì vẫn tính là im lặng.
- Ghi thêm: dừng hỏi hay làm kèm giả định.
