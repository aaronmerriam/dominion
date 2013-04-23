import operator
from functools import partial
from itertools import chain
from random import choice, normalvariate, getrandbits, shuffle
from pprint import pprint

from dominion.cards import Province, Gold, Silver, Smithy, Laboratory, Duchy, Estate

from .base import BaseBot

"""
Commands
- set of evaluatable conditions
- single action
"""


def command(condition, action, **kwargs):
    """
    This is the base function for executing a logical operation.  Typical usage
    is to partial this with a condition and action and then allow the bot to
    call it with `**kwargs`.
    """
    if condition(**kwargs):
        return action(**kwargs)
    return True


def operator_condition(operation, conditions, **kwargs):
    """
    Joins a set of conditions into a single condition with an operator like
    AND/OR etc.  See the python operator library for more details.
    """
    return reduce(
        operation,
        map(operator.truth, (condition(**kwargs) for condition in conditions)),
    )

and_conditions = partial(operator_condition, operator.and_)
or_conditions = partial(operator_condition, operator.or_)


def negate_conditional(condition, **kwargs):
    """
    negates a condition.
    """
    def not_condition(**kwargs):
        return not condition(**kwargs)
    return not_condition


def card_in_hand(card, turn, **kwargs):
    return card in turn.hand


def has_action(turn, **kwargs):
    return turn.available_actions


def has_buy(turn, **kwargs):
    return turn.available_buys


def play_card(card, turn, **kwargs):
    turn.play_action(turn.hand.index_of_card(card))


def card_in_deck(card, turn, player, **kwargs):
    return compare_number_of_card_in_deck(card, operator.gt, 0, **kwargs)


def compare_number_of_card_in_deck(card, op, count, turn, player, **kwargs):
    card_count = sum(isinstance(c, card) for c in chain(turn.hand, turn.discard, player.deck, player.discard))
    return op(card_count, count)


def can_afford_card(card, turn, **kwargs):
    return card.cost <= turn.available_treasure + turn.hand.total_treasure_value()


def card_is_purchasable(card, game, **kwargs):
    return card in game.supply and game.supply.cards[card]


def purchase_card(card, turn, **kwargs):
    turn.buy_card(card)


def buy_card_command(card, *extra_conditions):
    """
    Given a card class, this will construct a command executable that will
    purchase the card if it is both affordable and available for purchase.
    """
    conditions = list(chain([
        has_buy,
        partial(can_afford_card, card),
        partial(card_is_purchasable, card),
    ], extra_conditions))
    return partial(
        command,
        partial(and_conditions, conditions),
        partial(purchase_card, card),
    )


def play_card_command(card, *extra_conditions):
    conditions = list(chain([
        has_action,
        partial(card_in_hand, card),
    ], extra_conditions))
    return partial(
        command,
        partial(and_conditions, conditions),
        partial(play_card, card),
    )


def buy_n_of_card_command(card, n, *extra_conditions):
    conditions = list(chain([
        has_buy,
        partial(can_afford_card, Smithy),
        partial(card_is_purchasable, Smithy),
        partial(compare_number_of_card_in_deck, Smithy, operator.lt, n),
    ], extra_conditions))
    return partial(
        command,
        partial(and_conditions, conditions),
        partial(purchase_card, Smithy),
    )


class BaseLogicBot(BaseBot):
    buy_commands = []
    action_commands = []

    def do_turn(self):
        self.do_actions()
        self.do_buys()

    def get_command_kwargs(self, **kwargs):
        defaults = {
            'turn': self.turn,
            'game': self.turn.game,
            'player': self,
        }
        defaults.update(kwargs)
        return defaults

    def do_actions(self):
        for command in self.action_commands:
            if command(**self.get_command_kwargs()) is False:
                break
            continue

    def do_buys(self):
        self.turn.spend_all_treasures()
        for command in self.buy_commands:
            if command(**self.get_command_kwargs()) is False:
                break
            continue


class MoneyLogicBot(BaseLogicBot):
    buy_commands = (
        buy_card_command(Province),
        buy_card_command(Gold),
        buy_card_command(Silver),
    )


class SmithyLogicBot(BaseLogicBot):
    action_commands = (
        play_card_command(Smithy),
    )
    buy_commands = (
        buy_n_of_card_command(Smithy, 1),
        buy_card_command(Province),
        buy_card_command(Gold),
        buy_card_command(Silver),
    )


class SmithyLabLogicBot(BaseLogicBot):
    action_commands = (
        play_card_command(Laboratory),
        play_card_command(Smithy),
    )
    buy_commands = (
        buy_n_of_card_command(Smithy, 1),
        buy_card_command(Province),
        buy_card_command(Gold),
        buy_n_of_card_command(Laboratory, 2),
        buy_card_command(Silver),
    )


class RandomLogicBot(BaseLogicBot):
    def __init__(self, *args, **kwargs):
        super(RandomLogicBot, self).__init__(*args, **kwargs)
        self.signature = {
            'actions': [],
            'buys': [
                Gold,
                Silver,
                Province,
            ],
        }
        for i in range(int(abs(normalvariate(0, 1.2)) + 2)):
            card = choice(self.game.supply.action_cards)
            count = int(abs(normalvariate(0, 1.1))) + 1
            self.signature['buys'].append((card, count))
            if card.is_action:
                self.signature['actions'].append(card)
        if getrandbits(1):
            self.signature['buys'].append(Duchy)
        if getrandbits(1):
            self.signature['buys'].append(Estate)
        shuffle(self.signature['actions'])
        def sort_buy(buy):
            if isinstance(buy, type):
                return -1 * buy.cost
            else:
                return -1 * buy[0].cost
        self.signature['buys'].sort(key=sort_buy)
        for buy in self.signature['buys']:
            if isinstance(buy, type):
                self.buy_commands.append(buy_card_command(buy))
            else:
                self.buy_commands.append(buy_n_of_card_command(*buy))
        for action in self.signature['actions']:
            self.action_commands.append(play_card_command(action))
