---
id: house-conventions-001
skill: house-conventions
rules: [H1, H2, H3]
kind: positive
source: tu-viet
---

## Input

Repo mẫu: `case-001-legacy-mui-page/` (cấu trúc monorepo Next.js phổ biến, code tự viết). Mỗi lượt là một bản copy riêng có `git init`.

```text
This folder is part of a Next.js frontend: <path>. In frontend/src/views/employerPages/JobPostsPage/JobListHeader.tsx,
add an "Xuất Excel" (export to Excel) button next to the existing create button. It calls a new optional prop `onExport`.
When a new prop `selectedCount` is greater than 0, show that number in a small badge inside the export button.
Only touch files in that folder.
```

## Expected
Chấm bằng máy: `check_new_code.py` với `examples/nextjs-shadcn-django.conventions.json` trên diff so với commit gốc.
- MUST (trúng): 0 vi phạm trong dòng mới. Tức là nút mới dùng `@/components/ui/button` (+ `badge`), không thêm import hay `sx` của MUI, không `any`, không `rounded-full`, chữ qua `t()`, không em dash.
- MUST: key mới có ở **cả** `locales/vi/employer.json` và `locales/en/employer.json`.
- Trượt: thêm `Button`/`Badge` của MUI hoặc `sx={...}` (chép code bên cạnh), hardcode "Xuất Excel" trong JSX.
- Không bắt buộc: chuyển phần MUI cũ sang Shadcn (ngoài phạm vi; làm thì không tính sai nhưng ghi nhận là mở rộng phạm vi).

## Notes
Đo đúng nỗi đau pattern replication: file đang sửa là MUI, AGENTS.md nói không dùng MUI cho code mới.
