# Deploy

- Production: 3 replica, `RollingUpdate`. Job `prisma migrate deploy` chạy trước khi rollout.
- Postgres 16.
- Bảng `Order` khoảng 40 triệu dòng, nhận đơn mới liên tục 24/7 (khoảng 200 insert/giây giờ cao điểm).
