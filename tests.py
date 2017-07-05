import unittest2 as unittest
from trades import *


class MarketTestCase(unittest.TestCase):
    def setUp(self):
        self.market = Market("I will become a billionaire in five years",
                    [{"title":"yes", "q": 0}, {"title":"no", "q":0}],
                    100)

    def testBuyTen(self):
        print self.market.query_cost("yes", 10)
        print round_up(5.13)
        self.assertTrue(self.market.query_cost("yes", 10)==round_up(5.13))


if __name__ == "__main__":
    unittest.main()
