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
