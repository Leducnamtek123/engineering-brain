# Quy ước dự án — luật H

Nguồn duy nhất cho cách viết code mới trong codebase còn code cũ lệch quy ước. Mẫu viết luật: `DEVELOP.md`.

---

## H1. Code mới theo quy ước đích, không chép code bên cạnh

- Mức: must · Trạng thái: draft
- Test: `tests/house-conventions/case-001-legacy-mui-page.md`, `tests/house-conventions/case-002-django-side-effect.md`
- Nguồn: [AgentPatterns: Pattern Replication Risk](https://agentpatterns.ai/patterns/anti-patterns/pattern-replication-risk/) (kiểm 2026-10-26)

**Luật.** Khi file đang sửa (hoặc file mẫu gần nhất) dùng pattern mà tài liệu dự án nói là cũ hoặc cấm, phần code **mới thêm**
phải theo quy ước đích. Ví dụ ở dự án Square: thêm nút vào trang MUI thì dùng `Button` của Shadcn + Tailwind, chuỗi qua `t()`.

*Vì sao:* agent học từ code nó đọc thấy và coi code cũ, code chuẩn như nhau, nên nhân bản pattern cũ ra khắp nơi.
AgentPatterns dẫn GitClear: code copy/paste tăng từ 8.3% lên 12.3%. Ở chính dự án Square, `InterviewedCandidatesPanel`
được thêm mới với khoảng 90 dòng vi phạm (MUI, `any`) và phải có commit refactor sửa lại ngay hôm sau.

**Cách làm.** Xác định quy ước đích từ tài liệu, không từ file bên cạnh. Nếu hai thứ trộn lẫn trông xấu, vẫn ưu tiên quy ước
và ghi chú trong báo cáo; không tự chuyển cả file cũ trừ khi được giao.

**Kiểm chứng.** Ratchet (H3) không còn vi phạm trong dòng mới.

**Ngoại lệ.** Người dùng yêu cầu rõ giữ nguyên pattern cũ (ví dụ sửa nóng một dòng trong file MUI): ghi lý do.

---

## H2. Tìm building block có sẵn trước khi viết mới

- Mức: should · Trạng thái: draft
- Test: `tests/house-conventions/case-001-legacy-mui-page.md`, `tests/house-conventions/case-002-django-side-effect.md`
- Nguồn: [AgentPatterns: Pattern Replication Risk](https://agentpatterns.ai/patterns/anti-patterns/pattern-replication-risk/) (kiểm 2026-10-26)

**Luật.** Trước khi tạo component, hook, helper, service mới, liệt kê các thư mục building block của dự án
(`--blocks`) và tìm thứ đã có. Có thì dùng; không có mới viết, và viết vào đúng thư mục đó.

*Vì sao:* agent hay tự viết lại tiện ích đã có ("hand-rolled utilities you meant to retire"), các bản sao lệch nhau dần.

**Cách làm.** Tìm theo tên và theo chức năng (grep động từ chính: `format`, `notify`, `close`...). Ghi vào báo cáo đã dùng gì.

**Kiểm chứng.** Báo cáo có mục building block; review không thấy hàm trùng chức năng.

**Ngoại lệ.** Building block có sẵn sai hoặc không đủ: dùng và mở rộng nó thay vì viết bản song song, trừ khi được giao khác.

---

## H3. Kiểm dòng mới bằng máy trước khi báo xong

- Mức: must · Trạng thái: draft
- Test: `tests/house-conventions/case-001-legacy-mui-page.md`, `tests/house-conventions/case-002-django-side-effect.md`, `tests/house-conventions/case-003-clean-control.md`
- Nguồn: [I Wrote 200 Lines of Rules for Claude Code. It Ignored Them All.](https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639) (kiểm 2026-10-26); [AgentPatterns: Pattern Replication Risk](https://agentpatterns.ai/patterns/anti-patterns/pattern-replication-risk/) (kiểm 2026-10-26)

**Luật.** Chạy `scripts/check_new_code.py` với cấu hình của dự án trên diff so với nhánh gốc. Chỉ dòng **mới** bị soát,
nên code cũ không làm nhiễu. Không báo xong khi còn vi phạm chưa giải thích.

*Vì sao:* luật bằng chữ bị bỏ qua; kiểm bằng code thì không. AgentPatterns: lint chặn pattern cũ hiệu quả hơn lời dặn
"hãy dùng API mới", vì lời dặn phải cạnh tranh với hàng trăm chỗ code cũ agent đọc thấy. Ở Square, 30 commit gần nhất
vẫn thêm khoảng 229 dòng vi phạm dù `AGENTS.md` đã cấm.

**Cách làm.** Đưa cùng script vào pre-commit hoặc CI với `--base origin/main` để chặn ở cả người lẫn agent.

**Kiểm chứng.** Script in `0 vi phạm trong dòng mới`.

**Ngoại lệ.** Dòng di chuyển nguyên trạng từ file khác (refactor đổi chỗ) có thể bị đếm là mới: ghi rõ trong báo cáo.
