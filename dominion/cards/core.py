from __future__ import division

from .base import Treasure, Action, Victory, Attack, Reaction, pop_points

from .events import (  # NOQA
    extra_1_buys, extra_2_buys, extra_3_buys,
    extra_1_actions, extra_2_actions, extra_3_actions,
    extra_1_treasures, extra_2_treasures, extra_3_treasures,
    extra_1_cards, extra_2_cards, extra_3_cards,
    others_discard_to_3, draw_4_discard_1, free_buy_up_to_4,
)


class Copper(Treasure):
    cost = 0
    treasure_value = 1


class Silver(Treasure):
    cost = 3
    treasure_value = 2


class Gold(Treasure):
    cost = 6
    treasure_value = 3


class Estate(Victory):
    cost = 2
    victory_points = 1


class Duchy(Victory):
    cost = 5
    victory_points = 2


class Province(Victory):
    cost = 8
    victory_points = 3


class Market(Action):
    cost = 5
    events = (
        extra_1_cards,
        extra_1_actions,
        extra_1_buys,
        extra_1_treasures,
    )


class Militia(Action, Attack):
    cost = 4
    events = (
        others_discard_to_3,
        extra_2_treasures,
    )


class Envoy(Action):
    cost = 4
    events = (
        draw_4_discard_1,
    )


class Moat(Action, Reaction):
    cost = 2
    events = (
        extra_2_cards,
    )


class Village(Action):
    cost = 3
    events = (
        extra_1_cards,
        extra_2_actions,
    )


class Woodcutter(Action):
    cost = 3
    events = (
        extra_1_buys,
        extra_2_treasures,
    )


class Workshop(Action):
    cost = 3
    events = (
        free_buy_up_to_4,
    )


class Bureaucrat(Action, Attack):
    cost = 4
    events = (
        'gain_silver_on_deck',
        'force_victory_to_deck',
    )

    def gain_silver_on_deck(self, turn, player, **kwargs):
        if turn.game.supply.cards[Silver]:
            silver = turn.game.supply.cards[Silver].draw_card()
            player.deck.add_cards(silver)

    def force_victory_to_deck(self, other_players, **kwargs):
        for player in other_players:
            victory_cards = pop_points(player.turn.hand)
            if victory_cards:
                cards = player.select_to_return_to_deck(victory_cards, 1, True, True)
                player.deck.add_cards(*cards)


class Gardens(Victory):
    cost = 4

    def total_victory_point_value(self, deck):
        return len(deck) // 10


class Smithy(Action):
    cost = 4
    events = (
        extra_3_cards,
    )


class Festival(Action):
    cost = 5
    events = (
        extra_2_actions,
        extra_1_buys,
        extra_2_treasures,
    )


class Laboratory(Action):
    cost = 5
    events = (
        extra_2_cards,
        extra_1_actions,
    )
