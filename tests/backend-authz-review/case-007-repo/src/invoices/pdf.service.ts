import { Injectable } from '@nestjs/common';
import PDFDocument from 'pdfkit';
import { formatMoney, sumMinor } from '../common/money';

interface PdfInvoice {
  number: string;
  currency: string;
  issuedAt: Date;
  customerName: string;
  lines: { description: string; quantity: number; unitPriceMinor: number }[];
}

@Injectable()
export class PdfService {
  render(invoice: PdfInvoice): Promise<Buffer> {
    return new Promise((resolve, reject) => {
      const doc = new PDFDocument({ size: 'A4', margin: 48 });
      const chunks: Buffer[] = [];
      doc.on('data', (c: Buffer) => chunks.push(c));
      doc.on('end', () => resolve(Buffer.concat(chunks)));
      doc.on('error', reject);

      doc.fontSize(18).text(`Hóa đơn ${invoice.number}`);
      doc.fontSize(10).text(`Khách hàng: ${invoice.customerName}`);
      doc.text(`Ngày: ${invoice.issuedAt.toISOString().slice(0, 10)}`);
      doc.moveDown();
      for (const line of invoice.lines) {
        const amount = formatMoney(line.quantity * line.unitPriceMinor, invoice.currency);
        doc.text(`${line.description}  x${line.quantity}  ${amount}`);
      }
      doc.moveDown().fontSize(12).text(`Tổng: ${formatMoney(sumMinor(invoice.lines), invoice.currency)}`);
      doc.end();
    });
  }
}
