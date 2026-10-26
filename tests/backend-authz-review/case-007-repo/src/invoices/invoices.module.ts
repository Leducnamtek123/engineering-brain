import { Module } from '@nestjs/common';
import { InvoicesController } from './invoices.controller';
import { InvoicesService } from './invoices.service';
import { InvoicesRepository } from './invoices.repository';
import { PdfService } from './pdf.service';
import { OrgAccessService } from '../common/org-access.service';
import { PrismaService } from '../prisma.service';

@Module({
  controllers: [InvoicesController],
  providers: [InvoicesService, InvoicesRepository, PdfService, OrgAccessService, PrismaService],
})
export class InvoicesModule {}
