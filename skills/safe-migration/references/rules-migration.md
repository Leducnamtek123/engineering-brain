# Migration an toàn — luật M

Nguồn duy nhất cho thay đổi schema khi deploy. Mẫu viết luật: `DEVELOP.md`.

---

## M1. Đổi tên, xoá, đổi kiểu: chia expand rồi contract

- Mức: must · Trạng thái: draft
- Test: `lab:tests/safe-migration/case-001-rename-rolling.md`, `lab:tests/safe-migration/case-003-additive-control.md`
- Nguồn: [Prisma docs: Expand-and-contract migrations](https://www.prisma.io/docs/guides/database/data-migration) (kiểm 2026-10-26); [Squawk rules: renaming-column, ban-drop-column](https://squawkhq.com/docs/rules) (kiểm 2026-10-26)

**Luật.** Không đổi tên, xoá, hay đổi kiểu cột/bảng mà code đang chạy còn dùng trong **một** lần deploy. Chia thành:
1. **Expand**: thêm cột hoặc bảng mới, code ghi vào cả hai (hoặc backfill), deploy.
2. Chuyển code sang đọc cái mới, deploy.
3. **Contract**: khi không còn gì đọc hay ghi cái cũ thì mới xoá, deploy riêng.

*Vì sao:* khi rolling update, bản app cũ vẫn chạy sau khi migration đã chạy. `RENAME COLUMN` làm mọi query của bản cũ
lỗi ngay, dù không mất dữ liệu. `DROP` thì mất dữ liệu luôn. Prisma docs: deploy bước expand rồi *"đợi tới khi không còn gì đọc hoặc ghi"* cột cũ mới contract.

**Cách làm.** Thấy `RENAME`, `DROP`, `ALTER ... TYPE`: tìm code còn dùng tên cũ, đề xuất các bước cụ thể (SQL từng bước, code đổi ở bước nào).

**Kiểm chứng.** Mỗi migration để riêng thì bản app ngay trước nó vẫn chạy đúng.

**Ngoại lệ.** App chỉ có một instance và chấp nhận downtime đã báo trước, hoặc bảng và cột chưa từng được code dùng: ghi rõ lý do.

---

## M2. NOT NULL cần default hoặc backfill trước

- Mức: must · Trạng thái: draft
- Test: `lab:tests/safe-migration/case-002-big-table.md`
- Nguồn: [PostgreSQL docs: ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) (kiểm 2026-10-26); [Squawk rules: adding-required-field, adding-not-nullable-field](https://squawkhq.com/docs/rules) (kiểm 2026-10-26)

**Luật.** `ADD COLUMN ... NOT NULL` phải có `DEFAULT`. `SET NOT NULL` trên cột cũ chỉ chạy sau khi đã backfill hết NULL,
và trên bảng lớn thì thêm `CHECK (... IS NOT NULL) NOT VALID`, `VALIDATE` rồi mới `SET NOT NULL`.

*Vì sao:* Postgres docs: `SET NOT NULL` chỉ áp dụng được khi không còn dòng nào NULL, và sẽ quét toàn bảng. Thêm cột NOT NULL
không default thì lỗi ngay khi bảng có dữ liệu. Ngược lại, thêm cột có `DEFAULT` là hằng số thì Postgres chỉ lưu vào metadata, **rất nhanh, không ghi lại bảng**.

**Cách làm.** Đừng báo nhầm `ADD COLUMN ... DEFAULT <hằng số>` là chậm. Chỉ cảnh báo khi default là hàm volatile (`clock_timestamp()`, `random()`), hoặc không có default.

**Kiểm chứng.** Chạy migration trên bản copy có dữ liệu thật (hoặc seed có NULL), không lỗi.

**Ngoại lệ.** Bảng chắc chắn rỗng ở mọi môi trường.

---

## M3. Index trên bảng đã có dữ liệu dùng CONCURRENTLY

- Mức: must · Trạng thái: draft
- Test: `lab:tests/safe-migration/case-002-big-table.md`, `lab:tests/safe-migration/case-003-additive-control.md`
- Nguồn: [PostgreSQL docs: CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html) (kiểm 2026-10-26); [Squawk rules: require-concurrent-index-creation](https://squawkhq.com/docs/rules) (kiểm 2026-10-26)

**Luật.** `CREATE INDEX` trên bảng đã có dữ liệu phải dùng `CREATE INDEX CONCURRENTLY`, để riêng một migration và không nằm trong transaction.

*Vì sao:* Postgres docs: build index thường *"locks out writes"* tới khi xong. Bảng lớn thì app không ghi được trong nhiều phút.

**Cách làm.** Tách câu tạo index ra migration riêng, dùng `CONCURRENTLY`, kiểm tra index không bị `INVALID` sau khi chạy. Với Prisma, xem migration đó có bị bọc transaction không trước khi dùng `CONCURRENTLY`.

**Kiểm chứng.** Sau deploy, index ở trạng thái valid (`pg_index.indisvalid`).

**Ngoại lệ.** Bảng vừa tạo trong cùng migration, hoặc bảng rất nhỏ và chấp nhận khoá ngắn.

---

## M4. Không chạy lệnh phá dữ liệu trên DB không phải local

- Mức: must · Trạng thái: draft
- Test: `lab:tests/safe-migration/case-001-rename-rolling.md`
- Nguồn: [OECD AI Incident: Replit agent deletes production database](https://oecd.ai/en/incidents/2025-07-19-1eb1) (kiểm 2026-10-26)

**Luật.** Agent không tự chạy `prisma migrate reset`, `prisma db push --accept-data-loss`, `prisma migrate dev`, hay SQL
`DROP`/`TRUNCATE`/`DELETE` không có `WHERE` trên database không phải local. Chỉ đề xuất lệnh; người duyệt chạy.

*Vì sao:* sự cố Replit 2025: agent xoá database production dù đã được dặn đóng băng thay đổi. Môi trường dev và prod dùng chung DB.

**Cách làm.** Trước mọi lệnh DB, xác định `DATABASE_URL` trỏ đi đâu. Không phải localhost thì dừng và hỏi.

**Kiểm chứng.** Lịch sử lệnh của agent không có các lệnh trên nhắm vào DB dùng chung.

**Ngoại lệ.** Không có.
