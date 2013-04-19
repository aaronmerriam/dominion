import logging
from random import randint, shuffle

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

    def do_turn(self, turn):
        self.log(logging.DEBUG, 'Player {0} Hand: T:{1}'.format(self.game.get_turn(), self.hand.get_treasure_value(),))
        self.log(logging.DEBUG, 'Player {0} Victory Points: V:{1}'.format(self.game.get_turn(), self.victory_point_count(),))
        self.do_actions(turn)
        self.do_buys(turn)
        self.do_cleanup(turn)
        self.refill_hand()

    def do_actions(self, turn):
        pass

    def do_buys(self, turn):
        pass

    def do_cleanup(self, turn):
        # Cycle all of the cards left in our hand into the discard.
        while self.hand:
            self.discard_cards(self.hand.draw_card())
        # Put all of the played cards in the discard.
        while turn.cards:
            self.discard_cards(turn.cards.draw_card())


class SimpleBuyStrategy(BasePlayer):
    def do_buys(self, turn):
        treasures = CardCollection(*filter(lambda c: c.is_treasure, self.hand.cards))
        self.hand = CardCollection(*filter(lambda c: not c.is_treasure, self.hand.cards))

        to_buy = None
        if treasures.get_treasure_value() >= 8:
            to_buy = Province
        elif treasures.get_treasure_value() >= 6:
            to_buy = Gold
        elif treasures.get_treasure_value() >= 3:
            to_buy = Silver
        else:
            to_buy = Copper

        if to_buy is not None:
            turn.spend_treasure(*treasures)
            turn.buy_card(to_buy)
        else:
            self.hand.add_cards(*treasures)


class RandomActionStrategy(BasePlayer):
    def do_actions(self, turn):
        """
        This is a horrible implementation of this.
        """
        actions = CardCollection(*filter(lambda c: c.is_action, self.hand.cards))
        actions.shuffle()
        self.hand = CardCollection(*filter(lambda c: not c.is_action, self.hand.cards))

        while turn.actions and actions:
            if randint(0, len(actions) + 1) > len(actions):
                break
            turn.play_action(actions.draw_card())
        self.hand.add_cards(*actions)

    def do_buys(self, turn):
        treasures = CardCollection(*filter(lambda c: c.is_treasure, self.hand.cards))
        turn.spend_treasure(*treasures)
        self.hand = CardCollection(*filter(lambda c: not c.is_treasure, self.hand.cards))

        while turn.buys:
            affordable_cards = filter(lambda c: c.cost <= turn.treasure and self.game.supply.cards[c], self.game.supply.cards)
            shuffle(affordable_cards)
            if not affordable_cards or randint(0, len(affordable_cards) + 1) > len(affordable_cards):
                break
            turn.buy_card(affordable_cards.pop())
