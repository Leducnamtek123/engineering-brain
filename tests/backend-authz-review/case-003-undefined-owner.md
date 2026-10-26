---
id: backend-authz-review-003
skill: backend-authz-review
rules: [A1, A2]
kind: positive
source: tu-viet
---

## Input

```text
Review this NestJS code for access-control issues.

// jwt.strategy.ts
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({ jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(), secretOrKey: process.env.JWT_SECRET });
  }
  async validate(payload: { sub: string; email: string }) {
    return { sub: payload.sub, email: payload.email };
  }
}

// invoices.controller.ts
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

  @Get()
  async list(@Req() req) {
    return this.prisma.invoice.findMany({ where: { ownerId: req.user.sub } });
  }
}
```

## Expected
- MUST find (A2): `validate()` trả `{ sub, email }`, không có `id`, nên `req.user.id` là `undefined`. Prisma bỏ qua điều kiện `ownerId: undefined`, nên `getOne` trả hóa đơn của bất kỳ ai (IDOR). Mức High trở lên.
- MUST NOT flag `list`: dùng `req.user.sub`, khớp với strategy.
- MUST NOT nói `getOne` an toàn chỉ vì "đã lọc theo `ownerId`".

## Notes
Bẫy: nhìn lướt thì `getOne` trông giống hệt bản an toàn ở ca 002. Phải đối chiếu strategy mới thấy lỗi.
