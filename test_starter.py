"""Автоматические тесты для recommend_price. Запуск: python -m unittest -v"""

import asyncio
import unittest
from decimal import Decimal

from starter import recommend_price, sample_fetch_offers


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_basic_calculation(self):
        result = await recommend_price(
            sample_fetch_offers,
            current_price=Decimal("4900.00"),
            min_price=Decimal("4500.00"),
        )
        self.assertEqual(result["price"], Decimal("4728.00"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_timeout_keeps_current_price(self):
        async def slow_fetch():
            await asyncio.sleep(0.1)
            return {"status": "success", "offers": []}

        result = await recommend_price(
            slow_fetch,
            current_price=Decimal("4000.00"),
            min_price=Decimal("4500.00"),
            timeout_s=0.01,
        )
        self.assertEqual(result["price"], Decimal("4000.00"))
        self.assertEqual(result["decision"], "HOLD")

    async def test_exactly_30_percent_is_allowed(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "OTHER", "price": Decimal("71.07"), "delivery_days": 2}
                ],
            }

        result = await recommend_price(
            fetch_offers,
            current_price=Decimal("100.00"),
            min_price=Decimal("1.00"),
        )
        self.assertEqual(result["price"], Decimal("70.00"))
        self.assertEqual(result["decision"], "APPLY")


if __name__ == "__main__":
    unittest.main()
