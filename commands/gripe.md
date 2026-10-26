---
description: Ghi lại một điều AI vừa làm bạn khó chịu vào ~/.brain/gripes.md, làm nguồn cho skill sau này
argument-hint: <điều làm bạn khó chịu, một câu>
allowed-tools: Bash(mkdir:*), Read, Write, Edit
---

Người dùng vừa phàn nàn về cách AI làm việc: "$ARGUMENTS"

Thêm **một** mục vào cuối file `~/.brain/gripes.md` (tạo thư mục và file nếu chưa có, file mới bắt đầu bằng dòng `# Gripes`). Không sửa mục cũ.

```markdown
## YYYY-MM-DD · <tên thư mục dự án hiện tại> · <model đang chạy>
- Gripe: <nguyên văn lời người dùng>
- AI đã làm: <1–2 câu, việc cụ thể trong phiên này dẫn tới lời phàn nàn; không rõ thì ghi "không rõ">
- Người dùng muốn: <1 câu, suy từ lời phàn nàn; không chắc thì ghi "chưa rõ">
- Loại: <một trong: bỏ quy ước, báo xong khi chưa kiểm, sửa lan ngoài phạm vi, lặp lỗi cũ, làm quá yêu cầu, không hỏi khi nên hỏi, hỏi khi không cần, khác>
```

Quy tắc:
- Không chép code, đường dẫn tuyệt đối, tên khách hàng, secret, token hay dữ liệu nhạy cảm vào file. Chỉ mô tả hành vi.
- Không tranh luận lời phàn nàn và không xin lỗi dài dòng. Ghi xong thì báo một dòng: đã ghi, loại gì.
- Nếu lời phàn nàn chỉ ra việc cần sửa ngay trong task hiện tại, nói rõ một câu và hỏi người dùng có muốn sửa luôn không.
