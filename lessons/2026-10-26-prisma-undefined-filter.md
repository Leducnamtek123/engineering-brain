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
- [x] Luật mới A2 (2026-10-26, v0.1.1; câu chữ sửa ở v0.1.2 sau khi agent báo dư). Nguồn: Prisma docs "Null and undefined".
- [x] Sửa `Expected` của ca 002: ghi chú ở mức "chưa kiểm chứng" thì tính là trúng, báo thành lỗi thì tính là báo sai.
- [x] Ca mới `case-003-undefined-owner`.

## Bài học thêm từ vòng 2
Luật mới viết quá rộng làm agent báo dư ngay lập tức. Mỗi luật nên có ít nhất một ca negative hoặc một phần "MUST NOT flag" nằm sát ranh giới của luật.
