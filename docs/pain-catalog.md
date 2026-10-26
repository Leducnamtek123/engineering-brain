# Catalog nỗi đau theo vai trò — chọn skill có giá trị thật

Ngày: 2026-10-27. Nguồn: 7 lượt nghiên cứu song song (Sonnet, web search), mỗi vai trò một lượt, cộng `docs/pain-research.md`.

**Độ tin cậy.** Các con số dưới đây phần lớn được đọc qua bản tóm tắt của công cụ tìm kiếm, **chưa mở bài gốc**. Nhiều số đến từ chính các vendor bán giải pháp (ghi `[vendor]`). Trước khi đưa một con số vào luật của skill, phải mở link gốc và ghi ngày kiểm tra (quy ước của `DEVELOP.md`). Không tìm được thread Reddit hay HN cụ thể nào; cộng đồng chủ yếu được phản ánh qua blog.

## Bộ lọc (rút từ khoảng 140 lượt đo của chính repo này)

Skill tạo khác biệt lớn khi:
1. **AI mặc định làm tệ**, có bằng chứng đo được (benchmark, thí nghiệm). Kiến thức phổ biến như OWASP hay Postgres thì model đã thuộc.
2. **Có máy kiểm** được đầu ra (script, linter, hook), vì luật bằng chữ bị bỏ qua.
3. Tốt nhất là gắn với **quy ước riêng của đội** hoặc có **code cũ ngược quy ước** trong tầm nhìn của agent.

Thêm một phát hiện ảnh hưởng tới **cách đóng gói**: Vercel đo thấy agent **không gọi skill trong 56% trường hợp**. Với API ngoài dữ liệu huấn luyện, một chỉ mục ngắn trong `AGENTS.md` đạt 100%, còn skill tối đa 79% `[vendor]`. Hệ quả cho repo:
- Mỗi skill cần một dòng chỉ mục trong `AGENTS.md` của dự án áp dụng.
- Phần bắt buộc phải đi qua **hook hoặc CI**, không chỉ nằm trong skill.

## Bảng tổng hợp

Ký hiệu: ✅ có bằng chứng đo · ◐ chỉ giai thoại hoặc vendor · ✖ không thấy · — model đã làm tốt.

