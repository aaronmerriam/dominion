def bonus_buys(num_extra, turn, **kwargs):
    turn.buys += num_extra


def bonus_actions(num_extra, turn, **kwargs):
    turn.actions += num_extra


def bonus_treasure(num_extra, turn, **kwargs):
    turn.treasure += num_extra


def bonus_cards(num_extra, player, **kwargs):
    for i in xrange(num_extra):
        player.hand.add_cards(player.draw_card())
