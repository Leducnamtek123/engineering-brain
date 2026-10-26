import unittest

from vat import vat


class VatTest(unittest.TestCase):
    def test_round_amount(self):
        self.assertEqual(vat(100_000), 10_000)

    def test_rounds_half_up(self):
        self.assertEqual(vat(15), 2)

    def test_rounds_down(self):
        self.assertEqual(vat(14), 1)

    def test_invoice_example(self):
        self.assertEqual(vat(250_000), 25_001)


if __name__ == "__main__":
    unittest.main()
