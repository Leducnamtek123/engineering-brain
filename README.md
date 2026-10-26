# engineering-brain

Bộ skill kỹ thuật cho coding agent. Mỗi luật đều **có nguồn, có ngày kiểm tra và có test**.
Skill viết theo chuẩn mở Agent Skills (`SKILL.md`), nên dùng được với Claude Code, Codex,
Gemini CLI, Cursor, và vẫn còn nguyên khi đổi model.

## Skill hiện có

| Skill | Gọi bằng | Làm gì | Kết quả đo (chi tiết: `TESTS.md`) |
| --- | --- | --- | --- |
| `house-conventions` | `/brain:house-conventions` | Code mới theo quy ước đích của dự án, không chép code cũ bên cạnh; ratchet chỉ soát dòng mới | **Baseline đạt 2/8, có skill đạt 8/8** |
| `test-integrity` | `/brain:test-integrity` | Không sửa, skip, hardcode test để cho pass; test sai thì dừng và báo | Không ai gian lận ở ca rõ ràng (0/24); skill đổi mặc định sang theo spec |
| `safe-migration` | `/brain:safe-migration` | Migration Prisma/Postgres an toàn khi rolling deploy; script soát SQL | Baseline đã bắt được hết; giảm báo sai trên Haiku; script kiểm đúng 3/3 ca |
| `backend-authz-review` | `/brain:backend-authz-review` | Soát endpoint thiếu kiểm tra quyền sở hữu (IDOR) | Baseline đã bắt được hết; giảm báo sai trên Haiku |

Tất cả luật đang ở trạng thái `draft`: chưa có người chuyên môn duyệt.

Script dùng độc lập được (không cần agent), hợp để đưa vào pre-commit hoặc CI:
`skills/house-conventions/scripts/check_new_code.py`, `skills/safe-migration/scripts/check_migration.py`, `skills/test-integrity/scripts/check_test_diff.py`.

## Cài

Claude Code:

```bash
/plugin marketplace add Leducnamtek123/engineering-brain
/plugin install brain@engineering-brain
```

Agent khác: trỏ agent tới `skills/<tên>/SKILL.md`, hoặc copy thư mục skill vào chỗ agent đó đọc skill.

## Cách repo này lớn lên

1. Chọn một lỗi AI hay mắc trong dự án thật.
2. Viết ca test có đáp án (`tests/` ở repo lab), chạy **khi chưa có skill** để lấy mốc so sánh.
3. Viết luật có nguồn trong `skills/<tên>/references/`.
4. Chạy lại test **khi có skill**. Chỉ giữ luật nào làm kết quả tốt hơn.
5. Sau mỗi task thật, ghi bài học vào `lessons/` của repo lab. Mỗi tuần nâng bài học lặp lại thành luật hoặc test.

Chi tiết cho người sửa skill: `DEVELOP.md`. Kết quả: `TESTS.md`. Ca test, bài học, nghiên cứu: repo private [engineering-brain-lab](https://github.com/Leducnamtek123/engineering-brain-lab).
