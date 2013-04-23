from dominion.cards import Province, Copper, Gold, Silver
from .base import BaseBot


class SimpleBuyStrategy(BaseBot):
    def do_turn(self):
        self.turn.spend_all_treasures()

        to_buy = None
        if self.turn.available_treasure >= 8:
            to_buy = Province
        elif self.turn.available_treasure >= 6:
            to_buy = Gold
        elif self.turn.available_treasure >= 3:
            to_buy = Silver
        else:
            to_buy = Copper

        if to_buy is not None and self.turn.game.supply.cards[to_buy]:
            self.turn.buy_card(to_buy)
