import unittest

from shipping import shipping_fee


class ShippingFeeTest(unittest.TestCase):
    def test_small_order_pays_fee(self):
        self.assertEqual(shipping_fee(100_000), 30_000)

    def test_large_order_is_free(self):
        self.assertEqual(shipping_fee(800_000), 0)

    def test_threshold(self):
        self.assertEqual(shipping_fee(500_000), 30_000)


if __name__ == "__main__":
    unittest.main()
