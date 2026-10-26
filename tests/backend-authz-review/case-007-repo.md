---
id: backend-authz-review-007
skill: backend-authz-review
rules: [A1]
kind: positive
source: tu-viet
---

## Input

Repo mẫu: thư mục `case-007-repo/` (11 file). Khi chạy, **copy riêng thư mục `src/`** sang chỗ khác để agent không đọc được file này.

```text
This folder is a small NestJS repo: <path>/src. A PR just added `GET /invoices/:id/pdf`
(see the "Added in this PR" comments). Review the repo for access-control issues.
Start reading at src/invoices/invoices.controller.ts. You may read any file under <path>; do not read anything outside it.
```

## Expected
- MUST find (hit): `GET /invoices/:id/pdf` không chặn được org khác. `InvoicesRepository.findForPdf` `select` không có `orgId`, và `OrgAccessService.assertSameOrg` chỉ so khi `resource.orgId` truthy (`if (resource.orgId && ...)`). Vì vậy `orgId` là `undefined`, bước kiểm tra bị bỏ qua, và user org A tải được PDF hóa đơn org B. Cần nêu được **cả hai** nửa, hoặc ít nhất kết luận rõ endpoint PDF bị bypass vì thiếu `orgId`.
- Partial: chỉ chê điều kiện `resource.orgId &&` là "rủi ro" mà không nối với `findForPdf`, hoặc không kết luận endpoint PDF bị lộ.
- MUST NOT flag `GET /invoices/:id` là IDOR: `findById` tải đủ field nên có `orgId`, kiểm tra chạy đúng. (Chỉ ra helper "dễ vỡ" thì chấp nhận được, miễn không kết luận endpoint này đang lộ.)
- MUST NOT flag `list`: lọc theo `user.orgId` lấy từ token.
- Không tính báo sai: admin đọc chéo org (đã có comment nói là chủ ý); `JWT_SECRET` có thể undefined; thiếu test.

## Notes
- Code nhiễu: `money.ts`, `pdf.service.ts`, `app.module.ts`, `prisma.service.ts`, `invoices.module.ts`.
- Lỗi xuyên 3 file: controller (trông đúng) → service (gọi helper, trông đúng) → repository (thiếu `orgId`) + helper (bỏ qua khi thiếu).
- Đọc controller với service sẽ thấy cả hai endpoint đều gọi `assertSameOrg`, rất dễ kết luận "đã kiểm tra quyền".
