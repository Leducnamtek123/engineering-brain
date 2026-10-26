# Phát triển engineering-brain

Ghi chú cho người sửa skill. Người dùng skill đọc `README.md`.

## Cấu trúc

```
.claude-plugin/
├── plugin.json            khai báo plugin "brain"
└── marketplace.json       marketplace "engineering-brain", cài được cả local lẫn GitHub
AGENTS.md                  lối vào cho mọi agent (CLAUDE.md chỉ import file này)
skills/
└── backend-authz-review/  → /brain:backend-authz-review
    ├── SKILL.md           bộ định tuyến: phạm vi, các bước, bảng "Mở khi", mẫu báo
    ├── VERSION            phải khớp plugin.json
    └── references/
        ├── rules-authz.md luật A, mỗi luật có mã, nguồn, ngày kiểm, test
        └── locked-rules.md luật đã chốt và lý lẽ đã bị bác
tests/<skill>/             ca test có đáp án, mỗi file một ca
TESTS.md                   danh sách ca và bảng kết quả baseline với có skill
lessons/                   bài học thô sau mỗi task, chưa phải luật
BACKLOG.md                 skill và luật định làm
scripts/lint.py            soát cấu trúc trước khi commit
```

Skill tự chứa: mọi luật nó dùng nằm trong `references/` của chính nó, nên copy một thư mục
skill sang agent khác là chạy được.

## Mẫu một luật

Đặt trong `skills/<skill>/references/rules-<nhóm>.md`. Mã gồm chữ cái của nhóm + số, ví dụ `A1`, `F3`.

```markdown
## X1. Tên ngắn nói rõ vấn đề

- Mức: must · Trạng thái: draft
- Test: `tests/<skill>/case-001-....md`
- Nguồn: [Tên nguồn](https://...) (kiểm YYYY-MM-DD)

**Luật.** Một hai câu làm theo được và kiểm tra được. Không dùng tính từ kiểu "tốt", "hiện đại".

*Vì sao:* hậu quả nếu bỏ qua.

**Cách làm.** Các bước agent phải làm.

**Kiểm chứng.** Chứng minh đạt bằng test, lệnh, ảnh chụp hoặc người review.

**Ngoại lệ.** Trường hợp cần xử lý khác.
```

- Mức: `must` (bắt buộc), `should` (khuyến nghị), `info` (tham khảo).
- Trạng thái: `draft` → `reviewed` (người có chuyên môn đã duyệt) → `verified` (test có skill tốt hơn baseline) → `deprecated`.
- Agent **không** tự nâng trạng thái lên `verified`.
- Nguồn kiểm quá 180 ngày thì lint cảnh báo: đọc lại nguồn rồi cập nhật ngày.

## Test

Mỗi ca trong `tests/<skill>/` có `kind: positive` (có lỗi phải bắt) hoặc `kind: negative`
(code đúng, không được báo). Phải có cả hai loại, không thì không đo được báo sai.

1. **Baseline:** chạy ca khi **chưa có** skill. Prompt giống hệt nhau giữa các lần.
2. **Có skill:** chạy lại y hệt khi có skill.
3. Chấm theo `Expected`: trúng, bỏ sót, báo sai. Người chấm không phải agent vừa làm bài.
4. Ghi vào bảng trong `TESTS.md`, kèm agent, model, ngày. Mỗi cấu hình ít nhất 2 lần.
5. Đổi model hay agent thì chạy lại hết.

Test ở máy:

```bash
/plugin marketplace add ./
/plugin install brain@engineering-brain
```

Trước khi commit:

```bash
python scripts/lint.py
```

## Ra bản mới

Người đã cài chỉ nhận bản mới khi `version` trong `.claude-plugin/plugin.json` tăng.

| Thay đổi | Tăng |
| --- | --- |
| Sửa luật, thêm luật, thêm ca test | patch: `0.1.0 → 0.1.1` |
| Skill mới, đổi cấu trúc | minor: `0.1.x → 0.2.0` |

Tăng ở **cả** `plugin.json` lẫn `skills/*/VERSION` (lint báo nếu lệch). Push xong thì gắn tag `vX.Y.Z` và tạo GitHub Release.

## Quyết định nền

**File markdown trong git là gốc sự thật** (2026-10-26). Memory như basic-memory, mem0 hay
Graphiti nếu có chỉ là index, xoá đi dựng lại được. Lý do: đổi agent không mất gì, git cho
lịch sử và review, không phải vận hành DB. Hệ quả: khi kho lớn tới mức grep chậm mới thêm index.
