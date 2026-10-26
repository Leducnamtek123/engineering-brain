# Backlog

## Bây giờ
- Repo này dùng cho nhiều dự án: không chứa tên hay code của dự án cụ thể. Dữ liệu thật chỉ được đọc để thử; chủ dự án tự áp dụng (copy `check_new_code.py` + một file `conventions.json` vào repo đích).
- Viết hướng dẫn ngắn "áp dụng house-conventions cho repo của bạn": cách viết `conventions.json` từ AGENTS.md có sẵn, cách chạy thử trên N commit gần nhất để lấy mốc.
- Chọn license (đang để `TODO` trong `plugin.json`, chưa có file `LICENSE`).
- Nhờ người có chuyên môn duyệt luật để lên `reviewed`: A1, A2 (bảo mật), M1–M4 (DB), H1–H3 (tech lead của dự án áp dụng).

## Sau
- test-integrity: ca khó hơn, nơi agent không giải hợp lệ được (kiểu LiveCodeBench), để đo tỷ lệ gian lận thật.
- house-conventions: chỉ mục building block tự sinh nếu `--blocks` (liệt kê thư mục) không đủ.
- Thêm index tìm kiếm (basic-memory) khi grep `lessons/` không còn đủ.
- Lộ trình skill theo vai trò (BA, QA, pentest, DevOps, lead…): xem `docs/pain-catalog.md`. Mỗi skill bắt đầu bằng đo baseline; baseline đã đạt thì không làm.
- Đối chiếu `docs/pain-catalog.md` với kết quả GPT deep research (`docs/research-prompt.md`).

## Đã xong (2026-10-26)
- backend-authz-review: A1, A2, 7 ca, 5 vòng (46 lượt). Baseline đã bắt được hết IDOR; skill giảm báo sai trên Haiku.
- test-integrity: T1–T4, script soát diff test, 3 ca (24 lượt). Không ai gian lận ở ca rõ ràng.
- safe-migration: M1–M4, script soát SQL, 3 ca (24 lượt). Baseline đã bắt được hết; script kiểm đúng 3/3.
- house-conventions: H1–H3, ratchet theo cấu hình, 3 ca (24 lượt). **Baseline 2/8, có skill 8/8.**
- Agent đọc `lessons/` lúc bắt đầu task; CI chạy lint (đang chờ billing GitHub).
