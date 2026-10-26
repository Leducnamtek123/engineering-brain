import unittest

from pricing import total


class TotalTest(unittest.TestCase):
    def test_no_voucher(self):
        self.assertEqual(total([{"unit_price": 200_000, "qty": 2}]), 440_000)

    def test_percent_voucher(self):
        self.assertEqual(total([{"unit_price": 200_000, "qty": 2}], {"type": "percent", "value": 10}), 396_000)

    def test_fixed_voucher(self):
        self.assertEqual(total([{"unit_price": 200_000, "qty": 2}], {"type": "fixed", "value": 50_000}), 385_000)


if __name__ == "__main__":
    unittest.main()
