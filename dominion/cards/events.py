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
    turn.hand.add_cards(*player.draw_cards(num_extra))

extra_1_cards = partial(extra_cards, 1)
extra_2_cards = partial(extra_cards, 2)
extra_3_cards = partial(extra_cards, 3)


def discard_to(discard_to, turn, other_players, card=BaseCard(), **kwargs):
    for player in other_players:
        discard_kwargs = {
            'is_attack': card.is_attack,
            'is_own_cards': player.turn == turn,
        }
        num_discard = max(0, len(player.turn.hand) - discard_to)
        player.select_for_discard(player.turn.hand, num_discard, **discard_kwargs)

others_discard_to_3 = partial(discard_to, 3)


def draw_x_discard_y(x, y, turn, player, card, **kwargs):
    discard_kwargs = {
        'is_attack': card.is_attack,
        'is_own_cards': player.turn == turn,
    }
    cards = CardCollection(player.draw_cards(x))
    player.select_for_discard(cards, y, **discard_kwargs)
    turn.hand.add_cards(*cards)

draw_4_discard_1 = partial(draw_x_discard_y, 4, 1)


def free_buy_up_to_x(x, turn, player, **kwargs):
    affordable_cards = turn.game.supply.affordable_cards(x)
    # `card` is a card class
    cards = player.select_to_add_to_deck(affordable_cards, x)
    for card in cards:
        turn.discard_cards(turn.game.supply.draw_card(card))

free_buy_up_to_4 = partial(free_buy_up_to_x, 4)
