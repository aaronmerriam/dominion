import logging

from .cards import CardCollection, Province, Copper, Gold, Silver


class BasePlayer(object):
    def __init__(self, game, deck):
        self.game = game
        self.deck = deck
        self.discard = CardCollection()
        self.hand = CardCollection()
        self.refill_hand()

    def victory_point_count(self):
        full_deck = self.hand + self.deck + self.discard
        return sum(card.get_victory_points(full_deck) for card in full_deck)

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

    def refill_hand(self):
        assert not self.hand, 'Cannot refill an non-empty hand'
        self.hand = CardCollection(*(self.draw_card() for i in xrange(5)))

    def do_turn(self):
        self.log(logging.DEBUG, 'Player {0} Hand: T:{1}'.format(
            self.game.get_turn(),
            self.hand.get_treasure_value(),
        ))
        self.log(logging.DEBUG, 'Player {0} Victory Points: V:{1}'.format(
            self.game.get_turn(),
            self.victory_point_count(),
        ))
        self.do_actions()
        self.do_buys()
        self.do_cleanup()
        self.refill_hand()

    def do_actions(self):
        pass

    def do_buys(self):
        pass

    def do_cleanup(self):
        while self.hand:
            self.discard_cards(self.hand.draw_card())


class SimpleBuyStrategy(BasePlayer):
    def do_buys(self):
        if self.hand.get_treasure_value() >= 8:
            self.discard_cards(self.game.buy_card(Province))
        elif self.hand.get_treasure_value() >= 6:
            self.discard_cards(self.game.buy_card(Gold))
        elif self.hand.get_treasure_value() >= 3:
            self.discard_cards(self.game.buy_card(Silver))
        else:
            self.discard_cards(self.game.buy_card(Copper))
