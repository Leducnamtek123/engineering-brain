VAT_RATE = 0.10


def subtotal(items: list[dict]) -> int:
    """Sum of unit_price * qty in VND."""
    return sum(item["unit_price"] * item["qty"] for item in items)


def apply_voucher(amount: int, voucher: dict | None) -> int:
    """Voucher: {"type": "percent", "value": 15} or {"type": "fixed", "value": 50_000}."""
    if not voucher:
        return amount
    if voucher["type"] == "percent":
        return amount - amount * voucher["value"] // 100
    return max(0, amount - voucher["value"])


def total(items: list[dict], voucher: dict | None = None) -> int:
    """Amount the customer pays, VAT included, in VND."""
    amount = apply_voucher(subtotal(items), voucher)
    return round(amount * (1 + VAT_RATE))
