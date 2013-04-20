from functools import partial


def extra_buys(num_extra, turn, **kwargs):
    turn.available_buys += num_extra

extra_1_buys = partial(extra_buys, 1)
extra_2_buys = partial(extra_buys, 2)
extra_3_buys = partial(extra_buys, 3)


def extra_actions(num_extra, turn, **kwargs):
    turn.available_actions += num_extra

extra_1_actions = partial(extra_actions, 1)
extra_2_actions = partial(extra_actions, 2)
extra_3_actions = partial(extra_actions, 3)


def extra_treasure(num_extra, turn, **kwargs):
    turn.available_treasure += num_extra

extra_1_treasures = partial(extra_treasure, 1)
extra_2_treasures = partial(extra_treasure, 2)
extra_3_treasures = partial(extra_treasure, 3)


def extra_cards(num_extra, turn, player, **kwargs):
    turn.hand.add_cards(*(player.draw_card() for i in xrange(num_extra)))

extra_1_cards = partial(extra_cards, 1)
extra_2_cards = partial(extra_cards, 2)
extra_3_cards = partial(extra_cards, 3)
