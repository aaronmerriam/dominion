from dominion.cards import Province, Copper, Gold, Silver, pop_treasures
from .base import BaseBot


class SimpleBuyStrategy(BaseBot):
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
