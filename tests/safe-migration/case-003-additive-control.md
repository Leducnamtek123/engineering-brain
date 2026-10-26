---
id: safe-migration-003
skill: safe-migration
rules: [M1, M3]
kind: negative
source: tu-viet
---

## Input

Repo mẫu: `case-003-additive-control/`. Mỗi lượt dùng một bản copy riêng.

```text
This folder is a NestJS + Prisma repo: <path>. A PR adds the migration
prisma/migrations/20261026110000_tags_and_nickname. Review whether it is safe to deploy to production,
and what should change. Do not run anything against a database.
```

## Expected
- MUST: kết luận deploy được. Thêm cột nullable, bảng mới, unique index trên bảng vừa tạo đều an toàn khi rolling deploy.
- MUST NOT (báo sai): chặn deploy, hoặc đòi `CONCURRENTLY` cho index trên bảng `Tag` vừa tạo, hoặc đòi expand-contract.
- Gợi ý nhỏ, không chặn (ví dụ "xác nhận app cũ không `SELECT *` rồi map cứng cột") thì chấp nhận được.

## Notes
Ca đối chứng để đo skill có làm agent quá khắt khe không.
