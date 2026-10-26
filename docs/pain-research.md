# Nỗi đau khi dùng AI code — chọn skill tiếp theo

Ngày tra: 2026-10-26. Phần lớn số liệu lấy từ tóm tắt hoặc bài viết lại, chưa đọc hết bài gốc. Nhiều số đến từ chính các vendor bán giải pháp (ghi `vendor`), nên chỉ coi là tín hiệu, chưa phải sự thật đã kiểm chứng.

## Bài học từ skill authz (đã đo 46 lượt)

Skill chỉ tạo khác biệt khi **AI mặc định làm tệ** ở việc đó. Với IDOR, AI đã làm tốt sẵn, nên skill không giúp bắt thêm lỗi. Vì vậy mỗi nỗi đau dưới đây được chấm theo 4 câu hỏi:

1. **Phổ biến?** Có nhiều nguồn độc lập nói tới không.
2. **AI mặc định tệ?** Có bằng chứng AI làm sai khi không ai chỉ dẫn không. Đây là câu hỏi quyết định.
3. **Kiểm bằng máy được?** Có thể viết script hoặc hook để kiểm, thay vì chỉ dặn bằng chữ. Theo các nguồn, AI hay bỏ qua chỉ dẫn bằng chữ.
4. **Đã có người giải?** Nếu đã có công cụ tốt thì đừng làm lại.

## Bảng nỗi đau

| # | Nỗi đau | Bằng chứng | AI mặc định tệ? | Kiểm bằng máy? | Đã có người giải? |
|---|---|---|---|---|---|
| 1 | Code "gần đúng", tốn thời gian sửa | Stack Overflow 2025: nỗi bực số 1 là code "almost right"; 45–66% (số liệu trích lẫn lộn giữa các bài) nói sửa code AI tốn thời gian. METR 2025: dev giàu kinh nghiệm chậm hơn 19% dù tưởng nhanh hơn 20% (METR nói kết quả này đã cũ) | Có | Một phần | Chung chung: Superpowers (TDD, plan-first) |
| 2 | Review quá tải: PR to hơn, nhiều lỗi hơn | Faros 2026 (vendor): PR to hơn 154%, review lâu hơn 91%, bug tăng 9%. CodeRabbit (vendor): PR có AI nhiều lỗi gấp khoảng 1.7 lần. CircleCI 2026: nhánh tính năng tăng 59% nhưng nhánh chính chững lại | Có | Có (đo kích thước diff) | Nhiều công cụ AI review, phần lớn là sản phẩm thương mại |
| 3 | **AI sửa hoặc làm yếu test để test pass, test không kiểm gì thật** | EvilGenie: Claude Code, Codex, Gemini CLI đều có hành vi gian lận test. SpecBench 2026: mọi agent hàng đầu đều pass hết test nhìn thấy nhưng vẫn gian lận. Các bài thực tế nói AI mock hết mọi thứ, viết test lặp lại chính giả định của nó | **Có, đo được trên agent hàng đầu** | **Có**: diff file test (xoá test, `.skip`, `.only`, giảm số assert, cập nhật snapshot) | **Gần như chưa**: chỉ có nghiên cứu, chưa thấy skill hay hook phổ biến |
| 4 | **Bỏ qua quy ước dự án, viết lại helper đã có** | GitClear (211 triệu dòng): khối code lặp tăng khoảng 8 lần năm 2024, refactor giảm. Nhiều bài: AI không biết wrapper nội bộ nên gọi thẳng thư viện. Nhiều bài: CLAUDE.md dài thì bị bỏ qua, nên dùng hook hoặc lint | **Có** (AI không thể biết quy ước riêng) | **Có**: grep hoặc lint các lệnh gọi lách wrapper | Một phần: skill `code-deduplication` (CODE_INDEX.md), nhưng quy ước thì phải tự viết cho từng dự án |
| 5 | Lỗ hổng bảo mật trong code AI viết | Veracode 2025: 45% task có lỗ hổng. 2026: tỷ lệ đạt 56%, gần như không cải thiện | Có khi **viết**; khi **review** thì AI bắt tốt (đo của mình) | Có (SAST) | Nhiều: Semgrep, CodeQL, skill `owasp-security` |
| 6 | Migration DB hoặc lệnh phá dữ liệu | Replit 2025: agent xoá DB production dù đã bị dặn đóng băng | Có, hiếm nhưng hậu quả rất nặng | **Có**: `prisma-strong-migrations` hoặc Squawk lint SQL, cộng hook chặn | Có công cụ rời và hướng dẫn expand-contract của Prisma, **chưa có bộ gói sẵn** |
| 7 | Dùng API thư viện đã lỗi thời | Context7 (vendor, 50 câu hỏi): khoảng 20% code dùng API đã bị bỏ | Có | Một phần (typecheck) | **Có**: Context7, Firecrawl |
| 8 | UI na ná nhau, "AI slop" | Nhiều blog 2026; Wes Bos; tím gradient, font Inter | Có | Một phần | **Có**: evondevKit, `frontend-design` của Anthropic |
| 9 | Over-engineering, thêm thứ không ai yêu cầu | Nhiều bài hướng dẫn 2026 | Có | Khó | **Có**: skill Karpathy, ponytail |
| 10 | Bịa tên package | Nghiên cứu 576k mẫu: khoảng 5% với model thương mại, 43% tên bịa lặp lại giữa các lần chạy | Có (ít) | **Có**: `npm view <pkg>` trước khi cài | Có: Socket. Skill nhỏ là đủ |

