from random import shuffle

from .base import BaseBot, do_nothing


class RandomActionStrategy(BaseBot):
    def do_turn(self):
        self.do_actions()
        self.do_buys()

    def do_actions(self):
        actions = [i for i, card in enumerate(self.turn.hand) if card.is_action]

        while self.turn.available_actions and actions:
            if do_nothing(actions):
                break
            self.turn.play_action(actions.pop())

    def do_buys(self):
        self.turn.spend_all_treasures()

        while self.turn.available_buys:
            affordable_cards = self.game.supply.affordable_cards(self.turn.available_treasure)
            shuffle(affordable_cards)
            if not affordable_cards or do_nothing(affordable_cards):
                break
            self.turn.buy_card(affordable_cards.pop())
