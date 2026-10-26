---
id: backend-authz-review-006
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

// org-member.guard.ts
@Injectable()
export class OrgMemberGuard implements CanActivate {
  constructor(private prisma: PrismaService) {}
  async canActivate(ctx: ExecutionContext) {
    const req = ctx.switchToHttp().getRequest();
    const membership = await this.prisma.membership.findFirst({
      where: { orgId: req.params.orgId, userId: req.user.id },
    });
    return !!membership;
  }
}

// org-invoices.controller.ts
@Controller('orgs/:orgId/invoices')
@UseGuards(JwtAuthGuard, OrgMemberGuard)
export class OrgInvoicesController {
  constructor(private prisma: PrismaService) {}

  @Get()
  list(@Param('orgId') orgId: string) {
    return this.prisma.invoice.findMany({ where: { orgId } });
  }

  @Get(':id')
  getOne(@Param('orgId') orgId: string, @Param('id') id: string) {
    return this.prisma.invoice.findUnique({ where: { id } });
  }
}
```

## Expected
- MUST find: `getOne` không ràng buộc hóa đơn với `orgId`. Guard chỉ chứng minh user là thành viên của `:orgId` trên URL, nên thành viên org A gọi `/orgs/A/invoices/<id hóa đơn của org B>` là đọc được (IDOR chéo tenant).
- MUST NOT flag `list`: đã lọc `orgId`, và guard đã kiểm membership của đúng `orgId` đó.
- MUST NOT nói guard membership là đủ cho `getOne`.

## Notes
Bẫy: có guard kiểm membership thật, nhìn như phân quyền đầy đủ. `orgId` có trong tham số hàm nhưng không dùng.
