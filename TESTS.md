# Test

Cách chạy và chấm: `DEVELOP.md`, mục "Test".

**Chốt xong một luật thì ghi ngược vào skill**: sửa `references/`, thêm dòng vào bảng
"Mở khi" của `SKILL.md` nếu chưa có, rồi tick ca ở đây.

## backend-authz-review

| Ca | Loại | Luật | Đã chạy |
| --- | --- | --- | --- |
| `case-001-idor` — guard có, `getOne` thiếu `ownerId` | positive | A1 | ☐ |
| `case-002-safe` — truy vấn đã lọc `ownerId`, endpoint công khai | negative | A1 | ☐ |

### Kết quả

| Ngày | Agent | Model | Cấu hình | Lần | Trúng | Bỏ sót | Báo sai | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | baseline | 1 | | | | |
| | | | có skill | 1 | | | | |

Kết luận: chưa chạy.
