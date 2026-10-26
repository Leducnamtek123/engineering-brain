# Deploy

- Production: 3 replica, `RollingUpdate`. Job `prisma migrate deploy` chạy trước khi rollout.
- Postgres 16. Bảng `User` khoảng 2 triệu dòng.
