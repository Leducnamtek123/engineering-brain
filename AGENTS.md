# AGENTS.md

Lối vào cho mọi coding agent. Giữ file này ngắn: chi tiết nằm trong `skills/`, chỉ đọc khi task cần.

## Khi nhận task
- Tìm skill phù hợp trong `skills/*/SKILL.md`. Có thì làm theo bảng "Mở khi" của nó.
- Khi sửa skill của repo này: bài học thô, ca test và nghiên cứu nằm ở repo private [engineering-brain-lab](https://github.com/Leducnamtek123/engineering-brain-lab) (`lessons/`, `tests/`, `docs/`). Bài học là ghi chép thô chưa duyệt: dùng để cảnh giác, không coi là luật.
- Luật `draft` vẫn dùng được nhưng phải ghi rõ "(luật draft)".

## Khi xong task (bước compound)
Nếu task có lỗi đáng nhớ, một lần sửa sai, hay một cách làm hiệu quả: tạo một file trong
`lessons/` của repo lab theo `lessons/_TEMPLATE.md`. Không tự biến bài học thành luật; việc đó cần người duyệt.

## Khi sửa repo này
- Theo `DEVELOP.md`. Chạy `python scripts/lint.py --lab ../engineering-brain-lab` trước khi commit.
- Không tự đổi trạng thái luật sang `verified`, không sửa `locked-rules.md` khi chưa được hỏi.
- Không ghi secret, token, dữ liệu khách hàng vào repo.
