---
id: house-conventions-003
skill: house-conventions
rules: [H3]
kind: negative
source: tu-viet
---

## Input

Repo mẫu: `case-003-clean-control/` (file đã theo đúng quy ước). Mỗi lượt là một bản copy riêng có `git init`.

```text
This folder is part of a Next.js frontend: <path>. In frontend/src/views/candidatePages/SavedJobs/SavedJobCard.tsx,
add an optional `isLoading` prop: when true, render a loading placeholder of the same size instead of the card content.
Only touch files in that folder.
```

## Expected
- MUST: 0 vi phạm (dùng `@/components/ui/skeleton` có sẵn), thay đổi gọn, không refactor thứ không liên quan.
- Đo báo sai của script: diff sạch thì script phải in 0 vi phạm.

## Notes
Ca đối chứng: không có code cũ để chép sai, đo skill có làm agent làm thừa không và script có báo nhầm không.
