# Prompt nghiên cứu sâu: nỗi đau khi dùng AI coding agent

Dùng với chế độ Deep Research (ChatGPT, Gemini, Perplexity…). Dán nguyên khối dưới đây.

```text
Vai trò: bạn là nhà nghiên cứu về trải nghiệm lập trình viên (DevEx). Trả lời bằng tiếng Việt, giữ thuật ngữ kỹ thuật tiếng Anh.

MỤC TIÊU
Tôi đang xây một bộ "skill" (file hướng dẫn + script kiểm tra) cho coding agent như Claude Code, Codex, Cursor, Gemini CLI.
Tôi đã đo và biết: skill CHỈ có giá trị ở những việc mà AI MẶC ĐỊNH LÀM SAI hoặc làm tệ. Ở việc AI đã làm tốt
(ví dụ phát hiện lỗi IDOR kinh điển), skill gần như vô ích. Hãy tìm cho tôi những nỗi đau thật, lặp lại, mà AI mặc định làm tệ.

PHẠM VI
- Thời gian: ưu tiên 2025–2026. Ghi ngày của từng nguồn.
- Công việc: web backend (Node/NestJS, Prisma/Postgres), frontend (React/Next.js, Tailwind), test, review, migration, deploy, monorepo.
- Nguồn phải quét, càng nhiều càng tốt:
  1. Khảo sát lớn: Stack Overflow Developer Survey, JetBrains State of Developer Ecosystem, GitHub Octoverse, DORA, METR, các báo cáo của Faros, GitClear, Veracode, CodeRabbit, LinearB, Sonar (đánh dấu là vendor).
  2. Nghiên cứu học thuật: arXiv, ICLR, ICSE, FSE 2025–2026 về hành vi của coding agent (reward hacking, test, context file, skills, hallucination).
  3. Cộng đồng: Reddit (r/ClaudeAI, r/ChatGPTCoding, r/cursor, r/ExperiencedDevs, r/webdev), Hacker News, GitHub Issues của anthropics/claude-code, openai/codex, cursor, google-gemini/gemini-cli (lọc issue có nhiều reaction), dev.to, Medium, X/Twitter của dev có tiếng.
  4. Cộng đồng Việt Nam: Viblo, TopDev, ITviec blog, VNReview, các group Facebook lập trình lớn, J2TEAM. Ghi rõ nếu không tìm thấy.
  5. Sự cố thật: postmortem, incident (ví dụ agent xoá DB, lộ secret, phá migration).

VỚI MỖI NỖI ĐAU, TRẢ LỜI ĐỦ 6 MỤC
1. Mô tả cụ thể: AI làm sai gì, trong tình huống nào. Kèm 1–2 ví dụ thật (trích ngắn, có link).
2. Mức phổ biến: bao nhiêu nguồn ĐỘC LẬP nhắc tới; số liệu định lượng nếu có (ghi rõ số mẫu, phương pháp).
3. Bằng chứng AI MẶC ĐỊNH làm tệ: có benchmark hay thí nghiệm so sánh không? Model đời mới (2026) đã khắc phục chưa?
4. Kiểm bằng máy được không: lint, script, hook, test, CI nào bắt được? Hay chỉ người mới nhận ra?
5. Giải pháp đã có: công cụ, skill, MCP server, rule file nào đã giải; hiệu quả có được đo không; còn thiếu gì.
6. Phụ thuộc dự án: đây là lỗi chung (model có thể học) hay lỗi do quy ước riêng của từng đội (model không thể tự biết)?

ĐẦU RA
A. Bảng tổng hợp ít nhất 20 nỗi đau: tên | phổ biến (cao/trung/thấp + số nguồn) | AI mặc định tệ (có/không/chưa rõ + bằng chứng) | kiểm bằng máy (có/một phần/không) | đã có giải pháp tốt (có/một phần/chưa) | chung hay riêng dự án.
B. Top 5 "khoảng trống": phổ biến, AI mặc định tệ, kiểm được bằng máy, CHƯA có giải pháp tốt. Mỗi mục đề xuất skill cụ thể: luật gì, script kiểm gì, cách đo trước/sau.
C. Danh sách những thứ KHÔNG nên làm skill vì AI đã làm tốt hoặc đã có công cụ tốt, kèm bằng chứng.
D. Danh sách nguồn: tiêu đề, link, ngày, loại (khảo sát / học thuật / vendor / cộng đồng / sự cố).

QUY TẮC
- Không bịa nguồn, số liệu, trích dẫn. Không tìm được thì ghi "không tìm thấy".
- Tách rõ: số liệu đo được, ý kiến của một người, và suy luận của bạn.
- Đánh dấu [vendor] cho nguồn từ công ty bán giải pháp đó.
- Khi các nguồn mâu thuẫn, nêu cả hai và nói nguồn nào đáng tin hơn, vì sao.
- Ưu tiên nguồn gốc (paper, báo cáo gốc, issue gốc) hơn bài viết lại.
```

## Sau khi có kết quả

Dán kết quả vào `docs/` (ví dụ `docs/pain-research-gpt.md`) rồi đối chiếu với `docs/pain-research.md`. Nỗi đau nào cả hai bên đều xếp cao thì ưu tiên. Mọi số liệu dùng để viết luật phải được mở link gốc và ghi ngày kiểm.
