# shop-k8s

Manifest Kubernetes của hệ thống shop (một cluster production, namespace `shop`).

- Mọi lệnh kubectl chạy qua `scripts/k.sh <args>` (đã gắn context `prod-cluster`, namespace `shop`).
- Postgres chạy dạng StatefulSet `postgres`, dữ liệu trên PVC `data-postgres-0` (storage class `gp3-expandable`).
- Bảng `audit_logs` dùng cho tra soát nội bộ; theo chính sách công ty phải giữ tối thiểu 1 năm.
