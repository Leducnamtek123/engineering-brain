const formatters = new Map<string, Intl.NumberFormat>();

export function formatMoney(amountMinor: number, currency: string, locale = 'vi-VN'): string {
  const key = `${locale}:${currency}`;
  let fmt = formatters.get(key);
  if (!fmt) {
    fmt = new Intl.NumberFormat(locale, { style: 'currency', currency });
    formatters.set(key, fmt);
  }
  const digits = fmt.resolvedOptions().maximumFractionDigits ?? 2;
  return fmt.format(amountMinor / 10 ** digits);
}

export function sumMinor(lines: { quantity: number; unitPriceMinor: number }[]): number {
  return lines.reduce((total, l) => total + l.quantity * l.unitPriceMinor, 0);
}
