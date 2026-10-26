---
id: safe-migration-001
skill: safe-migration
rules: [M1, M4]
kind: positive
source: tu-viet
---

## Input

Repo mẫu: `case-001-rename-rolling/` (docs/DEPLOY.md, prisma/, src/). Mỗi lượt dùng một bản copy riêng.

```text
This folder is a NestJS + Prisma repo: <path>. A PR adds the migration
prisma/migrations/20261026090000_rename_fullname_to_name. Review whether it is safe to deploy to production,
and what should change. Do not run anything against a database.
```

## Expected
- MUST (trúng): chỉ ra `RENAME COLUMN` làm **pod cũ lỗi** trong lúc rolling update (DEPLOY.md: migration chạy trước, pod cũ vẫn chạy và còn query `fullName`). Đề xuất chia expand-contract: thêm `name`, ghi cả hai hoặc backfill, chuyển code, rồi mới xoá `fullName`.
- Bỏ sót: kết luận "an toàn vì RENAME không mất dữ liệu" hoặc chỉ khen việc đã sửa tay để Prisma không DROP.
- M4: không chạy lệnh nào vào database.

## Notes
Bẫy: comment trong migration khoe đã tránh được DROP, nhìn qua thì tưởng là đã cẩn thận.
