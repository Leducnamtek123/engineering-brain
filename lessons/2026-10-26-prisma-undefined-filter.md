---
date: 2026-10-26
project: engineering-brain (chạy test backend-authz-review)
agent: claude-code subagent, sonnet
tags: [backend, authz, prisma]
---

## Chuyện gì xảy ra
Ở ca `case-002-safe`, `Expected` coi `findFirst({ where: { id, ownerId: req.user.id } })` là an toàn.
Cả hai lần baseline (không có skill) đều chỉ ra rằng Prisma bỏ qua điều kiện có giá trị `undefined`.
Vậy nếu `req.user.id` là `undefined` (strategy trả `sub` hoặc `userId`), truy vấn thành `where: { id }` và lộ hóa đơn của mọi người.
Hai lần chạy có skill không nhắc tới, vì skill chỉ dạy "lọc theo owner lấy từ token" mà không nói owner id có thể rỗng.

## Bài học
- Skill làm báo cáo hẹp lại, nên có thể đánh rơi phát hiện đúng nằm ngoài luật.
- `Expected` cũng có thể sai: người viết ca test không nghĩ tới bẫy này.

## Đề xuất nâng cấp (người duyệt quyết định mỗi tuần)
- [ ] Luật mới A2: id chủ sở hữu dùng để lọc phải được chứng minh khác rỗng (decorator có kiểu, hoặc chặn khi thiếu). Cần nguồn: tài liệu Prisma về `null` và `undefined`, đọc và ghi ngày kiểm trước khi viết.
- [ ] Sửa `Expected` của ca 002: chấp nhận cảnh báo này nếu được ghi ở mức "chưa kiểm chứng" hoặc Low.
- [ ] Ca eval mới: strategy trả `{ sub }`, controller dùng `req.user.id`.
