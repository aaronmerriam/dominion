import unittest

from dominion.core import Supply
from dominion.cards import (  # NOQA
    BASE_SUPPLY_CARDS, Copper, Silver, Gold, Estate, Duchy, Province
)


class TestSupply(unittest.TestCase):
    def setUp(self):
        self.supply = Supply(BASE_SUPPLY_CARDS, [])

    def test_affordable_cards(self):
        self.assertIn(Copper, self.supply.affordable_cards(0))
        self.assertNotIn(Silver, self.supply.affordable_cards(0))
        self.assertNotIn(Estate, self.supply.affordable_cards(0))

        self.assertIn(Copper, self.supply.affordable_cards(6))
        self.assertIn(Gold, self.supply.affordable_cards(6))
        self.assertIn(Duchy, self.supply.affordable_cards(6))
        self.assertNotIn(Province, self.supply.affordable_cards(6))
