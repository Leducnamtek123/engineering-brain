---
name: backend-authz-review
description: Soát phân quyền backend - endpoint thiếu kiểm tra quyền sở hữu (IDOR), tin danh tính từ request, guard chỉ xác thực mà không phân quyền. Dùng khi review diff API, endpoint mới, hoặc nhắc "check phân quyền", "endpoint này an toàn không", "review authz", "IDOR", "access control".
---

# Soát phân quyền backend

> **Chỉ báo lỗi chỉ được ra chỗ.** Mỗi lỗi có `file:dòng`, mã luật, lý do, cách sửa.
> Kiểm tra quyền nằm ở chỗ không thấy được (middleware, policy layer) thì ghi
> **"chưa kiểm chứng"**, không đoán là có hay không.
> **Chỉ soát và báo, không tự sửa** trừ khi người dùng bảo sửa.

Phạm vi: endpoint đọc, sửa, xoá tài nguyên theo id lấy từ request. Không lo xác thực
(đăng nhập, token), không lo rate limit. Đề ngoài phạm vi thì báo một dòng rồi vẫn làm.

## Các bước

1. Liệt kê mọi endpoint trong phạm vi có đọc id từ path, query hoặc body.
2. Mỗi endpoint, mở luật ở bảng dưới và soát theo phần **Cách làm** của luật đó.
3. Không báo endpoint trả dữ liệu công khai, hoặc truy vấn đã ràng buộc theo chủ sở hữu lấy từ token.
4. Báo theo mẫu ở cuối.

## Mở khi

| Gặp | Mở |
| --- | --- |
| Endpoint đọc, sửa, xoá theo id | `references/rules-authz.md` mục `A1` |
| Định đổi một luật, hoặc thấy mình đang nghĩ "guard là đủ" | `references/locked-rules.md` |

Chỉ áp dụng luật có trạng thái `reviewed` hoặc `verified`. Luật `draft` thì vẫn dùng được
nhưng ghi rõ "(luật draft)" cạnh lỗi.

## Mẫu báo

| Mức | file:dòng | Luật | Vấn đề | Cách sửa |
| --- | --- | --- | --- | --- |

Cuối báo cáo: số endpoint đã soát, số lỗi, những chỗ chưa kiểm chứng.
