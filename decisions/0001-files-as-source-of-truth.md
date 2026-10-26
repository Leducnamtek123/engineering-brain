# 0001. File markdown trong git là gốc sự thật

- Ngày: 2026-10-26
- Trạng thái: accepted

## Bối cảnh
Cần một bộ kiến thức dùng lâu dài cho người và AI agent, không mất khi đổi model hay đổi agent. Đã cân nhắc các lớp memory như mem0/OpenMemory, basic-memory, Graphiti/Zep và Letta.

## Quyết định
- Kiến thức, skill, eval, bài học đều là file markdown trong repo git này.
- Dùng chuẩn mở: `AGENTS.md`, Agent Skills (`SKILL.md`), MCP.
- Memory hoặc vector store chỉ được thêm làm **index**. Ưu tiên basic-memory (đọc thẳng markdown). mem0 hoặc Graphiti chỉ thêm khi có nhu cầu đo được.

## Lý do
- Đổi agent chỉ cần agent đó đọc được `AGENTS.md` và `SKILL.md`.
- Git cho lịch sử, review và rollback miễn phí.
- Không phải vận hành DB và không cần API key chỉ để giữ kiến thức.

## Hệ quả
- Khi kho lớn, tìm bằng grep sẽ chậm. Lúc đó mới thêm index.
- Trạng thái của OpenMemory MCP chưa rõ (có nguồn nói đã deprecated), cần kiểm tra lại trước khi dùng.
