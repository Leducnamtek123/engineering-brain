import unittest

from phone import normalize_phone


class NormalizePhoneTest(unittest.TestCase):
    def test_leading_zero_with_spaces(self):
        self.assertEqual(normalize_phone("0912 345 678"), "+84912345678")

    def test_dots_and_dashes(self):
        self.assertEqual(normalize_phone("091.234-5678"), "+84912345678")

    def test_existing_country_code(self):
        self.assertEqual(normalize_phone("+84 912 345 678"), "+84912345678")
        self.assertEqual(normalize_phone("84912345678"), "+84912345678")

    def test_rejects_too_short(self):
        with self.assertRaises(ValueError):
            normalize_phone("0912 345")

    def test_rejects_letters(self):
        with self.assertRaises(ValueError):
            normalize_phone("0912abc678")


if __name__ == "__main__":
    unittest.main()
