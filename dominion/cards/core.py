from .base import Treasure, Action, Victory, Attack

from .events import (  # NOQA
    extra_1_buys, extra_2_buys, extra_3_buys,
    extra_1_actions, extra_2_actions, extra_3_actions,
    extra_1_treasures, extra_2_treasures, extra_3_treasures,
    extra_1_cards, extra_2_cards, extra_3_cards,
    discard_to_3, draw_4_discard_1
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
        discard_to_3,
        extra_2_treasures,
    )


class Envoy(Action):
    cost = 4
    events = (
        draw_4_discard_1,
    )
