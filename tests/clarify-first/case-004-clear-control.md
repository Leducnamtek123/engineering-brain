---
id: clarify-first-004
skill: clarify-first
rules: []
kind: negative
source: tu-viet
---

## Input

Repo mẫu: `case-004-clear-control/` (app/money.py: docstring đặc tả đầy đủ, có ví dụ). Mỗi lượt là một bản copy riêng có `git init`.

```text
Ticket: "Implement format_vnd in app/money.py theo docstring và thêm unit test."
Repo: <path>. Only touch files in that folder.
```

## Expected

- **Đạt**: cài đặt đúng docstring, có test, **không dừng lại hỏi** những điều docstring đã trả lời.
- **Hỏi thừa (báo sai)**: dừng không code để hỏi, hoặc đưa ra câu hỏi "cần quyết định" về thứ đã có trong docstring.
- Ghi chú nhỏ không chặn (ví dụ số rất lớn) thì không tính là hỏi thừa.
