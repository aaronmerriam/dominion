from random import shuffle

from .cards import pop_treasures, pop_actions

from .base import BaseBot, do_nothing


class Condition(object):
    actions = []

    def __init__(self, turn, player, **kwargs):
        self.turn = turn
        self.game = turn.game
        self.player = player

    def __nonzero__(self):
        return self.eval(self.get_eval_kwargs())

    def __call__(self):
        return self.execute()

    def get_eval_kwargs(self, **kwargs):
        defaults = {
            'turn': self.turn,
            'game': self.game,
            'player': self.player,
        }
        defaults.update(kwargs)
        return defaults

    def eval(self, **kwargs):
        raise NotImplementedError('Must implement this in subclasses')

    def execute(self):
        pass


class CardInHandCondition(Condition):
    def __init__(self, card, **kwargs):
        self.card = card

    def eval(self, turn):
        return self.card in turn.hand


def buy_card(card, turn, **kwargs):
    # check card is in supply.
    # check can afford card.
    # spend treasures.
    # buy card.
    pass


def play_action(card, turn, **kwargs):
    # 
    pass


class LogicBot(BaseBot):
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
