from functools import partial

from .base import BaseCard, CardCollection


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


def discard_to(discard_to, turn, others, card=BaseCard(), **kwargs):
    # TODO: automatic detection of discarding own, or other persons cards.
    for player in others:
        num_discard = max(0, len(player.turn.hand) - discard_to)
        player.self_discard(player.turn.hand, num_discard, is_attack=card.is_attack)

discard_to_3 = partial(discard_to, 3)


def draw_x_discard_y(x, y, turn, player, **kwargs):
    # TODO: automatic detection of discarding own, or other persons cards.
    cards = CardCollection([player.draw_card() for i in xrange(x)])
    player.self_discard(cards, y)
    turn.hand.add_cards(cards)

draw_4_discard_1 = partial(draw_x_discard_y, 4, 1)
