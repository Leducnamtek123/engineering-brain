---
date: 2026-10-26
project: engineering-brain (đo 4 skill, khoảng 140 lượt)
agent: claude-code subagent, sonnet + haiku
tags: [meta, eval, skill-design]
---

## Chuyện gì xảy ra
- backend-authz-review, test-integrity, safe-migration: baseline đã làm đúng gần hết. Skill chỉ giảm báo sai trên Haiku và giữ khuôn báo cáo.
- house-conventions: baseline đạt 2/8, có skill đạt 8/8. Baseline đọc AGENTS.md cấm MUI mà vẫn chép MUI từ file bên cạnh.

## Bài học
Skill có giá trị lớn khi thỏa **cả ba**:
1. Kiến thức **riêng của dự án**, model không thể có sẵn. Kiến thức phổ biến như OWASP hay Postgres thì model đã thuộc.
2. Có **code cũ ngược quy ước** trong tầm nhìn của agent. Đây là chỗ luật bằng chữ thua.
3. Có **máy kiểm** (ratchet chỉ soát dòng mới) để agent tự sửa trước khi báo xong.

Thiếu cả ba thì skill chủ yếu chỉ giúp model nhỏ đỡ báo sai.

## Đề xuất nâng cấp (người duyệt quyết định mỗi tuần)
- [ ] Đưa `check_new_code.py` + `square.conventions.json` vào pre-commit hoặc CI của square-tuyen-dung (`--base origin/main`). Cần người của dự án đồng ý.
- [ ] Skill tiếp theo chọn theo 3 tiêu chí trên, không theo chủ đề nghe quan trọng.
