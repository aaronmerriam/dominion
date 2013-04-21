import logging
from random import randint

from dominion.cards import CardCollection


class BaseBot(object):
    def __init__(self, game, deck):
        self.game = game
        self.deck = deck
        self.discard = CardCollection()

    def victory_point_count(self):
        full_deck = self.turn.hand + self.deck + self.discard
        return sum(card.total_victory_point_value(full_deck) for card in full_deck)

    def log(self, level, message):
        self.game.log(level, message)

    def draw_card(self):
        if not self.deck:
            self.log(logging.DEBUG, 'Player {0} Reshuffling'.format(self.game.get_turn()))
            self.discard.shuffle()
            self.deck, self.discard = self.discard, self.deck
        return self.deck.draw_card()

    def discard_cards(self, *cards):
        assert all(cards)
        self.discard.add_cards(*cards)

    def set_turn(self, turn):
        self.turn = turn

    def do_turn(self):
        pass

    def cleanup_turn(self):
        self.discard_cards(*[c for c in self.turn.hand])
        self.discard_cards(*[c for c in self.turn.discard])

    def self_discard(self, cards, num_discard, is_attack=True):
        for i in xrange(num_discard):
            cards.draw_card()


def do_nothing(choices, nothing_weight=1):
    """
    Helper functions for randomly picking to do nothing during a turn.
    """
    return randint(0, len(choices) + nothing_weight) > len(choices)
