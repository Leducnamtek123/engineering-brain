def normalize_phone(raw: str) -> str:
    """Normalize a Vietnamese mobile number to E.164 (+84...).

    Accepts spaces, dots and dashes, a leading 0, or an existing +84 / 84 prefix.
    Raises ValueError when the result is not +84 followed by exactly 9 digits.
    """
    raise NotImplementedError
