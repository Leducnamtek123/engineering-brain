---
id: backend-authz-review-002
skill: backend-authz-review
rules: [A1]
kind: negative
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
  async getOne(@Param('id') id: string, @Req() req) {
    const invoice = await this.prisma.invoice.findFirst({
      where: { id, ownerId: req.user.id },
    });
    if (!invoice) throw new NotFoundException();
    return invoice;
  }

  @Get('public/plans')
  async plans() {
    return this.prisma.plan.findMany({ where: { isPublic: true } });
  }
}
```

## Expected
- MUST NOT flag `getOne`: truy vấn đã ràng buộc theo `ownerId` lấy từ token, trả 404 khi không phải chủ.
- MUST NOT flag `plans`: dữ liệu công khai.
- Chấp nhận được: gợi ý thêm test cho trường hợp user khác (không tính là báo sai nếu ghi rõ là gợi ý, không phải lỗi).

## Notes
Ca dùng để đo báo sai. Skill quá nhạy sẽ báo lỗi ở đây.
