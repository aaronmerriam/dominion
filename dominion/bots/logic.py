import operator
from functools import partial

from .cards import Province, Gold, Silver, pop_treasures
from .base import BaseBot

"""
Commands
- set of evaluatable conditions
- single action
- return value:
    - True - 
"""

def command(conditions, action, **kwargs):
    if all(condition(**kwargs) for condition in conditions):
        return action(**kwargs)
    return False

def repeat_command_up_to_n(n, command, **kwargs):
    while command(**kwargs):
        pass
    return True


def operator_condition(operation, conditions, **kwargs):
    return reduce(
        operation,
        map(operator.truth, (condition(**kwargs) for condition in conditions)),
    )

and_conditions = partial(operator_condition, operator.and_)
or_conditions = partial(operator_condition, operator.or_)


def card_in_hand(card, turn, **kwargs):
    return card in turn.hand


def card_in_deck(card, turn, player, **kwargs):
    return any(
        card in turn.hand,
        card in turn.discard,
        card in player.deck,
        card in player.discard,
    )


def can_afford_card(card, turn, **kwargs):
    return card.cost <= turn.available_treasure + turn.hand.total_treasure_value()


can_afford_province = partial(can_afford_card, Province)
can_afford_gold = partial(can_afford_card, Gold)
can_afford_silver = partial(can_afford_card, Silver)


def card_is_purchasable(card, game, **kwargs):
    return card in game.supply and game.supply.cards[card]

province_is_purchasable = partial(card_is_purchasable, Province)
gold_is_purchasable = partial(card_is_purchasable, Gold)
silver_is_purchasable = partial(card_is_purchasable, Silver)


can_purchase_province = partial(and_conditions, [can_afford_province, province_is_purchasable])
can_purchase_gold = partial(and_conditions, [can_afford_gold, gold_is_purchasable])
can_purchase_silver = partial(and_conditions, [can_afford_silver, silver_is_purchasable])


def purchase_card(card, turn, **kwargs):
    treasures = pop_treasures(turn.hand)
    turn.spend_treasures(*treasures)
    turn.buy_card(card)

buy_province = partial(purchase_card, Province)
buy_gold = partial(purchase_card, Gold)
buy_silver = partial(purchase_card, Silver)


class LogicBot(BaseBot):
    def do_turn(self):
        self.do_actions()
        self.do_buys()

    def do_actions(self):
        for command in self.action_commands:
            if command.execute(self.turn):
                continue
            else:
                break

    def do_buys(self):
        for command in self.buy_commands:
            if command.execute(self.turn):
                continue
            else:
                break
