def format_vnd(amount: int) -> str:
    """Format an integer amount of VND for display.

    Rules:
    - Thousands separator is a dot, no decimals: 1234567 -> "1.234.567 ₫".
    - One normal space, then the "₫" sign, after the number.
    - Zero: "0 ₫". Negative numbers keep a leading minus: -50000 -> "-50.000 ₫".
    - Raise TypeError if amount is not an int (bool is not accepted).
    """
    raise NotImplementedError
