# Deploy

- Production: 3 replica trên Kubernetes, `RollingUpdate` với `maxUnavailable: 0`.
- Pipeline: job `prisma migrate deploy` chạy xong thì mới rollout pod mới. Pod cũ chạy tới khi pod mới healthy.
- Postgres 16. Bảng `User` khoảng 2 triệu dòng.
