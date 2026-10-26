---
name: house-conventions
description: Giữ code mới đúng quy ước đích của dự án khi codebase còn code cũ lệch quy ước (đang chuyển MUI sang Shadcn, còn any, còn chuỗi hardcode...). Tìm building block có sẵn trước khi viết mới, viết theo quy ước chứ không chép code bên cạnh, rồi chạy ratchet chỉ soát dòng mới. Dùng khi thêm hoặc sửa tính năng trong dự án có AGENTS.md/coding standards, hoặc nhắc "theo quy ước dự án", "đừng dùng MUI", "check convention", "ratchet".
---

# Quy ước dự án: code mới theo đích, không theo hàng xóm

> **Code xung quanh không phải là quy ước.** Trong codebase đang chuyển đổi, file bên cạnh thường là
> code cũ cần bỏ. Viết theo tài liệu quy ước, rồi để **máy** kiểm dòng mới; đừng tin trí nhớ.

## Các bước

1. Đọc tài liệu quy ước của dự án (`AGENTS.md` gốc và của thư mục con, `docs/*standards*`). Tìm file cấu hình ratchet của dự án (`conventions.json`; dự án Square dùng `examples/square.conventions.json` trong skill này).
2. **Trước khi viết component, helper, service mới**: chạy `python <thư mục skill>/scripts/check_new_code.py --config <cấu hình> --blocks` và tìm trong các thư mục đó thứ đã có (luật `H2`).
3. Viết code theo quy ước đích (luật `H1`), kể cả khi sửa ngay trong file cũ còn lệch quy ước. Không tự refactor phần code cũ không liên quan.
4. Chạy `python <thư mục skill>/scripts/check_new_code.py --config <cấu hình> --repo <repo> --base <ref>` (luật `H3`). Sửa hết vi phạm trong dòng mới, hoặc giải thích từng cái còn lại.
5. Báo theo mẫu dưới.

## Mở khi

| Gặp | Mở |
| --- | --- |
| File đang sửa dùng pattern khác quy ước (MUI, any, chuỗi hardcode...) | `references/rules-conventions.md` mục `H1` |
| Sắp viết component, helper, hook, service mới | `references/rules-conventions.md` mục `H2` |
| Trước khi báo xong | `references/rules-conventions.md` mục `H3` |

## Mẫu báo

- Đã dùng building block có sẵn: <danh sách, hoặc "không có cái phù hợp, đã tìm ở ...">
- Ratchet: <0 vi phạm / N vi phạm còn lại kèm lý do từng cái>
- Code cũ lệch quy ước thấy được nhưng **không sửa** vì ngoài phạm vi: <file, nếu có>