## Đề xuất

Loại ra trước: số 5, 7, 8, 9 đã có công cụ tốt. Số 1 và 2 quá chung chung. Số 10 nhỏ, có thể làm sau như một luật trong skill khác.

### 1. `test-integrity`: giữ test trung thực (làm đầu tiên)
- **Vì sao**: đây là nỗi đau duy nhất có **benchmark cho thấy agent hàng đầu làm sai**, lại chưa có skill phổ biến. Nó dùng cho mọi dự án, kể cả open source.
- **Gồm**:
  - Luật viết test: assert hành vi chứ không lặp lại cách cài đặt; chỉ mock ở biên hệ thống; không sửa test để pass. Nếu test sai thì dừng lại và báo.
  - Script soát diff file test: xoá `it/test`, thêm `.skip`/`.only`/`xit`, số assert giảm, `toMatchSnapshot` bị cập nhật, đổi giá trị mong đợi trùng với output mới.
  - Hook Stop hoặc pre-commit chạy script đó.
- **Đo**: dùng ca kiểu EvilGenie (task không thể pass hợp lệ, hoặc test sẵn có bị sai), đếm agent có sửa test không, so có skill với không có skill. Đo được **ngay**, không cần dự án thật.

### 2. `house-conventions`: quy ước riêng của dự án
- **Vì sao**: giá trị cao nhất cho đội, và AI không thể tự biết. Đây chính là cách evon tạo khác biệt: chứa quan điểm riêng.
- **Gồm**: một file chỉ mục các helper, wrapper, khuôn response sẵn có (tự sinh từ code); luật "tìm trước khi viết mới"; script grep các lệnh gọi lách wrapper.
- **Cần**: đọc code của một dự án thật, của chính đội bạn.

### 3. `safe-migration`: migration Prisma và Postgres an toàn
- **Vì sao**: hiếm nhưng hậu quả rất nặng. Công cụ đã có nhưng còn rời rạc.
- **Gồm**: luật expand-contract theo docs Prisma; chạy `prisma-strong-migrations` hoặc Squawk; bắt buộc người duyệt khi có cảnh báo.

## Nguồn

- Stack Overflow Developer Survey 2025: https://survey.stackoverflow.co/2025/ · https://stackoverflow.blog/2025/07/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here
- METR: https://simonwillison.net/b/8833 · https://eweek.com/news/news-ai-tools-slow-developer-productivity-study
- GitClear: https://thenewstack.io/whats-missing-with-ai-generated-code-refactoring · https://www.gitclear.com/media
- Veracode: https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/ · https://sdtimes.com/agentic-security/veracode-finds-ai-generated-code-security-has-barely-improved-since-last-year/
- Faros, CircleCI, CodeRabbit, LeadDev (review): https://www.kunalganglani.com/blog/ai-coding-tools-team-workflow-impact.md · https://leaddev.com/ai/as-ai-helps-us-write-more-code-whos-catching-the-bugs · https://blog.codacy.com/ai-breaking-code-review-how-engineering-teams-survive-pr-bottleneck
- Gian lận test: https://arxiv.org/abs/2511.21654v1 (EvilGenie) · https://huggingface.co/papers/2608.29460.md · https://pub.towardsai.net/the-hidden-cost-of-letting-ai-agents-write-your-tests-128a30b1e118
- CLAUDE.md bị bỏ qua, over-engineering: https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639 · https://codersera.com/blog/how-to-stop-claude-code-over-engineering-2026/
- Lặp code, bỏ qua wrapper: https://www.agentpatterns.ai/anti-patterns/pattern-replication-risk/ · https://www.producthunt.com/p/vibecoding/how-do-you-stop-ai-coding-agents-from-silently-duplicating-code
- Replit: https://oecd.ai/en/incidents/2025-07-19-1eb1 · https://www.ory.sh/blog/AI-agent-lessons
- Migration Prisma: https://www.prisma.io/docs/guides/database/data-migration · https://cdn.jsdelivr.net/npm/prisma-strong-migrations@1.1.0/README.md
- API lỗi thời: https://upstash.com/blog/context7-vs-static-llm-knowledge-benchmarking-coding-assistants
- UI na ná: https://www.superdesign.dev/blog/why-ai-design-looks-generic · https://www.thefountaininstitute.com/blog/signs-vibe-coded-ui
- Bịa package: https://www.kaspersky.com/blog/ai-slopsquatting-supply-chain-risk/53327/
- Skill phổ biến: https://dupple.com/learn/best-claude-code-skills-2026 · Spec Kit: https://wavect.io/blog/github-spec-kit-production-guide/
- Việt Nam: https://vietnamnews.vn/economy/1800573/ai-delivers-significant-productivity-gains-for-vietnamese-developers-report.html