| # | Vai trò | Nỗi đau | AI mặc định tệ? | Máy kiểm? | Đã có giải pháp tốt? | Riêng dự án? |
|---|---|---|---|---|---|---|
| 1 | BA / dev | Yêu cầu mơ hồ nhưng agent **code luôn thay vì hỏi** | ✅ 6 paper; Pass@1 giảm 35–52% (HumanEvalComm); scaffold tách bước phát hiện mơ hồ 69,4% so với 61,2% (UA-Multi) | Một phần: cổng "câu hỏi mở / giả định có nhãn" | Chưa: chỉ có benchmark | Chung |
| 2 | BA / QA | Acceptance criteria không kiểm được, thiếu ca âm và biên | ◐ 2 nghiên cứu mẫu nhỏ; Thoughtworks khoảng 27% test case mơ hồ `[vendor]` | Có: parse Given/When/Then, đếm ca âm và biên, từ cấm | Chỉ có template, không có checker | Ngưỡng theo đội |
| 3 | BA / QA / lead | Mất truy vết requirement → task → test → code; agent sửa ngoài phạm vi | ◐ paper "Code Review to Code Critique" (khoảng 7.500 lượt chạy, chưa đọc gốc) | Có: REQ-ID mồ côi, file ngoài phạm vi trong diff | Chưa có bản đóng gói cho agent | Định dạng theo đội |
| 4 | Frontend | **Accessibility** của UI do AI dựng | ✅ Microsoft: 12% đạt khi không chỉ dẫn, 86% với skill của họ `[vendor]`; 541 lỗi ngữ nghĩa mà axe bỏ sót (CHI EA'26) | Có: axe + Playwright, kèm assertion hành vi | **Microsoft đã có skill 86%**, còn trống phần ngữ nghĩa | Chung |
| 5 | Frontend | API framework mới hoặc cũ (Next.js 15/16…) | ✅ Vercel: baseline 53% `[vendor]` | Có: `tsc`, `next build`, codemod, ratchet | Next.js 16.2 tự ship AGENTS.md | Theo phiên bản dự án |
| 6 | Frontend | Hydration mismatch, `"use client"` sai chỗ, lạm dụng `useEffect` | ◐ blog cộng đồng | Có: Playwright bắt console "Hydration", ESLint | react-doctor (chưa có eval) | Chung |
| 7 | Frontend / lead | **Chép pattern cũ, lệch design system / token** | ✅ đo của repo này: 2/8 → 8/8; ContextCov đặt tên là "Context Drift" | Có: ratchet chỉ soát dòng mới | `house-conventions` (đã làm) | **Riêng** |
| 8 | Backend | Side effect / idempotency / transaction (gửi trùng, charge hai lần) | ◐ blog | Có: rule tĩnh + test hai request song song cùng key | Gần như chưa có | **Riêng** |
| 9 | Backend | Contract OpenAPI lệch giữa BE và FE | ◐ giai thoại | Có, rất rõ: `oasdiff breaking`, regenerate type rồi `git diff` | oasdiff, Specmatic | Chính sách theo đội |
| 10 | Backend | N+1, thiếu phân trang | ✖ chưa có benchmark cho code AI | Có: đếm query ở N=1 so với N=25 | Sentry `django-perf-review` | Ngưỡng theo dự án |
| 11 | Backend | Logging và xử lý lỗi | ✅ 4.550 PR: agent bỏ 67% yêu cầu log | Có: lint `except: pass`, ratchet | Rule chung, chưa theo quy ước đội | Quy ước theo đội |
| 12 | QA | E2E "xanh mà không bảo vệ gì" (assert URL thay vì kết quả nghiệp vụ) | ◐ vendor | Một phần: lint assertion nghiệp vụ; bẻ app thử | Chỉ có checklist | Kết quả nghiệp vụ theo dự án |
| 13 | QA | Flaky: setup qua UI, `waitForTimeout`, không cleanup khi chạy song song | ◐ | Rất tốt: `--repeat-each=10 --workers=4`, lint | `eslint-plugin-playwright` (thiếu chạy lặp) | Fixture theo dự án |
| 14 | QA | Over-mocking | ✅ 1,2 triệu commit: agent thêm mock 36% so với người 26% (chưa đọc gốc) | Có: đếm mock trên mỗi test | Chỉ có văn bản hướng dẫn | Ngưỡng theo đội |
| 15 | QA | Chất lượng unit test | — Supercov: mutation score 92% `[vendor]`; Leith: không kém người | | | **Bỏ** |
| 16 | Pentest | Báo cáo lỗ hổng "AI slop", không tái hiện được (curl dừng bounty) | ◐ sự cố có thật, chưa có tỷ lệ | Có: bắt buộc PoC chạy được, CVSS khớp vector, kiểm scope | XBOW có validator nội bộ | Theo chương trình |
| 17 | AppSec | **Triage false positive của SAST** theo sanitizer nội bộ | ✅ precision Semgrep 35,7% so với hệ lai 89,5% (25 dự án, preprint) | Có, nếu có bộ nhãn | Semgrep/Snyk AI (chung, không biết sanitizer nội bộ) | **Riêng** |
| 18 | AppSec | Code AI **viết** thiếu phân quyền (khác với **review**: model review tốt) | ◐ Tenzai, Veracode `[vendor]` | Một phần: test A gọi tài nguyên của B, ma trận route × policy | | **Riêng** |
| 19 | AppSec | Prompt injection vào agent và MCP | ✅ AIShellJack tới 84% thành công trên Cursor/Copilot | Có: lint `.mcp.json`, allowlist, quét skill lạ | Rời rạc | Chung |
| 20 | DevOps | **Agent chạy lệnh phá hạ tầng** (destroy, xoá DB và backup) | ✅ nhiều sự cố thật 2025–2026 | Có: hook PreToolUse, Conftest trên plan, `prevent_destroy` | Hook có sẵn, chưa đóng gói | Danh sách tài nguyên quan trọng theo dự án |
| 21 | DevOps | **IaC do AI sinh "chạy được nhưng không an toàn"** | ✅ Checkov đạt 8,4–23%; 35,8% manifest K8s có smell | Rất tốt: Checkov, Trivy, kube-linter | Scanner chỉ đo, không sinh đúng | Baseline theo đội |
| 22 | DevOps | GitHub Actions: script injection, `pull_request_target`, không pin SHA | ◐ 38% tổ chức dính `[vendor]`; chưa đo workflow do AI viết | Rất tốt: zizmor, actionlint | zizmor (chỉ kiểm) | Allowlist theo đội |
| 23 | Lead | PR quá to, review quá tải | ✅ Faros: PR to hơn 154%, review lâu hơn 91% `[vendor]` | Có: giới hạn dòng và file mỗi PR, hotspot | Danger, Graphite (không giúp agent tự tách) | Ngưỡng theo đội |
| 24 | Lead | Code trùng, không dùng helper có sẵn | ✅ GitClear 8 lần `[vendor]` | Có: jscpd trên dòng mới, chỉ mục helper | jscpd (không bắt "có helper sẵn mà không dùng") | **Riêng** |
| 25 | Lead | AGENTS.md hoặc tài liệu cũ, lệnh và đường dẫn chết | ◐ khảo sát vendor | Có: kiểm lệnh, đường dẫn, symbol trong tài liệu còn tồn tại | Ít | Nội dung theo dự án |
| 26 | Lead | Nhiều agent đụng nhau | ◐ chưa xác minh | Một phần: hai nhánh cùng sửa file hotspot | | Hotspot theo dự án |

Bỏ khỏi danh sách (thiếu bằng chứng hoặc model đã tốt): ước lượng story point, concurrency nói chung, locator Playwright (model đã dùng `getByRole`), secrets (gitleaks đã đủ), bịa package (model thương mại khoảng 5%), chất lượng unit test.

## Lộ trình skill đề xuất

Thứ tự theo: bằng chứng "AI mặc định tệ" mạnh nhất, máy kiểm được, và vai trò chưa có skill nào.

| Thứ tự | Skill | Vai trò | Nỗi đau | Tạo ra gì (kiểu evon) | Máy kiểm | Đo trước/sau |
|---|---|---|---|---|---|---|
| 1 | `clarify-first` (**đã đo baseline 2026-10-27: 10/12 lượt tự nêu đúng, chưa làm skill**, xem `TESTS.md`) | BA, dev | #1 | Bản "câu hỏi mở + giả định có nhãn" trước khi code; mỗi giả định có giá trị mặc định | Cổng: không có code khi còn câu hỏi chặn; giả định nào cũng có nhãn | Dùng 3–6 task thiếu thông tin lấy từ HumanEvalComm/ClarifyCodeBench (bộ công khai, đã đo baseline sẵn) |
| 2 | `infra-guard` (**đã đo baseline 2026-10-27: 0/12 lượt chạy lệnh phá, chưa làm skill**, xem `TESTS.md`) | DevOps | #20 | Gói hook (chặn `terraform destroy/apply`, `kubectl delete`, `migrate reset`…) + runbook một trang | Hook xác định; Conftest trên plan JSON | Ba prompt nguy hiểm ("dọn staging" khi state trỏ prod…): đếm lệnh phá bị chặn |
| 3 | `iac-secure-by-default` | DevOps | #21 | Module Terraform và manifest K8s theo baseline của đội | Checkov/Trivy/kube-linter trên dòng mới + `terraform validate` | Ba yêu cầu (S3 cho log, Deployment, RDS): tỷ lệ đạt Checkov trước/sau |
| 4 | `story-spec` + `req-trace` | BA, QA | #2, #3 | File story có REQ-ID, Given/When/Then, tối thiểu ca âm và biên; bảng test case truy vết | Parse: thiếu ca âm/biên, từ cấm, REQ mồ côi, test mồ côi, file ngoài phạm vi | Ba yêu cầu mơ hồ: số ca âm/biên, số REQ bị sót |
| 5 | `finding-triage` | AppSec, pentest | #17 | `triage.jsonl` (TP/FP/cần người), mỗi kết luận FP phải trích `file:line` của guard | Precision/recall trên bộ nhãn; kiểm trích dẫn có thật | Ba finding: FP nhờ ORM nội bộ, taint thật qua helper, dữ liệu chỉ trong fixture |
| 6 | `vuln-report-gate` | Pentest | #16 | `report.md` mẫu cố định (tác động, scope, bước tái hiện, PoC, CVSS kèm vector) | CVSS tính lại từ vector, PoC chạy ra oracle trên lab, URL trong scope | Ba ca: header bị thổi thành High, IDOR có PoC, nghi ngờ chưa tái hiện được |
| 7 | `e2e-guard` | QA | #12, #13 | Test Playwright + manifest kết quả nghiệp vụ mỗi test kiểm | Lint + `--repeat-each=10 --workers=4` phải xanh 100% | Cần app chạy được; ba luồng (checkout, form, phân quyền) |
| 8 | `side-effect-safety` | Backend | #8 | Mẫu service: idempotency key, side effect trong `on_commit` | Ratchet + test gửi trùng | Ba ca: gửi email trong transaction, webhook trùng, retry quanh side effect |
| 9 | `pr-slice` | Lead | #23, #26 | `PLAN.md` chia PR có thứ tự, danh sách file mỗi PR, file hotspot | Dòng/file mỗi PR, hotspot bị chạm chung | Ba task lớn: số PR vượt ngưỡng |
| (đã có) | `house-conventions` | Mọi vai trò code | #7, #24 | Ratchet theo cấu hình | Có | 2/8 → 8/8 |

Không đề xuất làm lại `a11y` vì Microsoft đã có skill đạt 86%. Chỉ làm nếu nhắm vào lỗi ngữ nghĩa mà axe bỏ sót.

## Nguyên tắc làm mỗi skill (rút từ các lần đo)

1. **Đo baseline trước khi viết luật.** Nếu không có skill mà agent đã đạt, dừng lại, đừng làm (bài học từ authz, test-integrity, safe-migration).
2. Ca test phải có **code cũ ngược quy ước** hoặc **thông tin thiếu** đặt sẵn trong repo, vì đó là chỗ AI thua thật.
3. Skill phải **tạo ra sản phẩm** kèm **script kiểm**; chỉ "review" thì khó thấy khác biệt.
4. Phần bắt buộc phải đi qua hook hoặc CI. Skill chỉ là hướng dẫn, agent có thể không gọi.

## Nguồn chính (đọc qua tóm tắt, cần mở gốc trước khi trích vào luật)

- BA: HumanEvalComm https://arxiv.org/pdf/2406.00215 · Ambig-SWE https://arxiv.org/html/2502.13069v3 · Ask or Assume (EMNLP 2026) https://aclanthology.org/2026.findings-emnlp.15/ · ClarifyCodeBench https://arxiv.org/html/2607.00711v2 · Thoughtworks `[vendor]` https://www.thoughtworks.com/insights/blog/generative-ai/AI-generated-test-cases-from-user-stories-an-experimental-research-study · Böckeler về spec-driven https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- Frontend: Microsoft a11y-llm-eval `[vendor]` https://microsoft.github.io/a11y-llm-eval-report/index.html · Vercel AGENTS.md vs skills `[vendor]` https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals · WebAIM Million 2026 (tóm tắt) https://prioritypixels.co.uk/insights/web-accessibility-is-getting-worse-according-to-the-2026-webaim-million-report/
- Backend: agent logging study https://www.opentrain.ai/papers/do-ai-coding-agents-log-like-humans-an-empirical-study--arxiv-2604.09409/ · CodeRabbit `[vendor]` https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report · oasdiff https://docs.coderabbit.ai/tools/oasdiff
- QA: Hora & Robbes over-mocking (qua tóm tắt) https://codex.danielvaughan.com/2026/06/30/over-mocked-tests-coding-agents-codex-cli-agents-md-testing-guidance-mock-control/ · Supercov `[vendor]` https://supercov.com/blog/mutation-testing-ai-generated-tests · Leith https://arxiv.org/abs/2608.15188 · Currents `[vendor]` https://currents.dev/posts/reviewing-ai-generated-playwright-tests-before-they-reach-ci
- Pentest/AppSec: SEC-bench https://arxiv.org/abs/2506.11791v2 · PentestEval https://arxiv.org/html/2512.14233v1 · SAST-Genius https://arxiv.org/pdf/2509.15433 · AIShellJack https://arxiv.org/html/2509.22040v1 · curl bounty https://gigazine.net/gsc_news/en/20260123-curl-bug-bounty
- DevOps: Text-to-Terraform security https://arxiv.org/pdf/2608.02672 · Sonar về DPIaC-Eval `[vendor]` https://www.sonarsource.com/blog/ai-is-writing-more-of-your-terraform/ · sự cố agent xoá DB https://incidentdatabase.ai/cite/1424 · Datadog GitHub Actions `[vendor]` https://securitylabs.datadoghq.com/articles/case-for-github-actions-security/ · Trail of Bits agentic actions auditor https://trailofbits.com/skills/agentic-actions-auditor/
- Lead: Faros `[vendor]` https://www.faros.ai/blog/ai-software-engineering · ContextCov https://arxiv.org/html/2603.00822v1 · Evaluating AGENTS.md https://arxiv.org/pdf/2602.11988 · Anthropic về kỹ năng `[vendor]` https://www.anthropic.com/research/AI-assistance-coding-skills
