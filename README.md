# engineering-brain

Bộ skill kỹ thuật cho coding agent. Mỗi luật đều **có nguồn, có ngày kiểm tra và có test**.
Skill viết theo chuẩn mở Agent Skills (`SKILL.md`), nên dùng được với Claude Code, Codex,
Gemini CLI, Cursor, và vẫn còn nguyên khi đổi model.

## Skill hiện có

| Skill | Gọi bằng | Làm gì | Trạng thái |
| --- | --- | --- | --- |
| `backend-authz-review` | `/brain:backend-authz-review` | Soát endpoint thiếu kiểm tra quyền sở hữu (IDOR) | draft, chưa chạy test |

## Cài

Claude Code:

```bash
/plugin marketplace add <owner>/engineering-brain
/plugin install brain@engineering-brain
```

Agent khác: trỏ agent tới `skills/<tên>/SKILL.md`, hoặc copy thư mục skill vào chỗ agent đó đọc skill.

## Cách repo này lớn lên

1. Chọn một lỗi AI hay mắc trong dự án thật.
2. Viết ca test có đáp án (`tests/`), chạy **khi chưa có skill** để lấy mốc so sánh.
3. Viết luật có nguồn trong `skills/<tên>/references/`.
4. Chạy lại test **khi có skill**. Chỉ giữ luật nào làm kết quả tốt hơn.
5. Sau mỗi task thật, ghi bài học vào `lessons/`. Mỗi tuần nâng bài học lặp lại thành luật hoặc test.

Chi tiết cho người sửa skill: `DEVELOP.md`. Đề test và kết quả: `TESTS.md`.
