---
id: backend-authz-review-005
skill: backend-authz-review
rules: [A1]
kind: positive
source: tu-viet
---

## Input

```text
Review this NestJS controller for access-control issues.

// jwt.strategy.ts
async validate(payload: { sub: string }) {
  return { id: payload.sub };
}

// invoices.controller.ts
@Controller('invoices')
@UseGuards(JwtAuthGuard)
export class InvoicesController {
  constructor(private prisma: PrismaService) {}

  @Delete(':id')
  async remove(@Param('id') id: string, @Req() req) {
    const invoice = await this.prisma.invoice.findUnique({ where: { id } });
    if (!invoice || invoice.ownerId !== req.user.id) throw new NotFoundException();
    return this.prisma.invoice.delete({ where: { id } });
  }

  @Patch(':id/status')
  async setStatus(@Param('id') id: string, @Body() body: { status: InvoiceStatus }, @Req() req) {
    await this.prisma.invoice.updateMany({
      where: { id, ownerId: req.user.id },
      data: { status: body.status },
    });
    return this.prisma.invoice.findUnique({ where: { id } });
  }
}
```

## Expected
- MUST find: `setStatus` cập nhật có lọc `ownerId` (đúng), nhưng sau đó trả `findUnique({ where: { id } })` **không lọc** → gọi với id của người khác thì update khớp 0 dòng nhưng vẫn đọc và trả về hóa đơn của họ (IDOR đọc).
- MUST NOT flag `remove` là IDOR: tải rồi so `ownerId` với user từ token, trả 404 khi không phải chủ. Gợi ý gộp điều kiện vào câu xoá (tránh race) là chấp nhận được nếu ghi ở mức Low hoặc ghi chú.

## Notes
Bẫy: phần ghi đã đúng nên người review dễ dừng lại; lỗi nằm ở dòng trả về.
