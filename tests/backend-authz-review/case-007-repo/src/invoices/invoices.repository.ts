import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma.service';

@Injectable()
export class InvoicesRepository {
  constructor(private readonly prisma: PrismaService) {}

  listByOrg(orgId: string, take: number, skip: number) {
    return this.prisma.invoice.findMany({
      where: { orgId },
      orderBy: { issuedAt: 'desc' },
      take,
      skip,
    });
  }

  findById(id: string) {
    return this.prisma.invoice.findUnique({ where: { id }, include: { lines: true } });
  }

  // Added in this PR. Only load what the PDF template needs; invoices can have hundreds of lines.
  findForPdf(id: string) {
    return this.prisma.invoice.findUnique({
      where: { id },
      select: {
        id: true,
        number: true,
        currency: true,
        issuedAt: true,
        customerName: true,
        lines: { select: { description: true, quantity: true, unitPriceMinor: true } },
      },
    });
  }
}
