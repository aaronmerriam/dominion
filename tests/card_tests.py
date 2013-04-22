import unittest

from dominion.cards import (  # NOQA
    CardCollection, Treasure, pop_treasures, Copper,
    Silver, Gold, Estate, Duchy, Province, pop_matching_cards,
    Gardens,
)


class TestCards(unittest.TestCase):
    def test_card_equality(self):
        self.assertEqual(Copper(), Copper())


class TestCardCollection(unittest.TestCase):
    def setUp(self):
        self.cards = CardCollection([Copper(), Silver(), Gold(), Gold(), Duchy(), Estate(), Estate(), Copper(), Duchy()])

    def test_total_treasure_value(self):
        self.assertEqual(self.cards.total_treasure_value(), 10)

    def test_add_cards(self):
        self.assertEqual(len(self.cards), 9)

        self.cards.add_cards(Province())
        self.assertEqual(len(self.cards), 10)
        self.assertEqual(Province(), self.cards[9])

        self.cards.add_cards(Duchy(), Duchy())
        self.assertEqual(len(self.cards), 12)

    def test_draw_card(self):
        self.assertEqual(self.cards.draw_card(), Duchy())
        self.assertEqual(self.cards.draw_card(), Copper())
        self.assertEqual(self.cards.draw_card(), Estate())

    def test_pop_card(self):
        self.assertEqual(self.cards.pop_card(7), Copper())
        self.assertEqual(self.cards.pop_card(2), Gold())
        self.assertEqual(self.cards.pop_card(2), Gold())

    def test_in(self):
        self.assertTrue(Copper() in self.cards)
        self.assertFalse(Copper() in CardCollection([Estate(), Estate(), Gold()]))

    def test_pop_function(self):
        duchies = pop_matching_cards(lambda c: c == Duchy(), self.cards)
        self.assertEqual(len(duchies), 2)
        self.assertTrue(all([c == Duchy() for c in duchies]))
        self.assertEqual(len(self.cards), 7)
        self.assertFalse(any([c == Duchy() for c in self.cards]))


class TestGarden(unittest.TestCase):
    def test_victory_point_value(self):
        deck = CardCollection([Gardens()] + [Copper() for i in xrange(8)])  # 9 cards
        self.assertEqual(deck[0].total_victory_point_value(deck), 0)

        deck = CardCollection([Gardens()] + [Copper() for i in xrange(9)])  # 10 cards
        self.assertEqual(deck[0].total_victory_point_value(deck), 1)
        deck = CardCollection([Gardens()] + [Copper() for i in xrange(10)])  # 11 cards
        self.assertEqual(deck[0].total_victory_point_value(deck), 1)

        deck = CardCollection([Gardens()] + [Copper() for i in xrange(18)])  # 19 cards
        self.assertEqual(deck[0].total_victory_point_value(deck), 1)

        deck = CardCollection([Gardens()] + [Copper() for i in xrange(34)])  # 35 cards
        self.assertEqual(deck[0].total_victory_point_value(deck), 3)
