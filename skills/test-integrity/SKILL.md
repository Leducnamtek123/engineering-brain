---
name: test-integrity
description: Giữ test trung thực khi làm task có test - không sửa, xoá, skip test hay hardcode kết quả để cho pass; khi test sai hoặc mâu thuẫn spec thì dừng và báo theo mẫu. Dùng khi được giao "làm cho test pass", sửa bug có test đỏ, viết hoặc sửa test, hoặc review diff có đụng file test ("check test", "test integrity", "test bị sửa").
---

# Giữ test trung thực

> **Test là thước đo, không phải chướng ngại.** Không bao giờ làm cho test pass bằng cách
> đổi thước đo. Khi không thể pass một cách hợp lệ, **dừng và báo** theo mẫu ở cuối. Báo đúng
> là hoàn thành task, không phải thất bại.

## Khi viết code để test pass

1. Đọc spec trước test: docstring, README, `SPEC.md`, issue, comment. Test chỉ là một nguồn.
2. Cài đặt theo **hành vi đúng**, không theo từng ca test.
3. Gặp một trong các tình huống sau thì mở `references/rules-tests.md` và làm theo luật tương ứng:

| Gặp | Luật |
| --- | --- |
| Muốn sửa, xoá, `skip`, `only`, nới assert, cập nhật snapshot để test xanh | `T1` |
| Chỉ pass được nếu nhận diện input của test (if theo giá trị cụ thể, bảng tra kết quả) | `T2` |
| Test và spec nói khác nhau | `T3` |
| Viết test mới hoặc sửa test theo yêu cầu | `T4` |

4. Trước khi báo xong: chạy lại toàn bộ test, và chạy `scripts/check_test_diff.py` (trong thư mục skill) nếu repo dùng git.

## Khi review diff

Chạy `python <thư mục skill>/scripts/check_test_diff.py --base <ref>`. Mỗi cảnh báo phải được giải thích
trong mô tả PR (vì sao test đổi). Không có lời giải thích thì coi là lỗi.

## Mẫu báo khi dừng

```
TEST CẦN NGƯỜI QUYẾT
- Test: <file>::<tên test>
- Mong đợi trong test: <giá trị>
- Theo spec/hành vi đúng: <giá trị>, nguồn: <file:dòng hoặc câu spec>
- Đã làm: <cài đặt theo spec / chưa đổi gì>; test này đang <đỏ/xanh>
- Đề xuất: <sửa test thành ... / sửa spec thành ...>
```
