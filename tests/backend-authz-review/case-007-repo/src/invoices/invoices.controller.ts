import { Controller, Get, Header, Param, Query, StreamableFile, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { CurrentUser, AuthUser } from '../auth/current-user.decorator';
import { InvoicesService } from './invoices.service';

@Controller('invoices')
@UseGuards(AuthGuard('jwt'))
export class InvoicesController {
  constructor(private readonly invoices: InvoicesService) {}

  @Get()
  list(@CurrentUser() user: AuthUser, @Query('page') page = '1') {
    return this.invoices.listForOrg(user, Math.max(1, Number(page) || 1));
  }

  @Get(':id')
  getOne(@CurrentUser() user: AuthUser, @Param('id') id: string) {
    return this.invoices.getOne(user, id);
  }

  // Added in this PR: download an invoice as PDF.
  @Get(':id/pdf')
  @Header('Content-Type', 'application/pdf')
  async getPdf(@CurrentUser() user: AuthUser, @Param('id') id: string) {
    const buffer = await this.invoices.renderPdf(user, id);
    return new StreamableFile(buffer);
  }
}
