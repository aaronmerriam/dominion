import unittest

from dominion.core import Game
from dominion.bots import BasePlayer
from dominion.cards import (  # NOQA
    CardCollection, Treasure, pop_treasures, Copper,
    Silver, Gold, Estate, Duchy, Province, pop_matching_cards,
)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game((BasePlayer, BasePlayer))
        self.game.initialize_game()

    def test_manual_round_progress(self):
        for i in range(10):
            round = self.game.get_round()
            self.game.process_round()
            self.assertEqual(round + 1, self.game.get_round())

    def test_get_current_player(self):
        for i in range(len(self.game.players)):
            self.game.turn = i
            self.assertEqual(self.game.players[i], self.game.get_current_player())

    def test_get_other_players(self):
        for i in range(len(self.game.players)):
            self.game.turn = i
            self.assertNotIn(self.game.players[i], self.game.get_other_players())
