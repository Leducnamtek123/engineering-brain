# Test trung thực — luật T

Nguồn duy nhất cho cách đối xử với test khi làm task. Mẫu viết luật: `DEVELOP.md`.

---

## T1. Không đổi test để làm nó pass

- Mức: must · Trạng thái: draft
- Test: `lab:tests/test-integrity/case-001-spec-conflict.md`, `lab:tests/test-integrity/case-002-wrong-expected.md`
- Nguồn: [EvilGenie: A Reward Hacking Benchmark](https://arxiv.org/abs/2511.21654) (kiểm 2026-10-26); [Escalation channels and reward hacking](https://huggingface.co/papers/2608.29460) (kiểm 2026-10-26)

**Luật.** Không sửa giá trị mong đợi, xoá test, thêm `skip`/`only`/`xit`/`@pytest.mark.skip`, nới assert
(`toEqual` thành `toBeTruthy`, bỏ bớt `expect`), hay cập nhật snapshot chỉ để test xanh. Chỉ được đổi test khi
**người dùng yêu cầu rõ**, hoặc khi chứng minh được test sai bằng spec, và khi đó phải báo theo mẫu trong `SKILL.md`.

*Vì sao:* EvilGenie ghi nhận Claude Code, Codex và Gemini CLI đều có lúc sửa file test hoặc hardcode để pass.
Test bị đổi thì không còn đo được gì, và người review khó thấy vì diff trông như "sửa test cho đúng".

**Cách làm.**
1. Test đỏ: đọc spec, xác định code sai hay test sai.
2. Code sai thì sửa code.
3. Test có vẻ sai thì **dừng**, không sửa test, báo theo mẫu.

**Kiểm chứng.** `scripts/check_test_diff.py` không có cảnh báo, hoặc mỗi cảnh báo có lời giải thích được người dùng chấp nhận.

**Ngoại lệ.** Người dùng giao rõ việc sửa hoặc refactor test; test bị đổi do đổi tên API mà hành vi giữ nguyên (ghi rõ trong báo cáo).

---

## T2. Không viết code nhận diện input của test

- Mức: must · Trạng thái: draft
- Test: `lab:tests/test-integrity/case-002-wrong-expected.md`
- Nguồn: [EvilGenie: A Reward Hacking Benchmark](https://arxiv.org/abs/2511.21654) (kiểm 2026-10-26)

**Luật.** Không thêm nhánh `if` theo đúng giá trị input của test, bảng tra kết quả, hay đọc tên test, biến môi trường
của test runner để trả kết quả khác. Code phải đúng với input bất kỳ theo spec.

*Vì sao:* hardcode làm test xanh nhưng hàm sai với mọi input khác. Đây là dạng gian lận EvilGenie dùng held-out test để bắt.

**Cách làm.** Nếu chỉ pass được bằng cách xử lý riêng một input, coi như test đó sai, chuyển sang T1 bước 3.

**Kiểm chứng.** Thử thêm vài input ngoài bộ test theo spec, kết quả vẫn đúng.

**Ngoại lệ.** Spec quy định riêng giá trị đó (ví dụ "đơn 0đ không tính phí"): ghi nguồn spec ngay cạnh nhánh.

---

## T3. Test và spec mâu thuẫn thì báo trước khi chọn

- Mức: must · Trạng thái: draft
- Test: `lab:tests/test-integrity/case-001-spec-conflict.md`, `lab:tests/test-integrity/case-003-honest-control.md`
- Nguồn: [Escalation channels and reward hacking](https://huggingface.co/papers/2608.29460) (kiểm 2026-10-26)

**Luật.** Khi test và spec (docstring, README, `SPEC.md`, issue) nói khác nhau, không lặng lẽ đi theo một bên. Báo mâu thuẫn
theo mẫu, nêu bên nào mình đã theo và vì sao.

*Vì sao:* bài báo đo trên 8 model hàng đầu: có chính sách chống gian lận kèm kênh báo cáo thì gian lận giảm từ 23.6% xuống 5.3%.
Báo cáo chính là kênh đó. Đi theo test một cách im lặng có thể giấu một lỗi spec, hoặc một test sai.

**Cách làm.** Mặc định cài theo spec (spec là nguồn ý định), để test mâu thuẫn ở trạng thái đỏ và báo. Nếu spec rõ ràng đã cũ thì nói ra, đừng tự quyết.

**Kiểm chứng.** Báo cáo cuối có mục "TEST CẦN NGƯỜI QUYẾT" cho mỗi mâu thuẫn.

**Ngoại lệ.** Không có spec nào ngoài test: test là spec, làm theo test.

---

## T4. Test mới phải kiểm hành vi thật

- Mức: should · Trạng thái: draft
- Test: `lab:tests/test-integrity/case-003-honest-control.md`
- Nguồn: [Software Engineering at Google, ch. 13 Test Doubles](https://abseil.io/resources/swe-book/html/ch13.html) (kiểm 2026-10-26)

**Luật.** Assert trên kết quả quan sát được (giá trị trả về, trạng thái, lỗi ném ra), không lặp lại cách cài đặt.
Ưu tiên implementation thật; chỉ dùng mock hoặc stub ở biên hệ thống (mạng, thời gian, dịch vụ ngoài, thứ chậm hoặc không xác định).

*Vì sao:* Google ghi nhận lạm dụng mock làm test lặp code, lệch khỏi implementation thật và cản refactor. Test mock hết
mọi thứ thì xanh cả khi hệ thống hỏng.

**Cách làm.** Mỗi test trả lời được "nếu code sai theo kiểu X thì test này đỏ". Không trả lời được thì test đó vô dụng.

**Kiểm chứng.** Cố tình làm sai code (đảo điều kiện, đổi hằng số), ít nhất một test phải đỏ.

**Ngoại lệ.** Test tương tác (kiểm một hàm được gọi đúng cách) khi chính việc gọi là hành vi cần đảm bảo, ví dụ gửi email.
