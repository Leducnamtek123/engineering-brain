# Test

Cách chạy và chấm: `DEVELOP.md`, mục "Test".

**Chốt xong một luật thì ghi ngược vào skill**: sửa `references/`, thêm dòng vào bảng
"Mở khi" của `SKILL.md` nếu chưa có, rồi tick ca ở đây.

## backend-authz-review

| Ca | Loại | Luật | Đã chạy |
| --- | --- | --- | --- |
| `case-001-idor` — guard có, `getOne` thiếu `ownerId` | positive | A1 | ✅ 2026-10-26 |
| `case-002-safe` — truy vấn đã lọc `ownerId`, endpoint công khai | negative | A1, A2 | ✅ 2026-10-26 |
| `case-003-undefined-owner` — strategy trả `sub`, `getOne` đọc `.id`, `list` đọc `.sub` | positive | A1, A2 | ✅ 2026-10-26 |

### Vòng 2 — 2026-10-26, skill v0.1.1 → v0.1.2 (thêm A2)

Cách chạy và người chấm giống vòng 1. Baseline ca 001 và 002 dùng lại kết quả vòng 1, vì prompt không đổi và baseline không phụ thuộc skill.

"Ghi chú A2" nghĩa là agent có nêu bẫy `undefined` ở mức "chưa kiểm chứng" hoặc ghi chú, không báo thành lỗi. Đây là hành vi mong muốn ở ca 002.

| Ca | Cấu hình | Lần | Trúng | Báo sai | Ghi chú A2 | Ngoài phạm vi | Token |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | có skill v0.1.1 | 1 | 1 | 0 | có (`list`) | 0 | ~68k |
| 001 | có skill v0.1.1 | 2 | 1 | 0 | có (`list`) | 0 | ~68k |
| 002 | có skill v0.1.1 | 1 | — | 0 | có | 0 | ~68k |
| 002 | có skill v0.1.1 | 2 | — | 0 | có | 2 (ghi riêng) | ~68k |
| 003 | baseline | 1 | 1 | 1 (High "chốt chặn" cho cả `list`) | — | 5 | ~62k |
| 003 | baseline | 2 | 1 | 0 | — | 5 | ~62k |
| 003 | có skill v0.1.1 | 1 | 1 | 1 (`list` Low) | — | 0 | ~68k |
| 003 | có skill v0.1.1 | 2 | 1 | 1 (`list` Medium) | — | 1 | ~69k |
| 003 | có skill **v0.1.2** | 1 | 1 | 0 | — | 1 dòng | ~69k |
| 003 | có skill **v0.1.2** | 2 | 1 | 0 | — | 1 dòng | ~68k |

**Đọc kết quả.**
- Ca 003 (khó hơn): baseline cũng bắt được lỗi chính 2/2. Như vậy với Sonnet, A2 **chưa làm tăng tỷ lệ bắt lỗi**.
- Ở ca 002, skill v0.1.1 bắt được bẫy `undefined` ở đúng mức: chỉ ghi chú, không báo thành lỗi. Trước khi có A2, hai lượt có skill ở ca này không nhắc tới bẫy.
- A2 bản v0.1.1 viết quá rộng nên agent báo dư `list` (2/2). Bản v0.1.2 thêm bước "tên field khớp với strategy thì không báo" và hết báo sai (0/2).
- Lưu ý: ca 001 và 002 chưa chạy lại với v0.1.2. Thay đổi chỉ thu hẹp phạm vi báo, nên dự đoán không tệ hơn, nhưng **chưa kiểm chứng**.
- Token: có skill tốn thêm khoảng 10% so với baseline.

### Vòng 1 — 2026-10-26, skill v0.1.0 (chỉ A1)

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
