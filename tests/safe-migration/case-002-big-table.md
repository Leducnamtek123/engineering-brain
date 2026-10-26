---
id: safe-migration-002
skill: safe-migration
rules: [M2, M3]
kind: positive
source: tu-viet
---

## Input

Repo mẫu: `case-002-big-table/`. Mỗi lượt dùng một bản copy riêng.

```text
This folder is a NestJS + Prisma repo: <path>. A PR adds the migration
prisma/migrations/20261026100000_order_channel_and_customer_index. Review whether it is safe to deploy to production,
and what should change. Do not run anything against a database.
```

## Expected
- MUST (trúng): `CREATE INDEX` trên `Order` (40 triệu dòng, ghi 24/7) không có `CONCURRENTLY` sẽ **khoá ghi** tới khi build xong. Đề xuất `CREATE INDEX CONCURRENTLY` để riêng một migration, ngoài transaction.
- MUST NOT (báo sai): nói `ADD COLUMN "channel" TEXT NOT NULL DEFAULT 'web'` sẽ ghi lại hay khoá lâu bảng. Postgres 16 với default hằng số chỉ lưu vào metadata. Nêu nhẹ kiểu "xác nhận version Postgres" thì chấp nhận được; kết luận nó nguy hiểm thì tính là báo sai.

## Notes
Đo cả trúng (index) lẫn báo sai (fast default) trong cùng một ca.
