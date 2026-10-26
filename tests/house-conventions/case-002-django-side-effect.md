---
id: house-conventions-002
skill: house-conventions
rules: [H1, H2, H3]
kind: positive
source: tu-viet
---

## Input

Repo mẫu: `case-002-django-side-effect/`. Mỗi lượt là một bản copy riêng có `git init`.

```text
This folder is part of a Django REST Framework backend: <path>. Add a `reopen` action to JobPostViewSet in
api/apps/jobs/views.py: it sets a closed job post back to open, clears closed_at and closed_by, records a
JobPostActivity with action "reopened", and notifies followers with the notify_followers task (event "reopened").
Only touch files in that folder.
```

## Expected
Chấm bằng máy: `check_new_code.py` với `examples/square.conventions.json`.
- MUST (trúng): 0 vi phạm trong dòng mới. Logic ghi nằm trong `services.py` (ví dụ `reopen_job_post`, theo mẫu `close_job_post`), có `transaction.atomic()`, `notify_followers.delay` chỉ trong `transaction.on_commit`, view chỉ gọi service.
- Trượt: chép action `boost` cũ (ghi `.save()` trong view, `.delay` gọi thẳng).
- Không bắt buộc: sửa `boost` cũ (ngoài phạm vi).

## Notes
Có sẵn cả mẫu tốt (`close` + `close_job_post`) lẫn mẫu xấu (`boost`) trong cùng file: đo agent chép theo cái nào.
