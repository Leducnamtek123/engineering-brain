---
id: backend-authz-review-002
skill: backend-authz-review
rules: [A1, A2]
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
- MUST NOT flag `getOne` là lỗi: truy vấn đã ràng buộc theo `ownerId`, trả 404 khi không phải chủ.
- SHOULD note ở mức "chưa kiểm chứng" hoặc Low (A2): không thấy strategy nên chưa chắc `req.user.id` có giá trị. Nếu là `undefined`, Prisma bỏ điều kiện `ownerId`. Ghi như vậy thì tính là **trúng ghi chú**. Báo thành lỗi Medium/High thì tính là **báo sai**, vì code không cho thấy giá trị có thể rỗng.
- MUST NOT flag `plans`: dữ liệu công khai.
- Chấp nhận được: gợi ý thêm test cho trường hợp user khác (không tính là báo sai nếu ghi rõ là gợi ý, không phải lỗi).

## Notes
Ca dùng để đo báo sai. Skill quá nhạy sẽ báo lỗi ở đây.
Sửa 2026-10-26: bản đầu coi `getOne` an toàn tuyệt đối. Baseline chỉ ra bẫy Prisma `undefined`, nên thêm dòng SHOULD note (xem `lessons/2026-10-26-prisma-undefined-filter.md`).
