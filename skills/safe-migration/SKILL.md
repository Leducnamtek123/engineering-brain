---
name: safe-migration
description: Viết và soát migration database (Prisma, Postgres) để deploy không làm mất dữ liệu hay làm sập app đang chạy - expand-contract khi đổi tên/xoá/đổi kiểu, NOT NULL cần backfill, index phải CONCURRENTLY, cấm lệnh phá dữ liệu trên DB thật. Dùng khi tạo hoặc review migration, sửa schema.prisma, hoặc nhắc "migration này an toàn không", "deploy schema", "đổi tên cột", "thêm index", "safe migration".
---

# Migration an toàn

> **Migration chạy trên dữ liệu thật, cùng lúc với bản app cũ còn đang chạy.** Mọi thay đổi phải
> đúng với **cả bản app cũ lẫn bản mới** trong lúc deploy. Không chắc thì chia nhiều bước.

## Các bước

1. Đọc cách deploy của dự án (`docs/`, `README`, CI): có rolling update hay nhiều replica không, migration chạy lúc nào. **Không có thông tin thì giả định rolling update** (bản cũ và bản mới chạy song song).
2. Đọc SQL migration thật (`prisma/migrations/*/migration.sql`), không chỉ `schema.prisma`. Prisma có thể sinh `DROP` + `ADD` khi bạn chỉ định đổi tên.
3. Chạy `python <thư mục skill>/scripts/check_migration.py <file hoặc thư mục>`. Với mỗi cảnh báo, mở luật tương ứng:

| Gặp | Luật |
| --- | --- |
| `RENAME`, `DROP COLUMN/TABLE`, đổi kiểu cột | `M1` |
| `ADD COLUMN ... NOT NULL` không có default, `SET NOT NULL` | `M2` |
| `CREATE INDEX` trên bảng đã có dữ liệu | `M3` |
| Định chạy `migrate reset`, `db push --accept-data-loss`, `migrate dev`, SQL tay trên DB không phải local | `M4` |

4. Báo theo mẫu dưới. Không tự chạy migration lên DB dùng chung.

## Không báo nhầm

- `ADD COLUMN` cho phép NULL, hoặc có `DEFAULT` là hằng số (Postgres 11 trở lên): nhanh, không ghi lại bảng.
- `CREATE INDEX` trên bảng vừa `CREATE TABLE` trong cùng migration: chưa có dữ liệu, không cần `CONCURRENTLY`.
- `CREATE TABLE` mới, thêm bảng hay cột mà code cũ không dùng tới: an toàn.

## Mẫu báo

| Mức | file:dòng | Luật | Vấn đề khi deploy | Cách sửa (các bước) |
| --- | --- | --- | --- | --- |

Cuối báo cáo: kết luận **Deploy được / Phải chia bước / Chặn**, và những gì chưa kiểm chứng (kích thước bảng, cách deploy).
