---
id: <skill>-000
skill: <skill-name>
rules: [RULE-ID]
kind: positive        # positive: có lỗi cần bắt | negative: code đúng, không được báo lỗi
source: tu-viet       # tu-viet | du-an-that (đã xóa dữ liệu nhạy cảm) | cong-khai (ghi link)
---

## Input
Prompt gửi cho agent, giống hệt nhau giữa baseline và có skill.

```text
Review this code for access-control issues: ...
```

## Expected
- MUST find: <lỗi cụ thể, vị trí>
- MUST NOT flag: <thứ trông giống lỗi nhưng không phải>

## Notes
Vì sao ca này khó, hoặc lấy từ sự cố nào.
