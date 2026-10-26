# shop-infra

Hạ tầng AWS quản lý bằng Terraform trong `infra/`, mỗi môi trường là một workspace (`staging`, `prod`).

Luôn chạy Terraform qua `scripts/tf.sh <args>`: script tự nạp credentials của workspace đang chọn.
Workspace đang chọn được lưu ở `infra/.terraform/environment`.
