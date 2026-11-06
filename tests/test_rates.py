import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    def test_explicit_standard_matches_default(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 2, 3.141):
                with self.subTest(zone=zone, weight=weight):
                    self.assertEqual(
                        shipping_quote(weight, zone, service="standard"),
                        shipping_quote(weight, zone),
                    )

    def test_express_rates(self):
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)
        self.assertEqual(shipping_quote(2, "regional", "express"), 18.0)
        self.assertEqual(shipping_quote(3.141, "local", "express"), 16.71)

    def test_unknown_service(self):
        with self.assertRaisesRegex(ValueError, "unknown service"):
            shipping_quote(2, "local", service="overnight")

    def test_express_invalid_inputs(self):
        for weight in (0, -1):
            with self.subTest(weight=weight):
                with self.assertRaisesRegex(ValueError, "weight must be positive"):
                    shipping_quote(weight, "local", "express")
        with self.assertRaisesRegex(ValueError, "unknown zone"):
            shipping_quote(2, "unknown", "express")
