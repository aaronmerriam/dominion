import unittest

from dominion.core import Supply
from dominion.cards import (  # NOQA
    CardCollection, Treasure, pop_treasures, Copper,
    Silver, Gold, Estate, Duchy, Province, pop_matching_cards,
)


class TestSupply(unittest.TestCase):
    def setUp(self):
        self.supply = Supply()

    def test_affordable_cards(self):
        self.assertIn(Copper, self.supply.affordable_cards(0))
        self.assertNotIn(Silver, self.supply.affordable_cards(0))
        self.assertNotIn(Estate, self.supply.affordable_cards(0))

        self.assertIn(Copper, self.supply.affordable_cards(6))
        self.assertIn(Gold, self.supply.affordable_cards(6))
        self.assertIn(Duchy, self.supply.affordable_cards(6))
        self.assertNotIn(Province, self.supply.affordable_cards(6))
