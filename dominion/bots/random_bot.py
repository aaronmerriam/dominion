from random import shuffle

from dominion.cards import pop_treasures, pop_actions

from .base import BaseBot, do_nothing


class RandomActionStrategy(BaseBot):
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
