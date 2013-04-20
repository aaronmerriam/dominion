import logging
from random import randint, shuffle

from .cards import CardCollection, Province, Copper, Gold, Silver, pop_treasures, pop_actions


class BasePlayer(object):
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


class SimpleBuyStrategy(BasePlayer):
    def do_turn(self):
        treasures = pop_treasures(self.turn.hand)
        self.turn.spend_treasures(*treasures)

        to_buy = None
        if treasures.total_treasure_value() >= 8:
            to_buy = Province
        elif treasures.total_treasure_value() >= 6:
            to_buy = Gold
        elif treasures.total_treasure_value() >= 3:
            to_buy = Silver
        else:
            to_buy = Copper

        if to_buy is not None:
            self.turn.buy_card(to_buy)


def do_nothing(choices, nothing_weight=1):
    """
    Helper functions for randomly picking to do nothing during a turn.
    """
    return randint(0, len(choices) + nothing_weight) > len(choices)


class RandomActionStrategy(BasePlayer):
    def do_turn(self):
        self.do_actions()
        self.do_buys()

    def do_actions(self):
        actions = pop_actions(self.turn.hand)

        while self.turn.available_actions and actions:
            if do_nothing(actions):
                break
            self.turn.play_action(actions.draw_card())
        self.turn.discard_cards(*actions)

    def do_buys(self):
        treasures = pop_treasures(self.turn.hand)
        self.turn.spend_treasures(*treasures)

        while self.turn.available_buys:
            affordable_cards = self.game.supply.affordable_cards(self.turn.available_treasure)
            shuffle(affordable_cards)
            if not affordable_cards or do_nothing(affordable_cards):
                break
            self.turn.buy_card(affordable_cards.pop())
