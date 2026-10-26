---
id: backend-authz-review-001
skill: backend-authz-review
rules: [A1]
kind: positive
source: tu-viet
---

## Input

```text
Review this NestJS controller for access-control issues.

@Controller('invoices')
@UseGuards(JwtAuthGuard)
export class InvoicesController {
  constructor(private prisma: PrismaService) {}

  @Get(':id')
  async getOne(@Param('id') id: string) {
    return this.prisma.invoice.findUnique({ where: { id } });
  }

  @Get()
  async list(@Req() req) {
    return this.prisma.invoice.findMany({ where: { ownerId: req.user.id } });
  }
}
```

## Expected
- MUST find: `getOne` tải invoice chỉ theo `id`, không ràng buộc `ownerId` với `req.user.id` → user khác đọc được (IDOR).
- MUST NOT flag: `list` (đã lọc theo `req.user.id`).
- MUST NOT say "safe because JwtAuthGuard": guard chỉ xác thực, không phân quyền.

## Notes
Bẫy phổ biến: thấy guard là coi như an toàn.
