# Phân quyền backend — luật A

Nguồn duy nhất cho kiểm tra quyền trên endpoint. Mỗi luật có mã cố định, không đổi mã khi sửa nội dung.
Mẫu viết một luật: `DEVELOP.md`, mục "Mẫu một luật".

---

## A1. Endpoint trả dữ liệu theo id phải kiểm tra quyền sở hữu

- Mức: must · Trạng thái: draft
- Test: `tests/backend-authz-review/case-001-idor.md`, `tests/backend-authz-review/case-002-safe.md`
- Nguồn: [OWASP Top 10 A01:2025](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) (kiểm 2026-10-26); [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) (kiểm 2026-10-26)

**Luật.** Lấy danh tính từ ngữ cảnh xác thực phía server, rồi kiểm tra tài nguyên thuộc quyền
của danh tính đó trước khi trả hoặc sửa. Đã đăng nhập chưa đủ để coi là có quyền.

*Vì sao:* thiếu bước này, user A đổi id trong URL là đọc hoặc sửa được dữ liệu của user B (IDOR).
OWASP Top 10 (2021 và 2025) xếp Broken Access Control ở vị trí A01.

**Cách làm.**
1. Tìm mọi chỗ đọc id từ request.
2. Xem truy vấn có ràng buộc theo chủ sở hữu không (ví dụ `where: { id, ownerId: currentUser.id }`),
   hoặc có bước kiểm tra quyền rõ ràng sau khi tải.
3. Id chủ sở hữu phải lấy từ token hoặc session, **không** lấy từ request.
4. Thiếu thì báo, kèm `file:dòng` và cách sửa.

**Kiểm chứng.** Có test cho 3 trường hợp: chủ sở hữu truy cập được; user khác bị từ chối (403 hoặc 404);
chưa đăng nhập bị 401.

**Ngoại lệ.**
- Vai trò admin hoặc support có quyền rộng hơn: kiểm tra vai trò rõ ràng và có log truy cập.
- Tài nguyên chia sẻ theo nhóm: kiểm tra membership thay cho `ownerId`.

---

## A2. Id chủ sở hữu dùng để lọc phải chắc chắn có giá trị

- Mức: must · Trạng thái: draft
- Test: `tests/backend-authz-review/case-002-safe.md`, `tests/backend-authz-review/case-003-undefined-owner.md`
- Nguồn: [Prisma docs — Null and undefined](https://www.prisma.io/docs/orm/v7/prisma-client/special-fields-and-types/null-and-undefined) (kiểm 2026-10-26); [OWASP Top 10 A01:2025](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) (kiểm 2026-10-26)

**Luật.** Giá trị chủ sở hữu đưa vào điều kiện lọc (`ownerId`, `userId`, `orgId`) phải được chứng minh
khác `undefined` trước khi truy vấn. Lọc đúng tên cột chưa đủ.

*Vì sao:* với Prisma, `undefined` nghĩa là "bỏ qua trường này": `where: { id, ownerId: undefined }` chạy
thành `where: { id }` và trả bản ghi của bất kỳ ai. Chỉ cần strategy JWT trả `sub` thay vì `id`, hoặc
ai đó đổi tên field, là điều kiện phân quyền biến mất mà không có lỗi nào. Prisma khuyên bật preview
feature `strictUndefinedChecks` để `undefined` gây lỗi thay vì bị bỏ qua.

**Cách làm.**
1. Với mỗi điều kiện lọc theo chủ sở hữu ở A1, tìm nơi giá trị đó được tạo ra (ví dụ `validate()` của strategy, decorator lấy user).
2. **Báo lỗi** khi code cho thấy giá trị có thể là `undefined`: tên field không khớp (strategy trả `sub`, controller đọc `.id`), dùng `?.`, hoặc field tùy chọn.
3. **Không báo** khi tên field khớp với thứ strategy trả ra từ payload của token đã xác minh (strategy trả `sub`, controller đọc `.sub`). Token do server ký nên coi như field đó có mặt. Muốn gợi ý thêm kiểm tra trong `validate()` thì ghi một dòng ở "ngoài phạm vi", không đưa vào bảng lỗi.
4. **Không thấy** nơi tạo giá trị: ghi vào "chưa kiểm chứng", **không** báo lỗi.
5. Cách sửa gợi ý: decorator có kiểu và ném `UnauthorizedException` khi thiếu id; hoặc bật `strictUndefinedChecks`.

**Kiểm chứng.** Có test: user có token nhưng thiếu field id thì bị từ chối (401), không nhận được dữ liệu.

**Ngoại lệ.** ORM hay query builder không bỏ qua `undefined` (ví dụ SQL tham số hoá thuần, hoặc đã bật
`strictUndefinedChecks`) thì chỉ cần ghi chú, không báo lỗi.
