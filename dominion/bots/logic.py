import operator
from functools import partial

from dominion.cards import Province, Gold, Silver, pop_treasures, Smithy

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


def play_card(card, turn, **kwargs):
    for i in xrange(len(turn.hand)):
        if isinstance(turn.hand[i], card):
            turn.play_action(turn.hand.pop_card(i))
            break


def play_card_command(card):
    return partial(
        command,
        partial(and_conditions, (
            partial(card_in_hand, card),
            has_action,
        )),
        partial(play_card, card),
    )


def card_in_deck(card, turn, player, **kwargs):
    return any((
        card in turn.hand,
        card in turn.discard,
        card in player.deck,
        card in player.discard,
    ))


def can_afford_card(card, turn, **kwargs):
    return card.cost <= turn.available_treasure + turn.hand.total_treasure_value()


def card_is_purchasable(card, game, **kwargs):
    return card in game.supply and game.supply.cards[card]


def purchase_card(card, turn, **kwargs):
    treasures = pop_treasures(turn.hand)
    turn.spend_treasures(*treasures)
    turn.buy_card(card)


def buy_card_command(card):
    """
    Given a card class, this will construct a command executable that will
    purchase the card if it is both affordable and available for purchase.
    """
    return partial(
        command,
        partial(and_conditions, (
            partial(can_afford_card, card),
            partial(card_is_purchasable, card),
        )),
        partial(purchase_card, card),
    )


buy_1_smithy = partial(
    command,
    partial(and_conditions, (
        partial(can_afford_card, Smithy),
        partial(card_is_purchasable, Smithy),
        partial(not_conditional, partial(card_in_deck, Smithy)),
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
            if command(**self.get_command_kwargs()):
                continue
            break

    def do_buys(self):
        for command in self.buy_commands:
            if command(**self.get_command_kwargs()):
                continue
            break


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
        buy_1_smithy,
        buy_card_command(Province),
        buy_card_command(Gold),
        buy_card_command(Silver),
    )
