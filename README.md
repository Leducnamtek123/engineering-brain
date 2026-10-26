# engineering-brain

Bộ não dài hạn cho người và AI agent: quy tắc có nguồn, skill, eval và bài học. Toàn bộ là file markdown trong git, nên đổi model hay đổi agent (Claude Code, Codex, Gemini CLI, Cursor, model local) vẫn dùng được.

## Nguyên tắc

1. **File trong git là gốc sự thật.** Memory (basic-memory, mem0…) nếu có chỉ là index, xóa đi dựng lại được.
2. **Chuẩn mở:** `AGENTS.md` là lối vào, skill theo định dạng Agent Skills (`SKILL.md`), tool và memory nối qua MCP.
3. **Không có eval thì không có quy tắc verified.** Quy tắc chỉ được giữ khi chạy có nó tốt hơn chạy không có nó.
4. **AI viết nháp, người duyệt.** Trạng thái: `draft → reviewed → verified → deprecated`.
5. **Skill nhỏ.** Mỗi skill chỉ 2–3 phần, chi tiết để ở `knowledge/`.

## Cấu trúc

```
AGENTS.md            lối vào cho mọi agent
CLAUDE.md            chỉ import AGENTS.md
knowledge/<domain>/  quy tắc, mỗi file một quy tắc (mẫu: knowledge/_TEMPLATE.md)
skills/<name>/       skill theo chuẩn Agent Skills
evals/<skill>/       ca test có đáp án + kết quả so sánh
lessons/             bài học sau mỗi task (thô, chưa phải quy tắc)
decisions/           quyết định lớn (ADR)
scripts/             kiểm tra cấu trúc
```

## Quy trình

### A. Mở một góc hẹp mới
1. Chọn một lỗi lặp lại, ghi Problem Brief vào `decisions/` hoặc issue.
2. Gom 10–20 task thật, viết thành ca test trong `evals/<skill>/cases/`. Phải có cả **ca đúng** (code không lỗi) để đo báo sai.
3. Chạy **baseline**: agent làm các ca **khi chưa có skill**, ghi vào `results.md`.
4. Nghiên cứu nguồn, viết quy tắc trong `knowledge/` (status `draft`).
5. Viết skill nhỏ trỏ tới các quy tắc.
6. Người có chuyên môn duyệt (`reviewed`).
7. Chạy lại các ca **khi có skill**. Tốt hơn baseline thì đổi sang `verified`, không thì sửa hoặc bỏ.

### B. Vòng hằng ngày
Plan (đọc AGENTS.md + skill) → Work (worktree riêng) → Verify (test, người hoặc agent khác) → **Compound**: ghi bài học vào `lessons/`.

### C. Mỗi tuần
Đọc `lessons/`. Bài học nào lặp từ 2 lần trở lên thì nâng thành quy tắc, ca eval, test hồi quy hoặc lint. Chạy lại eval, ghi `CHANGELOG.md`.

### D. Khi đổi model hoặc agent
Chạy lại toàn bộ `evals/` với model mới. Quy tắc nào không còn giúp thì hạ về `reviewed` hoặc `deprecated`.

## Bậc tự động hóa
1. Chỉ báo cáo → 2. Tạo patch hoặc PR nháp → 3. Tự sửa việc nhỏ có test.
Merge, deploy, migration DB và các việc khó hoàn tác **luôn cần người duyệt**.

## Kiểm tra cấu trúc

```bash
python scripts/check_rules.py
```
