# Evals

Mỗi skill có một thư mục `evals/<skill>/`:

```
cases/       mỗi file một ca (mẫu: _CASE_TEMPLATE.md)
results.md   bảng so sánh baseline với có skill (mẫu: _RESULTS_TEMPLATE.md)
```

## Cách chạy (thủ công, đủ dùng lúc đầu)
1. **Baseline:** mở agent ở thư mục **không có** skill. Dán phần `Input` của từng ca, prompt giống nhau cho mọi lần chạy.
2. **Có skill:** chạy lại y hệt, nhưng ở repo có skill (hoặc gọi skill bằng tên).
3. Chấm theo `Expected` của từng ca: trúng (`hit`), bỏ sót (`miss`), báo sai (`false positive`).
4. Ghi vào `results.md` kèm model, agent, ngày chạy.
5. Mỗi cấu hình chạy ít nhất 2 lần, vì kết quả AI dao động.

Người chấm không nên là chính agent vừa làm bài. Dùng người, hoặc một agent/model khác chỉ được xem đầu ra và `Expected`.

## Khi nào nâng quy tắc lên `verified`
- Có skill tốt hơn baseline về hit, và không tăng false positive.
- Đã chạy trên ít nhất 2 codebase hoặc 2 ca khác loại.

Khi có trên khoảng 20 ca, chạy tay sẽ chậm. Lúc đó mới cân nhắc tự động hóa, ví dụ bằng chế độ eval của skill-creator hoặc một script gọi agent CLI.
