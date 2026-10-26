---
id: BE-AUTHZ-001
title: Endpoint trả dữ liệu theo id phải kiểm tra quyền sở hữu
domain: backend
requirement: must
status: draft
owner: chua-co
sources:
  - url: https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
    checked: 2026-10-26
  - url: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
    checked: 2026-10-26
evals:
  - evals/backend-authz-review/cases/case-001-idor.md
  - evals/backend-authz-review/cases/case-002-safe.md
---

## Scope
Endpoint đọc, sửa hoặc xóa một tài nguyên theo id lấy từ request (path, query, body), khi tài nguyên đó thuộc về một user hoặc tổ chức. Không áp dụng cho dữ liệu công khai.

## Rule
Lấy danh tính từ ngữ cảnh xác thực phía server, rồi kiểm tra tài nguyên thuộc quyền của danh tính đó trước khi trả hoặc sửa. Đã đăng nhập chưa đủ để coi là có quyền.

## Rationale
Thiếu bước này, user A đổi id trong URL là đọc hoặc sửa được dữ liệu của user B (IDOR). OWASP Top 10 (2021 và 2025) xếp Broken Access Control ở vị trí A01.

## Procedure
1. Tìm mọi chỗ đọc id từ request.
2. Kiểm tra truy vấn có ràng buộc theo chủ sở hữu không (ví dụ `where: { id, ownerId: currentUser.id }`), hoặc có bước kiểm tra quyền rõ ràng sau khi tải.
3. Kiểm tra id chủ sở hữu lấy từ token hoặc session, **không** lấy từ request.
4. Nếu thiếu: báo lỗi, nêu file:dòng, gợi ý cách sửa.

## Verification
Có test cho 3 trường hợp: chủ sở hữu truy cập được; user khác bị từ chối (403 hoặc 404); chưa đăng nhập bị 401.

## Exceptions
- Vai trò admin hoặc support có quyền rộng hơn: phải kiểm tra vai trò rõ ràng và có log truy cập.
- Tài nguyên chia sẻ theo nhóm: kiểm tra membership thay cho ownerId.
