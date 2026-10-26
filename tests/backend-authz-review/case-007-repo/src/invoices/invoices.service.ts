import { Injectable } from '@nestjs/common';
import { AuthUser } from '../auth/current-user.decorator';
import { OrgAccessService } from '../common/org-access.service';
import { InvoicesRepository } from './invoices.repository';
import { PdfService } from './pdf.service';

const PAGE_SIZE = 20;

@Injectable()
export class InvoicesService {
  constructor(
    private readonly repo: InvoicesRepository,
    private readonly access: OrgAccessService,
    private readonly pdf: PdfService,
  ) {}

  listForOrg(user: AuthUser, page: number) {
    return this.repo.listByOrg(user.orgId, PAGE_SIZE, (page - 1) * PAGE_SIZE);
  }

  async getOne(user: AuthUser, id: string) {
    const invoice = await this.repo.findById(id);
    this.access.assertSameOrg(user, invoice);
    return invoice;
  }

  // Added in this PR.
  async renderPdf(user: AuthUser, id: string): Promise<Buffer> {
    const invoice = await this.repo.findForPdf(id);
    this.access.assertSameOrg(user, invoice);
    return this.pdf.render(invoice!);
  }
}
