---
id: backend-authz-review-004
skill: backend-authz-review
rules: [A1]
kind: positive
source: tu-viet
---

## Input

```text
Review this NestJS code for access-control issues.

// jwt.strategy.ts
async validate(payload: { sub: string }) {
  return { id: payload.sub };
}

// invoices.controller.ts
@Controller('invoices')
@UseGuards(JwtAuthGuard)
export class InvoicesController {
  constructor(private invoices: InvoicesService) {}

  @Get(':id')
  getOne(@Param('id') id: string, @Req() req) {
    return this.invoices.findForUser(id, req.user.id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() dto: UpdateInvoiceDto, @Req() req) {
    return this.invoices.update(id, dto);
  }
}

// invoices.service.ts
@Injectable()
export class InvoicesService {
  constructor(private prisma: PrismaService) {}

  async findForUser(id: string, userId: string) {
    const invoice = await this.prisma.invoice.findFirst({ where: { id, ownerId: userId } });
    if (!invoice) throw new NotFoundException();
    return invoice;
  }

  update(id: string, dto: UpdateInvoiceDto) {
    return this.prisma.invoice.update({ where: { id }, data: dto });
  }
}
```

## Expected
- MUST find: `PATCH /invoices/:id` gọi `InvoicesService.update` chỉ theo `id`, không truyền và không kiểm tra user → sửa được hóa đơn của người khác. Controller có `req` nhưng không dùng.
- MUST NOT flag `getOne` / `findForUser`: đã lọc `ownerId`, `validate()` trả `id` nên A2 không áp dụng.

## Notes
Bẫy: kiểm tra quyền nằm ở service, đọc controller không thấy lỗi. Endpoint đọc đúng nên dễ tưởng cả file đúng.
