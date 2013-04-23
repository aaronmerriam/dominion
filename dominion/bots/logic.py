import operator
from functools import partial
from itertools import chain

from dominion.cards import Province, Gold, Silver, Smithy, Laboratory

from .base import BaseBot

"""
Commands
- set of evaluatable conditions
- single action
"""


def command(condition, action, **kwargs):
    if condition(**kwargs):
        return action(**kwargs)
    return True


def operator_condition(operation, conditions, **kwargs):
    return reduce(
        operation,
        map(operator.truth, (condition(**kwargs) for condition in conditions)),
    )

and_conditions = partial(operator_condition, operator.and_)
or_conditions = partial(operator_condition, operator.or_)


def not_conditional(condition, **kwargs):
    return not condition(**kwargs)


def card_in_hand(card, turn, **kwargs):
    return card in turn.hand


def has_action(turn, **kwargs):
    return turn.available_actions


def has_buy(turn, **kwargs):
    return turn.available_buys


def play_card(card, turn, **kwargs):
    for i in xrange(len(turn.hand)):
        if isinstance(turn.hand[i], card):
            turn.play_action(i)
            break


def card_in_deck(card, turn, player, **kwargs):
    return any((
        card in turn.hand,
        card in turn.discard,
        card in player.deck,
        card in player.discard,
    ))


def compare_number_of_card_in_deck(card, op, count, turn, player, **kwargs):
    card_count = sum(isinstance(c, card) for c in chain(turn.hand, turn.discard, player.deck, player.discard))
    return op(card_count, count)


def can_afford_card(card, turn, **kwargs):
    return card.cost <= turn.available_treasure + turn.hand.total_treasure_value()


def card_is_purchasable(card, game, **kwargs):
    return card in game.supply and game.supply.cards[card]


def purchase_card(card, turn, **kwargs):
    turn.buy_card(card)


def buy_card_command(card):
    """
    Given a card class, this will construct a command executable that will
    purchase the card if it is both affordable and available for purchase.
    """
    return partial(
        command,
        partial(and_conditions, (
            has_buy,
            partial(can_afford_card, card),
            partial(card_is_purchasable, card),
        )),
        partial(purchase_card, card),
    )


def play_card_command(card):
    return partial(
        command,
        partial(and_conditions, (
            has_action,
            partial(card_in_hand, card),
        )),
        partial(play_card, card),
    )


def buy_n_of_card_command(card, n):
    return partial(
        command,
        partial(and_conditions, (
            has_buy,
            partial(can_afford_card, Smithy),
            partial(card_is_purchasable, Smithy),
            partial(compare_number_of_card_in_deck, Smithy, operator.lt, n),
        )),
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
