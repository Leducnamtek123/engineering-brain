# Test

Cách chạy và chấm: `DEVELOP.md`, mục "Test".

**Chốt xong một luật thì ghi ngược vào skill**: sửa `references/`, thêm dòng vào bảng
"Mở khi" của `SKILL.md` nếu chưa có, rồi tick ca ở đây.

## backend-authz-review

| Ca | Loại | Luật | Đã chạy |
| --- | --- | --- | --- |
| `case-001-idor` — guard có, `getOne` thiếu `ownerId` | positive | A1 | ✅ 2026-10-26 |
| `case-002-safe` — truy vấn đã lọc `ownerId`, endpoint công khai | negative | A1 | ✅ 2026-10-26 |

### Kết quả 2026-10-26

Cách chạy: subagent Claude Code, model `sonnet`, mỗi lượt là một phiên mới.
- Baseline: chỉ có prompt, không được đọc file nào.
- Có skill: đọc đúng một file gồm `SKILL.md` và `references/`, không thấy `Expected`.

Người chấm là phiên chính (model `opus`), khác model với người làm bài. Lưu ý: chính người chấm đã viết `Expected`.

Cột "Ngoài phạm vi" đếm số mục không thuộc phân quyền, như phân trang, DTO, kiểu của `req`, `ParseUUIDPipe`. Các mục này không tính là báo sai nhưng làm báo cáo loãng.

| Ca | Cấu hình | Lần | Trúng | Bỏ sót | Báo sai | Ngoài phạm vi | Kết luận agent đưa ra | Token |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | baseline | 1 | 1 | 0 | 1 (thiếu RBAC, cả `list`) | 3 | Sửa trước khi merge | ~61k |
| 001 | baseline | 2 | 1 | 0 | 1 (thiếu RBAC) | 4 | Sửa trước khi merge | ~61k |
| 001 | có skill | 1 | 1 | 0 | 0 | 0 | 1 lỗi High | ~67k |
| 001 | có skill | 2 | 1 | 0 | 0 | 0 | 1 lỗi High | ~67k |
| 002 | baseline | 1 | — | — | 1 (`getOne`, Medium) | 3 | **Sửa trước khi merge** cho code đúng | ~62k |
| 002 | baseline | 2 | — | — | 2 (`getOne` High, mô hình quyền) | 3 | **Sửa trước khi merge** cho code đúng | ~62k |
| 002 | có skill | 1 | — | — | 0 | 2 (ghi riêng) | 0 lỗi | ~67k |
| 002 | có skill | 2 | — | — | 0 | 1 (ghi riêng) | 0 lỗi | ~67k |

Tổng:
- Baseline: trúng 2/2, báo sai 5, ngoài phạm vi 13.
- Có skill: trúng 2/2, báo sai 0, ngoài phạm vi 3, các mục này đều được ghi riêng.
- Có skill tốn thêm khoảng 9% token.

**Kết luận.**
- Cả hai cấu hình đều bắt được IDOR ở ca dễ, nên skill **không làm tăng tỷ lệ bắt lỗi** ở mức độ khó này.
- Skill **cắt hết báo sai**. Không có skill, agent kết luận "Sửa trước khi merge" cho code đúng ở cả 2 lần chạy ca 002.
- Skill giữ báo cáo gọn và đúng phạm vi.

**Phát hiện ngược.** Ở ca 002, cả hai lần baseline đều nêu một rủi ro có thật mà `Expected` không tính tới: Prisma bỏ qua điều kiện có giá trị `undefined` trong `where`. Nếu `req.user.id` là `undefined`, chẳng hạn khi strategy trả `sub` thay vì `id`, thì bộ lọc `ownerId` mất tác dụng. Hai lần chạy có skill không nêu rủi ro này. Như vậy skill làm báo cáo hẹp lại và có thể làm mất phát hiện đúng ở ngoài luật. Đã ghi vào `lessons/2026-10-26-prisma-undefined-filter.md`.

**Quyết định.** A1 giữ `draft`, chưa đủ điều kiện `verified`:
- Mới chạy trên 1 codebase giả lập, 2 ca.
- Chưa có người chuyên môn duyệt.
- Cần thêm ca khó hơn: lỗi nằm ở service chứ không ở controller, id lồng nhau, update hay delete.
